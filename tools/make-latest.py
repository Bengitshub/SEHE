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

# Contact page: ONE HTML widget placed directly above the native Duda form's row
# (since v7 the form is docked into the page on the published site).
FILES['contact-page.txt'] = one('SEHE-contact-page_v*.txt')

os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*')):
    os.remove(f)

manifest = []
for name, src in sorted(FILES.items()):
    shutil.copyfile(src, os.path.join(OUT, name))
    body = open(src, encoding='utf-8').read()
    vm = re.search(r'VERSION (v\d+)', body)
    manifest.append((name, vm.group(1) if vm else '-', os.path.basename(src)))
manifest.sort()

readme = ['SEHE — LATEST paste-ready files',
          '=' * 60,
          'Always paste from THIS folder. Filenames never change; the',
          'contents are regenerated whenever anything is updated, so the',
          'same link is always the newest version (shown below).',
          '',
          'COPY THE WHOLE FILE. Open the downloaded file (or GitHub\'s Raw view),',
          'select all, copy. Never copy from a preview: on 25 Sep two Contact',
          'pastes were cut off at line 150 and the page vanished. After',
          'pasting, scroll to the bottom of Duda\'s code box. Files ending in an',
          '"END OF FILE" line (contact, reviews, privacy) must show that line',
          'last.',
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
          '  privacy-policy-page.txt, terms-page.txt, contact-page.txt',
          '  CONTACT: paste contact-page.txt into ONE widget in a full-width',
          '  row placed DIRECTLY ABOVE the native Duda form row. Keep the form',
          '  as it is; on the published page it moves into the design.',
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
