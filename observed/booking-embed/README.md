# The booking embed, as authored by theCreator (Joel / Izaac)

**Captured 20 Sep 2026 from the live site. This is THEIR code, not ours.
Do not overwrite it.** One file per tour page, each holding section 5
(`5. Booking / Available Dates`) exactly as served.

## Current live state — all SEVEN tour pages carry the embed
Checkfront is gone from every tour page.

| Page | iframe src | iframe title |
|---|---|---|
| 14day-2627 | `/sir-ed?keyword=14+day&from=2026-10-01&to=2027-04-30` | Book the 14 Day Explorer 2026/27 |
| 11day-2627 | `/sir-ed?keyword=11+day&from=2026-10-01&to=2027-04-30` | Book the 11 Day Explorer 2026/27 |
| winter-2026 | `/sir-ed?keyword=winter&from=2026-07-01&to=2026-12-31` | Book the 12 Day Winter Edition 2026 |
| winter-2027 | `/sir-ed?keyword=winter&from=2027-06-01&to=2027-09-30` | Book the 12 Day Winter Edition 2027 |
| pinnacle-2027 | `/sir-ed?keyword=pinnacle` *(no date window)* | Book The Pinnacle |
| 14day-2728 | `/sir-ed?keyword=14+day&from=2027-09-01&to=2028-04-30` | Book the 14 Day Explorer 2027/28 |
| 11day-2728 | `/sir-ed?keyword=11+day&from=2027-09-01&to=2028-04-30` | Book the 11 Day Explorer 2027/28 |

Host origin: `https://bookings.pounamutourismgroup.com`

## Are all seven built the same way?
**Yes.** Normalised and with per-page `keyword`/`from`/`to`/`title` masked,
six of the seven sections are byte-identical. Pinnacle is the only
structural variant: it passes `keyword=pinnacle` with **no `from`/`to`
window** (and its `<noscript>` link matches). Its Block B header also still
reads "(booking embed **test**)" — it was the pilot page.

Both winter pages use `keyword=winter`; the ONLY thing separating 2026 from
2027 is the `from`/`to` window. If their date keys ever shift, one winter
page could show the other's departures. Worth flagging to Joel.

## What our code does and does not touch
Our part of section 5 is the wrapper only — `.sehe-booking-section`,
the eyebrow "Available Dates", the heading "Choose your departure", and
`.booking-wrapper`. Their script appends `iframe.mlw-embed` into
`.booking-wrapper` and listens for `mlw-resize` / `mlw-scroll-top` /
`mlw-open` postMessages to auto-size.

**The departures stopgap (`stopgap/SEHE-hide-departures.txt`) does not
touch any of it.** Verified live on 14day-2627 and pinnacle-2027: with the
stopgap applied, the iframe stays present and visible, its height is
unchanged (2595px and 475px respectively), its src is unchanged, the
section stays visible at the same height, the heading stays, and the
booking app still renders inside the frame.

## How to avoid overwriting their work
1. `LATEST/tourpage-*-blockB.txt` still contain the OLD Checkfront widget.
   They are marked ON HOLD in `LATEST/_READ-ME-FIRST.txt`. **Do not paste
   them** while the embed is live — it would restore Checkfront.
2. When our tour-page masters are next updated, section 5 must be rebuilt
   from the files in this folder, not from the repo's Checkfront version.
3. Page-code changes should come to us rather than being edited in Duda
   directly, so the two do not overwrite each other.
