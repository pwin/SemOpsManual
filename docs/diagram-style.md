<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# Appendix A — Diagram and brand conventions

Every diagram in this manual is Mermaid, rendered natively by GitHub, and is
built to two hard constraints:

1. **Screen** — readable at GitHub's rendered document width without zooming.
2. **A4 print** — readable in portrait A4 (≈170 mm of usable width) after the
   browser scales the page to fit.

The second constraint is the binding one. A diagram that is comfortable on a
27-inch monitor routinely becomes unreadable at A4 because the whole SVG is
scaled down uniformly to fit the page width — halve the width and you halve the
type size. Everything below exists to stop that happening.

---

## A.1 The width rule

> **A diagram may be at most 5 nodes wide. Beyond that, go vertical.**

Mermaid lays a flowchart out along its declared direction and grows the SVG
until every node fits. There is no wrapping. A ten-stage `flowchart LR` becomes
a very wide, very short SVG; scaled into an A4 column it renders at roughly
7-point type and is functionally useless on paper.

The rule in practice:

| Nodes in the longest rank | Direction to use |
|---|---|
| 2–4 | `flowchart LR` is fine, and reads well |
| 5 | `LR` only if labels are short; otherwise `TD` |
| 6+ | `flowchart TD`, or split into two diagrams |

The nine-stage SemOps pipeline is never drawn as one nine-wide row anywhere in
this manual. It is drawn top-down, or split into three groups of three. That is
a deliberate consequence of this rule, not an accident of taste.

## A.2 The label rule

> **At most ~28 characters per label line. Break with `<br/>`, never rely on
> Mermaid to wrap — it does not.**

A single long label sets the width of its entire rank and drags the whole
diagram wider. Prefer:

```
A["Ontology PR gate<br/>checks --own-namespace"]
```

over:

```
A["Ontology PR gate running checks with the own-namespace filter"]
```

Subtitles and qualifiers belong in the prose under the diagram, not inside the
node. A diagram that needs a paragraph inside a box is a table in disguise.

## A.3 The size rule

> **Aim for 12 nodes. Hard-stop at 16.**

Past roughly sixteen boxes a reader stops tracing edges and starts scanning for
the one box they care about — at which point a table serves them better and
prints perfectly. Several places in this manual deliberately use a table where a
diagram would have been the flashier choice, for exactly this reason. See
[§A.7](#a7-when-not-to-draw-a-diagram).

## A.4 Colour: explicit fills, always

GitHub renders Mermaid against both a light and a dark page theme, and readers
print from either. A node with no explicit fill inherits a theme-dependent
background; a node with an explicit fill but no explicit text colour can end up
dark-on-dark.

> **Every styled node sets `fill`, `stroke`, and `color` together.**

Light fills with the dark navy text colour survive both themes, and print
legibly on a monochrome laser printer, where the palette collapses to greys of
visibly different densities.

### The palette

Sampled from the Semantechs mark in [`assets/`](../assets/):

| Role in a diagram | Stroke | Fill | Sampled from |
|---|---|---|---|
| **Authoring / human work** | `#FD5B1C` | `#FFE6DA` | turtle shell, upper field |
| **Automation / CI gates** | `#02B7D4` | `#D9F4FA` | the SPARQL hook |
| **Data and ingestion** | `#7CBA07` | `#ECF7D5` | turtle body |
| **Operations / runtime** | `#0CB88E` | `#D9F5EC` | lower-right field |
| **Governance / decision** | `#FE8902` | `#FFF0D6` | owl plumage |
| **Not covered by tooling** | `#8A93A0` | `#F1F3F5` | — (deliberately grey) |
| Text and edges | `#14243A` | — | outline ink |

Grey is reserved. It means "SemOps asks for this and the toolchain in this
manual does not provide it" — the visual counterpart of
[Chapter 14](14-coverage-and-gaps.md). Never use grey decoratively.

### The standard preamble

Copy this block verbatim into new diagrams:

```
%%{init: {'theme':'base','themeVariables':{
  'fontSize':'15px','fontFamily':'Segoe UI, Helvetica, Arial, sans-serif',
  'lineColor':'#14243A','primaryTextColor':'#14243A',
  'edgeLabelBackground':'#FFFFFF'}}}%%
```

`fontSize` is set at 15px rather than the 16px default because it holds a little
more text per rank at the same rendered width — which, per §A.1, is the scarce
resource. Do not go below 14px; the A4 downscale is unforgiving.

Then declare only the classes the diagram actually uses:

```
classDef human   fill:#FFE6DA,stroke:#FD5B1C,stroke-width:2px,color:#14243A;
classDef ci      fill:#D9F4FA,stroke:#02B7D4,stroke-width:2px,color:#14243A;
classDef data    fill:#ECF7D5,stroke:#7CBA07,stroke-width:2px,color:#14243A;
classDef ops     fill:#D9F5EC,stroke:#0CB88E,stroke-width:2px,color:#14243A;
classDef govern  fill:#FFF0D6,stroke:#FE8902,stroke-width:2px,color:#14243A;
classDef gap     fill:#F1F3F5,stroke:#8A93A0,stroke-width:2px,color:#14243A,stroke-dasharray:4 3;
```

The dashed border on `gap` carries the same meaning as the grey fill, so the
distinction survives both colour-blind readers and monochrome printing. No
meaning in this manual is ever carried by hue alone.

## A.5 Checking a diagram before committing

Three checks, in increasing order of effort:

1. **Count.** Longest rank ≤ 5, longest label line ≤ 28 characters, nodes ≤ 16.
2. **Screen.** Push to a branch and view the rendered Markdown on GitHub. Mermaid
   in a local editor preview does not always agree with GitHub's renderer.
3. **Print.** `Ctrl+P` from the GitHub page, A4 portrait, "Fit to page width",
   and read the smallest label. If you are squinting, apply §A.1 and split it.

Step 3 is the one people skip and the one that catches real problems.

## A.6 Accessibility

- Alt text on every raster image.
- No meaning carried by colour alone — pair every colour distinction with
  position, a border style, or a word in the label.
- Palette contrast: all six fills carry the `#14243A` text colour at a contrast
  ratio above 12:1, comfortably clear of the WCAG AA 4.5:1 threshold for body
  text.

## A.7 When not to draw a diagram

A diagram earns its place when it shows a **mechanism** — a flow, a gate, a
loop, a boundary crossing. It does not earn its place when it is:

- an unordered list of things (use a list);
- a mapping from one set to another (use a table — it also prints perfectly and
  is searchable, which an SVG is not);
- a sequence of commands (use a fenced code block).

[Chapter 14](14-coverage-and-gaps.md)'s coverage matrix is the clearest case:
six operating-model layers against two toolchains is a table, and would have
been a worse diagram.

---

## A.8 The mark

The Semantechs mark — turtle, owl, hook, `XML` — reads as a summary of the stack
this manual operates: **Turtle** the serialisation, **OWL** the ontology
language, the hook for **SPARQL**, and `XML` for the RDF/XML lineage that most
real-world vocabularies (FOAF among them, as
[Chapter 8](08-model-and-validate.md) shows) are still published in.

Full-resolution original: [`assets/semantechs-logo.png`](../assets/semantechs-logo.png)
(1024×1024). Use [`assets/semantechs-logo-320.png`](../assets/semantechs-logo-320.png)
for in-page headers — at 320 px it is a tenth of the file size and no page in
this manual displays the mark above 160 px.

---

## A.9 The print edition

`tools/build-pdf.mjs` produces the A4 PDF. It renders every Mermaid block to a
PNG through a headless Chromium, assembles the chapters into one Markdown file,
generates the index, and runs pandoc → typst.

```bash
cd tools && npm install && npx puppeteer browsers install chrome-headless-shell
node build-pdf.mjs
```

Four things learned building it are worth knowing before you add a diagram.

**Mermaid needs a real browser.** Its layout comes from actual text metrics
(`getBBox`), which no DOM shim supplies accurately. A jsdom-based render produces
boxes of the wrong size. Diagrams are rasterised at `deviceScaleFactor: 3` rather
than passed through as SVG, so their text never depends on the PDF engine
resolving the right webfont.

**The width rule has a hard number in print.** A diagram is placed into the
~170 mm text block, so a diagram *W* pixels wide renders its 15px labels at
`15 / W × 170` mm. Keeping labels at or above 8pt means:

> **W ≤ ~910 px.** The build prints a warning for any diagram over that.

Two diagrams originally breached it — both because side-by-side subgraphs, not
node count, set the width. §A.1's "5 nodes per rank" rule does not constrain
subgraphs, so check the rendered pixel width, not just the node count.

**Force subgraphs to stack with invisible links.** Mermaid places unconnected
subgraphs side by side, which is what blew the width budget. An invisible link
stacks them vertically and improves the web rendering too:

```
PEER ~~~ CHAIN ~~~ OPEN
```

**Beware cycles.** A feedback edge drawn straight back to the first node makes
Mermaid's layout break the cycle by hoisting the *last* group to the top — the
nine-stage pipeline rendered as Run/Author/Ship until the loop was redrawn as a
terminal node. If a diagram's vertical order looks wrong, a back edge is why.

---

| ← [15. Adoption roadmap](15-adoption-roadmap.md) | [Contents](../README.md) |
|---|---|
