/**
 * Render every ```mermaid block in the manual to a high-DPI PNG.
 *
 * Mermaid computes its layout from real text metrics (SVGGraphicsElement.getBBox),
 * which no DOM shim provides accurately, so this drives a headless Chromium.
 * Output is rasterised rather than SVG so that diagram text never depends on the
 * PDF engine resolving the right webfont.
 *
 * Chromium is located in this order:
 *   1. $CHROME_PATH
 *   2. a chrome-headless-shell in the puppeteer cache (~/.cache/puppeteer)
 * If neither is present, run:  npx puppeteer browsers install chrome-headless-shell
 */
import fs from 'fs';
import os from 'os';
import path from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const TOOLS = path.dirname(new URL(import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, '$1');
const REPO = path.resolve(TOOLS, '..');
const OUT = path.join(REPO, 'build', 'diagrams');

const ORDER = [
  'README.md',
  'docs/01-the-business-case.md',
  'docs/02-people-and-cognition.md',
  'docs/03-across-the-boundary.md',
  'docs/04-from-research-to-industry.md',
  'docs/05-genai-and-agents.md',
  'docs/06-stages-and-stories.md',
  'docs/07-the-toolchain.md',
  'docs/08-model-and-validate.md',
  'docs/09-continuous-integration.md',
  'docs/10-ingest-and-transform.md',
  'docs/11-release-and-change.md',
  'docs/12-operate-and-consume.md',
  'docs/13-coverage-and-gaps.md',
  'docs/14-adoption-roadmap.md',
  'docs/diagram-style.md',
];

function findChromium() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const cache = path.join(os.homedir(), '.cache', 'puppeteer', 'chrome-headless-shell');
  if (fs.existsSync(cache)) {
    const versions = fs.readdirSync(cache).sort().reverse();
    for (const v of versions) {
      const exe = path.join(cache, v, `chrome-headless-shell-${v.split('-')[0]}`, 'chrome-headless-shell.exe');
      if (fs.existsSync(exe)) return exe;
      const nix = path.join(cache, v, `chrome-headless-shell-${v.split('-')[0]}`, 'chrome-headless-shell');
      if (fs.existsSync(nix)) return nix;
    }
  }
  return null;
}

const CHROME = findChromium();
if (!CHROME) {
  console.error('No Chromium found. Run:  npx puppeteer browsers install chrome-headless-shell');
  process.exit(1);
}
const MERMAID_JS = require.resolve('mermaid/dist/mermaid.min.js');
const puppeteer = (await import('puppeteer-core')).default;

fs.mkdirSync(OUT, { recursive: true });

const blocks = [];
for (const rel of ORDER) {
  const txt = fs.readFileSync(path.join(REPO, rel), 'utf8');
  const re = /```mermaid\n([\s\S]*?)```/g;
  let m, i = 0;
  while ((m = re.exec(txt))) {
    const slug = rel.replace(/^docs\//, '').replace(/\.md$/, '').replace(/[^a-z0-9]+/gi, '-');
    blocks.push({ rel, idx: ++i, id: `${slug}-${i}`, code: m[1] });
  }
}
console.log(`      rendering ${blocks.length} diagrams`);

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'shell',
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
});
const page = await browser.newPage();
// deviceScaleFactor 3 keeps diagram text crisp well past 300dpi once the image
// is placed into A4's ~170mm text block.
await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 3 });
await page.setContent(
  `<!doctype html><html><head><meta charset="utf-8"><style>
     html,body{margin:0;padding:0;background:#ffffff;}
     #c{display:inline-block;padding:6px;background:#ffffff;}
     #c svg{display:block;}
   </style></head><body><div id="c"></div></body></html>`,
  { waitUntil: 'load' }
);
await page.addScriptTag({ path: MERMAID_JS });
await page.evaluate(() => {
  window.mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    securityLevel: 'loose',
    flowchart: { htmlLabels: true, useMaxWidth: false },
  });
});

const manifest = [];
for (const b of blocks) {
  const res = await page.evaluate(async ({ code, id }) => {
    const el = document.getElementById('c');
    el.innerHTML = '';
    try {
      const { svg } = await window.mermaid.render('m_' + id.replace(/\W/g, '_'), code);
      el.innerHTML = svg;
      const s = el.querySelector('svg');
      // Mermaid emits a max-width style that would let the capture collapse to
      // the viewport width; pin the intrinsic viewBox size instead.
      const vb = s.getAttribute('viewBox').split(/[\s,]+/).map(Number);
      s.style.maxWidth = 'none';
      s.style.width = vb[2] + 'px';
      s.style.height = vb[3] + 'px';
      s.setAttribute('width', vb[2]);
      s.setAttribute('height', vb[3]);
      return { ok: true, w: Math.round(vb[2]), h: Math.round(vb[3]) };
    } catch (e) {
      return { ok: false, err: String((e && e.message) || e) };
    }
  }, { code: b.code, id: b.id });

  if (!res.ok) {
    console.error(`      FAIL ${b.id}: ${res.err}`);
    process.exitCode = 1;
    continue;
  }
  const file = path.join(OUT, `${b.id}.png`);
  await (await page.$('#c')).screenshot({ path: file });
  manifest.push({ ...b, png: `${b.id}.png`, w: res.w, h: res.h });
}

fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2));
await browser.close();
console.log(`      ${manifest.length} PNG written`);
