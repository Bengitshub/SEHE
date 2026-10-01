import re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
LIVE = open(live_path('reviews.html'), encoding='utf-8').read()

# ── Earlier guest feedback: pulled straight from the live page's paragraph
#    widgets (Lisa Godwin … Francie Taylor), text kept exactly as published.
def para_widgets(h):
    out = []
    for m in re.finditer(r'<div class="[^"]*dmNewParagraph[^"]*"[^>]*data-element-type="paragraph"[^>]*id="(\d+)"[^>]*>(.*?)</div>', h, re.S):
        ps = re.findall(r'<p[^>]*>(.*?)</p>', m.group(2), re.S)
        txt = []
        for p in ps:
            for seg in re.split(r'<br\s*/?>', p):   # <br> separates name and quote in some widgets
                t = re.sub(r'<[^>]+>', '', seg)
                t = html.unescape(t).replace('\u00a0', ' ')
                t = re.sub(r'\s+', ' ', t).strip()
                if t:
                    txt.append(t)
        out.append((m.group(1), txt))
    return out

widgets = para_widgets(LIVE)
start = next(i for i, (wid, t) in enumerate(widgets) if t and t[0].startswith('Lisa Godwin'))
end = next(i for i, (wid, t) in enumerate(widgets) if t and t[0].startswith('Francie Taylor'))
EARLIER_ALL = [(wid, t) for wid, t in widgets[start:end + 1]]
assert len(EARLIER_ALL) == 17, len(EARLIER_ALL)
# An entry whose name links to a Trustpilot user profile on the live page is a
# Trustpilot review: it cannot sit in direct guest feedback with a travel date
# (Guardrails 8/9), and it cannot be shown as a Trustpilot review without its
# review date. It is left out and flagged. Exactly one entry (Lisa Godwin).
def tp_linked(wid):
    m = re.search(r'<div[^>]*\bid="%s"[^>]*>(.*?)</div>' % wid, LIVE, re.S)
    return 'trustpilot.com/users/' in m.group(1)
DROPPED = [t for wid, t in EARLIER_ALL if tp_linked(wid)]
assert [t[0].split(',')[0] for t in DROPPED] == ['Lisa Godwin'], DROPPED
EARLIER = [t for wid, t in EARLIER_ALL if not tp_linked(wid)]
assert len(EARLIER) == 16
press_intro = next(t for wid, t in widgets if t and t[0].startswith('Newspaper articles'))
assert 'originally called the Great Southern Steam Tour before a relationship was established with Hillary family last year' in ' '.join(press_intro), press_intro

# ── Selected Trustpilot reviews — VERBATIM from the brief's appendix (all
#    5-star; dates are REVIEW dates). Do not edit wording or punctuation.
TP = [
 # Supplied 25 Sep 2026 from the public Trustpilot profile (round-2 feedback), all 5-star,
 # newest first; dates are the months the reviews were POSTED. Verbatim, typos and
 # spacing included ("experiences hosts", "superb !", "sites", "Accommodation,food").
 ('Louise H.', 'Australia', 'September 2026', ['What a wonderful trip! fantastic driver and passionate, friendly and caring guides. Nothing was too much trouble. Accommodation throughout was great and the food was exceptional.']),
 ('Graeme M.', 'Australia', 'August 2026', ["What a great experience. Looked after from day 1 right to the end by experiences hosts. Great sights, accommodation, experiences and food. I'd do it again anytime."]),
 ('SC H.', 'USA', 'July 2026', ["The tour was well organized and gave us broad exposure to New Zealand's natural diversity. We also enjoyed learning more about New Zealand's culture and history. …"]),
 ('Pam L.', 'New Zealand', 'July 2026', ['It allowed me to catch up on experiences that over the years living in NZ I had missed. It was paced so that you were never really rushed and had time to take all the sites in. Great tour guides and they created a great atmosphere amongst the travelers and they created many laughs all along the trip. …']),
 ('Mike', 'New Zealand', 'July 2026', ['The holiday was superb ! The route was well thought out to take in most of the places that we wanted to visit in South Island, and was so well organised. The guides ran a smooth operation and were most helpful when rain prevented tours on one day. We met some lovely people, had a lot of laughs and thoroughly enjoyed ourselves. Recommended !']),
 ('Jo B.', 'USA', 'June 2026', ['Every day is full of wonderful surprises! The destinations are remarkable but the beauty of this trip is all of the carefully thought out stops for coffee, ice cream, views, waterfalls or even short walks with very few other tourist groups. I highly recommend this tour. I’m doing a repeat!']),
 ('Rick P.', 'USA', 'June 2026', ['This was an incredible trip! Our guides and driver were exceptional! We are early 70’s but fit and the pace of the trip was perfect. … This was a wonderfully organized trip and all the hotels and food stops were very good. …']),
 ('Leonie M.', 'Australia', 'June 2026', ['From start to finish this experience was amazing. Accommodation,food,experiences & guides were exceptional. Everything was as stated & the commentary and knowledge of the guides was amazing.']),
 ('Doug D.', 'Canada', 'June 2026', ["The South Island is the true heart of New Zealand, and I can't think of a better way to experience it than with this particular tour. Trains, boats, and coaches took us to all the spots worth seeing, often in a better-planned fashion than other tours we observed. Friendly, helpful staff, excellent meals (even for us vegetarians), along with cooperative weather made this perfect. …"]),
 ('Richard S.', 'Australia', 'May 2026', ['Thank you for such a brilliant, well organised adventure. From day one to the last day everything flowed like a well oiled machine. We were very fortunate with the weather being able to see snow capped mountains, cascading waterfalls and glistening lakes. Highlights are too many to list. …']),
 ('Ellen J.', 'Australia', 'April 2026', ['Words can not describe the beauty you will see, the wonderful people you will meet and the fun you will have on this tour. From the start when you book your tour until your final day on the tour it’s all so easy and they look after you, they care. A truly unforgettable experience.']),
 ('David', 'USA', 'March 2026', ['I would describe this as a "world-class" tour. The guides and drivers were amazing. The organization and logistics were impressive. The South Island is vast, beautiful, interesting, and often spectacular. We can definitely recommend the "Sir Edmund Hillary Explorer" Tour.']),
]
assert len(TP) == 12


def tp_card(name, country, when, paras):
    body = '\n'.join(f'          <p>{E(p)}</p>' for p in paras)
    return f"""      <li class="rv-card">
        <figure>
          <img class="rv-stars" src="{TP_STARS_IMG}" alt="5 out of 5 stars" width="1000" height="188" loading="lazy">
          <blockquote cite="{TP_PROFILE}">
{body}
          </blockquote>
          <figcaption><span class="rv-name">{E(name)}</span>, {E(country)}<br>Reviewed {E(when)} on <a href="{TP_PROFILE}" target="_blank" rel="noopener">Trustpilot{NEWTAB}</a></figcaption>
        </figure>
      </li>"""


def earlier_item(lines):
    attrib, paras = lines[0], lines[1:]
    name, rest = attrib.split(',', 1)
    body = '\n'.join(f'          <p>{E(p)}</p>' for p in paras)
    return f"""      <figure class="rv-quote">
        <blockquote>
{body}
        </blockquote>
        <figcaption><strong>{E(name)}</strong>,{E(rest)}</figcaption>
      </figure>"""


PRESS = [
 ('Stuff', 'https://www.stuff.co.nz/travel/back-your-backyard/300285057/all-aboard-for-the-first-great-southern-train-tour',
  'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/N34A3054-500eeb72-640w.jpg', 640, 340, 'The Marlborough Flyer'),
 ('Otago Daily Times', 'https://www.odt.co.nz/news/dunedin/south-just-beautiful-by-train-iwwoh6fm',
  'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/Southland+track-640w.jpg', 640, 640, 'Southland Amazing Views'),
 ('NZ Herald', 'https://www.nzherald.co.nz/nz/flyer-to-return-as-part-of-southern-rail-tour-after-eight-years/H6B3Z5BLTUFTBJTFOPM2EDEZAA/',
  'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/Kingston-Flyer-About-SEHE-Rail-Tour-1-640w.jpg', 640, 427, 'The Kingston Flyer'),
]
# the three press links must be the live page's own links
MOVED = {  # live-page link -> current address of the same article (checked 25 Sep 2026: 200)
    'https://www.nzherald.co.nz/nz/flyer-to-return-as-part-of-southern-rail-tour-after-eight-years/H6B3Z5BLTUFTBJTFOPM2EDEZAA/':
        'https://www.nzherald.co.nz/travel/flyer-to-return-as-part-of-southern-rail-tour-after-eight-years/H6B3Z5BLTUFTBJTFOPM2EDEZAA/',
    'https://www.odt.co.nz/news/dunedin/south-just-beautiful-by-train-iwwoh6fm':
        'https://www.odt.co.nz/news/dunedin/south-%E2%80%98just-beautiful%E2%80%99-train',
}
for _, url, img, *_ in PRESS:
    assert MOVED.get(url, url) in LIVE, url
    assert img in LIVE, img

HERO_BASE = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/TranzAlpine--View-of-Cragieburn-Range-across-Lake-Sarah--CLEM1410_-43.050997-171.773006--CROP'
# poster for the click-to-load video: the video's own thumbnail from Vimeo oEmbed (width=1280), 25 Sep 2026
VIMEO_THUMB = 'https://i.vimeocdn.com/video/1995021277-0571f59c32ed5cb894ea27fe0106547312b38278a5633158b36df60a16841444-d_1280?region=us'
assert HERO_BASE in LIVE

EXTRA_CSS = r"""
  /* ── Reviews page ───────────────────────────────────────────────────── */
  @W .rv-proof { display: flex; flex-wrap: wrap; align-items: center; gap: 16px 24px; margin-top: 28px; }
  @W .rv-trustbox { width: 100%; max-width: 440px; min-height: 24px; }
  @W .rv-trustbox a { color: #ffffff !important; font-weight: 600; }
  @W .rv-grid { list-style: none !important; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 330px), 1fr)); gap: 22px; align-items: stretch; }
  @W .rv-card { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .rv-card::before, @W .rv-card::marker { content: none !important; }
  @W .rv-card figure { margin: 0 !important; height: 100%; display: flex; flex-direction: column; background: #ffffff; border: 1px solid var(--border); border-radius: 12px; padding: 26px 26px 22px; }
  @W .rv-stars { display: block; width: 118px; height: auto; margin: 0 0 16px; }
  @W .rv-card blockquote { flex: 1 1 auto; margin: 0 0 20px !important; padding: 0 !important; border: 0 !important; quotes: none; background: none !important; }
  @W .rv-card blockquote p { font-size: 17.5px !important; line-height: 1.7 !important; color: var(--text) !important; font-style: normal !important; }
  @W .rv-card figcaption { border-top: 1px solid var(--border-light); padding-top: 14px; font-size: 15.5px !important; line-height: 1.55 !important; color: var(--text-2) !important; }
  @W .rv-name { font-family: 'Montserrat', sans-serif !important; font-weight: 700; color: var(--navy); font-size: 16px; }
  @W .rv-more { margin-top: 24px; }
  @W .rv-more .rv-grid { margin-top: 24px !important; }
  @W .rv-all { margin-top: 26px !important; }
  @W .rv-video-frame { position: relative; width: 100%; max-width: 900px; background: var(--navy-dark); border-radius: 12px; overflow: hidden; }
  @W .rv-video-frame::before { content: ''; display: block; padding-top: 56.25%; }
  @W .rv-video-frame iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
  /* click-to-load: poster + play button; the player loads only when asked (also covers blocked Vimeo) */
  @W .rv-video-facade { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: block; color: #ffffff !important; text-decoration: none !important; }
  @W .rv-video-facade img { position: absolute; top: 0; left: 0; width: 100% !important; height: 100% !important; object-fit: cover; }
  @W .rv-video-facade::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 45%; background: linear-gradient(180deg, rgba(8,21,37,0) 0%, rgba(8,21,37,.85) 100%); }
  @W .rv-play { position: absolute; top: 50%; left: 50%; width: 84px; height: 84px; margin: -42px 0 0 -42px; border-radius: 50%; background: rgba(14,45,82,.88); border: 3px solid #ffffff; z-index: 2; transition: transform .2s, background-color .2s; }
  @W .rv-play::before { content: ''; position: absolute; top: 50%; left: 50%; margin: -15px 0 0 -9px; border-style: solid; border-width: 15px 0 15px 26px; border-color: transparent transparent transparent #ffffff; }
  @W .rv-video-facade:hover .rv-play { transform: scale(1.06); background: var(--gold-ink); }
  @W .rv-video-facade:focus-visible { outline: 3px solid var(--navy) !important; outline-offset: 3px !important; }
  @W .rv-video-title { position: absolute; left: 22px; right: 22px; bottom: 18px; z-index: 2; font-family: 'Montserrat', sans-serif !important; font-size: 18px !important; font-weight: 600 !important; line-height: 1.35 !important; color: #ffffff !important; text-shadow: 0 1px 10px rgba(8,21,37,.8); }
  @W .rv-video-len { font-weight: 400; opacity: .9; }
  @media (max-width: 540px) {
    @W .rv-play { top: 40%; width: 60px; height: 60px; margin: -30px 0 0 -30px; }
    @W .rv-play::before { margin: -11px 0 0 -6px; border-width: 11px 0 11px 19px; }
    @W .rv-video-title { font-size: 15px !important; left: 14px; right: 14px; bottom: 10px; }
  }
  @W .rv-video-link { margin-top: 14px !important; }
  @W .rv-write { background: var(--cream); border: 1px solid var(--border-light); border-left: 4px solid var(--gold); border-radius: 12px; padding: 28px 32px !important; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 18px 32px; }
  @W .rv-write h2 { font-size: clamp(24px, 2.4vw, 28px) !important; margin: 0 0 6px !important; }
  @W .rv-write-copy { flex: 1 1 420px; }
  @W .rv-press { list-style: none !important; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 22px; }
  @W .rv-press li { margin: 0 !important; padding: 0 !important; list-style: none !important; background: #ffffff; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
  @W .rv-press li::before, @W .rv-press li::marker { content: none !important; }
  @W .rv-press img { display: block; width: 100%; height: 210px; object-fit: cover; }
  @W .rv-press-body { padding: 18px 22px 22px; display: flex; flex-direction: column; align-items: flex-start; gap: 14px; flex: 1 1 auto; }
  @W .rv-press h3 { font-size: 20px !important; line-height: 1.3 !important; }
  @W .rv-earlier-list { margin-top: 26px; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 440px), 1fr)); gap: 30px 40px; }
  @W .rv-quote { margin: 0 !important; padding: 2px 0 2px 20px !important; border-left: 3px solid var(--gold); }
  @W .rv-quote blockquote { margin: 0 0 10px !important; padding: 0 !important; border: 0 !important; background: none !important; }
  @W .rv-quote blockquote p { color: var(--text) !important; font-style: normal !important; }
  @W .rv-quote blockquote p + p { margin-top: 10px !important; }
  @W .rv-quote blockquote p, @W .rv-quote figcaption { max-width: 60ch; }
  @W .rv-video-link a { display: inline-flex; align-items: center; min-height: 44px; }
  @W .rv-card figcaption a { display: inline-block; padding: 8px 0; margin: -8px 0; }
  @W .rv-quote figcaption { font-size: 15.5px !important; line-height: 1.5 !important; color: var(--text-2) !important; }
  @W .rv-quote figcaption strong { font-family: 'Montserrat', sans-serif !important; color: var(--navy); font-weight: 700; }
  @media (max-width: 860px) {
    @W .rv-card figure { padding: 22px 20px 18px; }
    @W .rv-write { padding: 22px 20px !important; }
    @W .rv-proof .sp-btn, @W .rv-write .sp-btn, @W .rv-more summary { width: 100%; justify-content: center; }
    @W .rv-press img { height: 190px; }
  }
"""

hero_extra = f"""    <div class="rv-proof">
      <div id="sehe-rv-trustbox" class="trustpilot-widget rv-trustbox" data-locale="en-NZ" data-template-id="{TP_MICRO_COMBO}" data-businessunit-id="{TP_BU}" data-style-height="20px" data-style-width="100%" data-theme="dark">
        <a href="{TP_PROFILE}" target="_blank" rel="noopener">Read our reviews on Trustpilot{NEWTAB}</a>
      </div>
      <a class="sp-btn sp-btn--gold" href="{TP_PROFILE}" target="_blank" rel="noopener">Read all reviews on Trustpilot{NEWTAB}</a>
    </div>"""

first, rest = TP[:6], TP[6:]
press_items = '\n'.join(f"""      <li>
        <img src="{img}" alt="{A(alt)}" width="{w}" height="{h}" loading="lazy">
        <div class="rv-press-body">
          <h3>{E(pub)}</h3>
          <a class="sp-btn sp-btn--ghost" href="{url}" target="_blank" rel="noopener">Read the {E(pub)} article{NEWTAB}</a>
        </div>
      </li>""" for pub, url, img, w, h, alt in PRESS)

HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — REVIEWS PAGE (/reviews)
     COMPLETE PAGE  ·  VERSION v7  ·  2026-09-25  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
       v7 — END OF FILE line added as the last line (25 Sep 2026): if it is
            the last line in Duda's code box, the whole file is pasted (two
            Contact pastes had been cut off at line 150). Page code
            identical to v6.
       v6 — Fix (25 Sep 2026): the "Show 6 more reviews" button showed as
            plain text on the published page and its label never changed
            to "Show fewer reviews". Duda publishes the CSS child
            combinator as an HTML entity, which drops the rule; every
            selector now uses plain descendant selectors. Copy unchanged.
       v5 — Approved copy update (round 3, 25 Sep 2026): H1 "What our guests
            say"; new hero intro; the intro paragraphs under "Selected
            reviews" and "Earlier guest feedback" removed (each review card
            still shows "Reviewed [month year] on Trustpilot", and the "Read
            all reviews on Trustpilot" link stays below the cards); video
            heading "Hear from our guests", and the play button's label
            matches; press heading "Our first tour in 2021" with a new
            intro; new help-band text (SH-02). Reviews and testimonials
            unchanged, word for word.
       v4 — Round-2 feedback (25 Sep 2026): the 12 selected Trustpilot reviews
            replaced with the newer set taken from the public profile on
            25 Sep 2026 (Louise H. Sep 2026 ... David Mar 2026), verbatim,
            newest first, 6 shown + 6 behind "Show more". Video is now
            click-to-load: the video's own Vimeo thumbnail as the poster,
            a play button and the title; the player loads on click (a
            plain Vimeo link without JS; also covers networks that block
            Vimeo); "Watch on Vimeo" kept. The help band no longer links
            straight to /brochure-collection (every brochure form redirects
            there, and a visit counts as a brochure conversion).
       v3 — Third independent review (25 Sep 2026): line length tightened to
            about 60 characters' width (~66-72 characters; the old caps
            rendered up to ~85); on phones the darker hero veil now also
            applies to compact heroes (shared kit).
       v2 — Review fixes (independent check, 25 Sep 2026): Lisa Godwin's entry
            left out of earlier guest feedback — on the live site her name
            links to her Trustpilot profile, so it is a Trustpilot review and
            cannot be shown as direct feedback with a travel date (flagged;
            16 entries remain). NZ Herald link updated to the article's
            current address (the old one returns 404); ODT link set to its
            current address (the old one redirects). Earlier-feedback lines
            capped at 68 characters; "Watch on Vimeo" and the review-card
            Trustpilot links get bigger tap areas; kicker/button type larger.
       v1 — First new-design build of /reviews (Brief v2, 25 Sep 2026).
            Order: hero with the live TrustBox · selected Trustpilot reviews
            (6 shown + 6 behind "Show more", all in the HTML) · guest video ·
            "Travelled with us?" link · In the press · earlier guest feedback
            2021–2025 (collapsed) · help band with journeys/brochures/contact.
            Copy sources: Trustpilot reviews = the brief's appendix, verbatim,
            review dates; earlier feedback, press links, video and banner photo
            = the live /reviews page (25 Sep 2026), verbatim. Two deliberate
            edits: the press note drops "last year" (stale; no year added) and
            reads "the Hillary family".
     -----------------------------------------------------------------------
     WHERE IT GOES: page "reviews-new" (duplicate of /reviews). Delete every
     old content row, add ONE full-width row (padding 0, no max width) with
     ONE HTML widget, paste this whole file. Full steps + rollback:
     notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: no rating/score/count is hard-coded — the only rating shown
     is the live TrustBox (Micro Combo, template 5419b6ffb0d04a076446a9af).
     No Trustpilot bootstrap here (Head HTML loads it once, site-wide); the
     script below only asks it to render this box. No schema markup. No
     departure data. No tracking code. All CSS scoped to .sehe-pg-reviews.
     ===================================================================== -->"""

body = f"""{HEADER}
{FONTS}
{css('sehe-pg-reviews', EXTRA_CSS)}
<div class="sehe-pg-reviews">
{hero(HERO_BASE + '-1920w.webp', 'Guest reviews', 'What our guests say',
      'From scenic rail journeys to the people along the way, hear what our guests remember most.',
      hero_extra, srcset=f'{HERO_BASE}-640w.webp 640w, {HERO_BASE}-1280w.webp 1280w, {HERO_BASE}-1920w.webp 1920w',
      img_alt='', label_id='sehe-rv-title')}
<div class="sp-body">

  <section class="sp-section" aria-labelledby="sehe-rv-selected">
    <div class="sp-head">
      <p class="sp-kicker">From Trustpilot</p>
      <h2 id="sehe-rv-selected">Selected reviews</h2>
    </div>
    <ul class="rv-grid" role="list">
{chr(10).join(tp_card(*r) for r in first)}
    </ul>
    <details class="sp-more rv-more">
      <summary><span class="sp-when-closed">Show 6 more reviews</span><span class="sp-when-open">Show fewer reviews</span></summary>
      <ul class="rv-grid" role="list">
{chr(10).join(tp_card(*r) for r in rest)}
      </ul>
    </details>
    <p class="rv-all"><a class="sp-btn" href="{TP_PROFILE}" target="_blank" rel="noopener">Read all reviews on Trustpilot{NEWTAB}</a></p>
  </section>

  <section class="sp-section" aria-labelledby="sehe-rv-video">
    <div class="sp-head">
      <p class="sp-kicker">Guest video</p>
      <h2 id="sehe-rv-video">Hear from our guests</h2>
    </div>
    <div class="rv-video-frame">
      <a class="rv-video-facade" href="https://vimeo.com/1067162461" data-sehe-video="https://player.vimeo.com/video/1067162461?autoplay=1&amp;dnt=1" data-sehe-video-title="The Sir Edmund Hillary Explorer Rail &amp; Coach Tour - More Passenger Testimonials">
        <img src="{VIMEO_THUMB}" alt="" width="1280" height="720" loading="lazy">
        <span class="rv-play" aria-hidden="true"></span>
        <span class="rv-video-title">Play the video: Hear from our guests <span class="rv-video-len">(1 min 30 sec)</span></span>
      </a>
    </div>
    <p class="rv-video-link"><a href="https://vimeo.com/1067162461" target="_blank" rel="noopener">Watch on Vimeo{NEWTAB}</a></p>
  </section>

  <section class="sp-section rv-write" aria-labelledby="sehe-rv-write">
    <div class="rv-write-copy">
      <h2 id="sehe-rv-write">Travelled with us?</h2>
      <p>We would love to hear how your journey went. You can share your experience on Trustpilot.</p>
    </div>
    <a class="sp-btn sp-btn--ghost" href="{TP_WRITE}" target="_blank" rel="noopener">Write a review on Trustpilot{NEWTAB}</a>
  </section>

  <section class="sp-section" aria-labelledby="sehe-rv-press">
    <div class="sp-head">
      <p class="sp-kicker">In the press</p>
      <h2 id="sehe-rv-press">Our first tour in 2021</h2>
      <p>Our first tour was called the Great Southern Steam Tour. Our association with the Hillary family came later.</p>
    </div>
    <ul class="rv-press" role="list">
{press_items}
    </ul>
  </section>

  <section class="sp-section" aria-labelledby="sehe-rv-earlier">
    <div class="sp-head">
      <p class="sp-kicker">Guest feedback</p>
      <h2 id="sehe-rv-earlier">Earlier guest feedback, 2021–2025</h2>
    </div>
    <details class="sp-more">
      <summary><span class="sp-when-closed">Show earlier guest feedback</span><span class="sp-when-open">Hide earlier guest feedback</span></summary>
      <div class="rv-earlier-list">
{chr(10).join(earlier_item(x) for x in EARLIER)}
      </div>
    </details>
  </section>

{band('Need help choosing the right tour?',
      'Talk to our New Zealand team about dates, rooms and what you&#39;d like to see. We&#39;ll help you choose a journey that suits you.',
      [('View all journeys', '/journeys', 'gold', False),
       ('Contact us', '/contact', 'light', False), (PHONE_TXT, PHONE_TEL, 'light', False)])}

</div>
</div>
{trustbox_loader('sehe-rv-trustbox')}
<script>
(function () {{
  /* Click-to-load video: the Vimeo player is created only when the visitor
     presses play. Without JS the poster is a plain link to the video on
     Vimeo. No less-than sign and no ampersand in this script. */
  var a = document.querySelector('.sehe-pg-reviews [data-sehe-video]');
  if (!a) return;
  a.addEventListener('click', function (e) {{
    e.preventDefault();
    var f = document.createElement('iframe');
    f.src = a.getAttribute('data-sehe-video');
    f.title = a.getAttribute('data-sehe-video-title') || 'Video';
    f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
    f.setAttribute('allowfullscreen', '');
    a.parentNode.replaceChild(f, a);
    f.focus();
  }});
}})();
</script>
"""

out = os.path.join(REPO_ROOT, 'SEHE-reviews-page_v7.txt')
body = body.rstrip('\n') + '\n' + end_marker('reviews-page.txt', 'v7') + '\n'
open(out, 'w', encoding='utf-8').write(body)
bad = check_script_safety(body)
assert not bad, bad
assert not check_style_safety(body), check_style_safety(body)
print('wrote', out, len(body), 'bytes;', len(EARLIER), 'earlier items;', len(TP), 'TP reviews; dropped:', [d[0] for d in DROPPED])
