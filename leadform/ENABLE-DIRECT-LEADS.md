# SEHE — DIRECT LEAD CAPTURE (phase 2, after the switch-over)

**What this is:** the tour pages' brochure forms submit for real — straight into the
existing Zapier → ActiveCampaign → Excel flow — via the Worker's new `/lead`
endpoint. No Duda form widgets, no page sandwich, single-block pages forever.

**State right now:** everything is built and tested; the endpoint is **dormant**
(answers 503) until one secret is set. Until then nothing changes for visitors —
the form politely takes them to /brochure-collection as it does today.

**Data flow (identical data to the old Duda-form flow):**
```
page form  →  Worker /lead  →  that tour's EXISTING Zapier catch hook  →  ActiveCampaign + Excel
              (validates: honeypot, email,
               origin, rate limit; hook URLs
               live in a Worker secret)
```
The Worker sends the exact June field aliases (`name/Name/first_name/dmform-1`,
`email/Email/dmform-3`, `country/Country/dmform-2`, `tour`, `source_url`) so the
Zaps map without changes. Only Duda's own form inbox drops out — Excel + AC are
the systems of record.

---

## Step 1 — check the seven Zaps are alive (Ben, in Zapier)

These hooks came from the June wiring. Confirm each Zap is **ON** and mapped to
AC + the Excel log (fire a test from Zapier's editor if unsure):

| Tour | Hook |
|---|---|
| Winter 2026 | `https://hooks.zapier.com/hooks/catch/17636803/2gtdpq9/` |
| 14-Day 26/27 | `https://hooks.zapier.com/hooks/catch/17636803/u07v9hh/` |
| 11-Day 26/27 | `https://hooks.zapier.com/hooks/catch/17636803/un7qd8k/` |
| Pinnacle 2027 | `https://hooks.zapier.com/hooks/catch/21787136/u3tn2o7/` |
| Winter 2027 | `https://hooks.zapier.com/hooks/catch/17636803/un7qno2/` |
| 11-Day 27/28 | `https://hooks.zapier.com/hooks/catch/17636803/4bz3y7f/` |
| 14-Day 27/28 | `https://hooks.zapier.com/hooks/catch/17636803/4bzbs7k/` |

If any is dead, make a new catch hook and swap its URL into the JSON below.

## Step 2 — set the secret (Cloudflare)

Dashboard → Workers & Pages → `sehe-next-departures` → Settings → Variables and
Secrets → **Add** → type *Secret* → name `ZAPIER_HOOKS_JSON` → value = this JSON
on one line (edit URLs if any changed in step 1):

```json
{"winter-2026":"https://hooks.zapier.com/hooks/catch/17636803/2gtdpq9/","14day-2627":"https://hooks.zapier.com/hooks/catch/17636803/u07v9hh/","11day-2627":"https://hooks.zapier.com/hooks/catch/17636803/un7qd8k/","pinnacle-2027":"https://hooks.zapier.com/hooks/catch/21787136/u3tn2o7/","winter-2027":"https://hooks.zapier.com/hooks/catch/17636803/un7qno2/","11day-2728":"https://hooks.zapier.com/hooks/catch/17636803/4bz3y7f/","14day-2728":"https://hooks.zapier.com/hooks/catch/17636803/4bzbs7k/"}
```

Then paste the current `worker/sehe-worker_LIVE-auto.js` over the worker code and
**Save and Deploy** (the /lead endpoint ships with it; the departures feed is
untouched).

**Step 2b — edge rate limit (the real flood protection):** Dashboard → your domain
→ Security → WAF → **Rate limiting rules** → Create: *If URI Path equals `/lead`,
rate 10 requests per 10 seconds per IP → Block for 1 minute.* (The free plan
includes one rate-limiting rule.) This stops a scripted flood at Cloudflare's
edge before it can burn Zapier task quota; the Worker's own limits are the
second layer.

Smoke-test from any terminal (expect `{"ok":true}` and a row in Zapier history):
```
curl -X POST https://sehe-next-departures.ben-757.workers.dev/lead \
  -H "Content-Type: application/json" -H "Origin: https://www.siredmundhillaryexplorer.com" \
  -d '{"name":"Test Lead","email":"test@webhero.au","country":"New Zealand","page":"14day-2627","tour":"14-Day Spring/Summer Tour 2026/27"}'
```

## Step 3 — flip the pages (build side)

Tell the build side "flip the forms" — one command pre-flights all 7 pages,
regenerates them with the live form (version bump + changelog), and runs BOTH
project validators on every output, failing loudly before anything ships. Then
it's one single-block paste per page and a test lead each. Already dry-run-proven:
validators, revert-guard, publish-safety scan, JS syntax, and submit simulations
(valid lead / invalid input alerts and lets the visitor retry / worker down /
endpoint dormant — a visitor is never stuck and an invalid entry is never
silently lost).

## Step 4 — retire the sandwich

Once each flipped page's test lead lands in AC + Excel, delete that page's Duda
form row (the one between Block A and Block B). Pages are single-block from then on.

## Safety properties (why this can't hurt)

- **Dormant by default** — without the secret, /lead answers 503 and the form
  falls back to today's behaviour.
- **Visitor never stuck** — success, failure, timeout: all paths continue to
  /brochure-collection within 3.5 s. No-JS still works via the form's action.
- **Spam** — layered: the edge WAF rate rule (step 2b) is the hard cap; then the
  Worker's per-IP limit (20/min) and a global forward budget (30/min per isolate)
  both answer floods with fake success; a hidden honeypot absorbs naive bots;
  server-side validation rejects junk. Names/countries are defused against
  spreadsheet-formula injection before they reach the Excel log, and non-http
  source URLs are dropped. Hook URLs never appear in page source. (The origin
  check only scopes CORS and drops foreign browser posts — it is not the spam
  defense.)
- **Departures feed** — /lead is an isolated route; the feed code path is unchanged
  (33/33 worker tests pass, including 12 for /lead).
