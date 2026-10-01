import re, html, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
REPO = REPO_ROOT
FAQ = json.load(open(os.path.join(DATA_DIR, 'faq-config.json'), encoding='utf-8'))['faqList']
assert len(FAQ) == 26


def clean(fragment):
    t = re.sub(r'<br\s*/?>', ' ', fragment)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t).replace(' ', ' ')).strip()


def paras_of(answer_html):
    return [clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', answer_html, re.S) if clean(p)]


QS = [clean(q['questionTitle']) for q in FAQ]
ANS = [paras_of(q['questionAnswer']) for q in FAQ]
assert all(ANS), [i for i, a in enumerate(ANS) if not a]

# Kirsty's answers (email, 26 Sep 2026): the ONLY changes to answer wording.
# Each old passage must occur exactly once in its answer.
ANSWER_EDITS = [
    ('What hygiene measures are in place during the tour?', 'F8',
     'is carried onboard each coach; however, we strongly encourage guests to bring their own personal supplies, including N95-grade face masks and Rapid Antigen Tests (RATs). Coach surfaces',
     'is carried onboard each coach. Coach surfaces'),
    ('What is your Cancellation Policy?', 'F3',
     'In the event that Pounamu Tourism Group cancels a tour, 100% refund will apply.',
     'If Pounamu Tourism Group cancels the tour, a 100% refund will apply. We will also try to offer different suitable dates as an option.'),
]
for _q, _code, _old, _new in ANSWER_EDITS:
    _i = QS.index(_q)
    _hits = [k for k, _p in enumerate(ANS[_i]) if _old in _p]
    assert len(_hits) == 1 and ANS[_i][_hits[0]].count(_old) == 1, (_code, _hits)
    ANS[_i][_hits[0]] = ANS[_i][_hits[0]].replace(_old, _new)

# Approved question wording (round 3, 25 Sep 2026). ANSWERS ARE LOCKED; only these 12
# questions change. Anchor IDs stay built from the ORIGINAL wording so every existing
# link (e.g. #faq-what-are-the-payment-terms) keeps working. Keys = original question text;
# the Q-numbers are the display order on this page.
NEWQ = {
    'I have mobility issues, can I join the tour?': ('Q2', 'Can I join the tour if I have limited mobility?'),
    'Is pre- or post-tour accommodation available?': ('Q8', 'Can I book accommodation before or after the tour?'),
    'What are the Payment Terms?': ('Q9', 'What are the payment terms?'),
    'How do I make bank payments to NZ from overseas?': ('Q10', 'How do I pay by bank transfer from overseas?'),
    'Do you accept payments by Paypal or Wise?': ('Q11', 'Do you accept payments by PayPal or Wise?'),
    'What is your Cancellation Policy?': ('Q12', 'What is your cancellation policy?'),
    'Where can I view the booking Terms & Conditions?': ('Q13', 'Where can I view the booking terms and conditions?'),
    'What should I pack to wear?': ('Q15', 'What clothes should I pack?'),
    'When can I book an Optional Extra Excursion?': ('Q16', 'When can I book an optional extra excursion?'),
    'Do I need Travel Insurance?': ('Q17', 'Do I need travel insurance?'),
    'What facilities are available on the Coach & Trains?': ('Q19', 'What facilities are available on the coach and trains?'),
    'How does seating work on the Coach and Trains?': ('Q21', 'How does seating work on the coach and trains?'),
}
assert all(k in QS for k in NEWQ), [k for k in NEWQ if k not in QS]
SHOWN = [NEWQ.get(q, (None, q))[1] for q in QS]      # display text; QS keeps the original

CATS = [
    ('faq-choosing', 'Choosing your journey', [0, 1, 3, 6, 7, 8, 14]),
    ('faq-booking', 'Booking and payments', [9, 10, 11, 12, 13, 21]),
    ('faq-before', 'Before you travel', [15, 16, 19, 22, 24]),
    ('faq-on-tour', 'On tour', [2, 4, 5, 17, 18, 20, 23, 25]),
]
assert sorted(i for _, _, ids in CATS for i in ids) == list(range(26))

EMAIL = 'info@pounamutourismgroup.com'


def slug(q):
    return 'faq-' + re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')[:60].rstrip('-')


def answer_html(i):
    out = []
    for p in ANS[i]:
        if i == 8:
            # three dash-led items in one paragraph -> the same words as a list
            items = [x.strip() for x in re.split(r'(?:^|\s)- (?=[A-Z][A-Za-z &]+:)', p) if x.strip()]
            assert len(items) == 3, items
            lis = []
            for it in items:
                label, rest = it.split(':', 1)
                lis.append(f'<li><strong>{E(label)}:</strong>{E(rest)}</li>')
            out.append('<ul class="fq-list">' + ''.join(lis) + '</ul>')
            continue
        t = E(p)
        if i in (11, 12):
            t = t.replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>', 1)
        if i == 21:
            assert p == 'Terms & conditions can be viewed here.', p
            t = 'Terms &amp; conditions can be viewed <a href="/terms-and-conditions">here.</a>'
        out.append(f'<p>{t}</p>')
    return '\n          '.join(out)


EXTRA_CSS = r"""
  /* ── FAQ page ───────────────────────────────────────────────────────── */
  /* top of the page: the four section links and 'Open all answers' are the
     SAME button (the kit's ghost button: 6px corners, 2px navy border, 16px
     Montserrat, 50px tall). One row on desktop; on phones the section links
     form a 2 x 2 grid of equal-height buttons with 'Open all answers' below. */
  @W .fq-top { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px 24px; }
  @W .fq-jump { display: flex; flex-wrap: wrap; gap: 10px; margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .fq-jump li { display: flex; margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .fq-jump li::before, @W .fq-jump li::marker { content: none !important; }
  @W .fq-jump .sp-btn { flex: 1 1 auto; }
  @W .fq-tools { margin: 0 !important; min-height: 50px; }
  @W .fq-cat { scroll-margin-top: 130px; }
  @W .fq-cat + .fq-cat { margin-top: 56px !important; }
  @W .fq-cat h2 { font-size: clamp(26px, 2.6vw, 32px) !important; line-height: 1.2 !important; margin: 0 0 18px !important; padding-bottom: 12px !important; border-bottom: 2px solid var(--gold); }
  @W .fq-item { scroll-margin-top: 130px; border: 1px solid var(--border); border-radius: 10px; background: #ffffff; margin: 0 0 12px !important; overflow: hidden; }
  @W .fq-item summary { list-style: none; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 60px; padding: 16px 20px !important; font-family: 'Montserrat', sans-serif !important; font-size: 17.5px !important; font-weight: 600 !important; line-height: 1.4 !important; color: var(--navy) !important; }
  @W .fq-item summary::-webkit-details-marker { display: none; }
  @W .fq-item summary::after { content: '+'; flex: none; width: 30px; height: 30px; border: 2px solid var(--gold); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; color: var(--gold-ink); font-size: 20px; font-weight: 600; line-height: 1; }
  @W .fq-item[open] summary::after { content: '\2212'; }
  @W .fq-item[open] summary { border-bottom: 1px solid var(--border-light); }
  @W .fq-item summary:hover { background: var(--cream); }
  @W .fq-item summary:focus-visible { outline-offset: -3px !important; }
  @W .fq-a { padding: 16px 20px 20px; max-width: 66ch; }
  @W .fq-a p { font-size: 17px !important; line-height: 1.7 !important; color: var(--text) !important; }
  @W .fq-a p + p, @W .fq-a p + ul, @W .fq-a ul + p { margin-top: 12px !important; }
  @W .fq-list { margin: 0 !important; padding: 0 0 0 22px !important; }
  @W .fq-list li { margin: 0 0 10px !important; font-size: 17px !important; line-height: 1.7 !important; color: var(--text) !important; list-style: disc !important; }
  @W .fq-list li strong { color: var(--navy); }
  @media (max-width: 860px) {
    @W .fq-top { display: block; }
    @W .fq-jump { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-auto-rows: 1fr; }
    @W .fq-jump .sp-btn { width: 100%; padding: 10px 14px; }
    @W .fq-tools { margin: 10px 0 0 !important; }
    @W .fq-tools .sp-btn { width: 100%; }
    @W .fq-item summary { font-size: 17px !important; padding: 14px 16px !important; }
    @W .fq-a { padding: 14px 16px 18px; }
  }
"""

ENHANCE = r"""<script>
(function () {
  /* FAQ enhancements — add only. (1) A link to a question (#faq-...) opens
     that answer. (2) An "Open all answers" button. With JS off every
     question still opens on its own. No less-than sign and no ampersand. */
  var root = document.querySelector('.sehe-pg-faq');
  if (!root) return;
  var items = Array.prototype.slice.call(root.querySelectorAll('details.fq-item'));
  function openFromHash() {
    var id = decodeURIComponent((location.hash || '').replace('#', ''));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    if (el.tagName === 'DETAILS') { el.open = true; el.scrollIntoView(); }
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);
  var slot = root.querySelector('[data-fq-tools]');
  if (!slot) return;
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'sp-btn sp-btn--ghost';
  btn.setAttribute('aria-controls', 'faq-accordion-1');
  function label() {
    var allOpen = items.every(function (d) { return d.open; });
    btn.textContent = allOpen ? 'Close all answers' : 'Open all answers';
    btn.setAttribute('aria-expanded', allOpen ? 'true' : 'false');
  }
  btn.addEventListener('click', function () {
    var allOpen = items.every(function (d) { return d.open; });
    items.forEach(function (d) { d.open = !allOpen; });
    label();
  });
  items.forEach(function (d) { d.addEventListener('toggle', label); });
  label();
  slot.appendChild(btn);
})();
</script>"""

HERO = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/185465114_4147253738668973_1837289544185548089_n'

HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — FAQ PAGE (/f-a-q)
     COMPLETE PAGE  ·  VERSION v8  ·  2026-09-26  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
       v8 — F3 wording corrected (26 Sep 2026). v7 made the refund
            conditional ("If none suit"), which Kirsty did not say. The
            answer keeps the refund and adds her point separately: "If
            Pounamu Tourism Group cancels the tour, a 100% refund will
            apply. We will also try to offer different suitable dates as
            an option." The Terms use the same words. Nothing else changed.
       v7 — Kirsty's answers (email, 26 Sep 2026). F8: the hygiene answer
            loses the sentence about bringing N95-grade masks and Rapid
            Antigen Tests. F3: when we cancel a tour, the cancellation answer
            now says we will try to offer different suitable dates as an
            option, and a 100% refund applies if none suit (matching the
            Terms). END OF FILE line added. Every other answer, question and
            anchor ID unchanged.
       v6 — Ben (25 Sep 2026): every button at the top is rounded the same.
            The four section links were pills; they are now the same ghost
            button as 'Open all answers' (6px corners, 2px navy border,
            16px Montserrat, 50px tall), in one row on desktop. On phones
            they form a 2 x 2 grid of equal-height buttons, with 'Open all
            answers' full width below. Copy, answers and anchor IDs
            unchanged.
       v5 — Fix before first paste (25 Sep 2026): Duda publishes the CSS
            child combinator as an HTML entity and the browser drops the
            rule, so the question accordions would have lost their styling
            and the +/- signs on the live page. Every selector now uses
            plain descendant selectors. Copy, answers and anchor IDs
            unchanged.
       v4 — Approved copy update (round 3, 25 Sep 2026): 12 QUESTIONS reworded
            (Q2, Q8-Q13, Q15-Q17, Q19, Q21 in this page's order). Every
            answer is unchanged, word for word, and every anchor ID is
            unchanged (IDs still come from the original question wording,
            so links like #faq-what-are-the-payment-terms keep working).
       v3 — Third independent review (25 Sep 2026): line length tightened to
            about 60 characters' width (~66-72 characters; the old caps
            rendered up to ~85); on phones the darker hero veil now also
            applies to compact heroes (shared kit).
       v2 — Review fixes (independent check, 25 Sep 2026): no tag-like tokens
            left in comments; the bold item labels in "What is not included"
            are now declared below; conflicts with other pages are listed in
            the runbook section 7. Kicker/button type larger (shared kit).
            Wording unchanged (all 26 answers re-verified).
       v1 — First new-design build of /f-a-q (Brief v2, 25 Sep 2026).
            All 26 questions and answers from the live FAQ widget, WORDING
            UNCHANGED (payment and cancellation terms included), grouped in
            four sections with jump links: Choosing your journey · Booking
            and payments · Before you travel · On tour. Native details and
            summary accordions (keyboard and screen-reader friendly, work
            with JS off); each question has its own link (#faq-...).
            Presentation-only changes: the three dash-led items in "What is
            not included in the tour price?" show as a bulleted list with
            each item's label in bold (same words); the
            email address in the two payment answers is a mailto: link;
            the Terms link is a normal same-tab link. No FAQPage schema.
            Facts that disagree with other pages are FLAGGED in the runbook
            (section 7), not edited.
     -----------------------------------------------------------------------
     WHERE IT GOES: page "f-a-q-new" (duplicate of /f-a-q). Delete every old
     content row, add ONE full-width row (padding 0), ONE HTML widget, paste
     this whole file. Steps + rollback: notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: no schema; no rating; no tracking; no departure data; CSS
     scoped to .sehe-pg-faq; script adds only.
     ===================================================================== -->"""

cats_html = []
for cid, title, ids in CATS:
    items = []
    for i in ids:
        items.append(f"""      <details class="fq-item" id="{slug(QS[i])}">
        <summary>{E(SHOWN[i])}</summary>
        <div class="fq-a">
          {answer_html(i)}
        </div>
      </details>""")
    cats_html.append(f"""    <section class="fq-cat" id="{cid}" aria-labelledby="{cid}-h">
      <h2 id="{cid}-h">{title}</h2>
{chr(10).join(items)}
    </section>""")

jump = '\n'.join(f'      <li><a class="sp-btn sp-btn--ghost" href="#{cid}">{title}</a></li>' for cid, title, _ in CATS)

body = f"""{HEADER}
{FONTS}
{css('sehe-pg-faq', EXTRA_CSS)}
<div class="sehe-pg-faq">
{hero(HERO + '-1920w.jpg', 'FAQ', 'Frequently Asked Questions',
      'Answers to the questions we hear most often. Can&#39;t find what you need? Our New Zealand team is here to help.',
      compact=True, srcset=f'{HERO}-640w.jpg 640w, {HERO}-1280w.jpg 1280w, {HERO}-1920w.jpg 1920w', label_id='sehe-fq-title', pos='center 55%')}
<div class="sp-body">
  <nav class="sp-section fq-top" aria-label="FAQ sections">
    <ul class="fq-jump" role="list">
{jump}
    </ul>
    <div class="fq-tools" data-fq-tools></div>
  </nav>
  <div class="sp-section" id="faq-accordion-1">
{chr(10).join(cats_html)}
  </div>
{band('Can&#39;t find your answer?', 'Our New Zealand team is here to help. Call us, or send us a message from the contact page.',
      [('Contact us', '/contact', 'gold', False), (PHONE_TXT, PHONE_TEL, 'light', False), ('View all journeys', '/journeys', 'light', False)])}
</div>
</div>
{ENHANCE}
"""
out = os.path.join(REPO, 'SEHE-faq-page_v8.txt')
body = body.rstrip('\n') + '\n' + end_marker('faq-page.txt', 'v8') + '\n'
open(out, 'w', encoding='utf-8').write(body)
assert not check_script_safety(body), check_script_safety(body)
assert not check_style_safety(body), check_style_safety(body)
# verbatim list: every question and every answer paragraph (answer 8 checked item by item)
vb = []
for i in range(26):
    vb.append(SHOWN[i])
    for p in ANS[i]:
        if i == 8:
            vb += [x.strip() for x in re.split(r'(?:^|\s)- (?=[A-Z][A-Za-z &]+:)', p) if x.strip()]
        else:
            vb.append(p)
open(os.path.join(OUT_DIR, 'verbatim-faq.txt'), 'w', encoding='utf-8').write('\n'.join(vb) + '\n')
print('wrote', out, len(body), 'bytes;', len(vb), 'verbatim passages')
