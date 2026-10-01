import re, html, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
REPO = REPO_ROOT
LIVE = open(live_path('himalayan-trust.html'), encoding='utf-8').read()


def clean(fragment):
    t = re.sub(r'<br\s*/?>', ' ', fragment)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t).replace(' ', ' ')).strip()


def widget_paras(wid):
    m = re.search(r'<div[^>]*\bid="%s"[^>]*>(.*?)</div>' % wid, LIVE, re.S)
    out = []
    for blk in re.findall(r'<(?:p|h2|h3)[^>]*>(.*?)</(?:p|h2|h3)>', m.group(1), re.S):
        out += [clean(x) for x in re.split(r'<br\s*/?>', blk) if clean(x)]   # <br> separates lines inside one heading
    return out


HEAD = widget_paras('1536461117')          # H2 + two H3s
assert HEAD == ["Sir Edmund Hillary's Himalayan Trust", 'FOUNDED IN 1960', '"Committed to the people of the Everest region since 1960"'] or HEAD[0].startswith('Sir Edmund Hillary'), HEAD
HERITAGE = widget_paras('1044067974')
TODAY_RAW = widget_paras('1095481005')
# two sentences are split across paragraphs on the live page — rejoin them (same words)
TODAY = []
for p in TODAY_RAW:
    if TODAY and (TODAY[-1].endswith(' the') or TODAY[-1].endswith(', but')):
        TODAY[-1] = TODAY[-1] + ' ' + p
    else:
        TODAY.append(p)
assert any(p.endswith('In healthcare, the Himalayan Trust has supported hospitals with doctors’ salaries, training, supplies, clinical support and maintenance.') for p in TODAY), TODAY
assert any(p.endswith('vital work, but we need you help to do so.') for p in TODAY), TODAY
CAPTIONS = [widget_paras(w)[0] for w in ['1313540575', '1307350643', '1113021231', '1932959872', '1818143321']]

IMG = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/'
PHOTOS = [  # (file stem, alt from what the photo shows, credit from file name)
    ('Ed+Hillary+recieving+Petition+from+Sherpas', 'Black-and-white photograph of Sir Edmund Hillary talking with a group of Sherpa men', ''),
    ('Ed+building+Khunde+Hospital', 'Black-and-white photograph of volunteers cutting timber planks at the Khunde Hospital building site, mountains behind', ''),
    ('Nepal+Monitoring+2022+5MB-7684', 'Young children sitting on cushions in a bright classroom', ''),
    ('Himalayan+Trust+Trip-82', 'Three schoolchildren with their hands together in greeting, snow-capped peaks behind', ''),
    ('2016_02_25_Nepal_Himalayan_Trust%C3%82-SamTarling_X7A1810', 'A nurse taking a patient’s blood pressure in a clinic', 'Sam Tarling'),
]
for stem, *_ in PHOTOS:
    assert stem in LIVE, stem
LOGO_W = IMG + 'Himalayan+Logo+White-640w.png'
# Approved copy, round 3 (25 Sep 2026): HT-03 our note above the Trust's sections; HT-06 the closing band
HT03 = 'The Himalayan Trust shares its story and its work in the Everest region below, in its own words.'
HT06 = "Sir Edmund Hillary's spirit of adventure inspires our rail and coach journeys through New Zealand's South Island." 
LOGO_M = IMG + 'HT+Logo+MAIN-640w.png'
HT = 'https://himalayantrust.org/'
HT_DONATE = 'https://himalayantrust.org/donate'


def linkify(p):
    t = E(p)
    t = t.replace(HT_DONATE, f'<a href="{HT_DONATE}" target="_blank" rel="noopener">{HT_DONATE}{NEWTAB}</a>')
    t = re.sub(r'(?<!["/>])https://himalayantrust\.org/(?!donate)', f'<a href="{HT}" target="_blank" rel="noopener">{HT}{NEWTAB}</a>', t)
    return t


EXTRA_CSS = r"""
  /* ── Himalayan Trust page ───────────────────────────────────────────── */
  @W .ht-logo-link { display: inline-block; margin: 0 0 18px; text-decoration: none !important; }
  @W .ht-logo-link img { display: block; width: 260px !important; height: auto !important; }
  @W .ht-note { display: flex; flex-wrap: wrap; align-items: center; gap: 18px 28px; padding: 22px 26px !important; background: var(--cream); border: 1px solid var(--border-light); border-left: 4px solid var(--gold); border-radius: 12px; }
  @W .ht-note p { flex: 1 1 420px; font-size: 17px !important; color: var(--text) !important; }
  @W .ht-note img { width: 200px !important; height: auto !important; flex: none; }
  @W .ht-copy p { max-width: 60ch; }
  @W .ht-copy p + p { margin-top: 16px !important; }
  @W .ht-photos { list-style: none !important; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr)); gap: 26px; }
  @W .ht-photos li { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .ht-photos li::before, @W .ht-photos li::marker { content: none !important; }
  @W .ht-photos figure { margin: 0 !important; }
  @W .ht-photos img { display: block; width: 100% !important; height: auto !important; aspect-ratio: 1280 / 783; object-fit: cover; border-radius: 10px; }
  @W .ht-photos figcaption { margin-top: 10px !important; font-size: 16px !important; line-height: 1.55 !important; color: var(--text) !important; }
  @W .ht-photos figcaption small { display: block; margin-top: 2px; font-size: 14px; color: var(--text-2); }
  @W .ht-actions { margin-top: 26px !important; }
  @media (max-width: 860px) {
    @W .ht-logo-link img { width: 200px !important; }
    @W .ht-note { padding: 18px 18px !important; }
    @W .ht-note img { width: 160px !important; }
  }
"""


def photo(i):
    stem, alt, credit = PHOTOS[i]
    cred = f'<small>Photo: {E(credit)}</small>' if credit else ''
    return (f'      <li><figure><img src="{IMG}{stem}-640w.webp" srcset="{IMG}{stem}-640w.webp 640w, {IMG}{stem}-1280w.webp 1280w" '
            f'sizes="(max-width: 860px) 100vw, 400px" alt="{A(alt)}" width="1280" height="783" loading="lazy">'
            f'<figcaption>{E(CAPTIONS[i])}{cred}</figcaption></figure></li>')


HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — HIMALAYAN TRUST PAGE (/himalayan-trust)
     COMPLETE PAGE  ·  VERSION v5  ·  2026-09-25  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
       v5 — Shared kit fix (25 Sep 2026): no CSS child combinators any more.
            Duda publishes that character as an HTML entity and the browser
            drops the rule. This page has no show-more button, so nothing
            visible changes. Copy unchanged.
       v4 — Approved copy update (round 3, 25 Sep 2026): our note above the
            Trust's sections now reads "The Himalayan Trust shares its story
            and its work in the Everest region below, in its own words."
            (HT-03); the closing band's line is HT-06; the two logo links
            lose their em dash and read "Himalayan Trust website (opens in
            a new tab)". The Trust's own text is unchanged, word for word.
       v3 — Third independent review (25 Sep 2026): line length tightened to
            about 60 characters' width (~66-72 characters; the old caps
            rendered up to ~85); on phones the darker hero veil now also
            applies to compact heroes (shared kit).
       v2 — Review fixes (independent check, 25 Sep 2026): the "who is
            speaking" note now covers only the two sections headed "The
            Himalayan Trust" (the closing band is SEHE speaking, and says
            so); Khunde Hospital photo alt text corrected (cutting timber
            planks). Two captions whose dates differ from their photo file
            names are FLAGGED, not edited. Kicker/button type larger.
       v1 — First new-design build of /himalayan-trust (Brief v2, 25 Sep 2026).
            All text, captions, logos and links from the live page, wording
            unchanged (two sentences that were split across paragraphs are
            rejoined — same words). NEW: a note making clear the words are the
            Himalayan Trust's own ("we" = the Trust, not Sir Edmund Hillary
            Explorer), so nothing suggests SEHE runs the Trust's projects or
            that a booking includes a donation. Statistics kept as written and
            FLAGGED ($3 a day; 2.6 million tree seedlings over 30 years).
            Photo credit "Sam Tarling" is from that photo's file name.
            The live page is noindex — keep it that way unless Ben decides.
     -----------------------------------------------------------------------
     WHERE IT GOES: page "himalayan-trust-new" (duplicate of /himalayan-trust).
     Delete every old content row, add ONE full-width row (padding 0), ONE
     HTML widget, paste this whole file. Steps + rollback:
     notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: no new facts; no schema; no tracking; no departure data;
     CSS scoped to .sehe-pg-trust.
     ===================================================================== -->"""

hero_extra = ''
body = f"""{HEADER}
{FONTS}
{css('sehe-pg-trust', EXTRA_CSS)}
<div class="sehe-pg-trust">
{hero(IMG + 'Himalayan+Trust+Trip-82-1920w.webp', 'Founded in 1960', E(HEAD[0]), E(HEAD[2]),
      srcset=f"{IMG}Himalayan+Trust+Trip-82-640w.webp 640w, {IMG}Himalayan+Trust+Trip-82-1280w.webp 1280w, {IMG}Himalayan+Trust+Trip-82-1920w.webp 1920w",
      img_alt='', label_id='sehe-ht-title', pos='center 35%')}
<div class="sp-body">
  <aside class="sp-section ht-note" aria-label="Who is speaking on this page">
    <p>{E(HT03)}</p>
    <a class="ht-logo-link" href="{HT}" target="_blank" rel="noopener"><img src="{LOGO_M}" alt="Himalayan Trust" width="640" height="192"><span class="sp-sr"> website (opens in a new tab)</span></a>
  </aside>

  <section class="sp-section ht-copy" aria-labelledby="sehe-ht-heritage">
    <div class="sp-head">
      <p class="sp-kicker">The Himalayan Trust</p>
      <h2 id="sehe-ht-heritage">Our heritage</h2>
    </div>
{chr(10).join('    <p>' + E(p) + '</p>' for p in HERITAGE)}
  </section>

  <section class="sp-section ht-copy" aria-labelledby="sehe-ht-today">
    <div class="sp-head">
      <p class="sp-kicker">The Himalayan Trust</p>
      <h2 id="sehe-ht-today">The Himalayan Trust today</h2>
    </div>
{chr(10).join('    <p>' + linkify(p) + '</p>' for p in TODAY)}
    <div class="sp-actions ht-actions">
      <a class="sp-btn" href="{HT_DONATE}" target="_blank" rel="noopener">Donate to the Himalayan Trust{NEWTAB}</a>
      <a class="sp-btn sp-btn--ghost" href="{HT}" target="_blank" rel="noopener">Visit himalayantrust.org{NEWTAB}</a>
    </div>
  </section>

  <section class="sp-section" aria-label="Photographs from the Himalayan Trust">
    <ul class="ht-photos" role="list">
{chr(10).join(photo(i) for i in range(5))}
    </ul>
  </section>

{band('About the Sir Edmund Hillary Explorer',
      E(HT06),
      [('About us', '/about', 'gold', False), ('View all journeys', '/journeys', 'light', False)])}
</div>
</div>
"""
# the hero carries the Trust's white logo above the eyebrow
logo_html = f'    <a class="ht-logo-link" href="{HT}" target="_blank" rel="noopener"><img src="{LOGO_W}" alt="Himalayan Trust" width="640" height="199"><span class="sp-sr"> website (opens in a new tab)</span></a>\n'
body = body.replace('    <p class="sp-eyebrow">Founded in 1960</p>', logo_html + '    <p class="sp-eyebrow">Founded in 1960</p>', 1)
out = os.path.join(REPO, 'SEHE-himalayan-trust-page_v5.txt')
open(out, 'w', encoding='utf-8').write(body)
assert not check_script_safety(body)
assert not check_style_safety(body), check_style_safety(body)
vb = [HEAD[0], HEAD[2]] + HERITAGE + TODAY + CAPTIONS + [HT03, HT06]
open(os.path.join(OUT_DIR, 'verbatim-trust.txt'), 'w', encoding='utf-8').write('\n'.join(vb) + '\n')
print('wrote', out, len(body), 'HEAD', HEAD, 'TODAY paras', len(TODAY))
