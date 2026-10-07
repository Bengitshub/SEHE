# Cloudflare Worker: `sehe-next-departures`

One Cloudflare Worker serves three endpoints for siredmundhillaryexplorer.com:

| Endpoint | What it does | Used by |
|---|---|---|
| `GET /` | Live departures feed (JSON): every tour's dates, each available, nearing (75%+ booked) or sold out | Homepage departure board, Journeys cards, Brochure Collection, the seven tour pages (hero counts, next departure, date lists, sold-out states) |
| `GET /items-audit` | Watchdog report: Checkfront products named "Sir Edmund Hillary Explorer" compared with the Worker's schedule | People, on demand |
| `POST /lead` | Direct brochure-lead capture, forwarding to each tour's Zap. **Parked:** it answers 503 until its secret is set | Nothing yet (Phase 2, `leadform/ENABLE-DIRECT-LEADS.md`) |

## Where it runs

- **Account:** Ben's Cloudflare account. The workers.dev subdomain is `ben-757`.
- **URL:** `https://sehe-next-departures.ben-757.workers.dev/`. This URL is written into 10 page masters (see the table below).
- **No KV, no cron, no custom domain.** The feed is built on request from Checkfront, cached at Cloudflare's edge for 10 minutes, and the last good result is kept in memory. If Checkfront fails, it serves the last good result (or the schedule with every future date available) with a `__warning` field, cached for 60 seconds. The pages keep their baked-in content if the Worker can't be reached.

| Masters that contain the URL |
|---|
| `SEHE-homepage_v38.txt`, `SEHE-journeys-page_v23.txt`, `SEHE-brochure-collection_v3.txt` |
| The seven tour masters `SEHE-*-tour_v*.txt` (their Block A files in `switchover/` and `LATEST/`) |

## Files in this folder

- `sehe-worker_LIVE-auto.js`: the code you paste into Cloudflare. `tools/make-latest.py` copies it to `LATEST/worker-sehe-next-departures.js`.
- `worker.js`: identical except for one final `export { … }` line the tests need. Make every change in both files.
- `worker.test.mjs`: offline tests, with no network. Run `node worker/worker.test.mjs`; it must report `ALL PASSED — 48 passed`. The July 2026 fixtures run on a frozen clock, so the tests don't fail as those dates pass.

## Settings (Cloudflare → Workers & Pages → `sehe-next-departures` → Settings → Variables and Secrets)

| Name | Type | Needed? | Purpose |
|---|---|---|---|
| `CF_API_KEY`, `CF_API_SECRET` | Secret | Optional | Checkfront token authentication. Without them the Worker uses Checkfront's public API, which works today. |
| `NEW_ITEM_ALERT_HOOK` | Secret | Optional | A Zapier catch hook the watchdog posts to when Checkfront has an SEHE product the schedule doesn't know. |
| `ZAPIER_HOOKS_JSON` | Secret | Only for `/lead` | A JSON map from tour key to that tour's Zapier hook. See `leadform/ENABLE-DIRECT-LEADS.md`. |

Secret values are never kept in this repo (repo rule 4). Check in Cloudflare which ones are set.

## Output of `GET /`

```json
{
  "14day-2728": {
    "all":  [ { "start": "2027-10-04", "end": "2027-10-17", "status": "available" } ],
    "next": "2027-10-04",
    "availableCount": 12, "soldoutCount": 1, "nearingCount": 0, "total": 13
  }
}
```

- **Keys:** `winter-2026`, `winter-2027`, `pinnacle-2027`, `11day-2627`, `14day-2627`, `11day-2728`, `14day-2728`.
- **Dates** are `YYYY-MM-DD`. `all` runs in date order and includes sold-out dates; they are never dropped.
- **`next`** is the first bookable date, or `null`.

## The schedule (keep it current)

`SCHEDULE` near the top of the code lists every departure date per tour, with its Checkfront item ID(s) and number of nights:

| Tour | Checkfront item ID(s) |
|---|---|
| Winter 2026 | 289, 392 |
| Winter 2027 | 373 |
| Pinnacle 2027 | 315 |
| 11-Day 2026/27 | 305 |
| 14-Day 2026/27 | 302, 374 (the solo split; a date is open if either has a seat) |
| 11-Day 2027/28 | 387 |
| 14-Day 2027/28 | 388 |

- **To add a season:** add its dates (and item ID) to `SCHEDULE`, and to the baked fallback in the page masters.
- **When a date sells out:** don't edit anything. It happens automatically.

## Current status, 1 Oct 2026 (read this before changing anything)

- **Bookings have moved.** In September 2026 bookings moved from Checkfront to The Creator's booking app (`notes/2026-09-06-booking-system-cutover.md`). **The feed still reads Checkfront.**
- **The live feed (checked 1 Oct 2026).** It answers HTTP 200 with no warning, and `/items-audit` is clean. But Checkfront no longer offers any Winter 2027, Pinnacle 2027, 11-Day 2027/28 or 14-Day 2027/28 date, so the feed marks all of them **sold out**. The two 2026/27 spring/summer tours still show some dates available.
- **The site doesn't show this.** Since 20 Sep 2026 the site-wide Head HTML hides departure dates, counts and the departure board: the block "TEMPORARY: hide unverifiable departure data" in `stopgap/SEHE-head-html-REWRITE.txt`. On 1 Oct no current tour showed a false "sold out"; the visible sold-out labels are the genuine Winter 2026 and past-season ones.
- **Do not remove that stopgap** until the Worker reads the new booking app.
- **The plan:** The Creator exposes a read-only departures endpoint. Change the Worker's data source to it and keep the output above identical, so no page needs editing.

## Deploying a change

1. Edit `sehe-worker_LIVE-auto.js` and make the same change in `worker.js`.
2. Run `node worker/worker.test.mjs` and confirm `ALL PASSED`.
3. Run `python3 tools/make-latest.py`.
4. In Cloudflare, open Workers & Pages → `sehe-next-departures` → **Edit code**. Select all, paste the file, and click **Deploy**.
5. Check the result:
   - the URL returns JSON with the seven keys and no `__warning`;
   - `/items-audit` shows `"ok": true` and `"newItems": []`.

**Rollback:** in the Worker's Deployments tab, roll back to the previous version, or paste the previous file from git history.

## Handing over the Cloudflare account (Ben's contract ends 31 Oct 2026)

The Worker lives in Ben's Cloudflare account. There are two ways to hand it over:

**A. Keep the account and add the company (no page changes).**

1. Ben invites the company's site manager (Aaron) as **Super Administrator**: Manage Account → Members → Invite.
2. Aaron accepts, and the company adds its own billing details if Cloudflare asks.
3. Ben removes himself once the company has confirmed access.

The URL stays the same, so nothing on the site changes. Renaming the workers.dev subdomain later would change the URL, and then option B's page steps apply.

**B. Recreate the Worker in the company's own Cloudflare account.**

1. Create a Worker named `sehe-next-departures`, paste `sehe-worker_LIVE-auto.js`, and add any secrets from the table above.
2. Note its new URL: `https://sehe-next-departures.<company-subdomain>.workers.dev/`.
3. Replace `https://sehe-next-departures.ben-757.workers.dev` in the 10 masters listed above.
4. Bump each master's version, then run `python3 tools/make-blocks.py --apply` and `python3 tools/make-latest.py`.
5. Re-paste:
   - the homepage, Journeys and Brochure Collection;
   - Block A of each tour page.
6. Keep Ben's Worker running until every page is re-pasted.
