#!/usr/bin/env python3
"""Homepage v34 — journeys intro under the heading + section text-gap tightening.

Ben: "Let's put the text field in explore our journeys section, under the
heading. and let's ensure we are not giving too much space between text inside
sections."

1. The journeys intro paragraph sat BESIDE the heading (flex space-between,
   bottom-aligned right column). The head becomes plain flow: kicker, heading,
   then the paragraph directly under it.
2. Vertical-rhythm pass, desktop: the big head-to-content gaps (46-64px) come
   down to 30-44px; medium text gaps trimmed ~15-25%; hero untouched (Ben:
   the hero is good). Mobile overrides from the v15 compaction stay in place.

Usage: python3 tools/homepage-v34-spacing.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-homepage_v33.txt'
PREVIEW = 'sehe-homepage-complete.html'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body

R = [
    # ---- 1. journeys head: stack the intro under the heading ----------------
    ('.shx-journeys-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 24px; margin-bottom: 46px; }',
     '.shx-journeys-head { margin-bottom: 30px; }'),
    ('.shx-journeys-head p { max-width: 46ch; font-size: 17px !important; color: var(--body-soft) !important; }',
     '.shx-journeys-head p { max-width: 62ch; font-size: 17px !important; color: var(--body-soft) !important; margin: 12px 0 0 !important; }'),
    ('.shx-journeys-head { margin-bottom: 24px; gap: 12px; }',
     '.shx-journeys-head { margin-bottom: 20px; }'),
    # ---- 2. section kickers sit closer to their headings --------------------
    ('letter-spacing: 2.4px; text-transform: uppercase; color: var(--gold-deep) !important; margin: 0 0 18px !important; }',
     'letter-spacing: 2.4px; text-transform: uppercase; color: var(--gold-deep) !important; margin: 0 0 14px !important; }'),
    # ---- 3. the big head-to-content gaps ------------------------------------
    ('.shx-promise-intro { max-width: 62ch; font-size: 18.5px !important; color: rgba(243,236,221,.85) !important; margin: 0 0 58px !important; }',
     '.shx-promise-intro { max-width: 62ch; font-size: 18.5px !important; color: rgba(243,236,221,.85) !important; margin: 0 0 32px !important; }'),
    ('.shx-seasons-duo { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; margin-top: 58px; }',
     '.shx-seasons-duo { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; margin-top: 34px; }'),
    ('.shx-six-head { max-width: 720px; margin-bottom: 50px; }',
     '.shx-six-head { max-width: 720px; margin-bottom: 34px; }'),
    (".shx-guests-fav { font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 19px !important; color: var(--gold-deep) !important; margin: 0 0 54px !important; }",
     ".shx-guests-fav { font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 19px !important; color: var(--gold-deep) !important; margin: 0 0 34px !important; }"),
    ('.shx-booking h2 { font-size: clamp(28px, 3.4vw, 38px) !important; color: var(--ink) !important; line-height: 1.16 !important; margin: 0 0 54px !important; }',
     '.shx-booking h2 { font-size: clamp(28px, 3.4vw, 38px) !important; color: var(--ink) !important; line-height: 1.16 !important; margin: 0 0 34px !important; }'),
    ('.shx-guests-photos { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-top: 64px; }',
     '.shx-guests-photos { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-top: 44px; }'),
    ('.shx-guests-more { margin-top: 54px; padding-top: 26px;',
     '.shx-guests-more { margin-top: 38px; padding-top: 22px;'),
    ('.shx-finder { margin-top: 52px; background: var(--paper); border: 1px solid var(--paper-line); border-radius: 3px; padding: 34px 38px; }',
     '.shx-finder { margin-top: 40px; background: var(--paper); border: 1px solid var(--paper-line); border-radius: 3px; padding: 34px 38px; }'),
    ('.shx-season { font-family: \'Montserrat\', sans-serif !important; font-weight: 600 !important; font-size: 19px !important; letter-spacing: -0.2px; color: var(--gold-deep) !important; margin: 44px 0 4px !important; }',
     '.shx-season { font-family: \'Montserrat\', sans-serif !important; font-weight: 600 !important; font-size: 19px !important; letter-spacing: -0.2px; color: var(--gold-deep) !important; margin: 34px 0 4px !important; }'),
    # ---- 4. medium text-to-text gaps ----------------------------------------
    ('line-height: 1.12 !important; color: var(--ink) !important; margin: 0 0 26px !important; }',
     'line-height: 1.12 !important; color: var(--ink) !important; margin: 0 0 20px !important; }'),
    ('.shx-legacy-copy p { margin: 0 0 20px !important; font-size: 18.5px !important; color: var(--body-ink) !important; }',
     '.shx-legacy-copy p { margin: 0 0 16px !important; font-size: 18.5px !important; color: var(--body-ink) !important; }'),
    ('.shx-quote { margin: 34px 0 0; padding: 26px 0 0; border-top: 5px double var(--gold); }',
     '.shx-quote { margin: 26px 0 0; padding: 22px 0 0; border-top: 5px double var(--gold); }'),
    ('color: var(--ink) !important; display: block; margin-bottom: 22px; }',
     'color: var(--ink) !important; display: block; margin-bottom: 16px; }'),
    ('stroke-linecap: round; stroke-linejoin: round; margin-bottom: 18px; }',
     'stroke-linecap: round; stroke-linejoin: round; margin-bottom: 14px; }'),
    ('.shx-step { border-top: 5px double var(--gold); padding-top: 22px; margin-bottom: 34px; }',
     '.shx-step { border-top: 5px double var(--gold); padding-top: 18px; margin-bottom: 26px; }'),
    (".shx-practical h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 23px !important; color: var(--ink) !important; margin: 0 0 22px !important; }",
     ".shx-practical h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 23px !important; color: var(--ink) !important; margin: 0 0 18px !important; }"),
    ('.shx-six-note { margin-top: 30px; font-size: 16px !important; color: var(--body-soft) !important; }',
     '.shx-six-note { margin-top: 24px; font-size: 16px !important; color: var(--body-soft) !important; }'),
    ('.shx-legacy-fact { margin-top: 30px; padding: 20px 24px;',
     '.shx-legacy-fact { margin-top: 24px; padding: 20px 24px;'),
    ('.shx-final-sub { max-width: 56ch; margin: 0 auto 34px !important;',
     '.shx-final-sub { max-width: 56ch; margin: 0 auto 28px !important;'),
    ('color: rgba(243,236,221,.6) !important; margin-bottom: 40px !important; }',
     'color: rgba(243,236,221,.6) !important; margin-bottom: 32px !important; }'),
    ('.shx-broch-sub { font-size: 16.5px !important; line-height: 1.65 !important; color: var(--body-soft) !important; margin: 0 0 26px !important; max-width: 52ch; }',
     '.shx-broch-sub { font-size: 16.5px !important; line-height: 1.65 !important; color: var(--body-soft) !important; margin: 0 0 22px !important; max-width: 52ch; }'),
]

for old, new in R:
    n = body.count(old)
    assert n == 1, f'expected 1 occurrence, got {n}: {old[:80]}...'
    body = body.replace(old, new, 1)
print(f'  {len(R)} replacements applied')

# ---- version + changelog ----------------------------------------------------
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — JOURNEYS INTRO UNDER THE HEADING + TEXT-GAP TIGHTENING (Ben).
            The "Explore our journeys." intro no longer sits beside the heading
            (flex space-between removed): kicker, heading, paragraph now stack.
            Page-wide vertical-rhythm pass, desktop: head-to-content gaps
            46-64px cut to 30-44px (journeys head, promise intro, seasons duo,
            Super 6 head, guests pull-quote, booking h2, guests photo grid),
            kicker-to-heading 18 to 14px, plus smaller trims (legacy copy,
            quote block, steps, practicals, final call, brochure sub). Hero
            untouched. Mobile keeps its v15 compaction overrides.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants ---------------------------------------------------------------
for tag in ('div', 'section', 'style', 'script'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, f'<{tag}> {o} open vs {c} close'
for sm in re.finditer(r'<script>(.*?)</script>', body, re.S):
    assert not re.search(r'<[A-Za-z]', sm.group(1)), 'sanitizer hazard'
assert body.count('&mdash;') == src.count('&mdash;')

newname = f'SEHE-homepage_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run)')
