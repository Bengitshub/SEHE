#!/usr/bin/env python3
"""Labelled contact sheets: one per export folder (every PNG appears once), plus an index."""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
ROOT, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
try: FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15); FONTB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: FONT = ImageFont.load_default(); FONTB = FONT
TW = 300; PAD = 14; LABEL_H = 40; COLS = 4
folders = {}
for root, _, files in os.walk(ROOT):
    pngs = sorted(f for f in files if f.endswith('.png'))
    if pngs: folders[os.path.relpath(root, ROOT)] = pngs
index = []
for folder, pngs in sorted(folders.items()):
    thumbs = []
    for f in pngs:
        im = Image.open(os.path.join(ROOT, folder, f)).convert('RGB')
        th = TW / im.width; t = im.resize((TW, max(1, int(im.height * th))))
        thumbs.append((f, im.size, t))
    rows = (len(thumbs) + COLS - 1) // COLS
    row_h = [max(t[2].height for t in thumbs[r*COLS:(r+1)*COLS]) + LABEL_H + PAD for r in range(rows)]
    W = COLS * (TW + PAD) + PAD; Hh = 70 + sum(row_h) + PAD
    sheet = Image.new('RGB', (W, Hh), (240, 238, 233)); d = ImageDraw.Draw(sheet)
    d.text((PAD, 18), f'{folder}   ·   {len(pngs)} files', fill=(26, 58, 92), font=FONTB)
    y = 70
    for r in range(rows):
        for c, (f, size, t) in enumerate(thumbs[r*COLS:(r+1)*COLS]):
            x = PAD + c * (TW + PAD)
            sheet.paste(t, (x, y)); d.rectangle([x-1, y-1, x+t.width, y+t.height], outline=(200, 195, 185))
            d.text((x, y + t.height + 4), f'{f[:-4][:38]}', fill=(29, 39, 51), font=FONT)
            d.text((x, y + t.height + 21), f'{size[0]}×{size[1]}', fill=(107, 119, 133), font=FONT)
        y += row_h[r]
    name = folder.replace('/', '__') + '.png'; sheet.save(os.path.join(OUT, name), optimize=True)
    index.append((folder, len(pngs), name)); print(f'  sheet {name}: {len(pngs)} thumbs, {sheet.size}')
with open(os.path.join(OUT, 'INDEX.txt'), 'w') as fh:
    fh.write('CONTACT SHEETS — one per export folder; every delivered PNG appears exactly once.\n\n')
    for folder, n, name in index: fh.write(f'{n:>3}  {folder:<62} -> {name}\n')
    fh.write(f'\nTOTAL {sum(n for _, n, _ in index)} creatives across {len(index)} folders\n')
print('total thumbs:', sum(n for _, n, _ in index))
