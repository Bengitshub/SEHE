# SEHE — FINAL SWITCH-OVER PACK (for Aaron)

**Prepared:** 8 July 2026 (rev 5, 13 Jul — docking rolled out to ALL 7 pages’ blocks, Winter-2026 5 Sep sell-out baked; rev 4 — the real form now auto-docks INTO the brochure card on published pages via a script in Block A; rev 3 aligned booking data to the live-site widgets: full Checkfront date lists incl. Oct 2026, worker-wins live merge) · **Scope:** put the 7 new tour pages live on the real URLs, install the real lead-capture forms, set SEO titles, deploy the availability worker.

Everything in this folder is verified: every page passed the project validators, the live `-new` previews were crawled and fact-checked, and each Block A + Block B pair reconstructs its page byte-for-byte.

---

## 0. What you're switching

| # | Tour | New page (already built & verified) | Goes live at (real URL) | Files in this pack |
|---|---|---|---|---|
| 1 | 14-Day Spring/Summer 2026/27 · v17 | `/14/day-spr/sum-26/27-new` | `/2026-2027-spring/summer-tour-14-days` | `SEHE-14day-2627_v17-blockA/B.txt` |
| 2 | 11-Day Spring/Summer 2026/27 · v15 | `/11/day-spr/sum-26/27-new` | `/2026-2027-spring/summer-tour-11-day-tours` | `SEHE-11day-2627_v15-blockA/B.txt` |
| 3 | 12-Day Winter Edition 2026 · v14 | `/12/day-winter-26-new` | `/2026-winter-edition-tours` | `SEHE-winter-2026_v14-blockA/B.txt` |
| 4 | 12-Day Winter Edition 2027 · v8 | `/12/day-winter-27-new` | `/2027-winter-edition-tours` | `SEHE-winter-2027_v8-blockA/B.txt` |
| 5 | 15-Day Pinnacle Tour 2027 · v8 | `/15/day-pinnacle-27-new` | `/pinnacle-tour-2027` | `SEHE-pinnacle-2027_v8-blockA/B.txt` |
| 6 | 11-Day Spring/Summer 2027/28 · v10 | `/11/day-spr/sum-27/28-new` | `/2026-2027-spring/2027-2028-spring/summer-tour-11-days` | `SEHE-11day-2728_v10-blockA/B.txt` |
| 7 | 14-Day Spring/Summer 2027/28 · v19 | `/14/day-spr/sum-27/28-new` | `/2026-2027-spring/2027-2028-spring/summer-tour-14-days` | `SEHE-14day-2728_v19-blockA/B.txt` |

> **STATUS:** Page 1 (14-Day 26/27) is **already fully prepped** on its `-new` URL — sandwich installed, form skinned and lead-tested, SEO title set. For page 1 skip §1 and §2 and do **only §3** (the URL swap). Pages 2–7 need the full §1 → §2 → §3 sequence.

Also in the pack: `duda-brochure-form-skin.css` (form styling) and `sehe-worker_LIVE-auto.js` (availability worker).

---

## 1. WHY the A/B blocks (the lead-capture fix — read this first)

The form currently on each `-new` page is a **design placeholder — it captures nothing**. Submitting it just redirects to /brochure-collection. **Do not leave it as the only form on a live page.**

The fix keeps the **existing Duda forms** (so the webhook → Zapier → ActiveCampaign automations keep working untouched — same form element, same submissions, same reCAPTCHA and confirmation email). A Duda form only works as a real Duda widget, so each page becomes a sandwich:

```
[ HTML widget: BLOCK A ]   ← page top → brochure card (placeholder form already removed)
[ Duda row, bg #f9f7f3 ] ← the NATIVE Duda brochure form widget, skinned
[ HTML widget: BLOCK B ]   ← booking section → rest of page
```

**Per page:**
1. In the Duda editor for the page, replace the current single HTML widget's contents with **Block A**.
2. Add a **new row directly below** it → set the row background to **#f9f7f3** (continues the brochure band).
3. Into that row, **copy the brochure form element across from the old live page** (copy, **don't move** — the old page keeps its form for rollback; it must be the same form so the webhook fires). Keep its fields: Name / Email / Country. The step-7 test lead confirms the copy submits and the automation fires.
4. Open the form widget's **Design → Custom CSS** → paste ALL of `duda-brochure-form-skin.css` into the "GENERAL CSS FOR ALL DEVICES" panel (replace whatever is there) and **clear** the device-specific panel. The form now matches the page design.
5. Add a **new HTML widget below the form row** → paste **Block B**.
6. The end of Block A contains this same instruction as an HTML comment, so you can't lose your place.
7. **Where the form appears:** in the editor the form sits in its own row (so it stays selectable/editable). On the **published** page a script in Block A automatically moves it INTO the brochure card's right-hand column — the exact spot the design intends. Don't try to drag it into the HTML block yourself.

> Sanity check before publishing: the page reads Hero → … → Brochure card ("Complete the short form just below…") → the real form → Booking/dates → itinerary continues → footer sections.

---

## 2. Per-page SEO title (Page Settings → SEO → "SEO Title")

| Page | Paste this exactly |
|---|---|
| 14-Day 26/27 | `14-Day Spring/Summer 2026/27 Rail & Coach Tour \| Sir Edmund Hillary Explorer` |
| 11-Day 26/27 | `11-Day Spring/Summer 2026/27 Rail & Coach Tour \| Sir Edmund Hillary Explorer` |
| Winter 2026 | `12-Day Winter Edition 2026 \| Sir Edmund Hillary Explorer` |
| Winter 2027 | `12-Day Winter Edition 2027 \| Sir Edmund Hillary Explorer` |
| Pinnacle 2027 | `15-Day Pinnacle Tour 2027 with Peter Hillary \| Sir Edmund Hillary Explorer` |
| 11-Day 27/28 | `11-Day Spring/Summer 2027/28 Rail & Coach Tour \| Sir Edmund Hillary Explorer` |
| 14-Day 27/28 | `14-Day Spring/Summer 2027/28 Rail & Coach Tour \| Sir Edmund Hillary Explorer` |

(Type the `|` as a normal pipe — the backslashes above are just table escaping.)

---

## 3. The URL switch itself

Recommended method (keeps SEO, no content re-paste):

1. On the **old live page**: Page Settings → change its URL → append `-old` (e.g. `/2026-winter-edition-tours-old`). Decline/remove any auto-redirect Duda offers for this rename. Set the renamed `-old` page to **noindex** (SEO panel) — it stays for rollback and must not be indexed as a duplicate.
2. On the **new page** (the one you just gave the form sandwich): Page Settings → change its URL from the `-new` slug to the **real URL** (exact strings in the §0 table).
3. Create a **301 redirect** from the `-new` slug to the real URL (Site Settings → URL Redirects) so any preview links people saved keep working.
4. Check the site **navigation** still points at the right page (if nav items are linked by page, they follow automatically; if linked by URL, re-point them).
5. **Publish / Update Site.** After publishing, **resubmit the sitemap in Search Console** so Google picks up the new URLs quickly.
6. Repeat per page. Do them one at a time — after each one, ping Ben/the verifier (see §5).

Alternative (if URL swapping is awkward): paste Block A + form + Block B into the old live page directly and publish. Same result, more paste work.

**Rollback** (any page, any reason): swap the URLs back (old page → real URL again). Nothing is deleted at any point — keep the `-old` pages until sign-off.

---

## 4. Availability worker — ALREADY DEPLOYED ✓

The updated worker went live on 8 July and has been verified (Pinnacle now returns 14 Jan → **29 Jan 2027**; all tours checked). **No Cloudflare work needed** — the `sehe-worker_LIVE-auto.js` in this pack is a reference copy only.

One item remains here: confirm with Kirsty that the **Checkfront Pinnacle product** (item 315) resolves bookings to an **end date of 29 January 2027** (15 nights), so booking confirmations match the pages.

**Open question for Kirsty (post-launch, Ben to raise):** the hero "Departures" stat currently live-updates from the worker feed so it always matches the booking list (e.g. it moved 15 → 14 by itself when 12 Oct sold out). Ben may prefer it frozen — decide together after launch; freezing risks the hero contradicting the list below it.

---

## 5. Verification (after each page)

Tell Ben the page is flipped — the build side will re-crawl the live URL and confirm within minutes. What's being checked (also easy to eyeball):

- The new design is on the **real URL** and the version marker matches §0 (View Source → search `VERSION v`).
- The brochure form renders **inside the white brochure card** (right column, under the subtitle) — not as a separate band below the card.
- The bottom of the page is intact (the "About" band and "Still comparing tours?" cards render — proves the full paste survived).
- Departure dates show instantly and sold-out dates are red — confirm you can see **sold-out badges** (e.g. 19 & 26 Oct on the 14-Day): that proves the live feed is working, not just the baked list.
- **Submit a test lead** through the brochure form → confirm it arrives wherever leads normally land (Duda form inbox → webhook → automation). One test per page.
- Browser tab shows the new SEO title.

## 6. Don'ts

- **Don't** copy the *markup* of a Duda form into an HTML widget — a pasted copy looks right but never submits and never fires the webhook. Only the real widget counts.
- **Don't** edit anything inside the HTML blocks — every page is validated as-is. If something looks wrong, flag it; don't hand-fix in Duda.
- **Don't** delete the old pages until Ben signs off — they're the rollback.
