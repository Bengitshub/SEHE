#!/usr/bin/env python3
"""Winter 2026 landing page — sold-out state.

Ben left the treatment to me. Decision: keep the page fully live and indexed
(it still earns the "winter 2026" searches), but make the sold-out status
unmissable and route the intent to Winter 2027:

  1. a sold-out band immediately under the hero — status pill, plain-English
     explanation, and a primary CTA to the 2027 Winter Edition;
  2. the hero ticket's Departures cell reads "Sold out / 2027 season now
     booking" instead of a departure count;
  3. the hero-ticket script becomes sold-out aware, so it can no longer
     "helpfully" repaint a count over the sold-out wording when the worker
     data lands (previously it fell back to showing all 5 dates);
  4. the dates section says plainly that these dates are gone.

The brochure form stays exactly as it is — a sold-out season is still a good
lead: those people are the 2027 buyers.

Usage: python3 tools/winter2026-ownpage.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-12day-winter-2026-tour_v20.txt'
PREVIEW = 'sehe-12day-winter-2026-page-complete.html'
W2027 = 'https://www.siredmundhillaryexplorer.com/2027-winter-edition-tours'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body

# ---- 1. sold-out band, injected right after the hero -----------------------
BAND = '''
<!-- ===== 1b. 2026 season sold out ===== -->
<style>
  .sehe-tourpage .sehe-soldout-band { background: #153b67; }
  .sehe-tourpage .sehe-soldout-inner { max-width: 1240px; margin: 0 auto; padding: 30px 32px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 20px 32px; }
  .sehe-tourpage .sehe-soldout-copy { flex: 1 1 640px; }
  .sehe-tourpage .sehe-soldout-mark { display: inline-flex; align-items: center; gap: 8px; font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 2.2px; text-transform: uppercase; color: #fff !important; background: rgba(184, 64, 64, 0.95); padding: 7px 14px; border-radius: 20px; margin-bottom: 14px; }
  .sehe-tourpage .sehe-soldout-copy h2 { font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 23px !important; line-height: 1.25 !important; letter-spacing: -0.2px; color: #fff !important; margin: 0 0 8px !important; }
  .sehe-tourpage .sehe-soldout-copy p { font-family: 'Open Sans', sans-serif !important; font-size: 15px !important; line-height: 1.65 !important; color: rgba(255, 255, 255, 0.82) !important; margin: 0 !important; max-width: 62ch; }
  .sehe-tourpage .sehe-soldout-actions { display: flex; flex-wrap: wrap; gap: 12px; }
  .sehe-tourpage .sehe-soldout-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-family: 'Montserrat', sans-serif !important; font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 1.2px; text-decoration: none !important; padding: 15px 24px; border-radius: 4px; border: 1.5px solid #c8a56c; white-space: nowrap; }
  .sehe-tourpage .sehe-soldout-btn--primary { background: #c8a56c; color: #0d2036 !important; }
  .sehe-tourpage .sehe-soldout-btn--ghost { background: transparent; color: #fff !important; }
  @media (max-width: 860px) {
    .sehe-tourpage .sehe-soldout-inner { padding: 24px 20px; gap: 16px; }
    .sehe-tourpage .sehe-soldout-copy h2 { font-size: 19px !important; }
    .sehe-tourpage .sehe-soldout-copy p { font-size: 14.5px !important; }
    .sehe-tourpage .sehe-soldout-actions { width: 100%; }
    .sehe-tourpage .sehe-soldout-btn { width: 100%; }
  }
</style>
<div class="sehe-tourpage">
  <section class="sehe-soldout-band" aria-label="The 2026 Winter Edition is sold out">
    <div class="sehe-soldout-inner">
      <div class="sehe-soldout-copy">
        <span class="sehe-soldout-mark">2026 Season Sold Out</span>
        <h2>Every 2026 Winter Edition departure is now fully booked</h2>
        <p>All five departures between June and September 2026 have sold. The 12-Day Winter Edition returns next winter with six departures from July to September 2027 &mdash; the same journey, the same snow-covered South Island.</p>
      </div>
      <div class="sehe-soldout-actions">
        <a class="sehe-soldout-btn sehe-soldout-btn--primary" href="''' + W2027 + '''">View the 2027 Winter Edition</a>
        <a class="sehe-soldout-btn sehe-soldout-btn--ghost" href="#tour-brochure">Get the Brochure</a>
      </div>
    </div>
  </section>
</div>

'''

HERO_END = '  </section>\n</div>\n\n\n<!-- ===== 2. What sets this tour apart ===== -->'
assert HERO_END in body, 'hero end anchor not found'
if 'sehe-soldout-band' not in body:
    body = body.replace(HERO_END, '  </section>\n</div>\n' + BAND + '\n<!-- ===== 2. What sets this tour apart ===== -->', 1)

# ---- 2. hero ticket cell ---------------------------------------------------
OLD_TICKET = '<div class="sehe-hx-k">Departures</div><div class="sehe-hx-v"><span data-sehe-dep-count>1</span><small data-sehe-dep-range>Sep 2026</small></div>'
NEW_TICKET = '<div class="sehe-hx-k">Departures</div><div class="sehe-hx-v"><span data-sehe-dep-count>Sold out</span><small data-sehe-dep-range>2027 season now booking</small></div>'
assert OLD_TICKET in body, 'hero ticket cell not found'
body = body.replace(OLD_TICKET, NEW_TICKET, 1)

# ---- 3. make the hero-ticket script sold-out aware -------------------------
OLD_PAINT = """    var avail = d.all.filter(function(x){ return x && x.status !== 'soldout'; });
    var all = avail.length ? avail : d.all;
    var cEl = document.querySelector('[data-sehe-dep-count]');
    if (cEl) cEl.textContent = all.length;
    var rEl = document.querySelector('[data-sehe-dep-range]');
    if (rEl) {"""
NEW_PAINT = """    var avail = d.all.filter(function(x){ return x && x.status !== 'soldout'; });
    var all = avail.length ? avail : d.all;
    var cEl = document.querySelector('[data-sehe-dep-count]');
    var rEl = document.querySelector('[data-sehe-dep-range]');
    /* Sold-out season: never repaint a departure count over the sold-out
       wording — the baked cell is already correct and more useful. */
    if (!avail.length) {
      if (cEl) cEl.textContent = 'Sold out';
      if (rEl) rEl.innerHTML = '2027 season now booking';
      return;
    }
    if (cEl) cEl.textContent = all.length;
    if (rEl) {"""
assert OLD_PAINT in body, 'hero paint block not found'
body = body.replace(OLD_PAINT, NEW_PAINT, 1)

# ---- 4. dates section framing ---------------------------------------------
OLD_DATES = '''     <span class="sehe-section-eyebrow">Available Dates</span>
     <h2 class="sehe-section-heading">Choose your departure</h2>'''
NEW_DATES = '''     <span class="sehe-section-eyebrow">2026 Departures</span>
     <h2 class="sehe-section-heading">The 2026 season has sold out</h2>
     <p class="sehe-soldout-dates-note">Every date below is fully booked. The same journey runs again next winter &mdash; <a href="''' + W2027 + '''">see the 2027 Winter Edition departures</a>.</p>'''
assert OLD_DATES in body, 'dates header not found'
body = body.replace(OLD_DATES, NEW_DATES, 1)

DATES_CSS_ANCHOR = '  <section class="sehe-booking-section" id="tour-dates">'
DATES_CSS = """<style>
  .sehe-tourpage .sehe-soldout-dates-note { font-family: 'Open Sans', sans-serif !important; font-size: 15px !important; line-height: 1.6 !important; color: #51617a !important; margin: 14px 0 0 !important; }
  .sehe-tourpage .sehe-soldout-dates-note a { color: #153b67 !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 2px; }
</style>
"""
if 'sehe-soldout-dates-note {' not in body:
    body = body.replace(DATES_CSS_ANCHOR, DATES_CSS + DATES_CSS_ANCHOR, 1)

# ---- 5. version + changelog ------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm, 'VERSION header not found'
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — 2026 SEASON SOLD OUT. All five departures are filled (worker feed:
            no next date). The page stays live and indexed, but now says so
            plainly: a sold-out band under the hero with the explanation and a
            primary CTA to the 2027 Winter Edition; the hero ticket's
            Departures cell reads "Sold out / 2027 season now booking"; the
            dates section is retitled "The 2026 season has sold out" with a
            link across to 2027. The hero-ticket script is now sold-out aware —
            previously, with zero available dates it fell back to painting the
            full count (5) over the cell, which read as availability. Brochure
            form untouched: a sold-out season still makes a good 2027 lead.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants ------------------------------------------------------------
assert body.count('<section class="sehe-soldout-band"') == 1
assert body.count('sehe-soldout-btn--primary') == 2, 'expect one CSS rule + one button'
assert body.count('<div') - body.count('</div>') == src.count('<div') - src.count('</div>'), 'div balance drifted'
assert body.count('<section') - body.count('</section>') == src.count('<section') - src.count('</section>'), 'section balance drifted'
assert 'Sold out' in body

newname = f'SEHE-12day-winter-2026-tour_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run); band+ticket+script+dates all matched')
