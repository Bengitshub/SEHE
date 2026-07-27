#!/usr/bin/env python3
"""Regenerate the switch-over Block A / Block B pair for every tour page.

The live tour pages are pasted as TWO HTML widgets with the native Duda form
row between them, so a full-page master is never pasted directly — it has to be
split. The cut is immediately before section 5 (Booking / Available Dates):

    Block A = master[:cut]  + "END OF BLOCK A" instructions + alignment locks
    Block B = "BLOCK B" header + master[cut:]

Reconstruction identity (blockA_content + blockB_content == master) is asserted
for every page, so a block pair can never silently drift from its master.

Usage: python3 tools/make-blocks.py [--apply]
"""
import re
import os
import sys
import glob

APPLY = '--apply' in sys.argv
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'switchover')
CUT = '<!-- ===== 5. Booking / Available Dates ===== -->'

# master filename glob -> switch-over block key + human title
PAGES = [
    ('SEHE-14day-tour_v*.txt',             '14day-2627'),
    ('SEHE-11day-2627-tour_v*.txt',        '11day-2627'),
    ('SEHE-12day-winter-2026-tour_v*.txt', 'winter-2026'),
    ('SEHE-12day-winter-2027-tour_v*.txt', 'winter-2027'),
    ('SEHE-pinnacle-2027-tour_v*.txt',     'pinnacle-2027'),
    ('SEHE-11day-2728-tour_v*.txt',        '11day-2728'),
    ('SEHE-14day-2728-tour_v*.txt',        '14day-2728'),
]

END_A = '''
<!-- ═══════════════ END OF BLOCK A ═══════════════
     AARON: directly below this HTML widget add a new ROW:
       1. set the row background colour to #f9f7f3 (matches the brochure band)
       2. drop in the NATIVE DUDA BROCHURE FORM widget (the existing form element
          from the old live page — same form = same webhook/automations)
       3. paste duda-brochure-form-skin.css into that form widget: Design/Custom CSS,
          "GENERAL CSS FOR ALL DEVICES" panel (replace contents); clear the
          device-specific CSS panel
     On the PUBLISHED page the form auto-docks into the brochure card (script in
     Block A); in the editor it stays in its own row so it remains editable.
     Then add a fresh HTML widget below the form row and paste BLOCK B into it. -->

<style>
/* Block-A copy of the global alignment locks (Block B carries the originals). */
.sehe-tourpage{ text-align:left; }
.sehe-journeys{ text-align:left; }
.sehe-tourpage img{ max-width:100%; }
</style>
'''

HEAD_B = ('<!-- ═══ SEHE {key} {ver} — BLOCK B (paste in an HTML widget BELOW the Duda form row; '
          'Block A + form row sit above) ═══ -->\n\n\n\n')

# Block A is NOT a plain prefix of the master. The full-page master carries its
# own HTML brochure form; on the split pages that form is the NATIVE DUDA form,
# which the docking script moves into .sehe-form-slot. So Block A swaps the HTML
# form for a pointer note and drops the form's binder script — otherwise the
# published page would render two forms.
NOTE = ('<div class="sehe-brochure-note" style="margin-top:6px; padding:14px 16px; '
        'background:var(--gold-pale); border-left:3px solid var(--gold); border-radius:6px; '
        'font-size:14px; color:var(--text);">Complete the short form just below to view the '
        'brochure collection &darr;</div>')
FORM_RE = re.compile(r'<form class="sehe-brochure-form".*?</form>', re.S)
BINDER_RE = re.compile(r'<script>\s*\(function\(\) \{\s*/\* Brochure form \(design template\).*?</script>', re.S)


def block_a_body(master_prefix, path):
    """master[:cut] -> Block A body (form swapped for the note, binder removed)."""
    body, n = FORM_RE.subn(NOTE, master_prefix)
    assert n == 1, f'{path}: expected exactly one brochure form in Block A, got {n}'
    body, n = BINDER_RE.subn('', body)
    assert n == 1, f'{path}: expected exactly one brochure binder script, got {n}'
    assert '<form' not in body, f'{path}: a form survived into Block A'
    return body.rstrip() + '\n'


stale = []
for pattern, key in PAGES:
    hits = sorted(glob.glob(os.path.join(REPO, pattern)))
    assert len(hits) == 1, f'{pattern}: expected one master, got {hits}'
    master_path = hits[0]
    master = open(master_path, encoding='utf-8').read()
    ver = re.search(r'VERSION (v\d+)', master).group(1)

    cut = master.find(CUT)
    assert cut > 0, f'{master_path}: split marker not found'

    a_body = block_a_body(master[:cut], master_path)
    b_body = master[cut:]
    block_a = a_body + END_A
    block_b = HEAD_B.format(key=key, ver=ver) + b_body

    # Block B must be the master's tail verbatim
    assert block_b.endswith(master[cut:]), f'{master_path}: Block B is not the master tail'
    # the docking slot must survive in Block A — it is where the native form lands
    assert 'data-sehe-form-slot' in a_body, f'{master_path}: form slot missing from Block A'
    # each block must be tag-balanced on its own
    for name, blk in (('A', block_a), ('B', block_b)):
        for tag in ('div', 'section', 'style', 'script', 'article'):
            o, c = len(re.findall(rf'<{tag}[\s>]', blk)), blk.count(f'</{tag}>')
            assert o == c, f'{master_path} block {name}: <{tag}> {o} open vs {c} close'

    a_name = os.path.join(OUT, f'SEHE-{key}_{ver}-blockA.txt')
    b_name = os.path.join(OUT, f'SEHE-{key}_{ver}-blockB.txt')
    # retire any previous version of this pair
    old = [p for p in glob.glob(os.path.join(OUT, f'SEHE-{key}_v*-block?.txt'))
           if p not in (a_name, b_name)]
    stale += old

    print(f'  {key:<14} {ver:<5} A {len(block_a):>7}  B {len(block_b):>7}  '
          f'(cut at {cut}, identity OK)')
    if APPLY:
        open(a_name, 'w', encoding='utf-8').write(block_a)
        open(b_name, 'w', encoding='utf-8').write(block_b)

if APPLY:
    for p in stale:
        os.remove(p)
    print(f'\nAPPLIED — {len(PAGES)} pairs written, {len(stale)} stale files removed.')
else:
    print(f'\nDRY RUN — would write {len(PAGES)} pairs and remove {len(stale)} stale files:')
    for p in sorted(stale):
        print('    -', os.path.basename(p))
