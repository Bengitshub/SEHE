"""Guardrail checks for an old-page master. usage: verify.py <master> [live-snapshot] [--verbatim-file f]"""
import re, sys, html
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kit import check_script_safety, check_style_safety
m = open(sys.argv[1], encoding='utf-8').read()
noncomment = re.sub(r'<!--.*?-->', '', m, flags=re.S)
visible = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', noncomment, flags=re.S)
text = re.sub(r' ([,.;:!?])', r'\1', html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', visible))).replace('\u00a0', ' '))
fails, notes = [], []
def need(c, msg):
    (notes if c else fails).append(('ok   ' if c else 'FAIL ') + msg)
need(not check_script_safety(m), "inline scripts contain no '<' or '&'")
bad_css = check_style_safety(m)
need(not bad_css, "no '>' or '<' inside <style> (Duda publishes '>' as &gt; and the rule is dropped)" + (': ' + ' || '.join(bad_css[:3]) if bad_css else ''))
need(not re.search(r'<(dl|dt|dd)\b', noncomment), 'no dl/dt/dd tags (never proven in a Duda HTML widget on this site)')
need(not re.search(r'application/ld\+json|itemtype=|itemprop=|AggregateRating', m), 'no schema / microdata')
own = re.sub(r'<blockquote.*?</blockquote>', ' ', visible, flags=re.S)   # our own copy only (guest quotes excluded)
owntext = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', own)))
hit = re.search(r'(TrustScore|\b4\.[5-9]\b|\b\d{2,3}\s+reviews|Rated\s+(5|five)|\bExcellent\b)', owntext, re.I)
need(not hit, 'no hard-coded TrustScore / rating / review count / "Excellent" in our own copy' + (': ' + hit.group(0) if hit else ''))
need(not re.search(r'tp\.widget\.bootstrap', noncomment), 'no extra Trustpilot bootstrap')
need(not re.search(r'checkfront\.com|CHECKFRONT_|workers\.dev|__seheDeparture|data-sehe-dep|data-departure|next departure', noncomment, re.I), 'no departure data / Worker / Checkfront code')
need(not re.search(r'googletagmanager|gtag\(|fbq\(|adroll|clarity\.ms|hotjar|dataLayer', noncomment, re.I), 'no tracking code')
imgs = re.findall(r'<img[^>]*\ssrc="([^"]+)"', noncomment) + re.findall(r'srcset="([^"]+)"', noncomment) + re.findall(r'url\([\'"]?(https?://[^\'")]+)', noncomment)
hosts = [x.split('=',1)[1] for x in sys.argv if x.startswith('--allow-image-host=')]
badimg = [u for u in imgs for part in u.split(',') for x in [part.strip().split(' ')[0]] if x and not re.match(r'https://l?irp\.cdn-website\.com/35e9f777/', x) and not any(x.startswith('https://' + hh + '/') for hh in hosts)]
need(not badimg, 'all images on the Duda CDN (35e9f777)' + (' + allowed: ' + ','.join(hosts) if hosts else '') + (': ' + str(badimg[:3]) if badimg else ''))
alts = re.findall(r'<img(?![^>]*\balt=)[^>]*>', noncomment)
need(not alts, 'every <img> has an alt attribute')
for t in re.findall(r'href="(tel:[^"]*)"', noncomment):
    need(re.fullmatch(r'tel:\+?[0-9]+', t) is not None, f'tel link well-formed: {t}')
for t in re.findall(r'href="(mailto:[^"]*)"', noncomment):
    need(re.fullmatch(r'mailto:[\w.+-]+@[\w.-]+\.\w+', t) is not None, f'mailto link well-formed: {t}')
need(not re.search(r'small[- ]group', text, re.I), 'no "small group(s)" wording')
need(not re.search(r'rail touring', text, re.I), 'no "rail touring" wording')
amounts = re.findall(r'(?:NZ|AU|US)?\$\s?\d[\d,.]*', text)
allowed = [x for x in sys.argv if x.startswith('--allow-amount=')]
amounts = [x for x in amounts if ('--allow-amount=' + x) not in allowed]
need(not amounts, 'no prices / dollar amounts on the page' + (': ' + str(amounts[:4]) if amounts else ''))
ext = re.findall(r'<a [^>]*target="_blank"[^>]*>', noncomment)
need(all('noopener' in a for a in ext), 'target=_blank links carry rel=noopener')
css = re.sub(r'/\*.*?\*/', '', ' '.join(re.findall(r'<style>(.*?)</style>', m, re.S)), flags=re.S)
sel = [s.strip() for blk in re.findall(r'([^{}]+)\{', re.sub(r'@media[^{]+\{', '', css)) for s in blk.split(',')]
wrap = re.search(r'class="(sehe-pg-[a-z-]+)"', m).group(1)
leak = [s for s in sel if s and not s.startswith('@') and wrap not in s and not s.startswith('from') and not s.startswith('to')]
need(not leak, f'every CSS selector scoped to .{wrap}' + (': ' + str(leak[:4]) if leak else ''))
# verbatim: every line of the verbatim file must appear in the visible text
if '--verbatim-file' in sys.argv:
    vf = sys.argv[sys.argv.index('--verbatim-file') + 1]
    lines = [l.rstrip('\n') for l in open(vf, encoding='utf-8') if l.strip()]
    miss = [l for l in lines if re.sub(r' ([,.;:!?])', r'\1', re.sub(r'\s+', ' ', l.strip())) not in text]
    need(not miss, f'{len(lines) - len(miss)}/{len(lines)} verbatim passages present' + (': MISSING ' + ' || '.join(x[:70] for x in miss[:4]) if miss else ''))
print('\n'.join(notes + fails)); print(f'== {len(fails)} failure(s)'); sys.exit(1 if fails else 0)
