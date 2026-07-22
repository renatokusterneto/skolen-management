const { chromium } = require('../logo-animation/node_modules/playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 1080 });

  const files = [
    'skolen-b2b.html',
    'skolen-callout.html',
    'skolen-transform.html',
    'skolen-badge.html',
  ];

  const dir = path.join(__dirname, 'testes');

  for (const f of files) {
    const src = path.join(dir, f);
    const out = path.join(dir, f.replace('.html', '.png'));
    const url = 'file:///' + src.replace(/\\/g, '/');
    await page.goto(url);
    await page.waitForTimeout(600);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: 1080 } });
    console.log('rendered:', f);
  }

  await browser.close();
  console.log('done');
})();
