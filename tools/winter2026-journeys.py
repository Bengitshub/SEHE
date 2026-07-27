#!/usr/bin/env python3
"""Winter 2026 sold out — Journeys index page.

Same treatment as the tour pages' compare grid, plus the two things unique to
this page: the inline SOLDOUT schedule (which drives the per-card date
calendar) and the baked calendar chips themselves.

Usage: python3 tools/winter2026-journeys.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-journeys-page_v15.txt'
PREVIEW = 'sehe-journeys-page-complete.html'
W2027 = 'https://www.siredmundhillaryexplorer.com/2027-winter-edition-tours'

src = open(os.path.join(REPO, SRC), encoding='utf-8').read()
body = src

# ---- 1. the schedule: every 2026 winter departure is now sold ---------------
OLD_SOLD = "    'winter-2026': ['2026-06-27','2026-07-18'],"
NEW_SOLD = "    'winter-2026': ['2026-06-27','2026-07-18','2026-08-01','2026-09-05','2026-09-12'],"
assert OLD_SOLD in body, 'SOLDOUT winter-2026 line not found'
body = body.replace(OLD_SOLD, NEW_SOLD, 1)

# ---- 2. lift the winter-2026 card out --------------------------------------
CARD_RE = re.compile(
    r'   <article class="journey-card[^"]*" data-season="winter" data-tour="winter-2026">.*?\n   </article>\n', re.S)
m = CARD_RE.search(body)
assert m, 'winter-2026 card not found'
card = m.group(0)
body = body[:m.start()] + body[m.end():]

# ---- 3. bake the sold-out state into the card ------------------------------
card, n = re.subn(r'<span class="journey-card-status">(\s*)<span class="journey-card-status-dot">(\s*)</span>(\s*)Now Booking(\s*)</span>',
                  r'<span class="journey-card-status journey-card-status-sold">\1<span class="journey-card-status-dot">\2</span>\3Sold Out\4</span>', card, count=1)
assert n == 1, 'status pill not rewritten'

card, n = re.subn(r'<div class="journey-card-next" data-next-placeholder="">',
                  '<div class="journey-card-next journey-card-next-soldout" data-next-placeholder="" data-sold-note="2027 season now booking">', card, count=1)
assert n == 1, 'next block not rewritten'

card, n = re.subn(r'(<span class="journey-card-next-label">\s*)Now Booking(\s*</span>)', r'\1Season Complete\2', card, count=1)
assert n == 1, 'next label not rewritten'
card, n = re.subn(r'(<span class="journey-card-next-date">\s*)Departures available [^<]*?(\s*</span>)', r'\g<1>2027 season now booking\2', card, count=1)
assert n == 1, 'next date not rewritten'

# every remaining bookable chip in this card's calendar becomes sold
card, n = re.subn(r'<span>(\d{1,2})</span>', r'<span class="jc-day-sold" title="Sold out">\1</span>', card)
print(f'  calendar chips marked sold: {n}')
assert '<span>' not in card.split('journey-card-departures')[1].split('jc-legend')[0], 'a bookable chip survived'

# departures fact -> em dash (what the live script computes for zero available)
card, n = re.subn(r'(<span class="journey-card-fact-value" data-departure-value="">\s*)[^<]*?(\s*</span>)', r'\1&mdash;\2', card, count=1)
assert n == 1, 'departure count not rewritten'

SOLD_NOTE = ('     <p class="journey-card-soldnote"><strong>2026 season sold out.</strong> '
             'Every 2026 Winter Edition departure has now been filled. The 12-Day Winter Edition '
             f'returns next winter &mdash; <a href="{W2027}">see the 2027 departures</a>.</p>\n')
card, n = re.subn(r'(\s*)<div class="journey-card-actions">', '\n' + SOLD_NOTE + r'\1<div class="journey-card-actions">', card, count=1)
assert n == 1, 'sold note not inserted'

# ---- 4. re-insert as the LAST card ----------------------------------------
tail = body.rfind('   </article>\n')
assert tail > 0
body = body[:tail + len('   </article>\n')] + card + body[tail + len('   </article>\n'):]

# ---- 5. CSS + script upgrades ---------------------------------------------
# this page's CSS is pretty-printed, one declaration per line
CSS_ANCHOR = '  .journey-card-next-soldout {\n    border-left-color: var(--red);\n  }\n'
assert CSS_ANCHOR in body, 'CSS anchor missing'
body = body.replace(CSS_ANCHOR, CSS_ANCHOR + (
    '  .journey-card-status-sold {\n'
    '    background: rgba(184, 64, 64, 0.95);\n'
    '  }\n'
    '  .journey-card-status-sold .journey-card-status-dot {\n'
    '    animation: none;\n'
    '  }\n'
    '  .journey-card-soldnote {\n'
    '    margin: 0 0 14px !important;\n'
    '    padding: 10px 12px;\n'
    '    background: rgba(184, 64, 64, 0.06);\n'
    '    border-left: 3px solid var(--red);\n'
    "    font-family: 'Open Sans', sans-serif !important;\n"
    '    font-size: 13px !important;\n'
    '    line-height: 1.5 !important;\n'
    '    color: var(--navy) !important;\n'
    '  }\n'
    '  .journey-card-soldnote a {\n'
    '    color: var(--navy) !important;\n'
    '    font-weight: 700;\n'
    '    text-decoration: underline !important;\n'
    '    text-underline-offset: 2px;\n'
    '  }\n'), 1)

SCRIPT_OLD = "placeholder.querySelector('.journey-card-next-date').textContent = 'New season opening soon';"
SCRIPT_NEW = "placeholder.querySelector('.journey-card-next-date').textContent = (placeholder.getAttribute('data-sold-note') || 'New season opening soon');"
assert SCRIPT_OLD in body, 'script branch missing'
body = body.replace(SCRIPT_OLD, SCRIPT_NEW)

# ---- 6. version + changelog ------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm, 'VERSION header not found'
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — WINTER 2026 SOLD OUT. All five 2026 Winter Edition departures are
            now filled (worker feed agrees: no next date). SOLDOUT schedule
            updated to the full five dates, every calendar chip on that card
            renders red, the card moves to the END of the grid, and it ships
            the sold-out state baked in: red "Sold Out" pill, "Season Complete
            / 2027 season now booking", em-dash count, and a note linking to
            the 2027 Winter Edition. Card, brochure link and tour page all stay
            live. The availability script now honours a per-card data-sold-note
            so a sold-out tour can name its successor season.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants ------------------------------------------------------------
order = re.findall(r'article class="journey-card[^"]*" data-season="[a-z-]*" data-tour="([a-z0-9-]*)"', body)
assert order[-1] == 'winter-2026', f'winter-2026 not last: {order}'
assert body.count('<article class="journey-card') == src.count('<article class="journey-card')
assert body.count('<p class="journey-card-soldnote"') == 1
print(f'  order: {", ".join(order)}')

newname = f'SEHE-journeys-page_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'  APPLIED -> {newname}')
else:
    print(f'  ok -> {newname} (dry run)')
