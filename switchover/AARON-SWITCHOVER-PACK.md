# SEHE tour pages — switch-over notes (Ben → Aaron)

13 July 2026

Aaron — all seven new tour pages are built, prepped and verified on their
preview URLs. The brochure forms are installed and lead-tested end-to-end
(same native Duda forms, so the webhook → Zapier → ActiveCampaign automations
are untouched), SEO titles are set, and departure availability feeds live
from Checkfront through our Cloudflare worker, which is already deployed —
no infra work in this job. What's left is the URL swaps, and you know Duda
better than I do.

## The swap list

| # | Tour | Preview (current) | Real URL (target) | Live version marker |
|---|------|-------------------|-------------------|---------------------|
| 1 | 14-Day Spring/Summer 26/27 | `/14/day-spr/sum-26/27-new` | `/2026-2027-spring/summer-tour-14-days` | v21 |
| 2 | 11-Day Spring/Summer 26/27 | `/11/day-spr/sum-26/27-new` | `/2026-2027-spring/summer-tour-11-day-tours` | v20 |
| 3 | Winter Edition 2026 | `/12/day-winter-26-new` | `/2026-winter-edition-tours` | v18 |
| 4 | Winter Edition 2027 | `/12/day-winter-27-new` | `/2027-winter-edition-tours` | v13 |
| 5 | Pinnacle Tour 2027 | `/15/day-pinnacle-27-new` | `/pinnacle-tour-2027` | v13 |
| 6 | 11-Day Spring/Summer 27/28 | `/11/day-spr/sum-27/28-new` | `/2026-2027-spring/2027-2028-spring/summer-tour-11-days` | v15 |
| 7 | 14-Day Spring/Summer 27/28 | `/14/day-spr/sum-27/28-new` | `/2026-2027-spring/2027-2028-spring/summer-tour-14-days` | v24 |

The `SEHE-*-blockA/B.txt` files in this folder are the pages' HTML-widget
source — versioned reference/rebuild material only, nothing for you to paste.
(Two files sit one rev ahead of the live marker; that's expected — a button
label was standardised in the editor rather than re-pasted.)

## Per page

1. Old live page → Page Settings → append `-old` to its URL. Decline Duda's
   auto-redirect offer. Set the `-old` page to noindex.
2. New page → set the real URL (exact strings above).
3. 301 redirect: `-new` slug → real URL (Site Settings → URL Redirects).
4. Sanity-check nav: page-linked items follow the rename automatically,
   URL-linked ones won't.
5. Publish. One page at a time, and message me after each — I have automated
   checks against the live URLs and will confirm within minutes.
6. Search Console sitemap resubmit once, after the last page.

Rollback for any page is just swapping the URLs back. Nothing gets deleted —
please keep the `-old` pages until I sign off.

## Architecture notes (so nothing surprises you)

- Each page is three stacked elements: HTML widget (top half) → native Duda
  form widget → HTML widget (bottom half). Native form = untouched lead flow.
- In the **editor** the form sits in its own row below the top widget —
  deliberate, so it stays selectable. On the **published** page a script in
  the top widget docks it into the brochure card and normalises its geometry
  inline. Don't drag it into the HTML block, and don't read the editor
  layout as broken.
- Please don't hand-edit inside the HTML widgets — the source is validated
  and versioned on our side. If something looks off, flag it and I'll ship a
  corrected block.
- The form styling lives in each form widget's Custom CSS (all-devices
  panel); `duda-brochure-form-skin.css` in this folder is the reference copy.

## What I verify after each flip (easy to eyeball too)

- New design serving on the real URL (View Source → `VERSION v` matches the
  table above).
- Form renders **inside** the white brochure card, edge-flush with the
  heading — not as a band below the card.
- Page bottom intact (the "Still comparing tours?" cards render).
- Sold-out departures struck red (e.g. 12/19/26 Oct on the 14-Day) — proves
  the live feed, not just the baked list.
- Browser tab shows the tour's SEO title.

Test leads were already fired and confirmed per page — no need to repeat
unless you want your own.

## Already handled / not in this job

- Cloudflare availability worker: deployed and verified 8 July
  (`sehe-worker_LIVE-auto.js` here is a reference copy only).
- A couple of Checkfront/content questions sit with Kirsty and me for
  post-launch.

Cheers — ping me as you flip each one.
Ben
