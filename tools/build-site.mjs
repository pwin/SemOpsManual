/**
 * Build the web edition of the SemOps Manual: one static HTML page per chapter,
 * for serving under https://www.semantechs.co.uk/SemOps_Manual/.
 *
 *   node tools/build-site.mjs [--out <dir>] [--skip-diagrams]
 *
 * Output defaults to build/site/. The pages are self-contained static files
 * with no third-party requests (one inline line collapses the contents on phones), so the directory can be copied
 * as-is into the website repository.
 *
 * Diagrams reuse the PNGs from render-diagrams.mjs (the same images as the
 * print edition), displayed at their natural CSS size so the 3x raster stays
 * sharp on high-DPI screens. --skip-diagrams reuses an existing render.
 */
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const REPO = path.resolve(path.dirname(new URL(import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, '$1'), '..');
const DIAGRAMS = path.join(REPO, 'build', 'diagrams');
const PANDOC = process.env.PANDOC || 'C:/Program Files/Pandoc/pandoc.exe';

const args = process.argv.slice(2);
const outArg = args.indexOf('--out');
const OUT = path.resolve(outArg >= 0 ? args[outArg + 1] : path.join(REPO, 'build', 'site'));
const SKIP_DIAGRAMS = args.includes('--skip-diagrams');

const SITE_HOME = '/';
const GITHUB = 'https://github.com/pwin/SemOpsManual';
const PDF = `${GITHUB}/releases/latest`;

/** Reading order, grouped by part. `page` is the output filename. */
const PARTS = [
  { title: null, chapters: [
    { file: 'README.md', page: 'index.html', label: '', short: 'Introduction' },
  ] },
  { title: 'Part I — Why this is hard', chapters: [
    { file: 'docs/01-the-business-case.md', label: '1' },
    { file: 'docs/02-people-and-cognition.md', label: '2' },
    { file: 'docs/03-across-the-boundary.md', label: '3' },
    { file: 'docs/04-from-research-to-industry.md', label: '4' },
    { file: 'docs/05-genai-and-agents.md', label: '5' },
  ] },
  { title: 'Part II — The SemOps frame', chapters: [
    { file: 'docs/06-stages-and-stories.md', label: '6' },
    { file: 'docs/07-the-toolchain.md', label: '7' },
  ] },
  { title: 'Part III — The practice', chapters: [
    { file: 'docs/08-model-and-validate.md', label: '8' },
    { file: 'docs/09-continuous-integration.md', label: '9' },
    { file: 'docs/10-ingest-and-transform.md', label: '10' },
    { file: 'docs/11-rules-and-inference.md', label: '11' },
    { file: 'docs/12-release-and-change.md', label: '12' },
    { file: 'docs/13-operate-and-consume.md', label: '13' },
  ] },
  { title: 'Part IV — The ledger', chapters: [
    { file: 'docs/14-coverage-and-gaps.md', label: '14' },
    { file: 'docs/15-adoption-roadmap.md', label: '15' },
    { file: 'docs/diagram-style.md', label: 'A' },
  ] },
];

const CHAPTERS = PARTS.flatMap((p) => p.chapters);
for (const ch of CHAPTERS) {
  ch.page ??= path.basename(ch.file).replace(/\.md$/, '.html');
  if (!ch.short) {
    const h1 = fs.readFileSync(path.join(REPO, ch.file), 'utf8').match(/^# (.+)$/m);
    ch.short = h1[1].replace(/^[\dA-Z]+\.\s+/, '').replace(/^Appendix [A-Z]\s*[—-]\s*/, '');
  }
}

// ---------------------------------------------------------------- markdown

function stripLogo(md) {
  return md.replace(/<p align="center">\s*<img[^>]*>\s*<\/p>\s*/g, '');
}

/** Remove the "| <- prev | next -> |" table at the foot of a chapter; the page supplies its own. */
function stripNav(md) {
  return md.replace(/\n---\n+\|[^\n]*\|\n\|[-\s|]+\|\n*$/g, '\n');
}

function prepareReadme(md) {
  // The centred title block becomes the page header.
  md = md.replace(/<h1 align="center">[\s\S]*?<\/p>\s*---\s*/, '');
  // The closing logo-and-strapline block duplicates the site footer. Cut at the
  // last centred block; a lazy regex would start at the logo at the very top.
  return md.slice(0, md.lastIndexOf('<p align="center">'));
}

function substituteDiagrams(md, rel, byKey) {
  let i = 0;
  return md.replace(/```mermaid\n[\s\S]*?```/g, () => {
    i += 1;
    const m = byKey.get(`${rel}#${i}`);
    if (!m) throw new Error(`no rendered diagram for ${rel} #${i} - run without --skip-diagrams`);
    return `\n<figure class="diagram"><img src="diagrams/${m.png}" width="${m.w}" height="${m.h}" alt="Diagram" loading="lazy"></figure>\n`;
  });
}

// ---------------------------------------------------------------- html

const PAGE_OF = new Map(CHAPTERS.map((c) => [path.basename(c.file), c.page]));

/**
 * Chapter links become links between pages. Links into files that exist only
 * in the repository (notebooks, tooling, licence) go to GitHub.
 */
function rewriteLinks(html) {
  return html.replace(/href="((?!https?:|mailto:|#)[^"]+)"/g, (whole, target) => {
    const [file, hash] = target.split('#');
    const clean = file.replace(/^(\.\.?\/)+/, '');
    const base = path.basename(clean);
    if (PAGE_OF.has(base)) return `href="${PAGE_OF.get(base)}${hash ? '#' + hash : ''}"`;
    const kind = clean.endsWith('/') ? 'tree' : 'blob';
    return `href="${GITHUB}/${kind}/main/${clean}${hash ? '#' + hash : ''}"`;
  });
}

function toHtml(md) {
  return execFileSync(PANDOC, ['-f', 'gfm', '-t', 'html5', '--syntax-highlighting=none', '--wrap=none'], {
    input: md,
    encoding: 'utf8',
    maxBuffer: 64 * 1024 * 1024,
  });
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function rail(current) {
  const items = PARTS.map((part) => {
    const links = part.chapters.map((c) => {
      const cur = c === current ? ' aria-current="page"' : '';
      return `<li><a href="${c.page}"${cur}><span class="n">${c.label}</span><span>${esc(c.short)}</span></a></li>`;
    }).join('\n');
    const head = part.title ? `<p class="part">${esc(part.title)}</p>` : '';
    return `${head}<ol>\n${links}\n</ol>`;
  }).join('\n');
  return items;
}

function pager(i) {
  const prev = CHAPTERS[i - 1];
  const next = CHAPTERS[i + 1];
  const cell = (c, dir) => c
    ? `<a class="${dir}" href="${c.page}"><small>${dir === 'prev' ? '&larr; Previous' : 'Next &rarr;'}</small>${c.label ? c.label + '. ' : ''}${esc(c.short)}</a>`
    : '<span></span>';
  return `<nav class="pager" aria-label="Chapters">${cell(prev, 'prev')}${cell(next, 'next')}</nav>`;
}

function page(ch, i, body) {
  const title = ch.label ? `${ch.label === 'A' ? 'Appendix A' : ch.label + '.'} ${ch.short} — The SemOps Manual` : 'The SemOps Manual';
  const hero = ch.label ? '' : `
    <header class="hero">
      <img src="semantechs-logo-320.png" alt="" width="96" height="96">
      <div>
        <h1>The SemOps Manual</h1>
        <p><em>Running a semantic practice the way you run software — people, process, and a toolchain that actually exists.</em></p>
      </div>
    </header>`;
  return `<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="The SemOps Manual: the operational discipline for building, deploying, governing and evolving semantic knowledge systems, connected stage by stage to toolchains that run today.">
<link rel="icon" href="semantechs-logo-320.png">
<link rel="stylesheet" href="manual.css">
</head>
<body>
<header class="topbar">
  <a class="home" href="${SITE_HOME}">&larr; Semantechs home</a>
  <a class="title" href="index.html"><img src="semantechs-logo-320.png" alt="" width="28" height="28">The SemOps Manual</a>
  <span class="links"><a href="${PDF}">A4 PDF</a><a href="${GITHUB}">GitHub</a></span>
</header>
<div class="shell">
  <details class="rail" open>
    <summary>Contents</summary>
    ${rail(ch)}
  </details>
  <script>if (matchMedia('(max-width: 900px)').matches) document.querySelector('.rail').removeAttribute('open');</script>
  <main>
    ${hero}
    <article>
${body}
    </article>
    ${pager(i)}
  </main>
</div>
<footer class="foot">
  <p>MIT — © 2026 Peter Winstanley · <a href="${SITE_HOME}">Semantechs Consulting Ltd</a> · The Semantechs mark is a trademark.</p>
</footer>
</body>
</html>
`;
}

// ---------------------------------------------------------------- build

if (!SKIP_DIAGRAMS) {
  console.log('[1/3] rendering diagrams');
  execFileSync(process.execPath, [path.join(REPO, 'tools', 'render-diagrams.mjs')], { stdio: 'inherit' });
}
const manifest = JSON.parse(fs.readFileSync(path.join(DIAGRAMS, 'manifest.json'), 'utf8'));
const byKey = new Map(manifest.map((m) => [`${m.rel}#${m.idx}`, m]));

console.log('[2/3] converting chapters');
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'diagrams'), { recursive: true });

CHAPTERS.forEach((ch, i) => {
  // A checkout with core.autocrlf has CRLF line endings; the patterns below expect LF.
  let md = fs.readFileSync(path.join(REPO, ch.file), 'utf8').replace(/\r\n/g, '\n');
  if (ch.file === 'README.md') md = prepareReadme(md);
  md = stripNav(stripLogo(md));
  md = substituteDiagrams(md, ch.file, byKey);
  const html = rewriteLinks(toHtml(md));
  fs.writeFileSync(path.join(OUT, ch.page), page(ch, i, html));
});

console.log('[3/3] copying assets');
for (const m of manifest) fs.copyFileSync(path.join(DIAGRAMS, m.png), path.join(OUT, 'diagrams', m.png));
fs.copyFileSync(path.join(REPO, 'assets', 'semantechs-logo-320.png'), path.join(OUT, 'semantechs-logo-320.png'));
fs.copyFileSync(path.join(REPO, 'tools', 'site.css'), path.join(OUT, 'manual.css'));

console.log(`      ${CHAPTERS.length} pages, ${manifest.length} diagrams -> ${OUT}`);
