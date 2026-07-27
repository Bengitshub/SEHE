#!/usr/bin/env python3
"""Winter 2026 is sold out (worker feed: next=null, 5/5 soldout, 27 Jul 2026).

Across every tour page that lists it in the "Still comparing tours?" grid:
  - move the winter-2026 card to LAST position,
  - bake the sold-out state (red status pill, sold-out next-block, "—" count),
  - add a note pointing at the 2027 Winter Edition,
  - teach the live enhancement script to honour a per-card data-sold-note, so
    the card keeps saying "2027 season now booking" instead of the generic
    "New season opening soon" once the worker data lands.

Enhance-only philosophy preserved: the baked HTML is now correct on its own,
and the script only ever refines it.

Usage: python3 tools/winter2026-soldout.py [--apply]
"""
import re
import sys
import os
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# tour pages that carry a winter-2026 compare card, with their preview twins
PAGES = [
    ('SEHE-14day-tour_v22.txt',          'sehe-14day-page-complete.html'),
    ('SEHE-11day-2627-tour_v20.txt',     'sehe-11day-2627-page-complete.html'),
    ('SEHE-12day-winter-2027-tour_v13.txt', 'sehe-12day-winter-2027-page-complete.html'),
    ('SEHE-pinnacle-2027-tour_v13.txt',  'sehe-pinnacle-2027-page-complete.html'),
    ('SEHE-11day-2728-tour_v15.txt',     'sehe-11day-2728-page-complete.html'),
    ('SEHE-14day-2728-tour_v24.txt',     'sehe-14day-2728-page-complete.html'),
]

CARD_RE = re.compile(
    r'   <article class="journey-card[^"]*" data-season="winter" data-tour="winter-2026">.*?\n   </article>\n',
    re.S)

W2027 = 'https://www.siredmundhillaryexplorer.com/2027-winter-edition-tours'

SOLD_NOTE = (
    '     <p class="journey-card-soldnote"><strong>2026 season sold out.</strong> '
    'Every 2026 Winter Edition departure has now been filled. The 12-Day Winter Edition '
    f'returns next winter &mdash; <a href="{W2027}">see the 2027 departures</a>.</p>\n')

# ---- exact strings we rewrite inside the moved card -------------------------
SUBS = [
    # red status pill
    ('<span class="journey-card-status"><span class="journey-card-status-dot"></span>Now Booking</span>',
     '<span class="journey-card-status journey-card-status-sold"><span class="journey-card-status-dot"></span>Sold Out</span>'),
    # sold-out next block, carrying the note the live script will reuse
    ('<div class="journey-card-next" data-next-placeholder="">',
     '<div class="journey-card-next journey-card-next-soldout" data-next-placeholder="" data-sold-note="2027 season now booking">'),
    ('<span class="journey-card-next-label">Now Booking</span>',
     '<span class="journey-card-next-label">Season Complete</span>'),
    ('<span class="journey-card-next-date">Departures available &mdash; see tour</span>',
     '<span class="journey-card-next-date">2027 season now booking</span>'),
    ('<span class="journey-card-next-date">Departures available — see tour</span>',
     '<span class="journey-card-next-date">2027 season now booking</span>'),
]

# departures fact -> em dash, matching what the live script computes for 0 available
FACT_RE = re.compile(r'(<span class="journey-card-fact-value" data-departure-value="">)[^<]*(</span>)')

CSS_ANCHOR = '  .journey-card-next-soldout { border-left-color: var(--red); }\n'
CSS_ADD = CSS_ANCHOR + (
    '  .journey-card-status-sold { background: rgba(184, 64, 64, 0.95); }\n'
    '  .journey-card-status-sold .journey-card-status-dot { animation: none; }\n'
    "  .journey-card-soldnote { margin: 0 0 14px !important; padding: 10px 12px; background: rgba(184, 64, 64, 0.06); border-left: 3px solid var(--red); font-family: 'Open Sans', sans-serif !important; font-size: 13px !important; line-height: 1.5 !important; color: var(--navy) !important; }\n"
    '  .journey-card-soldnote a { color: var(--navy) !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 2px; }\n')

SCRIPT_OLD = "placeholder.querySelector('.journey-card-next-date').textContent = 'New season opening soon';"
SCRIPT_NEW = "placeholder.querySelector('.journey-card-next-date').textContent = (placeholder.getAttribute('data-sold-note') || 'New season opening soon');"

ENTRY = """       v{v} — WINTER 2026 SOLD OUT. The 12-Day Winter Edition 2026 is fully
            booked (worker feed: 5 of 5 departures sold, no next date), so in
            the "Still comparing tours?" grid its card moves to the LAST
            position and now ships the sold-out state baked in: red "Sold Out"
            pill, sold-out next-block reading "Season Complete / 2027 season
            now booking", an em-dash departure count, and a note pointing to
            the 2027 Winter Edition. The card, its brochure link and the tour
            page all stay live. The availability script now honours a per-card
            data-sold-note, so a sold-out tour can name its successor season
            instead of the generic "New season opening soon".\n"""


def transform_card(card: str) -> str:
    out = card
    for old, new in SUBS:
        if old in out:
            out = out.replace(old, new)
    out = FACT_RE.sub(r'\1&mdash;\2', out, count=1)
    assert 'journey-card-status-sold' in out, 'status pill not rewritten'
    assert 'journey-card-next-soldout' in out, 'next block not rewritten'
    assert 'data-sold-note' in out, 'sold note attribute missing'
    if 'journey-card-soldnote' not in out:
        out = out.replace('     <div class="journey-card-actions">',
                          SOLD_NOTE + '     <div class="journey-card-actions">', 1)
    assert 'journey-card-soldnote' in out, 'sold note paragraph not inserted'
    return out


def process(path: str, preview: str):
    src = open(os.path.join(REPO, path), encoding='utf-8').read()
    before_articles = src.count('<article class="journey-card')

    m = CARD_RE.search(src)
    assert m, f'{path}: winter-2026 card not found'
    card = m.group(0)

    # 1) remove it from its current slot
    body = src[:m.start()] + src[m.end():]
    # 2) transform, then re-insert as the LAST card of that grid
    card = transform_card(card)
    tail = body.rfind('   </article>\n')
    assert tail > 0, f'{path}: no trailing article to append after'
    insert_at = tail + len('   </article>\n')
    body = body[:insert_at] + card + body[insert_at:]

    # 3) CSS + script upgrades
    assert CSS_ANCHOR in body, f'{path}: CSS anchor missing'
    if '.journey-card-status-sold' not in body.split('</style>')[0] or 'journey-card-soldnote {' not in body:
        body = body.replace(CSS_ANCHOR, CSS_ADD, 1)
    assert SCRIPT_OLD in body, f'{path}: sold-out script branch missing'
    body = body.replace(SCRIPT_OLD, SCRIPT_NEW)

    # 4) version bump + changelog
    vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
    assert vm, f'{path}: VERSION header not found'
    nv = str(int(vm.group(1)) + 1)
    body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
    body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY.format(v=nv), body, count=1)

    # ---- invariants ---------------------------------------------------------
    assert body.count('<article class="journey-card') == before_articles, 'card count changed'
    order = re.findall(r'article class="journey-card[^"]*" data-season="[a-z-]*" data-tour="([a-z0-9-]*)"', body)
    assert order[-1] == 'winter-2026', f'{path}: winter-2026 is not last -> {order}'
    assert body.count('<div') == src.count('<div') + SOLD_NOTE.count('<div'), 'div balance drifted'
    assert body.count('<p class="journey-card-soldnote"') == 1, 'sold note duplicated'

    newname = re.sub(r'_v\d+\.txt$', f'_v{nv}.txt', path)
    if APPLY:
        open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
        open(os.path.join(REPO, preview), 'w', encoding='utf-8').write(body)
        if newname != path:
            os.remove(os.path.join(REPO, path))
        print(f'  APPLIED {path} -> {newname}  (order: ...{", ".join(order[-2:])})')
    else:
        print(f'  ok {path} -> {newname}  (order: {", ".join(order)})')


if __name__ == '__main__':
    print('WINTER 2026 SOLD-OUT SWEEP' + ('  [APPLY]' if APPLY else '  [dry run]'))
    for p, prev in PAGES:
        process(p, prev)
    print('done.')
