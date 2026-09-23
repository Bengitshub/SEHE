# SEHE Creatives — editable sources (2026-09-23)

## What the creatives are
Every creative is a **React component written in JSX**, styled inline, laid out at its ad's exact pixel size, using the real photographs, logos and badges in `assets/`. There is no build step: the browser loads React, ReactDOM and Babel Standalone and transpiles the `.jsx` files as the page opens. Nothing here is an image-editor file. (The Canva design lives separately in the client's Canva account and is not part of this source.)

## Folders
- `source-original/` — the 49 supplied files **verbatim** (13 code/html files + 36 image assets). Untouched.
- `source-offline/` — the same 49 files with **only** the dependency URLs changed to local copies, plus:
  - `vendor/` — React 18.3.1, ReactDOM 18.3.1, Babel Standalone 7.29.0, html-to-image 1.11.11, JSZip 3.10.1. The React/ReactDOM/Babel files match the SRI hashes in the original HTML byte for byte.
  - `fonts/` — self-hosted woff2 (latin) for Lora, DM Sans, DM Mono **and Montserrat**, with `fonts.css`. The original loaded fonts from Google Fonts at runtime and never loaded Montserrat (see "Fonts" below).
  - `harness.html` — the page the replacement exporter drives: every creative (119 + 13 extras) at native size, with strict image-decode and font-load checks.
  - `Download Ads (patched).html` — the original browser exporter with the two proven fixes applied and labelled PATCH 1 / PATCH 2. The unpatched original is still there as `Download Ads.html`.
- `tools/` — the replacement exporter (`export-all.mjs`), validator, contact-sheet builder, and the scripts that proved the two defects (`reproduce.mjs`, `collision-probe.mjs`, `patched-check.mjs`).
- `docs/supplied/` — the documents as received. `docs/DESIGN_SYSTEM_FINDING.md`, `docs/HANDOVER_DOC_CORRECTION_NOTE.md`, `docs/FACTS_TO_VERIFY.md` — written for this handover.
- `MAPPING_expected-source-output.csv`, `MANIFEST.csv`.

## Setup (works offline)
```
cd source-offline
python3 -m http.server 8765          # Babel fetches .jsx over HTTP; file:// will not work
# open http://localhost:8765/index.html                  the design canvas (all sets, Tweaks panel)
# open http://localhost:8765/Download%20Ads%20(patched).html   the browser exporter, fixed
```
To export with the replacement exporter (Node 18+, playwright-core, a Chromium binary, Python 3 + Pillow) see `tools/run-export.sh`.

## Why the original export was blank — two proven causes
1. **Offscreen capture stage.** `Download Ads.html` hides `#stage` with `position:fixed; left:-99999px`. html-to-image copies those computed styles into its clone, so the content is drawn 99,999px outside the frame: every PNG is fully transparent. Reproduced with the original code path. Resetting `left:0` alone does **not** fix it (still transparent); `position:static; left:0; top:0` does. → PATCH 1.
2. **Identifier collision (`V3`).** `mof-v3.jsx` keeps its colour tokens in `const V3 = {…}`; the exporter declares `const V3 = [ …id list… ]` for the MOF v3 section. Babel Standalone compiles both to global `var`s, so the exporter's list overwrites the token object before rendering: pills lose their green, the navy poster field disappears, gold accents go. The design canvas (`index.html`) does not declare `V3` and renders correctly, which is why this was never seen. Proved with `collision-probe.mjs`. → PATCH 2 (rename to `V3LIST`). Without it, the 29 MOF v3 files would have exported wrong even after fix 1.

## Fonts
The creatives use **Lora + DM Sans** (DM Mono in one helper). `mof-v3.jsx` alone declares `HEAD = 'Montserrat', 'DM Sans'` and says Montserrat is "loaded via index.html" — it is not, in any supplied page, so MOF v3 rendered in the DM Sans fallback. `source-offline/` loads Montserrat so MOF v3 renders as its source declares; `harness.html?nomontserrat=1` reproduces the as-supplied fallback. No other set was changed.

## External dependencies (all vendored in `source-offline/`; the original fetched them at runtime)
React 18.3.1 · ReactDOM 18.3.1 · @babel/standalone 7.29.0 · html-to-image 1.11.11 · JSZip 3.10.1 (browser exporter only) · Google Fonts: Lora, DM Sans, DM Mono (+ Montserrat for MOF v3). Replacement exporter additionally: Node 18+, playwright-core, Chromium, Python 3, Pillow.

## Not included (not supplied)
`SEHE_Creative_and_Copy_Pack_2026-09-24.pdf` and its editable source · the separate TOF copy PDF/spreadsheet · Pinnacle reporting documents · the `previews/` older snapshot and `originals-supplied/` raw uploads (omitted by the sender to reduce upload size) · the Canva design.
