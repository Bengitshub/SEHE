# Sir Edmund Hillary Explorer — site code handover (for Izaac / Joel)

_Prepared 6 Sep 2026. Everything here is public in this repository; nothing
in it is secret (API keys live only in Cloudflare Worker secrets)._

## 1. What you are looking at
The SEHE website (siredmundhillaryexplorer.com) runs on **Duda**. Every
page's real content is one or more Duda **HTML widgets** whose code is
authored in this repo and pasted in. The paste-ready files live in
[`LATEST/`](../LATEST) (stable filenames, always the newest version).
This folder adds what an outside developer needs on top of that.

| Folder / file | What it is |
|---|---|
| [`live-extract/`](live-extract) | The SEHE widget code **exactly as served by Duda today**, one file per page (Duda re-serialises: lowercased attributes, `onerror` handlers, `/opt/…-1920w` image URLs). Ground truth of what is live. |
| [`../LATEST/`](../LATEST) | The clean paste-ready sources for every page + the Worker. |
| [`feed-sample.json`](feed-sample.json) | A snapshot of the live-departures feed the pages consume (section 4). |
| [`../observed/`](../observed) | Your booking embed as it was found on the live pages (section 5). |
| [`../notes/2026-09-06-booking-system-cutover.md`](../notes/2026-09-06-booking-system-cutover.md) | Timeline and verification of the cutover, for context. |

## 2. Page map (live state on 6 Sep 2026)
| URL | Built from | Live today |
|---|---|---|
| `/` | `LATEST/homepage.txt` (v38) | v27 on the root; **v38 is on `/v2`** (noindex) for testing |
| `/journeys` | `LATEST/journeys-page.txt` | v22 |
| `/brochure-collection` | `LATEST/brochure-collection.txt` | v2 |
| `/2026-2027-spring/summer-tour-14-days` | `tourpage-14day-2627-blockA/B.txt` | Block A v21 (old), Block B v28, **Checkfront widget** |
| `/2026-2027-spring/summer-tour-11-day-tours` | `tourpage-11day-2627-…` | A v20, B v26, Checkfront |
| `/2026-winter-edition-tours` (sold out) | `tourpage-winter-2026-…` | A v23, **your embed** (left as the live pilot) |
| `/2027-winter-edition-tours` | `tourpage-winter-2027-…` | A v13, B v19, Checkfront |
| `/pinnacle-tour-2027` | `tourpage-pinnacle-2027-…` | A v13, B v19, Checkfront |
| `/2026-2027-spring/2027-2028-spring/summer-tour-14-days` | `tourpage-14day-2728-…` | A v24, B v30, Checkfront |
| `/2026-2027-spring/2027-2028-spring/summer-tour-11-days` | `tourpage-11day-2728-…` | A v15, B v21, Checkfront |

## 3. How a tour page is assembled in Duda
Three rows, top to bottom:
1. **HTML widget = Block A** (hero, highlights, "Super 6", brochure card with a
   docking slot). Ends at the comment `END OF BLOCK A`.
2. **Native Duda form widget** (the brochure form — same element on every
   page, so its automations keep working). Block A's script moves it into the
   brochure card on the published page.
3. **HTML widget = Block B** — starts with `<!-- ===== 5. Booking / Available
   Dates ===== -->` and carries the booking section, inclusions, itinerary,
   route map, film, gallery, FAQ, "still comparing" cards, about.

`LATEST/tourpage-<key>-blockA.txt` + `blockB.txt` are generated from one
master per page by `tools/make-blocks.py`; the split is byte-verified.
Homepage, Journeys and Brochure Collection are single widgets.

Tour keys used everywhere: `14day-2627`, `11day-2627`, `winter-2026`,
`winter-2027`, `pinnacle-2027`, `14day-2728`, `11day-2728`.

## 4. The live-departures layer — the part your system needs to replace
A Cloudflare Worker (`LATEST/worker-sehe-next-departures.js`, deployed as
`sehe-next-departures`) reads Checkfront and serves one JSON document that
every page consumes (see `feed-sample.json`):

```
GET https://sehe-next-departures.ben-757.workers.dev/
{
  "14day-2627": { "next": "2026-11-16",
                  "all": [ { "start": "2026-10-12", "end": "2026-10-25", "status": "soldout" },
                           { "start": "2026-11-16", "end": "2026-11-29", "status": "available" }, … ] },
  "winter-2027": { … }, …
}
status ∈ available | nearing | soldout      ("nearing" = ≥75% sold → "Filling fast")
```
Other endpoints: `/items-audit` (watchdog: Checkfront items the site doesn't
know), `/lead` (dormant lead capture).

**What the pages do with it** (all enhance-only — baked HTML stands if the
feed is down):
- Tour page hero: `[data-sehe-dep-count]`, `[data-sehe-dep-range]` (count +
  season range), sold-out paint.
- Journey cards (`/journeys`, homepage, "still comparing" on tour pages):
  `.journey-card[data-tour=<key>]` → next departure, departure count,
  "Season complete" when everything is sold.
- Homepage departure board: `[data-shx-dep="<key>|<start>"]` cards; the
  feed hides sold/past dates and swaps pills; hook `window.__shxRailApply(data)`.
- Loader API on tour/journeys pages: `window.__seheLoadDepartures()` →
  Promise<data>; `window.__seheDepartureData` = last data.

**Ask:** a read-only endpoint from your system with the same information
(per tour key: start, end, status, ideally seats left). If it returns this
exact shape the Worker becomes a thin adapter and **no page changes**; if it
is a different shape we map it inside the Worker. CORS for
`siredmundhillaryexplorer.com`, cacheable for ~10 min, no auth.

## 5. The booking section contract
Block B, section 5. Structure we keep at cutover:
```
<section class="sehe-booking-section" id="tour-dates">
  <div class="sehe-booking-header"> eyebrow "Available Dates" / h2 "Choose your departure" </div>
  <div class="booking-wrapper">  ← your embed goes here (iframe.mlw-embed, mlw-resize bridge)  </div>
  static Trustpilot 5-star strip (site-wide brand element, was dropped by the direct paste)
</section>
```
Your embed as found on the live pages is in
[`../observed/live-tour-blockB-booking-embed-2026-08.html`](../observed/live-tour-blockB-booking-embed-2026-08.html)
(per-page `keyword` / `from` / `to`). It renders correctly on Duda (verified
desktop + iPhone, auto-height working). One note: it relies on
`document.currentScript.parentNode`; a `getElementById` target would be
more robust if Duda ever changes how it executes widget scripts.

At cutover we generate Block Bs with the embed inside this section and paste
all seven pages the same day — so please send page-code changes to us
rather than editing the widgets in Duda directly; edits made in Duda are
overwritten by the next paste.

## 6. Constraints worth knowing (Duda)
- Duda's publisher strips `<` followed by a letter inside inline scripts
  (`i < n` is fine, `<div` in a string is not). Never build tags in JS strings.
- Duda serves a **different DOM to mobile user agents** and centres text
  from the row wrapper down; our widgets carry `text-align:left !important`
  locks. Test with a real phone UA.
- Section padding: the theme injects `padding:50px 40px` on sections; ours
  override with `!important`.
- Design tokens: navy `#0d2036` / `#153b67`, gold `#c8a56c`, paper
  `#f7f1e6`; Montserrat 600/700 headings, Open Sans body.

## 7. Open questions for your side
1. Bookings received in the new system since the cutover, and where
   booking notifications go.
2. The departures endpoint (section 4) — shape, CORS, cache.
3. Which Google Ads account tag `AW-18077303178` belongs to, and whether GA4
   is on the app (the site is about to run Performance Max to `/journeys`).
4. A test booking on iPhone Safari **inside** a tour page (cross-site
   iframe storage is where checkouts usually break).
5. Agreed cutover date/time, and Checkfront closed for SEHE at that moment.
