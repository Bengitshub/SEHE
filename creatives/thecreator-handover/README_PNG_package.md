# SEHE Creatives — validated PNG exports (2026-09-23)

**132 PNGs: the 119 entries of the original export structure plus 13 canvas-only creatives.** Every file decoded, matched its intended pixel size, and is neither transparent nor a single colour. No render or asset failures; every image inside every creative decoded with real dimensions and every font face loaded before capture.

## Folders (unchanged names from the original exporter)
| Folder | Files |
|---|---|
| 01_Meta_Brand-Season/TOF_Feed | 16 |
| 01_Meta_Brand-Season/TOF_Stories_9x16 | 4 |
| 01_Meta_Brand-Season/MOF_Feed_1x1 | 13 |
| 01_Meta_Brand-Season/MOF_Feed_4x5 | 13 |
| 01_Meta_Brand-Season/MOF_Stories_9x16 | 3 |
| 02_Meta_14-Day-Tour/TOF_v1 | 15 |
| 02_Meta_14-Day-Tour/MOF | 15 |
| 02_Meta_14-Day-Tour/TOF_v2 | 15 |
| 03_Google_PMax/01_Journeys_Asset_Group | 11 |
| 03_Google_PMax/02_Brand_Homepage_Asset_Group | 11 |
| 03_Google_PMax/03_Logos | 3 |
| **04_Canvas_Only_Not_In_Exporter/** 01_Brand_TOF_Feed_extra (1) · 02_Brand_MOF_v1_HISTORICAL (6) · 03_Brand_MOF_v2_HISTORICAL (6) | 13 |

Sizes of the 119 expected entries: 1080x1080: 65, 1080x1350: 22, 1200x1200: 10, 1200x628: 8, 1080x1920: 7, 960x1200: 6, 1200x300: 1 — matching the expected counts exactly.

The 13 extras exist on the design canvas (`app.jsx`) but were never in the exporter's list: "Sail, Steam & Steel" (Brand TOF 14) and the earlier MOF v1 and v2 lines, which the project notes describe as kept for comparison until the client chose. They are delivered as **historical alternatives**, not as part of the approved sets.

## Identical files — by design, for review
Eight files are byte-identical in pairs because the source lists the same component with the same copy in two places (kept so the folder counts match the original structure):
Super 6 grid (TOF_v1/02 = MOF/08) · Departures (TOF_v1/07 = MOF/05) · Brand quote (TOF_v1/08 = MOF/14) · Price (MOF/02 = MOF/13).

## What is in here besides the creatives
- `contact-sheets/` — one labelled sheet per folder; every PNG appears once (INDEX.txt).
- `font-comparison/` — MOF v3 rendered with Montserrat (as its source declares) beside the DM Sans fallback the supplied HTML would have produced.
- `evidence/` — the reproduction of the original failure (A as-is = transparent; B `left:0` only = still transparent; C full override = content) and one capture from the patched original exporter.
- `render-report.json`, `validation.json`, `MAPPING_expected-source-output.csv` (expected entry → source file/component → delivered file, dimensions, SHA-256, status).
- `MANIFEST.csv` — path, dimensions, bytes, SHA-256 for every file in this package.

## Before publishing
The copy carries prices, departure dates, review figures, awards and inclusions that were **not** re-verified for this package — see `FACTS_TO_VERIFY.md` in the source package. Two are known to differ from the live website (the 14-Day departure list and the meal counts) and one from Trustpilot's current data.
