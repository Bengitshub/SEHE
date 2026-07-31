#!/usr/bin/env python3
"""Homepage v38 — restore the brochure-band CSS + de-AI the crawl texts (Ben).

TWO jobs:

1. REGRESSION FIX. The v37 board regeneration strips everything between the
   board CSS marker and the RESPONSIVE marker — and the v33 brochure-band CSS
   had been inserted exactly there, so v37 shipped the band unstyled. The
   chunk (recovered byte-for-byte from v36, minus the .shx-broch-fine rule
   whose element is being cut) is re-inserted ABOVE the board marker, outside
   the strip zone, so future regens cannot eat it again. The generator gains
   a matching assert.

2. TEXT PASS (Ben): "work on the AI 'One form' comments... 'Browse the
   brochure collection' like a human home page, not AI. 'View the brochure
   collection' not get... 'Instant access · no obligation' - this is
   terrible. remove it... less statement driven... Don't adjust headings,
   only crawl texts" (the brochure h2 IS the one-form comment he names, so it
   changes; every other heading stays).

Usage: python3 tools/homepage-v38-humantext.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-homepage_v37.txt'
PREVIEW = 'sehe-homepage-complete.html'
CHUNK = '/tmp/claude-0/-home-user-SEHE/0cc36833-90aa-502d-8b8c-c61310a548dd/scratchpad/broch-css-chunk.txt'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body

# ---- 1. restore the band CSS, out of the board's strip zone -----------------
chunk = open(CHUNK, encoding='utf-8').read()
assert chunk.startswith('  /* ---- 8b. BROCHURE COLLECTION')
assert '.shx-broch-card {' in chunk and '.sehe-form-slot .dmform {' in chunk
FINE_RULE = '  .shx-broch-fine { margin: 14px 0 0 !important; font-size: 13px !important; letter-spacing: .3px; color: var(--body-soft) !important; }\n'
assert FINE_RULE in chunk
chunk = chunk.replace(FINE_RULE, '', 1)
assert '.shx-broch-card {' not in body, 'band CSS already present?'
BOARD_CSS = '\n  /* ============ 1b. DEPARTURE BOARD ============ */'
assert body.count(BOARD_CSS) == 1
body = body.replace(BOARD_CSS, '\n' + chunk.rstrip() + BOARD_CSS, 1)

# ---- 2. the text pass -------------------------------------------------------
R = [
    # Ben's explicit brochure-band fixes
    ('<h2 class="shx-broch-title">Every brochure, one form.</h2>',
     '<h2 class="shx-broch-title">Browse the brochure collection.</h2>'),
    ('<p class="shx-broch-sub">Fill this in once and you unlock <strong>the complete collection</strong>: all seven journey brochures, with full itineraries, inclusions, season pricing and departure dates. Compare them at home, at your own pace.</p>',
     '<p class="shx-broch-sub">All seven journey brochures in one place, with full itineraries, inclusions, season pricing and departure dates. Fill in the short form and browse them at home in your own time.</p>'),
    ('<button type="submit">Get the Brochure Collection</button>',
     '<button type="submit">View the Brochure Collection</button>'),
    ('          <p class="shx-broch-fine">Instant access &middot; no obligation</p>\n', ''),
    # same voice where the band is referenced
    ('<p>Every journey&rsquo;s <strong>brochure is free</strong>. <a href="#brochures">Get the full collection below</a>.</p>',
     '<p>Every journey&rsquo;s <strong>brochure is free</strong>. <a href="#brochures">Browse the brochure collection below</a>.</p>'),
    ('<p>Browse the <a href="#journeys">journeys above</a>, or request a free brochure from any journey page; it arrives by email straight away.</p>',
     '<p>Browse the <a href="#journeys">journeys above</a>, or <a href="#brochures">view the brochure collection</a>.</p>'),
    # crawl: fragment-statement cadence in body texts (headings untouched)
    ('<p class="shx-seasons-intro">The same mountains, two very different seasons. Every journey above runs in one of them.</p>',
     '<p class="shx-seasons-intro">Every journey runs in one of two seasons, and the South Island feels very different in each.</p>'),
    ('over Tekapo. The South Island&rsquo;s quieter, cosier season: our 12-day Winter Editions.</p>',
     'over Tekapo. Winter is the South Island&rsquo;s quieter, cosier season, and our 12-day Winter Editions run right through it.</p>'),
    ('<p class="shx-film-sub">Steam, steel and the South Island rolling past the window &mdash; a quiet minute in the company of the Explorer.</p>',
     '<p class="shx-film-sub">A quiet minute on board, with the South Island rolling past the window.</p>'),
]
for old, new in R:
    n = body.count(old)
    assert n == 1, f'expected 1 occurrence, got {n}: {old[:80]}...'
    body = body.replace(old, new, 1)
print(f'  {len(R)} text edits applied')

# the changelog header may lawfully mention the old phrases; the PAGE may not
page = body[body.find('<style'):]
assert 'one form' not in page.lower()
assert 'Instant access' not in page
assert 'broch-fine' not in page
assert 'unlock' not in page.lower()

# ---- version + changelog ----------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — BAND CSS RESTORED + HUMAN-TEXT PASS (Ben). Regression fix:
            the v37 board regen strips [board-CSS .. RESPONSIVE] and the v33
            brochure CSS lived exactly there, so v37 rendered the band
            unstyled; the chunk is back, now ABOVE the board marker where
            regens cannot reach it. Text pass: "Every brochure, one form." ->
            "Browse the brochure collection."; sub rewritten without
            "unlock"/statement cadence; button "Get" -> "View the Brochure
            Collection" (matches the docked native form); "Instant access -
            no obligation" fine print DELETED (rule + element); finder foot
            and booking step 1 now say "browse/view the brochure collection"
            instead of sending people to journey pages; seasons intro and
            winter-card tail recast as sentences; film sub loses the
            "Steam, steel" triad. Headings elsewhere untouched.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants -------------------------------------------------------------
for tag in ('div', 'section', 'style', 'script'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, f'<{tag}> {o} open vs {c} close'
for sm in re.finditer(r'<script>(.*?)</script>', body, re.S):
    assert not re.search(r'<[A-Za-z]', sm.group(1)), 'sanitizer hazard'
assert body.count('.shx-broch-card {') == 2  # base rule + 1020px stack override
assert body.count('&mdash;') <= src.count('&mdash;')

newname = f'SEHE-homepage_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run)')
