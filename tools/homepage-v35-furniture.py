#!/usr/bin/env python3
"""Homepage v35 — furniture-text crawl (Ben): cut or fix the utility lines.

Ben's example: the departure board's foot line "Dates update live from our
booking system. See every journey and departure →". Verdict: the whole line
goes — "booking system" is behind-the-scenes narration, and the link is
redundant twice over (the rail's end-cap card says "See every journey →" and
the full journeys section is the very next scroll).

Full crawl verdicts (the reply to Ben lists them):
  CUT   board foot line + its two CSS rules.
  FIX   finder foot: "Request it on the journey page and it arrives by email"
        was the long way round now the page has its own brochure form — point
        it at #brochures instead.
  TRIM  brochure fine print: "every journey in one place" repeats the
        headline ("Every brochure, one form.").
  KEEP  seasons Pinnacle note, Super 6 trains note, Trustpilot line, board
        sub + live next-departure line, end-cap, hero call line.

Usage: python3 tools/homepage-v35-furniture.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-homepage_v34.txt'
PREVIEW = 'sehe-homepage-complete.html'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body

R = [
    # CUT: the board foot line, whole
    ('      <p class="shx-depboard-foot">Dates update live from our booking system. <a href="/journeys">See every journey and departure &rarr;</a></p>\n',
     ''),
    # CUT: its now-orphaned CSS
    ('  .shx-depboard-foot { margin: 4px 0 0 !important; font-size: 15px !important; color: var(--body-soft) !important; }\n', ''),
    ('  .shx-depboard-foot a { color: var(--ink) !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 3px; }\n', ''),
    # FIX: finder foot points at this page's own brochure band now
    ('<p>Every journey&rsquo;s <strong>brochure is free</strong>. Request it on the journey page and it arrives by email straight away.</p>',
     '<p>Every journey&rsquo;s <strong>brochure is free</strong>. <a href="#brochures">Get the full collection below</a>.</p>'),
    # TRIM: fine print no longer repeats the band headline
    ('<p class="shx-broch-fine">Instant access &middot; no obligation &middot; every journey in one place</p>',
     '<p class="shx-broch-fine">Instant access &middot; no obligation</p>'),
]

for old, new in R:
    n = body.count(old)
    assert n == 1, f'expected 1 occurrence, got {n}: {old[:80]}...'
    body = body.replace(old, new, 1)
print(f'  {len(R)} edits applied')

assert 'depboard-foot' not in body, 'board foot survived somewhere'
assert 'booking system' not in body

# finder foot needs its link styled like its old plain text (the foot p had no
# anchor before) — give it the page's standard inline-link treatment
OLDCSS = '.shx-finder-foot p { font-size: 15.5px !important; color: var(--body-soft) !important; }'
NEWCSS = ('.shx-finder-foot p { font-size: 15.5px !important; color: var(--body-soft) !important; }\n'
          '  .shx-finder-foot p a { color: var(--ink) !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 3px; }')
if OLDCSS in body:
    body = body.replace(OLDCSS, NEWCSS, 1)
else:
    fm = re.search(r'\.shx-finder-foot p \{[^}]*\}', body)
    assert fm, 'finder-foot p CSS not found'
    body = body.replace(fm.group(0), fm.group(0) + '\n  .shx-finder-foot p a { color: var(--ink) !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 3px; }', 1)

# ---- version + changelog ----------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — FURNITURE-TEXT CRAWL (Ben): the board's foot line ("Dates
            update live from our booking system. See every journey and
            departure") CUT whole — behind-the-scenes narration, and the link
            duplicated both the rail's end-cap card and the journeys section
            directly below. Finder foot no longer sends people to a journey
            page for the brochure ("Get the full collection below" -> the
            page's own #brochures band). Brochure fine print trimmed ("every
            journey in one place" repeated the band headline). Everything else
            audited and kept deliberately: seasons Pinnacle note, Super 6
            trains note, Trustpilot review line, board sub + live
            next-departure line, end-cap, hero call line.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants -------------------------------------------------------------
for tag in ('div', 'section', 'style', 'script'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, f'<{tag}> {o} open vs {c} close'
for sm in re.finditer(r'<script>(.*?)</script>', body, re.S):
    assert not re.search(r'<[A-Za-z]', sm.group(1)), 'sanitizer hazard'

newname = f'SEHE-homepage_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run)')
