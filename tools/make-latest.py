#!/usr/bin/env python3
"""Assemble LATEST/ — the one folder Ben pastes from.

Copies every current paste-ready deliverable to a STABLE filename (no version
numbers), so the same GitHub link always serves the newest content and stale
downloads can't happen. Regenerate after any master/blocks/worker change:

    python3 tools/make-latest.py
"""
import glob
import os
import re
import shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'LATEST')


def one(pattern):
    hits = sorted(glob.glob(os.path.join(REPO, pattern)))
    assert len(hits) == 1, f'{pattern}: expected exactly one match, got {hits}'
    return hits[0]


FILES = {
    'worker-sehe-next-departures.js': one('worker/sehe-worker_LIVE-auto.js'),
    'homepage.txt':            one('SEHE-homepage_v*.txt'),
    'journeys-page.txt':       one('SEHE-journeys-page_v*.txt'),
    'brochure-collection.txt': one('SEHE-brochure-collection_v*.txt'),
}
for key in ['14day-2627', '11day-2627', 'winter-2026', 'winter-2027', 'pinnacle-2027', '11day-2728', '14day-2728']:
    for blk in ['A', 'B']:
        FILES[f'tourpage-{key}-block{blk}.txt'] = one(f'switchover/SEHE-{key}_v*-block{blk}.txt')

# Old-design page rebuilds (Brief v2, Sep 2026) — one HTML widget each
for key in ['reviews', 'about', 'faq', 'gallery', 'himalayan-trust', 'privacy-policy', 'terms']:
    FILES[f'{key}-page.txt'] = one(f'SEHE-{key}-page_v*.txt')

# Contact page: ONE master, THREE HTML widgets around the native Duda form.
# The master is split at its BLOCK markers (edit the master, never LATEST).
CONTACT = one('SEHE-contact-page_v*.txt')
CONTACT_BLOCKS = {'A': 'contact-page-blockA-hero.txt', 'B': 'contact-page-blockB-details.txt',
                  'C': 'contact-page-blockC-more.txt'}


def split_blocks(path):
    body = open(path, encoding='utf-8').read()
    out = {}
    for letter in CONTACT_BLOCKS:
        start, end = f'<!-- ▼▼▼ BLOCK {letter} ▼▼▼ -->\n', f'\n<!-- ▲▲▲ END BLOCK {letter} ▲▲▲ -->'
        assert body.count(start) == 1 and body.count(end) == 1, f'{path}: BLOCK {letter} markers'
        out[letter] = body[body.index(start) + len(start):body.index(end)] + '\n'
        assert 'VERSION v' in out[letter], f'BLOCK {letter} has no version header'
    return out

os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*')):
    os.remove(f)

manifest = []
for name, src in sorted(FILES.items()):
    shutil.copyfile(src, os.path.join(OUT, name))
    body = open(src, encoding='utf-8').read()
    vm = re.search(r'VERSION (v\d+)', body)
    manifest.append((name, vm.group(1) if vm else '-', os.path.basename(src)))
for letter, block in split_blocks(CONTACT).items():
    name = CONTACT_BLOCKS[letter]
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(block)
    vm = re.search(r'VERSION (v\d+)', block)
    manifest.append((name, vm.group(1) if vm else '-', os.path.basename(CONTACT) + f' [BLOCK {letter}]'))
manifest.sort()

readme = ['SEHE — LATEST paste-ready files',
          '=' * 60,
          'Always paste from THIS folder. Filenames never change; the',
          'contents are regenerated whenever anything is updated, so the',
          'same link is always the newest version (shown below).',
          '',
          'WORKER  worker-sehe-next-departures.js',
          '        -> Cloudflare > Workers & Pages > sehe-next-departures >',
          '           Edit code > select all > paste > Deploy.',
          '',
          'SINGLE-WIDGET PAGES (paste the whole file into the page\'s one',
          'HTML widget): homepage.txt, journeys-page.txt,',
          'brochure-collection.txt',
          '',
          'TOUR PAGES (two widgets per page): blockA -> the TOP HTML widget,',
          'blockB -> the BOTTOM HTML widget (the native Duda form row sits',
          'between them; never touch it).',
          '',
          'REBUILT OLD-DESIGN PAGES (Sep 2026) — build each on a "<slug>-new"',
          'page first; full steps, SEO text and rollback in',
          'notes/2026-09-25-old-pages-rebuild-runbook.md',
          '  one HTML widget each: reviews-page.txt, about-page.txt,',
          '  faq-page.txt, gallery-page.txt, himalayan-trust-page.txt,',
          '  privacy-policy-page.txt, terms-page.txt',
          '  CONTACT (three HTML widgets + the NATIVE Duda form, untouched):',
          '    contact-page-blockA-hero.txt    -> row 1, full width (carries',
          '                                       the CSS for the whole page)',
          '    contact-page-blockB-details.txt -> row 2, LEFT column',
          '    (native Duda form)              -> row 2, RIGHT column',
          '    contact-page-blockC-more.txt    -> row 3, full width',
          '',
          '!! ON HOLD (Aug 2026): tourpage-*-blockB.txt. The live tour pages now',
          '   carry a DIFFERENT booking section (iframe to the new Pounamu Journeys',
          '   booking app, pasted outside this repo). Pasting these Block Bs would',
          '   put the Checkfront widget back. Do not paste until the booking-system',
          '   decision is made — see observed/README.md.',
          '',
          'CURRENT VERSIONS',
          '-' * 60]
for name, ver, src in manifest:
    readme.append(f'  {name:<38} {ver:<5} ({src})')
open(os.path.join(OUT, '_READ-ME-FIRST.txt'), 'w', encoding='utf-8').write('\n'.join(readme) + '\n')

print(f'LATEST/ assembled: {len(manifest)} files + _READ-ME-FIRST.txt')
for name, ver, src in manifest:
    print(f'  {name:<38} {ver:<5} <- {src}')
