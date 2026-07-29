/* =====================================================================
   SEHE — Live Departures Worker  (sehe-next-departures)
   ---------------------------------------------------------------------
   Cloudflare Worker that turns Checkfront availability into the JSON the
   tour pages consume. One GET to this Worker returns availability for
   every tour, keyed by departureKey.

   DESIGN (read this — it's why this version is reliable):
   The Worker owns the MASTER SCHEDULE of departures (SCHEDULE below) — the
   full set of dates that should ever appear, sold-out or not. For each
   scheduled date it asks Checkfront one simple question: "is this date
   still bookable?"  A date Checkfront no longer offers is marked
   status:"soldout" — it is NOT dropped. The page keeps showing it, in red.

   This avoids the trap that makes a naive feed unreliable: a sold-out
   fixed-date departure and a date with no departure look identical to a
   plain availability query, so sold-out dates silently vanish. Here the
   schedule is the source of truth for "what exists"; Checkfront only
   answers "is it available", which it does reliably.

   OUTPUT CONTRACT (what the pages expect):
     {
       "14day-2728": {
         "all":  [ { "start":"2027-10-04", "end":"2027-10-17", "status":"available" }, ... ],
         "next": "2027-10-04",            // first AVAILABLE start, or null
         "availableCount": 12, "soldoutCount": 1, "total": 13
       },
       ...
     }
   Dates are plain YYYY-MM-DD. "all" is ascending by start and includes
   BOTH available and sold-out future departures.

   AUTH:
   Defaults to Checkfront's PUBLIC API (no credentials). If Kirsty enables
   token auth instead, add the secrets and it's picked up automatically —
   no code change:
       wrangler secret put CF_API_KEY
       wrangler secret put CF_API_SECRET
   ===================================================================== */

const CHECKFRONT_HOST = 'pounamutourismgroup.checkfront.com';

/* Master schedule. Mirrors the page's RAW fallback. To add a new season,
   add its dates here (and in Checkfront). Selling out is automatic — never
   edit this when a date sells out.
     items:  Checkfront item_id(s). 14-Day carries 302 + 374 (solo split,
             see §3 of the brief): a date is available if EITHER has a seat.
     nights: added to start to compute the return date (end). */
const SCHEDULE = {
  'winter-2026':   { items: [289, 392], nights: 11, dates: ['2026-06-27','2026-07-18','2026-08-01','2026-09-05','2026-09-12'] },  /* 392 = 5 Sep 2026 departure (Kirsty) — available if EITHER item has a seat */
  'winter-2027':   { items: [373], nights: 11, dates: ['2027-07-10','2027-07-24','2027-08-07','2027-08-14','2027-08-21','2027-08-28'] },
  'pinnacle-2027': { items: [315], nights: 15, dates: ['2027-01-14'] },  /* ends 29 Jan 2027 (brochure); was 14 which computed 28 Jan */
  '11day-2627':    { items: [305], nights: 10, dates: ['2026-10-05','2026-11-02','2026-11-30','2027-02-01','2027-02-22','2027-03-01','2027-03-29'] },
  '14day-2627':    { items: [302, 374], nights: 13, dates: ['2026-10-12','2026-10-19','2026-10-26','2026-11-09','2026-11-16','2026-11-23','2027-01-04','2027-01-11','2027-01-18','2027-01-25','2027-02-08','2027-02-15','2027-03-08','2027-03-15','2027-03-22','2027-04-05','2027-04-12'] },
  '11day-2728':    { items: [387], nights: 10, dates: ['2027-09-27','2027-10-25','2027-11-29','2028-01-10','2028-02-28','2028-03-06','2028-04-17'] },
  '14day-2728':    { items: [388], nights: 13, dates: ['2027-10-04','2027-10-11','2027-10-18','2027-11-01','2027-11-08','2027-11-15','2027-11-22','2027-12-06','2028-01-17','2028-01-24','2028-01-31','2028-02-07','2028-02-14','2028-02-21','2028-03-13','2028-03-20','2028-03-27','2028-04-03','2028-04-10'] }
};

const CACHE_SECONDS = 600;            // 10 min — availability isn't second-by-second
let LAST_GOOD = null;                 // in-isolate last successful payload (resilience)

/* ---- NEW-ITEM WATCHDOG --------------------------------------------------
   Kirsty's Feb/Mar bug happened because two departures were created under a
   NEW Checkfront item id the site had never heard of. This watchdog crawls
   the Checkfront item list and flags any item whose name says it is a
   "Sir Edmund Hillary Explorer" product but whose id is not in SCHEDULE —
   the exact failure mode, self-maintaining (no baked ignore-list: Flyer /
   Mountaineer products never match the name test).
     • GET /items-audit             -> JSON report, on demand
     • on each feed rebuild         -> silent check; if NEW_ITEM_ALERT_HOOK
       (a Zapier catch-hook URL secret) is set, POSTs the finding once per
       isolate per distinct set. Failures are swallowed — the watchdog can
       never affect the availability feed. */
const SEHE_ITEM_NAME = /sir\s+edmund\s+hillary\s+explorer/i;

function knownItemIds() {
  const ids = new Set();
  for (const k of Object.keys(SCHEDULE)) for (const id of SCHEDULE[k].items) ids.add(String(id));
  return ids;
}

function filterNewSeheItems(itemsJson, known) {
  const items = (itemsJson && itemsJson.items) || {};
  const found = [];
  for (const id of Object.keys(items)) {
    const it = items[id] || {};
    const name = String(it.name || '');
    if (!SEHE_ITEM_NAME.test(name)) continue;         // not an SEHE product
    if (known.has(String(id))) continue;              // already scheduled
    found.push({ id: String(id), name: name, category_id: it.category_id, status: it.status });
  }
  found.sort((a, b) => Number(a.id) - Number(b.id));
  return found;
}

async function fetchAllItems(env) {
  const headers = { 'Accept': 'application/json' };
  if (env && env.CF_API_KEY && env.CF_API_SECRET) {
    headers['Authorization'] = 'Basic ' + btoa(`${env.CF_API_KEY}:${env.CF_API_SECRET}`);
  }
  const res = await fetch(`https://${CHECKFRONT_HOST}/api/3.0/item`, { headers });
  if (!res.ok) throw new Error(`Checkfront item list -> ${res.status}`);
  return res.json();
}

let NEW_ITEMS_ALERTED_SIG = null;   // per-isolate: alert once per distinct set

async function watchNewItems(env) {
  try {
    const newItems = filterNewSeheItems(await fetchAllItems(env), knownItemIds());
    if (!newItems.length) return newItems;
    const sig = newItems.map((x) => x.id).join(',');
    if (env && env.NEW_ITEM_ALERT_HOOK && sig !== NEW_ITEMS_ALERTED_SIG) {
      NEW_ITEMS_ALERTED_SIG = sig;
      await fetch(env.NEW_ITEM_ALERT_HOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert: 'new_checkfront_items',
          message: 'New Sir Edmund Hillary Explorer item(s) found in Checkfront that the website schedule does not know. Departures sold under these will NOT appear on the site until the worker SCHEDULE and the pages\' booking config include them.',
          new_items: newItems,
          detected: new Date().toISOString()
        })
      }).catch(() => {});
    }
    return newItems;
  } catch (e) { return []; }   // never let the watchdog matter to the feed
}

async function handleItemsAudit(env) {
  const known = knownItemIds();
  let report;
  try {
    const itemsJson = await fetchAllItems(env);
    const items = (itemsJson && itemsJson.items) || {};
    const sehe = Object.keys(items)
      .filter((id) => SEHE_ITEM_NAME.test(String((items[id] || {}).name || '')))
      .map((id) => ({ id: String(id), name: items[id].name, known: known.has(String(id)) }))
      .sort((a, b) => Number(a.id) - Number(b.id));
    report = {
      ok: true,
      knownScheduleIds: Array.from(known).sort((a, b) => Number(a) - Number(b)),
      seheItemsInCheckfront: sehe,
      newItems: sehe.filter((x) => !x.known),
      note: 'newItems non-empty means Checkfront sells SEHE product(s) this site does not know about.'
    };
  } catch (e) {
    report = { ok: false, error: String(e && e.message || e) };
  }
  return new Response(JSON.stringify(report, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...CORS }
  });
}

/* ---- date helpers (all UTC; Checkfront dates are plain calendar dates) -- */
function todayISO() { return new Date().toISOString().slice(0, 10); }
function isoToCompact(iso) { return iso.replace(/-/g, ''); }                 // 2027-10-04 -> 20271004
function compactToIso(c) { return c.slice(0, 4) + '-' + c.slice(4, 6) + '-' + c.slice(6, 8); } // 20271004 -> 2027-10-04
function compact(d) {                                                        // Date -> 20271004
  return d.getUTCFullYear() + String(d.getUTCMonth() + 1).padStart(2, '0') + String(d.getUTCDate()).padStart(2, '0');
}
function addNights(iso, n) {
  const d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

/* ---- Checkfront ---------------------------------------------------------
   Pull the availability calendar for one item across a date window and
   return a Set of available dates as compact 'YYYYMMDD' strings.

   CONFIRMED against a real response (item 388, GET /item/388/cal):
     { ..., "item": { "item_id":388, "cal": { "20271004":1, "20271005":0, ... } } }
   value 1 = available departure, 0 = not.  GOTCHA: Checkfront mixes non-date
   SUMMARY keys into the same cal object ("available":70,"booked":3,"status":"U",
   "span_closed":0,"unit":"D"). The 8-digit-key guard below skips those. The
   other shapes are kept as defensive fallbacks. */
function extractAvailable(json, itemId) {
  const out = new Set();
  if (!json || typeof json !== 'object') return out;
  let cal = null;
  if (json.item && json.item.cal) cal = json.item.cal;                       // confirmed shape
  else if (json.items && json.items[itemId] && json.items[itemId].cal) cal = json.items[itemId].cal;
  else if (json[itemId] && json[itemId].cal) cal = json[itemId].cal;
  else if (json.cal) cal = json.cal;
  if (!cal || typeof cal !== 'object') return out;
  for (const rawKey of Object.keys(cal)) {
    if (!/^\d{8}$/.test(rawKey)) continue;            // date keys only — skip summary keys
    if (isAvailableValue(cal[rawKey])) out.add(rawKey);
  }
  return out;
}
function isAvailableValue(v) {
  if (v === 1 || v === '1' || v === true) return true;
  if (typeof v === 'number') return v > 0;
  if (typeof v === 'string') return /^(a|y|avail)/i.test(v) || parseInt(v, 10) > 0;
  if (v && typeof v === 'object') {
    if (typeof v.available !== 'undefined') return Number(v.available) > 0;
    if (typeof v.status === 'string') return /^(a|y|avail)/i.test(v.status); // 'A' available; 'U'/'S'/'N' not
    if (typeof v.qty !== 'undefined') return Number(v.qty) > 0;
  }
  return false;
}

async function fetchItemAvailable(itemId, startCompact, endCompact, env) {
  const url = `https://${CHECKFRONT_HOST}/api/3.0/item/${itemId}/cal?start_date=${startCompact}&end_date=${endCompact}`;
  const headers = { 'Accept': 'application/json' };
  // Optional token auth — only if the secrets exist (public API needs none).
  if (env && env.CF_API_KEY && env.CF_API_SECRET) {
    headers['Authorization'] = 'Basic ' + btoa(`${env.CF_API_KEY}:${env.CF_API_SECRET}`);
  }
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`Checkfront ${itemId} -> ${res.status}`);
  const json = await res.json();
  return extractAvailable(json, String(itemId));
}

/* ---- per-date stock (for "Filling fast") -------------------------------
   The rated /item/{id}?start_date=D endpoint returns date D's stock at
   json.item.rate.dates[D].stock = { T, B, A } (Total, Booked, Available).
   Only used on the next few bookable departures per tour (cost). */
async function dateStock(itemId, dateC, env) {
  const url = `https://${CHECKFRONT_HOST}/api/3.0/item/${itemId}?start_date=${dateC}&end_date=${dateC}`;
  const headers = { 'Accept': 'application/json' };
  if (env && env.CF_API_KEY && env.CF_API_SECRET) {
    headers['Authorization'] = 'Basic ' + btoa(`${env.CF_API_KEY}:${env.CF_API_SECRET}`);
  }
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`Checkfront item ${itemId} -> ${res.status}`);
  const json = await res.json();
  const d = json && json.item && json.item.rate && json.item.rate.dates && json.item.rate.dates[dateC];
  const s = d && d.stock;
  if (!s) return null;
  return { total: Number(s.T) || 0, booked: Number(s.B) || 0, available: Number(s.A) || 0 };
}

/* ---- build the contract -------------------------------------------------
   SCHEDULE is Kirsty's full list of departures per tour. Status per date:
     • not bookable in the cal (1/0)        → "soldout"   (red)
     • bookable and >= NEARING_PCT booked    → "nearing"   (amber, "Filling fast")
     • bookable, below that                  → "available" (navy)
   The booked % needs a per-date stock call, so it's only checked on the next
   NEARING_LOOKAHEAD bookable departures per tour (where filling happens), to
   keep the Worker within Cloudflare's subrequest budget. 14-Day merges 302+374. */
const NEARING_PCT = 0.75;        // >= 75% booked  ->  "Filling fast"
const NEARING_LOOKAHEAD = 4;     // stock-check at most this many bookable dates/tour

async function buildPayload(env) {
  const today = todayISO();
  const todayC = isoToCompact(today);
  const out = {};

  for (const key of Object.keys(SCHEDULE)) {
    const conf = SCHEDULE[key];
    const allDates = conf.dates.slice().sort();                  // keep past departures (shown sold-out for demand proof)
    const scheduledFuture = allDates.filter((d) => d >= today);  // future dates drive the Checkfront query window

    const startC = scheduledFuture.length ? isoToCompact(scheduledFuture[0]) : todayC;
    const anchor = scheduledFuture.length ? scheduledFuture[scheduledFuture.length - 1] : today;
    const endC = isoToCompact(addNights(anchor, conf.nights + 30));
    const availableSet = new Set();
    for (const itemId of conf.items) {
      try { const s = await fetchItemAvailable(itemId, startC, endC, env); for (const d of s) availableSet.add(d); }
      catch (e) { /* leave empty -> those dates show sold-out */ }
    }

    let availableCount = 0, nearingCount = 0, soldoutCount = 0, checked = 0;
    const all = [];
    for (const iso of allDates) {
      const c = isoToCompact(iso), end = addNights(iso, conf.nights);
      if (iso < today) { all.push({ start: iso, end, status: 'soldout' }); soldoutCount++; continue; }   // departed -> kept, shown sold-out (demand proof)
      if (!availableSet.has(c)) { all.push({ start: iso, end, status: 'soldout' }); soldoutCount++; continue; }
      let status = 'available';
      if (checked < NEARING_LOOKAHEAD) {            // only the next few bookable dates
        checked++;
        let T = 0, B = 0, known = false;
        for (const itemId of conf.items) {
          try { const st = await dateStock(itemId, c, env); if (st) { known = true; T += st.total; B += st.booked; } }
          catch (e) { /* ignore */ }
        }
        if (known && T > 0 && (T - B) > 0 && (B / T) >= NEARING_PCT) status = 'nearing';
      }
      if (status === 'nearing') nearingCount++; else availableCount++;
      all.push({ start: iso, end, status });
    }
    const firstBookable = all.find((x) => x.status !== 'soldout');   // available or nearing
    out[key] = { all, next: firstBookable ? firstBookable.start : null, availableCount, nearingCount, soldoutCount, total: all.length };
  }
  return out;
}

/* ---- fallback when Checkfront is unreachable ----------------------------
   Return the schedule with everything marked available. Better to under-
   report sold-outs for a few minutes than to break the list; the booking
   widget is still the real-time gate at point of purchase. */
function scheduleFallback() {
  const today = todayISO();
  const out = {};
  for (const key of Object.keys(SCHEDULE)) {
    const conf = SCHEDULE[key];
    const all = conf.dates.slice().sort()
      .map((start) => ({ start, end: addNights(start, conf.nights), status: start < today ? 'soldout' : 'available' }));
    const av = all.filter((x) => x.status !== 'soldout');
    out[key] = { all, next: av.length ? av[0].start : null, availableCount: av.length, soldoutCount: all.length - av.length, total: all.length };
  }
  return out;
}

/* ---- LEAD CAPTURE (/lead) ----------------------------------------------
   POST /lead takes a brochure-form submission from the tour pages, validates
   it, and forwards it to that tour's EXISTING Zapier catch hook — the same
   Zaps (and field aliases) the June wiring used, so ActiveCampaign and the
   Excel log keep receiving identical data. The hook URLs live in ONE Worker
   secret so they never appear in the pages:

     Secret name:  ZAPIER_HOOKS_JSON
     Value: JSON object mapping page key -> hook URL, e.g.
       {"14day-2627":"https://hooks.zapier.com/hooks/catch/17636803/u07v9hh/", ...}

   Until that secret is set this endpoint answers 503 and the pages fall back
   to redirecting visitors to /brochure-collection (no lead lost UX-wise, the
   real form there still works). Honeypot field: "website" — any value gets a
   fake success (bots learn nothing). Best-effort per-IP rate limit. */
const LEAD_MAX_PER_MIN = 20;        // per IP — generous for shared IPs (hotel/CGNAT)
const LEAD_GLOBAL_PER_MIN = 30;     // per isolate, all IPs — bounds Zapier-quota burn;
                                    // the REAL global cap is the edge WAF rate rule (runbook)
const leadHits = new Map();
const leadForwards = [];
function leadAllowed(ip) {
  const now = Date.now();
  const arr = (leadHits.get(ip) || []).filter((t) => now - t < 60000);
  arr.push(now);
  leadHits.set(ip, arr);
  if (leadHits.size > 5000) {                     // memory guard: evict stale only
    for (const [k, v] of leadHits) { if (!v.some((t) => now - t < 60000)) leadHits.delete(k); }
  }
  return arr.length <= LEAD_MAX_PER_MIN;
}
function leadBudgetOk() {
  const now = Date.now();
  while (leadForwards.length && now - leadForwards[0] >= 60000) leadForwards.shift();
  if (leadForwards.length >= LEAD_GLOBAL_PER_MIN) return false;
  leadForwards.push(now);
  return true;
}
/* NOTE: the Origin check only scopes CORS and drops foreign BROWSER posts —
   it is NOT a spam defense (curl sends no Origin and passes). Abuse control =
   honeypot + validation + rate limits here, plus the edge WAF rate rule. */
function leadCors(request) {
  const origin = request.headers.get('Origin') || '';
  const ok = /(^|\.)siredmundhillaryexplorer\.com$/
    .test((() => { try { return new URL(origin).hostname; } catch (e) { return ''; } })());
  return {
    'Access-Control-Allow-Origin': ok ? origin : 'https://www.siredmundhillaryexplorer.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin'
  };
}
function leadJson(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...headers } });
}
async function handleLead(request, env, ctx) {
  const cors = leadCors(request);
  if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
  if (request.method !== 'POST') return leadJson({ ok: false, error: 'method' }, 405, cors);
  if (!env || !env.ZAPIER_HOOKS_JSON) return leadJson({ ok: false, error: 'not_enabled' }, 503, cors);
  let hooks;
  try { hooks = JSON.parse(env.ZAPIER_HOOKS_JSON); } catch (e) { return leadJson({ ok: false, error: 'bad_config' }, 503, cors); }
  /* defense in depth: a browser request from a non-allowlisted origin gets a
     fake success and is dropped (CORS already blocks the read; this blocks the
     write too). Requests without an Origin header (curl, server-side) pass —
     the honeypot, validation and rate limit still apply to them. */
  const reqOrigin = request.headers.get('Origin');
  if (reqOrigin && cors['Access-Control-Allow-Origin'] !== reqOrigin) return leadJson({ ok: true }, 200, cors);
  let body;
  try { body = await request.json(); } catch (e) { return leadJson({ ok: false, error: 'bad_json' }, 400, cors); }
  if (!body || typeof body !== 'object') return leadJson({ ok: false, error: 'bad_json' }, 400, cors);
  if (body.website) return leadJson({ ok: true }, 200, cors);                  // honeypot: fake success
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (!leadAllowed(ip)) return leadJson({ ok: true }, 200, cors);              // rate-limited: fake success
  const clean = (v, n) => String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, n);
  /* spreadsheet-formula defusal: the Excel/Sheets log must never receive a cell
     that starts with = + - or @ (formula injection) — prefix an apostrophe */
  const desheet = (s) => (/^[=+\-@]/.test(s) ? "'" + s : s);
  const name = clean(body.name, 200);
  const email = clean(body.email, 254);
  const country = clean(body.country, 100);
  const page = clean(body.page, 60);
  const tour = clean(body.tour, 120);
  const sourceUrl = clean(body.source_url, 300);
  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return leadJson({ ok: false, error: 'invalid' }, 422, cors);
  if (!leadBudgetOk()) return leadJson({ ok: true }, 200, cors);               // global budget: fake success
  const safeUrl = (() => { try { const u = new URL(sourceUrl); return (u.protocol === 'https:' || u.protocol === 'http:') ? sourceUrl : ''; } catch (e) { return ''; } })();
  const hook = hooks[page];
  if (!hook || String(hook).indexOf('https://hooks.zapier.com/') !== 0) return leadJson({ ok: false, error: 'unknown_page' }, 422, cors);
  /* identical alias set to the June wiring, so the Zaps map without changes */
  const sName = desheet(name), sCountry = desheet(country), sTour = desheet(tour);
  const p = new URLSearchParams();
  p.append('name', sName); p.append('Name', sName); p.append('first_name', sName); p.append('dmform-1', sName);
  p.append('email', email); p.append('Email', email); p.append('dmform-3', email);
  p.append('country', sCountry); p.append('Country', sCountry); p.append('dmform-2', sCountry);
  p.append('tour', sTour); p.append('source_url', safeUrl);
  p.append('page_key', page); p.append('source', 'sehe-tour-page-direct');
  const forward = fetch(hook, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: p.toString() }).catch(() => {});
  /* answer fast: the forward completes in the background (survives the visitor
     navigating away); the page redirects regardless of our response */
  if (ctx && ctx.waitUntil) { ctx.waitUntil(forward); return leadJson({ ok: true }, 200, cors); }
  await forward;
  return leadJson({ ok: true }, 200, cors);
}

const CORS = {
  'Access-Control-Allow-Origin': '*',           // data is public; the page just reads it
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};


export default {
  async fetch(request, env, ctx) {
    const path = new URL(request.url).pathname;
    if (path === '/lead') return handleLead(request, env, ctx);
    if (path === '/items-audit') return handleItemsAudit(env);
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    const cache = caches.default;
    const cacheKey = new Request(new URL(request.url).origin + '/', { method: 'GET' });
    const cached = await cache.match(cacheKey);
    if (cached) return cached;

    let payload, ok = true;
    try {
      payload = await buildPayload(env);
      LAST_GOOD = payload;
    } catch (err) {
      ok = false;
      payload = LAST_GOOD || scheduleFallback();   // last good, else safe all-available
      payload.__warning = 'checkfront_unavailable: ' + (err && err.message ? err.message : 'error');
    }

    const body = JSON.stringify(payload);
    const headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': `public, max-age=${ok ? CACHE_SECONDS : 60}`,
      ...CORS
    };
    const response = new Response(body, { headers });
    if (ok) ctx.waitUntil(cache.put(cacheKey, response.clone()));  // only cache good payloads
    ctx.waitUntil(watchNewItems(env));   // new-item watchdog: after the response, never in its way
    return response;
  }
};

