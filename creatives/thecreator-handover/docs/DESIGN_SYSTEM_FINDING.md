# Design-system finding: which system the creative sources actually use

_Prepared 23 Sep 2026 from the supplied source files. Nothing was restyled._

## The discrepancy that was raised

| Document | Type system | Navy | Gold |
|---|---|---|---|
| `SEHE_Creative_System_Spec.md` (supplied) | Lora / DM Sans | `#1a3a5c` | `#b8935a` |
| `SEHE_Creative_and_Copy_Pack_2026-09-24.pdf` (not supplied) | Montserrat / Open Sans | `#153b67` | `#c8a56c` |

## What the sources use — verified in code and in the rendered output

**The creatives are built on the Spec's system: Lora + DM Sans, navy `#1a3a5c`, gold `#b8935a`.**

Evidence:
- `index.html` and `Download Ads.html` define `--seh-navy:#1a3a5c`, `--seh-gold:#b8935a`, `--seh-cream:#f6f1e6`, `--seh-green:#2f6e4a` and load only Lora, DM Sans and DM Mono from Google Fonts.
- Across the six creative files there are 94 `fontFamily: 'Lora…'` and 49 `fontFamily: 'DM Sans…'` declarations; `mof-v3.jsx` hard-codes the same hex values in its `V3` token object.
- The render report from the replacement exporter lists the faces every creative actually loaded: **Lora 400/500 (+ italics) and DM Sans 400–700** for every set, with one exception below.
- Neither `#153b67` nor `#c8a56c` nor "Open Sans" appears anywhere in the creative sources.

## The one exception: MOF v3

`mof-v3.jsx` declares `const HEAD = "'Montserrat', 'DM Sans', sans-serif"` and its header comment says "Montserrat 600 headings, Lora reserved for the wordmark/serif accents … (loaded via index.html)". **But no supplied HTML page loads Montserrat.** So, as supplied, the MOF v3 set's eyebrows, pills, captions and proof lines rendered in the DM Sans fallback; only the file's *intent* was Montserrat. Serif headlines (Lora) are unaffected.

Resolution applied in this package, and made explicit:
- The offline source copy and the replacement exporter load Montserrat (weights 400–800) alongside the original three families, so MOF v3 renders as its source declares. The render report confirms `Montserrat 400/600/700` loaded for every MOF v3 file and for no other set.
- `out/font-comparison/MOFv3_font_comparison.png` shows three MOF v3 creatives both ways (intended Montserrat vs as-supplied DM Sans fallback). Pixel difference is 0.3–9% per creative, confined to the sans elements.
- No other set was changed. Brand TOF, 14-Day and PMax sets remain Lora + DM Sans exactly as they were.

## Interpretation

The two documents describe two different systems that both exist:
- **Lora / DM Sans / `#1a3a5c` / `#b8935a`** is the **ad-creative** system (the Spec, and the sources).
- **Montserrat / Open Sans / `#153b67` / `#c8a56c`** is the **website** system (the live siredmundhillaryexplorer.com pages use exactly these values).

MOF v3 is a partial bridge between them (Montserrat headings on the ad palette). The PDF appears to have described the website's system as if it were the creative system. This is a documentation error, not a reason to restyle the creatives.
