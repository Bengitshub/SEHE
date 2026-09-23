const { chromium } = await import(process.env.PW_PATH);
import { writeFileSync } from 'node:fs';
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
const page = await browser.newPage({ viewport:{width:1400,height:1600} });
await page.goto('http://127.0.0.1:8765/Download%20Ads%20(patched).html', { waitUntil:'load' });
await page.waitForFunction(() => typeof renderAndCapture === 'function' && window.htmlToImage, null, { timeout:60000 });
const r = await page.evaluate(async () => {
  const item = SECTIONS[2].items[0];  // MOF_Feed_1x1 / 1a-inclusions-editorial
  const blob = await renderAndCapture(item);
  const buf = new Uint8Array(await blob.arrayBuffer()); let s=''; for (let i=0;i<buf.length;i+=0x8000) s+=String.fromCharCode.apply(null, buf.subarray(i,i+0x8000));
  return { b64: btoa(s), v3: typeof V3, green: (window.V3||{}).green };
});
writeFileSync(process.env.OUT, Buffer.from(r.b64,'base64')); console.log('patched exporter: V3 is', r.v3, 'green =', r.green, '-> wrote', process.env.OUT);
await browser.close();
