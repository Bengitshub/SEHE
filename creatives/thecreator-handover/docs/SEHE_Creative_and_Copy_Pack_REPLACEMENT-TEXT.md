# Sir Edmund Hillary Explorer — Creative and Copy Pack
## Handover to The Creator · replacement text for the 24 Sep 2026 PDF

_This is the corrected text of the handover document. The original PDF (`SEHE_Creative_and_Copy_Pack_2026-09-24.pdf`) and its editable source were not supplied to this packaging job, so the PDF itself has **not** been edited; this text is provided to paste into the editable source or to use as the handover document in its own right. Prepared 23 Sep 2026._

---

## 1. What is being handed over

**A recovered, validated creative library, the copy it carries, and the campaign planning that goes with it.**

| | |
|---|---|
| **Creative library** | 119 ad creatives across three sets, plus 13 labelled historical alternatives — 132 PNGs, every one rendered at its intended pixel size and independently checked (dimensions, manifest hashes, all 14 contact sheets). |
| **Copy** | Embedded in each creative's source. Approved claims, banned phrasing and the locked Hillary quote are recorded in the Creative System Spec. A catalogue of every price, date, review, award and inclusion claim that must be confirmed before reuse is supplied (`FACTS_TO_VERIFY.md`). |
| **Campaign planning** | The Google Performance Max build sheet (campaign architecture, asset groups, final URLs, headlines, descriptions, sitelinks, callouts, search themes, audience signals, launch QA). |
| **Editable sources** | The complete React/JSX source of every creative with all 36 image assets, in two forms: the supplied files verbatim, and an offline-runnable copy with the runtime dependencies and fonts included. |
| **Design documentation** | Creative System Spec, project notes, per-tour image map, tour list, brochure cover/route URLs, two 14-Day brochure PDFs. |

Delivered as `SEHE_Creatives_PNG_2026-09-23` (creatives, contact sheets, manifests) and `SEHE_Creatives_Source_2026-09-23` (sources, tools, documents). Both carry a `MANIFEST.csv` with the SHA-256 of every file.

---

## 2. The creative library

### 2.1 Meta — Brand / Season set
Audience: Australian travellers 55+. Brand-level, not tour-specific. This set's conventions — the green "Now Booking · 2026–2028" pill, Trustpilot stack and WTA proof line on every creative, brand-level copy, homepage and Journeys-page destinations — apply to **this set**.

| Sub-set | Files | Size | Source |
|---|---|---|---|
| TOF Feed (discovery) | 16 | 1080×1080 (7) and 1080×1350 (9) | `ad-creatives.jsx` |
| TOF Stories / Reels | 4 | 1080×1920 | `tof-stories.jsx` |
| MOF v3 Feed 1:1 (decision support) | 13 | 1080×1080 | `mof-v3.jsx` |
| MOF v3 Feed 4:5 | 13 | 1080×1350 | `mof-v3.jsx` |
| MOF v3 Stories / Reels | 3 | 1080×1920 | `mof-v3.jsx` |

**Historical alternatives (labelled, kept for comparison only):** MOF v1 (6 creatives) and MOF v2 (6 creatives) are the earlier decision-support lines; the supplied notes record that the client was still to choose between v1 and v2 wording, and MOF v3 is labelled "layout-system tests A–F". Also kept: Brand TOF 14 "Sail, Steam & Steel" (Walter Peak), which exists on the design canvas but was never in the export list. These 13 are delivered under `04_Canvas_Only_Not_In_Exporter/`.

**Status:** approval and launch of this set are **not established from the supplied source files**.

### 2.2 Meta — 14-Day Spring/Summer Tour set
Tour-specific: 2026/27 and 2027/28 seasons, "Super 6" rail, from NZ$8,995 pp. Uses tour-specific years and tour pricing, not the brand-level conventions above.

| Sub-set | Files | Size | Source |
|---|---|---|---|
| TOF v1 (discovery) | 15 | 1080×1080 | `tour-14day.jsx` |
| MOF (decision support) | 15 | 1080×1080 | `tour-14day.jsx` |
| TOF v2 (fresh layout directions, to be culled against v1) | 15 | 1080×1080 | `tour-14day-v2.jsx` |

Four pairs of files are byte-identical because the source lists the same creative in two places (Super 6 grid, Departures, brand quote, Price); they are kept so the folder counts match the original structure and are flagged in the mapping.

**Status:** approval and launch **not established from the supplied source files**.

### 2.3 Google — Performance Max
Two asset groups with two different final URLs, plus logo assets. Minimal embedded copy, because Google overlays its own headlines and crops edges.

| Asset group | Files | Sizes | Final URL |
|---|---|---|---|
| 01 Journeys | 11 | 1200×628 (4) · 1200×1200 (4) · 960×1200 (3) | `/journeys` |
| 02 Brand / Homepage | 11 | 1200×628 (4) · 1200×1200 (4) · 960×1200 (3) | `/` |
| 03 Logos | 3 | 1200×1200 (2) · 1200×300 (1) | — |

Source: `pmax.jsx`. Three "clean" variants per group (L4, S4, P3) intentionally carry no headline.

**Status:** the build sheet is a planning document for "the first test". Whether the campaign was approved or launched is **not established from the supplied source files**.

---

## 3. Copy

- Copy is embedded in each creative's JSX; there is no separate copy deck in the supplied source. (A separate TOF copy PDF/spreadsheet is referenced elsewhere and remains outstanding — see section 8.)
- The Creative System Spec records the approved claims ("The South Island's Best Scenic Rail Journeys", "Voted New Zealand's Leading Tour Operator", "World Travel Awards Winner 2022–2025", "Fully guided rail & coach journeys", "Inspired by Sir Edmund Hillary", "Hosted by Peter Hillary" for Pinnacle only), the banned phrasing, the tone rules, the exact Hillary quote and the approved guest review.
- **Historical copy has been preserved exactly as written.** Nothing was rewritten.
- **Before any reuse**, the claims catalogued in `FACTS_TO_VERIFY.md` must be confirmed with the operator. Where that catalogue cites a figure from another source (website, booking system, a Trustpilot data check) it is a dated observation for comparison only, not a verified replacement; where sources conflict, neither is assumed correct. Four items are known conflicts or errors: the 14-Day departure list (creatives start 28 Sep 2026; the booking system, observed 20 Sep 2026, starts 12 Oct); the dinner count (creatives 10, website 9); the Trustpilot figures (creatives 4.8 · 70; a July/August 2026 data check returned 4.7 · 86); and one confirmed caption error — MOF v3 **1a-inclusions-editorial** (both sizes) captions a photograph of an outdoor viewing platform above a dam as "Aboard a South Island scenic railway". The historical renders are preserved; the caption must be corrected before reuse.

---

## 4. Campaign planning

### Google Performance Max — `PMax | AU | SEHE | Journeys | 2026–28`
From the supplied build sheet: market Australia; objective Leads; primary action brochure request / qualified enquiry; two asset groups (Journeys → `/journeys`; Brand/Homepage → `/`); call to action "Learn more"; recommended business name "Hillary Explorer" (the full name exceeds Google's 25-character field); Final URL expansion **off** at launch; brand exclusion where a branded Search campaign exists; Australia set to people in the location; Maximise Conversions without a forced target CPA; 15 short headlines, 5 long headlines and 5 descriptions per asset group (all within Google's character limits); 7 sitelinks; 10 callouts; a "Destinations" structured snippet; 15 search themes; first-party audience signals; a launch-QA checklist; and a note that a 15–25 second video in 16:9, 1:1 and 9:16 is the controlled next step.

**Budget:** the only figure anywhere in the available material is a **planned** starting recommendation of NZ$70/day (from the website repository's campaign sheet). No spend has been recorded in the supplied files; no figure should be read as spend.

### Meta campaigns
No campaign plan, budget or launch record for the Meta sets was supplied. Their status is not established from the supplied source files.

---

## 5. Conversion measurement

The build sheet's hierarchy: (1) confirmed booking or qualified booking enquiry; (2) completed brochure request — primary lead; (3) qualified call; (4) form starts, brochure-page visits and other engagement — secondary observation only.

**"Brochure Collection Page" is a URL-based custom conversion that counts visits to the brochure-collection page.** It does not independently verify that a brochure form was submitted; a visitor can reach that page by other routes. Treat it as a proxy for brochure leads until form submissions are tracked directly.

---

## 6. Design system and font treatment

The creatives are built on the system in the Creative System Spec: **Lora** (serif headlines, weight 500; italic support lines) and **DM Sans** (eyebrows, pills, captions, proof lines; 600, uppercase, tracked), with DM Mono in one helper. Palette: navy `#1a3a5c`, navy-deep `#112a45`, gold `#b8935a`, gold-soft `#d6b481`, cream `#f6f1e6`, Now-Booking green `#2f6e4a`. Verified in the source code and in the font-load report of every rendered file.

**MOF v3 is the one exception, and it must be described accurately.** Its source declares Montserrat for the sans elements ("Montserrat 600 headings, Lora reserved for serif accents"), but no supplied page loaded Montserrat, so every earlier render of MOF v3 fell back to DM Sans. The recovered package loads Montserrat so MOF v3 renders as its source declares, and includes a side-by-side of both treatments (`font-comparison/`). No other set was changed. The client should confirm which treatment MOF v3 is meant to ship in.

The website uses a different system — Montserrat / Open Sans, navy `#153b67`, gold `#c8a56c`. It is not the creative system and must not be applied to the creatives.

---

## 7. Files: included, available separately, missing

| Item | Status |
|---|---|
| React/JSX sources — 13 code/html files verbatim; 36 image assets byte-identical (SHA-256 verified), stored once in the offline copy | **Included** |
| Rendered PNGs — the 119 export entries | **Included** — validated and independently checked |
| 13 canvas-only creatives (Walter Peak; MOF v1 ×6; MOF v2 ×6) | **Included — historical alternatives** |
| 14 labelled contact sheets; `MANIFEST.csv` (path, dimensions, bytes, SHA-256); expected→source→output mapping; render and validation reports | **Included** |
| Offline runtime: React 18.3.1, ReactDOM 18.3.1, Babel Standalone 7.29.0, html-to-image 1.11.11, JSZip 3.10.1 (React/ReactDOM/Babel match the original SRI hashes); self-hosted Lora, DM Sans, DM Mono and Montserrat | **Included** |
| Replacement exporter, validator, contact-sheet builder; patched copy of the original browser exporter (original left unchanged) | **Included** |
| Creative System Spec; Project Notes; PMax build sheet; per-tour image map; tour list; brochure cover/route URLs; two 14-Day brochure PDFs | **Included** — as supplied |
| `SEHE_Creative_and_Copy_Pack_2026-09-24.pdf` and its editable source | **Not supplied** — this document is the replacement text |
| Separate TOF copy PDF / spreadsheet | **Outstanding** — referenced, not supplied |
| Pinnacle reporting documents | **Outstanding** — referenced, not supplied |
| `previews/` older shareable snapshot; `originals-supplied/` raw client uploads | **Available separately** — omitted from the upload archives by the sender to reduce size |
| The Canva design | **Available separately** — client's Canva account |
| `SEHE_Creatives_2026-09-23.zip` (original export) | Superseded — every PNG in it was fully transparent |

---

## 8. Availability note — the original export

The original browser export (`Download Ads.html`) produced fully transparent PNGs for two proven reasons: its capture stage was positioned off-screen with `position:fixed; left:-99999px`, which html-to-image copies into its clone; and its id list reused the name `V3`, overwriting the MOF v3 colour tokens under Babel's transform (which would have broken all 29 MOF v3 files even after the first fix). Both are fixed in the replacement exporter and in a labelled patched copy of the original exporter; the supplied files are untouched. All 132 creatives were re-exported with strict image-decode and font-load checks and independently verified.

---

## 9. Working with the sources

Serve `source-offline/` over a local web server (`python3 -m http.server 8765`) and open `index.html` for the full design canvas or `Download Ads (patched).html` for the browser exporter. `file://` does not work because Babel fetches the `.jsx` files over HTTP. Copy is edited directly in the components; sizes are set by each entry's `w`/`h`. Full instructions and the replacement-exporter commands are in the source package README and `tools/run-export.sh`.

---

## 10. Outstanding

1. The separate **TOF copy PDF / spreadsheet** — referenced, not supplied.
2. The **Pinnacle reporting documents** — referenced, not supplied.
3. The **editable source of the 24 Sep 2026 PDF** — needed only if the PDF itself is to be re-issued; otherwise this text stands in for it.
4. **Operator confirmation** of the items in `FACTS_TO_VERIFY.md`, in particular the 14-Day departure schedule, the dinner count, the Trustpilot figures, and the MOF v3 1a caption.
5. **Client decisions** not established from the supplied files: which MOF line is approved (v1 / v2 / v3); which font treatment MOF v3 ships in; and whether the Meta sets and the PMax campaign have been approved or launched.
