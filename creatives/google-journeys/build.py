#!/usr/bin/env python3
"""Google Ads image creatives — campaigns landing on /journeys.

Three concepts, each at the three ratios Performance Max / Display / Demand
Gen ask for, plus the two logo assets. Built from the LIVE site's design
system (same hexes, fonts, photography, badges) so the ad and the landing
page read as one thing — the scent trail from click to page never breaks.

  A  scenic    — signature TranzAlpine photograph, headline, CTA
  B  board     — the departure-board identity: navy, date-first rows, pills
  C  award     — proof-led: WTA shield, 2022-2025, Trustpilot, CTA

Sizes: landscape 1200x628 (1.91:1), square 1200x1200 (1:1), portrait
960x1200 (4:5); logo 1200x1200 (1:1) and 1200x300 (4:1).

Outputs HTML to the scratchpad; creatives/google-journeys/shot.mjs renders
them to JPG/PNG at exact pixel size. Copy follows the site's accuracy rules:
"fully guided ... by rail & coach", no "small groups", no prices (keeps the
set evergreen). Concept B carries real dates — refresh when they pass.

Usage: python3 creatives/google-journeys/build.py
"""
import base64
import hashlib
import os
import re
import subprocess

SCRATCH = '/tmp/claude-0/-home-user-SEHE/0cc36833-90aa-502d-8b8c-c61310a548dd/scratchpad'
OUT = os.path.join(SCRATCH, 'adpages')
CACHE = os.path.join(SCRATCH, 'adcache')
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

IMG = {
    'hero':    'https://irp.cdn-website.com/35e9f777/dms3rep/multi/TranzAlpine--View-of-Cragieburn-Range-across-Lake-Sarah--CLEM1410_-43.050997-171.773006--CROP.webp',
    'logo':    'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/SEH+Explorer_logo+white-350w.png',
    'shield':  'https://irp.cdn-website.com/35e9f777/dms3rep/multi/new-zealands-leading-tour-operator-2025-winner-shield-256-816b3264.png',
    'tp':      'https://irp.cdn-website.com/35e9f777/dms3rep/multi/Trustpilot_ratings_5star-RGB.png',
}


def fetch(url):
    key = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest())
    if not os.path.exists(key) or os.path.getsize(key) < 200:
        subprocess.run(['curl', '-sL', '--max-time', '60', url, '-o', key], check=True)
    data = open(key, 'rb').read()
    assert len(data) > 200, f'fetch failed: {url}'
    mime = 'image/png' if '.png' in url.lower() else ('image/webp' if '.webp' in url.lower() else 'image/jpeg')
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


D = {k: fetch(u) for k, u in IMG.items()}

# ---- fonts: Google css2 -> woff2 data URIs ----------------------------------
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
css = subprocess.run(['curl', '-sL', '-A', UA, '--max-time', '60',
                      'https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap'],
                     capture_output=True, text=True, check=True).stdout
assert '@font-face' in css, 'font css fetch failed'
# keep only latin subsets (the last block of each family/weight covers latin)
faces = re.findall(r'/\* (\S+) \*/\s*(@font-face \{[^}]+\})', css)
keep = [f for sub, f in faces if sub == 'latin']
fontcss = '\n'.join(keep)
for wurl in set(re.findall(r'url\((https://fonts\.gstatic\.com[^)]+)\)', fontcss)):
    fontcss = fontcss.replace(wurl, fetch(wurl.strip()))
assert 'fonts.gstatic.com' not in fontcss

BASE = f'''<meta charset="utf-8">
<style>
{fontcss}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ --ink: #0d2036; --ink-deep: #081525; --gold: #c8a56c; --gold-light: #d4b37e;
        --paper: #f7f1e6; --paper-line: #d8cbb0; --cream: #f3ecdd; --green: #2a7a4a; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; }}
body {{ font-family: 'Open Sans', sans-serif; }}
.mont {{ font-family: 'Montserrat', sans-serif; }}
.stage {{ position: relative; width: 100vw; height: 100vh; overflow: hidden; }}
.eyebrow {{ font-family: 'Montserrat', sans-serif; font-weight: 700; letter-spacing: .3em;
           text-transform: uppercase; color: var(--gold); display: inline-flex; align-items: center; gap: 14px; }}
.eyebrow::before {{ content: ''; width: 34px; height: 2px; background: var(--gold); }}
.cta {{ display: inline-block; font-family: 'Montserrat', sans-serif; font-weight: 700;
       text-transform: uppercase; background: var(--gold); color: var(--ink); border-radius: 6px; }}
.pill {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(42,122,74,.95); color: #fff;
        font-family: 'Montserrat', sans-serif; font-weight: 700; text-transform: uppercase; border-radius: 999px; }}
.pill i {{ width: 8px; height: 8px; background: #fff; border-radius: 50%; }}
</style>
'''

# ============================ CONCEPT A — SCENIC =============================
def concept_a(w, h, cls):
    port = cls == 'port'
    land = cls == 'land'
    logo_h = 64 if land else 84
    pad = 56 if land else 72
    h1 = 62 if land else (86 if not port else 74)
    sub = 24 if land else 30
    eb = 17 if land else 21
    cta_fs = 19 if land else 23
    grad = 'linear-gradient(180deg, rgba(8,21,37,.30) 0%, rgba(8,21,37,.06) 30%, rgba(8,21,37,.52) 62%, rgba(8,21,37,.94) 100%)'
    return BASE + f'''
<div class="stage" style="background-image:{grad},url('{D['hero']}'); background-size:cover; background-position:center 42%;">
  <img src="{D['logo']}" style="position:absolute; top:{pad-12}px; left:{pad}px; height:{logo_h}px; filter:drop-shadow(0 2px 10px rgba(8,21,37,.55));">
  <div style="position:absolute; left:{pad}px; right:{pad}px; bottom:{pad}px;">
    <span class="eyebrow" style="font-size:{eb}px; margin-bottom:{18 if land else 26}px; color:var(--gold-light); text-shadow:0 1px 4px rgba(8,21,37,.95), 0 2px 18px rgba(8,21,37,.9);">Sir Edmund Hillary Explorer</span>
    <div class="mont" style="font-weight:700; font-size:{h1}px; line-height:1.06; letter-spacing:-0.01em; color:#fff; text-shadow:0 2px 26px rgba(8,21,37,.55); max-width:{'12ch' if not land else '16ch'};">The South Island, by rail &amp; coach.</div>
    <div style="font-weight:600; font-size:{sub}px; color:rgba(255,255,255,.94); margin-top:{14 if land else 20}px; text-shadow:0 1px 14px rgba(8,21,37,.6);">Seven fully guided journeys &middot; 11&ndash;15 days</div>
    <div style="margin-top:{24 if land else 34}px;">
      <span class="cta" style="font-size:{cta_fs}px; letter-spacing:.08em; padding:{'16px 28px' if land else '20px 36px'};">Compare the Journeys &rarr;</span>
    </div>
    <div style="margin-top:{22 if land else 30}px; padding-top:{16 if land else 22}px; border-top:1px solid rgba(255,255,255,.30); font-size:{15 if land else 18}px; color:rgba(255,255,255,.85);">
      World Travel Awards &middot; NZ&rsquo;s Leading Tour Operator 2022&ndash;2025
    </div>
  </div>
</div>
'''

# ========================= CONCEPT B — DEPARTURE BOARD =======================
ROWS = [
    ('16 Nov 2026', '14-Day Spring/Summer Tour'),
    ('30 Nov 2026', '11-Day Spring/Summer Tour'),
    ('10 Jul 2027', '12-Day Winter Edition'),
]

def concept_b(w, h, cls):
    land = cls == 'land'
    port = cls == 'port'
    pad = 56 if land else 72
    logo_h = 60 if land else 78
    h1 = 52 if land else (66 if not port else 58)
    row_date = 30 if land else 36
    row_name = 19 if land else 23
    row_pad = '18px 26px' if land else '24px 30px'
    pill_fs = 12 if land else 14
    cta_fs = 19 if land else 22
    gap = 14 if land else 18
    rows = '\n'.join(
        f'''<div style="background:#fff; border-radius:10px; padding:{row_pad}; display:flex; align-items:center; justify-content:space-between; gap:18px; border-left:6px solid var(--gold);">
              <div>
                <div class="mont" style="font-weight:700; font-size:{row_date}px; color:var(--ink); line-height:1.1;">{d}</div>
                <div style="font-weight:600; font-size:{row_name}px; color:#51617a; margin-top:4px;">{n}</div>
              </div>
              <span class="pill" style="font-size:{pill_fs}px; letter-spacing:.08em; padding:9px 16px 9px 13px;"><i></i>Now Booking</span>
            </div>''' for d, n in ROWS)
    if land:
        # landscape: headline + CTA left, the three rows right — 628px is not
        # tall enough to stack head, rows and CTA (v1 clipped the third row)
        return BASE + f'''
<div class="stage" style="background:linear-gradient(160deg, #081525 0%, #0d2036 70%, #13294a 100%); display:flex; align-items:center; gap:44px; padding:0 {pad}px;">
  <div style="flex:1 1 46%;">
    <img src="{D['logo']}" style="height:{logo_h}px; margin-bottom:26px;">
    <div><span class="eyebrow" style="font-size:16px; margin-bottom:12px;">Departures</span></div>
    <div class="mont" style="font-weight:700; font-size:{h1}px; line-height:1.12; letter-spacing:-0.01em; color:#fff;">Now booking through to April 2028.</div>
    <div style="margin-top:26px;"><span class="cta" style="font-size:{cta_fs}px; letter-spacing:.08em; padding:16px 28px;">Find Your Departure &rarr;</span></div>
    <div style="margin-top:20px; font-size:15px; color:rgba(243,236,221,.65);">siredmundhillaryexplorer.com</div>
  </div>
  <div style="flex:1 1 54%; display:flex; flex-direction:column; gap:{gap}px;">
    {rows}
  </div>
</div>
'''
    return BASE + f'''
<div class="stage" style="background:linear-gradient(160deg, #081525 0%, #0d2036 70%, #13294a 100%); display:flex; flex-direction:column; justify-content:center; padding:0 {pad}px;">
  <img src="{D['logo']}" style="position:absolute; top:{pad-10}px; left:{pad}px; height:{logo_h}px;">
  <div>
    <span class="eyebrow" style="font-size:19px; margin-bottom:20px;">Departures</span>
    <div class="mont" style="font-weight:700; font-size:{h1}px; line-height:1.1; letter-spacing:-0.01em; color:#fff; max-width:14ch;">Now booking through to April 2028.</div>
    <div style="display:flex; flex-direction:column; gap:{gap}px; margin-top:38px;">
      {rows}
    </div>
    <div style="margin-top:38px; display:flex; align-items:center; justify-content:space-between; gap:20px;">
      <span class="cta" style="font-size:{cta_fs}px; letter-spacing:.08em; padding:19px 34px;">Find Your Departure &rarr;</span>
      <span style="font-size:17px; color:rgba(243,236,221,.65);">siredmundhillaryexplorer.com</span>
    </div>
  </div>
</div>
'''

# ============================ CONCEPT C — AWARD ==============================
def concept_c(w, h, cls):
    land = cls == 'land'
    port = cls == 'port'
    shield_h = 190 if land else 250
    t1 = 46 if land else (60 if not port else 54)
    t2 = 18 if land else 22
    line = 22 if land else 27
    cta_fs = 19 if land else 22
    vpad = 52 if land else 84
    if land:
        # landscape: shield left, text right
        return BASE + f'''
<div class="stage" style="background:linear-gradient(160deg, #081525 0%, #0d2036 100%); display:flex; align-items:center; gap:56px; padding:{vpad}px 64px; border-top:6px double var(--gold); border-bottom:6px double var(--gold);">
  <img src="{D['shield']}" style="height:210px; flex:none; filter:drop-shadow(0 10px 30px rgba(0,0,0,.4));">
  <div>
    <div class="eyebrow" style="font-size:{t2}px;">World Travel Awards &middot; 2022&ndash;2025</div>
    <div class="mont" style="font-weight:700; font-size:48px; line-height:1.12; color:#fff; margin-top:14px; max-width:16ch;">New Zealand&rsquo;s Leading Tour Operator.</div>
    <div style="font-size:{line}px; color:rgba(243,236,221,.9); margin-top:14px;">Fully guided South Island journeys by rail &amp; coach.</div>
    <div style="display:flex; align-items:center; gap:18px; margin-top:26px;">
      <span class="cta" style="font-size:{cta_fs}px; letter-spacing:.08em; padding:16px 28px;">View the Journeys &rarr;</span>
      <img src="{D['tp']}" style="height:34px;">
      <span style="font-size:18px; font-weight:600; color:rgba(243,236,221,.9);">Rated &ldquo;Excellent&rdquo;</span>
    </div>
  </div>
  <img src="{D['logo']}" style="position:absolute; top:38px; right:52px; height:58px;">
</div>
'''
    return BASE + f'''
<div class="stage" style="background:linear-gradient(160deg, #081525 0%, #0d2036 100%); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:{vpad}px 80px; border-top:7px double var(--gold); border-bottom:7px double var(--gold);">
  <img src="{D['logo']}" style="height:78px; margin-bottom:{34 if port else 44}px;">
  <img src="{D['shield']}" style="height:{shield_h}px; filter:drop-shadow(0 10px 30px rgba(0,0,0,.4));">
  <div class="eyebrow" style="font-size:{t2}px; margin-top:{30 if port else 38}px;">World Travel Awards &middot; 2022&ndash;2025</div>
  <div class="mont" style="font-weight:700; font-size:{t1}px; line-height:1.12; color:#fff; margin-top:16px; max-width:14ch;">New Zealand&rsquo;s Leading Tour Operator.</div>
  <div style="font-size:{line}px; color:rgba(243,236,221,.9); margin-top:16px; max-width:26ch;">Fully guided South Island journeys by rail &amp; coach.</div>
  <div style="display:flex; align-items:center; gap:20px; margin-top:{30 if port else 40}px;">
    <span class="cta" style="font-size:{cta_fs}px; letter-spacing:.08em; padding:19px 34px;">View the Journeys &rarr;</span>
    <img src="{D['tp']}" style="height:40px;">
    <span style="font-size:20px; font-weight:600; color:rgba(243,236,221,.9);">Rated &ldquo;Excellent&rdquo;</span>
  </div>
</div>
'''

# ============================== LOGO ASSETS ==================================
LOGO_1x1 = BASE + f'''
<div class="stage" style="background:#0d2036; display:flex; align-items:center; justify-content:center;">
  <img src="{D['logo']}" style="width:58%;">
</div>
'''
LOGO_4x1 = BASE + f'''
<div class="stage" style="background:#0d2036; display:flex; align-items:center; justify-content:center; gap:34px;">
  <img src="{D['logo']}" style="height:66%;">
  <div class="mont" style="font-weight:700; font-size:64px; letter-spacing:.12em; color:#f3ecdd;">SIR EDMUND HILLARY <span style="color:var(--gold);">EXPLORER</span></div>
</div>
'''

SIZES = {'land': (1200, 628), 'sq': (1200, 1200), 'port': (960, 1200)}
pages = {}
for cls, (w, h) in SIZES.items():
    pages[f'a-{cls}'] = concept_a(w, h, cls)
    pages[f'b-{cls}'] = concept_b(w, h, cls)
    pages[f'c-{cls}'] = concept_c(w, h, cls)
pages['logo-1x1'] = LOGO_1x1
pages['logo-4x1'] = LOGO_4x1

for name, html in pages.items():
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(html)
print(f'{len(pages)} ad pages written to {OUT}')
