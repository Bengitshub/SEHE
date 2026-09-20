# Live-site departure audit — findings (20 Sep 2026)

11-page parallel audit + adversarial completeness critic (444 elements
catalogued), run while preparing the "hide departures" stopgap.

## URGENT — three legacy pages still sell through the RETIRED system
| Page | HTTP | Checkfront widget | "Continue to Secure Booking" | noindex | in sitemap |
|---|---|---|---|---|---|
| `/2026-autumn-11-day-tours` | 200 | yes | yes | no | yes |
| `/2025-2026-new-tours` | 200 | yes | yes | no | yes |
| `/2025-2026-spring/summer-tours-10-day-tour` | 200 | yes | yes | no | yes |

Verified independently: each loads `checkfront.com/lib/interface--0.js`,
renders `#CHECKFRONT_WIDGET_01`, and links to `checkfront.com/reserve/`.
They are indexed (listed in sitemap.xml, no robots noindex), so a visitor
arriving from Google can transact in the system the business has left.
This is a bigger exposure than stale dates and needs a decision:
unpublish / redirect to the current tours / noindex.

## Baked departure counts already contradict each other
The 14-Day 2026/27 shows **14, 15 and 17** departures on different pages;
the 11-Day 2026/27 shows **5, 6 and 7**. This predates the booking move and
kills any idea of "freezing" the current numbers — every count must be
hidden, none can be trusted.

## Reachable by the stopgap (done)
Next-departure strips, "All departure dates" lists, departure counts, hero
departure fields, the homepage/v2 departure board. Verified hidden on all
16 live pages with zero new JS errors; sold-out markers deliberately kept.

## NOT reachable by CSS — needs a text edit or a separate decision
- Baked prose claims: "six departures across the deep-snow months"
  (Winter 2027 card), "One departure · 14 – 29 Jan 2027" (Pinnacle meta),
  "the widest choice of dates still open" (14-Day 2027/28).
- Homepage booking step 2: "Every journey page shows live availability for
  every date" — becomes untrue once availability is hidden.
- `h3.shx-season` reads "Spring / Summer 2027–28 · Now Booking" as bare
  text with no wrapper — CMS edit, not CSS.
- Brochure PDFs carry the full old schedule in their contents and
  filenames (e.g. `Web_10+Day+Tour+Brochure_31+March-9+April+2026.pdf`).
- Booking iframe windows are hard-coded; both winter pages use
  `keyword=winter` and differ only by `from`/`to`.
- Page titles / meta descriptions carry seasons; the winter-2027
  description is already mislabelled 2026.
