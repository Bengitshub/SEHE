import re, html, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
LIVE = open(live_path('about.html'), encoding='utf-8').read()
HOME = open(live_path('home.html'), encoding='utf-8').read()
JOURNEYS = open(live_path('journeys.html'), encoding='utf-8').read()
FAQ = json.load(open(os.path.join(DATA_DIR, 'faq-config.json'), encoding='utf-8'))
IMGTXT = json.load(open(os.path.join(DATA_DIR, 'about-imagetext.json'), encoding='utf-8'))
REPO = REPO_ROOT


def clean(fragment):
    t = re.sub(r'<br\s*/?>', ' ', fragment)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t).replace(' ', ' ')).strip()


# ── existing copy, verbatim ────────────────────────────────────────────────
paras = [clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', IMGTXT['text'], re.S)]
paras = [p for p in paras if p]
P_INSPIRE, P_AORAKI = paras[0], paras[1]
assert P_INSPIRE.startswith('Sir Edmund Hillary epitomised') and P_AORAKI.startswith('At Aoraki Mt Cook'), paras
assert 'Please view the' in paras[2] and 'about the Himalayan Trust' in paras[3], paras[2:]
# rail + coach: the FAQ's own answer to "Is the entire tour by train?"
q0 = FAQ['faqList'][0]
assert clean(q0['questionTitle']) == 'Is the entire tour by train?'
P_RAIL = clean(q0['questionAnswer'])
# operator lines — exactly as on the live homepage / journeys page
J_LEAD = "The Sir Edmund Hillary Explorer is New Zealand's leading tour operator, specialising in scenic rail and luxury coach tours of the South Island."
assert J_LEAD in html.unescape(JOURNEYS)
for s in ['100% New Zealand owned &amp; operated', 'World Travel Awards', '2022 · 2023 · 2024 · 2025']:
    assert s in HOME or html.unescape(s) in html.unescape(HOME), s

HERO = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/14_52+Reasons_Sir+Edmond+Hillary+Alpine+Centre-3'
# Approved copy, round 3 (25 Sep 2026). AB-03 hero intro, AB-07 / AB-08 story, AB-12 rail and coach.
AB03 = "Explore New Zealand's South Island by scenic rail and luxury coach with Sir Edmund Hillary Explorer."
AB07 = "Sir Edmund Hillary's spirit of adventure inspires our journeys through New Zealand's South Island. We honour that spirit as we explore the dramatic alpine scenery and remarkable landscapes for which this part of the country is known."
AB08 = "At Aoraki Mt Cook, visit the museum celebrating Sir Edmund Hillary's life and achievements. A member of the Hillary family joins the tour for an evening at the Sir Edmund Hillary Alpine Centre, sharing personal stories and how the family continues his legacy. On selected tours, learn about his team's Antarctic expedition using converted farm tractors at the International Antarctic Centre in Christchurch, and travel through Marlborough, where Hillary trained for the air force during the Second World War and climbed Mt Tapuae-o-Uenuku."
AB12 = "Rail and coach each offer a different view of the South Island. Scenic train journeys are complemented by coach travel to places the railway cannot reach, with frequent comfort stops along the way. All overnight stays are in comfortable hotels."
SH02 = "Talk to our New Zealand team about dates, rooms and what you'd like to see. We'll help you choose a journey that suits you." 
# phones: the same statue in portrait (a live Gallery photo, 1280x1919)
MOBILE_HERO = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/14_52+Reasons_Sir+Edmond+Hillary+Alpine+Centre-4'
assert MOBILE_HERO + '-1920w.jpg' in open(live_path('gallery.html'), encoding='utf-8').read()
PORTRAIT = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/Ed+Hillary+profile+1960'
WTA = 'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/new-zealands-leading-tour-operator-2025-winner-shield-256-816b3264-1920w.png'
# the six photographs from the old autoplaying carousel (the 2025/26 route map slide is left out — flagged)
# v2: the Wharf photo (its 640w file is an 880 KB PNG) and the humpback photo
# (file name suggests a third-party library image; licence unconfirmed) are
# left out and flagged.
PHOTOS = [
    ('woman-on-the-coastal-pacific', 'webp', 640, 442, 'A passenger taking in the coastline from a window seat on the Coastal Pacific', ''),
    ('L387-Aoraki-Mount-Cook-National-Park--Canterbury-Rob-Suisted', 'jpg', 640, 640, 'Aoraki Mount Cook, snow-covered above a turquoise lake and autumn trees', 'Rob Suisted'),
    ('Southland+track', 'jpg', 640, 640, 'A railway line running towards snow-capped mountains', ''),
    ('01-Kaikoura-Canterbury-Kyle-Mulinder', 'jpg', 640, 640, 'Fur seals on the rocks at Kaikōura, with snow on the mountains behind', 'Kyle Mulinder'),
]
car = json.load(open(os.path.join(DATA_DIR, 'about-carousel.json'), encoding='utf-8'))['carouselList']
for stem, ext, *_ in PHOTOS:
    assert any(stem in c['image'] for c in car), stem
assert HERO.rsplit('/', 1)[1].replace('+', ' ') in html.unescape(LIVE.replace('%20', ' ')), 'hero not the live About banner'

EXTRA_CSS = r"""
  /* ── About page ─────────────────────────────────────────────────────── */
  @W .sp-hero-img { object-position: 28% 40%; }
  /* the desktop banner is 1920x480: hold the hero at 480px so it is never enlarged */
  @media (min-width: 861px) { @W .ab-hero { min-height: 0 !important; height: 480px; } }
  @media (max-width: 860px) { @W .ab-hero .sp-hero-img { object-position: center 0% !important; } }
  @W .ab-story { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 48px; align-items: start; }
  @W .ab-portrait { position: relative; margin: 0 !important; }
  @W .ab-portrait img { display: block; width: 100% !important; height: auto !important; border-radius: 12px; }
  @W .ab-copy p + p { margin-top: 16px !important; }
  @W .ab-copy p { max-width: 60ch; }
  @W .ab-links { margin-top: 24px !important; }
  @W .ab-photos { list-style: none !important; margin: 28px 0 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
  @W .ab-photos li { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .ab-photos li::before, @W .ab-photos li::marker { content: none !important; }
  @W .ab-photos figure { position: relative; margin: 0 !important; }
  @W .ab-photos img { display: block; width: 100% !important; height: 220px !important; object-fit: cover; border-radius: 10px; }
  /* text on the photos, branded like the Gallery: a navy label with a gold dash
     (Montserrat capitals) and the photographer's credit in small white type.
     Clicks and selection pass through to the page. */
  @W figcaption.ab-cap { position: absolute; left: 0; right: 0; bottom: 0; margin: 0 !important; padding: 10px !important; display: flex; align-items: flex-end; justify-content: space-between; gap: 8px; pointer-events: none; }
  @W .ab-tag { display: inline-flex; align-items: center; gap: 8px; max-width: 100%; padding: 7px 11px 7px 10px; border-radius: 6px; background: rgba(14,45,82,.9); color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; font-size: 12.5px !important; font-weight: 600 !important; line-height: 1.25 !important; letter-spacing: .1em; text-transform: uppercase !important; box-shadow: 0 2px 10px rgba(8,21,37,.25); }
  @W .ab-tag::before { content: ''; flex: none; width: 14px; height: 2px; background: var(--gold-light); }
  @W .ab-by { margin-left: auto; font-family: 'Open Sans', sans-serif !important; font-size: 11.5px !important; line-height: 1.3 !important; color: rgba(255,255,255,.95) !important; text-shadow: 0 1px 6px rgba(8,21,37,.95); }
  @W .ab-facts { list-style: none !important; margin: 24px 0 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 16px; }
  @W .ab-facts li { margin: 0 !important; list-style: none !important; display: flex; align-items: center; gap: 16px; padding: 18px 20px !important; background: var(--cream); border: 1px solid var(--border-light); border-radius: 10px; }
  @W .ab-facts li::before, @W .ab-facts li::marker { content: none !important; }
  @W .ab-facts img { width: 64px !important; height: auto !important; flex: none; }
  @W .ab-facts strong { display: block; font-family: 'Montserrat', sans-serif !important; color: var(--navy); font-size: 17px; }
  @W .ab-facts span { font-size: 16px; color: var(--text-2); }
  @media (max-width: 860px) {
    @W .ab-story { grid-template-columns: 1fr; gap: 24px; }
    @W .ab-portrait { max-width: 420px; }
    @W .ab-photos { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    @W .ab-photos img { height: 170px !important; }
  }
  @media (max-width: 420px) {
    @W .ab-photos img { height: 150px !important; }
    @W figcaption.ab-cap { padding: 7px !important; }
    @W .ab-tag { gap: 6px; padding: 5px 8px; font-size: 11px !important; letter-spacing: .06em; }
    @W .ab-tag::before { width: 10px; }
    @W .ab-by { font-size: 10.5px !important; }
  }
"""


def photo(stem, ext, w, h, alt, credit):
    src = f'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/{stem}-640w.{ext}'
    cap = f'<figcaption class="ab-cap"><small class="ab-by">Photo: {E(credit)}</small></figcaption>' if credit else ''
    return f'      <li><figure><img src="{src}" alt="{A(alt)}" width="{w}" height="{h}" loading="lazy">{cap}</figure></li>'


HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — ABOUT PAGE (/about)
     COMPLETE PAGE  ·  VERSION v8  ·  2026-10-07  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
       v8 — Comments only (7 Oct 2026): a staff member's name removed
            from the code comments. Nothing on the page changes.
       v7 — Ben (26 Sep 2026): the text on the photos is branded like the
            Gallery. The portrait's caption is now a navy label with a gold
            dash on the photo ("Sir Edmund Hillary, 1960", without the full
            stop), and the two photographer credits sit on their photos in
            small white type. Copy otherwise unchanged from v6.
       v6 — Approved answers (email, 26 Sep 2026). A3: "keep both consistent
            with Hillary family member", so the sentence now matches the
            homepage: a member of the Hillary family joins the tour for an
            evening at the Sir Edmund Hillary Alpine Centre. A1 and A2 were
            not answered; the current itineraries include the International
            Antarctic Centre and Marlborough only on the 14-day and Pinnacle
            tours, so both now start "On selected tours". A4: no route map
            ("No need, please remove"). END OF FILE line added. Everything
            else unchanged.
       v5 — Shared kit fix (25 Sep 2026): no CSS child combinators any more.
            Duda publishes that character as an HTML entity and the browser
            drops the rule. This page has no show-more button, so nothing
            visible changes. Copy unchanged.
       v4 — Approved copy update (round 3, 25 Sep 2026): new hero intro
            (AB-03); the Hillary-connection text rewritten (AB-07, AB-08);
            the two links now read "Read our FAQs" and "About the
            Himalayan Trust" (same destinations, now 44px buttons); the rail
            and coach text rewritten (AB-12; the FAQ page's own answer is
            unchanged); new help-band text (SH-02). The guest speaker, the
            Antarctic Centre and Marlborough claims are still FLAGGED for
            approval (runbook section 7, A1-A3).
       v3 — Third independent review (25 Sep 2026): line length tightened to
            about 60 characters' width (~66-72 characters; the old caps
            rendered up to ~85); on phones the darker hero veil now also
            applies to compact heroes (shared kit).
       v2 — Review fixes (independent check, 25 Sep 2026): the hero banner is
            only 1920x480, so on desktop the hero is held at 480px (never
            enlarged) and phones get the tall photo of the same statue (a
            live Gallery photo) — sharp at every size. Two carousel photos
            left out and FLAGGED: the Wharf photo (its 640w file is an
            880 KB PNG) and the humpback whale (file name suggests a
            third-party library image; licence unconfirmed). Four photos
            remain. Declared: the old page's small Trustpilot box (hidden
            on phones) is not carried over — guest reviews are one tap away
            in the help band. Kicker/button type larger (shared kit).
       v1 — First new-design build of /about (Brief v2, 25 Sep 2026).
            Story in three parts: the Hillary connection (the live About
            text, verbatim, beside the 1960 portrait) · rail and coach (the
            FAQ's own answer, verbatim, and six photographs from the old
            carousel, now a still grid — no autoplay) · who we are (lines
            already on the live homepage and Journeys page). FAQ and
            Himalayan Trust links kept. Hero = the page's existing banner
            (Hillary statue, Aoraki Mt Cook). The carousel's 2025/26 route-
            map slide is not carried over (past season — flagged).
            FLAGGED FOR APPROVAL, NOT EDITED: the International Antarctic
            Centre visit; Marlborough / Mt Tapuae-o-Uenuku; "A guest speaker
            from the Hillary family".
     -----------------------------------------------------------------------
     WHERE IT GOES: page "about-new" (duplicate of /about). Delete every old
     content row, add ONE full-width row (padding 0), ONE HTML widget, paste
     this whole file. Steps + rollback: notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: no new tour facts; no rating hard-coded; no schema; no
     tracking; no departure data; CSS scoped to .sehe-pg-about.
     ===================================================================== -->"""

body = f"""{HEADER}
{FONTS}
{css('sehe-pg-about', EXTRA_CSS)}
<div class="sehe-pg-about">
{hero(HERO + '-1920w.jpg', 'About us', 'Inspired by Sir Edmund Hillary', E(AB03),
      img_alt='', label_id='sehe-ab-title', srcset=f'{HERO}-1920w.jpg 1920w', pos='28% 40%', extra_cls='ab-hero',
      mobile_srcset=f'{MOBILE_HERO}-640w.jpg 640w, {MOBILE_HERO}-1280w.jpg 1280w')}
<div class="sp-body">

  <section class="sp-section" aria-labelledby="sehe-ab-hillary">
    <div class="ab-story">
      <figure class="ab-portrait">
        <img src="{PORTRAIT}-640w.jpg" srcset="{PORTRAIT}-640w.jpg 640w, {PORTRAIT}-1920w.jpg 783w" sizes="(max-width: 860px) 420px, 480px" alt="Sir Edmund Hillary in 1960, smiling, in profile" width="640" height="800" loading="lazy">
        <figcaption class="ab-cap"><span class="ab-tag">Sir Edmund Hillary, 1960</span></figcaption>
      </figure>
      <div class="ab-copy">
        <p class="sp-kicker">The Hillary connection</p>
        <h2 id="sehe-ab-hillary" class="ab-h2">Our inspiration</h2>
        <p>{E(AB07)}</p>
        <p>{E(AB08)}</p>
        <div class="sp-actions ab-links">
          <a class="sp-btn sp-btn--ghost" href="/f-a-q">Read our FAQs</a>
          <a class="sp-btn sp-btn--ghost" href="/himalayan-trust">About the Himalayan Trust</a>
        </div>
      </div>
    </div>
  </section>

  <section class="sp-section" aria-labelledby="sehe-ab-rail">
    <div class="sp-head">
      <p class="sp-kicker">Rail and coach</p>
      <h2 id="sehe-ab-rail">How you travel</h2>
      <p>{E(AB12)}</p>
    </div>
    <ul class="ab-photos" role="list">
{chr(10).join(photo(*p) for p in PHOTOS)}
    </ul>
  </section>

  <section class="sp-section" aria-labelledby="sehe-ab-us">
    <div class="sp-head">
      <p class="sp-kicker">Who we are</p>
      <h2 id="sehe-ab-us">Part of Pounamu Tourism Group</h2>
      <p>Sir Edmund Hillary Explorer is part of <a href="https://www.pounamutourismgroup.com">Pounamu Tourism Group</a>.</p>
    </div>
    <ul class="ab-facts" role="list">
      <li><img src="{WTA}" alt="World Travel Awards winner shield, 2025" width="256" height="256" loading="lazy"><div><strong>World Travel Awards</strong><span>NZ&#8217;s Leading Tour Operator 2022 · 2023 · 2024 · 2025</span></div></li>
      <li><div><strong>Pounamu Tourism Group</strong><span>100% New Zealand owned &amp; operated</span></div></li>
    </ul>
  </section>

{band('Need help choosing the right tour?',
      E(SH02),
      [('View all journeys', '/journeys', 'gold', False), ('Guest reviews', '/reviews', 'light', False),
       ('Contact us', '/contact', 'light', False), (PHONE_TXT, PHONE_TEL, 'light', False)])}

</div>
</div>
"""
body = body.replace('<h2 id="sehe-ab-hillary" class="ab-h2">', '<h2 id="sehe-ab-hillary">')
EXTRA_H2 = '  @W .ab-copy h2 { font-size: clamp(28px, 3vw, 36px) !important; line-height: 1.2 !important; margin: 0 0 16px !important; }\n'
body = body.replace('  /* ── About page', EXTRA_H2.replace('@W', '.sehe-pg-about') + '  /* ── About page', 1)
out = os.path.join(REPO, 'SEHE-about-page_v8.txt')
body = body.rstrip('\n') + '\n' + end_marker('about-page.txt', 'v8') + '\n'
open(out, 'w', encoding='utf-8').write(body)
assert not check_script_safety(body)
assert not check_style_safety(body), check_style_safety(body)
open(os.path.join(OUT_DIR, 'verbatim-about.txt'), 'w', encoding='utf-8').write('\n'.join([AB03, AB07, AB08, AB12, SH02, 'Read our FAQs', 'About the Himalayan Trust', '100% New Zealand owned & operated', 'Sir Edmund Hillary Explorer is part of Pounamu Tourism Group.']) + '\n')
print('wrote', out, len(body))
