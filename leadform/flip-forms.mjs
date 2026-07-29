/* SEHE — flip the tour pages' brochure forms to DIRECT lead capture.
   Replaces each page's inert form binder with a live script that POSTs the
   lead to the Worker /lead endpoint (which forwards to that tour's existing
   Zapier hook -> ActiveCampaign + Excel), and adds a hidden honeypot field.
   Design untouched. Graceful: any failure still sends the visitor to
   /brochure-collection, so the button's promise is always kept. No-JS
   fallback unchanged (the form's action already points there).

   Usage:
     node leadform/flip-forms.mjs           -> DRY RUN into leadform/preview/
     node leadform/flip-forms.mjs --apply   -> real sweep: new versions +
                                               changelogs + preview re-sync
   Run AFTER Aaron's switch-over, once the ZAPIER_HOOKS_JSON secret is set
   and the worker redeployed (see ENABLE-DIRECT-LEADS.md). */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';

const APPLY = process.argv.includes('--apply');
const OUT = 'leadform/preview/';
const TODAY = new Date().toISOString().slice(0, 10);

const PAGES = [
  { file: 'SEHE-14day-tour_v28.txt',             key: '14day-2627',  tour: '14-Day Spring/Summer Tour 2026/27', prev: 'sehe-14day-page-complete.html' },
  { file: 'SEHE-11day-2627-tour_v26.txt',        key: '11day-2627',  tour: '11-Day Spring/Summer Tour 2026/27', prev: 'sehe-11day-2627-page-complete.html' },
  { file: 'SEHE-12day-winter-2026-tour_v28.txt', key: 'winter-2026', tour: '12-Day Winter Edition 2026',        prev: 'sehe-12day-winter-2026-page-complete.html' },
  { file: 'SEHE-12day-winter-2027-tour_v19.txt',   key: 'winter-2027', tour: '12-Day Winter Edition 2027',        prev: 'sehe-12day-winter-2027-page-complete.html' },
  { file: 'SEHE-pinnacle-2027-tour_v19.txt',       key: 'pinnacle-2027', tour: 'The Pinnacle Tour 2027',          prev: 'sehe-pinnacle-2027-page-complete.html' },
  { file: 'SEHE-11day-2728-tour_v21.txt',         key: '11day-2728',  tour: '11-Day Spring/Summer Tour 2027/28', prev: 'sehe-11day-2728-page-complete.html' },
  { file: 'SEHE-14day-2728-tour_v30.txt',        key: '14day-2728',  tour: '14-Day Spring/Summer Tour 2027/28', prev: 'sehe-14day-2728-page-complete.html' },
];

const HONEYPOT = '<div class="field" style="position:absolute; left:-9999px; top:-9999px;" aria-hidden="true"><input type="text" name="sehe_hp" tabindex="-1" autocomplete="off" value=""></div>\n      ';

const LIVE_SCRIPT = (key, tour) => `<script>
  (function() {
  /* Brochure form — DIRECT lead capture. Sends the lead to our Worker /lead
     endpoint, which validates it and forwards to this tour's existing Zapier
     hook (ActiveCampaign + the Excel log receive identical data to before).
     GRACEFUL: whatever happens — success, worker down, endpoint not yet
     enabled — the visitor continues to /brochure-collection within a few
     seconds, so the button's promise is always kept and no visitor is ever
     stuck. With JS off, the form's own action does the same redirect. */
  var ENDPOINT = 'https://sehe-next-departures.ben-757.workers.dev/lead';
  var PAGE_KEY = ${JSON.stringify(key)};
  var TOUR_NAME = ${JSON.stringify(tour)};
  var form = document.querySelector('.sehe-brochure-form');
  if (!form) return;
  var sel = form.querySelector('select[name="dmform-2"]');
  if (sel) {
    sel.addEventListener('change', function() {
      if (this.value) this.classList.add('has-value');
    });
  }
  var submitted = false;
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (submitted) return;
    var get = function(n) { var el = form.querySelector('[name="' + n + '"]'); return el ? (el.value || '').trim() : ''; };
    if (!get('dmform-1') || !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(get('dmform-3'))) {
      alert('Please enter your name and a valid email address.');
      return;
    }
    submitted = true;
    var data = {
      name: get('dmform-1'),
      email: get('dmform-3'),
      country: get('dmform-2'),
      website: get('sehe_hp'),   /* honeypot — humans never fill this; name chosen so browser autofill never matches it */
      page: PAGE_KEY,
      tour: TOUR_NAME,
      source_url: (window.location && window.location.href) ? window.location.href : ''
    };
    var btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.disabled = true; btn.textContent = 'One moment\\u2026'; }
    var done = false;
    var go = function() { if (!done) { done = true; window.location.href = '/brochure-collection'; } };
    setTimeout(go, 3500);   /* failsafe: never trap the visitor */
    try {
      fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data), keepalive: true })
        .then(go, go);
    } catch (err) { go(); }
  });
})();
</script>`;

const ENTRY = (v, key) => `       v${v} — DIRECT LEAD CAPTURE: the brochure form now submits for real — the
            lead goes to the Worker /lead endpoint, which forwards it to this
            tour's existing Zapier hook, so ActiveCampaign and the Excel log
            receive the same data as the old Duda-form flow (same field names).
            Hidden honeypot field added for spam protection; client-side name +
            email validation (invalid input alerts and lets the visitor fix it —
            no silent lead loss); double-submit guarded. Graceful on every
            failure path: the visitor always continues to /brochure-collection.
            Requires the ZAPIER_HOOKS_JSON Worker secret (see
            leadform/ENABLE-DIRECT-LEADS.md); until it is set the endpoint
            answers 503 and the visitor experience is unchanged.\n`;

if (!APPLY) mkdirSync(OUT, { recursive: true });
/* PRE-FLIGHT: verify every page transforms cleanly BEFORE writing anything,
   so a mid-run failure can never leave the set half-flipped. */
const errs = [];
for (const P of PAGES) {
  let src;
  try { src = readFileSync(P.file, 'utf8'); } catch (e) { errs.push(P.file + ': missing'); continue; }
  if (!/<script>\s*\(function\(\) \{\s*\/\* Brochure form \(design template\)[\s\S]*?<\/script>/.test(src)) errs.push(P.file + ': binder not found (already flipped?)');
  if (src.indexOf('<button type="submit">', src.indexOf('sehe-brochure-form')) < 0) errs.push(P.file + ': submit button not found');
  if (!/VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d/.test(src)) errs.push(P.file + ': VERSION header not found');
}
if (errs.length) { console.log('PRE-FLIGHT FAILED — nothing written:'); errs.forEach((x) => console.log('  !! ' + x)); process.exit(1); }
for (const P of PAGES) {
  let t = readFileSync(P.file, 'utf8');
  // 1) replace the inert binder IIFE with the live capture script
  const binder = t.match(/<script>\s*\(function\(\) \{\s*\/\* Brochure form \(design template\)[\s\S]*?<\/script>/);
  t = t.replace(binder[0], LIVE_SCRIPT(P.key, P.tour));
  // 2) inject the honeypot field just before the submit button
  const btnAt = t.indexOf('<button type="submit">', t.indexOf('sehe-brochure-form'));
  t = t.slice(0, btnAt) + HONEYPOT + t.slice(btnAt);
  // 3) version bump + changelog
  const vm = t.match(/VERSION v(\d+)(\s*·\s*)\d{4}-\d\d-\d\d/);
  const nv = String(Number(vm[1]) + 1);
  t = t.replace(vm[0], `VERSION v${nv}${vm[2]}${TODAY}`);
  t = t.replace(/CHANGELOG \(latest first\):\n/, (m) => m + ENTRY(nv, P.key));
  const newName = P.file.replace(/_v\d+\.txt$/, `_v${nv}.txt`);
  if (APPLY) {
    writeFileSync(newName, t);
    execSync(`python3 tools/check_tour_page.py ${newName}`, { stdio: 'inherit' });   // fails loudly
    execSync(`node tools/check-revert-guard.mjs ${newName}`, { stdio: 'inherit' });  // fails loudly
    writeFileSync(P.prev, t);
    if (newName !== P.file) execSync(`git rm -q ${P.file}`);
    console.log(`FLIPPED + VALIDATED ${newName}`);
  } else {
    writeFileSync(OUT + newName, t);
    console.log(`dry-run -> ${OUT}${newName}`);
  }
}
console.log(APPLY ? '\nAPPLIED — deliver the new versions.' : '\nDRY RUN — outputs in leadform/preview/ for validation; masters untouched.');
