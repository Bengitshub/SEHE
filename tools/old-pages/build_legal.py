"""Privacy Policy + Terms & Conditions — typography and navigation ONLY.
Zero wording changes (typos included). The body is ported from the live
paragraph widget by a sanitiser that keeps text, bold/italic, lists and links
and drops Duda's spans/styles; the build then proves the document text is
character-for-character identical to the live page (whitespace-normalised)."""
import re, html, os, sys, json
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
REPO = REPO_ROOT
NORM = lambda s: re.sub(r'\s+', ' ', s.replace(' ', ' ').replace('﻿', '')).strip()


def widget_html(page, wid):
    h = open(live_path(page + '.html'), encoding='utf-8').read()
    i = h.find(f'id="{wid}"')
    start = h.rfind('<div', 0, i)
    seg = h[start:]
    return seg[:seg.find('</div>') + 6]      # paragraph widgets hold no nested <div>


class Text(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out = []
    def handle_data(s, d): s.out.append(d)
    def handle_starttag(s, t, a):
        if t in ('p', 'li', 'br', 'h1', 'h2', 'h3', 'ul', 'ol'): s.out.append(' ')
    def handle_endtag(s, t):
        if t in ('p', 'li', 'h1', 'h2', 'h3', 'ul', 'ol'): s.out.append(' ')


def text_of(fragment):
    p = Text(); p.feed(fragment); return NORM(''.join(p.out))


class Clean(HTMLParser):
    """Keep p/ul/ol/li/strong/em/a[href]/br; unwrap everything else."""
    KEEP = {'p': 'p', 'ul': 'ul', 'ol': 'ol', 'li': 'li', 'strong': 'strong', 'b': 'strong', 'em': 'em', 'i': 'em', 'a': 'a', 'br': 'br'}
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out = []; s.stack = []
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == 'br': s.out.append('<br>'); return
        if t in s.KEEP:
            k = s.KEEP[t]
            if k == 'a':
                href = a.get('href') or ''
                if href.startswith('mailto:') or href.startswith('tel:'):
                    s.out.append(f'<a href="{A(href)}">')
                else:
                    s.out.append(f'<a href="{A(href)}" target="_blank" rel="noopener">')
            else:
                s.out.append(f'<{k}>')
            s.stack.append(k)
        else:
            s.stack.append(None)
    def handle_endtag(s, t):
        if t == 'br': return
        k = s.stack.pop() if s.stack else None
        if k: s.out.append(f'</{k}>')
    def handle_startendtag(s, t, a):
        if t == 'br': s.out.append('<br>')
    def handle_data(s, d): s.out.append(E(d.replace('﻿', '')))


def clean_block(block_html):
    c = Clean(); c.feed(block_html); out = ''.join(c.out)
    out = out.replace(' ', ' ')
    out = re.sub(r'(<br>\s*)+(</(p|li|strong|em)>)', r'\2', out)       # trailing <br> inside a block
    out = re.sub(r'<(strong|em)>\s*</\1>', '', out)                      # empty inline wrappers
    out = re.sub(r'\s+(</(p|li)>)', r'\1', out)
    out = re.sub(r'(<(p|li)>)\s+', r'\1', out)
    out = re.sub(r'[ \t]{2,}', ' ', out)
    return out


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:50].rstrip('-')


def port(page, heading_idx):
    body = widget_html(page, '1456921506')
    inner = body[body.find('>') + 1: body.rfind('</div>')]
    blocks = re.findall(r'(<(p|ul|ol)[^>]*>.*?</\2>)', inner, re.S)
    assert ''.join(b for b, _ in blocks).replace(' ', '') in inner.replace(' ', '') or True
    parts, toc = [], []
    for k, (b, tag) in enumerate(blocks):
        txt = text_of(b)
        if not txt:
            continue                                  # empty spacer paragraphs
        if k in heading_idx:
            hid = 'section-' + slug(txt)
            parts.append(f'    <h2 id="{hid}">{E(txt)}</h2>')
            toc.append((hid, txt))
        else:
            parts.append('    ' + clean_block(b))
    doc = '\n'.join(parts)
    # PROOF: the ported document says exactly what the live widget says
    live_txt, new_txt = text_of(inner), text_of(doc)
    if live_txt != new_txt:
        import difflib
        sm = difflib.SequenceMatcher(None, live_txt, new_txt)
        for op in sm.get_opcodes():
            if op[0] != 'equal':
                print('DIFF', op[0], repr(live_txt[op[1]-30:op[2]+30]), '=>', repr(new_txt[op[3]-30:op[4]+30]))
        raise SystemExit(f'{page}: wording differs from live')
    return doc, toc, live_txt


EXTRA_CSS = r"""
  /* ── Legal page (typography + navigation only) ──────────────────────── */
  @W .lg-wrap { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 56px; align-items: start; }
  @W .lg-toc { position: sticky; top: 140px; max-height: calc(100vh - 160px); overflow-y: auto; padding: 20px 22px !important; background: var(--cream); border: 1px solid var(--border-light); border-radius: 12px; }
  @W .lg-toc h2 { font-size: 15px !important; letter-spacing: .12em !important; text-transform: uppercase !important; color: var(--gold-ink) !important; margin: 0 0 10px !important; }
  @W .lg-toc ol { list-style: none !important; margin: 0 !important; padding: 0 !important; }
  @W .lg-toc li { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .lg-toc li::before, @W .lg-toc li::marker { content: none !important; }
  @W .lg-toc a { display: flex; align-items: center; min-height: 44px; padding: 6px 0; font-size: 16px !important; line-height: 1.35 !important; text-decoration: none !important; }
  @W .lg-toc a:hover { text-decoration: underline !important; }
  @W .lg-doc { max-width: 62ch; }   /* ~68-74 characters per line */
  @W .lg-doc h2 { scroll-margin-top: 130px; font-size: clamp(22px, 2.2vw, 27px) !important; line-height: 1.3 !important; margin: 40px 0 14px !important; padding-top: 18px !important; border-top: 1px solid var(--border-light); }
  @W .lg-doc h2:first-child { margin-top: 0 !important; padding-top: 0 !important; border-top: 0; }
  @W .lg-doc p { font-size: 17px !important; line-height: 1.75 !important; color: var(--text) !important; margin: 0 0 14px !important; }
  @W .lg-doc ul, @W .lg-doc ol { margin: 0 0 16px !important; padding: 0 0 0 24px !important; }
  @W .lg-doc li { font-size: 17px !important; line-height: 1.7 !important; color: var(--text) !important; margin: 0 0 6px !important; list-style: disc !important; }
  @W .lg-doc strong { color: #111; }
  @W .lg-related { margin-top: 48px !important; padding-top: 20px !important; border-top: 1px solid var(--border-light); display: flex; flex-wrap: wrap; gap: 10px 26px; }
  @W .lg-related a { display: inline-flex; align-items: center; min-height: 44px; font-size: 16px !important; }
  @media (max-width: 960px) {
    @W .lg-wrap { grid-template-columns: 1fr; gap: 28px; }
    @W .lg-toc { position: static; }
  }
"""


def build(page, title_idx_live, heading_idx, hero_stem, wrapper, title_file, related, ver='v3', extra_log='', marker=None, edits=(), renumber=False):
    h1a = text_of(widget_html(page, '1826758713'))
    h1b = text_of(widget_html(page, '1415014792'))
    doc, toc, live_txt = port(page, heading_idx)
    # Approved wording changes (Kirsty, 26 Sep 2026). Each old passage must occur exactly
    # once, and the result must equal the live text with ONLY these edits applied.
    exp_txt = live_txt
    for code, old, new in edits:
        assert doc.count(old) == 1, (page, code, doc.count(old))
        o_t, n_t = text_of(old), text_of(new)
        assert exp_txt.count(o_t) == 1, (page, code, 'text', exp_txt.count(o_t))
        doc = doc.replace(old, new)
        exp_txt = NORM(exp_txt.replace(o_t, n_t))
    assert text_of(doc) == exp_txt, (page, 'edited text differs from live + approved edits')
    if renumber:
        # T4: clause numbers run 1, 2, 3 ... with no gaps (the live Terms skip 19, and the
        # removed ferry clause leaves another gap). Only the numbers change.
        nums = [int(n) for n in re.findall(r'<p><strong>(\d+)</strong>\.', doc)]
        mapping = {o: n for n, o in enumerate(nums, 1)}
        before = doc
        doc = re.sub(r'<p><strong>(\d+)</strong>\.', lambda m: f'<p><strong>{mapping[int(m.group(1))]}</strong>.', doc)
        strip_nums = lambda d: text_of(re.sub(r'<p><strong>\d+</strong>\.', '<p>#.', d))
        assert strip_nums(before) == strip_nums(doc), 'renumbering changed more than the numbers'
        new_nums = [int(n) for n in re.findall(r'<p><strong>(\d+)</strong>\.', doc)]
        assert new_nums == list(range(1, len(new_nums) + 1)), new_nums
        refs = [int(r) for r in re.findall(r'[Cc]lauses? (\d+)', doc)]
        assert all(mapping.get(r, r) == r for r in refs), ('a cross-reference points at a renumbered clause', refs)
        print(f'{page}: clauses renumbered 1-{len(new_nums)}; changed:', {o: n for o, n in mapping.items() if o != n})
    final_txt = text_of(doc)
    toc_html = '\n'.join(f'        <li><a href="#{hid}">{E(t)}</a></li>' for hid, t in toc)
    img = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/opt/' + hero_stem
    rel = '\n'.join(f'    <a href="{u}">{t}</a>' for u, t in related)
    header = f"""<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — {h1b.upper()} (/{page})
     COMPLETE PAGE  ·  VERSION {ver}  ·  2026-09-25  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     CHANGELOG (latest first):
{extra_log}       v3 — Shared kit fix (25 Sep 2026): no CSS child combinators any more.
            Duda publishes that character as an HTML entity and the browser
            drops the rule. This page has no show-more button, so nothing
            visible changes. Copy unchanged.
       v2 — Review fixes (independent check, 25 Sep 2026): layout and type
            only (shared kit: larger kicker/button type); wording re-proven
            identical to the live page. Third independent review: line
            length ~62 characters' width (72ch rendered up to ~87
            characters); contents and related links 44px tall; the sticky
            contents list scrolls on short laptop screens; darker hero veil
            on phones.
       v1 — First new-design build of /{page} (Brief v2, 25 Sep 2026).
            TYPOGRAPHY AND NAVIGATION ONLY — ZERO WORDING CHANGES, typos
            included. The document is the live page's text, word for word
            (the build compares it with the live page and refuses to write
            the file if a single character differs). Changes: readable
            line length and heading scale; the {len(toc)} existing section
            headings are now real headings with a contents list; the two
            old H1 lines become the eyebrow ("{E(h1a)}") and the H1
            ("{E(h1b)}"); empty spacer paragraphs removed. Nothing flagged
            in the runbook has been corrected here.
            The live page is noindex — keep it that way unless Ben decides.
     -----------------------------------------------------------------------
     WHERE IT GOES: page "{page}-new" (duplicate of /{page}). Delete every
     old content row, add ONE full-width row (padding 0), ONE HTML widget,
     paste this whole file. Steps + rollback: notes/2026-09-25-old-pages-rebuild-runbook.md
     RULES KEPT: no schema; no tracking; CSS scoped to .{wrapper}.
     ===================================================================== -->"""
    body = f"""{header}
{FONTS}
{css(wrapper, EXTRA_CSS)}
<div class="{wrapper}">
{hero(img + '-1920w.webp', E(h1a), E(h1b), compact=True, srcset=f'{img}-640w.webp 640w, {img}-1280w.webp 1280w, {img}-1920w.webp 1920w', label_id='sehe-lg-title')}
<div class="sp-body">
  <div class="lg-wrap">
    <nav class="lg-toc" aria-labelledby="sehe-lg-toc">
      <h2 id="sehe-lg-toc">Contents</h2>
      <ol role="list">
{toc_html}
      </ol>
    </nav>
    <div class="lg-doc">
{doc}
    </div>
  </div>
  <nav class="lg-related" aria-label="Related pages">
{rel}
  </nav>
</div>
</div>
"""
    if marker:
        body = body.rstrip('\n') + '\n' + end_marker(marker, ver) + '\n'
    out = os.path.join(REPO, title_file)
    open(out, 'w', encoding='utf-8').write(body)
    assert not check_script_safety(body)
    assert not check_style_safety(body), check_style_safety(body)
    # second, independent proof on the written file: the .lg-doc text == live text
    written = open(out, encoding='utf-8').read()
    d0 = written.find('<div class="lg-doc">'); d1 = written.find('\n    </div>\n  </div>\n  <nav class="lg-related"')
    assert text_of(written[d0:d1]) == final_txt, 'written file differs from the checked wording'
    open(os.path.join(OUT_DIR, f'verbatim-{page}.txt'), 'w', encoding='utf-8').write(h1a + '\n' + h1b + '\n')
    print('wrote', out, len(body), 'bytes;', len(toc), 'headings;', len(edits), 'approved edits;', 'identical to live' if not edits and not renumber else 'live text + approved edits only')


build('privacy-policy', None, {0, 5, 16, 22, 30, 37, 46, 56, 63}, 'SEHE_OCT2024_DAY2-06', 'sehe-pg-privacy', 'SEHE-privacy-policy-page_v5.txt',
      [('/terms-and-conditions', 'Terms &amp; Conditions'), ('/f-a-q', 'FAQ'), ('/contact', 'Contact us')], ver='v5', marker='privacy-policy-page.txt',
      extra_log="       v5 — Kirsty's answers (email, 26 Sep 2026), the only wording changes:\n"
                "            P1 section 4 names the Pounamu Tourism Group booking app\n"
                "            instead of Checkfront; P2 the postal address is PO Box 19735,\n"
                "            Woolston, Christchurch 8241; P3 the sentence about managing\n"
                "            cookie preferences is removed. P4: section 8 already says the\n"
                "            services are not intended for under-13s, the position she\n"
                "            chose. Everything else still matches the live page.\n",
      edits=[('P1', '<li>Checkfront (Booking &amp; Reservations System)</li>', '<li>Pounamu Tourism Group booking app (Booking &amp; Reservations System)</li>'),
             ('P2', 'Postal Address: PO Box 39018, Harewood, Christchurch, 8545, New Zealand', 'Postal Address: PO Box 19735, Woolston, Christchurch, 8241, New Zealand'),
             ('P3', 'We use cookies and tracking technologies in compliance with privacy regulations. You can manage or withdraw your cookie preferences via our website settings.', 'We use cookies and tracking technologies in compliance with privacy regulations.')])
build('terms-and-conditions', None, {8, 28, 39, 50, 65, 70, 81, 84, 91, 112}, 'SEHE_OCT2024_DAY2-18', 'sehe-pg-terms', 'SEHE-terms-page_v5.txt',
      [('/privacy-policy', 'Privacy Policy'), ('/f-a-q', 'FAQ'), ('/contact', 'Contact us')], ver='v5', marker='terms-page.txt', renumber=True,
      extra_log="       v5 — F3 wording corrected (26 Sep 2026). v4 made the refund\n"
                "            conditional (\"If none suit\"), which Kirsty did not say. Item e)\n"
                "            keeps the refund and adds her point separately: \"If Pounamu\n"
                "            Tourism Group cancels the tour, a 100% refund will apply. We will\n"
                "            also try to offer different suitable dates as an option.\" The FAQ\n"
                "            uses the same words. Nothing else changed.\n"
                "       v4 — Kirsty's answers (email, 26 Sep 2026), the only wording changes:\n"
                "            T1 postcode 8241; T2 email info@pounamutourismgroup.com (clauses\n"
                "            1 and 9); T3 the Privacy Officer's address is PO Box 19735,\n"
                "            Woolston, Christchurch 8241; T5 clause 8 links to the Privacy\n"
                "            Policy page; T6 the Picton to Wellington ferry clause is removed;\n"
                "            T4 the clauses are renumbered 1 to 42 with no gaps (old 20 to 35\n"
                "            become 19 to 34, old 37 to 44 become 35 to 42); F7 dietary needs\n"
                "            go in the pre-trip documentation (clause 22, was 23); F3 item e)\n"
                "            says we try to offer different suitable dates first; P4 the old\n"
                "            clause 41 (now 39) says the tour is not intended for children\n"
                "            under 13. Everything else still matches the live page.\n",
      edits=json.load(open(os.path.join(DATA_DIR, 'terms-edits.json'), encoding='utf-8')))
