import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto('https://www.olx.pl/');

  const firstSpan = await page.$('span');

  if (firstSpan) {
    console.log(await firstSpan.evaluate(node => node.textContent));
  } else {
    console.log('No span element found.');
  }

  await browser.close();
})();