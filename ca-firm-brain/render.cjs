// Renders the poster to PNG (dark and light, 2x). Usage: node ca-firm-brain/render.cjs
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = __dirname;
  const pages = fs.readdirSync(dir).filter(f => /^\d\d-.*\.html$/.test(f));
  const browser = await chromium.launch();
  for (const f of pages) {
    for (const theme of ['dark', 'light']) {
      const page = await browser.newPage({ viewport: { width: 1700, height: 3200 }, deviceScaleFactor: 2 });
      await page.goto('file://' + path.join(dir, f));
      await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
      await page.waitForTimeout(1500);
      await page.evaluate(() => document.fonts.ready);
      const out = path.join(dir, f.replace('.html', theme === 'dark' ? '.png' : '-light.png'));
      await page.locator('#diagram').screenshot({ path: out });
      console.log('wrote', path.relative(process.cwd(), out));
      await page.close();
    }
  }
  await browser.close();
})();
