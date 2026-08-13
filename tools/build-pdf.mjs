/**
 * Build the A4 print edition of the SemOps Manual.
 *
 *   node tools/build-pdf.mjs
 *
 * Two stages:
 *   1. render  - each ```mermaid block is rendered to a high-DPI PNG by a
 *                headless Chromium, because Mermaid needs real text metrics
 *                (getBBox) that a DOM shim cannot supply.
 *   2. assemble - the chapters are concatenated into one print-ready Markdown
 *                file (nav furniture stripped, cross-references flattened,
 *                diagrams substituted), an index is generated, and pandoc
 *                renders it to PDF through typst.
 *
 * Prerequisites are checked at startup and reported precisely if missing.
 */
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const REPO = path.resolve(path.dirname(new URL(import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, '$1'), '..');
const BUILD = path.join(REPO, 'build');
const DIAGRAMS = path.join(BUILD, 'diagrams');

const PANDOC = process.env.PANDOC || 'C:/Program Files/Pandoc/pandoc.exe';
const TYPST = process.env.TYPST || 'C:/Users/Pedro/AppData/Local/Temp/typst-x86_64-pc-windows-msvc/typst.exe';

/** Reading order. The label is what the index and page headers refer to. */
const ORDER = [
  { file: 'README.md',                        label: 'Introduction', title: 'Introduction' },
  { file: 'docs/01-the-business-case.md',     label: '1' },
  { file: 'docs/02-people-and-cognition.md',  label: '2' },
  { file: 'docs/03-across-the-boundary.md',   label: '3' },
  { file: 'docs/04-from-research-to-industry.md', label: '4' },
  { file: 'docs/05-genai-and-agents.md',      label: '5' },
  { file: 'docs/06-stages-and-stories.md',    label: '6' },
  { file: 'docs/07-the-toolchain.md',         label: '7' },
  { file: 'docs/08-model-and-validate.md',    label: '8' },
  { file: 'docs/09-continuous-integration.md', label: '9' },
  { file: 'docs/10-ingest-and-transform.md',  label: '10' },
  { file: 'docs/11-release-and-change.md',    label: '11' },
  { file: 'docs/12-operate-and-consume.md',   label: '12' },
  { file: 'docs/13-coverage-and-gaps.md',     label: '13' },
  { file: 'docs/14-adoption-roadmap.md',      label: '14' },
  { file: 'docs/diagram-style.md',            label: 'A' },
];

// ---------------------------------------------------------------- helpers

/** Text-block width of the A4 page, given 2cm side margins. */
const TEXT_WIDTH_MM = 210 - 2 * 20;

/**
 * Widest a diagram may be before its 15px labels fall below ~8pt on the page.
 * 15px / W * TEXT_WIDTH_MM >= 2.8mm  =>  W <= ~910px.
 */
const MAX_DIAGRAM_PX = 910;

function stripLogo(md) {
  return md.replace(/<p align="center">\s*<img[^>]*>\s*<\/p>\s*/g, '');
}

/** Remove the "| <- prev | next -> |" navigation table at the foot of a chapter. */
function stripNav(md) {
  return md.replace(/\n---\n+\|[^\n]*\|\n\|[-\s|]+\|\n*$/g, '\n');
}

/** Flatten intra-manual links to their text; leave real URLs alone. */
function flattenLinks(md) {
  return md.replace(/\[([^\]]+)\]\(((?!https?:|mailto:)[^)]+)\)/g, '$1');
}

function pageBreak() {
  return '\n\n```{=typst}\n#pagebreak(weak: true)\n```\n\n';
}

// ---------------------------------------------------------------- stage 1

function renderDiagrams() {
  console.log('[1/4] rendering diagrams');
  execFileSync(process.execPath, [path.join(REPO, 'tools', 'render-diagrams.mjs')], {
    stdio: 'inherit',
  });
}

// ---------------------------------------------------------------- stage 2

function assemble() {
  console.log('[2/4] assembling print-ready Markdown');
  const manifest = JSON.parse(fs.readFileSync(path.join(DIAGRAMS, 'manifest.json'), 'utf8'));
  const byKey = new Map(manifest.map((m) => [`${m.rel}#${m.idx}`, m]));

  const chapters = [];
  let oversize = 0;

  for (const entry of ORDER) {
    let md = fs.readFileSync(path.join(REPO, entry.file), 'utf8');
    md = stripLogo(md);
    md = stripNav(md);

    if (entry.file === 'README.md') {
      // The web README is the table of contents. In print, the generated
      // outline does that job, so keep only the framing material.
      md = md
        .replace(/<h1 align="center">[\s\S]*?<\/p>\s*---\s*/, '')
        // "Read it on paper" points at this very document; drop it in print.
        .replace(/## Read it on paper[\s\S]*?(?=## Contents)/, '')
        .replace(/## Contents[\s\S]*?(?=## How to read it)/, '')
        .replace(/<p align="center">[\s\S]*?<\/p>\s*$/, '');
      md = `# ${entry.title}\n\n${md.replace(/^##\s+What this is/m, '## What this is')}`;
    }

    // Substitute rendered diagrams, sized so they never exceed the text block.
    let i = 0;
    md = md.replace(/```mermaid\n[\s\S]*?```/g, () => {
      i += 1;
      const m = byKey.get(`${entry.file}#${i}`);
      if (!m) throw new Error(`no rendered diagram for ${entry.file} #${i}`);
      if (m.w > MAX_DIAGRAM_PX) {
        console.log(`      ! ${m.id} is ${m.w}px wide (> ${MAX_DIAGRAM_PX}px): labels will print small`);
        oversize += 1;
      }
      const naturalMm = (m.w * 25.4) / 96;
      const widthMm = Math.min(TEXT_WIDTH_MM, Math.round(naturalMm));
      const rel = `diagrams/${m.png}`;
      return `![](${rel}){width=${widthMm}mm}`;
    });

    md = flattenLinks(md);
    chapters.push({ ...entry, md: md.trim() });
  }

  if (oversize) console.log(`      ${oversize} diagram(s) over the width budget`);
  return chapters;
}

// ---------------------------------------------------------------- stage 3

/**
 * Build an alphabetical index of the things a reader looks up: subcommands,
 * flags, and check identifiers. Entries reference chapters, which is honest --
 * they are resolved from the source, not from final pagination.
 */
function buildIndex(chapters) {
  console.log('[3/4] generating index');
  // Distinctive names can be indexed wherever they appear as inline code.
  // Ambiguous ones are ordinary English ("data", "run", "checks") and are only
  // indexed at a real invocation, or they match in every chapter and the entry
  // stops pointing anywhere useful.
  const DISTINCTIVE = ['docgen', 'triplify', 'sketch', 'version-diff', 'consistency-remote', 'pattern-consistency'];
  const AMBIGUOUS = ['ontology', 'checks', 'data', 'run', 'consistency'];
  const SUBCOMMANDS = [...DISTINCTIVE, ...AMBIGUOUS];
  const VSCODE = [
    'New Ontology', 'Add Class', 'Add Subclass', 'Add Sibling Class',
    'Run Local Checks', 'Run Deep Validation', 'Run Full Triplify',
    'Query Workbench', 'Visualize Subject Graph', 'Show Metrics & DL Expressivity',
    'Infer Ontology + Query from CSV', 'Run Ontology Script',
  ];

  const hits = new Map(); // term -> {kind, chapters:Set}
  const add = (term, kind, label) => {
    if (!hits.has(term)) hits.set(term, { kind, chapters: new Set() });
    hits.get(term).chapters.add(label);
  };

  for (const ch of chapters) {
    const body = ch.md;

    for (const f of body.match(/--[a-z][a-z0-9-]{2,}/g) || []) add(f, 'flag', ch.label);
    for (const c of body.match(/\b[A-Z]{3}-\d{3}\b/g) || []) add(c, 'check', ch.label);

    for (const s of SUBCOMMANDS) {
      const esc = s.replace(/-/g, '\\-');
      // A real invocation: "ontology-quality-suite checks" / "ontology_suite checks".
      const invoked = new RegExp(`(ontology-quality-suite|ontology_suite)\\s+${esc}\\b`).test(body);
      // Or, for the distinctive names only, a bare inline-code mention.
      const mentioned = DISTINCTIVE.includes(s) && new RegExp('`' + esc + '`').test(body);
      if (invoked || mentioned) add(s, 'command', ch.label);
    }
    for (const v of VSCODE) {
      if (body.includes(v)) add(`${v} (VS Code)`, 'vscode', ch.label);
    }
  }

  const order = { command: 0, flag: 1, check: 2, vscode: 3 };
  const sortKey = (t) => t.replace(/^-+/, '').toLowerCase();
  const rows = [...hits.entries()]
    .sort((a, b) => sortKey(a[0]).localeCompare(sortKey(b[0])) || order[a[1].kind] - order[b[1].kind]);

  const chapterSort = (a, b) => {
    const rank = (x) => (x === 'Introduction' ? -1 : x === 'A' ? 999 : Number(x));
    return rank(a) - rank(b);
  };

  const group = (kind, heading, note) => {
    const sel = rows.filter(([, v]) => v.kind === kind);
    if (!sel.length) return '';
    let out = `\n### ${heading}\n\n${note ? note + '\n\n' : ''}| Entry | Chapters |\n|---|---|\n`;
    for (const [term, v] of sel) {
      const chs = [...v.chapters].sort(chapterSort).join(', ');
      out += `| \`${term}\` | ${chs} |\n`;
    }
    return out;
  };

  let out = `# Index\n\nEntries reference **chapters**, not pages — they are resolved from the
source text, so they stay correct as the manual is revised. Use the outline at
the front for page numbers.\n`;

  out += group('command', 'Commands', '`ontology-quality-suite <command>`, or `python -m ontology_suite <command>`.');
  out += group('flag', 'Flags and options');
  out += group('check', 'Check identifiers');

  const vs = rows.filter(([, v]) => v.kind === 'vscode');
  if (vs.length) {
    out += `\n### VS Code commands\n\n| Command | Chapters |\n|---|---|\n`;
    for (const [term, v] of vs) {
      out += `| ${term.replace(' (VS Code)', '')} | ${[...v.chapters].sort(chapterSort).join(', ')} |\n`;
    }
  }

  console.log(`      ${rows.length} index entries`);
  return out;
}

// ---------------------------------------------------------------- stage 4

function writeAndRender(chapters, indexMd) {
  const date = new Date().toISOString().slice(0, 10);
  const meta = `---
title: "The SemOps Manual"
subtitle: "Running a semantic practice the way you run software"
author: "Peter Winstanley"
date: "${date}"
papersize: a4
margin:
  x: 20mm
  y: 20mm
mainfont: "Cambria"
codefont: "Consolas"
fontsize: 10pt
linestretch: 1.1
linkcolor: "#1a5f7a"
logo: "logo.png"
toc-depth: 2
---

`;

  const body = chapters.map((c) => c.md).join(pageBreak()) + pageBreak() + indexMd;
  const mdPath = path.join(BUILD, 'semops-manual.md');
  fs.writeFileSync(mdPath, meta + body, 'utf8');

  // typst refuses paths outside --root, so the mark is copied in rather than
  // referenced at ../assets.
  fs.copyFileSync(path.join(REPO, 'assets', 'semantechs-logo-320.png'), path.join(BUILD, 'logo.png'));

  console.log('[4/4] rendering PDF via pandoc + typst');
  const pdfPath = path.join(BUILD, 'SemOps-Manual-A4.pdf');

  // Two steps rather than --pdf-engine: pandoc's own PDF path copies images to
  // an absolute temp directory, and typst rejects absolute drive-letter paths
  // ("path contains invalid component `C:`"). Writing .typ keeps the image
  // references relative to build/, which typst accepts with --root.
  execFileSync(PANDOC, [
    'semops-manual.md',
    // pandoc's own markdown, not gfm: gfm does not offer link_attributes, which
    // is what sizes ![](x.png){width=90mm}. -smart keeps "--flag" literal in
    // prose instead of folding the double hyphen into an en dash.
    '--from', 'markdown-smart',
    '--to', 'typst',
    '--standalone',
    '--toc',
    '--template', path.join(REPO, 'tools', 'typst-template.typ'),
    '-o', 'semops-manual.typ',
  ], { cwd: BUILD, stdio: 'inherit' });

  // Centre diagrams. pandoc emits them as inline #box(image(...)), which sits
  // hard against the left margin; there is no metadata switch for this.
  const typPath = path.join(BUILD, 'semops-manual.typ');
  const typ = fs.readFileSync(typPath, 'utf8')
    .replace(/#box\(image\((.*?)\)\)/g, '#align(center, image($1))');
  fs.writeFileSync(typPath, typ, 'utf8');

  execFileSync(TYPST, ['compile', '--root', '.', 'semops-manual.typ', pdfPath], {
    cwd: BUILD,
    stdio: 'inherit',
  });

  const mb = (fs.statSync(pdfPath).size / 1024 / 1024).toFixed(2);
  console.log(`\nwrote ${path.relative(REPO, pdfPath)} (${mb} MB)`);
  return pdfPath;
}

// ---------------------------------------------------------------- main

for (const [what, p] of [['pandoc', PANDOC], ['typst', TYPST]]) {
  if (!fs.existsSync(p)) {
    console.error(`missing ${what}: ${p}\nSet the ${what.toUpperCase()} environment variable to override.`);
    process.exit(1);
  }
}

fs.mkdirSync(BUILD, { recursive: true });
if (!process.argv.includes('--skip-render')) renderDiagrams();
const chapters = assemble();
const indexMd = buildIndex(chapters);
writeAndRender(chapters, indexMd);
