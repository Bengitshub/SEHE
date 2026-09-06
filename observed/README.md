# Observed live code (NOT authored here)

Snapshots of code found on the live site that did not come from this repo.
Kept so the repo records the divergence and the decision that follows.

## live-tour-blockB-booking-embed-2026-08.html
Fetched from the live 14-day 2026/27 page. All seven tour pages carry it.
Someone with Duda editor access replaced Block B's section 5 (our Checkfront
DROPLET widget + TOUR_DATA/SOLDOUT config + static 5-star Trustpilot strip)
with an iframe to a new booking app:

    https://bookings.pounamutourismgroup.com/sir-ed?keyword=...&from=...&to=...

The app identifies itself as "Pounamu Journeys Operations Console" (custom
Vite-built SPA, Cloudflare, its own Google Ads tag AW-18077303178), and the
embed uses an "mlw-" postMessage bridge for auto-height. The Pinnacle page's
header reads "(booking embed test)" — it was trialled there first.
Per page: 14-day 26/27 keyword=14+day 2026-10-01..2027-04-30; 11-day 26/27
keyword=11+day same window; winter 2026 keyword=winter 2026-07-01..2026-12-31;
winter 2027 keyword=winter 2027-06-01..2027-09-30; pinnacle keyword=pinnacle;
14-day 27/28 and 11-day 27/28 2027-09-01..2028-04-30.

Everything else in Block B (sections 6-13, mobile tweaks, hero-departures
script) is content-identical to the repo's v28 blocks once Duda's
re-serialisation (lowercased viewbox, onerror handlers, /opt/ image URLs)
is normalised. Block A on the live pages is still the deferred old v21.
