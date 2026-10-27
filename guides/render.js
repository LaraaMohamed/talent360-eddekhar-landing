const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const dir = path.join(__dirname, 'out');
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    const p = await b.newPage();
    await p.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(dir, f.replace('.html', '.pdf')), format: 'A4', printBackground: true });
    await p.setViewportSize({ width: 794, height: 1123 });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')), fullPage: true });
    console.log(f, await p.evaluate(() => document.fonts.check('12px Almarai') + ' ' + document.fonts.check('12px Montserrat')));
  }
  await b.close();
})();
