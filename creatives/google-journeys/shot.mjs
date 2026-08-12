/* Render the ad pages to exact-size JPG/PNG. Run build.py first.
   Usage: node creatives/google-journeys/shot.mjs
   (set PW_PATH to a playwright-core entry file if it is not resolvable
   from this file's location, e.g. PW_PATH=file:///…/node_modules/playwright-core/index.mjs) */
const { chromium } = await import(process.env.PW_PATH || 'playwright-core');
import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const S = '/tmp/claude-0/-home-user-SEHE/0cc36833-90aa-502d-8b8c-c61310a548dd/scratchpad';
const IN = join(S, 'adpages');
const SIZES = { land: [1200, 628], sq: [1200, 1200], port: [960, 1200], '1x1': [1200, 1200], '4x1': [1200, 300] };

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
for (const f of readdirSync(IN).filter((x) => x.endsWith('.html'))) {
  const name = f.replace('.html', '');
  const key = Object.keys(SIZES).find((k) => name.endsWith(k));
  const [w, h] = SIZES[key];
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await ctx.route('**/*', (r) => (r.request().url().startsWith('file://') || r.request().url().startsWith('data:')) ? r.continue() : r.abort());
  const page = await ctx.newPage();
  await page.goto('file://' + join(IN, f), { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(700);
  const png = name.startsWith('logo');
  await page.screenshot({
    path: join(HERE, `sehe-journeys-${name}.${png ? 'png' : 'jpg'}`),
    ...(png ? {} : { type: 'jpeg', quality: 92 }),
  });
  console.log(`sehe-journeys-${name} ${w}x${h}`);
  await ctx.close();
}
await browser.close();
