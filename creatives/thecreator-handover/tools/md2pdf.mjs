const { chromium } = await import(process.env.PW_PATH);
const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
const page = await browser.newPage();
await page.goto('file://' + process.env.IN, { waitUntil:'load' });
await page.pdf({ path: process.env.OUT, format:'A4', printBackground:true, margin:{ top:'18mm', bottom:'18mm', left:'16mm', right:'16mm' } });
console.log('pdf written'); await browser.close();
