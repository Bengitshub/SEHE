// Reproduce the ORIGINAL exporter's failure using its own code path (html-to-image on the offscreen #stage),
// then isolate the cause with two variants. Nothing in Download Ads.html is modified except dependency URLs.
const { chromium } = await import(process.env.PW_PATH);
import { writeFileSync } from 'node:fs';
const OUT = process.env.OUT;
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
const page = await browser.newPage({ viewport:{ width:1400, height:1600 }, deviceScaleFactor:1 });
const errs=[]; page.on('pageerror', e=>errs.push(String(e.message).slice(0,160))); page.on('console', m=>{ if(m.type()==='error') errs.push('console: '+m.text().slice(0,160)); });
await page.goto('http://127.0.0.1:8765/Download%20Ads.html', { waitUntil:'load' });
await page.waitForFunction(() => typeof renderAndCapture === 'function' && typeof SECTIONS !== 'undefined' && window.htmlToImage, null, { timeout:60000 });
const sectionCount = await page.evaluate(() => SECTIONS.map(s => s.key+':'+s.items.length));
console.log('original exporter sections:', sectionCount.join(' | '));
const blobToB64 = `async b => { const buf = await b.arrayBuffer(); let s=''; const u=new Uint8Array(buf); for (let i=0;i<u.length;i+=0x8000) s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000)); return btoa(s); }`;
async function capture(label, overrideStyle) {
  const b64 = await page.evaluate(async ([ov, conv]) => {
    const item = SECTIONS[0].items[0];                     // 01-best-scenic-rail, 1080x1080
    const stage = document.getElementById('stage');
    stage.style.width = item.w+'px'; stage.style.height = item.h+'px';
    if (!window.__root) window.__root = ReactDOM.createRoot(stage);
    window.__root.render(React.createElement(item.C));
    await document.fonts.ready; await new Promise(r=>setTimeout(r,450));
    const imgs = stage.querySelectorAll('img');
    await Promise.all([...imgs].map(img => img.complete ? Promise.resolve() : new Promise(r => { img.onload = img.onerror = r; })));
    await new Promise(r=>setTimeout(r,250));
    const opts = { width:item.w, height:item.h, pixelRatio:1, cacheBust:false };
    if (ov) opts.style = ov;
    const blob = await window.htmlToImage.toBlob(stage, opts);
    const stageRect = stage.getBoundingClientRect();
    return { b64: await (eval(conv))(blob), stageLeft: stageRect.left, imgs: imgs.length };
  }, [overrideStyle || null, blobToB64]);
  writeFileSync(`${OUT}/repro-${label}.png`, Buffer.from(b64.b64, 'base64'));
  console.log(`captured ${label}: stage computed left=${b64.stageLeft}px, imgs in creative=${b64.imgs}`);
}
await capture('A-as-is', null);
await capture('B-left0-only', { left:'0' });
await capture('C-full-override', { position:'static', left:'0', top:'0' });
console.log('page errors:', errs.length ? errs.slice(0,5) : 'none');
await browser.close();
