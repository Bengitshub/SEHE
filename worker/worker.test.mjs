/* Offline unit tests for the SEHE departures Worker (no network).
   Logic: SCHEDULE is Kirsty's full list; a scheduled date the cal can't book is
   kept as status:"soldout" (red). Only scheduled dates are shown. 302+374 merge.
   Run:  node worker/worker.test.mjs */
import {
  addNights, isoToCompact, extractAvailable, isAvailableValue, buildPayload, SCHEDULE, handleLead,
  knownItemIds, filterNewSeheItems, watchNewItems, handleItemsAudit
} from './worker.js';

let pass = 0, fail = 0;
function eq(actual, expected, msg) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a === e) pass++; else { fail++; console.log(`  ✗ ${msg}\n      expected ${e}\n      got      ${a}`); }
}
function ok(cond, msg) { if (cond) pass++; else { fail++; console.log(`  ✗ ${msg}`); } }

/* ---- 1. availability value parsing -------------------------------------- */
ok(isAvailableValue(1) === true, 'value 1 is available');
ok(isAvailableValue(0) === false, 'value 0 is not');
ok(isAvailableValue('1') === true, "string '1' is available");

/* ---- 2. real /cal shape (item 388) — summary keys must be ignored -------- */
const REAL_388 = { item: { item_id: 388, cal: {
  '20271004': 1, '20271011': 1, '20271018': 1, '20271031': 0,
  'available': 70, 'booked': 3, 'status': 'U', 'span_closed': 0, 'unit': 'D',
  '20271101': 1, '20280214': 1
} } };
const g = extractAvailable(REAL_388, '388');
ok(g.has('20271004') && !g.has('20271031'), '388: 1 = available, 0 = not');
ok(!g.has('available') && !g.has('70'), '388: summary keys excluded');

/* ---- 3. end-date computation -------------------------------------------- */
eq(addNights('2027-10-04', 13), '2027-10-17', '14-day end = start + 13 nights');

/* ---- mock Checkfront ------------------------------------------------------
   /item/{id}/cal         → availability (1/0) from availByItem.
   /item/{id}?start_date= → rated single-date stock {T,B,A} from stockByItem
                            (defaults to T:80 B:0 A:80 = 0% booked = available). */
function mockCheckfront(availByItem, stockByItem) {
  globalThis.fetch = async (url) => {
    const calM = url.match(/\/item\/(\d+)\/cal/);
    if (calM) {
      const id = calM[1], cal = {};
      for (const d of (availByItem[id] || [])) cal[d] = 1;
      cal.available = 70; cal.booked = 3; cal.status = 'U'; cal.span_closed = 0; cal.unit = 'D';
      return { ok: true, json: async () => ({ item: { item_id: Number(id), cal } }) };
    }
    const rm = url.match(/\/item\/(\d+)\?start_date=(\d{8})/);
    if (rm) {
      const id = rm[1], date = rm[2];
      // An item only has rated stock for a date it actually offers (or an explicit
      // fixture). An item with no seat on this date (e.g. a merge partner like 392
      // that only carries one departure) returns no rated stock, so it isn't summed.
      const fixture = stockByItem && stockByItem[id] && stockByItem[id][date];
      const offered = (availByItem[id] || []).includes(date);
      const stock = fixture || (offered ? { T: 80, B: 0, A: 80 } : null);
      const dates = stock ? { [date]: { stock } } : {};
      return { ok: true, json: async () => ({ item: { item_id: Number(id), rate: { dates } } }) };
    }
    return { ok: false, json: async () => ({}) };
  };
}

/* ---- 4. a scheduled date the cal can't book is SOLD OUT (kept, red) ------ */
mockCheckfront({ '289': ['20260801', '20260905', '20260912'] });   // 27 Jun & 18 Jul not bookable
let t = (await buildPayload({}))['winter-2026'];
eq(t.all.filter((x) => x.status === 'soldout').map((x) => x.start), ['2026-06-27', '2026-07-18'], 'winter: 27 Jun & 18 Jul sold out (red)');
ok(t.total === 5 && t.availableCount === 3 && t.soldoutCount === 2, 'winter: 5 dates, 3 available, 2 sold out');
eq(t.next, '2026-08-01', 'winter: next = first available (1 Aug)');
ok(t.all.length === SCHEDULE['winter-2026'].dates.length, 'winter: full list kept, nothing dropped');

/* ---- 5. the 302 + 374 merge; Oct 26 dates sold out ---------------------- */
const main2627 = ['20261109', '20261116', '20261123', '20270104', '20270111', '20270118', '20270125', '20270215', '20270315', '20270322', '20270405', '20270412'];
mockCheckfront({ '302': main2627, '374': ['20270208', '20270308'] });
t = (await buildPayload({}))['14day-2627'];
const st = (iso) => t.all.find((x) => x.start === iso).status;
eq(st('2027-02-08'), 'available', '2627: 8 Feb available via #374 merge');
eq(st('2027-03-08'), 'available', '2627: 8 Mar available via #374 merge');
eq(st('2026-10-12'), 'soldout', '2627: 12 Oct sold out (red)');
ok(t.total === SCHEDULE['14day-2627'].dates.length, '2627: full 17-date list kept');

/* ---- 6. list-driven: a cal date NOT in the schedule is NOT shown --------- */
const sched2728 = SCHEDULE['14day-2728'].dates.map(isoToCompact);
mockCheckfront({ '388': sched2728.concat('20280228') });   // Checkfront has an extra bookable date (28 Feb 2028 is not scheduled)
t = (await buildPayload({}))['14day-2728'];
ok(!t.all.some((x) => x.start === '2028-02-28'), '2728: a non-scheduled Checkfront date is NOT shown (no auto-discovery)');
ok(t.total === 19 && t.soldoutCount === 0, '2728: exactly the 19 scheduled, all available');

/* ---- 7. "Filling fast": a bookable date >= 75% booked -> nearing (amber) -- */
mockCheckfront(
  { '289': ['20260801', '20260905', '20260912'] },          // all 3 bookable
  { '289': { '20260801': { T: 80, B: 62, A: 18 } } }        // 1 Aug = 77.5% booked
);
t = (await buildPayload({}))['winter-2026'];
eq(t.all.find((x) => x.start === '2026-08-01').status, 'nearing', 'winter: 1 Aug "Filling fast" (78% booked)');
eq(t.all.find((x) => x.start === '2026-09-05').status, 'available', 'winter: 5 Sep available (0% booked)');
ok(t.nearingCount === 1 && t.soldoutCount === 2, 'winter: 1 nearing, 2 sold out');
eq(t.next, '2026-08-01', 'winter: next = first bookable (nearing still counts)');

// just under the threshold stays available
mockCheckfront({ '289': ['20260801'] }, { '289': { '20260801': { T: 80, B: 59, A: 21 } } });   // 73.75%
ok((await buildPayload({}))['winter-2026'].all.find((x) => x.start === '2026-08-01').status === 'available', 'winter: 74% booked is still available (under 75%)');

/* ---- 9. /lead endpoint --------------------------------------------------- */
function leadReq(body, opts) {
  const o = opts || {};
  return {
    method: o.method || 'POST',
    headers: { get: (k) => (k === 'Origin' ? (o.origin || 'https://www.siredmundhillaryexplorer.com') : k === 'CF-Connecting-IP' ? (o.ip || '1.2.3.' + Math.floor(Math.random() * 250)) : null) },
    json: async () => body,
  };
}
const HOOKS = JSON.stringify({ '14day-2627': 'https://hooks.zapier.com/hooks/catch/17636803/u07v9hh/' });
let sent = null;
globalThis.fetch = async (url, init) => { sent = { url, body: init.body }; return { ok: true }; };
const fakeCtx = () => ({ p: null, waitUntil(x) { this.p = x; } });

let r = await handleLead(leadReq({}, { method: 'GET' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 405, '/lead: GET rejected');
r = await handleLead(leadReq({ name: 'A', email: 'a@b.co', page: '14day-2627' }), {});
ok(r.status === 503, '/lead: 503 when the secret is not set (endpoint dormant)');
r = await handleLead(leadReq(null), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 400, '/lead: literal-null body -> clean 400, no crash');
sent = null;
r = await handleLead(leadReq({ name: 'Bot', email: 'x@y.co', page: '14day-2627', website: 'spam.com' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 200 && sent === null, '/lead: honeypot gets fake success, nothing forwarded');
r = await handleLead(leadReq({ name: 'A', email: 'not-an-email', page: '14day-2627' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 422, '/lead: invalid email rejected');
r = await handleLead(leadReq({ name: 'A', email: 'jane@gmailcom', page: '14day-2627' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 422, '/lead: email with no dot after the @ rejected');
r = await handleLead(leadReq({ name: 'A', email: 'a@b.co', page: 'nope' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 422, '/lead: unknown page key rejected');
sent = null;
let cx = fakeCtx();
r = await handleLead(leadReq({ name: 'J Smith', email: 'j.smith@gmail.com', country: 'Australia', page: '14day-2627' }), { ZAPIER_HOOKS_JSON: HOOKS }, cx);
await cx.p;
ok(r.status === 200 && sent && sent.url.indexOf('u07v9hh') > 0, '/lead: dotted-local-part email (j.smith@) ACCEPTED and forwarded');
sent = null; cx = fakeCtx();
r = await handleLead(leadReq({ name: 'Jane Doe', email: 'jane@example.com', country: 'Australia', page: '14day-2627', tour: '14-Day Spring/Summer Tour 2026/27', source_url: 'https://www.siredmundhillaryexplorer.com/x' }), { ZAPIER_HOOKS_JSON: HOOKS }, cx);
await cx.p;
const q = new URLSearchParams(sent.body);
ok(r.status === 200 && q.get('name') === 'Jane Doe' && q.get('dmform-1') === 'Jane Doe' && q.get('Email') === 'jane@example.com' && q.get('dmform-2') === 'Australia' && q.get('tour') === '14-Day Spring/Summer Tour 2026/27' && q.get('source_url') === 'https://www.siredmundhillaryexplorer.com/x', '/lead: June-compatible field aliases all present');
sent = null; cx = fakeCtx();
r = await handleLead(leadReq({ name: '=HYPERLINK("http://evil","x")', email: 'a@b.co', country: '+junk', page: '14day-2627', source_url: 'javascript:alert(1)' }), { ZAPIER_HOOKS_JSON: HOOKS }, cx);
await cx.p;
const q2 = new URLSearchParams(sent.body);
ok(q2.get('name').charAt(0) === "'" && q2.get('country').charAt(0) === "'" && q2.get('source_url') === '', '/lead: spreadsheet formulas defused, non-http source_url dropped');
sent = null;
r = await handleLead(leadReq({ name: 'A', email: 'a@b.co', page: '14day-2627' }, { origin: 'https://evil.example.com' }), { ZAPIER_HOOKS_JSON: HOOKS });
ok(r.status === 200 && sent === null, '/lead: foreign Origin gets fake success, nothing forwarded');
const ipFixed = { ip: '9.9.9.9' };
let last = null;
for (let i = 0; i < 22; i++) last = await handleLead(leadReq({ name: 'A', email: 'a@b.co', page: '14day-2627' }, ipFixed), { ZAPIER_HOOKS_JSON: HOOKS });
sent = null;
last = await handleLead(leadReq({ name: 'A', email: 'a@b.co', page: '14day-2627' }, ipFixed), { ZAPIER_HOOKS_JSON: HOOKS });
ok(last.status === 200 && sent === null, '/lead: per-IP rate limit kicks in (fake success, nothing forwarded)');


/* ---- 12. new-item watchdog ---------------------------------------------- */
console.log('watchdog: known ids, name filter, alerting, failure isolation');
{
  const known = knownItemIds();
  ok(known.has('302') && known.has('374') && known.has('289') && known.has('392'), 'knownItemIds carries the split items');
  eq(known.size, 9, 'nine scheduled item ids');

  const ITEMS = { items: {
    '302': { name: 'Sir Edmund Hillary Explorer: 14-Day Tour', category_id: '5', status: 'U' },
    '310': { name: 'General Admission - Marlborough Flyer Steam Train', category_id: '5', status: 'U' },
    '401': { name: '* Sir Edmund Hillary Explorer: 14-Day Tour EXTRA', category_id: '5', status: 'U' },
    '402': { name: 'SIR EDMUND HILLARY EXPLORER: Winter Edition 2028', category_id: '5', status: 'U' },
    '403': { name: 'Family Pass - Return Trip (Blenheim)', category_id: '5', status: 'U' }
  } };
  const found = filterNewSeheItems(ITEMS, known);
  eq(found.map((x) => x.id), ['401', '402'], 'flags only unscheduled SEHE-named items');
  eq(filterNewSeheItems({ items: {} }, known), [], 'empty item list -> nothing');
  eq(filterNewSeheItems(null, known), [], 'missing payload -> nothing');

  // alert fires once per distinct set, to the hook, with the ids
  const calls = [];
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (url, opts) => {
    if (String(url).endsWith('/api/3.0/item')) return { ok: true, json: async () => ITEMS };
    calls.push({ url: String(url), body: opts && opts.body });
    return { ok: true };
  };
  const env = { NEW_ITEM_ALERT_HOOK: 'https://hooks.zapier.com/hooks/catch/TEST/abc' };
  const r1 = await watchNewItems(env);
  eq(r1.map((x) => x.id), ['401', '402'], 'watchdog returns the new items');
  const r2 = await watchNewItems(env);
  eq(r2.length, 2, 'second run still reports');
  eq(calls.length, 1, 'but alerts only once per distinct set');
  ok(calls[0].url.indexOf('hooks.zapier.com') !== -1, 'alert went to the hook');
  ok(String(calls[0].body).indexOf('"401"') !== -1 && String(calls[0].body).indexOf('"402"') !== -1, 'alert body names the ids');

  // /items-audit endpoint
  const res = await handleItemsAudit(env);
  const audit = JSON.parse(await res.text());
  ok(audit.ok === true, 'items-audit ok');
  eq(audit.newItems.map((x) => x.id), ['401', '402'], 'items-audit lists the new items');
  ok(audit.seheItemsInCheckfront.some((x) => x.id === '302' && x.known === true), 'items-audit marks known items');

  // failure isolation: item list down -> watchdog returns [], never throws
  globalThis.fetch = async () => { throw new Error('checkfront down'); };
  const r3 = await watchNewItems(env);
  eq(r3, [], 'watchdog swallows fetch failure');
  const res2 = await handleItemsAudit(env);
  const audit2 = JSON.parse(await res2.text());
  ok(audit2.ok === false, 'items-audit reports failure honestly');
  globalThis.fetch = realFetch;
}

console.log(`\n${fail === 0 ? 'ALL PASSED' : 'FAILURES'} — ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
