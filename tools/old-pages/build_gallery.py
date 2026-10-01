import re, html, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
REPO = REPO_ROOT
LIVE = open(live_path('gallery.html'), encoding='utf-8').read()
ITEMS = json.load(open(os.path.join(DATA_DIR, 'gallery-items.json'), encoding='utf-8'))
assert len(ITEMS) == 32
# Title corrections approved 25 Sep 2026 (Ben: "yes it is milford"): the place is
# Milford Sound, singular. Every other title stays verbatim.
TITLE_FIX = {21: ('Milford Sounds cruise', 'Milford Sound cruise'), 22: ('Milford Sounds', 'Milford Sound')}
for k, (old, new) in TITLE_FIX.items():
    assert ITEMS[k]['title'] == old, (k, ITEMS[k]['title'])
    ITEMS[k]['title'] = new
INTRO = 'Photos kindly supplied by passengers from previous tours.'
assert INTRO in LIVE
# Approved copy, round 3 (25 Sep 2026): GL-03 replaces the old intro (resolves flag G1); SH-02 band text
GL03 = 'A closer look at the scenery and experiences along the way, including photographs shared by our guests.'
SH02 = "Talk to our New Zealand team about dates, rooms and what you'd like to see. We'll help you choose a journey that suits you." 

# alt text written from what each photo shows (checked visually, 25 Sep 2026);
# the visible caption is the live gallery title, verbatim
ALT = [
    'The lakefront at Queenstown with snow-capped mountains beyond',
    'The Sir Edmund Hillary statue at Aoraki Mt Cook',
    'People on a lakeside lawn beside the TSS Earnslaw steamship',
    'A whale’s tail rising from the sea off Kaikōura',
    'Four tour guides in high-visibility vests under a sign reading Mossburn 1879',
    'Passengers watching the Kingston Flyer steam train at the platform',
    'A turquoise river mouth winding to the coast between green hills',
    'The Rogers K92 steam locomotive with its carriages',
    'Aerial view over the islands and bays of the Marlborough Sounds',
    'Arrowtown’s main street with autumn colour on the hills behind',
    'Snow-capped mountains beyond a golden tussock plain',
    'Dunedin Railway Station behind flower beds in full bloom',
    'A group of guests raising their glasses at a long dinner table',
    'Aerial view of the Kaikōura coastline',
    'Golden trees along a braided river valley below the mountains',
    'Sunrise over the sea, framed by Norfolk pines',
    'A river gorge winding through bush-covered hills',
    'Snow-capped mountains reflected in still water',
    'A restored Invercargill Tramways tram car on display',
    'Two guests smiling in their seats in a train carriage',
    'Yachts moored off the Picton foreshore on a misty morning',
    'A passenger on a cruise boat deck beside a waterfall and a rainbow',
    'A tall waterfall above a rocky river in native bush',
    'The TSS Earnslaw steamship at its wharf',
    'Larnach Castle and its garden gazebo',
    'A seated figure beside whiskey barrels under an Old Hokonui Whiskey sign',
    'Mountains and sky reflected in a still lake, framed by reeds',
    'A high tea table set with cakes and fine china',
    'A lake shore with bright flowers in the foreground and mountains beyond',
    'A still lake reflecting the hills and sky, framed by trees',
    'Passengers beside a stopped train at a gorge photo stop',
    'The Rogers K92 steam locomotive under a glowing sky',
]
assert len(ALT) == 32
CREDIT = {8: 'Rob Suisted', 11: 'David Wall'}   # from the file names (AS38-…-Rob-Suisted, U112-…-David-Wall)
for k, name in CREDIT.items():
    assert name.replace(' ', '-') in ITEMS[k]['src'], (k, name)

# hero: a passenger photo (Picton foreshore) — the intro under it says the photos come from passengers
HERO_K = next(k for k, it in enumerate(ITEMS) if it['title'] == 'Picton foreshore')
HERO_BASE, HERO_EXT = ITEMS[HERO_K]['src'].rsplit('-1920w.', 1)
# the live gallery's true order is Duda's index attribute (its desktop markup runs column by column)
ORDER = sorted(range(len(ITEMS)), key=lambda k: ITEMS[k]['index'])

# Ben (25 Sep 2026): "just enjoy the photos with minimal text other than key parts
# of the tours". A label shows ON the photo only for the signature experiences the
# current tour pages name (hero/highlights and itineraries), once each, on the
# photo that shows it best. Labels are the gallery titles, verbatim. Every other
# title stays in the photo viewer and in the figcaption for screen readers.
# Milford Sound's label went on once its spelling was confirmed (v7).
KEY = {0: 'Queenstown', 1: 'Aoraki Mt Cook', 3: 'Kaikoura', 5: 'Kingston Flyer', 7: 'Rogers K92', 21: 'Milford Sound cruise',
       23: 'TSS Earnslaw', 24: 'Larnach Castle', 28: 'Walter Peak', 30: 'Taieri Gorge photostop'}
for k, t in KEY.items():
    assert ITEMS[k]['title'] == t, (k, ITEMS[k]['title'])

EXTRA_CSS = r"""
  /* ── Gallery page ───────────────────────────────────────────────────── */
  @W .gl-credit { position: absolute; right: 30px; bottom: 12px; margin: 0 !important; font-size: 13px !important; color: rgba(255,255,255,.85) !important; text-shadow: 0 1px 8px rgba(8,21,37,.9); }
  @W .gl-grid { list-style: none !important; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
  @W .gl-grid li { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .gl-grid li::before, @W .gl-grid li::marker { content: none !important; }
  @W .gl-grid figure { position: relative; margin: 0 !important; }
  @W a.gl-open { display: block; border-radius: 10px; overflow: hidden; background: var(--off-white); text-decoration: none !important; }
  @W a.gl-open img { display: block; width: 100% !important; height: auto !important; aspect-ratio: 4 / 3; object-fit: cover; transition: transform .35s ease; }
  @W a.gl-open:hover img { transform: scale(1.03); }
  @W a.gl-open:focus-visible { outline-offset: 3px !important; }
  /* photos first: no caption under the photos. A navy label sits ON the photo
     for the signature tour experiences only, and the photographer's credit
     where there is one. Every other title is in the photo viewer, and in the
     figcaption for screen readers. Clicks pass through to the photo link. */
  @W .gl-grid figcaption.gl-cap { position: absolute; left: 0; right: 0; bottom: 0; margin: 0 !important; padding: 10px !important; display: flex; align-items: flex-end; justify-content: space-between; gap: 8px; pointer-events: none; }
  @W .gl-tag { display: inline-flex; align-items: center; gap: 8px; max-width: 100%; padding: 7px 11px 7px 10px; border-radius: 6px; background: rgba(14,45,82,.9); color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; font-size: 12.5px !important; font-weight: 600 !important; line-height: 1.25 !important; letter-spacing: .1em; text-transform: uppercase !important; box-shadow: 0 2px 10px rgba(8,21,37,.25); }
  @W .gl-tag::before { content: ''; flex: none; width: 14px; height: 2px; background: var(--gold-light); }
  @W .gl-by { margin-left: auto; font-family: 'Open Sans', sans-serif !important; font-size: 11.5px !important; line-height: 1.3 !important; color: rgba(255,255,255,.95) !important; text-shadow: 0 1px 6px rgba(8,21,37,.95); }
  /* lightbox — native dialog element: Esc closes, focus stays inside, page behind is inert */
  @W dialog.gl-box { width: min(1180px, 96vw); max-width: 96vw; max-height: 94vh; padding: 0 !important; border: 0; border-radius: 12px; background: #0b1726; color: #ffffff; overflow: visible; }
  @W dialog.gl-box::backdrop { background: rgba(8,21,37,.88); }
  @W dialog.gl-box:not([open]) { display: none !important; }
  @W .gl-box-inner { position: relative; display: flex; flex-direction: column; align-items: center; padding: 56px 72px 18px; }
  @W .gl-box-img { display: block; max-width: 100% !important; max-height: calc(94vh - 160px) !important; width: auto !important; height: auto !important; border-radius: 6px; }
  @W .gl-box-cap { margin: 14px 0 0 !important; text-align: center !important; }
  @W .gl-box-title { margin: 0 !important; font-family: 'Montserrat', sans-serif !important; font-size: 17px !important; font-weight: 600 !important; line-height: 1.35 !important; color: #ffffff !important; text-align: center !important; }
  @W .gl-box-title::before { content: ''; display: block; width: 36px; height: 2px; margin: 0 auto 10px; background: var(--gold-light); }
  @W .gl-box-title:empty { display: none; }
  @W .gl-box-meta { margin: 4px 0 0 !important; font-size: 13.5px !important; line-height: 1.5 !important; color: rgba(255,255,255,.75) !important; text-align: center !important; }
  @W .gl-btn { position: absolute; display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 50%; border: 2px solid rgba(255,255,255,.8); background: rgba(8,21,37,.6); color: #ffffff; font-family: 'Montserrat', sans-serif; font-size: 30px; line-height: 1; cursor: pointer; padding: 0 !important; }
  @W .gl-btn:hover { background: #ffffff; color: var(--navy-dark); }
  @W .gl-btn:focus-visible { outline: 3px solid var(--gold-light) !important; outline-offset: 3px !important; }
  @W .gl-prev { left: 10px; top: 50%; transform: translateY(-50%); }
  @W .gl-next { right: 10px; top: 50%; transform: translateY(-50%); }
  @W .gl-close { right: 10px; top: 8px; font-size: 26px; }
  @media (max-width: 860px) { @W .gl-credit { right: 18px; bottom: 8px; } }
  /* 32 photos: 4 across on desktop and tablet (8 even rows), 2 across on phones */
  @media (max-width: 760px) {
    @W .gl-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    @W .gl-grid figcaption.gl-cap { padding: 7px !important; }
    @W .gl-tag { gap: 6px; padding: 5px 8px; font-size: 11px !important; letter-spacing: .06em; }
    @W .gl-tag::before { width: 10px; }
    @W .gl-by { font-size: 10.5px !important; }
  }
  /* phones, and any short screen (landscape phones, 200% zoom): the viewer fills
     the screen so Close and the arrows are always visible */
  @media (max-width: 860px), (max-height: 620px) {
    @W dialog.gl-box { width: 100vw; max-width: 100vw; height: 100vh; height: 100dvh; max-height: none; margin: 0; border-radius: 0; }
    @W .gl-box-inner { height: 100%; justify-content: center; padding: 64px 10px 78px; }
    @W .gl-box-img { max-height: calc(100vh - 220px) !important; max-height: calc(100dvh - 220px) !important; }
    @W .gl-prev, @W .gl-next { top: auto; bottom: 14px; transform: none; }
    @W .gl-prev { left: calc(50% - 64px); }
    @W .gl-next { right: calc(50% - 64px); }
    @W .gl-close { top: 8px; right: 10px; }
  }
  @media (prefers-reduced-motion: reduce) { @W a.gl-open:hover img { transform: none; } }
"""

ENHANCE = r"""<script>
(function () {
  /* Gallery lightbox — add only. Each photo is a plain link to the larger
     image, so without JS (or without dialog support) the photo simply
     opens. Keys: Esc closes (native), Left and Right arrows move.
     No less-than sign and no ampersand in this script. */
  var root = document.querySelector('.sehe-pg-gallery');
  if (!root) return;
  var box = root.querySelector('[data-gl-box]');
  if (!box) return;
  if (typeof box.showModal !== 'function') return;
  var links = Array.prototype.slice.call(root.querySelectorAll('a.gl-open'));
  var img = box.querySelector('.gl-box-img');
  var ttl = box.querySelector('.gl-box-title');
  var meta = box.querySelector('.gl-box-meta');
  var cur = 0, opener = null;
  function show(i) {
    var n = links.length;
    cur = (i + n) % n;
    var a = links[cur];
    var t = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = t ? t.alt : '';
    var c = a.getAttribute('data-credit') || '';
    ttl.textContent = a.getAttribute('data-title') || '';
    meta.textContent = (c ? c + ' · ' : '') + 'Photo ' + (cur + 1) + ' of ' + n;
  }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      opener = a;
      show(i);
      box.showModal();
      box.querySelector('.gl-close').focus();
    });
  });
  box.querySelector('.gl-prev').addEventListener('click', function () { show(cur - 1); });
  box.querySelector('.gl-next').addEventListener('click', function () { show(cur + 1); });
  box.querySelector('.gl-close').addEventListener('click', function () { box.close(); });
  var ring = [box.querySelector('.gl-prev'), box.querySelector('.gl-next'), box.querySelector('.gl-close')];
  box.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
    if (e.key === 'Tab') {
      var at = ring.indexOf(document.activeElement);
      if (e.shiftKey) {
        if (at === 0 || at === -1) { e.preventDefault(); ring[2].focus(); }
      } else {
        if (at === 2 || at === -1) { e.preventDefault(); ring[0].focus(); }
      }
    }
  });
  box.addEventListener('click', function (e) { if (e.target === box) box.close(); });
  box.addEventListener('close', function () {
    img.removeAttribute('src');
    /* focus goes back to the photo that was on screen, so keyboard users keep their place */
    var back = links[cur] || opener;
    if (back) back.focus();
  });
})();
</script>"""


def tile(k, it):
    title = it['title']
    credit = CREDIT.get(k)
    thumb = it['src'].replace('-1920w.', '-640w.')
    parts = []
    if title:
        parts.append(f'<span class="gl-tag">{E(title)}</span>' if k in KEY else f'<span class="sp-sr">{E(title)}</span>')
    if credit:
        parts.append(f'<small class="gl-by">Photo: {E(credit)}</small>')
    fig = f'<figcaption class="gl-cap">{"".join(parts)}</figcaption>' if parts else ''
    data = f' data-title="{A(title)}"' if title else ''
    data += f' data-credit="Photo: {A(credit)}"' if credit else ''
    return (f'      <li><figure><a class="gl-open" href="{it["src"]}"{data}>'
            f'<img src="{thumb}" alt="{A(ALT[k])}" loading="lazy" width="640" height="480">'
            f'<span class="sp-sr"> (view larger)</span></a>{fig}</figure></li>')


HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — GALLERY PAGE (/gallery)
     COMPLETE PAGE  ·  VERSION v7  ·  2026-09-25  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
       v7 — Ben (25 Sep 2026): "yes it is milford". Two titles corrected
            from "Milford Sounds" to "Milford Sound" (the cruise photo and the
            waterfall), and the Milford Sound cruise photo now carries a label
            like the other signature experiences (10 labels). Every other
            title unchanged, word for word.
       v6 — Ben (25 Sep 2026): photos first, minimal text. No caption under
            the photos any more. A navy label with a gold dash (Montserrat
            capitals, the verbatim title) sits on the photo only for the
            9 signature experiences the current tours name: Queenstown,
            Aoraki Mt Cook, Kaikoura, Kingston Flyer, Rogers K92, TSS
            Earnslaw, Larnach Castle, Walter Peak, Taieri Gorge photostop.
            Milford Sound gets its label once the 'Sounds' spelling is
            settled (G3). Every title still shows in the photo viewer,
            now in the brand style, and screen readers still hear it.
            The two photographer credits stay on their photos. Grid: 4
            across (8 even rows), 2 across on phones, 4:3 tiles.
       v5 — Shared kit fix (25 Sep 2026): no CSS child combinators any more.
            Duda publishes that character as an HTML entity and the browser
            drops the rule. This page has no show-more button, so nothing
            visible changes. Copy unchanged.
       v4 — Approved copy update (round 3, 25 Sep 2026): new hero intro
            (GL-03), which resolves flag G1 (the old intro said every photo
            came from passengers); new help-band text (SH-02). Photo titles
            unchanged, word for word.
       v3 — Round-2 feedback (25 Sep 2026): the help band no longer links
            straight to /brochure-collection (every brochure form redirects
            there, and a visit counts as a brochure conversion). Nothing
            else changed.
       v2 — Review fixes (independent check, 25 Sep 2026): no tag-like tokens
            left in comments; kicker/button type larger (shared kit).
            Third independent review: photo ORDER corrected to the live
            gallery's own order (Duda's index attribute — its desktop markup
            runs column by column, which v1 had copied); two alt texts
            tightened (the Mossburn sign; a seated display figure); hero is
            now a passenger photo (Picton foreshore) since the intro under
            it says the photos come from passengers; lightbox fills the
            screen on phones and short screens so Close is always visible,
            stays hidden where the dialog element is not supported, reads
            the caption to screen readers, and returns focus to the photo
            last shown; line length ~60 characters' width.
       v1 — First new-design build of /gallery (Brief v2, 25 Sep 2026).
            All 32 photos from the live Duda gallery, same order, same
            titles (verbatim), same images on the Duda CDN. New: a
            responsive grid (4 / 3 / 2 columns), real alt text for every
            photo, the photographer credits that are in two file names
            (Rob Suisted, David Wall), and a keyboard lightbox (native
            dialog element: Esc closes, arrows move, Tab loops inside,
            focus returns to the photo). No filters — the gallery has no category
            data to filter on. Compact hero on photo 9 of the gallery (the
            old banner is an 880 KB PNG whose larger sizes redirect in a
            loop on the CDN). Intro sentence kept verbatim — FLAGGED: two
            photos are professional images, not passenger photos.
     -----------------------------------------------------------------------
     WHERE IT GOES: page "gallery-new" (duplicate of /gallery). Delete every
     old content row, add ONE full-width row (padding 0), ONE HTML widget,
     paste this whole file. Steps + rollback: notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: Duda-CDN images only; no autoplay; no schema; no tracking;
     no departure data; CSS scoped to .sehe-pg-gallery; script adds only.
     ===================================================================== -->"""

grid = '\n'.join(tile(k, ITEMS[k]) for k in ORDER)
credit_html = ''
body = f"""{HEADER}
{FONTS}
{css('sehe-pg-gallery', EXTRA_CSS)}
<div class="sehe-pg-gallery">
{hero(f'{HERO_BASE}-1920w.{HERO_EXT}', 'On tour', 'Gallery', E(GL03), extra=credit_html, compact=True,
      srcset=f'{HERO_BASE}-640w.{HERO_EXT} 640w, {HERO_BASE}-1280w.{HERO_EXT} 1280w, {HERO_BASE}-1920w.{HERO_EXT} 1920w', label_id='sehe-gl-title', pos='center 55%')}
<div class="sp-body">
  <section class="sp-section" aria-labelledby="sehe-gl-title">
    <ul class="gl-grid" role="list">
{grid}
    </ul>
  </section>
{band('Need help choosing the right tour?',
      E(SH02),
      [('View all journeys', '/journeys', 'gold', False),
       ('Contact us', '/contact', 'light', False), (PHONE_TXT, PHONE_TEL, 'light', False)])}
</div>
  <dialog class="gl-box" aria-label="Photo viewer" data-gl-box>
    <div class="gl-box-inner">
      <img class="gl-box-img" alt="">
      <div class="gl-box-cap" aria-live="polite"><p class="gl-box-title"></p><p class="gl-box-meta"></p></div>
      <button type="button" class="gl-btn gl-prev" aria-label="Previous photo">‹</button>
      <button type="button" class="gl-btn gl-next" aria-label="Next photo">›</button>
      <button type="button" class="gl-btn gl-close" aria-label="Close photo viewer">×</button>
    </div>
  </dialog>
</div>
{ENHANCE}
"""
out = os.path.join(REPO, 'SEHE-gallery-page_v7.txt')
open(out, 'w', encoding='utf-8').write(body)
assert not check_script_safety(body), check_script_safety(body)
assert not check_style_safety(body), check_style_safety(body)
open(os.path.join(OUT_DIR, 'verbatim-gallery.txt'), 'w', encoding='utf-8').write('\n'.join([GL03, SH02] + [it['title'] for it in ITEMS if it['title']]) + '\n')
# every live gallery image must be present
for it in ITEMS:
    assert it['src'] in body, it['src']
print('wrote', out, len(body))
