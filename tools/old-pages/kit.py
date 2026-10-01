"""Shared kit for the old-page rebuilds (Reviews, Contact, About, FAQ, Gallery,
Himalayan Trust, Privacy, Terms). Each page is scoped under its own wrapper
class `.sehe-pg-<name>`; inner classes use the `sp-` vocabulary so every page
looks like one family with the Journeys/Brochure pages."""
import html, re, os

# Repo-relative locations (this folder is tools/old-pages/). Live inputs come
# from the redacted backups in the repo; builder outputs other than the masters
# (verbatim checklists, the Contact preview copy) go to out/, which git ignores.
KIT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(KIT_DIR, '..', '..'))
DATA_DIR = os.path.join(KIT_DIR, 'data')
OUT_DIR = os.path.join(KIT_DIR, 'out')
os.makedirs(OUT_DIR, exist_ok=True)


def live_path(name):
    """The served HTML a builder ports from: the eight old pages as of 25 Sep 2026,
    and (for About's fact checks) the homepage and Journeys as of 6 Sep 2026."""
    if name in ('home.html', 'journeys.html'):
        return os.path.join(REPO_ROOT, 'backups', '2026-09-06-live-site', 'pages', name)
    return os.path.join(REPO_ROOT, 'backups', '2026-09-25-old-pages', name)

E = lambda s: html.escape(s, quote=False)
A = lambda s: html.escape(s, quote=True)

TP_PROFILE = 'https://nz.trustpilot.com/review/siredmundhillaryexplorer.com'
TP_WRITE = 'https://nz.trustpilot.com/evaluate/siredmundhillaryexplorer.com'
TP_BU = '67af6f95db89fc000f855205'
TP_MICRO_COMBO = '5419b6ffb0d04a076446a9af'
TP_STARS_IMG = 'https://irp.cdn-website.com/35e9f777/dms3rep/multi/Trustpilot_ratings_5star-RGB.png'
LOGO = 'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/SEH+Explorer_logo+white-350w.png'
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700'
         '&amp;family=Open+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">')
PHONE_TEL = 'tel:+6439741812'
PHONE_TXT = '+64 3 974 1812'

NEWTAB = '<span class="sp-sr"> (opens in a new tab)</span>'

KIT_CSS = r"""
  /* ── Duda host row ─────────────────────────────────────────────────────
     Let the hero run full-bleed and stop the row adding a white strip under
     the transparent site header. :has() rules sit on their own so a browser
     without :has() drops only these lines (the runbook also sets the row's
     padding to 0 in the editor, which covers those browsers). */
  #dm .dmContent .dmRespRow:has(@HOST) { padding-top: 0 !important; padding-bottom: 0 !important; overflow: visible !important; max-width: none !important; }
  #dm .dmContent .dmRespRow:has(@HOST) .dmRespColsWrapper { overflow: visible !important; max-width: none !important; }
  #dm .dmContent .dmRespRow:has(@HOST) .dmRespCol { overflow: visible !important; max-width: none !important; padding-left: 0 !important; padding-right: 0 !important; }
  #dm .dmContent .dmCustomHtml:has(@HOST) { overflow: visible !important; }

  /* ── Page scope + tokens (Journeys v22 palette) ─────────────────────── */
  @W, @W *, @W *::before, @W *::after { box-sizing: border-box; }
  @W {
    --navy: #153b67; --navy-dark: #0e2d52; --gold: #c8a56c; --gold-light: #d4b37e;
    --gold-ink: #7a5f30; /* gold for small text on light backgrounds (5.9:1 on white) */
    --off-white: #f9f7f3; --cream: #faf8f3; --text: #1a1a1a; --text-2: #454545;
    --border: #d8d3c8; --border-light: #e8e4db; --white: #ffffff;
    display: block; width: 100%; margin: 0 !important; padding: 0 !important;
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    font-size: 17px; line-height: 1.65; color: var(--text); text-align: left !important;
    -webkit-text-size-adjust: 100%; text-size-adjust: 100%; overflow-wrap: break-word;
  }
  /* theme rule ".dmFullRowRespTmpl section{padding:50px 40px}" would re-pad every section */
  @W section, @W aside, @W nav { padding: 0 !important; margin: 0; }
  @W h1, @W h2, @W h3, @W h4 {
    font-family: 'Montserrat', -apple-system, 'Segoe UI', Arial, sans-serif !important; font-weight: 600 !important;
    color: var(--navy) !important; text-transform: none !important; text-align: left !important;
    letter-spacing: -0.01em !important; margin: 0 !important; padding: 0 !important;
  }
  @W p, @W li, @W dt, @W dd, @W figcaption, @W blockquote, @W summary, @W td, @W th {
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif !important;
    text-align: left !important; text-transform: none !important;
  }
  @W p { font-size: 17px !important; line-height: 1.7 !important; color: var(--text-2) !important; margin: 0 !important; }
  @W a { color: var(--navy) !important; text-decoration: underline !important; text-underline-offset: 3px; text-decoration-thickness: 1px; }
  @W a:hover { color: var(--navy-dark) !important; text-decoration-thickness: 2px; }
  @W a:focus-visible, @W summary:focus-visible, @W button:focus-visible { outline: 3px solid var(--navy) !important; outline-offset: 3px !important; border-radius: 4px; }
  @W img { max-width: 100%; height: auto; border: 0; }
  @W .sp-sr { position: absolute !important; width: 1px !important; height: 1px !important; margin: -1px !important; padding: 0 !important; overflow: hidden !important; clip: rect(0 0 0 0) !important; white-space: nowrap !important; border: 0 !important; }

  /* ── Hero (same build as the Journeys / Brochure heroes) ────────────── */
  @W .sp-hero {
    position: relative; width: 100vw; margin-left: calc(50% - 50vw) !important; margin-right: calc(50% - 50vw) !important;
    padding: 0 !important; min-height: max(540px, 68vh); min-height: max(540px, 68svh);
    display: flex; align-items: flex-end; background-color: #081525; overflow: hidden;
  }
  @W .sp-hero--compact { min-height: max(380px, 46vh); min-height: max(380px, 46svh); }
  @W .sp-hero-img { position: absolute; top: 0; left: 0; width: 100% !important; height: 100% !important; max-width: none !important; object-fit: cover; object-position: center 50%; display: block; }
  @W .sp-hero-veil { position: absolute; top: 0; right: 0; bottom: 0; left: 0; background: linear-gradient(180deg, rgba(8,21,37,.62) 0%, rgba(8,21,37,.26) 28%, rgba(8,21,37,.58) 56%, rgba(8,21,37,.95) 100%); }
  @W .sp-hero--compact .sp-hero-veil { background: linear-gradient(180deg, rgba(8,21,37,.70) 0%, rgba(8,21,37,.52) 40%, rgba(8,21,37,.92) 100%); }
  /* the site header's logo slot is a transparent placeholder until you scroll —
     put the real roundel in its lane so the brand is there on load */
  @W .sp-hero-logo { position: absolute; top: 26px; left: 0; width: 16.66% !important; height: 92px !important; max-width: none !important; object-fit: contain; object-position: center; z-index: 2; filter: drop-shadow(0 2px 10px rgba(8,21,37,.5)); }
  @W .sp-hero-inner { position: relative; z-index: 1; width: 100%; max-width: 1240px; margin: 0 auto; padding: 150px 30px 58px; }
  @W .sp-hero--compact .sp-hero-inner { padding: 140px 30px 46px; }
  @W .sp-eyebrow {
    display: inline-flex; align-items: center; gap: 16px; font-family: 'Montserrat', sans-serif !important;
    font-size: 13.5px !important; font-weight: 700 !important; letter-spacing: .42em !important; text-transform: uppercase !important;
    color: #d4b37e !important; margin: 0 0 22px !important; text-shadow: 0 1px 12px rgba(8,21,37,.95);
  }
  @W .sp-eyebrow::before, @W .sp-eyebrow::after { content: ''; width: 44px; height: 1px; background: #d4b37e; flex: none; }
  @W .sp-hero h1 { font-weight: 700 !important; font-size: clamp(40px, 5.2vw, 66px) !important; line-height: 1.08 !important; color: #ffffff !important; text-shadow: 0 2px 26px rgba(8,21,37,.55); }
  @W .sp-hero--compact h1 { font-size: clamp(36px, 4.2vw, 54px) !important; }
  @W .sp-hero-sub { margin: 22px 0 0 !important; max-width: 620px; font-size: clamp(17px, 1.5vw, 19px) !important; line-height: 1.65 !important; color: rgba(255,255,255,.95) !important; text-shadow: 0 1px 14px rgba(8,21,37,.6); }
  @W .sp-hero a:focus-visible, @W .sp-band a:focus-visible { outline-color: var(--gold-light) !important; }

  /* ── Body, section heads ────────────────────────────────────────────── */
  @W .sp-body { max-width: 1240px; margin: 0 auto !important; padding: 64px 30px 76px !important; }
  @W .sp-section + .sp-section, @W .sp-section + .sp-band, @W .sp-band + .sp-section { margin-top: 76px !important; }
  @W .sp-head { max-width: 780px; margin: 0 0 28px !important; }
  @W .sp-kicker { display: block; font-family: 'Montserrat', sans-serif !important; font-size: 14px !important; font-weight: 700 !important; letter-spacing: .14em !important; text-transform: uppercase !important; color: var(--gold-ink) !important; margin: 0 0 10px !important; }
  @W .sp-head h2 { font-size: clamp(28px, 3vw, 36px) !important; line-height: 1.2 !important; margin: 0 0 12px !important; }
  @W .sp-head p { max-width: 60ch; }   /* ~66-72 characters per line in Open Sans */
  @W .sp-head p + p { margin-top: 10px !important; }

  /* ── Buttons (48px+ tap targets) ────────────────────────────────────── */
  @W .sp-actions { display: flex; flex-wrap: wrap; gap: 12px; }
  @W .sp-btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 50px; padding: 12px 24px;
    border-radius: 6px; border: 2px solid var(--navy); background: var(--navy); color: #ffffff !important;
    font-family: 'Montserrat', sans-serif !important; font-size: 16px !important; font-weight: 600 !important; line-height: 1.25 !important;
    text-decoration: none !important; text-align: center !important; cursor: pointer; transition: background-color .2s, color .2s, border-color .2s;
  }
  @W .sp-btn:hover { background: var(--navy-dark); border-color: var(--navy-dark); color: #ffffff !important; }
  @W .sp-btn--ghost { background: transparent; color: var(--navy) !important; }
  @W .sp-btn--ghost:hover { background: var(--navy); color: #ffffff !important; }
  @W .sp-btn--gold { background: var(--gold); border-color: var(--gold); color: var(--navy-dark) !important; }
  @W .sp-btn--gold:hover { background: var(--gold-light); border-color: var(--gold-light); color: var(--navy-dark) !important; }
  @W .sp-btn--light { background: transparent; border-color: rgba(255,255,255,.85); color: #ffffff !important; }
  @W .sp-btn--light:hover { background: #ffffff; border-color: #ffffff; color: var(--navy-dark) !important; }

  /* ── Disclosure ("show more") — native details element, works with JS off.
     Plain descendant selectors only: Duda's publisher rewrites the child
     combinator as an HTML entity, and the browser then drops the whole rule. ── */
  @W details.sp-more summary {
    list-style: none; display: inline-flex; align-items: center; gap: 12px; min-height: 50px; padding: 12px 22px;
    border: 2px solid var(--navy); border-radius: 6px; background: #ffffff; color: var(--navy) !important;
    font-family: 'Montserrat', sans-serif !important; font-size: 16px !important; font-weight: 600 !important; cursor: pointer;
  }
  @W details.sp-more summary::-webkit-details-marker { display: none; }
  @W details.sp-more summary::after { content: '+'; font-size: 22px; line-height: 1; font-weight: 400; }
  @W details.sp-more[open] summary::after { content: '\2212'; }
  @W details.sp-more summary:hover { background: var(--navy); color: #ffffff !important; }
  @W .sp-when-open { display: none; }
  @W details[open] summary .sp-when-open { display: inline; }
  @W details[open] summary .sp-when-closed { display: none; }

  /* ── Navy help band (the Journeys contact card, scoped) ─────────────── */
  @W .sp-band { background: var(--navy); border: 1px solid var(--gold); border-radius: 12px; padding: 34px 36px !important; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 22px 36px; }
  @W .sp-band-copy { flex: 1 1 420px; }
  @W .sp-band h2 { color: #ffffff !important; font-size: clamp(24px, 2.4vw, 28px) !important; line-height: 1.25 !important; margin: 0 0 8px !important; }
  @W .sp-band p { color: rgba(255,255,255,.88) !important; max-width: 62ch; }
  @W .sp-band .sp-actions { flex: 1 1 440px; justify-content: flex-end; }

  @media (max-width: 860px) {
    @W .sp-hero { min-height: max(460px, 60svh); }
    @W .sp-hero--compact { min-height: max(340px, 42svh); }
    /* phones crop to the brightest part of the frame — darker veil keeps contrast */
    @W .sp-hero-veil, @W .sp-hero--compact .sp-hero-veil { background: linear-gradient(180deg, rgba(8,21,37,.66) 0%, rgba(8,21,37,.48) 30%, rgba(8,21,37,.72) 58%, rgba(8,21,37,.96) 100%); }
    @W .sp-hero-inner, @W .sp-hero--compact .sp-hero-inner { padding: 118px 20px 40px; }
    @W .sp-hero-logo { left: 50%; width: 56px !important; transform: translateX(-50%); top: 18px; height: 56px !important; }
    @W .sp-eyebrow { gap: 0; font-size: 12.5px !important; letter-spacing: .2em !important; margin-bottom: 14px !important; }
    @W .sp-eyebrow::before, @W .sp-eyebrow::after { display: none; }
    @W .sp-hero h1, @W .sp-hero--compact h1 { font-size: 34px !important; line-height: 1.14 !important; }
    @W .sp-hero-sub { font-size: 17px !important; line-height: 1.6 !important; margin-top: 14px !important; }
    @W .sp-body { padding: 44px 18px 56px !important; }
    @W .sp-section + .sp-section, @W .sp-section + .sp-band, @W .sp-band + .sp-section { margin-top: 56px !important; }
    @W .sp-band { padding: 24px 20px !important; }
    @W .sp-band .sp-actions { justify-content: flex-start; }
    @W .sp-actions .sp-btn { flex: 1 1 100%; }
  }
  @media (max-width: 540px) {
    @W .sp-hero h1, @W .sp-hero--compact h1 { font-size: 30px !important; }
    @W .sp-hero-inner, @W .sp-hero--compact .sp-hero-inner { padding: 106px 18px 34px; }
  }
  @media (prefers-reduced-motion: reduce) {
    @W *, @W *::before, @W *::after { transition: none !important; scroll-behavior: auto !important; }
  }
"""


def css(wrapper, extra='', host=None):
    host = host or ('.' + wrapper)
    return '<style>' + (KIT_CSS + extra).replace('@HOST', host).replace('@W', '.' + wrapper) + '</style>'


def hero(img, eyebrow, h1, sub='', extra='', compact=False, srcset='', img_alt='', label_id='sp-page-title', pos='center 50%',
         mobile_srcset='', mobile_pos='center 50%', extra_cls=''):
    cls = ('sp-hero sp-hero--compact' if compact else 'sp-hero') + (' ' + extra_cls if extra_cls else '')
    ss = f' srcset="{srcset}" sizes="100vw"' if srcset else ''
    style = f' style="object-position:{pos}"' if pos != 'center 50%' else ''
    imgtag = f'<img class="sp-hero-img" src="{img}"{ss} alt="{A(img_alt)}"{style} fetchpriority="high">'
    if mobile_srcset:
        # art direction: phones get their own (taller) photograph
        imgtag = f'<picture><source media="(max-width: 860px)" srcset="{mobile_srcset}" sizes="100vw">{imgtag}</picture>'
    out = [f'<section class="{cls}" aria-labelledby="{label_id}">',
           f'  {imgtag}',
           '  <div class="sp-hero-veil" aria-hidden="true"></div>',
           f'  <img class="sp-hero-logo" src="{LOGO}" alt="Sir Edmund Hillary Explorer" width="350" height="350">',
           '  <div class="sp-hero-inner">',
           f'    <p class="sp-eyebrow">{eyebrow}</p>',
           f'    <h1 id="{label_id}">{h1}</h1>']
    if sub:
        out.append(f'    <p class="sp-hero-sub">{sub}</p>')
    if extra:
        out.append(extra)
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def band(heading, text, buttons):
    """buttons: list of (label, href, style, newtab)"""
    b = []
    for label, href, style, newtab in buttons:
        t = ' target="_blank" rel="noopener"' if newtab else ''
        b.append(f'      <a class="sp-btn sp-btn--{style}" href="{href}"{t}>{label}{NEWTAB if newtab else ""}</a>')
    return '\n'.join([
        '  <aside class="sp-band" aria-label="' + A(html.unescape(re.sub('<[^>]+>', '', heading))) + '">',
        '    <div class="sp-band-copy">',
        f'      <h2>{heading}</h2>',
        f'      <p>{text}</p>',
        '    </div>',
        '    <div class="sp-actions">',
        *b,
        '    </div>',
        '  </aside>'])


def trustbox_loader(el_id):
    # Guarded: the Trustpilot bootstrap is loaded once site-wide from Head HTML.
    # Never adds another bootstrap. No '<' and no '&' anywhere in this script
    # (Duda's publisher escapes both inside inline scripts).
    return f"""<script>
(function () {{
  var box = document.getElementById('{el_id}');
  if (!box) return;
  var tries = 0;
  function ready() {{
    if (box.querySelector('iframe')) return true;
    if (window.Trustpilot) {{
      if (typeof window.Trustpilot.loadFromElement === 'function') {{ window.Trustpilot.loadFromElement(box, true); return true; }}
    }}
    return false;
  }}
  var timer = setInterval(function () {{
    tries = tries + 1;
    if (ready()) {{ clearInterval(timer); return; }}
    if (tries === 40) clearInterval(timer);
  }}, 500);
}})();
</script>"""


def check_script_safety(txt):
    """README rule 3 + the 20 Sep finding: no '<' and no '&' inside inline scripts."""
    bad = []
    for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', txt, re.S):
        body = m.group(1)
        if '<' in body or '&' in body:
            bad.append(body[:120])
    return bad


def check_style_safety(txt):
    """25 Sep finding (live /reviews-new): Duda's publisher rewrites '>' inside
    <style> as '&gt;', so any rule using the child combinator (or :has(> ...))
    is silently dropped on the published page. No '>' and no '<' in any style
    block, comments included."""
    bad = []
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', txt, re.S):
        for i, line in enumerate(m.group(1).splitlines()):
            if '>' in line or '<' in line:
                bad.append(line.strip()[:120])
    return bad


def dudafy(txt):
    """What Duda actually publishes for a widget: '>' inside <style> becomes
    '&gt;'. Visual tests run on this, not on the raw paste."""
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + m.group(2).replace('>', '&gt;') + m.group(3), txt, flags=re.S)


def end_marker(paste_name, version):
    """25 Sep 2026: two Contact pastes were cut off at line 150 (copied from a
    preview that shows only the first 150 lines), so the page never reached
    Duda. This line is the very last line of the file: if it is the last line
    in Duda's code box, the whole file went in."""
    return f'<!-- END OF FILE: {paste_name} {version}. If this is the last line in the Duda code box, the whole file is pasted. -->'
