const { chromium } = await import(process.env.PW_PATH);
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname } from 'node:path';
const OUT = process.env.OUT; const QS = process.env.QS || ''; const ONLY = process.env.ONLY ? JSON.parse(process.env.ONLY) : null;
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
const page = await browser.newPage({ viewport:{ width:1300, height:2000 }, deviceScaleFactor:1 });
const errs=[]; page.on('pageerror', e=>errs.push(String(e.message).slice(0,200)));
await page.goto('http://127.0.0.1:'+(process.env.PORT||'8765')+'/harness.html'+QS, { waitUntil:'load' });
await page.waitForFunction(() => window.HARNESS_READY === true, null, { timeout:90000 });
const items = await page.evaluate(() => window.EXPORT_ITEMS);
const idx = ONLY || items.map((_, i) => i);
const report = []; let fails = 0;
for (const i of idx) {
  let rep;
  try { rep = await page.evaluate(i => window.renderItem(i), i); }
  catch (e) { report.push({ ...items[i], error: String(e.message).slice(0,200), allImagesOk:false }); fails++; console.log(`[${i}] RENDER ERROR ${items[i].id}: ${e.message}`); continue; }
  const path = `${OUT}/${rep.folder}/${rep.id}.png`; mkdirSync(dirname(path), { recursive:true });
  await page.locator('#stage').screenshot({ path });
  const bad = [...rep.images.filter(r=>!r.ok), ...rep.backgrounds.filter(r=>!r.ok)];
  const ok = rep.allImagesOk && rep.fontsMissing.length === 0;
  if (!ok) fails++;
  report.push(rep);
  console.log(`[${String(i).padStart(3)}] ${ok?'ok ':'BAD'} ${rep.folder}/${rep.id} ${rep.w}x${rep.h} imgs=${rep.images.length}${rep.backgrounds.length?'+'+rep.backgrounds.length+'bg':''} fonts=[${rep.fontsUsed.map(f=>f.split('|')[0]).filter((v,i,a)=>a.indexOf(v)===i).join(', ')}]${rep.fontsUndeclared.length?' UNDECLARED='+rep.fontsUndeclared.join(','):''}${bad.length?' BAD_IMAGES='+JSON.stringify(bad):''}${rep.fontsMissing.length?' FONTS_MISSING='+rep.fontsMissing.join(','):''}`);
}
writeFileSync(`${OUT}/export-report.json`, JSON.stringify(report, null, 1));
console.log(`\nexported ${idx.length} items, ${fails} flagged; page errors: ${errs.length ? JSON.stringify(errs.slice(0,5)) : 'none'}`);
await browser.close();
