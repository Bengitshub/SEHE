#!/usr/bin/env python3
"""Homepage — add the Brochure Collection band (section 8b).

Ben (voice note, 31 Jul): campaigns land people on the homepage, so it needs a
brochure form of its own — but framed the OPPOSITE way to the tour pages. Tour
pages say "get this tour's brochure" and the collection is the happy surprise;
the homepage says up front: one form, you get access to EVERY brochure.

Mechanics (this is why no new Zapier webhook is needed): exactly the tour-page
sandwich. This band ships an HTML fallback form (GET -> /brochure-collection,
Phase-2-flippable) plus the standard hidden .sehe-form-slot. Ben copies the SAME
native Duda form element onto the homepage in a row below the widget; the
docking script — extracted verbatim from the live 14-day master so it is
byte-identical to the proven one — moves it into the slot on the published site
and the fallback form hides. Same form element = same webhook/automations.

Also retargets the hero's "View Tour Brochures" ghost button from #journeys to
the new #brochures band — it finally has a real destination.

Placement: between 8. GUESTS (paper) and 9. BOOKING (paper-deep), as a navy
interruption — story, film and quotes have done their work; this is the "decide
at home" offer, with booking right below for the ready.

Usage: python3 tools/homepage-brochure.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-homepage_v32.txt'
PREVIEW = 'sehe-homepage-complete.html'
TOUR = 'SEHE-14day-tour_v29.txt'  # docking-script donor (resolved by glob below)

import glob
tour_hits = glob.glob(os.path.join(REPO, 'SEHE-14day-tour_v*.txt'))
assert len(tour_hits) == 1, tour_hits
TOUR = tour_hits[0]

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
tour = open(TOUR, encoding='utf-8').read()
src = body

# ---- 0. lift the PROVEN docking script from the live 14-day master ----------
DOCK_RE = re.compile(r'<script>\s*\n\s*\(function\(\) \{\s*\n\s*/\* Brochure form DOCKING.*?\n\}\)\(\);\n</script>', re.S)
dm = DOCK_RE.search(tour)
assert dm, 'docking script not found in 14-day master'
DOCK = dm.group(0)
assert 'data-sehe-form-slot' in DOCK and 'sehe-form-docked' in DOCK
# sanitizer: no "<" glued to a word character anywhere in the script body
assert not re.search(r'<[A-Za-z](?!script)', DOCK.replace('<script>', '').replace('</script>', '')), 'dock script not sanitizer-safe'

COVERS = [
    ('https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/Web_2027+Winter+Tour+Brochure_SEHE-1-1920w.webp',
     'Winter Edition 2027 tour brochure cover'),
    ('https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/26-27+Spring-Summer+Tour_Brochure-Cover-1920w.webp',
     '14-Day Spring/Summer tour brochure cover'),
    ('https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/Web_Pinnacle+Tour_Brochure_January+2027-1-1920w.webp',
     'Pinnacle Tour brochure cover'),
]
# the pinnacle cover URL above must exist in the pinnacle master (typo guard)
pin = open(glob.glob(os.path.join(REPO, 'SEHE-pinnacle-2027-tour_v*.txt'))[0], encoding='utf-8').read()
if COVERS[2][0] not in pin:
    real = re.search(r'sehe-brochure-cover-img" src="([^"]+)"', pin).group(1)
    COVERS[2] = (real, COVERS[2][1])
for u, _ in COVERS:
    assert u.startswith('https://lirp.cdn-website.com/'), u

CSS = '''
  /* ---- 8b. BROCHURE COLLECTION (navy capture band) ---- */
  .shx-broch { background: var(--ink); }
  .shx-broch-card { display: grid; grid-template-columns: 0.92fr 1.08fr; max-width: 1080px; margin: 0 auto; background: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,.32); }
  .shx-broch-coverside { position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px; background: var(--paper); border-right: 1px solid var(--paper-line); padding: 52px 34px; }
  .shx-broch-fan { position: relative; width: 100%; max-width: 320px; aspect-ratio: 5 / 4; }
  .shx-broch-fan img { position: absolute; top: 50%; left: 50%; width: 52%; border-radius: 6px; box-shadow: 0 14px 30px rgba(13,32,54,.28); border: 1px solid rgba(13,32,54,.08); }
  .shx-broch-fan img:nth-child(1) { transform: translate(-92%, -50%) rotate(-9deg); }
  .shx-broch-fan img:nth-child(3) { transform: translate(-8%, -50%) rotate(9deg); }
  .shx-broch-fan img:nth-child(2) { transform: translate(-50%, -54%); width: 56%; z-index: 2; box-shadow: 0 20px 44px rgba(13,32,54,.38); }
  .shx-broch-badge { display: inline-flex; align-items: center; gap: 8px; font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 1.2px; text-transform: uppercase; color: var(--ink) !important; background: #ffffff; border: 1px solid var(--gold); border-radius: 20px; padding: 8px 16px; }
  .shx-broch-formside { padding: 50px 48px 44px; text-align: left; }
  .shx-broch-title { font-family: 'Montserrat', sans-serif !important; font-size: clamp(26px, 3vw, 33px) !important; font-weight: 600 !important; letter-spacing: -0.2px; line-height: 1.16 !important; color: var(--ink) !important; margin: 0 0 12px !important; }
  .shx-broch-sub { font-size: 16.5px !important; line-height: 1.65 !important; color: var(--body-soft) !important; margin: 0 0 26px !important; max-width: 52ch; }
  .shx-broch-sub strong { color: var(--body-ink); }
  .shx-broch-fine { margin: 14px 0 0 !important; font-size: 13px !important; letter-spacing: .3px; color: var(--body-soft) !important; }
  /* fallback form fields (hidden once the native Duda form docks) */
  .sehe-brochure-form { display: block !important; }
  .sehe-brochure-form .field { display: block !important; margin-bottom: 14px !important; }
  .sehe-brochure-form .field:last-of-type { margin-bottom: 0 !important; }
  .sehe-brochure-form label.field-label { display: block !important; font-family: 'Montserrat', sans-serif !important; font-size: 11px !important; font-weight: 700 !important; color: var(--body-ink) !important; text-transform: uppercase !important; letter-spacing: 1.2px !important; margin: 0 0 7px 0 !important; line-height: 1.3 !important; }
  .sehe-brochure-form input[type="text"], .sehe-brochure-form input[type="email"], .sehe-brochure-form select { display: block !important; width: 100% !important; padding: 13px 16px !important; background: #ffffff !important; border: 1px solid var(--paper-line) !important; border-radius: 6px !important; font-family: 'Open Sans', sans-serif !important; font-size: 15px !important; color: var(--body-ink) !important; line-height: 1.4 !important; -webkit-appearance: none !important; appearance: none !important; outline: none !important; margin: 0 !important; box-sizing: border-box !important; transition: border-color .2s ease, box-shadow .2s ease !important; }
  .sehe-brochure-form input:hover, .sehe-brochure-form select:hover { border-color: var(--gold) !important; }
  .sehe-brochure-form input:focus, .sehe-brochure-form select:focus { border-color: var(--ink) !important; box-shadow: 0 0 0 3px rgba(13,32,54,.1) !important; }
  .sehe-brochure-form input::placeholder { color: #8a93a3 !important; opacity: 1 !important; }
  .sehe-brochure-form select { padding-right: 44px !important; background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8' fill='none'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%230d2036' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") !important; background-repeat: no-repeat !important; background-position: right 16px center !important; background-size: 12px 8px !important; cursor: pointer !important; color: #8a93a3 !important; }
  .sehe-brochure-form select.has-value { color: var(--body-ink) !important; }
  .sehe-brochure-form button[type="submit"] { display: block !important; width: 100% !important; padding: 17px 24px !important; background: var(--ink) !important; border: 1.5px solid var(--ink) !important; color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; font-size: 13px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 1.4px !important; border-radius: 6px !important; cursor: pointer !important; margin: 22px 0 0 0 !important; line-height: 1 !important; -webkit-appearance: none !important; appearance: none !important; transition: background .2s ease, box-shadow .2s ease !important; }
  .sehe-brochure-form button[type="submit"]:hover { background: var(--ink-soft) !important; box-shadow: 0 6px 18px rgba(13,32,54,.3) !important; }
  /* docked native Duda form: fit rules (skin CSS travels inside the widget) */
  .sehe-form-slot { display: block; }
  .sehe-form-slot .dmform { max-width: none !important; margin: 0 !important; padding: 0 !important; }
  .sehe-form-slot .dmform-wrapper { padding: 0 !important; }
  .sehe-form-slot .dmform-title { display: none !important; }
  .sehe-form-slot .dmformsubmit { float: none !important; width: 100% !important; margin: 22px 0 0 0 !important; }
  .sehe-form-slot .dmformsubmit input[type="submit"] { display: block !important; width: 100% !important; box-sizing: border-box !important; }
  .shx-broch-formside.sehe-form-docked .sehe-brochure-form { display: none !important; }
  @media (max-width: 1020px) {
    .shx-broch-card { grid-template-columns: 1fr; }
    .shx-broch-coverside { border-right: none; border-bottom: 1px solid var(--paper-line); padding: 44px 28px 36px; }
  }
  @media (max-width: 540px) {
    .shx-broch-formside { padding: 34px 22px 32px; }
    .shx-broch-fan { max-width: 260px; }
    .shx-broch-sub { font-size: 15.5px !important; }
  }
'''

HTML = '''  <!-- ============ 8b. BROCHURE COLLECTION ============ -->
  <section class="shx-broch shx-band" id="brochures">
    <div class="shx-wrap">
      <div class="shx-broch-card">
        <div class="shx-broch-coverside">
          <div class="shx-broch-fan" aria-hidden="true">
            <img src="{c0}" alt="" loading="lazy">
            <img src="{c1}" alt="" loading="lazy">
            <img src="{c2}" alt="" loading="lazy">
          </div>
          <span class="shx-broch-badge">7 Journeys &middot; Free PDF Downloads</span>
        </div>
        <div class="shx-broch-formside">
          <span class="shx-kicker">The Brochure Collection</span>
          <h2 class="shx-broch-title">Every brochure, one form.</h2>
          <p class="shx-broch-sub">Fill this in once and you unlock <strong>the complete collection</strong>: all seven journey brochures, with full itineraries, inclusions, season pricing and departure dates. Compare them at home, at your own pace.</p>
          <form class="sehe-brochure-form" action="/brochure-collection" method="get" novalidate="">
            <div class="field"><input type="text" name="dmform-1" placeholder="Name" autocomplete="name" required=""></div>
            <div class="field"><input type="email" name="dmform-3" placeholder="Email" autocomplete="email" required=""></div>
            <div class="field">
              <label class="field-label" for="seheHomeCountry">Country of Residence</label>
              <select name="dmform-2" id="seheHomeCountry" required="">
                <option value="" selected="" disabled="" hidden="">Select your country</option>
                <option value="Australia">Australia</option>
                <option value="United States">United States</option>
                <option value="New Zealand">New Zealand</option>
                <option value="India">India</option>
                <option value="Canada">Canada</option>
                <option value="United Kingdom">United Kingdom</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <button type="submit">Get the Brochure Collection</button>
          </form>
          <div class="sehe-form-slot" data-sehe-form-slot hidden></div>
          <p class="shx-broch-fine">Instant access &middot; no obligation &middot; every journey in one place</p>
        </div>
      </div>
    </div>
  </section>
{dock}
<script>
  (function() {{
  /* Brochure fallback form: submitting continues to the brochure collection
     page. Hidden automatically once the native Duda form docks in its place. */
  var form = document.querySelector('.shx-broch .sehe-brochure-form');
  if (!form) return;
  var sel = form.querySelector('select[name="dmform-2"]');
  if (sel) {{
    sel.addEventListener('change', function() {{
      if (this.value) this.classList.add('has-value');
      else this.classList.remove('has-value');
    }});
  }}
  form.addEventListener('submit', function(e) {{
    e.preventDefault();
    window.location.href = '/brochure-collection';
  }});
}})();
</script>
'''.format(c0=COVERS[0][0], c1=COVERS[1][0], c2=COVERS[2][0], dock=DOCK)

# ---- 1. CSS in the main sheet, just above the responsive block --------------
CSS_ANCHOR = '  /* ============ RESPONSIVE ============ */'
assert body.count(CSS_ANCHOR) == 1
body = body.replace(CSS_ANCHOR, CSS + '\n' + CSS_ANCHOR, 1)

# ---- 2. section between GUESTS and BOOKING ----------------------------------
HTML_ANCHOR = '  <!-- ============ 9. BOOKING YOUR JOURNEY ============ -->'
assert body.count(HTML_ANCHOR) == 1
body = body.replace(HTML_ANCHOR, HTML + '\n' + HTML_ANCHOR, 1)

# ---- 3. hero ghost button finally gets a real destination -------------------
BTN_OLD = 'href="#journeys" aria-label="View tour brochures'
assert body.count(BTN_OLD) == 1
body = body.replace(BTN_OLD, 'href="#brochures" aria-label="View tour brochures', 1)

# ---- 4. version + changelog -------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — BROCHURE COLLECTION BAND added (Ben): new section 8b between
            Guests and Booking — navy band, white two-column card: fanned
            covers (winter 2027 / 14-day 26-27 / pinnacle) + badge on the left,
            form on the right. Framed the OPPOSITE way to tour pages: one form,
            access to ALL seven brochures, said up front. Ships the HTML
            fallback form (continues to /brochure-collection; Phase-2
            flippable) plus the standard .sehe-form-slot; the docking script is
            lifted VERBATIM from the live 14-day master, so when the native
            Duda form widget (the same form element as the tour pages = same
            webhook/automations, no new Zapier work) is pasted below this
            widget it docks in and the fallback hides. Hero's "View Tour
            Brochures" ghost button retargeted #journeys -> #brochures.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants -------------------------------------------------------------
assert body.count('<section class="shx-broch') == 1
assert body.count('data-sehe-form-slot') == 2  # slot div + dock script selector
assert body.count('sehe-brochure-form') >= 4   # form, CSS rules, helper
for tag in ('div', 'section', 'style', 'script'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, f'<{tag}> {o} open vs {c} close'
# every inline script stays sanitizer-safe
for sm in re.finditer(r'<script>(.*?)</script>', body, re.S):
    bad = re.search(r'<[A-Za-z]', sm.group(1))
    assert not bad, f'sanitizer hazard: {sm.group(1)[max(0,bad.start()-40):bad.start()+20]!r}'
print(f'  em-dashes: {src.count("&mdash;")} -> {body.count("&mdash;")}')

newname = f'SEHE-homepage_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run)')
