import puppeteer from 'puppeteer';

export async function getSpotifyDownloadLink(url) {
  if (!url) return null;

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    headless: true,
  });

  try {
    const page = await browser.newPage();
    await page.goto('https://spotidownloader.com/en', { waitUntil: 'domcontentloaded', timeout: 0 });

    await page.waitForSelector('input[name="url"]');
    await page.type('input[name="url"]', url);

    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' }),
    ]);

    await page.waitForSelector('.button.is-success.is-fullwidth', { timeout: 15000 });

    const downloadUrl = await page.$eval('.button.is-success.is-fullwidth', el => el.href);

    return downloadUrl;
  } catch (err) {
    console.error('Scraping failed:', err.message);
    return null;
  } finally {
    await browser.close();
  }
}
