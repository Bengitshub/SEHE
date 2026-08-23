# Google Ads creatives — campaigns landing on /journeys

Round 1: three concepts x three required ratios + the two logo assets.
Regenerate any time with:

    python3 creatives/google-journeys/build.py
    PW_PATH=file://<scratchpad>/node_modules/playwright-core/index.mjs \
      node creatives/google-journeys/shot.mjs

| File | Size | Google asset slot |
|---|---|---|
| `sehe-journeys-{a,b,c}-land.jpg` | 1200x628 | Landscape image (1.91:1) |
| `sehe-journeys-{a,b,c}-sq.jpg` | 1200x1200 | Square image (1:1) |
| `sehe-journeys-{a,b,c}-port.jpg` | 960x1200 | Portrait image (4:5, Demand Gen) |
| `sehe-journeys-logo-1x1.png` | 1200x1200 | Logo (1:1) |
| `sehe-journeys-logo-4x1.png` | 1200x300 | Logo (4:1) |

Concepts:
- **A scenic** — signature TranzAlpine/Craigieburn photograph (the train is
  visible mid-frame), "The South Island, by rail & coach." CTA: Compare the
  Journeys. WTA line as the footer.
- **B departure board** — the homepage board identity: navy, date-first white
  rows with green "Now Booking" pills, "Now booking through to April 2028."
  CARRIES REAL DATES (16 Nov 2026 / 30 Nov 2026 / 10 Jul 2027): regenerate
  when a listed date passes or sells out; the April 2028 horizon holds until
  the 2028/29 season releases.
- **C award-led** — WTA 2025 winner shield, "New Zealand's Leading Tour
  Operator", 2022-2025, Trustpilot 5-star strip + Rated "Excellent". Proof
  assets are the ones already published on the site; confirm paid-media
  usage rights before spend (WTA winner marks + Trustpilot brand assets).

Copy rules honoured: "fully guided ... journeys by rail & coach", no
"small groups", no prices (evergreen). All type/colours/photography match
the live site so the ad and the landing page read as one thing.

The full Performance Max build sheet (settings, verified text assets,
conversions, audience signal, launch checklist) lives in `pmax/`.
