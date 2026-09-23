const { chromium } = await import(process.env.PW_PATH);
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
for (const [label, url, ready] of [
  ['ORIGINAL Download Ads.html', 'http://127.0.0.1:8765/Download%20Ads.html', 'typeof renderAndCapture === "function"'],
  ['replacement harness.html',   'http://127.0.0.1:8765/harness.html',        'window.HARNESS_READY === true'],
  ['ORIGINAL index.html (canvas)','http://127.0.0.1:8765/index.html',          'document.querySelector("#root *") !== null'],
]) {
  const page = await browser.newPage({ viewport:{width:1200,height:900} });
  await page.goto(url, { waitUntil:'load' }); await page.waitForFunction(ready, null, { timeout:90000 }); await page.waitForTimeout(800);
  const r = await page.evaluate(() => ({ type: typeof V3, isArray: Array.isArray(V3), green: (typeof V3==='object' && V3) ? V3.green : undefined, navyDeep: (typeof V3==='object' && V3) ? V3.navyDeep : undefined, keys: (typeof V3==='object' && V3 && !Array.isArray(V3)) ? Object.keys(V3).join(',') : (Array.isArray(V3) ? 'array len '+V3.length : '-') }));
  console.log(`${label.padEnd(30)} V3 -> ${r.isArray ? 'ARRAY (the exporter id list) — TOKENS CLOBBERED' : 'object: '+r.keys}  green=${r.green} navyDeep=${r.navyDeep}`);
  await page.close();
}
await browser.close();
