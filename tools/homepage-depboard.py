#!/usr/bin/env python3
"""Homepage — 'All aboard.' departure board (Ben's idea, 29 Jul).

A date-first rail directly under the hero: every UPCOMING BOOKABLE departure
across all tours, ordered purely by date, with month-jump chips. NOT a
carousel — nothing moves unless the guest moves it (arrows / swipe / scroll;
scroll-snap; no autoplay), honouring the older-audience conversion review.

Enhance-only, twice over:
  * The rail is BAKED from a live worker-feed snapshot at build time — the
    section is complete and correct with JavaScript off or the worker down.
  * On load, the page's existing feed fetch also refreshes the rail: cards
    whose date has passed or sold out are hidden, 'Filling fast' chips are
    applied. Missing data can only ever leave the baked state standing.

Tour names, prices, durations and links are read from the homepage's own
journey cards (single source of voice). Cards carry NO photographs (Ben,
31 Jul): the board's photo pools doubled the journeys-section imagery one
scroll below, so each card opens with a navy date header instead — variant C
of the assessed options (flat B / navy-header C), chosen because the date is
the card's actual message and the header echoes the rail's navy end-cap.

Usage: python3 tools/homepage-depboard.py <homepage-master.txt> [--apply]
"""
import json
import re
import sys
import os
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]
APPLY = '--apply' in sys.argv
FEED = '/tmp/claude-0/-home-user-SEHE/0cc36833-90aa-502d-8b8c-c61310a548dd/scratchpad/feed-bake.json'

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
MON3 = [m[:3] for m in MONTHS]

body = open(os.path.join(REPO, SRC), encoding='utf-8').read()
src_orig = body

# ---- tour meta from the homepage's own cards --------------------------------
META = {}
for m in re.finditer(r'<article class="shx-jc[^"]*">[\s\S]*?</article>', body):
    card = m.group(0)
    key_m = re.search(r'data-shx-next="([a-z0-9-]+)"', card)
    if not key_m:
        continue
    key = key_m.group(1)
    name = re.search(r'<h3>([\s\S]*?)</h3>', card).group(1).strip()
    href = re.search(r'class="shx-btn[^"]*" href="([^"]+)"', card).group(1)
    price_m = re.search(r'From <strong>(NZ\$[\d,]+)</strong>', card)
    days_m = re.search(r'<strong>(\d+) days</strong>\s*&middot;\s*(\d+) nights', card)
    META[key] = {
        'name': name, 'href': href,
        'price': price_m.group(1) if price_m else '',
        'days': days_m.group(1) if days_m else '',
        'nights': days_m.group(2) if days_m else '',
    }
assert len(META) >= 6, f'expected 6+ tours from cards, got {list(META)}'

# ---- departures from the feed snapshot --------------------------------------
feed = json.load(open(FEED))
today = date.today().isoformat()
deps = []
for key, t in feed.items():
    if key not in META:
        continue                                   # e.g. winter-2026: sold out, no card hook
    for x in t['all']:
        if x['status'] == 'soldout' or x['start'] < today:
            continue
        deps.append({'key': key, 'start': x['start'], 'end': x['end'], 'status': x['status']})
deps.sort(key=lambda d: d['start'])
assert len(deps) >= 40, f'only {len(deps)} departures baked — feed snapshot suspect'


def pretty(iso):
    y, mo, dy = iso.split('-')
    return int(dy), MON3[int(mo) - 1], y


def countdown(iso, today_iso):
    from datetime import date as _d
    a = _d(*[int(x) for x in today_iso.split('-')])
    b = _d(*[int(x) for x in iso.split('-')])
    n = (b - a).days
    if n <= 0: return 'Departs today'
    if n == 1: return 'Departs tomorrow'
    if n < 14: return f'Departs in {n} days'
    if n < 70: return f'Departs in {max(2, round(n / 7))} weeks'
    return f'Departs in {max(2, round(n / 30.4))} months'


def rng(a, b):
    d1, m1, y1 = pretty(a)
    d2, m2, y2 = pretty(b)
    if (m1, y1) == (m2, y2):
        return f'{d1}&ndash;{d2} {m1} {y1}'
    if y1 == y2:
        return f'{d1} {m1} &ndash; {d2} {m2} {y1}'
    return f'{d1} {m1} {y1} &ndash; {d2} {m2} {y2}'


# ---- month chips + cards -----------------------------------------------------
first = deps[0]
first_meta = META[first['key']]
fd, fm, fy = pretty(first['start'])
NEXTAWAY = f"{fd} {fm} {fy} &middot; {first_meta['name']}"
NEXTHREF = first_meta['href']
months_seen = []
cards = []
for d in deps:
    y, mo = d['start'][:4], int(d['start'][5:7])
    mkey = f'{y}-{d["start"][5:7]}'
    if mkey not in [m[0] for m in months_seen]:
        months_seen.append((mkey, f'{MON3[mo-1]} {y}'))
    meta = META[d['key']]
    dy, m3, yy = pretty(d['start'])
    from datetime import date as _d
    days_out = (_d(*[int(x) for x in d['start'].split('-')]) - _d(*[int(x) for x in today.split('-')])).days
    if days_out <= 31:
        pill_mod, pill_txt, near = '--closing', 'Closing soon', ' shx-dep--closing'
    elif d['status'] == 'nearing':
        pill_mod, pill_txt, near = '--near', 'Filling fast', ' shx-dep--near'
    else:
        pill_mod, pill_txt, near = '--go', 'Now Booking', ''
    nearchip = f'<span class="shx-dep-pill shx-dep-pill{pill_mod}"><span class="shx-dep-pill-dot"></span><span class="shx-dep-pill-label">{pill_txt}</span></span>'
    count_txt = countdown(d['start'], today)
    cards.append(f'''        <article class="shx-dep{near}" data-shx-dep="{d['key']}|{d['start']}" data-month="{mkey}">
          <a class="shx-dep-link" href="{meta['href']}" aria-label="{meta['name']} departing {dy} {m3} {yy} — view the journey">
            <span class="shx-dep-head">{nearchip}<span class="shx-dep-date"><strong>{dy} {m3}</strong> {yy}</span><span class="shx-dep-rule"></span></span>
            <span class="shx-dep-body">
              <span class="shx-dep-count" data-shx-count="{d['start']}">{count_txt}</span>
              <span class="shx-dep-name">{meta['name']}</span>
              <span class="shx-dep-meta">{rng(d['start'], d['end'])} &middot; {meta['days']} days</span>
              <span class="shx-dep-foot"><span class="shx-dep-price">From {meta['price']}</span><span class="shx-dep-go">View journey &rarr;</span></span>
            </span>
          </a>
        </article>''')

LASTMONTH = months_seen[-1][1].replace('Apr', 'April').replace('Oct', 'October').replace('Nov', 'November').replace('Dec', 'December').replace('Jan', 'January').replace('Feb', 'February').replace('Mar', 'March').replace('Jun', 'June').replace('Jul', 'July').replace('Aug', 'August').replace('Sep', 'September').replace('May', 'May')
chips = '\n'.join(
    f'        <button type="button" class="shx-depmonth{" is-active" if i == 0 else ""}" data-shx-month="{k}">{label}</button>'
    for i, (k, label) in enumerate(months_seen))

SECTION = f'''
  <!-- ============ 1b. DEPARTURE BOARD — "All aboard." (date-first rail) ============ -->
  <section class="shx-depboard shx-band" aria-label="Upcoming departures across all journeys">
    <div class="shx-wrap">
      <div class="shx-depboard-head">
        <div>
          <span class="shx-kicker">Departing Soon</span>
          <h2 class="shx-display">Find your next departure.</h2>
          <p class="shx-depnext"><span class="shx-depnext-dot" aria-hidden="true"></span>Next departure: <a data-shx-nextaway href="{NEXTHREF}"><strong>{NEXTAWAY}</strong></a></p>
          <p class="shx-depboard-sub">Choose a date that suits you &mdash; now booking through to {LASTMONTH}.</p>
        </div>
        <div class="shx-depboard-arrows" aria-hidden="false">
          <button type="button" class="shx-deparrow" data-shx-deparrow="-1" aria-label="Scroll to earlier departures">&larr;</button>
          <button type="button" class="shx-deparrow" data-shx-deparrow="1" aria-label="Scroll to later departures">&rarr;</button>
        </div>
      </div>
      <div class="shx-depmonths" role="tablist" aria-label="Jump to a month">
{chips}
      </div>
    </div>
    <div class="shx-deprail-outer">
      <div class="shx-deprail" data-shx-deprail tabindex="0" aria-label="Departures, earliest first — scroll for more">
{chr(10).join(cards)}
        <article class="shx-dep shx-dep-end">
          <a class="shx-dep-endlink" href="/journeys">
            <span class="shx-dep-endtitle">End of season.</span>
            <span class="shx-dep-endsub">That&rsquo;s every date to {LASTMONTH}. The 2028/29 season will be released soon.</span>
            <span class="shx-dep-endgo">See every journey &rarr;</span>
          </a>
        </article>
      </div>
    </div>
  </section>
'''

CSS = '''
  /* ============ 1b. DEPARTURE BOARD ============ */
  .shx-depboard { background: var(--paper); border-bottom: 1px solid var(--paper-line); }
  .shx-depboard-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 18px; margin-bottom: 22px; }
  .shx-depboard h2 { font-size: clamp(28px, 3.4vw, 38px) !important; color: var(--ink) !important; line-height: 1.15 !important; margin: 0 !important; }
  .shx-depboard-sub { margin: 10px 0 0 !important; max-width: 60ch; font-size: 17px !important; color: var(--body-soft) !important; }
  .shx-depnext { display: flex; align-items: center; gap: 9px; margin: 12px 0 0 !important; font-size: 15px !important; color: var(--body-soft) !important; }
  .shx-depnext a { text-decoration: none !important; }
  .shx-depnext a:hover strong { text-decoration: underline; text-underline-offset: 3px; }
  .shx-depnext strong { color: var(--ink); font-weight: 700 !important; }
  .shx-depnext-dot { width: 9px; height: 9px; border-radius: 50%; background: #2a7a4a; flex: none; animation: shx-deppulse 1.8s ease-in-out infinite; }
  @keyframes shx-deppulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(42, 122, 74, .45); } 55% { box-shadow: 0 0 0 7px rgba(42, 122, 74, 0); } }
  .shx-depboard-arrows { display: flex; gap: 10px; }
  .shx-deparrow { width: 52px; height: 52px; border-radius: 50%; border: 1.5px solid var(--gold); background: #ffffff; color: var(--ink); font-size: 20px; cursor: pointer; transition: background .2s ease; }
  .shx-deparrow:hover { background: var(--gold-pale); }
  .shx-depmonths { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 8px; scrollbar-width: thin; }
  .shx-depmonth { flex: none; border: 1px solid var(--paper-line); background: #ffffff; border-radius: 20px; padding: 8px 15px; font-family: 'Montserrat', sans-serif !important; font-size: 12px !important; font-weight: 700 !important; letter-spacing: .4px; color: var(--body-soft); cursor: pointer; }
  .shx-depmonth.is-active { background: var(--ink); border-color: var(--ink); color: #ffffff; }
  .shx-deprail-outer { overflow: hidden; }
  .shx-deprail { display: flex; gap: 18px; overflow-x: auto; padding: 6px 0 18px; scroll-snap-type: x proximity; -webkit-overflow-scrolling: touch; scrollbar-width: thin;
    padding-left: max(32px, calc(50vw - 590px)); padding-right: 32px; }
  .shx-dep { flex: 0 0 420px; scroll-snap-align: start; background: #ffffff; border: 1px solid var(--paper-line); border-radius: 10px; overflow: hidden; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
  .shx-dep:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(21, 59, 103, .08); border-color: var(--gold); }
  .shx-dep[hidden] { display: none; }
  .shx-dep-link { display: block; text-decoration: none !important; color: inherit; }
  .shx-dep-head { position: relative; display: block; background: var(--ink); padding: 22px 20px 20px; }
  .shx-dep-rule { display: block; width: 44px; height: 2px; background: var(--gold); margin: 12px 0 0; }
  .shx-dep-pill { position: absolute; top: 14px; right: 14px; display: inline-flex; align-items: center; gap: 6px; color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; font-size: 10.5px !important; font-weight: 700 !important; letter-spacing: 1px; text-transform: uppercase; padding: 6px 11px 6px 9px; border-radius: 20px; box-shadow: 0 2px 6px rgba(0,0,0,.18); }
  .shx-dep-pill--go { background: rgba(42, 122, 74, .95); }
  .shx-dep-pill--near { background: rgba(196, 126, 22, .96); }
  .shx-dep-pill-dot { width: 6px; height: 6px; background: #ffffff; border-radius: 50%; animation: shx-deppulse-w 1.6s ease-in-out infinite; }
  @keyframes shx-deppulse-w { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
  .shx-dep-pill--closing { background: rgba(178, 74, 18, .96); }
  .shx-dep-count { display: block; font-family: 'Montserrat', sans-serif !important; font-size: 11.5px !important; font-weight: 700 !important; letter-spacing: .8px; text-transform: uppercase; color: var(--gold-deep) !important; line-height: 1.3 !important; margin: 0 0 6px; }
  .shx-dep-end { background: var(--ink); border-color: var(--gold); display: flex; }
  .shx-dep-endlink { display: flex; flex-direction: column; justify-content: center; gap: 10px; padding: 28px 26px; text-decoration: none !important; }
  .shx-dep-endtitle { font-family: 'Montserrat', sans-serif !important; font-size: 20px !important; font-weight: 700 !important; letter-spacing: -0.2px; color: #ffffff !important; line-height: 1.3 !important; }
  .shx-dep-endsub { font-size: 14.5px !important; color: rgba(243,236,221,.8) !important; line-height: 1.55 !important; }
  .shx-dep-endgo { font-family: 'Montserrat', sans-serif !important; font-size: 12.5px !important; font-weight: 700 !important; letter-spacing: .6px; text-transform: uppercase; color: var(--gold) !important; }
  .shx-dep-body { display: block; padding: 16px 20px 18px; }
  .shx-dep-date { display: block; font-family: 'Montserrat', sans-serif !important; font-size: 30px !important; line-height: 1.15 !important; color: rgba(243,236,221,.72) !important; margin: 0; }
  .shx-dep-date strong { color: #ffffff; font-weight: 700 !important; }
  .shx-dep-name { display: block; font-family: 'Montserrat', sans-serif !important; font-size: 16.5px !important; font-weight: 700 !important; letter-spacing: -0.2px; line-height: 1.25 !important; color: var(--ink) !important; margin-bottom: 3px; }
  .shx-dep-meta { display: block; font-size: 14px !important; line-height: 1.45 !important; color: var(--body-soft) !important; margin-bottom: 10px; }
  .shx-dep-foot { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
  .shx-dep-price { font-size: 14px !important; color: var(--body-soft) !important; }
  .shx-dep-go { display: inline-flex; align-items: center; font-family: 'Montserrat', sans-serif !important; font-size: 12px !important; font-weight: 700 !important; letter-spacing: .8px; text-transform: uppercase; color: #ffffff !important; background: var(--ink); border: 1.5px solid var(--ink); border-radius: 4px; padding: 9px 14px; white-space: nowrap; transition: background .2s ease; }
  .shx-dep:hover .shx-dep-go { background: var(--ink-soft); }
  @media (max-width: 860px) {
    .shx-depboard-arrows { display: none; }
    .shx-deprail { padding-left: 20px; padding-right: 20px; }
    .shx-dep { flex-basis: 78vw; }
  }
  @media (max-width: 540px) {
    .shx-deprail { gap: 12px; padding-left: 16px; padding-right: 16px; }
    .shx-dep { flex-basis: 82vw; }
    .shx-dep-head { padding: 18px 18px 16px; }
    .shx-dep-date { font-size: 25px !important; }
    .shx-dep-body { padding: 14px 18px 16px; }
    .shx-depboard-sub { font-size: 15.5px !important; }
  }
'''

JS = '''
  /* DEPARTURE BOARD — nothing moves unless the guest moves it. Baked cards
     are the base state; this only hides passed/sold dates, adds "Filling
     fast", and wires arrows + month jumps. */
  (function () {
  var rail = document.querySelector('[data-shx-deprail]');
  if (!rail) return;
  var reduced = false;
  try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (err) { reduced = false; }
  var today = new Date().toISOString().slice(0, 10);
  var cards = rail.querySelectorAll('[data-shx-dep]');
  for (var i = 0; i < cards.length; i += 1) {
    var start = (cards[i].getAttribute('data-shx-dep') || '').split('|')[1] || '';
    if (start && start < today) { cards[i].setAttribute('hidden', ''); }
  }
  var counts = rail.querySelectorAll('[data-shx-count]');
  for (var i = 0; i < counts.length; i += 1) {
    var d0 = new Date(today + 'T00:00:00Z');
    var d1 = new Date(counts[i].getAttribute('data-shx-count') + 'T00:00:00Z');
    var n = Math.round((d1 - d0) / 86400000);
    var t = '';
    if (n <= 0) { t = 'Departs today'; }
    else if (n === 1) { t = 'Departs tomorrow'; }
    else if (n < 14) { t = 'Departs in ' + n + ' days'; }
    else if (n < 70) { t = 'Departs in ' + Math.max(2, Math.round(n / 7)) + ' weeks'; }
    else { t = 'Departs in ' + Math.max(2, Math.round(n / 30.4)) + ' months'; }
    counts[i].textContent = t;
    if (n <= 31 && n >= 0) {
      var card = counts[i].closest('[data-shx-dep]');
      var pill = card && card.querySelector('.shx-dep-pill');
      var lab = card && card.querySelector('.shx-dep-pill-label');
      if (card && card.className.indexOf('shx-dep--closing') < 0) { card.className += ' shx-dep--closing'; }
      if (pill) { pill.className = 'shx-dep-pill shx-dep-pill--closing'; }
      if (lab) { lab.textContent = 'Closing soon'; }
    }
  }
  var away = document.querySelector('[data-shx-nextaway]');
  function refreshNextAway() {
    if (!away) return;
    var first = rail.querySelector('[data-shx-dep]:not([hidden])');
    if (!first) return;
    var dateEl = first.querySelector('.shx-dep-date');
    var nameEl = first.querySelector('.shx-dep-name');
    if (dateEl && nameEl) {
      var strongEl = away.querySelector('strong') || away;
      strongEl.textContent = dateEl.textContent.trim() + ' \u00b7 ' + nameEl.textContent.trim();
      var linkEl = first.querySelector('.shx-dep-link');
      if (away.tagName === 'A' && linkEl) { away.setAttribute('href', linkEl.getAttribute('href')); }
    }
  }
  refreshNextAway();
  window.__shxRailApply = function (data) {
    if (!data || typeof data !== 'object') return;
    var list = rail.querySelectorAll('[data-shx-dep]');
    for (var i = 0; i < list.length; i += 1) {
      var bits = (list[i].getAttribute('data-shx-dep') || '').split('|');
      var tour = data[bits[0]];
      if (!tour || !tour.all) continue;
      for (var k = 0; k < tour.all.length; k += 1) {
        if (tour.all[k].start !== bits[1]) continue;
        if (tour.all[k].status === 'soldout') { list[i].setAttribute('hidden', ''); }
        else if (tour.all[k].status === 'nearing' && list[i].className.indexOf('shx-dep--closing') < 0) {
          list[i].className += (list[i].className.indexOf('shx-dep--near') < 0 ? ' shx-dep--near' : '');
          var pill = list[i].querySelector('.shx-dep-pill');
          var lab = list[i].querySelector('.shx-dep-pill-label');
          if (pill) { pill.className = 'shx-dep-pill shx-dep-pill--near'; }
          if (lab) { lab.textContent = 'Filling fast'; }
        }
        break;
      }
    }
    refreshNextAway();
  };
  function step(dir) {
    var card = rail.querySelector('[data-shx-dep]:not([hidden])');
    var w = card ? card.getBoundingClientRect().width + 18 : 440;
    rail.scrollBy({ left: dir * w * 2, behavior: reduced ? 'auto' : 'smooth' });
  }
  var arrows = document.querySelectorAll('[data-shx-deparrow]');
  for (var a = 0; a < arrows.length; a += 1) {
    arrows[a].addEventListener('click', function () { step(parseInt(this.getAttribute('data-shx-deparrow'), 10)); });
  }
  var chips = document.querySelectorAll('[data-shx-month]');
  function setActive(mkey) {
    for (var c = 0; c < chips.length; c += 1) {
      chips[c].className = 'shx-depmonth' + (chips[c].getAttribute('data-shx-month') === mkey ? ' is-active' : '');
    }
  }
  for (var c = 0; c < chips.length; c += 1) {
    chips[c].addEventListener('click', function () {
      var mkey = this.getAttribute('data-shx-month');
      var target = rail.querySelector('[data-month="' + mkey + '"]:not([hidden])');
      if (!target) return;
      setActive(mkey);
      rail.scrollTo({ left: target.offsetLeft - rail.offsetLeft - 4, behavior: reduced ? 'auto' : 'smooth' });
    });
  }
  var ticking = false;
  rail.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var edge = rail.getBoundingClientRect().left + 40;
      var list = rail.querySelectorAll('[data-shx-dep]:not([hidden])');
      for (var i = 0; i < list.length; i += 1) {
        var r = list[i].getBoundingClientRect();
        if (r.right > edge) { setActive(list[i].getAttribute('data-month')); break; }
      }
    });
  });
})();
'''

# ---- strip any previously baked board (idempotent regeneration) -------------
SEC_OPEN = '\n  <!-- ============ 1b. DEPARTURE BOARD'
if SEC_OPEN in body:
    i0 = body.find(SEC_OPEN)
    i1 = body.find('</section>', i0) + len('</section>') + 1
    body = body[:i0] + body[i1:]
CSS_OPEN = '\n  /* ============ 1b. DEPARTURE BOARD ============ */'
if CSS_OPEN in body:
    c0 = body.find(CSS_OPEN)
    c1 = body.find('  /* ============ RESPONSIVE ============ */', c0)
    body = body[:c0] + '\n' + body[c1:]
JS_OPEN = "\n  /* DEPARTURE BOARD — nothing moves"
if JS_OPEN in body:
    j0 = body.find(JS_OPEN)
    j1 = body.find('})();', j0) + len('})();') + 1
    body = body[:j0] + '\n' + body[j1:]
OLD_HOOK = "\n    if (window.__shxRailApply) { window.__shxRailApply(data); }"
body = body.replace(OLD_HOOK, '', 1)

# ---- integrate ---------------------------------------------------------------
# 1. section after the hero
HERO_END = '  </section>\n\n  <!-- ============ 2. CHOOSE YOUR JOURNEY'
assert HERO_END in body, 'hero/journeys seam not found'
body = body.replace(HERO_END, '  </section>\n' + SECTION + '\n  <!-- ============ 2. CHOOSE YOUR JOURNEY', 1)

# 2. CSS before the RESPONSIVE block
MARK = '  /* ============ RESPONSIVE ============ */'
assert MARK in body
body = body.replace(MARK, CSS + '\n' + MARK, 1)

# 3. wire the rail into the existing feed apply()
OLD_APPLY = "      if (label) { chips[i].textContent = label; }\n    }\n  }"
assert OLD_APPLY in body, 'chips apply() anchor not found'
body = body.replace(OLD_APPLY, OLD_APPLY.replace(
    "    }\n  }",
    "    }\n    if (window.__shxRailApply) { window.__shxRailApply(data); }\n  }"), 1)

# 4. rail behaviour script before the chips IIFE
CHIPS_OPEN = "<!-- ===== LIVE NEXT-DEPARTURE CHIPS + FILM REVEAL (enhance-only) ===== -->\n<script>"
assert CHIPS_OPEN in body
body = body.replace(CHIPS_OPEN, CHIPS_OPEN + JS, 1)

# ---- sanity ------------------------------------------------------------------
for tag in ('div', 'section', 'style', 'script', 'article', 'button', 'span'):
    o, c = len(re.findall(rf'<{tag}[\s>]', body)), body.count(f'</{tag}>')
    assert o == c, (tag, o, c)
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', body)
bad = sum(len(re.findall(r'<[a-zA-Z]', s)) for s in scripts)
assert bad == 0, f'{bad} tag-like tokens inside scripts (Duda sanitizer hazard)'
assert 'shx-dep-img' not in body, 'photo cards survived the variant-C rebuild'
# the CSS strip removes [board-CSS .. RESPONSIVE]; nothing else may live there.
# v37 lesson: the brochure-band CSS did, and a regen shipped the band naked.
if '<section class="shx-broch' in body:
    assert '.shx-broch-card {' in body, 'brochure-band CSS lost — it must sit ABOVE the board CSS marker'
assert body.count('shx-dep-head') >= len(deps) + 1  # every card + the CSS rule
assert body.count('data-shx-dep=') == len(deps)
assert body.count('shx-depmonth"') + body.count('shx-depmonth is-active"') >= len(months_seen)

print(f'section: {len(deps)} departures, {len(months_seen)} month chips '
      f'({months_seen[0][1]} -> {months_seen[-1][1]})')
if APPLY:
    open(os.path.join(REPO, SRC), 'w', encoding='utf-8').write(body)
    print(f'APPLIED into {SRC} (version bump is the caller\'s job)')
else:
    print('dry run — nothing written')
