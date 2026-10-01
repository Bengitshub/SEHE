import re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

HERE = os.path.dirname(__file__)
LIVE = open(live_path('contact.html'), encoding='utf-8').read()
REPO = REPO_ROOT

# facts that must already be on the live page (no new facts)
for fact in ['PO Box 19735, Woolston, Christchurch, 8241', 'info@pounamutourismgroup.com', 'tel:00116439741812',
             'tel:0116439741812', 'https://facebook.com/SirEdmundHillaryExplorer', 'http://instagram.com/SirEdmundHillaryExplorer',
             'https://www.pounamutourismgroup.com', 'Send us an enquiry', 'Thank you for contacting us.']:
    assert fact in LIVE, fact

WTA = 'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/new-zealands-leading-tour-operator-2025-winner-shield-256-816b3264-1920w.png'
HERO = 'https://lirp.cdn-website.com/35e9f777/dms3rep/multi/opt/L161-Milford-Sound-Fiordland-Rob-Suisted'
assert open(os.path.join(REPO, 'SEHE-14day-tour_v28.txt'), encoding='utf-8').read().count(HERO + '-1920w.jpg')

W = 'sehe-pg-contact'
FORM = '#dm .dmContent .sehe-pg-contact .ct-formslot .dmform'

EXTRA_CSS = r"""
  /* ── Contact page ───────────────────────────────────────────────────── */
  @W .sp-hero--compact { min-height: max(340px, 40vh); min-height: max(340px, 40svh); }
  @W .sp-hero--compact .sp-hero-inner { padding: 136px 30px 42px; }
  @W .sp-hero-sub { max-width: 640px; }

  /* details (left) + the docked native form (right). Until the form is docked
     (or if it never is) the details take the full width and the form stays in
     its own Duda row below this widget. */
  @W .ct-body { padding-top: 56px !important; padding-bottom: 56px !important; }
  @W .ct-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 40px; align-items: start; }
  @W.ct-docked .ct-grid { grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 64px; }
  @W .ct-formside[hidden] { display: none !important; }
  @W .ct-quick-sec { margin-top: 56px !important; }
  @W .ct-details { display: block; }
  @W .ct-head h3 { font-family: 'Montserrat', -apple-system, 'Segoe UI', Arial, sans-serif !important; font-weight: 600 !important; font-size: clamp(26px, 2.6vw, 32px) !important; line-height: 1.2 !important; color: #153b67 !important; text-transform: none !important; text-align: left !important; letter-spacing: -0.01em !important; margin: 0 0 20px !important; }
  #FORM .dmform-title { font-family: 'Montserrat', -apple-system, 'Segoe UI', Arial, sans-serif !important; font-weight: 600 !important; font-size: clamp(26px, 2.6vw, 32px) !important; line-height: 1.2 !important; color: #153b67 !important; text-transform: none !important; text-align: left !important; letter-spacing: -0.01em !important; margin: 0 0 20px !important; }
  @W .ct-list { list-style: none !important; margin: 0 !important; padding: 0 !important; }
  @W .ct-item { list-style: none !important; margin: 0 !important; padding: 14px 0 !important; border-bottom: 1px solid var(--border-light); }
  @W .ct-item::before, @W .ct-item::marker { content: none !important; }
  @W .ct-item:first-child { padding-top: 0 !important; }
  @W .ct-item:last-child { border-bottom: 0 !important; padding-bottom: 0 !important; }
  @W .ct-item .ct-label { font-family: 'Montserrat', sans-serif !important; font-size: 14px !important; font-weight: 700 !important; letter-spacing: .04em; line-height: 1.4 !important; color: var(--gold-ink) !important; margin: 0 0 2px !important; }
  @W .ct-item .ct-value { margin: 0 !important; font-size: 18px !important; line-height: 1.5 !important; color: var(--text) !important; }
  @W .ct-item .ct-value a { display: inline-block; padding: 6px 0; min-height: 44px; font-weight: 600; }
  @W .ct-item--main .ct-value a { font-family: 'Montserrat', sans-serif !important; font-size: 26px !important; font-weight: 700 !important; text-decoration: none !important; color: var(--navy) !important; }
  @W .ct-item--main .ct-value a:hover { text-decoration: underline !important; }
  @W .ct-item--email .ct-value a { word-break: break-all; }
  @W .ct-item .ct-note { font-size: 15.5px !important; color: var(--text-2) !important; margin-top: 2px !important; }
  @W .ct-chat { margin: 22px 0 0; }
  @W .ct-chat[hidden] { display: none !important; }
  @W button.sp-btn { -webkit-appearance: none; appearance: none; }
  @W .ct-trust { display: flex; align-items: center; gap: 16px; margin: 26px 0 0; padding: 18px 0 0; border-top: 1px solid var(--border-light); }
  @W .ct-trust img { width: 72px !important; height: auto !important; flex: none; }
  @W .ct-trust-copy { display: flex; flex-direction: column; gap: 8px; min-width: 0; flex: 1 1 auto; }
  @W .ct-trust-copy p { font-size: 15.5px !important; line-height: 1.5 !important; }
  @W .ct-trustbox { width: 100%; max-width: 420px; min-height: 24px; }

  /* ── The native Duda form, once docked into .ct-formslot — LOOK ONLY ───
     The form stays a real Duda form: recipient, subject, Zapier webhook,
     field IDs (dmform-0/1/3), its field labels (they are the keys the email
     and the Zapier webhook receive), reCAPTCHA and the success message are
     not touched. Visible field names are CSS text beside the untouched
     labels, matched by field TYPE (Duda renames the fields while it sends,
     so a name match would vanish after a failed send). Descendant selectors
     only (see the kit note); reCAPTCHA's own hidden textarea is excluded by
     its class so it stays hidden. */
  #FORM { font-family: 'Open Sans', -apple-system, 'Segoe UI', Arial, sans-serif !important; max-width: none !important; padding: 0 !important; margin: 0 !important; }
  #FORM, #FORM * { box-sizing: border-box !important; }
  #FORM .dmform-title { display: block !important; visibility: visible !important; }
  #FORM .dmform-wrapper, #FORM form { margin: 0 !important; padding: 0 !important; }
  #FORM .dmforminput { float: none !important; width: 100% !important; margin: 0 0 18px !important; padding: 0 !important; }
  #FORM .dmforminput::before { display: block; margin: 0 0 6px; font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 15.5px; line-height: 1.3; color: #1a1a1a; }
  #FORM .dmforminput:has(input[type="text"])::before { content: 'Your name'; }
  #FORM .dmforminput:has(input[type="email"])::before { content: 'Your email address'; }
  #FORM .dmforminput:has(textarea:not(.g-recaptcha-response))::before { content: 'Your message'; }
  #FORM .dmforminput input[type="text"], #FORM .dmforminput input[type="email"], #FORM .dmforminput textarea:not(.g-recaptcha-response) {
    width: 100% !important; display: block !important; margin: 0 !important; padding: 13px 16px !important;
    background: #ffffff !important; color: #1a1a1a !important; border: 1px solid #8a8378 !important; border-radius: 6px !important;
    font-family: 'Open Sans', -apple-system, 'Segoe UI', Arial, sans-serif !important; font-size: 17px !important; line-height: 1.45 !important;
    height: auto !important; min-height: 52px !important; box-shadow: none !important; -webkit-appearance: none !important; appearance: none !important;
  }
  #FORM .dmforminput textarea:not(.g-recaptcha-response) { min-height: 170px !important; resize: vertical !important; }
  #FORM .dmforminput input::placeholder, #FORM .dmforminput textarea::placeholder { color: #6b655c !important; opacity: 1 !important; }
  #FORM .dmforminput input[type="text"]:focus, #FORM .dmforminput input[type="email"]:focus, #FORM .dmforminput textarea:not(.g-recaptcha-response):focus { outline: 3px solid #153b67 !important; outline-offset: 1px !important; border-color: #153b67 !important; }
  #FORM .dmformsubmit { float: none !important; display: block !important; width: 100% !important; max-width: none !important; height: auto !important; min-height: 0 !important; margin: 8px 0 0 !important; padding: 0 !important; border: 0 !important; border-radius: 0 !important; background: none !important; box-shadow: none !important; text-align: left !important; line-height: normal !important; }
  #FORM .dmformsubmit::before, #FORM .dmformsubmit::after { display: none !important; }
  #FORM .dmformsubmit input[type="submit"] {
    width: 100% !important; display: block !important; height: auto !important; min-height: 54px !important; padding: 16px 24px !important; margin: 0 !important;
    background: #153b67 !important; border: 2px solid #153b67 !important; border-radius: 6px !important; color: #ffffff !important; cursor: pointer !important;
    font-family: 'Montserrat', sans-serif !important; font-size: 16px !important; font-weight: 600 !important; letter-spacing: .02em !important; text-transform: none !important; line-height: 1.2 !important;
    -webkit-appearance: none !important; appearance: none !important;
  }
  #FORM .dmformsubmit input[type="submit"]:hover { background: #0e2d52 !important; border-color: #0e2d52 !important; }
  #FORM .dmformsubmit input[type="submit"]:focus-visible { outline: 3px solid #153b67 !important; outline-offset: 3px !important; }
  /* success / error messages: shown by Duda's own script; GTM's 'Contact Us
     Form Submitted' needs .dmform-success fully on screen, so keep it compact */
  #FORM .dmform-success, #FORM .dmform-error { margin: 0 !important; padding: 18px 20px !important; border-radius: 8px !important; font-family: 'Open Sans', sans-serif !important; font-size: 17px !important; line-height: 1.6 !important; color: #1a1a1a !important; text-align: left !important; background: #faf8f3 !important; border: 1px solid #e8e4db !important; border-left: 4px solid #c8a56c !important; }
  #FORM .dmform-error { border-left-color: #b84040 !important; }

  /* quick links */
  @W .ct-quick { list-style: none !important; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 16px; }
  @W .ct-quick li { margin: 0 !important; padding: 0 !important; list-style: none !important; }
  @W .ct-quick li::before, @W .ct-quick li::marker { content: none !important; }
  @W .ct-quick a { display: flex; flex-direction: column; gap: 4px; height: 100%; min-height: 96px; padding: 18px 20px; border: 1px solid var(--border); border-radius: 10px; background: #ffffff; text-decoration: none !important; transition: border-color .2s, box-shadow .2s; }
  @W .ct-quick a:hover { border-color: var(--navy); box-shadow: 0 2px 10px rgba(21,59,103,.08); }
  @W .ct-quick strong { font-family: 'Montserrat', sans-serif !important; font-size: 17px; font-weight: 600; color: var(--navy); }
  @W .ct-quick span { font-size: 15.5px; line-height: 1.5; color: var(--text-2); }

  @media (max-width: 860px) {
    @W.ct-docked .ct-grid { grid-template-columns: minmax(0, 1fr); gap: 44px; }
    @W .ct-body { padding-top: 36px !important; padding-bottom: 40px !important; }
    @W .sp-hero--compact .sp-hero-inner { padding: 112px 20px 34px; }
    @W .ct-item--main .ct-value a { font-size: 24px !important; }
    @W .ct-chat .sp-btn { width: 100%; }
    @W .ct-quick-sec { margin-top: 44px !important; }
  }
""".replace('#FORM', FORM)

TRUSTBOX = f"""        <div id="sehe-ct-trustbox" class="trustpilot-widget ct-trustbox" data-locale="en-NZ" data-template-id="{TP_MICRO_COMBO}" data-businessunit-id="{TP_BU}" data-style-height="20px" data-style-width="100%">
          <a href="{TP_PROFILE}" target="_blank" rel="noopener">Read our reviews on Trustpilot{NEWTAB}</a>
        </div>"""

ENHANCE = r"""<script>
(function () {
  /* Contact page enhancement — add only, never remove.
     "Start a chat" appears only once tawk.to (already on every page) is ready.
     The native form is not touched by any script.
     No less-than sign and no ampersand in this script (Duda's publisher escapes both). */
  var tries = 0;
  function chat() {
    var box = document.querySelector('.sehe-pg-contact [data-sehe-chat]');
    if (!box) return true;
    if (window.Tawk_API) {
      if (typeof window.Tawk_API.maximize === 'function') {
        box.hidden = false;
        var btn = box.querySelector('button');
        if (btn) {
          if (!btn.getAttribute('data-bound')) {
            btn.setAttribute('data-bound', '1');
            btn.addEventListener('click', function () { window.Tawk_API.maximize(); });
          }
        }
        return true;
      }
    }
    return false;
  }
  var timer = setInterval(function () {
    tries = tries + 1;
    if (chat()) { clearInterval(timer); return; }
    if (tries === 60) clearInterval(timer);
  }, 500);
})();
</script>"""


DOCK = r"""<script>
(function () {
  /* Contact form DOCKING, the same method the live tour pages use for their
     brochure forms. The real Duda form sits in its own row directly BELOW
     this widget, so its recipient, subject, webhook, reCAPTCHA and success
     message are all Duda's own. On the published site this script moves
     that form into the right-hand column as soon as the page contains it,
     before Duda draws the reCAPTCHA checkbox. If a checkbox is already
     drawn, or anything is missing, nothing moves and the form simply stays
     below. In the Duda editor nothing moves. The script never changes the
     form itself. No less-than sign and no ampersand in this script. */
  if (!/(^|\.)siredmundhillaryexplorer\.com$/.test(window.location.hostname)) return;
  var root = document.querySelector('.sehe-pg-contact');
  var slot = root ? root.querySelector('[data-sehe-contact-slot]') : null;
  if (!slot) return;
  var side = slot.parentElement;
  var done = false, tries = 0, timer = null;
  function findForm() {
    var all = document.querySelectorAll('div[data-element-type="dContactUsRespId"]');
    for (var i = 0; i !== all.length; i += 1) {
      if (all[i].querySelector('input[type="email"]')) return all[i];
    }
    return null;
  }
  function hideIfEmpty(row) {
    if (!row.querySelector('[data-element-type]')) row.style.setProperty('display', 'none', 'important');
  }
  function tick() {
    if (done) return;
    var w = findForm();
    if (!w) return;
    done = true;
    window.clearInterval(timer);
    if (w.querySelector('iframe')) return;   /* reCAPTCHA already drawn: leave the form where it is */
    var row = w.closest('.dmRespRow');
    slot.appendChild(w);
    side.hidden = false;
    root.classList.add('ct-docked');
    if (row) {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { hideIfEmpty(row); });
      } else {
        hideIfEmpty(row);
      }
    }
  }
  timer = window.setInterval(function () {
    tries += 1;
    tick();
    if (tries === 300) window.clearInterval(timer);
  }, 50);
  document.addEventListener('DOMContentLoaded', tick);
  tick();
})();
</script>"""


# No direct link to /brochure-collection: every brochure form redirects there, and a visit
# counts as a brochure conversion. Brochures are requested from each tour page's form,
# which the Journeys cards link to.
QUICK = [
    ('/f-a-q', 'Frequently asked questions', 'Booking, payments and what to expect on tour'),
    ('/journeys', 'Journeys and brochures', 'Compare our tours, then request a brochure from any tour page'),
    ('/reviews', 'Guest reviews', 'Read what our guests say about their journey'),
]
quick_html = '\n'.join(f'      <li><a href="{u}"><strong>{t}</strong><span>{d}</span></a></li>' for u, t, d in QUICK)

PAGE = f"""{FONTS}
{css(W, EXTRA_CSS)}
<div class="sehe-pg-contact">
{hero(HERO + '-1920w.jpg', 'Contact us', 'Let&#39;s plan your New Zealand journey.',
      'Ask us about choosing a tour, travelling solo, room options or an existing booking. Our New Zealand team is here to help.',
      compact=True, srcset=f'{HERO}-640w.jpg 640w, {HERO}-1280w.jpg 1280w, {HERO}-1920w.jpg 1920w', label_id='sehe-ct-title', pos='center 62%')}
<div class="sp-body ct-body">
  <h2 class="sp-sr">Ways to get in touch</h2>
  <div class="ct-grid">
    <div class="ct-details">
      <div class="ct-head">
        <h3>Contact details</h3>
      </div>
      <ul class="ct-list" role="list">
        <li class="ct-item ct-item--main">
          <p class="ct-label">Phone</p>
          <p class="ct-value"><a href="tel:+6439741812">+64 3 974 1812</a></p>
        </li>
        <li class="ct-item">
          <p class="ct-label">From within New Zealand</p>
          <p class="ct-value"><a href="tel:039741812">(03) 974 1812</a></p>
        </li>
        <li class="ct-item">
          <p class="ct-label">From Australia</p>
          <p class="ct-value"><a href="tel:00116439741812">0011 64 3 974 1812</a></p>
        </li>
        <li class="ct-item">
          <p class="ct-label">From the USA or Canada</p>
          <p class="ct-value"><a href="tel:0116439741812">011 64 3 974 1812</a></p>
        </li>
        <li class="ct-item ct-item--email">
          <p class="ct-label">Email</p>
          <p class="ct-value"><a href="mailto:info@pounamutourismgroup.com">info@pounamutourismgroup.com</a></p>
        </li>
        <li class="ct-item">
          <p class="ct-label">Postal address</p>
          <p class="ct-value">PO Box 19735, Woolston, Christchurch 8241, New Zealand</p>
          <p class="ct-note">For mail only.</p>
        </li>
      </ul>
      <div class="ct-chat" data-sehe-chat hidden>
        <button type="button" class="sp-btn sp-btn--ghost">Chat with us</button>
      </div>
      <div class="ct-trust">
        <img src="{WTA}" alt="World Travel Awards: New Zealand&#39;s Leading Tour Operator 2025" width="256" height="256" loading="lazy">
        <div class="ct-trust-copy">
          <p>World Travel Awards winner: New Zealand&#39;s Leading Tour Operator 2025.</p>
{TRUSTBOX}
        </div>
      </div>
    </div>
    <div class="ct-formside" hidden>
      <div class="ct-formslot" data-sehe-contact-slot></div>
    </div>
  </div>
  <section class="sp-section ct-quick-sec" aria-labelledby="sehe-ct-quick">
    <div class="sp-head">
      <h2 id="sehe-ct-quick">Helpful information</h2>
    </div>
    <ul class="ct-quick" role="list">
{quick_html}
    </ul>
  </section>
</div>
</div>
{trustbox_loader('sehe-ct-trustbox')}
{ENHANCE}
{DOCK}"""

MASTER_HEADER = """<!-- =====================================================================
     SIR EDMUND HILLARY EXPLORER — CONTACT PAGE (/contact)
     COMPLETE PAGE  ·  VERSION v9  ·  2026-09-25  (paste into ONE Duda HTML widget)
     -----------------------------------------------------------------------
     WHERE IT GOES (the whole page is ONE widget):
       page "contact-new" (duplicate of /contact). Delete the banner row, the
       "Contact Us" text row and the Facebook/Instagram row. In the form's row
       delete the "Send us an enquiry" text and the Trustpilot widget, and KEEP
       THE FORM exactly as it is (button stays "Send"). Add ONE full-width row
       (padding 0) DIRECTLY ABOVE the form's row, add ONE HTML widget, paste
       this whole file. Set the form row's padding to 0 too.
       On the published page the form moves into the right-hand column. In the
       Duda editor it stays in its own row below: that is expected.
       Steps + rollback: notes/2026-09-25-old-pages-rebuild-runbook.md
     -----------------------------------------------------------------------
     CHANGELOG (latest first; v1 to v6 are in the repo history):
       v9 — The real cause of the vanishing, found on the live contact-new
            (25 Sep 2026): the copied text stopped at line 150, inside the
            CSS, so the page's HTML never reached Duda (it happened to v7
            and to one v8 attempt; the complete v8 paste works). The code
            was never the problem. v9 adds an END OF FILE line as the last
            line: if it is the last line in Duda's code box, the whole file
            is pasted. Copy from the downloaded file, never from a preview.
            Page code identical to v8.
       v8 — v7 vanished in the Duda editor after Update. v8 uses only markup
            already working in this site's Duda widgets: the contact list is
            a plain list (no definition-list tags), the CSS has no child
            combinators (Duda publishes that character as an HTML entity,
            which silently drops the rule), and the docking script polls
            the way the live tour pages' script does. Copy unchanged.
       v7 — CONSOLIDATED: the three blocks (A/B/C) became ONE HTML widget;
            on the published site a small script moves the native form into
            the right-hand column (the tour pages' docking method).
     -----------------------------------------------------------------------
     PASTE FROM LATEST/: contact-page.txt (one file, one widget).
     RULES KEPT: native form untouched (recipient, subject, webhook, field
     IDs, labels, reCAPTCHA, success message); every phone and email link is
     a plain link (GTM "Phone Link Clicked" fires on phone-link clicks);
     nothing here can show .dmform-success (GTM "Contact Us Form Submitted"
     keys on it); no rating hard-coded (live TrustBox only); no extra
     bootstrap; no chat system added (tawk.to already loads site-wide); no
     schema; no tracking; no departure data; CSS scoped to .sehe-pg-contact.
     ===================================================================== -->"""

master = MASTER_HEADER + '\n' + PAGE + '\n' + end_marker('contact-page.txt', 'v9') + '\n'
out = os.path.join(REPO, 'SEHE-contact-page_v9.txt')
open(out, 'w', encoding='utf-8').write(master)
assert not check_script_safety(master), check_script_safety(master)
assert not check_style_safety(master), check_style_safety(master)
open(os.path.join(OUT_DIR, 'contact-page.html'), 'w', encoding='utf-8').write(master)
print('wrote', out, len(master), 'bytes')
