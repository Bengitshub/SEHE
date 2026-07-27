#!/usr/bin/env python3
"""Journeys page — add a hero above everything, in the homepage's language.

Ben: "Redesign the journeys page to include a hero above everything that
currently exists. Something similar to the home page, but maybe use the eyebrow,
heading and subheading texts in the hero and the rest stays about the same."

So the page's existing header block (eyebrow / "All Upcoming Tours" / intro
paragraph) is lifted out of the body and becomes the hero's content, and the
old header block is removed so nothing is said twice. Everything below —
inclusions strip, Trustpilot line, filters, cards — is untouched.

Two deliberate calls:
  * Height. The homepage hero is full-screen; this one is ~72vh with a 560px
    floor. This page's job is comparison, and a full-screen hero would push
    every card below the fold. It still reads as a hero, but the first cards
    peek.
  * Logo. Same trick as the homepage: the site header ships a transparent
    placeholder and only swaps in the real roundel on scroll, so the brand is
    invisible on load. The white roundel sits in the header's logo lane.

Usage: python3 tools/journeys-hero.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-journeys-page_v16.txt'
PREVIEW = 'sehe-journeys-page-complete.html'

HERO_IMG = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/Coastal-Pacific_North-of-Claverly--KR.webp'
LOGO = 'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/SEH+Explorer_logo+white-350w.png'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body

# ---- 1. lift the existing header's three texts ------------------------------
m = re.search(r'  <div class="sehe-journeys-header">\s*'
              r'<span class="sehe-journeys-eyebrow">\s*(?P<eyebrow>.*?)\s*</span>\s*'
              r'<h2>\s*(?P<title>.*?)\s*</h2>.*?'
              r'<p>\s*(?P<sub>.*?)\s*</p>\s*</div>\n', body, re.S)
assert m, 'journeys header block not found'
eyebrow, title, sub = m.group('eyebrow'), m.group('title'), m.group('sub')
print(f'  eyebrow : {eyebrow}')
print(f'  title   : {title}')
print(f'  sub     : {sub[:70]}...')

# remove the old header (its content now lives in the hero)
body = body[:m.start()] + body[m.end():]
assert 'sehe-journeys-header">' not in body, 'header block survived'

HERO = f'''<!-- ═══ HERO ═══ -->
<style>
  /* Duda: keep the hosting row from boxing or clipping a full-bleed hero, and
     stop the theme rule ".dmFullRowRespTmpl section{{padding:50px 40px}}" from
     re-padding it. */
  #dm .dmContent .dmRespRow, #dm .dmContent .dmRespColsWrapper, #dm .dmContent .dmRespCol {{ overflow: visible !important; max-width: none !important; }}
  #dm .dmContent .dmCustomHtml {{ overflow: visible !important; }}
  .sehe-jhero, .sehe-jhero *, .sehe-jhero *::before, .sehe-jhero *::after {{ box-sizing: border-box; }}
  .sehe-jhero {{
    position: relative; width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw);
    padding: 0 !important; min-height: max(560px, 72vh); min-height: max(560px, 72svh);
    display: flex; align-items: flex-end; background-color: #081525;
    background-image: linear-gradient(180deg, rgba(8,21,37,.62) 0%, rgba(8,21,37,.26) 28%, rgba(8,21,37,.58) 56%, rgba(8,21,37,.95) 100%), url('{HERO_IMG}');
    background-size: cover; background-position: center 46%;
  }}
  /* the site header's logo slot is a transparent placeholder until you scroll —
     put the real roundel in its lane so the brand is there on load */
  .sehe-jhero-logo {{ position: absolute; top: 26px; left: 0; width: 16.66%; height: 92px; object-fit: contain; object-position: center; z-index: 2; filter: drop-shadow(0 2px 10px rgba(8,21,37,.5)); }}
  .sehe-jhero-inner {{ position: relative; width: 100%; max-width: 1240px; margin: 0 auto; padding: 150px 30px 58px; }}
  .sehe-jhero-eyebrow {{ display: inline-flex; align-items: center; gap: 16px; font-family: 'Montserrat', sans-serif !important; font-size: 13.5px !important; font-weight: 700 !important; letter-spacing: .42em; text-transform: uppercase; color: #c8a56c !important; margin: 0 0 22px !important; text-shadow: 0 1px 12px rgba(8,21,37,.95); }}
  .sehe-jhero-eyebrow::before, .sehe-jhero-eyebrow::after {{ content: ''; width: 44px; height: 1px; background: #c8a56c; flex: none; }}
  .sehe-jhero h1 {{ font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: clamp(40px, 5.2vw, 68px) !important; line-height: 1.06 !important; letter-spacing: -0.01em; color: #ffffff !important; margin: 0 !important; text-shadow: 0 2px 26px rgba(8,21,37,.55); }}
  .sehe-jhero-sub {{ font-family: 'Open Sans', sans-serif !important; margin: 26px 0 0 !important; max-width: 640px; font-size: clamp(16.5px, 1.5vw, 19px) !important; line-height: 1.65 !important; color: rgba(255,255,255,.94) !important; text-shadow: 0 1px 14px rgba(8,21,37,.6); }}
  @media (max-width: 860px) {{
    .sehe-jhero {{ min-height: max(480px, 64svh); background-position: center 50%; }}
    .sehe-jhero-inner {{ padding: 118px 22px 44px; }}
    .sehe-jhero-logo {{ left: 50%; width: auto; transform: translateX(-50%); top: 18px; height: 56px; }}
    /* the flanking rules float mid-line once the eyebrow wraps */
    .sehe-jhero-eyebrow {{ gap: 0; font-size: 11px !important; letter-spacing: .26em; margin-bottom: 16px !important; }}
    .sehe-jhero-eyebrow::before, .sehe-jhero-eyebrow::after {{ display: none; }}
    .sehe-jhero h1 {{ font-size: 34px !important; line-height: 1.14 !important; }}
    .sehe-jhero-sub {{ font-size: 16px !important; line-height: 1.55 !important; margin-top: 16px !important; }}
  }}
  @media (max-width: 540px) {{
    .sehe-jhero {{ min-height: max(440px, 60svh); }}
    .sehe-jhero-inner {{ padding: 104px 18px 38px; }}
    .sehe-jhero h1 {{ font-size: 30px !important; }}
  }}
</style>
<section class="sehe-jhero" aria-label="{title}">
  <img class="sehe-jhero-logo" src="{LOGO}" alt="Sir Edmund Hillary Explorer" loading="eager">
  <div class="sehe-jhero-inner">
    <span class="sehe-jhero-eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="sehe-jhero-sub">{sub}</p>
  </div>
</section>

'''

# ---- 2. drop the hero in above everything ----------------------------------
ANCHOR = ' <div class="sehe-journeys">'
assert ANCHOR in body, 'journeys container not found'
body = body.replace(ANCHOR, HERO + ANCHOR, 1)

# the grid now sits under a hero — it no longer needs its own big top padding
sub_n = body.count('padding: 48px 30px 60px;')
assert sub_n == 1, f'container padding rule not unique ({sub_n})'
body = body.replace('padding: 48px 30px 60px;', 'padding: 54px 30px 60px;', 1)

# ---- 3. version + changelog ------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — HERO ADDED above everything (Ben), in the homepage's language:
            full-bleed photograph, the SEHE roundel in the site header's logo
            lane so the brand is visible on load, and the page's own eyebrow,
            heading and intro paragraph lifted up into it. The old
            .sehe-journeys-header block is removed so nothing is said twice;
            the inclusions strip, Trustpilot line, filters and cards below are
            untouched. Hero runs ~72vh rather than the homepage's full screen —
            this page exists to compare tours, and a full-screen hero would
            push every card below the fold. Photograph is the Coastal Pacific
            north of Claverley, chosen so the page does not read as a copy of
            the homepage hero.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants ------------------------------------------------------------
assert body.count('<section class="sehe-jhero"') == 1
assert body.count('<h1>') == 1, 'expected exactly one h1 on the page'
assert body.count('sehe-journeys-eyebrow') == src.count('sehe-journeys-eyebrow') - 1
assert body.count('<div') - body.count('</div>') == src.count('<div') - src.count('</div>'), 'div balance drifted'
assert body.count('<section') - body.count('</section>') == src.count('<section') - src.count('</section>') + 0, 'section balance drifted'
for tag in ('div', 'section', 'style', 'script'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, f'<{tag}> {o} open vs {c} close'

newname = f'SEHE-journeys-page_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run)')
