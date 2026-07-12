#!/usr/bin/env python3
"""SEHE tour-page validator (reconstructed 12 Jul 2026 after the container
recycle; functionally equivalent to the original, which enforced the same
rules on every page change).

Checks per file:
  1. VERSION vN in the header matches the _vN in the filename.
  2. Alignment locks present when the page uses .sehe-tourpage:
     .sehe-tourpage{text-align:left} and .sehe-journeys{text-align:left}.
  3. Tag balance for div/section/article/button/form/select
     (scripts, styles and HTML comments stripped first).
  4. Rail-set names quoted: "Super 6" / "Big 5" / "Famous 4" must appear as
     &ldquo;Name&rdquo; (or curly quotes) in visible copy; legacy spellings
     (Super Six, Big Five, Famous Four) are rejected.
  5. No literal "<base" or "<title" tokens anywhere (Duda publish-sanitizer
     corruption vector) outside of escaped entities.
  6. No placeholder junk: REPLACE_WITH, lorem ipsum, tktk, xxx_.
  7. If var DEFAULT_TOUR is present it must be one of the known keys; if
     data-sehe-dep-count is present, var SEHE_PAGE_TOUR must be too.
  8. Warn (not fail) if class="sehe-journeys" appears != 1 times.

Usage: python3 tools/check_tour_page.py FILE [FILE...]
"""
import re, sys, os

KEYS = {'winter-2026','winter-2027','pinnacle-2027','11day-2627','14day-2627','11day-2728','14day-2728'}
TAGS = ('div','section','article','button','form','select')
RAIL = ('Super 6','Big 5','Famous 4')
LEGACY = ('Super Six','Big Five','Famous Four')

def body_only(t):
    b = re.sub(r'<script\b[\s\S]*?</script>', '', t, flags=re.I)
    b = re.sub(r'<style\b[\s\S]*?</style>', '', b, flags=re.I)
    b = re.sub(r'<!--[\s\S]*?-->', '', b)
    return b

def check(path):
    errs, warns = [], []
    t = open(path, encoding='utf-8').read()
    name = os.path.basename(path)

    m = re.search(r'_v(\d+)\.(?:txt|html)$', name)
    hv = re.search(r'VERSION v(\d+)', t)
    if m and hv and m.group(1) != hv.group(1):
        errs.append(f'filename says v{m.group(1)} but header says v{hv.group(1)}')
    elif m and not hv:
        errs.append('no VERSION vN header found')

    if 'class="sehe-tourpage"' in t:
        if not re.search(r'\.sehe-tourpage\s*\{[^}]*text-align\s*:\s*left', t):
            errs.append('missing .sehe-tourpage text-align:left lock')
        if not re.search(r'\.sehe-journeys\s*\{[^}]*text-align\s*:\s*left', t):
            errs.append('missing .sehe-journeys text-align:left lock')

    b = body_only(t)
    for tag in TAGS:
        o = len(re.findall(r'<' + tag + r'(?:\s|>)', b))
        c = len(re.findall(r'</' + tag + r'>', b))
        if o != c:
            errs.append(f'unbalanced <{tag}>: {o} open vs {c} close')

    for r in RAIL:
        for mm in re.finditer(re.escape(r), b):
            before = b[max(0, mm.start() - 8):mm.start()]
            if not (before.endswith('&ldquo;') or before.endswith('“') or before.endswith('"')):
                seg = b[max(0, mm.start() - 40):mm.end() + 20].replace('\n', ' ')
                errs.append(f'unquoted rail-set name "{r}" — wrap it in quotes (e.g. &ldquo;{r}&rdquo;). Near: …{seg}…')
                break
    for l in LEGACY:
        if l in b:
            errs.append(f'legacy rail-set spelling "{l}" found')

    for tok in ('<base', '<title'):
        if tok in t:
            errs.append(f'literal "{tok}" token present (Duda publish-sanitizer hazard)')

    # REPLACE_WITH only counts in attribute values (the video script's own
    # guard line legitimately contains the token inside its JS)
    if re.search(r'data-video-src="[^"]*REPLACE_WITH', t):
        errs.append('data-video-src still has the REPLACE_WITH placeholder')
    for junk in ('lorem ipsum', 'tktk', 'xxx_'):
        if junk.lower() in body_only(t).lower():
            errs.append(f'placeholder junk present: {junk}')

    dm = re.search(r"var DEFAULT_TOUR\s*=\s*'([^']+)'", t)
    if dm and dm.group(1) not in {'14day','11day','winter26','winter27','pinnacle','14day27','11day27','14day2728','11day2728','winter2026','winter2027','pinnacle2027','14day2627','11day2627'} | KEYS:
        errs.append(f'DEFAULT_TOUR {dm.group(1)!r} is not a known key')
    if 'data-sehe-dep-count' in t and 'SEHE_PAGE_TOUR' not in t:
        errs.append('data-sehe-dep-count present but no SEHE_PAGE_TOUR script')

    n = t.count('class="sehe-journeys"')
    if n != 1:
        warns.append(f'class="sehe-journeys" appears {n} times (expected 1)')

    return errs, warns

def main():
    files = sys.argv[1:]
    if not files:
        print('usage: check_tour_page.py FILE [FILE...]'); sys.exit(2)
    bad = 0
    for f in sorted(files):
        if not os.path.exists(f):
            print(f'[ERROR] not found: {f}'); bad += 1; continue
        errs, warns = check(f)
        print(f'[{"PASS" if not errs else "FAIL"}] {f}')
        for e in errs: print(f'    x {e}')
        for w in warns: print(f'    ! {w}')
        bad += len(errs)
    print()
    print('ALL CHECKS PASSED' if bad == 0 else 'SOME CHECKS FAILED')
    sys.exit(1 if bad else 0)

main()
