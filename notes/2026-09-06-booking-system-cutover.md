# Booking-system cutover — what happened, verified (6 Sep 2026)

Paul Jackson's email (Thu 3 Sep, 11:58): SEHE is moving from Checkfront to
the new booking system built by Joel & Izaac Reed (thecreator.co.nz), already
used for The Mainlander; "SEHE will move across in the near future".
Ben: no bookings seen since Thursday.

## Timeline (UTC; NZST = +12)
- 30 Jul: last time this repo verified Checkfront widgets live on the tour
  pages (Kirsty's 302/374 split fix confirmed in the live widget).
- Thu 3 Sep: Paul's email. Exact cutover time not recoverable (Duda exposes
  no publish timestamps; Wayback unreachable from here). "No bookings since
  Thursday" places the cutover at or just after the email.
- Sun 6 Sep 09:01: ALL SEVEN tour pages carried the new embed — Block B
  section 5 replaced by an iframe to bookings.pounamutourismgroup.com
  (Pinnacle header "booking embed test": trialled there first).
- Sun 6 Sep ~10:30: SIX pages back on this repo's LATEST Block Bs
  (14day v28, 11day v26, winter-2027 v19, pinnacle v19, 14day-2728 v30,
  11day-2728 v21 — exact LATEST versions). Winter-2026 still on the embed.
  Ben re-pasted LATEST Block Bs "to make all items bookable" (confirmed);
  winter-2026 was left on the embed.

## Verified facts
- GitHub never contained the embed; single branch; all commits ours.
- The embed WORKS on a real Duda page (winter-2026, rendered headless via a
  curl-backed network shim): iframe created inside .booking-wrapper,
  auto-height bridge working (559px desktop / 635px iPhone), inventory
  loads, no JS errors. So the booking drop was NOT a broken widget.
- The app ("Pounamu Journeys Operations Console", custom Vite SPA, data in
  Supabase, own Google Ads tag AW-18077303178) has NO Checkfront dependency:
  inventory was copied, not synced. For 14-day 26/27 its 17 dates match
  Checkfront's 17 exactly; Oct 12/19/26 + Nov 9 sold out in both; Nov 16
  "selling fast" (Checkfront: available).
- Checkfront is still fully live for PTG: items 302/305/315/373/374/387/388
  active, /items-audit clean, restored widget loads its calendar
  ("New Booking: Mon Nov 16, 2026"), Trustpilot strip back.
- Ben's screenshot = the new app's "all journeys" view (BOOK NOW bar,
  CHOOSE YOUR JOURNEY, 20%-deposit footer) — texts confirmed inside the
  app frame.
- The embed dropped: the static 5-star Trustpilot strip, TOUR_DATA/SOLDOUT
  config, the sold-out handling; sections 6-13 untouched.

## Risks right now
1. Two systems selling the same seats if both stay bookable (Checkfront is
   live on six pages; the app on one, and standalone).
2. The site's live-departures layer (homepage board, journeys cards, hero
   counts) reads Checkfront via the worker; once Checkfront stops being
   maintained it will drift from what the app sells.
3. Conversion tracking split across two Google Ads tags.

## Recommendation
One system on all seven pages at a time. Joint test booking in the app
(desktop + iPhone Safari) → cut all seven to the embed the same day using
repo-generated Block Bs (embed per page + Trustpilot strip + our header) →
close Checkfront for SEHE → Joel/Izaac expose a read-only departures
endpoint → re-point the worker (site pages unchanged).
