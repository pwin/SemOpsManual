# Build tools

Produces the A4 print edition from the Markdown chapters.

```bash
cd tools
npm install
npx puppeteer browsers install chrome-headless-shell   # once
node build-pdf.mjs
```

Output lands in `build/SemOps-Manual-A4.pdf`, which is git-ignored — the PDF is
**published as a release asset, not committed**, so the repository does not gain
a ~3 MB binary on every revision.

To publish a new edition:

```bash
cp build/SemOps-Manual-A4.pdf build/SemOps-Manual-vX.Y.Z-A4.pdf
gh release create vX.Y.Z build/SemOps-Manual-vX.Y.Z-A4.pdf \
  --title "vX.Y.Z — The SemOps Manual" --notes-file NOTES.md --latest
```

Version the asset filename. A downloaded `SemOps-Manual-A4.pdf` is ambiguous
once a reader has two of them.

## What it does

| Stage | Script | What happens |
|---|---|---|
| 1 | `render-diagrams.mjs` | Every ```` ```mermaid ```` block → PNG at 3× scale, via headless Chromium |
| 2 | `build-pdf.mjs` | Chapters concatenated; logos, nav tables and the web contents page stripped; cross-references flattened; diagrams substituted at a computed mm width |
| 3 | `build-pdf.mjs` | Index generated from the source text |
| 4 | `build-pdf.mjs` | pandoc → typst → PDF |

## Prerequisites

| Tool | Why | Override |
|---|---|---|
| pandoc | Markdown → typst | `PANDOC` env var |
| typst | typst → PDF | `TYPST` env var |
| Chromium | Mermaid layout needs real text metrics | `CHROME_PATH` env var |

Neither pandoc's LaTeX path nor a browser print is used. LaTeX is a heavyweight
dependency for one document; a browser print cannot produce a table of contents
with page numbers, because CSS `target-counter` is unimplemented in Chromium.
typst does both, from a single ~25 MB binary.

## Files

| File | Purpose |
|---|---|
| `build-pdf.mjs` | The build |
| `render-diagrams.mjs` | Stage 1, also runnable alone |
| `typst-template.typ` | pandoc's default typst template, plus a `logo` variable |
| `template.typst` | pandoc's `conf` partial, patched — see below |

`template.typst` carries three fixes that the stock template needs for a
document like this:

- **Logo on the title page.** A `logo` parameter, rendered above the title.
- **Breakable figures.** pandoc wraps every table in a `#figure`, and figures do
  not break across pages by default — a long table orphaned its heading on the
  previous page and then printed rows on top of each other past the bottom
  margin.
- **Left-aligned tables.** The default centres cells and justifies inside them,
  which hyphenated short cells into things like "seman-tic versioning".

## Known rough edges

- **`--pdf-engine=typst` does not work here.** pandoc copies images to an
  absolute temp directory and typst rejects absolute drive-letter paths
  (`path contains invalid component "C:"`). The build writes `.typ` and invokes
  typst itself, which keeps image paths relative to `build/`.
- **The reader is `markdown-smart`, not `gfm`.** `gfm` does not offer
  `link_attributes`, so `![](x.png){width=90mm}` would not size anything.
  `-smart` keeps `--flag` literal in prose rather than folding the double hyphen
  into an en dash.
- **Diagram width is the binding print constraint.** See
  [Appendix A §A.9](../docs/diagram-style.md). The build warns above ~910 px.
