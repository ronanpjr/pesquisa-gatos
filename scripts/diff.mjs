#!/usr/bin/env node
/**
 * Renderiza o flyer em W_REF = 1024.5 px com deviceScaleFactor: 2 (largura final 2049 px),
 * fatia em faixas de 2049x1200 px e compara cada faixa com ref/strip-NN.png usando
 * `magick compare -metric AE -fuzz 6%`.
 */
import { chromium } from "playwright";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const URL = process.env.FLYER_URL || "http://127.0.0.1:8765/index.html";
const COMPARE_DIR = process.env.COMPARE_DIR || "docs/compare";

fs.mkdirSync("diff", { recursive: true });
fs.mkdirSync(COMPARE_DIR, { recursive: true });

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".png": "image/png",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1025, height: 1200 },
  deviceScaleFactor: 2,
  reducedMotion: "reduce",
});
const page = await context.newPage();

// Se o servidor HTTP local não estiver acessível (ex.: sandbox sem bind), serve do disco
await page.route("**/*", async (route) => {
  try {
    const u = new URL(route.request().url());
    const rel = decodeURIComponent(u.pathname === "/" ? "/index.html" : u.pathname);
    const file = path.join(ROOT, rel);
    if (fs.existsSync(file) && fs.statSync(file).isFile()) {
      const ext = path.extname(file).toLowerCase();
      await route.fulfill({
        status: 200,
         contentType: MIME[ext] || "application/octet-stream",
        body: fs.readFileSync(file),
      });
      return;
    }
  } catch {}
  await route.continue();
});

await page.goto(URL, { waitUntil: "networkidle" });

// Força o flyer a ocupar exatamente W_REF = 1024.5 px, sem moldura externa de desktop
await page.addStyleTag({
  content: `
    :root { --maxw: 1024.5px !important; }
    html, body { margin: 0 !important; padding: 0 !important; background: #faf1e8 !important; }
    .flyer {
      width: 1024.5px !important;
      max-width: 1024.5px !important;
      margin: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
    }
  `,
});

// Força carregamento de todas as imagens lazy e aguarda fontes + decodificação
await page.evaluate(async () => {
  document.documentElement.classList.add("pdf-ref-mode");
  for (const img of document.querySelectorAll("img")) {
    img.loading = "eager";
    try { await img.decode(); } catch {}
  }
  await document.fonts.ready;
});
await page.waitForTimeout(150);

const fullRaw = "diff/site-raw.png";
const fullPng = "diff/site-full.png";
await page.screenshot({ path: fullRaw, fullPage: true });
await browser.close();

// Recorta exatamente 2049 px de largura (2 * 1024.5)
spawnSync("magick", [fullRaw, "-crop", "2049x+0+0", "+repage", fullPng], { stdio: "inherit" });

for (const f of fs.readdirSync("diff")) {
  if (/^(site|strip)-\d+\.png$/.test(f)) fs.unlinkSync(path.join("diff", f));
}
spawnSync("magick", [fullPng, "-crop", "2049x1200", "+repage", "diff/site-%02d.png"], { stdio: "inherit" });

const refStrips = fs.readdirSync("ref").filter((f) => /^strip-\d+\.png$/.test(f)).sort();
const rows = [];
let totalPx = 0;
let totalDiff = 0;

console.log("\n| Faixa | y0–y1 (pt) | Pixels dif. | Total px | % dif. |");
console.log("|---|---:|---:|---:|---:|");

for (const rf of refStrips) {
  const idx = rf.match(/\d+/)[0];
  const refPath = path.join("ref", rf);
  const sitePath = path.join("diff", `site-${idx}.png`);
  const diffPath = path.join("diff", `strip-${idx}.png`);
  const cmpPath = path.join(COMPARE_DIR, `strip-${idx}.png`);

  const dimOut = spawnSync("magick", ["identify", "-format", "%w %h", refPath], { encoding: "utf8" }).stdout.trim();
  const [rw, rh] = dimOut.split(" ").map(Number);
  const pxCount = rw * rh;

  // Normaliza a faixa do site para as dimensões exatas da faixa de referência
  const normSite = `diff/site-norm-${idx}.png`;
  if (fs.existsSync(sitePath)) {
    spawnSync("magick", [sitePath, "-background", "#faf1e8", "-extent", `${rw}x${rh}`, normSite]);
  } else {
    spawnSync("magick", ["-size", `${rw}x${rh}`, "xc:#faf1e8", normSite]);
  }

  const cmp = spawnSync("magick", ["compare", "-metric", "AE", "-fuzz", "6%", refPath, normSite, diffPath], {
    encoding: "utf8",
  });
  const aeRaw = (cmp.stderr || cmp.stdout || "0").trim().split(/\s+/)[0];
  const ae = Number(aeRaw) || 0;
  const pct = (ae / pxCount) * 100;

  spawnSync("magick", [refPath, normSite, diffPath, "+append", cmpPath]);

  const y0 = Number(idx) * 600;
  const y1 = Math.min(9417, y0 + rh / 2);
  console.log(`| strip-${idx} | ${y0}–${y1} | ${ae} | ${pxCount} | ${pct.toFixed(2)}% |`);
  rows.push({ idx, y0, y1, ae, pxCount, pct: Number(pct.toFixed(2)) });
  totalPx += pxCount;
  totalDiff += ae;
}

const totalPct = ((totalDiff / totalPx) * 100).toFixed(2);
console.log(`| **Total** | **0–9417** | **${totalDiff}** | **${totalPx}** | **${totalPct}%** |\n`);
fs.writeFileSync("diff/summary.json", JSON.stringify({ totalDiff, totalPx, totalPct: Number(totalPct), rows }, null, 2));
