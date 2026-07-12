/* Regression guard for the recurring "departure dates reset after paste" bug.

   ROOT CAUSE (seen on the Journeys page, then again on the tour pages): a render
   function WIPES its baked HTML when window.__seheDepartureData isn't populated at
   the moment it runs. Duda can run a render pass before — or without — the top data
   script, so the booking paint() fell through to "No departures" and the cross-sell
   renderCard() flipped the baked "Now Booking" to "Season Complete".

   THE RULE: a render may only ENHANCE the baked HTML. When the data for its tour
   isn't ready it must RETURN and leave the baked markup alone — never blank it.

   This test extracts a tour page's real booking + cross-sell scripts and runs them
   against a minimal DOM with the data MISSING, asserting the baked content survives
   (and, with data present, that they still render). Run on every tour page:
     node tools/check-revert-guard.mjs SEHE-<tour>_vN.txt [more files...] */
import { readFileSync } from 'node:fs';

const BAKED = 'BAKED_HTML_MARKER';
const stub = () => ({ textContent: '', innerHTML: '', classList: { add() {}, remove() {} },
  addEventListener() {}, getAttribute() { return null; }, setAttribute() {},
  querySelector() { return null; }, querySelectorAll() { return []; } });

function bookingWidget() {
  const c = stub(); c.innerHTML = BAKED;
  const n = stub(); n.textContent = 'baked count';
  const w = stub(); w._a = { 'data-tour': 'X' }; w.getAttribute = (k) => w._a[k]; w.setAttribute = (k, v) => (w._a[k] = v);
  w.querySelector = (s) => (s === '[data-departure-content]' ? c : s === '[data-departure-count]' ? n : null);
  w._c = c; return w;
}
function card() {
  const lbl = { textContent: 'Now Booking' }, date = { textContent: 'Departures available — see tour' };
  const ph = stub(); ph.querySelector = (s) => (s === '.journey-card-next-label' ? lbl : s === '.journey-card-next-date' ? date : null);
  const c = stub(); c._a = { 'data-tour': 'X', 'data-season': 'spring-summer' }; c.getAttribute = (k) => c._a[k];
  c.querySelector = (s) => (s === '[data-next-placeholder]' ? ph : s === '[data-departure-value]' ? { textContent: '' } : s === '[data-departure-label]' ? { textContent: '' } : null);
  c._lbl = lbl; return c;
}
const journeysWidget = (theCard) => { const w = stub(); w.querySelectorAll = (s) => (s.indexOf('filter-btn') >= 0 ? [] : s.indexOf('journey-card') >= 0 ? [theCard] : []); return w; };

function run(src, data, qmap) {
  const win = { __seheDepartureData: data, __seheLoadDepartures: undefined, console, matchMedia: () => ({ matches: false }), setInterval: () => 0 };
  const doc = { querySelector: (s) => qmap[s] || null };
  new Function('window', 'document', 'console', src)(win, doc, console);
}

function checkFile(path) {
  const t = readFileSync(path, 'utf8');
  const scripts = [...t.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  const booking = scripts.find((s) => s.includes('function paint(widget, key)'));
  const xsell = scripts.find((s) => s.includes('function renderCard(card, data)'));
  let fail = 0;
  const ok = (c, m) => { if (!c) { fail++; console.log('    ✗ ' + m); } };

  if (booking) {
    const w = bookingWidget();
    try { run(booking, undefined, { '.sehe-departure-list[data-tour]': w }); } catch (e) { fail++; console.log('    ✗ booking threw with missing data: ' + e.message); }
    ok(w._c.innerHTML === BAKED, 'booking render WIPED the baked dates when __seheDepartureData was missing (must leave them)');
    const w2 = bookingWidget();
    const data = { X: { all: [{ start: '2027-09-27', end: '2027-10-07', status: 'available' }], next: '2027-09-27' } };
    try { run(booking, data, { '.sehe-departure-list[data-tour]': w2 }); } catch (e) { fail++; console.log('    ✗ booking threw with present data: ' + e.message); }
    ok(/September 2027/.test(w2._c.innerHTML), 'booking render did not paint the dates when data WAS present');
  } else { console.log('    ! no booking departure-list script found (skipped)'); }

  if (xsell) {
    const c = card();
    try { run(xsell, undefined, { '.sehe-journeys': journeysWidget(c), '[data-quote-target]': null }); } catch (e) { fail++; console.log('    ✗ cross-sell threw with missing data: ' + e.message); }
    ok(c._lbl.textContent === 'Now Booking', 'cross-sell render FLIPPED the baked card when data was missing (must leave "Now Booking")');
  } else { console.log('    ! no cross-sell renderCard script found (skipped)'); }

  return fail;
}

const files = process.argv.slice(2);
if (!files.length) { console.log('usage: node tools/check-revert-guard.mjs <tour-page.txt> [...]'); process.exit(2); }
let bad = 0;
for (const f of files) { const n = checkFile(f); console.log(`[${n === 0 ? 'PASS' : 'FAIL'}] ${f}`); bad += n; }
console.log('\n' + (bad === 0 ? 'ALL PASSED — baked departure HTML is never wiped on missing data' : 'FAILURES — a render wipes baked HTML when data is missing'));
process.exit(bad ? 1 : 0);
