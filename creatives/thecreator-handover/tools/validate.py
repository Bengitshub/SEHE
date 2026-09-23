#!/usr/bin/env python3
"""Validate every exported PNG: decodes, exact expected dimensions, not fully
transparent, not a single uniform colour, SHA-256 (for duplicate detection),
plus the harness readiness report (all images decoded, fonts loaded)."""
import os, sys, json, hashlib
from PIL import Image
ROOT = sys.argv[1]; REPORT = sys.argv[2]
rep = {r['folder']+'/'+r['id']: r for r in json.load(open(REPORT))}
rows = []; hashes = {}
for root, _, files in os.walk(ROOT):
    for f in sorted(files):
        if not f.endswith('.png'): continue
        p = os.path.join(root, f); key = os.path.relpath(p, ROOT)[:-4]
        r = rep.get(key, {}); row = {'file': key + '.png', 'expected': f"{r.get('w')}x{r.get('h')}", 'problems': []}
        try:
            im = Image.open(p); im.load()
            row['actual'] = f'{im.width}x{im.height}'; row['bytes'] = os.path.getsize(p)
            if (im.width, im.height) != (r.get('w'), r.get('h')): row['problems'].append('WRONG SIZE')
            rgba = im.convert('RGBA'); a = rgba.getchannel('A').getextrema()
            if a == (0, 0): row['problems'].append('FULLY TRANSPARENT')
            small = rgba.convert('RGB').resize((64, 64)); cols = len(set(small.getdata()))
            row['distinct_colours_64px'] = cols
            if cols == 1: row['problems'].append('UNIFORM SINGLE COLOUR')
            if r and not r.get('allImagesOk', False): row['problems'].append('IMAGE LOAD FAILURE (harness)')
            if r and r.get('fontsMissing'): row['problems'].append('FONT NOT LOADED: ' + ','.join(r['fontsMissing']))
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); row['sha256'] = h
            hashes.setdefault(h, []).append(key)
        except Exception as e:
            row['problems'].append(f'DECODE FAILED: {e}')
        rows.append(row)
for h, ks in hashes.items():
    if len(ks) > 1:
        for k in ks:
            for row in rows:
                if row['file'] == k + '.png': row['problems'].append('IDENTICAL TO: ' + ', '.join(x for x in ks if x != k))
ok = [r for r in rows if not r['problems']]; bad = [r for r in rows if r['problems']]
print(f'validated {len(rows)} PNGs: {len(ok)} clean, {len(bad)} flagged')
for r in bad: print('  FLAG', r['file'], '->', '; '.join(r['problems']))
json.dump(rows, open(os.path.join(os.path.dirname(REPORT), 'validation.json'), 'w'), indent=1)
