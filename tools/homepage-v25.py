#!/usr/bin/env python3
"""Homepage v25 — brand alignment to the tour landing pages + Winter 2026 sold out.

Ben: "the branding seems to be slightly off in terms of headings, not the hero,
that is good. More closely to the landing pages of the tours, but branding wise,
and the tour boxes."

Measured differences against the tour pages' system, and what this fixes:

  heading weight   tour pages Montserrat 600 / -0.2px   home was 700 / -0.4px
  heading scale    .sehe-section-heading clamp(28,3.4vw,38)  home was clamp(32,3.6vw,48)
  eyebrow          11px / 700 / 2.4px / gold-dark, with a 28px leading rule
                   home was 13px / .42em / no rule, plus a separate double rule
  tour boxes       white card, 10px radius, hover lift + gold border
                   home was flat paper, 3px radius, no hover
  card title       22px / 700 / -0.3px      home was clamp(22,1.9vw,27) / no tracking
  card badge       white pill, navy text, 1.2px tracking, soft shadow
                   home was solid ink, .18em

Hero, film and final headings are deliberately left at their larger display
scale — those are statement moments and Ben confirmed the hero is right.

Also: Winter 2026 is sold out, so within the Winter Editions group the 2027
card now leads and 2026 sits below it, marked sold out and pointing at 2027.

Usage: python3 tools/homepage-v25.py [--apply]
"""
import re
import os
import sys
from datetime import date

APPLY = '--apply' in sys.argv
TODAY = date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'SEHE-homepage_v24.txt'
PREVIEW = 'sehe-homepage-complete.html'

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src = body


def sub1(old, new, what):
    global body
    assert old in body, f'MISSING: {what}'
    body = body.replace(old, new, 1)


# =========================================================================
# A. BRAND ALIGNMENT
# =========================================================================

# A1 — heading weight/tracking to match the tour pages' h1-h4 rule
sub1("  .sehe-home-ledger .shx-display { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; letter-spacing: -0.4px; margin: 0; }",
     "  .sehe-home-ledger .shx-display { font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; letter-spacing: -0.2px; margin: 0; }",
     'shx-display weight/tracking')

# A2 — eyebrow becomes the tour pages' .sehe-section-eyebrow
sub1("  .shx-kicker { display: block; font-size: 13px !important; font-weight: 700 !important; letter-spacing: .42em; text-transform: uppercase; color: var(--gold-deep) !important; margin: 0 0 14px !important; }",
     "  .shx-kicker { display: inline-flex; align-items: center; gap: 10px; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 2.4px; text-transform: uppercase; color: var(--gold-deep) !important; margin: 0 0 18px !important; }\n"
     "  .shx-kicker::before { content: ''; width: 28px; height: 1px; background: var(--gold); flex: none; }",
     'kicker -> section eyebrow')
sub1("  .shx-kicker--light { color: var(--gold) !important; }",
     "  .shx-kicker--light { color: var(--gold-light) !important; }\n"
     "  .shx-kicker--light::before { background: var(--gold-light); }",
     'light eyebrow')

# the tour pages carry a --gold-light; the homepage needs it for eyebrows on ink
sub1("--gold: #c8a56c; --gold-deep: #a5804a; --gold-pale: #e9d9ba;",
     "--gold: #c8a56c; --gold-deep: #a68a55; --gold-light: #d4b37e; --gold-pale: #e9d9ba;",
     'gold tokens')

# A3 — the standalone double rule is superseded by the eyebrow's own rule
body = re.sub(r'\n\s*<hr class="shx-rule">', '', body)
sub1("  .shx-rule { width: 74px; border: 0; border-top: 1px solid var(--gold); border-bottom: 1px solid var(--gold); height: 5px; margin: 0 0 26px; background: transparent; }\n", '', 'rule CSS')
sub1("  .shx-film-in .shx-kicker, .shx-film-in .shx-rule { text-shadow: 0 1px 12px rgba(8,21,37,.9); }",
     "  .shx-film-in .shx-kicker { text-shadow: 0 1px 12px rgba(8,21,37,.9); }", 'film kicker shadow')
sub1("    .shx-rule { margin-bottom: 18px; }\n", '', 'mobile rule CSS')

# A4 — section heading scale to .sehe-section-heading
for sel in ['.shx-journeys h2', '.shx-promise h2', '.shx-seasons h2', '.shx-six h2', '.shx-guests h2']:
    body = body.replace('font-size: clamp(32px, 3.6vw, 48px) !important;', 'font-size: clamp(28px, 3.4vw, 38px) !important;')
body = body.replace('font-size: clamp(34px, 3.8vw, 52px) !important;', 'font-size: clamp(30px, 3.5vw, 40px) !important;')   # legacy
body = body.replace('font-size: clamp(30px, 3.2vw, 42px) !important;', 'font-size: clamp(28px, 3.4vw, 38px) !important;')   # booking

# A5 — season group labels
sub1("  .shx-season { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 20px !important; color: var(--gold-deep) !important; margin: 44px 0 4px !important; }",
     "  .shx-season { font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 19px !important; letter-spacing: -0.2px; color: var(--gold-deep) !important; margin: 44px 0 4px !important; }",
     'season label')

# A6 — tour boxes: white card, 10px radius, hover lift + gold border
sub1("  .shx-jc { display: flex; flex-direction: column; background: var(--paper); border: 1px solid var(--paper-line); border-radius: 3px; overflow: hidden; }",
     "  .shx-jc { display: flex; flex-direction: column; background: #ffffff; border: 1px solid var(--paper-line); border-radius: 10px; overflow: hidden; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }\n"
     "  .shx-jc:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(21, 59, 103, .08); border-color: var(--gold); }",
     'journey card chrome')
sub1("  .shx-jc--signature { border: 1px solid var(--gold); box-shadow: 0 0 0 4px rgba(200,165,108,.16); }",
     "  .shx-jc--signature { border: 1px solid var(--gold); box-shadow: 0 0 0 4px rgba(200,165,108,.16); }\n"
     "  .shx-jc--signature:hover { box-shadow: 0 0 0 4px rgba(200,165,108,.16), 0 10px 28px rgba(21,59,103,.10); }",
     'signature hover')

# A7 — card title + badge
sub1("  .shx-jc-body h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: clamp(22px, 1.9vw, 27px) !important; line-height: 1.2 !important; color: var(--ink) !important; margin: 0 0 10px !important; }",
     "  .shx-jc-body h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 22px !important; line-height: 1.2 !important; letter-spacing: -0.3px; color: var(--ink) !important; margin: 0 0 10px !important; }",
     'card title')
sub1("  .shx-jc-badge { position: absolute; top: 14px; left: 14px; background: var(--ink); color: #fff !important; font-size: 12.5px !important; font-weight: 700 !important; letter-spacing: .18em; text-transform: uppercase; padding: 8px 14px; border-radius: 3px; }",
     "  .shx-jc-badge { position: absolute; top: 14px; left: 14px; background: #ffffff; color: var(--ink) !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 12px; border-radius: 3px; box-shadow: 0 2px 6px rgba(0,0,0,.15); }",
     'card badge')

# mobile eyebrow/badge overrides follow the new base
sub1("    .shx-kicker { font-size: 11px !important; letter-spacing: .26em; margin-bottom: 10px !important; }",
     "    .shx-kicker { font-size: 10.5px !important; letter-spacing: 1.8px; gap: 8px; margin-bottom: 14px !important; }\n"
     "    .shx-kicker::before { width: 20px; }",
     'mobile eyebrow')
sub1("    .shx-jc-badge { font-size: 11px !important; letter-spacing: .12em; padding: 6px 10px; }",
     "    .shx-jc-badge { font-size: 10.5px !important; letter-spacing: 1px; padding: 5px 10px; }",
     'mobile badge')
sub1("    .shx-jc-body h3 { font-size: 20px !important; margin-bottom: 8px !important; }",
     "    .shx-jc-body h3 { font-size: 19px !important; margin-bottom: 8px !important; }",
     'mobile card title')

# =========================================================================
# B. WINTER 2026 SOLD OUT — 2027 leads the group, 2026 sits below it
# =========================================================================
CARD_RE = re.compile(r'        <article class="shx-jc">\n          <div class="shx-jc-img" style="background-image:url\(\'https://irp\.cdn-website\.com/35e9f777/dms3rep/multi/183840-lake-sarah-in-snow-b1e7ecbb\.webp\'\);".*?\n        </article>\n', re.S)
m = CARD_RE.search(body)
assert m, 'winter-2026 homepage card not found'
w26 = m.group(0)
body = body[:m.start()] + body[m.end():]

# sold-out dressing
w26 = w26.replace('<span class="shx-jc-badge">Winter Edition</span>',
                  '<span class="shx-jc-badge shx-jc-badge--sold">2026 &middot; Sold Out</span>', 1)
w26 = w26.replace('<li>Final dates &middot; Sep 2026</li>', '<li>Jun &ndash; Sep 2026</li>', 1)
w26 = w26.replace('The Southern Alps under snow &mdash; alpine rail, Tekapo&rsquo;s star-filled skies, Queenstown in its winter coat. Nearly sold out.',
                  'The Southern Alps under snow &mdash; alpine rail, Tekapo&rsquo;s star-filled skies, Queenstown in its winter coat. Every 2026 departure has now sold &mdash; <a href="/2027-winter-edition-tours">the 2027 Winter Edition is booking now</a>.', 1)
w26 = w26.replace('<p class="shx-jc-next">Final departure <strong data-shx-next="winter-2026">12 September 2026</strong></p>',
                  '<p class="shx-jc-next shx-jc-next--sold">Season complete &mdash; <strong>2027 now booking</strong></p>', 1)
assert 'shx-jc-badge--sold' in w26 and 'shx-jc-next--sold' in w26 and 'data-shx-next="winter-2026"' not in w26

# re-insert directly AFTER the 2027 winter card (2027 leads, 2026 follows)
anchor = body.find('data-shx-next="winter-2027"')
assert anchor > 0, 'winter-2027 card not found'
close = body.find('        </article>\n', anchor) + len('        </article>\n')
body = body[:close] + w26 + body[close:]

# sold-out CSS
sub1("  .shx-jc-brochure {",
     "  .shx-jc-badge--sold { background: #b84040; color: #ffffff !important; }\n"
     "  .shx-jc-next--sold strong { color: #b84040 !important; }\n"
     "  .shx-jc-line a { color: var(--ink) !important; font-weight: 700; text-decoration: underline !important; text-underline-offset: 3px; }\n"
     "  .shx-jc-brochure {",
     'sold-out card CSS')

# =========================================================================
# C. version + changelog
# =========================================================================
vm = re.search(r'VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d', body)
assert vm
nv = str(int(vm.group(1)) + 1)
body = body.replace(vm.group(0), f'VERSION v{nv}{vm.group(2)}{TODAY}', 1)
ENTRY = f"""       v{nv} — BRAND ALIGNMENT TO THE TOUR PAGES + WINTER 2026 SOLD OUT.
            Ben: the headings and tour boxes read slightly off-brand against
            the tour landing pages (hero excepted — that one is right). Matched
            to the tour pages' own system, measured from their CSS: headings
            Montserrat 600 / -0.2px tracking (were 700 / -0.4px); section
            headings to the .sehe-section-heading scale clamp(28px, 3.4vw,
            38px) (were clamp(32px, 3.6vw, 48px)); the eyebrow is now the tour
            pages' .sehe-section-eyebrow — 11px, 2.4px tracking, gold-dark,
            with its own 28px leading rule — which retires the separate double
            rule beneath it; season labels 600/19px. Tour boxes now match the
            journey cards: white, 10px radius, hover lift with a gold border,
            22px/-0.3px titles, and white badge pills with 1.2px tracking and a
            soft shadow. Hero, film and final headings keep their display scale
            deliberately. WINTER 2026: fully booked, so the 2027 card now leads
            the Winter Editions group with 2026 beneath it, badged "2026 ·
            Sold Out", reading "Season complete — 2027 now booking", and
            linking across to the 2027 Winter Edition. Its live-chip hook is
            removed so nothing can repaint a date over the sold-out wording.\n"""
body = re.sub(r'(CHANGELOG \(latest first\):\n)', lambda mm: mm.group(1) + ENTRY, body, count=1)

# ---- invariants ------------------------------------------------------------
assert body.count('<article class="shx-jc') == src.count('<article class="shx-jc'), 'card count changed'
assert body.count('shx-rule') == 0, 'stray rule reference'
order = re.findall(r'data-shx-next="([a-z0-9-]+)"', body)
assert order == ['14day-2627', '11day-2627', 'winter-2027', 'pinnacle-2027', '14day-2728', '11day-2728'], order
w26_at = body.find('12-Day Winter Edition 2026')
w27_at = body.find('12-Day Winter Edition 2027')
assert w27_at < w26_at, '2027 must lead 2026'
assert body.count('<div') - body.count('</div>') == src.count('<div') - src.count('</div>'), 'div balance drifted'

newname = f'SEHE-homepage_v{nv}.txt'
if APPLY:
    open(os.path.join(REPO, newname), 'w', encoding='utf-8').write(body)
    open(os.path.join(REPO, PREVIEW), 'w', encoding='utf-8').write(body)
    os.remove(os.path.join(REPO, SRC))
    print(f'APPLIED -> {newname}')
else:
    print(f'ok -> {newname} (dry run); chip order {order}')
