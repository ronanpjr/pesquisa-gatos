import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const WIDTHS = [320, 360, 390, 430, 768, 1280];
const OUT_DIR = path.join(process.cwd(), "docs", "responsive");
fs.mkdirSync(OUT_DIR, { recursive: true });

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".png": "image/png",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

const browser = await chromium.launch({ headless: true });
const report = [];

for (const w of WIDTHS) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: 2 });
  await page.route("http://flyer.local/**", async (route) => {
    const u = new URL(route.request().url());
    let reqPath = decodeURIComponent(u.pathname);
    if (reqPath === "/") reqPath = "/index.html";
    const filePath = path.join(process.cwd(), reqPath);
    const ext = path.extname(filePath).toLowerCase();
    await route.fulfill({
      status: 200,
      contentType: MIME[ext] || "application/octet-stream",
      body: fs.readFileSync(filePath),
    });
  });

  await page.goto("http://flyer.local/", { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    for (const img of document.querySelectorAll("img")) {
      img.loading = "eager";
      await img.decode().catch(() => {});
    }
    await document.fonts.ready;
  });

  const check = await page.evaluate(() => {
    const docOverflow = document.documentElement.scrollWidth > window.innerWidth;
    const flyer = document.querySelector(".flyer");
    const flyerRect = flyer.getBoundingClientRect();
    return {
      innerWidth: window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      docOverflow,
      flyerWidth: Math.round(flyerRect.width * 10) / 10,
      flyerLeft: Math.round(flyerRect.left * 10) / 10,
    };
  });

  const shotPath = path.join(OUT_DIR, `site-${w}.png`);
  await page.screenshot({ path: shotPath, fullPage: true });
  await page.close();
  report.push(check);
}

await browser.close();
console.table(report);
fs.writeFileSync(path.join(OUT_DIR, "summary.json"), JSON.stringify(report, null, 2));
