<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# The SemOps Manual — Evidence

This document backs the [SemOps Manual](../README.md) claim by claim. For every
statement the manual makes that can be checked, it gives the command or code that
checks it, the input data, the output as recorded, and what the output was tested
for. It is generated, by [`verify.py`](verify.py), from the claims in
[`claims/`](claims/) and the recorded runs in [`outputs/`](outputs/), so it can be
regenerated rather than trusted.

There are two ways to read it.

- **From the manual.** The [annotated edition](manual/README.md) is the manual, word
  for word, with an *Evidence* line after each paragraph that makes a checked
  claim. Follow the line to the claim's entry here, and the entry's first link
  takes you back to the same paragraph.
- **From here.** The summary below lists every claim by chapter, with its result.

## Three kinds of claim

| Kind | What it means here |
|---|---|
| **Reproduced here** | The commands below reproduce it, from this folder, with the published packages and release binaries. The harness runs them and checks the output; the result is PASS or FAIL, with the date of the run. |
| **Cited from upstream** | It rests on something in one of the toolchain's own repositories (a commit, a file, a test, a release), linked at a fixed commit so the link cannot drift. Where a quotation is given, `verify.py` checks it against a local clone: the words must appear in that commit's message, or in that file at the cited lines. |
| **Argument** | A judgement, a recommendation, or a reading of the literature. Nothing can be run to prove it; the entry says what it rests on, so you can disagree with it on its merits. |

Some claims appear in more than one chapter (479 findings unscoped against 23
scoped is in four). Those entries point at the one claim that reproduces them,
rather than running the same thing four times.

## Reproduce it yourself

From the `evidence/` folder, on Linux, macOS or Windows (Git Bash or PowerShell):

```bash
python -m venv .venv                      # Python 3.11 or later
.venv/bin/pip install -r requirements.txt # Windows: .venv\Scripts\pip ...
python tools/fetch_binaries.py            # shacl, tarka, holos + holos-server, checksum-verified
npm ci                                    # the DSL, the WebAssembly engines, TypeScript
.venv/bin/python verify.py                # run every claim this machine can, then rebuild this file
```

`python verify.py --list` shows which claims your machine can run, and why not if
not; `--only 'C09.*'` runs one chapter; `--render` rebuilds this document from the
recorded outputs without running anything. A claim that cannot run on your
machine keeps its last recorded result, marked with its date.

Paths in the recorded outputs are rewritten (`.` for this folder, `<tmp>` for the
temporary directory, `~` for your home) so they compare across machines. Timings
are recorded but never asserted.

**Which versions.** The packages are installed as a reader would install them,
from PyPI and npm, not from any repository's lock file. So holosdb resolves to
0.25.0 and shacl to 0.3.4 here. At suite 0.24.3 those are also what the suite's
own `uv.lock` holds; at 0.22.0 it held holosdb 0.15.0 (C07.17), which is why the
lock is not what this reads. Where a release changed what a claim should see, the claim checks the
installed version and says which side of the change it ran on: suite 0.23.0
(C07.05, C07.26, C07.27, C08.19, C10.18, C10.29, C10.30, C14.21, C14.39), suite
0.24.0 (C10.18, C10.19), 0.24.1 (C13.03), and 0.24.2 and 0.24.3 (C07.05); the
engine's CLI at 0.3.4 (C11.07); HOLOS 0.21.1 (C13.10), 0.22.0 (C11.29, C13.10) and
0.23.0 (C13.10); and the DSL at 0.16.1 (C08.15, C08.16).

**What the machine needs.** Python 3.11 or later and Node 20 or later; the binaries
come from `tools/fetch_binaries.py`. A Java runtime, for the claims in which HermiT
runs (C08.19, C09.14, C10.18, C14.06, C14.39); without one they fail, which is
itself C14.09's point. Network access for C02.03, which downloads gist. Port 7899
free on 127.0.0.1, where the live-store claims start `holos-server`.

**Three environment variables matter.**

- `PYTHONHASHSEED` decides, almost entirely, whether owlready2 can load FOAF for
  the DL reasoner, and decides the order of `docgen`'s page (C14.06, C14.08,
  C13.12). The harness leaves it unset except where a claim sets it, exactly as a
  reader's shell would. Even pinned, about one run in ten under seed 0 goes the
  other way (C14.08 measures it), so the claims that need the reasoner *not* to
  run hide Java instead, which is certain, and the claims that need it to run use
  seed 5, which ran in every recorded attempt.
- `EVIDENCE_TESTING_REPO`, set to a checkout of the
  [testing repository](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing)
  at `7deaf86`, lets C09.15 and C09.16 run its test suite and competency board.
  Use a clone you do not mind it writing into: both rewrite generated files. That
  repository installs the suite from a sibling checkout,
  `../consolidated_ontology_suite_python` (at `v0.24.3` for the recorded run), and
  its competency tests triplify with oxi-gen, which the suite finds through
  `ONTOLOGY_SUITE_OXI_GEN_BIN`. If the clone lives in a temporary folder, make it
  with `git clone --no-local`: a local clone hardlinks the object files, which
  keep their old dates, and a temp-folder cleaner will take them.
- `EVIDENCE_REPOS`, the folder holding local clones of the six repositories
  (default: the folder above the manual), lets `verify.py` check the quoted
  sources. These are read for their history only, and never written to. `verify.py --sources` checks them without running anything else.

## What building this changed in the manual

Writing a check for every claim found claims that did not survive it. Each was
corrected in the manual before this document was generated, and each correction
has its own entry:

| Was | Now | Evidence |
|---|---|---|
| HermiT's outcome is fixed by the hash seed, "every time" | Nine runs in ten; something besides the seed decides the rest, not yet identified | [C14.06](#c14-06), [C14.08](#c14-08) |
| `REA-020`, the ontology is inconsistent, is a third confirmation of the contradiction | The ontology is consistent; `REA-020` is an artefact of how the bridge reads owlready2 | [C14.39](#c14-39) |
| `--inference owlrl` is refused | Refused under the default engine; accepted and ignored under `--engine sparql` | [C07.27](#c07-27) |
| A `CONCAT`-built IRI becomes a string literal while the counts look right | Only as an object; as a subject every triple on it is dropped | [C10.05](#c10-05) |
| Every `STR-006`/`DAT-002` is a missing department | Half are, half are `mailto:` mailboxes | [C10.20](#c10-20) |
| `UNMAPPED` findings lose title, severity and remediation | They keep severity and message, and lose the check id, title and remediation | [C08.24](#c08-24) |
| Rules arrived CLI-first at 0.1.7, and 0.1.9 fixed `$this` | Released in 0.1.8 in every binding, with the fix | [C11.03](#c11-03) |
| `native`, `native+sparql`, `sparql` take 2.8, 3.6 and 4.1 s | 1.7, 2.2 and 2.0 s, on the current engines | [C07.23](#c07-23) |
| The suite's lock went stale at holosdb 0.14.3 | The suite's own 0.14.3; the 0.22.0 release locked holosdb at 0.15.0 | [C07.17](#c07-17) |

And it found things the manual had not said at all, now in Chapter 14's ledger:
the merged sketch reading every mapping with the first file's prefixes
([C10.29](#c10-29)), HOLOS validation writing the shapes into the store it
validates and leaving them there, fixed in HOLOS 0.21.1 the same day ([C13.10](#c13-10)), `consistency` and `pattern-consistency` exiting 0 on what
they find ([C12.14](#c12-14)), and tarka's two OTTR modes disagreeing about a
`mailto:` cell ([C10.11](#c10-11)).

Several were fixed upstream while this edition was being checked: HOLOS 0.21.1
for the validation defect, and 0.22.0 for `holos validate`'s exit status and
default engine ([C11.29](#c11-29)); suite 0.23.0, with engine 0.3.3, for `REA-020`,
`--inference` and the merged sketch, and suite 0.24.0 and 0.24.1 for several of
Chapter 14's smaller rows; engine 0.3.4 for a command line that validated against
no shapes and said the data conformed ([C11.07](#c11-07)); and the DSL at 0.16.1
for its error on unchecked code and its `Quad` type ([C08.15](#c08-15),
[C08.16](#c08-16)). The manual describes both sides of each fix.

## Environment of the recorded run

| | Version |
|---|---|
| python | 3.12.13 |
| platform | Windows 11 (AMD64) |
| PyPI ontology-quality-suite | 0.24.3 |
| PyPI shacl | 0.3.4 |
| PyPI holosdb | 0.25.0 |
| PyPI tarka-rdf | 0.1.1 |
| PyPI rdflib | 7.6.0 |
| PyPI pyoxigraph | 0.5.11 |
| PyPI polars | 2.0.0 |
| release shacl | shacl 0.3.4 |
| release tarka | tarka 0.1.1 |
| release holos | holos 0.25.0 (b44aa1c) |
| node | v20.19.5 |
| npm ontology-suite | 0.16.1 |
| npm shacl-wasm-node | 0.3.4 |
| npm holos-wasm-node | 0.25.0 |
| npm typescript | 7.0.2 |
| java (for HermiT) | openjdk version "25.0.3" 2026-04-21 LTS |
| oxi-gen (testing repo only) | oxi_gen 0.5.1 |

## Summary

256 claims: 179 reproduced here, by 105 distinct runs (179 pass, 0 fail, 0 not yet run), 65 cited from upstream, 12 arguments. 129 source citations, 123 of them checked against the cited commit (the quoted words found in the commit message or in the file at the cited lines).

### Introduction (README)

| Claim | Kind | Result |
|---|---|---|
| [C00.01 — A 61-check registry](#c00-01) | Reproduced here | PASS (2026-10-22) |
| [C00.02 — Every Part III command was executed, and re-run for this edition](#c00-02) | Argument | Argument |
| [C00.03 — Twenty diagrams](#c00-03) | Reproduced here | PASS (2026-10-22) |
| [C00.04 — pip install shacl gives the library only](#c00-04) | Reproduced here | PASS (2026-10-22) |
| [C00.05 — 54 or 55, and REA-021 or REA-022](#c00-05) | Reproduced here | PASS (2026-10-22) |
| [C00.06 — Everything else is exactly reproducible](#c00-06) | Reproduced here | PASS (2026-10-22) |

### 1. The business case

| Claim | Kind | Result |
|---|---|---|
| [C01.01 — Ten systems, forty-five pairings; twenty, a hundred and ninety](#c01-01) | Reproduced here | PASS (2026-10-22) |
| [C01.02 — An ontology decays without deliberate maintenance](#c01-02) | Argument | Argument |

### 2. People and cognition

| Claim | Kind | Result |
|---|---|---|
| [C02.01 — Building the vocabulary exposes fracture lines](#c02-01) | Argument | Argument |
| [C02.02 — Organisations move from labels to verbs](#c02-02) | Argument | Argument |
| [C02.03 — gist 14.1.0: 42 of 66 object properties constrain neither; gist 13: 40 of 63](#c02-03) | Reproduced here | PASS (2026-10-22) |
| [C02.04 — 479 findings, 23 once scoped](#c02-04) | Reproduced here | PASS (2026-10-22) |

### 3. Across the boundary: peers and supply chains

| Claim | Kind | Result |
|---|---|---|
| [C03.01 — foaf:name has domain owl:Thing, and the suite has been taught it](#c03-01) | Reproduced here | PASS (2026-10-22) |
| [C03.02 — version-diff says MAJOR, with the machine-readable diff](#c03-02) | Reproduced here | PASS (2026-10-22) |
| [C03.03 — The tombstone is read in both directions](#c03-03) | Reproduced here | PASS (2026-10-22) |
| [C03.04 — Policy at the scan for a consortium](#c03-04) | Reproduced here | PASS (2026-10-22) |
| [C03.05 — A registry is a distributable artefact](#c03-05) | Reproduced here | PASS (2026-10-22) |
| [C03.06 — Speak the protocol, not the product](#c03-06) | Reproduced here | PASS (2026-10-22) |

### 4. From research to industry

| Claim | Kind | Result |
|---|---|---|
| [C04.01 — REA-022 carries owlready2's internal error](#c04-01) | Reproduced here | PASS (2026-10-22) |
| [C04.02 — The failure is in owlready2's loader, not HermiT](#c04-02) | Reproduced here | PASS (2026-10-22) |
| [C04.03 — Without Java, the operating system's message; LOG-001 regardless](#c04-03) | Reproduced here | PASS (2026-10-22) |
| [C04.04 — A perfect SHACL score broke production; 0.3.1 took 425](#c04-04) | Cited from upstream | Cited from upstream |
| [C04.05 — HOLOS reports correctness and coverage: 512 of 512, 82%](#c04-05) | Cited from upstream | Cited from upstream |
| [C04.06 — A research artefact's implicit expiry date](#c04-06) | Argument | Argument |

### 5. GenAI and agents

| Claim | Kind | Result |
|---|---|---|
| [C05.01 — Grounding in graphs improves step-wise reasoning and recall](#c05-01) | Argument | Argument |
| [C05.02 — findings.txt is addressed to a person or an agent](#c05-02) | Cited from upstream | Cited from upstream |
| [C05.03 — Tombstones at 100% apply; guesses at 57% do not](#c05-03) | Reproduced here | PASS (2026-10-22) |
| [C05.04 — An agent as a principal with roles](#c05-04) | Reproduced here | PASS (2026-10-22) |

### 6. Stages and stories

| Claim | Kind | Result |
|---|---|---|
| [C06.01 — One practice, three frameworks](#c06-01) | Argument | Argument |

### 7. The toolchain

| Claim | Kind | Result |
|---|---|---|
| [C07.01 — The versions every Part III number was measured against](#c07-01) | Reproduced here | PASS (2026-10-22) |
| [C07.02 — The engine changed and Chapter 9's figures did not](#c07-02) | Cited from upstream | Cited from upstream |
| [C07.03 — One registry: 61 checks in ten categories, 44 SPARQL files and 6 shape files](#c07-03) | Reproduced here | PASS (2026-10-22) |
| [C07.04 — The editor runs the same engines at the same versions](#c07-04) | Cited from upstream | Cited from upstream |
| [C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries](#c07-05) | Reproduced here | PASS (2026-10-22) |
| [C07.06 — STY-003's message vanished on 60 of 65 findings](#c07-06) | Cited from upstream | Cited from upstream |
| [C07.07 — STR() of a blank node: lenient, conformant, and the guard](#c07-07) | Reproduced here | PASS (2026-10-22) |
| [C07.08 — pyshacl stays as a witness because it caught a real regression](#c07-08) | Cited from upstream | Cited from upstream |
| [C07.09 — Positional dedup, '[a blank node]' in both repositories, owlrl leaves the checks path](#c07-09) | Cited from upstream | Cited from upstream |
| [C07.10 — The extension adds six checks of its own: three MDL, three MAL](#c07-10) | Cited from upstream | Cited from upstream |
| [C07.11 — VOC-001 is declared, not runnable, by the CLI](#c07-11) | Cited from upstream | Cited from upstream |
| [C07.12 — Severity belongs to the shape that produces the result](#c07-12) | Reproduced here | PASS (2026-10-22) |
| [C07.13 — The registry declares; the directories decide](#c07-13) | Cited from upstream | Cited from upstream |
| [C07.14 — Eleven CLI-only checks, three extension-only](#c07-14) | Cited from upstream | Cited from upstream |
| [C07.15 — A sixteen-case comment fixture both repositories carry](#c07-15) | Cited from upstream | Cited from upstream |
| [C07.16 — --extra native-shacl parses but installs nothing](#c07-16) | Cited from upstream | Cited from upstream |
| [C07.17 — A locked dependency does not move with pip --upgrade](#c07-17) | Cited from upstream | Cited from upstream |
| [C07.18 — Oxigraph went in 0.13.11; the .vsix shrank from 20.2 to 17.5 MB](#c07-18) | Cited from upstream | Cited from upstream |
| [C07.19 — vsce --no-dependencies packages an extension with no engines](#c07-19) | Cited from upstream | Cited from upstream |
| [C07.20 — Only ontology-quality-suite installs a command](#c07-20) | Reproduced here | PASS (2026-10-22) |
| [C07.21 — Each release carries SHA256SUMS](#c07-21) | Cited from upstream | Cited from upstream |
| [C07.22 — --engine: native misses QUA-004; sparql and both give 23](#c07-22) | Reproduced here | PASS (2026-10-22) |
| [C07.23 — The engine choice is not about speed at this size](#c07-23) | Reproduced here | PASS (2026-10-22) |
| [C07.24 — Until 0.6.0 the shapes put sh:severity in the wrong place](#c07-24) | Cited from upstream | Cited from upstream |
| [C07.25 — My own node-shape severity mistake](#c07-25) | Reproduced here | PASS (2026-10-22) |
| [C07.26 — --inference owlrl is refused: a traceback at 0.22.0, a usage error from 0.23.0](#c07-26) | Reproduced here | PASS (2026-10-22) |
| [C07.27 — --inference rdfs: half the suite at 0.22.0, every engine from 0.23.0](#c07-27) | Reproduced here | PASS (2026-10-22) |
| [C07.28 — --verbose shows what each input resolved to](#c07-28) | Reproduced here | PASS (2026-10-22) |
| [C07.29 — Each deliberate flaw produces exactly one finding](#c07-29) | Reproduced here | PASS (2026-10-22) |
| [C07.30 — v2 renames Engineer, with a migration annotation, and adds a class and a property](#c07-30) | Reproduced here | PASS (2026-10-22) |
| [C07.31 — The testing repository: seventeen fixtures, a 38-question board](#c07-31) | Cited from upstream | Cited from upstream |
| [C07.32 — A lenient engine let a check pass in tests and fail in the field](#c07-32) | Reproduced here | PASS (2026-10-22) |

### 8. Model and validate

| Claim | Kind | Result |
|---|---|---|
| [C08.01 — Outline prompts resolve restriction names since 0.14.0](#c08-01) | Cited from upstream | Cited from upstream |
| [C08.02 — Run Local Checks reads 44 SPARQL and 6 SHACL files from the 61-check registry](#c08-02) | Reproduced here | PASS (2026-10-22) |
| [C08.03 — Six checks only the editor has: three MDL, and since 0.16.0 three MAL](#c08-03) | Cited from upstream | Cited from upstream |
| [C08.04 — VOC-001 is declared in the registry but only the extension runs it](#c08-04) | Cited from upstream | Cited from upstream |
| [C08.05 — Eleven checks the editor cannot produce, two held back explicitly](#c08-05) | Cited from upstream | Cited from upstream |
| [C08.06 — The CLI catches the typo as STR-001, not VOC-001](#c08-06) | Reproduced here | PASS (2026-10-22) |
| [C08.07 — Sixteen checks offer a Quick Fix](#c08-07) | Cited from upstream | Cited from upstream |
| [C08.08 — Blank nodes cross the repair boundary as skolem IRIs](#c08-08) | Cited from upstream | Cited from upstream |
| [C08.09 — A literal's base direction survives a repair since 0.13.12](#c08-09) | Cited from upstream | Cited from upstream |
| [C08.10 — Refactoring masks comments since 0.13.5](#c08-10) | Cited from upstream | Cited from upstream |
| [C08.11 — The unresolved-import warning names where it looked](#c08-11) | Cited from upstream | Cited from upstream |
| [C08.12 — The DSL script type-checks and builds against the npm package](#c08-12) | Reproduced here | PASS (2026-10-22) |
| [C08.13 — tsc refuses a bare string as a datatype range (TS2322)](#c08-13) | Reproduced here | PASS (2026-10-22) |
| [C08.14 — The gate catches the contradiction in the script's output](#c08-14) | Reproduced here | PASS (2026-10-22) |
| [C08.15 — Unchecked code: an internal TypeError up to 0.16.0, an error naming the mistake from 0.16.1](#c08-15) | Reproduced here | PASS (2026-10-22) |
| [C08.16 — build().quads and n3's Writer: TS2345 up to 0.16.0, no cast needed from 0.16.1](#c08-16) | Reproduced here | PASS (2026-10-22) |
| [C08.17 — ontology reports 2 findings, and findings.txt quotes the line](#c08-17) | Reproduced here | PASS (2026-10-22) |
| [C08.18 — LOG-001's message is a model of what a message should be](#c08-18) | Reproduced here | PASS (2026-10-22) |
| [C08.19 — With HermiT running: REA-021, and up to 0.22.0 a false REA-020](#c08-19) | Reproduced here | PASS (2026-10-22) |
| [C08.20 — --profile is off by default and repeatable](#c08-20) | Reproduced here | PASS (2026-10-22) |
| [C08.21 — checks reports 479 findings against the fixture](#c08-21) | Reproduced here | PASS (2026-10-22) |
| [C08.22 — A project tree alone now warns that 42 built-in checks did not run](#c08-22) | Reproduced here | PASS (2026-10-22) |
| [C08.23 — Until 0.18.0 that run was silent; the testing repo's gate was in that state](#c08-23) | Cited from upstream | Cited from upstream |
| [C08.24 — With @builtin and a one-entry registry, every built-in finding is UNMAPPED](#c08-24) | Reproduced here | PASS (2026-10-22) |
| [C08.25 — A merged registry names every finding, and ACM-001 fires on its fault only](#c08-25) | Reproduced here | PASS (2026-10-22) |
| [C08.26 — The warning named the site path @builtin was made to avoid, until 0.24.0](#c08-26) | Reproduced here | PASS (2026-10-22) |
| [C08.27 — Checks are discovered by walking the directory](#c08-27) | Cited from upstream | Cited from upstream |
| [C08.28 — Every full run writes cucumber.json](#c08-28) | Reproduced here | PASS (2026-10-22) |
| [C08.29 — Guard a label with isBlank; COALESCE is the weaker fix](#c08-29) | Reproduced here | PASS (2026-10-22) |
| [C08.30 — CT-39 asserts that a finding names something findable](#c08-30) | Cited from upstream | Cited from upstream |
| [C08.31 — sh:severity on a node shape does not reach its property shapes](#c08-31) | Reproduced here | PASS (2026-10-22) |
| [C08.32 — Four checks shipped that matched nothing](#c08-32) | Cited from upstream | Cited from upstream |
| [C08.34 — inverse(p): the inline inverse, new in the DSL at 0.16.0](#c08-34) | Reproduced here | PASS (2026-10-22) |
| [C08.33 — How the editor behaviour was established](#c08-33) | Argument | Argument |

### 9. Continuous integration

| Claim | Kind | Result |
|---|---|---|
| [C09.01 — --fail-on Violation exits non-zero on the fixture](#c09-01) | Reproduced here | PASS (2026-10-22) |
| [C09.02 — The unscoped run reports 479 findings, every time](#c09-02) | Reproduced here | PASS (2026-10-22) |
| [C09.03 — --exclude-imports gives 27 findings, four of them false](#c09-03) | Reproduced here | PASS (2026-10-22) |
| [C09.04 — --own-namespace gives 23 findings, all Acme's](#c09-04) | Reproduced here | PASS (2026-10-22) |
| [C09.05 — The three runs compared: 479, 27, 23](#c09-05) | Reproduced here | PASS (2026-10-22) |
| [C09.06 — --themes groups findings under questions in your words](#c09-06) | Reproduced here | PASS (2026-10-22) |
| [C09.07 — A near-miss namespace warns, on stderr, and offers only real namespaces](#c09-07) | Reproduced here | PASS (2026-10-22) |
| [C09.08 — The warning fires only when there were findings to lose](#c09-08) | Cited from upstream | Cited from upstream |
| [C09.09 — A scoped run keeps the 'reasoner did not run' finding, from 0.24.0](#c09-09) | Reproduced here | PASS (2026-10-22) |
| [C09.10 — Which reports a run writes, and --reports minimal](#c09-10) | Reproduced here | PASS (2026-10-22) |
| [C09.11 — The report set changed in 0.17.0, though REPORTS.md says 0.15.0](#c09-11) | Cited from upstream | Cited from upstream |
| [C09.12 — The suite pins shacl below 0.4](#c09-12) | Reproduced here | PASS (2026-10-22) |
| [C09.13 — --reports minimal writes two files](#c09-13) | Reproduced here | PASS (2026-10-22) |
| [C09.14 — run reports 26 findings, one contradiction once, from 0.24.0](#c09-14) | Reproduced here | PASS (2026-10-22) |
| [C09.15 — The testing repository: 165 passed, 10 skipped](#c09-15) | Reproduced here | PASS (2026-10-22) |
| [C09.16 — The competency board: 27 green, 0 red](#c09-16) | Reproduced here | PASS (2026-10-22) |
| [C09.17 — Fourteen of 38 questions need no data](#c09-17) | Cited from upstream | Cited from upstream |
| [C09.18 — A clean minimal ontology is not writable](#c09-18) | Cited from upstream | Cited from upstream |
| [C09.19 — Seventeen fixtures; 58 of 61 checks pinned](#c09-19) | Cited from upstream | Cited from upstream |
| [C09.20 — The message assertion found EFF-001 within minutes](#c09-20) | Cited from upstream | Cited from upstream |
| [C09.21 — A gate as a config file](#c09-21) | Cited from upstream | Cited from upstream |
| [C09.22 — An ignored gate dies](#c09-22) | Argument | Argument |

### 10. Ingest and transform

| Claim | Kind | Result |
|---|---|---|
| [C10.01 — sketch: 38 Infos, 8 triples and 7 entities from one query file](#c10-01) | Reproduced here | PASS (2026-10-22) |
| [C10.02 — The 38 Infos, and what TQL-003 says](#c10-02) | Reproduced here | PASS (2026-10-22) |
| [C10.03 — --queries, --query-pattern (alias --file-pattern), four extensions](#c10-03) | Reproduced here | PASS (2026-10-22) |
| [C10.04 — TQL-004, with its position as fields](#c10-04) | Reproduced here | PASS (2026-10-22) |
| [C10.05 — A CONCAT-built IRI: dropped as a subject, a literal as an object](#c10-05) | Reproduced here | PASS (2026-10-22) |
| [C10.06 — sketch writes bind-facts.ttl and bind-review.txt](#c10-06) | Reproduced here | PASS (2026-10-22) |
| [C10.07 — tarka's output for E004 is the block quoted in earlier editions](#c10-07) | Reproduced here | PASS (2026-10-22) |
| [C10.08 — tarka takes oxi-gen's options; --test N reads N rows](#c10-08) | Reproduced here | PASS (2026-10-22) |
| [C10.09 — 1.7× and 2.6× faster than oxi-gen, by tarka's own measurement](#c10-09) | Cited from upstream | Cited from upstream |
| [C10.10 — The OTTR template lints clean and gives the same 40 triples](#c10-10) | Reproduced here | PASS (2026-10-22) |
| [C10.11 — Without a mailto: prefix, run -l drops every row, silently](#c10-11) | Reproduced here | PASS (2026-10-22) |
| [C10.12 — Parquet input, data frames, and typed literals from typed columns](#c10-12) | Reproduced here | PASS (2026-10-22) |
| [C10.13 — Shapes from the mapping, and --validate conforms](#c10-13) | Reproduced here | PASS (2026-10-22) |
| [C10.14 — Generated shapes accept the dangling departments](#c10-14) | Reproduced here | PASS (2026-10-22) |
| [C10.15 — --post streams into holos-server: the graph arrives whole](#c10-15) | Reproduced here | PASS (2026-10-22) |
| [C10.16 — tarka speaks the protocol, in RDF 1.1, with the engine built without RDF 1.2](#c10-16) | Cited from upstream | Cited from upstream |
| [C10.17 — The suite's triplify still needs oxi-gen, and says so](#c10-17) | Reproduced here | PASS (2026-10-22) |
| [C10.18 — data: 548 unscoped (549 at 0.23.0, 550 at 0.22.0), 54 scoped, with HermiT running](#c10-18) | Reproduced here | PASS (2026-10-22) |
| [C10.19 — 54 when HermiT does not run, and from 0.24.0 the scoped report says so](#c10-19) | Reproduced here | PASS (2026-10-22) |
| [C10.20 — Real defects: every worksIn target is untyped and dangling](#c10-20) | Reproduced here | PASS (2026-10-22) |
| [C10.21 — Half the defects are mailboxes](#c10-21) | Reproduced here | PASS (2026-10-22) |
| [C10.22 — CNF-005: Contractor never populated](#c10-22) | Reproduced here | PASS (2026-10-22) |
| [C10.23 — REA-021 confirms LOG-001 by a different route](#c10-23) | Reproduced here | PASS (2026-10-22) |
| [C10.24 — The suite's walkthrough called it environment-flaky](#c10-24) | Cited from upstream | Cited from upstream |
| [C10.25 — --sample caps the reasoning pass](#c10-25) | Reproduced here | PASS (2026-10-22) |
| [C10.26 — CT-32 to CT-38: when every file is right and the set is wrong](#c10-26) | Cited from upstream | Cited from upstream |
| [C10.27 — CT-32's mapping is wired to no CSV](#c10-27) | Cited from upstream | Cited from upstream |
| [C10.28 — tq:PrefixBinding and the per-file sketch dataset](#c10-28) | Reproduced here | PASS (2026-10-22) |
| [C10.29 — The merged sketch and one prefix bound two ways: odd file first](#c10-29) | Reproduced here | PASS (2026-10-22) |
| [C10.30 — The merged sketch and one prefix bound two ways: odd file last](#c10-30) | Reproduced here | PASS (2026-10-22) |

### 11. Rules and inference

| Claim | Kind | Result |
|---|---|---|
| [C11.01 — The suite and the extension do not run SHACL-AF rules](#c11-01) | Reproduced here | PASS (2026-10-22) |
| [C11.02 — The Python surface: inference modes, and an unknown one is an error](#c11-02) | Reproduced here | PASS (2026-10-22) |
| [C11.03 — Rules shipped in 0.1.8; the $this fix came with them](#c11-03) | Cited from upstream | Cited from upstream |
| [C11.04 — Warnings break conformance; --allow-warnings records the choice](#c11-04) | Reproduced here | PASS (2026-10-22) |
| [C11.05 — The WebAssembly build agrees since 0.3.2](#c11-05) | Reproduced here | PASS (2026-10-22) |
| [C11.06 — The one-shots refuse an empty shapes graph](#c11-06) | Reproduced here | PASS (2026-10-22) |
| [C11.07 — The CLI and an empty shapes graph: conforms up to 0.3.3, refused from 0.3.4](#c11-07) | Reproduced here | PASS (2026-10-22) |
| [C11.08 — 425 of 426 W3C tests, the exception named](#c11-08) | Cited from upstream | Cited from upstream |
| [C11.09 — holos rules materialises into a graph of its own](#c11-09) | Reproduced here | PASS (2026-10-22) |
| [C11.10 — RDFS closure lets a shape see a sub-property](#c11-10) | Reproduced here | PASS (2026-10-22) |
| [C11.30 — Since 0.3.3 the closure is handed out, minus what RDF cannot write](#c11-30) | Reproduced here | PASS (2026-10-22) |
| [C11.11 — Triple rules are off by default and fire with -a](#c11-11) | Reproduced here | PASS (2026-10-22) |
| [C11.12 — One result per source instance, at 1,000 and 100,000](#c11-12) | Reproduced here | PASS (2026-10-22) |
| [C11.13 — A SPARQL rule computes the area, and validation sees it](#c11-13) | Reproduced here | PASS (2026-10-22) |
| [C11.14 — Since 0.3.0 only sh:ShapesGraph declarations apply](#c11-14) | Cited from upstream | Cited from upstream |
| [C11.15 — Rule compile errors are held on the rule](#c11-15) | Cited from upstream | Cited from upstream |
| [C11.16 — Hazard 1: a rule on a shape with no target never fires](#c11-16) | Reproduced here | PASS (2026-10-22) |
| [C11.17 — Hazard 2: one pass does not close a transitive rule](#c11-17) | Reproduced here | PASS (2026-10-22) |
| [C11.18 — Hazard 3: equal sh:order cannot see each other's inferences](#c11-18) | Reproduced here | PASS (2026-10-22) |
| [C11.19 — Hazard 4: a conclusion from absence outlives the absence](#c11-19) | Reproduced here | PASS (2026-10-22) |
| [C11.20 — Rules never modify the input graph](#c11-20) | Cited from upstream | Cited from upstream |
| [C11.21 — The previous edition's timings, and 0.3.0's own measurement](#c11-21) | Cited from upstream | Cited from upstream |
| [C11.22 — The index holds the graph three times; results sorted by focus node](#c11-22) | Cited from upstream | Cited from upstream |
| [C11.23 — --build-index caches the parsed graph](#c11-23) | Reproduced here | PASS (2026-10-22) |
| [C11.24 — A SHACL function in a rule is an error, exit 2](#c11-24) | Reproduced here | PASS (2026-10-22) |
| [C11.25 — Rules in WebAssembly, and an unknown mode is an error there too](#c11-25) | Reproduced here | PASS (2026-10-22) |
| [C11.26 — The editor asks for inference 'none', deliberately](#c11-26) | Cited from upstream | Cited from upstream |
| [C11.27 — Named graphs are flattened](#c11-27) | Reproduced here | PASS (2026-10-22) |
| [C11.28 — Exit codes 0, 1 and 2](#c11-28) | Reproduced here | PASS (2026-10-22) |
| [C11.29 — holos validate: exit 0 whatever it found up to 0.21.1, a gate from 0.22.0](#c11-29) | Reproduced here | PASS (2026-10-22) |

### 12. Release and change

| Claim | Kind | Result |
|---|---|---|
| [C12.01 — version-diff: the verdict comes from the axioms](#c12-01) | Reproduced here | PASS (2026-10-22) |
| [C12.02 — Reversed, the diff describes the inverse release](#c12-02) | Reproduced here | PASS (2026-10-22) |
| [C12.03 — Without FOAF resolved, consistency reports foaf:name and foaf:mbox](#c12-03) | Reproduced here | PASS (2026-10-22) |
| [C12.04 — consistency: what breaks, and a 100% repair](#c12-04) | Reproduced here | PASS (2026-10-22) |
| [C12.05 — The tombstone is read in both directions; isReplacedBy in one](#c12-05) | Reproduced here | PASS (2026-10-22) |
| [C12.06 — Symmetric since suite 0.3.5, 12 August 2026](#c12-06) | Cited from upstream | Cited from upstream |
| [C12.07 — The reversed equivalentClass at 100%](#c12-07) | Reproduced here | PASS (2026-10-22) |
| [C12.08 — --apply-repairs changes the one code line on line 14](#c12-08) | Reproduced here | PASS (2026-10-22) |
| [C12.09 — Comments used to be rewritten too](#c12-09) | Cited from upstream | Cited from upstream |
| [C12.10 — String literals are still rewritten, deliberately](#c12-10) | Reproduced here | PASS (2026-10-22) |
| [C12.11 — The same defect in the editor](#c12-11) | Cited from upstream | Cited from upstream |
| [C12.12 — pattern-consistency catches MKT only from the output data](#c12-12) | Reproduced here | PASS (2026-10-22) |
| [C12.13 — Omit --output-data and it reports clean](#c12-13) | Reproduced here | PASS (2026-10-22) |
| [C12.14 — Both consistency commands are report-only by default](#c12-14) | Reproduced here | PASS (2026-10-22) |
| [C12.15 — The approval workflow is not implemented here](#c12-15) | Argument | Argument |
| [C12.16 — UPDATING.md as a governance playbook](#c12-16) | Cited from upstream | Cited from upstream |

### 13. Operate and consume

| Claim | Kind | Result |
|---|---|---|
| [C13.01 — consistency-remote against holos-server; the imports rule applies in the store](#c13-01) | Reproduced here | PASS (2026-10-22) |
| [C13.02 — The manifest, as JSON or built in Python; the flags](#c13-02) | Reproduced here | PASS (2026-10-22) |
| [C13.03 — The store a version behind: --fail-on-anything exits 1](#c13-03) | Reproduced here | PASS (2026-10-22) |
| [C13.04 — A mistyped role is refused at load, from 0.24.0](#c13-04) | Reproduced here | PASS (2026-10-22) |
| [C13.05 — SHACL validation flattens named graphs](#c13-05) | Reproduced here | PASS (2026-10-22) |
| [C13.06 — Policy at the scan: rows without the column, unless you are in HR](#c13-06) | Reproduced here | PASS (2026-10-22) |
| [C13.07 — The fluent API mistake](#c13-07) | Reproduced here | PASS (2026-10-22) |
| [C13.08 — The holos command gives the same answers](#c13-08) | Reproduced here | PASS (2026-10-22) |
| [C13.09 — 8 ns per quad, by HOLOS's own measurement](#c13-09) | Cited from upstream | Cited from upstream |
| [C13.10 — Validation and the store: written into it up to 0.21.0, untouched from 0.21.1](#c13-10) | Reproduced here | PASS (2026-10-22) |
| [C13.11 — docgen: 4 classes, 5 external terms, 3 resolved](#c13-11) | Reproduced here | PASS (2026-10-22) |
| [C13.12 — Three runs, three pages; pinned, one](#c13-12) | Reproduced here | PASS (2026-10-22) |
| [C13.13 — Every row carries source_file and line](#c13-13) | Reproduced here | PASS (2026-10-22) |
| [C13.14 — HOLOS: embeddable, RDF 1.2, GeoSPARQL](#c13-14) | Reproduced here | PASS (2026-10-22) |
| [C13.15 — The editor's checks run on holos-wasm-node](#c13-15) | Cited from upstream | Cited from upstream |
| [C13.16 — Observability and APIs are not covered](#c13-16) | Argument | Argument |

### 14. Coverage and gaps

| Claim | Kind | Result |
|---|---|---|
| [C14.01 — A scoped run could not see that the reasoner did not run (fixed in 0.24.0)](#c14-01) | Reproduced here | PASS (2026-10-22) |
| [C14.02 — The shacl CLI reported conformance when it checked nothing, up to 0.3.3](#c14-02) | Reproduced here | PASS (2026-10-22) |
| [C14.03 — holos validate exited 0 on a non-conforming graph, up to 0.21.1](#c14-03) | Reproduced here | PASS (2026-10-22) |
| [C14.04 — tarka drops instances it cannot build, silently, in the CLI and in Python](#c14-04) | Reproduced here | PASS (2026-10-22) |
| [C14.05 — docgen reshuffles the page on every run](#c14-05) | Reproduced here | PASS (2026-10-22) |
| [C14.06 — The reasoner's outcome follows the hash seed](#c14-06) | Reproduced here | PASS (2026-10-22) |
| [C14.07 — SHACL validates the union of the named graphs](#c14-07) | Reproduced here | PASS (2026-10-22) |
| [C14.08 — Almost: the seed decides most of owlready2's load, and not all of it](#c14-08) | Reproduced here | PASS (2026-10-22) |
| [C14.09 — Without Java the message is the operating system's](#c14-09) | Reproduced here | PASS (2026-10-22) |
| [C14.39 — REA-020 said inconsistent when only a class was unsatisfiable; fixed in 0.23.0](#c14-39) | Reproduced here | PASS (2026-10-22) |
| [C14.10 — A mistyped manifest role compared nothing, successfully (fixed in 0.24.0)](#c14-10) | Reproduced here | PASS (2026-10-22) |
| [C14.11 — --help offers owlrl; asking for it gives a traceback](#c14-11) | Reproduced here | PASS (2026-10-22) |
| [C14.12 — --inference is ignored under --engine sparql](#c14-12) | Reproduced here | PASS (2026-10-22) |
| [C14.13 — The near-miss warning listed blank-node identifiers, until 0.24.0](#c14-13) | Reproduced here | PASS (2026-10-22) |
| [C14.14 — --registry replaces, so @builtin with a house registry is UNMAPPED](#c14-14) | Reproduced here | PASS (2026-10-22) |
| [C14.15 — One contradiction, two LOG-001s, until 0.24.0](#c14-15) | Reproduced here | PASS (2026-10-22) |
| [C14.16 — The DSL's TypeError and Quad type, up to 0.16.0](#c14-16) | Reproduced here | PASS (2026-10-22) |
| [C14.17 — triplify drives oxi-gen only](#c14-17) | Reproduced here | PASS (2026-10-22) |
| [C14.18 — consistency and pattern-consistency are report-only by default](#c14-18) | Reproduced here | PASS (2026-10-22) |
| [C14.19 — The holos CLI and holosdb defaulted to different validators, up to 0.21.1](#c14-19) | Reproduced here | PASS (2026-10-22) |
| [C14.20 — sketch reads every file with the first file's prefixes](#c14-20) | Reproduced here | PASS (2026-10-22) |
| [C14.21 — Documentation drift, upstream](#c14-21) | Reproduced here | PASS (2026-10-22) |
| [C14.22 — The registry grew from 50 checks to 61](#c14-22) | Cited from upstream | Cited from upstream |
| [C14.23 — Closed: the engines are the toolchain's own](#c14-23) | Reproduced here | PASS (2026-10-22) |
| [C14.24 — Closed: messages on blank nodes](#c14-24) | Reproduced here | PASS (2026-10-22) |
| [C14.25 — Closed: findings say where they are](#c14-25) | Reproduced here | PASS (2026-10-22) |
| [C14.26 — Closed: house rules compose with the built-ins](#c14-26) | Reproduced here | PASS (2026-10-22) |
| [C14.27 — Five suite defects found by the testing repository](#c14-27) | Cited from upstream | Cited from upstream |
| [C14.28 — Closed: sh:conforms follows the specification](#c14-28) | Reproduced here | PASS (2026-10-22) |
| [C14.29 — Closed: the repair engine keeps blank nodes and base directions](#c14-29) | Cited from upstream | Cited from upstream |
| [C14.40 — Closed: HOLOS validation leaves the store as it found it, from 0.21.1](#c14-40) | Reproduced here | PASS (2026-10-22) |
| [C14.41 — Closed: three suite defects this edition found, fixed in 0.23.0](#c14-41) | Reproduced here | PASS (2026-10-22) |
| [C14.42 — Closed: gates that could not fail, and the DSL's two rough edges](#c14-42) | Reproduced here | PASS (2026-10-22) |
| [C14.30 — Early, but real: policy, rules, a triplifier](#c14-30) | Reproduced here | PASS (2026-10-22) |
| [C14.31 — Wrong: the migration annotation's direction](#c14-31) | Reproduced here | PASS (2026-10-22) |
| [C14.32 — Wrong: REA-022 as the tell in a scoped run](#c14-32) | Reproduced here | PASS (2026-10-22) |
| [C14.33 — Wrong: the reasoner as flaky](#c14-33) | Reproduced here | PASS (2026-10-22) |
| [C14.34 — Wrong: the reasoner as an optional extra](#c14-34) | Reproduced here | PASS (2026-10-22) |
| [C14.35 — Wrong: stale numbers](#c14-35) | Cited from upstream | Cited from upstream |
| [C14.36 — Wrong: where a CONCAT-built IRI goes](#c14-36) | Reproduced here | PASS (2026-10-22) |
| [C14.37 — Wrong: when rules arrived in the SHACL engine](#c14-37) | Cited from upstream | Cited from upstream |
| [C14.38 — Wrong: the SHACL engine's pass rate](#c14-38) | Cited from upstream | Cited from upstream |

### 15. Adoption roadmap

| Claim | Kind | Result |
|---|---|---|
| [C15.01 — 479 unscoped, 23 scoped, four false with --exclude-imports](#c15-01) | Reproduced here | PASS (2026-10-22) |
| [C15.02 — --output-data is not optional](#c15-02) | Reproduced here | PASS (2026-10-22) |
| [C15.03 — PYTHONHASHSEED for docgen](#c15-03) | Reproduced here | PASS (2026-10-22) |

### Appendix A — Diagram and brand conventions

| Claim | Kind | Result |
|---|---|---|
| [CA.01 — All six fills clear 12:1 against the text colour](#ca-01) | Reproduced here | PASS (2026-10-22) |
| [CA.02 — FOAF is published as RDF/XML](#ca-02) | Argument | Argument |

---

<a id="chapter-00"></a>
## Introduction (README)

Annotated chapter: [manual/README.md](manual/README.md) · plain chapter: [../README.md](../README.md)

<a id="c00-01"></a>
### C00.01 — A 61-check registry

**In the manual:** [README, at the claim](manual/README.md#ev-c00-01) · [plain edition](../README.md#what-this-is)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The gate: a Python CLI and library with the 61-check registry

**Evidence:** the same as [C07.03 — One registry: 61 checks in ten categories, 44 SPARQL files and 6 shape files](#c07-03), which reproduces it: step 1 output contains 'registry entries: 61 in 10 categories', 'portable .rq checks: 44; SHACL shape files: 6'

---

<a id="c00-02"></a>
### C00.02 — Every Part III command was executed, and re-run for this edition

**In the manual:** [README, at the claim](manual/README.md#ev-c00-02) · [plain edition](../README.md#what-this-is)  
**Kind:** Argument · **Result:** Argument

> Every command shown in Part III was **executed for real**

A statement of method. This folder is the re-run: each `run` claim records the date it last ran, and the environment table at the top of EVIDENCE.md gives the versions.

---

<a id="c00-03"></a>
### C00.03 — Twenty diagrams

**In the manual:** [README, at the claim](manual/README.md#ev-c00-03) · [plain edition](../README.md#read-it-on-paper)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> numbers, all twenty diagrams rendered, and an index of commands, flags and check

**Commands** (from the `evidence/` folder):

```bash
python scripts/count_mermaid.py ..
```

<details><summary><code>scripts/count_mermaid.py</code></summary>

```python
"""Count the Mermaid diagrams in the manual's chapters (the PDF renders these).

    python scripts/count_mermaid.py ..
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1])
total = 0
for p in sorted((repo / "docs").glob("*.md")):
    n = p.read_text(encoding="utf-8").count("```mermaid")
    total += n
    print(f"{n}  docs/{p.name}")
print(f"{total} diagrams in the chapters; README has {(repo / 'README.md').read_text(encoding='utf-8').count('```mermaid')} more")
```

</details>

**What is checked:** 19 Mermaid blocks across the chapters and the appendix, and the README's own, which the PDF keeps in its introduction: twenty

**Recorded result:** PASS — step 1 output contains '19 diagrams in the chapters; README has 1 more'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/count_mermaid.py ..
2  docs/01-the-business-case.md
1  docs/02-people-and-cognition.md
2  docs/03-across-the-boundary.md
1  docs/04-from-research-to-industry.md
2  docs/05-genai-and-agents.md
3  docs/06-stages-and-stories.md
1  docs/07-the-toolchain.md
1  docs/08-model-and-validate.md
1  docs/09-continuous-integration.md
1  docs/10-ingest-and-transform.md
1  docs/11-rules-and-inference.md
1  docs/12-release-and-change.md
1  docs/13-operate-and-consume.md
0  docs/14-coverage-and-gaps.md
1  docs/15-adoption-roadmap.md
0  docs/diagram-style.md
19 diagrams in the chapters; README has 1 more
[exit 0]
```

</details>

The previous wording said nineteen, which counted the chapters and not the PDF.

---

<a id="c00-04"></a>
### C00.04 — pip install shacl gives the library only

**In the manual:** [README, at the claim](manual/README.md#ev-c00-04) · [plain edition](../README.md#run-it-yourself)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `pip install shacl`

**Evidence:** the same as [C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries](#c07-05), which reproduces it: step 1 output contains 'commands installed: ontology-quality-suite', 'owlready2>=0.51', 'shacl 0.3.4/n    commands installed: none (library only)', 'tarka-rdf 0.1.1/n    commands installed: none (library only)', 'holosdb 0.25.0/n    commands installed: none (library only)'; suite 0.24.3: step 1 output contains 'shacl<0.4,>=0.3.3'; suite 0.24.3: step 1 output contains 'holosdb>=0.24'

---

<a id="c00-05"></a>
### C00.05 — 54 or 55, and REA-021 or REA-022

**In the manual:** [README, at the claim](manual/README.md#ev-c00-05) · [plain edition](../README.md#conventions)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Two outputs move unless you pin one variable, and both are labelled where they

**Evidence:** the same as [C10.18 — data: 548 unscoped (549 at 0.23.0, 550 at 0.22.0), 54 scoped, with HermiT running](#c10-18), which reproduces it: suite 0.24.3: step 2: 548 findings (66 V, 363 W, 119 I); suite 0.24.3: step 3: 54 findings (12 V, 40 W, 2 I); REA-021 present; REA-022 absent

The 54 is C10.19; the hash seed's part, and the residual it does not control, are C14.06 and C14.08; docgen's reshuffling is C13.12.

---

<a id="c00-06"></a>
### C00.06 — Everything else is exactly reproducible

**In the manual:** [README, at the claim](manual/README.md#ev-c00-06) · [plain edition](../README.md#conventions)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Everything else is exactly reproducible across repeated runs, and survived a change of the engine

**Evidence:** the same as [C09.02 — The unscoped run reports 479 findings, every time](#c09-02), which reproduces it: step 1: 479 findings (55 V, 340 W, 84 I); step 2: 479 findings (55 V, 340 W, 84 I); step 3: 479 findings (55 V, 340 W, 84 I)

C09.02 runs the unscoped gate three times; C07.02 compares the figures with the previous edition's, measured on rdflib and pyshacl.

---

<a id="chapter-01"></a>
## 1. The business case

Annotated chapter: [manual/docs/01-the-business-case.md](manual/docs/01-the-business-case.md) · plain chapter: [../docs/01-the-business-case.md](../docs/01-the-business-case.md)

<a id="c01-01"></a>
### C01.01 — Ten systems, forty-five pairings; twenty, a hundred and ninety

**In the manual:** [Chapter 1, at the claim](manual/docs/01-the-business-case.md#ev-c01-01) · [plain edition](../docs/01-the-business-case.md#integration-cost-that-scales-quadratically)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> mappings. Ten systems is forty-five potential pairings; twenty is a hundred and

**Commands** (from the `evidence/` folder):

```bash
python scripts/pairings.py 10 20
```

<details><summary><code>scripts/pairings.py</code></summary>

```python
"""Chapter 1 §1.1: point-to-point integration pairings for n systems, n(n-1)/2.

    python scripts/pairings.py 4 10 20
"""
import sys

for n in map(int, sys.argv[1:]):
    print(f"{n} systems: {n * (n - 1) // 2} potential point-to-point pairings; "
          f"{n} mappings to a shared model")
```

</details>

**What is checked:** n(n−1)/2 gives 45 for 10 systems and 190 for 20

**Recorded result:** PASS — step 1 output contains '10 systems: 45 potential point-to-point pairings', '20 systems: 190 potential point-to-point pairings'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/pairings.py 10 20
10 systems: 45 potential point-to-point pairings; 10 mappings to a shared model
20 systems: 190 potential point-to-point pairings; 20 mappings to a shared model
[exit 0]
```

</details>

---

<a id="c01-02"></a>
### C01.02 — An ontology decays without deliberate maintenance

**In the manual:** [Chapter 1, at the claim](manual/docs/01-the-business-case.md#ev-c01-02) · [plain edition](../docs/01-the-business-case.md#13-the-decay-problem-which-is-the-semops-problem)  
**Kind:** Argument · **Result:** Argument

> **An ontology is most accurate the day it ships. Every day after that, without

A judgement from practice. Chapter 14 §14.5 gives the observable form, the Warning trend in retained full_results.csv files, and C09.10 shows the file each run writes.

---

<a id="chapter-02"></a>
## 2. People and cognition

Annotated chapter: [manual/docs/02-people-and-cognition.md](manual/docs/02-people-and-cognition.md) · plain chapter: [../docs/02-people-and-cognition.md](../docs/02-people-and-cognition.md)

<a id="c02-01"></a>
### C02.01 — Building the vocabulary exposes fracture lines

**In the manual:** [Chapter 2, at the claim](manual/docs/02-people-and-cognition.md#ev-c02-01) · [plain edition](../docs/02-people-and-cognition.md#21-definitions-are-territory)  
**Kind:** Argument · **Result:** Argument

> exposes fracture lines that were already in the organisation

From the author's Semantic Arts article 'Team Building — The Importance of an Ontology', cited in the chapter's references. Experience, not measurement.

---

<a id="c02-02"></a>
### C02.02 — Organisations move from labels to verbs

**In the manual:** [Chapter 2, at the claim](manual/docs/02-people-and-cognition.md#ev-c02-02) · [plain edition](../docs/02-people-and-cognition.md#from-labels-to-verbs)  
**Kind:** Argument · **Result:** Argument

> There is a pattern across whole organisations, not just individuals, and it is worth

From the author's Semantic Arts article 'From Labels to Verbs — Child's Play!', cited in the chapter's references.

---

<a id="c02-03"></a>
### C02.03 — gist 14.1.0: 42 of 66 object properties constrain neither; gist 13: 40 of 63

**In the manual:** [Chapter 2, at the claim](manual/docs/02-people-and-cognition.md#ev-c02-03) · [plain edition](../docs/02-people-and-cognition.md#from-labels-to-verbs)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> current release, gist 14.1.0, 42 of its 66 object properties constrain neither;

**Commands** (from the `evidence/` folder):

```bash
python scripts/gist_properties.py 14.1.0 13.0.0
```

<details><summary><code>scripts/gist_properties.py</code></summary>

```python
"""Chapter 2 §2.3: how many of gist's object properties constrain neither domain nor range.

    python scripts/gist_properties.py 14.1.0 13.0.0

Downloads each release's web-download zip from github.com/semanticarts/gist (cached
in work/gist/), reads gistCore<version>.ttl, and counts the gist object
properties by which of rdfs:domain and rdfs:range they declare. gist is published
by Semantic Arts under its own licence; nothing of it is copied into this folder.
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph

sys.stdout.reconfigure(encoding="utf-8")
GIST = "https://w3id.org/semanticarts/ns/ontology/gist/"
cache = Path("work/gist")
cache.mkdir(parents=True, exist_ok=True)

for version in sys.argv[1:]:
    ttl = cache / f"gistCore{version}.ttl"
    if not ttl.is_file():
        url = f"https://github.com/semanticarts/gist/releases/download/v{version}/gist{version}_webDownload.zip"
        with urllib.request.urlopen(url) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        name = next(n for n in z.namelist() if n.endswith(f"gistCore{version}.ttl"))
        ttl.write_bytes(z.read(name))
    g = Graph()
    g.parse(ttl)
    ops = {p for p in g.subjects(RDF.type, OWL.ObjectProperty) if str(p).startswith(GIST)}
    dps = {p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if str(p).startswith(GIST)}
    dom = {p for p in ops if (p, RDFS.domain, None) in g}
    rng = {p for p in ops if (p, RDFS.range, None) in g}
    print(f"gist {version}: {len(ops)} object properties, {len(dps)} data properties; "
          f"domain only {len(dom - rng)}, range only {len(rng - dom)}, both {len(dom & rng)}, "
          f"neither {len(ops - dom - rng)}")
```

</details>

**What is checked:** gist 14.1.0 has 66 object properties, 42 with neither domain nor range; gist 13.0.0 has 63, 40

**Recorded result:** PASS — step 1 output contains 'gist 14.1.0: 66 object properties', 'neither 42', 'gist 13.0.0: 63 object properties', 'neither 40'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/gist_properties.py 14.1.0 13.0.0
gist 14.1.0: 66 object properties, 50 data properties; domain only 3, range only 14, both 7, neither 42
gist 13.0.0: 63 object properties, 50 data properties; domain only 3, range only 14, both 6, neither 40
[exit 0]
```

</details>

Downloads the two releases from Semantic Arts' GitHub; nothing of gist is copied into this folder.

---

<a id="c02-04"></a>
### C02.04 — 479 findings, 23 once scoped

**In the manual:** [Chapter 2, at the claim](manual/docs/02-people-and-cognition.md#ev-c02-04) · [plain edition](../docs/02-people-and-cognition.md#the-479-finding-report)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> FOAF imports resolved produces **479 findings**. Adding a single flag that scopes

**Evidence:** the same as [C09.04 — --own-namespace gives 23 findings, all Acme's](#c09-04), which reproduces it: step 1: 23 findings (1 V, 22 W, 0 I); own/full_results.csv: {'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}; every focus node starts with https://acme.example.org/ns/

---

<a id="chapter-03"></a>
## 3. Across the boundary: peers and supply chains

Annotated chapter: [manual/docs/03-across-the-boundary.md](manual/docs/03-across-the-boundary.md) · plain chapter: [../docs/03-across-the-boundary.md](../docs/03-across-the-boundary.md)

<a id="c03-01"></a>
### C03.01 — foaf:name has domain owl:Thing, and the suite has been taught it

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-01) · [plain edition](../docs/03-across-the-boundary.md#c-open-ecosystem-the-stability-problem)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The classic case is FOAF, which deliberately declares `foaf:name` with

**Commands** (from the `evidence/` folder):

```bash
python scripts/query_file.py fixtures/acme_robotics/reference_vocab/foaf.rdf "SELECT ?domain WHERE { <http://xmlns.com/foaf/0.1/name> <http://www.w3.org/2000/01/rdf-schema#domain> ?domain }"
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C03_01/employees.ttl
python scripts/without_java.py ontology-quality-suite data work/C03_01/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C03_01/data --fail-on never --reports minimal
```

**What is checked:** FOAF declares foaf:name's domain as owl:Thing; the unscoped data run over the acme employees reports no conformance finding about foaf:name

**Recorded result:** PASS — step 1 output contains 'http://www.w3.org/2002/07/owl#Thing'; no conformance finding concerns foaf:name

<details><summary>Output, as recorded</summary>

```text
$ python scripts/query_file.py fixtures/acme_robotics/reference_vocab/foaf.rdf "SELECT ?domain WHERE { <http://xmlns.com/foaf/0.1/name> <http://www.w3.org/2000/01/rdf-schema#domain> ?domain }"
domain
http://www.w3.org/2002/07/owl#Thing
[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C03_01/employees.ttl

[exit 0]

$ python scripts/without_java.py ontology-quality-suite data work/C03_01/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C03_01/data --fail-on never --reports minimal
without_java: java on PATH now: none
Findings: 548 total (65 Violation, 363 Warning, 120 Info)
Reports written to: ./work/C03_01/data
  - work/C03_01/data/findings.txt (start here -- what, where, and the source line)
  - work/C03_01/data/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmp0ikgzvqi -Y
[exit 0]
```

</details>

---

<a id="c03-02"></a>
### C03.02 — version-diff says MAJOR, with the machine-readable diff

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-02) · [plain edition](../docs/03-across-the-boundary.md#33-the-cross-boundary-release-problem)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The bump decision must be evidence-based, not a judgement call.**

**Evidence:** the same as [C12.01 — version-diff: the verdict comes from the axioms](#c12-01), which reproduces it: step 1 output contains 'Removed classes [MAJOR]:\n  - https://acme.example.org/ns/Engineer', 'https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee', 'Added classes [minor]:\n  - https://acme.example.org/ns/ProductManager/n  - https://acme.example.org/ns/SoftwareEngineer', 'Added properties [minor]:\n  - https://acme.example.org/ns/hireDate', 'Added equivalentClass axioms [minor]:\n  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer', 'Suggested version bump: MAJOR'; step 2 output contains 'diff.json', 'diff.txt'; step 3 exits non-zero (1)

---

<a id="c03-03"></a>
### C03.03 — The tombstone is read in both directions

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-03) · [plain edition](../docs/03-across-the-boundary.md#migration-annotations-are-a-cross-boundary-contract)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Earlier editions of this manual told you that the suite's rename detection read this

**Evidence:** the same as [C12.05 — The tombstone is read in both directions; isReplacedBy in one](#c12-05), which reproduces it: step 3 output contains 'employees.rq (confidence 100%)'; step 6 output contains 'employees.rq (confidence 100%)'; step 9 output contains 'employees.rq (confidence 57%)'

---

<a id="c03-04"></a>
### C03.04 — Policy at the scan for a consortium

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-04) · [plain edition](../docs/03-across-the-boundary.md#a-peer-consortium-the-coordination-problem)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> knowing even though the component is young. A store that enforces access policy **at

**Evidence:** the same as [C13.06 — Policy at the scan: rows without the column, unless you are in HR](#c13-06), which reproduces it: step 1 output contains '2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None/n    name=Bob, salary=None/n    name=Carol, salary=None', '3. the same, asked by alice with role hr:\n    name=Alice, salary=95000/n    name=Bob, salary=88000/n    name=Carol, salary=102000', '4. COUNT of salaries without the role:\n    n=0', '5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance/n    g=http://example.com/public/n6.', '6. named graphs, with clearance 3:\n    g=http://example.com/provenance/n    g=http://example.com/public/n    g=http://example.com/reviews', '7. salary denied with fail_closed():\n    HolosError: ', 'access denied by policy/n8. (mistake)', '8. (mistake) policy method called as a statement:\n    n=3'

---

<a id="c03-05"></a>
### C03.05 — A registry is a distributable artefact

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-05) · [plain edition](../docs/03-across-the-boundary.md#b-supply-chain-the-capability-asymmetry-problem)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> - Publish your SHACL shapes and check registry as files, not as prose in a PDF. The

**Evidence:** the same as [C08.25 — A merged registry names every finding, and ACM-001 fires on its fault only](#c08-25), which reproduces it: step 1 output contains '61 built-in + 1 project = 62 entries'; ACM-001 fires on E101 (no ID) and not on E100 (the control); with its title and remediation from the merged registry; and no finding is UNMAPPED

---

<a id="c03-06"></a>
### C03.06 — Speak the protocol, not the product

**In the manual:** [Chapter 3, at the claim](manual/docs/03-across-the-boundary.md#ev-c03-06) · [plain edition](../docs/03-across-the-boundary.md#35-where-this-leaves-the-practice)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> One last design lesson, which I took from the triplifier rather than from a

**Evidence:** the same as [C10.15 — --post streams into holos-server: the graph arrives whole](#c10-15), which reproduces it: step 1 exits 0; step 2 output contains 'https://acme.example.org/graph/triplified/employees', '40'

tarka's own reasoning is in its commit [26f256a](https://github.com/pwin/tarka/commit/26f256a28f10d299a4cf1c5dd49ba52cd37122a7) (C10.16).

---

<a id="chapter-04"></a>
## 4. From research to industry

Annotated chapter: [manual/docs/04-from-research-to-industry.md](manual/docs/04-from-research-to-industry.md) · plain chapter: [../docs/04-from-research-to-industry.md](../docs/04-from-research-to-industry.md)

<a id="c04-01"></a>
### C04.01 — REA-022 carries owlready2's internal error

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-01) · [plain edition](../docs/04-from-research-to-industry.md#43-a-verified-example-from-this-manuals-own-toolchain)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > The external DL reasoner ('hermit') could not be run: `cannot access local

**Evidence:** the same as [C14.06 — The reasoner's outcome follows the hash seed](#c14-06), which reproduces it: seed 5: HermiT ran 10 of 10, did not run 0; seed 0: HermiT ran 0 of 10, did not run 10; step 1 output contains "could not be run: cannot access local variable 'entity' where it is not associated with a value"

C14.06's record lists the REA-022 messages its seed-0 runs produced. 'Five runs of ten' describes this edition's unpinned runs.

---

<a id="c04-02"></a>
### C04.02 — The failure is in owlready2's loader, not HermiT

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-02) · [plain edition](../docs/04-from-research-to-industry.md#43-a-verified-example-from-this-manuals-own-toolchain)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Reading the traceback for this edition showed something else: owlready2's *loader*

**Evidence:** the same as [C14.08 — Almost: the seed decides most of owlready2's load, and not all of it](#c14-08), which reproduces it: line 2. failed 15 times (at least 9); line 3. loaded 15 times (at least 13); every failure was owlready2 building foaf:primaryTopic

---

<a id="c04-03"></a>
### C04.03 — Without Java, the operating system's message; LOG-001 regardless

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-03) · [plain edition](../docs/04-from-research-to-industry.md#43-a-verified-example-from-this-manuals-own-toolchain)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Java runtime** HermiT runs in. Hide Java and `REA-022` says so in different

**Evidence:** the same as [C14.09 — Without Java the message is the operating system's](#c14-09), which reproduces it: step 1 output contains 'without_java: java on PATH now: none'; REA-022 says 'cannot find the file specified'; and not 'entity'

That owlready2 installs with the suite is C07.05; LOG-001 without any reasoner is C08.17.

---

<a id="c04-04"></a>
### C04.04 — A perfect SHACL score broke production; 0.3.1 took 425

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-04) · [plain edition](../docs/04-from-research-to-industry.md#when-a-perfect-score-is-the-wrong-answer)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The SHACL engine passed all 426 W3C tests for a few days at 0.3.0, by enforcing one

**Evidence:** the same as [C11.08 — 425 of 426 W3C tests, the exception named](#c11-08) (cited from upstream).

---

<a id="c04-05"></a>
### C04.05 — HOLOS reports correctness and coverage: 512 of 512, 82%

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-05) · [plain edition](../docs/04-from-research-to-industry.md#when-a-perfect-score-is-the-wrong-answer)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> HOLOS reports its W3C results as **two numbers, because either alone misleads**:

**Sources:**

- [HOLOS README, conformance table](https://github.com/pwin/triplestore/blob/b44aa1c508536220f1d0de4a9323cf4bbcc63563/README.md#L122): “| SPARQL 1.1 | **512/512** · 100% | 512/625 · **82%** |” (quote found, checked 2026-10-22)
- [HOLOS README, tests not yet run](https://github.com/pwin/triplestore/blob/b44aa1c508536220f1d0de4a9323cf4bbcc63563/README.md#L155): “| SPARQL 1.1 | **512 / 512** | 0 | 113 | **0** |” (quote found, checked 2026-10-22)
- [HOLOS README, the withdrawn target](https://github.com/pwin/triplestore/blob/b44aa1c508536220f1d0de4a9323cf4bbcc63563/README.md#L106): “it was written before anything was measured” (quote found, checked 2026-10-22)

---

<a id="c04-06"></a>
### C04.06 — A research artefact's implicit expiry date

**In the manual:** [Chapter 4, at the claim](manual/docs/04-from-research-to-industry.md#ev-c04-06) · [plain edition](../docs/04-from-research-to-industry.md#41-different-objective-functions)  
**Kind:** Argument · **Result:** Argument

> an implicit expiry date that does not appear anywhere in its README.

A judgement about maintenance models, not a measurement.

---

<a id="chapter-05"></a>
## 5. GenAI and agents

Annotated chapter: [manual/docs/05-genai-and-agents.md](manual/docs/05-genai-and-agents.md) · plain chapter: [../docs/05-genai-and-agents.md](../docs/05-genai-and-agents.md)

<a id="c05-01"></a>
### C05.01 — Grounding in graphs improves step-wise reasoning and recall

**In the manual:** [Chapter 5, at the claim](manual/docs/05-genai-and-agents.md#ev-c05-01) · [plain edition](../docs/05-genai-and-agents.md#52-semantics-for-ai-the-grounding-direction)  
**Kind:** Argument · **Result:** Argument

> - Grounding each individual reasoning *step* against graph-structured data, rather

Reported results from the literature in the chapter's references; not reproduced here.

---

<a id="c05-02"></a>
### C05.02 — findings.txt is addressed to a person or an agent

**In the manual:** [Chapter 5, at the claim](manual/docs/05-genai-and-agents.md#ev-c05-02) · [plain edition](../docs/05-genai-and-agents.md#what-agents-actually-require-from-you)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> addressed, in its own documentation, to "a person at a terminal, or an agent".

**Sources:**

- [suite docs/REPORTS.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/REPORTS.md#L8): “a person at a terminal, or an agent” (quote found, checked 2026-10-22)

The '[a blank node]' fix it mentions is C07.07 and C07.09.

---

<a id="c05-03"></a>
### C05.03 — Tombstones at 100% apply; guesses at 57% do not

**In the manual:** [Chapter 5, at the claim](manual/docs/05-genai-and-agents.md#ev-c05-03) · [plain edition](../docs/05-genai-and-agents.md#53-agents-as-participants-in-the-pipeline)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> an explicit tombstone comes in at 100% and applies; the same rename guessed from

**Evidence:** the same as [C12.05 — The tombstone is read in both directions; isReplacedBy in one](#c12-05), which reproduces it: step 3 output contains 'employees.rq (confidence 100%)'; step 6 output contains 'employees.rq (confidence 100%)'; step 9 output contains 'employees.rq (confidence 57%)'

---

<a id="c05-04"></a>
### C05.04 — An agent as a principal with roles

**In the manual:** [Chapter 5, at the claim](manual/docs/05-genai-and-agents.md#ev-c05-04) · [plain edition](../docs/05-genai-and-agents.md#53-agents-as-participants-in-the-pipeline)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> service account that reads and writes everything. A store that enforces policy at the

**Evidence:** the same as [C13.06 — Policy at the scan: rows without the column, unless you are in HR](#c13-06), which reproduces it: step 1 output contains '2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None/n    name=Bob, salary=None/n    name=Carol, salary=None', '3. the same, asked by alice with role hr:\n    name=Alice, salary=95000/n    name=Bob, salary=88000/n    name=Carol, salary=102000', '4. COUNT of salaries without the role:\n    n=0', '5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance/n    g=http://example.com/public/n6.', '6. named graphs, with clearance 3:\n    g=http://example.com/provenance/n    g=http://example.com/public/n    g=http://example.com/reviews', '7. salary denied with fail_closed():\n    HolosError: ', 'access denied by policy/n8. (mistake)', '8. (mistake) policy method called as a statement:\n    n=3'

---

<a id="chapter-06"></a>
## 6. Stages and stories

Annotated chapter: [manual/docs/06-stages-and-stories.md](manual/docs/06-stages-and-stories.md) · plain chapter: [../docs/06-stages-and-stories.md](../docs/06-stages-and-stories.md)

<a id="c06-01"></a>
### C06.01 — One practice, three frameworks

**In the manual:** [Chapter 6, at the claim](manual/docs/06-stages-and-stories.md#ev-c06-01) · [plain edition](../docs/06-stages-and-stories.md#6-stages-and-stories)  
**Kind:** Argument · **Result:** Argument

> The SemOps strategy material describes the same practice three times, from three

A reading of the SemOps strategy material, which the manual takes as given. The mapping from each stage to commands is evidenced chapter by chapter in Part III.

---

<a id="chapter-07"></a>
## 7. The toolchain

Annotated chapter: [manual/docs/07-the-toolchain.md](manual/docs/07-the-toolchain.md) · plain chapter: [../docs/07-the-toolchain.md](../docs/07-the-toolchain.md)

<a id="c07-01"></a>
### C07.01 — The versions every Part III number was measured against

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-01) · [plain edition](../docs/07-the-toolchain.md#7-the-toolchain)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **Versions this edition was measured against.**

**Commands** (from the `evidence/` folder):

```bash
python scripts/versions.py
```

<details><summary><code>scripts/versions.py</code></summary>

```python
"""Chapter 7's versions box: what this machine actually has.

    python scripts/versions.py

Prints the PyPI package versions, the release binaries' own --version output and
the npm package versions, the same way the harness records them.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from harness.env import versions  # noqa: E402

for k, v in versions().items():
    print(f"{k:28} {v}")
```

</details>

**What is checked:** the installed packages, release binaries and npm packages are the versions in the table

**Recorded result:** PASS — step 1 output contains 'PyPI ontology-quality-suite  0.24.3', 'PyPI shacl                   0.3.4', 'PyPI holosdb                 0.25.0', 'PyPI tarka-rdf               0.1.1', 'release shacl                shacl 0.3.4', 'release tarka                tarka 0.1.1', 'release holos                holos 0.25.0', 'npm ontology-suite           0.16.1', 'npm shacl-wasm-node          0.3.4', 'npm holos-wasm-node          0.25.0'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/versions.py
python                       3.12.13
platform                     Windows 11 (AMD64)
PyPI ontology-quality-suite  0.24.3
PyPI shacl                   0.3.4
PyPI holosdb                 0.25.0
PyPI tarka-rdf               0.1.1
PyPI rdflib                  7.6.0
PyPI pyoxigraph              0.5.11
PyPI polars                  2.0.0
release shacl                shacl 0.3.4
release tarka                tarka 0.1.1
release holos                holos 0.25.0 (b44aa1c)
node                         v20.19.5
npm ontology-suite           0.16.1
npm shacl-wasm-node          0.3.4
npm holos-wasm-node          0.25.0
npm typescript               7.0.2
java (for HermiT)            openjdk version "25.0.3" 2026-04-21 LTS
oxi-gen (testing repo only)  oxi_gen 0.5.1
[exit 0]
```

</details>

The testing repository was used at [7deaf86](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/7deaf86a523fb313ccf47572df4e7276c779e28e); see C09.15.

---

<a id="c07-02"></a>
### C07.02 — The engine changed and Chapter 9's figures did not

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-02) · [plain edition](../docs/07-the-toolchain.md#7-the-toolchain)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> every figure in Chapter 9 came out the

**Sources:**

- [the previous edition of Chapter 9 (suite 0.14.2, rdflib and pyshacl)](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/09-continuous-integration.md#L56): “Findings: 479 total (55 Violation, 340 Warning, 84 Info)” (quote found, checked 2026-10-22)

Today's figures, on holosdb and the shacl engine, are reproduced in C09.02 (479: 55/340/84), C09.03 (27) and C09.04 (23).

---

<a id="c07-03"></a>
### C07.03 — One registry: 61 checks in ten categories, 44 SPARQL files and 6 shape files

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-03) · [plain edition](../docs/07-the-toolchain.md#71-the-idea-one-registry-two-runtimes-one-set-of-engines)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The suite's quality rules are not code. They are **data**

**Commands** (from the `evidence/` folder):

```bash
python scripts/inspect_packages.py
```

<details><summary><code>scripts/inspect_packages.py</code></summary>

```python
"""Chapter 7: what the four PyPI packages actually install, and what the suite's
check registry holds.

    python scripts/inspect_packages.py

For each package: its version, the console commands it installs (if any) and
its declared runtime dependencies. Then, inside the installed suite: the
registry's entry count, how many portable .rq checks and SHACL shape files ship,
and how many .rq checks guard their message against blank nodes with
IF(isBlank(...)).
"""
import json
import sys
from importlib import metadata, resources
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

for pkg in ("ontology-quality-suite", "shacl", "tarka-rdf", "holosdb"):
    d = metadata.distribution(pkg)
    commands = [ep.name for ep in d.entry_points if ep.group == "console_scripts"]
    reqs = [r for r in (d.requires or []) if "extra ==" not in r]
    print(f"{pkg} {d.version}")
    print(f"    commands installed: {', '.join(commands) if commands else 'none (library only)'}")
    print(f"    runtime dependencies: {', '.join(reqs) if reqs else 'none'}")

res = Path(str(resources.files("ontology_suite") / "resources"))
reg = json.loads((res / "registry.json").read_text(encoding="utf-8"))
entries = reg["checks"] if isinstance(reg, dict) and "checks" in reg else reg
rq = sorted((res / "sparql").rglob("*.rq"))
shapes = sorted((res / "shapes").glob("*.ttl"))
guarded = [p for p in rq if "isBlank(" in p.read_text(encoding="utf-8")]
categories = sorted({e["category"] for e in entries})
print(f"registry entries: {len(entries)} in {len(categories)} categories ({', '.join(categories)})")
print(f"portable .rq checks: {len(rq)}; SHACL shape files: {len(shapes)}")
print(f".rq checks guarding a message with IF(isBlank(...)): {len(guarded)}")
bare = [p for p in rq if "STR(?" in p.read_text(encoding="utf-8") and p not in guarded]
print(f".rq checks building a message with STR(?...) and no isBlank guard: {len(bare)}")
```

</details>

**What is checked:** the installed suite's registry has 61 entries in 10 categories, 44 .rq checks and 6 shape files

**Recorded result:** PASS — step 1 output contains 'registry entries: 61 in 10 categories', 'portable .rq checks: 44; SHACL shape files: 6'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/inspect_packages.py
ontology-quality-suite 0.24.3
    commands installed: ontology-quality-suite
    runtime dependencies: holosdb>=0.24, matplotlib>=3.7.0, owlready2>=0.51, owlrl>=6.0.2, pandas>=2.0.0, rdflib>=7.6.0, shacl<0.4,>=0.3.3, tabulate>=0.9.0
shacl 0.3.4
    commands installed: none (library only)
    runtime dependencies: none
tarka-rdf 0.1.1
    commands installed: none (library only)
    runtime dependencies: polars>=1.30
holosdb 0.25.0
    commands installed: none (library only)
    runtime dependencies: none
registry entries: 61 in 10 categories (conformance, data, efficiency, logical, quality, reasoning, structural, style, tarql, vocabulary)
portable .rq checks: 44; SHACL shape files: 6
.rq checks guarding a message with IF(isBlank(...)): 7
.rq checks building a message with STR(?...) and no isBlank guard: 34
[exit 0]
```

</details>

---

<a id="c07-04"></a>
### C07.04 — The editor runs the same engines at the same versions

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-04) · [plain edition](../docs/07-the-toolchain.md#71-the-idea-one-registry-two-runtimes-one-set-of-engines)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> the 44 portable checks run on **holosdb** in Python and on

**Sources:**

- [extension package.json (0.16.3)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/package.json#L489-L493): “"holos-wasm-node": "^0.25.0",” (quote found, checked 2026-10-22)
- [extension package-lock.json (0.16.3): the holos-wasm-node it bundles](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/package-lock.json): “"node_modules/holos-wasm-node"” (quote found, checked 2026-10-22)
- [suite uv.lock (0.24.3): the holosdb it locks](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/uv.lock#L167-L168): “version = "0.25.0"” (quote found, checked 2026-10-22)
- [HOLOS commit 8b2a949: every query entry point through one pipeline](https://github.com/pwin/triplestore/commit/8b2a9495af52ff56a7ebedd49e9dbd0f1ead93ce): “Send every query entry point through one pipeline” (quote found, checked 2026-10-22)

Below 1.0 a caret admits patch releases only, so `^0.25.0` means 0.25.x. The 0.16.3 release's lock file resolves it to 0.25.0, the version C07.01 shows for holosdb and the CLI, and the suite at 0.24.3 locks holosdb 0.25.0. The extension reaches HOLOS through `queryRdf`, the suite through `Store.query`; from HOLOS 0.24.0 both run the same pipeline. What 0.25.0 changed, its own SHACL validator, is in a part of HOLOS the extension does not call: it validates with shacl-wasm-node.

---

<a id="c07-05"></a>
### C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-05) · [plain edition](../docs/07-the-toolchain.md#the-python-suite)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> That one line now brings both engines: `holosdb` and `shacl` are runtime

**Commands** (from the `evidence/` folder):

```bash
python scripts/inspect_packages.py
```

<details><summary><code>scripts/inspect_packages.py</code></summary>

```python
"""Chapter 7: what the four PyPI packages actually install, and what the suite's
check registry holds.

    python scripts/inspect_packages.py

For each package: its version, the console commands it installs (if any) and
its declared runtime dependencies. Then, inside the installed suite: the
registry's entry count, how many portable .rq checks and SHACL shape files ship,
and how many .rq checks guard their message against blank nodes with
IF(isBlank(...)).
"""
import json
import sys
from importlib import metadata, resources
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

for pkg in ("ontology-quality-suite", "shacl", "tarka-rdf", "holosdb"):
    d = metadata.distribution(pkg)
    commands = [ep.name for ep in d.entry_points if ep.group == "console_scripts"]
    reqs = [r for r in (d.requires or []) if "extra ==" not in r]
    print(f"{pkg} {d.version}")
    print(f"    commands installed: {', '.join(commands) if commands else 'none (library only)'}")
    print(f"    runtime dependencies: {', '.join(reqs) if reqs else 'none'}")

res = Path(str(resources.files("ontology_suite") / "resources"))
reg = json.loads((res / "registry.json").read_text(encoding="utf-8"))
entries = reg["checks"] if isinstance(reg, dict) and "checks" in reg else reg
rq = sorted((res / "sparql").rglob("*.rq"))
shapes = sorted((res / "shapes").glob("*.ttl"))
guarded = [p for p in rq if "isBlank(" in p.read_text(encoding="utf-8")]
categories = sorted({e["category"] for e in entries})
print(f"registry entries: {len(entries)} in {len(categories)} categories ({', '.join(categories)})")
print(f"portable .rq checks: {len(rq)}; SHACL shape files: {len(shapes)}")
print(f".rq checks guarding a message with IF(isBlank(...)): {len(guarded)}")
bare = [p for p in rq if "STR(?" in p.read_text(encoding="utf-8") and p not in guarded]
print(f".rq checks building a message with STR(?...) and no isBlank guard: {len(bare)}")
```

</details>

**What is checked:** ontology-quality-suite declares holosdb (from 0.24 since suite 0.24.3, 0.23 at 0.24.2, 0.15 before), shacl (below 0.4; from 0.3.3 since suite 0.23.0, which needs shacl.rdfs_closure) and owlready2 as runtime dependencies and installs the only command; shacl, tarka-rdf and holosdb install none

**Recorded result:** PASS — step 1 output contains 'commands installed: ontology-quality-suite', 'owlready2>=0.51', 'shacl 0.3.4/n    commands installed: none (library only)', 'tarka-rdf 0.1.1/n    commands installed: none (library only)', 'holosdb 0.25.0/n    commands installed: none (library only)'; suite 0.24.3: step 1 output contains 'shacl<0.4,>=0.3.3'; suite 0.24.3: step 1 output contains 'holosdb>=0.24'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/inspect_packages.py
ontology-quality-suite 0.24.3
    commands installed: ontology-quality-suite
    runtime dependencies: holosdb>=0.24, matplotlib>=3.7.0, owlready2>=0.51, owlrl>=6.0.2, pandas>=2.0.0, rdflib>=7.6.0, shacl<0.4,>=0.3.3, tabulate>=0.9.0
shacl 0.3.4
    commands installed: none (library only)
    runtime dependencies: none
tarka-rdf 0.1.1
    commands installed: none (library only)
    runtime dependencies: polars>=1.30
holosdb 0.25.0
    commands installed: none (library only)
    runtime dependencies: none
registry entries: 61 in 10 categories (conformance, data, efficiency, logical, quality, reasoning, structural, style, tarql, vocabulary)
portable .rq checks: 44; SHACL shape files: 6
.rq checks guarding a message with IF(isBlank(...)): 7
.rq checks building a message with STR(?...) and no isBlank guard: 34
[exit 0]
```

</details>

---

<a id="c07-06"></a>
### C07.06 — STY-003's message vanished on 60 of 65 findings

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-06) · [plain edition](../docs/07-the-toolchain.md#why-own-the-engines)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> On the suite's stress fixture, 60 of 65 findings had no message at

**Sources:**

- [suite commit 9e6f99c](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/9e6f99c420699294917b608a36869500150933e9): “BIND left the variable unbound and the template dropped the message -- 60 of 65 findings on the stress fixture” (quote found, checked 2026-10-22)

---

<a id="c07-07"></a>
### C07.07 — STR() of a blank node: lenient, conformant, and the guard

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-07) · [plain edition](../docs/07-the-toolchain.md#why-own-the-engines)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> What happened next depended on the engine:

**Commands** (from the `evidence/` folder):

```bash
python scripts/engine_leniency.py
```

<details><summary><code>scripts/engine_leniency.py</code></summary>

```python
"""Chapter 7 §7.1: why the suite stopped evaluating on rdflib.

    python scripts/engine_leniency.py

SPARQL 1.1 §17.4.2.5 defines STR() for literals and IRIs. STR() of a blank node
is a type error, so CONCAT errors and BIND leaves the variable unbound. This asks
three engines the question STY-003 used to ask: build a message from a labelled
anonymous restriction.

  rdflib      lenient: returns the blank node's internal identifier
  holosdb     conformant: the message is unbound
  pyoxigraph  conformant: the message is unbound (optional; skipped if absent)

Then two repairs. COALESCE(STR(?e), ...) only helps where STR() raises, so the
lenient engine still prints the internal identifier (Chapter 8 §8.5). The form
the registry now uses, IF(isBlank(...)), every engine answers the same way.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = """@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:   <http://example.org/> .
ex:Thing a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty ex:p ; owl:someValuesFrom ex:Thing ;
                    rdfs:label "an anonymous restriction" ] .
"""
UNGUARDED = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?msg WHERE { ?e rdfs:label ?l . FILTER(isBlank(?e))
  BIND(CONCAT("A label on ", STR(?e), " has no language tag.") AS ?msg) }"""
COALESCED = UNGUARDED.replace('STR(?e)', 'COALESCE(STR(?e), "[a blank node]")')
GUARDED = UNGUARDED.replace('STR(?e)', 'IF(isBlank(?e), "[a blank node]", STR(?e))')


def rdflib_answer(q):
    from rdflib import Graph
    g = Graph()
    g.parse(data=DATA, format="turtle")
    return [str(r.msg) if r.msg is not None else "(unbound)" for r in g.query(q)]


def holosdb_answer(q):
    import tempfile, os
    from holosdb import Store
    with tempfile.NamedTemporaryFile("w", suffix=".ttl", delete=False, encoding="utf-8") as f:
        f.write(DATA)
    try:
        s = Store()
        s.load(f.name)
        out = []
        for r in s.query(q):
            d = r.to_dict()
            out.append(str(d["msg"]) if d.get("msg") is not None else "(unbound)")
        return out
    finally:
        os.unlink(f.name)


def pyoxigraph_answer(q):
    import io
    import pyoxigraph as ox
    st = ox.Store()
    st.load(io.BytesIO(DATA.encode()), format=ox.RdfFormat.TURTLE)
    return [(r["msg"].value if r["msg"] is not None else "(unbound)") for r in st.query(q)]


for label, q in (("unguarded STR(?e)", UNGUARDED), ("COALESCE(STR(?e), ...)", COALESCED),
                 ("guarded IF(isBlank(?e), ...)", GUARDED)):
    print(f"== {label}")
    for name, fn in (("rdflib", rdflib_answer), ("holosdb", holosdb_answer), ("pyoxigraph", pyoxigraph_answer)):
        try:
            print(f"   {name:11} {fn(q)}")
        except ImportError:
            print(f"   {name:11} (not installed)")
```

</details>

**What is checked:** unguarded: rdflib prints an internal identifier, holosdb and pyoxigraph leave the message unbound; COALESCE: rdflib still prints the identifier; IF(isBlank(...)): all three print '[a blank node]'

**Recorded result:** PASS — unguarded: rdflib names an internal identifier; holosdb and pyoxigraph leave the message unbound; COALESCE: rdflib still names the identifier, the other two say '[a blank node]'; IF(isBlank(...)): all three say '[a blank node]'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/engine_leniency.py
== unguarded STR(?e)
   rdflib      ['A label on n7233f7ec05c14d7aba48da44d530ebc2b1 has no language tag.']
   holosdb     ['(unbound)']
   pyoxigraph  ['(unbound)']
== COALESCE(STR(?e), ...)
   rdflib      ['A label on nb19027d1cef6409688dd4246bc41b84fb1 has no language tag.']
   holosdb     ['A label on [a blank node] has no language tag.']
   pyoxigraph  ['A label on [a blank node] has no language tag.']
== guarded IF(isBlank(?e), ...)
   rdflib      ['A label on [a blank node] has no language tag.']
   holosdb     ['A label on [a blank node] has no language tag.']
   pyoxigraph  ['A label on [a blank node] has no language tag.']
[exit 0]
```

</details>

---

<a id="c07-08"></a>
### C07.08 — pyshacl stays as a witness because it caught a real regression

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-08) · [plain edition](../docs/07-the-toolchain.md#why-own-the-engines)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> | `shacl` (SHACL) | pyshacl | pyshacl caught a real regression

**Sources:**

- [suite commit 9e6f99c](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/9e6f99c420699294917b608a36869500150933e9): “pyshacl is what caught the isIRI($this) blank-node regression in shacl 0.1.5” (quote found, checked 2026-10-22)

---

<a id="c07-09"></a>
### C07.09 — Positional dedup, '[a blank node]' in both repositories, owlrl leaves the checks path

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-09) · [plain edition](../docs/07-the-toolchain.md#why-own-the-engines)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The move had costs, and the suite is candid about them.

**Sources:**

- [suite commit 9e6f99c](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/9e6f99c420699294917b608a36869500150933e9): “merge._anonymous_key matches anonymous findings positionally within (check, path, value)” (quote found, checked 2026-10-22)
- [extension commit 7198f91](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/7198f91e256b613503ad385f666460006c4631fe): “The text "[a blank node]" is deliberately identical to the queries'” (quote found, checked 2026-10-22)

---

<a id="c07-10"></a>
### C07.10 — The extension adds six checks of its own: three MDL, three MAL

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-10) · [plain edition](../docs/07-the-toolchain.md#shared-does-not-mean-identical)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Then it adds six of its own with no CLI

**Evidence:** the same as [C08.03 — Six checks only the editor has: three MDL, and since 0.16.0 three MAL](#c08-03) (cited from upstream).

---

<a id="c07-11"></a>
### C07.11 — VOC-001 is declared, not runnable, by the CLI

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-11) · [plain edition](../docs/07-the-toolchain.md#being-in-the-registry-is-not-the-same-as-being-runnable)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Nothing in the Python package implements it; only `registry.json` mentions the id.

**Evidence:** the same as [C08.04 — VOC-001 is declared in the registry but only the extension runs it](#c08-04) (cited from upstream).

---

<a id="c07-12"></a>
### C07.12 — Severity belongs to the shape that produces the result

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-12) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Severity belongs to the shape that produces the result.**

**Inputs:** [`data/shacl/data.ttl`](data/shacl/data.ttl), [`data/shacl/shapes-warning.ttl`](data/shacl/shapes-warning.ttl), [`data/shacl/shapes-warning-on-node.ttl`](data/shacl/shapes-warning-on-node.ttl)

<details><summary><code>data/shacl/data.ttl</code></summary>

```turtle
# Chapter 11: two people, one of them with no name.
@prefix ex: <http://example.org/> .

ex:alice a ex:Person ; ex:name "Alice" .
ex:bob   a ex:Person .
```

</details>

<details><summary><code>data/shacl/shapes-warning.ttl</code></summary>

```turtle
# The same constraint, declared a Warning on the property shape that produces
# the result. Since engine 0.3.0 a Warning still breaks conformance.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:PersonShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:property [ sh:path ex:name ; sh:minCount 1 ; sh:severity sh:Warning ] .
```

</details>

<details><summary><code>data/shacl/shapes-warning-on-node.ttl</code></summary>

```turtle
# The trap: sh:severity on the node shape does not reach the nested property
# shape, which still produces its result at the default severity, Violation.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:PersonShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:severity sh:Warning ;
  sh:property [ sh:path ex:name ; sh:minCount 1 ] .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl -f turtle
shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning-on-node.ttl -f turtle
```

**What is checked:** sh:severity on the property shape gives a Warning; the same declaration on the node shape leaves the property shape's result a Violation

**Recorded result:** PASS — step 1 output contains 'sh:resultSeverity sh:Warning'; step 2 output contains 'sh:resultSeverity sh:Violation'; step 2 output has none of 'sh:resultSeverity sh:Warning'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl -f turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
_:r0 a sh:ValidationReport ;
	sh:conforms false ;
	sh:result _:r1 .
_:r1 a sh:ValidationResult ;
	sh:focusNode <http://example.org/bob> ;
	sh:resultPath <http://example.org/name> ;
	sh:resultSeverity sh:Warning ;
	sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
	sh:sourceShape _:1_b0 .
[exit 1]

$ shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning-on-node.ttl -f turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
_:r0 a sh:ValidationReport ;
	sh:conforms false ;
	sh:result _:r1 .
_:r1 a sh:ValidationResult ;
	sh:focusNode <http://example.org/bob> ;
	sh:resultPath <http://example.org/name> ;
	sh:resultSeverity sh:Violation ;
	sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
	sh:sourceShape _:1_b0 .
[exit 1]
```

</details>

---

<a id="c07-13"></a>
### C07.13 — The registry declares; the directories decide

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-13) · [plain edition](../docs/07-the-toolchain.md#being-in-the-registry-is-not-the-same-as-being-runnable)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> suite's own docs now put it in five words:

**Sources:**

- [suite docs/EXTENDING.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/EXTENDING.md#L29): “The registry declares; the directories decide.” (quote found, checked 2026-10-22)

C08.24 shows a query with no registry entry running and reporting as UNMAPPED.

---

<a id="c07-14"></a>
### C07.14 — Eleven CLI-only checks, three extension-only

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-14) · [plain edition](../docs/07-the-toolchain.md#being-in-the-registry-is-not-the-same-as-being-runnable)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Neither side runs all sixty-one.

**Evidence:** the same as [C08.05 — Eleven checks the editor cannot produce, two held back explicitly](#c08-05) (cited from upstream).

---

<a id="c07-15"></a>
### C07.15 — A sixteen-case comment fixture both repositories carry

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-15) · [plain edition](../docs/07-the-toolchain.md#shared-data-is-not-shared-behaviour)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The fix is a fixture of sixteen cases that **both repositories carry**

**Sources:**

- [suite commit 6295588](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/629558887b2d7fd378229e736be841de8e68ae28): “The cases are hand-written, not generated from either implementation.” (quote found, checked 2026-10-22)
- [extension commit 6489c1a](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/6489c1ae0c17a4cf7c30c2571dd6a605dbd90383): “A fixture of 16 cases now states that, and both repos carry it.” (quote found, checked 2026-10-22)

---

<a id="c07-16"></a>
### C07.16 — --extra native-shacl parses but installs nothing

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-16) · [plain edition](../docs/07-the-toolchain.md#the-python-suite)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> (`uv sync --extra native-shacl` still parses but

**Sources:**

- [suite pyproject.toml (0.22.0)](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/pyproject.toml#L81-L86): “It installs nothing: `shacl` is a runtime dependency now, not an opt-in.” (quote found, checked 2026-10-22)

---

<a id="c07-17"></a>
### C07.17 — A locked dependency does not move with pip --upgrade

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-17) · [plain edition](../docs/07-the-toolchain.md#the-python-suite)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> > **Upgrading a checkout.**

**Sources:**

- [suite commit 1b6000a](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/1b6000aa96742b04b2e70f29d07298bad3770a2d): “uv pip install --upgrade does not move it: uv run re-syncs from uv.lock, so uv lock --upgrade-package is the step.” (quote found, checked 2026-10-22)
- [suite commit 091e0e4](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/091e0e4effe1a9cbaddccc63436851decac09035): “The committed uv.lock had gone stale at 0.14.3” (quote found, checked 2026-10-22)
- [suite uv.lock at the 0.22.0 release](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/749af3e1be749ace3aab3ea4b492d72b3b21dbde/uv.lock#L167-L168): “version = "0.15.0"” (quote found, checked 2026-10-22)

---

<a id="c07-18"></a>
### C07.18 — Oxigraph went in 0.13.11; the .vsix shrank from 20.2 to 17.5 MB

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-18) · [plain edition](../docs/07-the-toolchain.md#the-vs-code-extension)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> went in 0.13.11, and the `.vsix` dropped from 20.2 MB to 17.5 MB with it.

**Sources:**

- [extension commit e4583b9](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/e4583b9a9d47f678bba2e5efaba7b7d0b21ca504): “The vsix goes from 20.22 MB to 17.52 MB.” (quote found, checked 2026-10-22)

---

<a id="c07-19"></a>
### C07.19 — vsce --no-dependencies packages an extension with no engines

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-19) · [plain edition](../docs/07-the-toolchain.md#the-vs-code-extension)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> `vsce package --no-dependencies`

**Sources:**

- [extension commit ec96b93](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/ec96b93b163f8c11b85cf90ecc5c9151f927c0b6): “contains none of the engines” (quote found, checked 2026-10-22)

---

<a id="c07-20"></a>
### C07.20 — Only ontology-quality-suite installs a command

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-20) · [plain edition](../docs/07-the-toolchain.md#the-engine-the-store-and-the-triplifier)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The wheels are libraries only.**

**Evidence:** the same as [C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries](#c07-05), which reproduces it: step 1 output contains 'commands installed: ontology-quality-suite', 'owlready2>=0.51', 'shacl 0.3.4/n    commands installed: none (library only)', 'tarka-rdf 0.1.1/n    commands installed: none (library only)', 'holosdb 0.25.0/n    commands installed: none (library only)'; suite 0.24.3: step 1 output contains 'shacl<0.4,>=0.3.3'; suite 0.24.3: step 1 output contains 'holosdb>=0.24'

---

<a id="c07-21"></a>
### C07.21 — Each release carries SHA256SUMS

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-21) · [plain edition](../docs/07-the-toolchain.md#the-engine-the-store-and-the-triplifier)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Windows, each release with a `SHA256SUMS` file. Check it.

<details><summary><code>tools/fetch_binaries.py</code></summary>

```python
"""Download the three release binaries the evidence uses, and check them.

    python tools/fetch_binaries.py

For this machine's platform, fetches `shacl` (SHACL Engine 0.3.4), `tarka`
(0.1.1) and `holos` + `holos-server` (HOLOS 0.25.0) from their GitHub releases,
verifies each archive against the release's SHA256SUMS, and unpacks it under
evidence/bin/. Nothing is installed anywhere else. If a binary is already
there, it is left alone; a superseded version of it is removed.
"""
import hashlib
import io
import platform
import shutil
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
RELEASES = {
    "shacl": ("pwin/SHACL_Engine", "v0.3.4", "shacl-0.3.4-{target}"),
    "tarka": ("pwin/tarka", "v0.1.1", "tarka-0.1.1-{target}"),
    "holos": ("pwin/triplestore", "v0.25.0", "holos-0.25.0-{target}"),
}


def target() -> str:
    system, machine = platform.system(), platform.machine().lower()
    arm = machine in ("arm64", "aarch64")
    if system == "Windows":
        return "x86_64-pc-windows-msvc"
    if system == "Darwin":
        return "aarch64-apple-darwin" if arm else "x86_64-apple-darwin"
    return "aarch64-unknown-linux-gnu" if arm else "x86_64-unknown-linux-gnu"


def get(url: str) -> bytes:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as exc:  # transient network errors happen; retry a few times
            if attempt == 4:
                raise
            print(f"    retrying after {exc}")
            time.sleep(3)
    raise RuntimeError("unreachable")


def main() -> int:
    t = target()
    ext = ".zip" if "windows" in t else ".tar.gz"
    for tool, (repo, tag, stem) in RELEASES.items():
        dest = BIN / tool
        folder = dest / stem.format(target=t)
        if folder.is_dir() and any(folder.rglob(tool + (".exe" if "windows" in t else ""))):
            print(f"{tool}: {tag} already present under {folder}")
            continue
        asset = stem.format(target=t) + ext
        base = f"https://github.com/{repo}/releases/download/{tag}/"
        print(f"{tool}: fetching {asset}")
        sums = get(base + "SHA256SUMS").decode()
        want = next((l.split()[0] for l in sums.splitlines() if l.strip().endswith(asset)), None)
        if not want:
            print(f"    {asset} is not listed in SHA256SUMS; this platform may not be built for {tag}")
            return 1
        blob = get(base + asset)
        have = hashlib.sha256(blob).hexdigest()
        if have != want:
            print(f"    checksum mismatch: expected {want}, got {have}")
            return 1
        print(f"    sha256 {have[:16]}... matches SHA256SUMS")
        dest.mkdir(parents=True, exist_ok=True)
        if ext == ".zip":
            zipfile.ZipFile(io.BytesIO(blob)).extractall(dest)
        else:
            tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz").extractall(dest, filter="data")
            for p in dest.rglob("*"):
                if p.is_file() and p.name.startswith(tool):
                    p.chmod(0o755)
        # Only the pinned version stays: the harness takes the first binary it
        # finds, so a superseded one left beside it could be the one that runs.
        for old in dest.iterdir():
            if old.is_dir() and old != folder:
                shutil.rmtree(old)
                print(f"    removed the superseded {old.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

</details>

**Sources:**

- [SHACL Engine v0.3.4 release](https://github.com/pwin/SHACL_Engine/releases/tag/v0.3.4)
- [HOLOS v0.25.0 release](https://github.com/pwin/triplestore/releases/tag/v0.25.0)
- [tarka v0.1.1 release](https://github.com/pwin/tarka/releases/tag/v0.1.1)

`tools/fetch_binaries.py` downloads each archive and refuses one whose SHA-256 does not match the release's SHA256SUMS; the binaries used throughout this evidence came through it.

---

<a id="c07-22"></a>
### C07.22 — --engine: native misses QUA-004; sparql and both give 23

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-22) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> All modes, against this manual's fixture with `--own-namespace`, same ontology,

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine native --out-dir work/C07_22/native --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine shacl --out-dir work/C07_22/shacl --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_22/sparql --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine native+sparql --out-dir work/C07_22/nativesparql --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine both --out-dir work/C07_22/both --fail-on never --reports minimal
```

**What is checked:** native and shacl: 22 (1 V, 21 W); sparql, native+sparql and both: 23 (1 V, 22 W); QUA-004 is the only difference

**Recorded result:** PASS — step 1: 22 findings (1 V, 21 W, 0 I); step 2: 22 findings (1 V, 21 W, 0 I); step 3: 23 findings (1 V, 22 W, 0 I); step 4: 23 findings (1 V, 22 W, 0 I); step 5: 23 findings (1 V, 22 W, 0 I); QUA-004 appears under sparql and not under native; and is the only difference between them

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine native --out-dir work/C07_22/native --fail-on never --reports minimal
Findings: 22 total (1 Violation, 21 Warning, 0 Info)
Reports written to: ./work/C07_22/native
  - work/C07_22/native/findings.txt (start here -- what, where, and the source line)
  - work/C07_22/native/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine shacl --out-dir work/C07_22/shacl --fail-on never --reports minimal
Findings: 22 total (1 Violation, 21 Warning, 0 Info)
Reports written to: ./work/C07_22/shacl
  - work/C07_22/shacl/findings.txt (start here -- what, where, and the source line)
  - work/C07_22/shacl/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_22/sparql --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C07_22/sparql
  - work/C07_22/sparql/findings.txt (start here -- what, where, and the source line)
  - work/C07_22/sparql/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine native+sparql --out-dir work/C07_22/nativesparql --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C07_22/nativesparql
  - work/C07_22/nativesparql/findings.txt (start here -- what, where, and the source line)
  - work/C07_22/nativesparql/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine both --out-dir work/C07_22/both --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C07_22/both
  - work/C07_22/both/findings.txt (start here -- what, where, and the source line)
  - work/C07_22/both/full_results.csv
[exit 0]
```

</details>

---

<a id="c07-23"></a>
### C07.23 — The engine choice is not about speed at this size

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-23) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> On the unscoped run the three take about 1.7 s (`native`), 2.0 s (`sparql`) and

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine native --out-dir work/C07_23/native --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine native+sparql --out-dir work/C07_23/both --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C07_23/sparql --fail-on never --reports minimal
```

**What is checked:** nothing is asserted about the times; they are recorded. Each run must succeed

**Recorded result:** PASS — whole-process times: native 3.9 s, native+sparql 3.7 s, sparql 4.1 s

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine native --out-dir work/C07_23/native --fail-on never --reports minimal
Findings: 286 total (6 Violation, 198 Warning, 82 Info)
Reports written to: ./work/C07_23/native
  - work/C07_23/native/findings.txt (start here -- what, where, and the source line)
  - work/C07_23/native/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine native+sparql --out-dir work/C07_23/both --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C07_23/both
  - work/C07_23/both/findings.txt (start here -- what, where, and the source line)
  - work/C07_23/both/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C07_23/sparql --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C07_23/sparql
  - work/C07_23/sparql/findings.txt (start here -- what, where, and the source line)
  - work/C07_23/sparql/full_results.csv
[exit 0]
```

</details>

Times vary by machine. Three repeated runs here gave native 1.7 s, sparql 2.0–2.1 s and native+sparql 2.1–2.3 s.

---

<a id="c07-24"></a>
### C07.24 — Until 0.6.0 the shapes put sh:severity in the wrong place

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-24) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **The severity lesson is about shape authoring, not engines.**

**Sources:**

- [this manual's earlier edition (14 August 2026, suite 0.5.x), measured then](https://github.com/pwin/SemOpsManual/blob/aba4679abe7456c70fd638ae18e0084e07f2f3b1/docs/07-the-toolchain.md#L197-L198): “`both` reports **five Violations where `native+sparql` reports two**” (quote found, checked 2026-10-22)
- [suite commit 2f4950c (0.6.0)](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/2f4950c4436868fb6ea203c0ce271727b256cfef): “sh:severity was declared inside each sh:sparql [...] SPARQLConstraint block rather than on the enclosing shape, where SHACL defines it.” (quote found, checked 2026-10-22)

The commit gives its own measurement on a different fixture: 17 V / 1 W / 0 I under pyshacl against 1 / 15 / 2 under the native engine, for the same 18 findings.

---

<a id="c07-25"></a>
### C07.25 — My own node-shape severity mistake

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-25) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> I tripped over the same thing myself while testing the engine for this

**Evidence:** the same as [C07.12 — Severity belongs to the shape that produces the result](#c07-12), which reproduces it: step 1 output contains 'sh:resultSeverity sh:Warning'; step 2 output contains 'sh:resultSeverity sh:Violation'; step 2 output has none of 'sh:resultSeverity sh:Warning'

---

<a id="c07-26"></a>
### C07.26 — --inference owlrl is refused: a traceback at 0.22.0, a usage error from 0.23.0

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-26) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **`--inference owlrl` and `both` are gone from the checks path.**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --inference owlrl --out-dir work/C07_26/owlrl --fail-on never --reports minimal
ontology-quality-suite checks --help
```

**What is checked:** --inference owlrl exits non-zero. At 0.22.0, with a Python traceback ending in the ValueError, and --help lists owlrl and both; from 0.23.0, with a one-line usage error, and --help offers none and rdfs only

**Recorded result:** PASS — step 1 exits non-zero (2); suite 0.24.3: step 1 output contains "argument --inference: invalid choice: 'owlrl'"; step 1 output has none of 'Traceback'; step 2 output contains '--inference {none,rdfs}'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --inference owlrl --out-dir work/C07_26/owlrl --fail-on never --reports minimal
usage: ontology-quality-suite checks [-h] [--ontology ONTOLOGY] [--data DATA]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--shapes SHAPES] [--sparql SPARQL]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--inference {none,rdfs}]
                                     [--engine {both,sparql,shacl,native,native+sparql}]
                                     [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [--own-namespace OWN_NAMESPACE] [-v]
ontology-quality-suite checks: error: argument --inference: invalid choice: 'owlrl' (choose from none, rdfs)
[exit 2]

$ ontology-quality-suite checks --help
usage: ontology-quality-suite checks [-h] [--ontology ONTOLOGY] [--data DATA]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--shapes SHAPES] [--sparql SPARQL]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--inference {none,rdfs}]
                                     [--engine {both,sparql,shacl,native,native+sparql}]
                                     [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [--own-namespace OWN_NAMESPACE] [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --data DATA
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --shapes SHAPES
  --sparql SPARQL       a directory of .rq check queries, or @builtin for the
                        suite's own tree wherever this install put it.
                        Repeatable: pass it more than once to run a project's
                        own checks alongside the suite's, which is what you
                        almost always want. Given at all, it replaces the
                        built-in tree, so `--sparql mine` runs only yours --
                        the run warns when that happens. See
… (48 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

---

<a id="c07-27"></a>
### C07.27 — --inference rdfs: half the suite at 0.22.0, every engine from 0.23.0

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-27) · [plain edition](../docs/07-the-toolchain.md#--engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **And `--inference rdfs` reached only half the suite until 0.23.0.**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference owlrl --out-dir work/C07_27/owlrl --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference rdfs --out-dir work/C07_27/rdfs --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference none --out-dir work/C07_27/none --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --inference rdfs --out-dir work/C07_27/both-rdfs --fail-on never --reports minimal
python scripts/diff_findings.py work/C07_27/none/full_results.csv work/C07_27/rdfs/full_results.csv
```

**What is checked:** at 0.22.0: under --engine sparql, owlrl, rdfs and none give 479 each, exit 0, and the default engine with rdfs gives 497. From 0.23.0: owlrl is refused; rdfs gives 489 under sparql and under the default engine alike, against 479 without it; the closure gains 21 findings (STR-007 9, STY-003 9, STR-009 3) and loses 11 (STR-007 9, STR-006, DAT-002)

**Recorded result:** PASS — suite 0.24.3: step 1 exits non-zero (2); step 2: 489 findings (57 V, 339 W, 93 I); step 3: 479 findings (55 V, 340 W, 84 I); step 4: 489 findings (57 V, 339 W, 93 I); step 5 output contains 'gained 21:', 'STR-007 9', 'STY-003 9', 'STR-009 3', 'lost 11:', 'STR-006 1', 'DAT-002 1'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference owlrl --out-dir work/C07_27/owlrl --fail-on never --reports minimal
usage: ontology-quality-suite checks [-h] [--ontology ONTOLOGY] [--data DATA]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--shapes SHAPES] [--sparql SPARQL]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--inference {none,rdfs}]
                                     [--engine {both,sparql,shacl,native,native+sparql}]
                                     [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [--own-namespace OWN_NAMESPACE] [-v]
ontology-quality-suite checks: error: argument --inference: invalid choice: 'owlrl' (choose from none, rdfs)
[exit 2]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference rdfs --out-dir work/C07_27/rdfs --fail-on never --reports minimal
Findings: 489 total (57 Violation, 339 Warning, 93 Info)
Reports written to: ./work/C07_27/rdfs
  - work/C07_27/rdfs/findings.txt (start here -- what, where, and the source line)
  - work/C07_27/rdfs/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --inference none --out-dir work/C07_27/none --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C07_27/none
  - work/C07_27/none/findings.txt (start here -- what, where, and the source line)
  - work/C07_27/none/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --inference rdfs --out-dir work/C07_27/both-rdfs --fail-on never --reports minimal
Findings: 489 total (57 Violation, 339 Warning, 93 Info)
Reports written to: ./work/C07_27/both-rdfs
  - work/C07_27/both-rdfs/findings.txt (start here -- what, where, and the source line)
  - work/C07_27/both-rdfs/full_results.csv
[exit 0]

$ python scripts/diff_findings.py work/C07_27/none/full_results.csv work/C07_27/rdfs/full_results.csv
gained 21: STR-007 9, STY-003 9, STR-009 3
lost 11: STR-007 9, DAT-002 1, STR-006 1
before 479, after 489
[exit 0]
```

</details>

**Sources:**

- [suite pipeline.py at 0.22.0: inference applied inside `if uses_shacl:`](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/749af3e1be749ace3aab3ea4b492d72b3b21dbde/ontology_suite/pipeline.py#L141-L168): “if inference not in ("none", "rdfs"):” (quote found, checked 2026-10-22)
- [suite commit d7d7a98, the fix](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/d7d7a987cb754221b6c57a5997445628e219851b): “The closure is now materialised once, centrally, and both arms read the result.” (quote found, checked 2026-10-22)

---

<a id="c07-28"></a>
### C07.28 — --verbose shows what each input resolved to

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-28) · [plain edition](../docs/07-the-toolchain.md#--verbose)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Every subcommand takes `-v`/`--verbose`, which prints what each input option

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_28/v --fail-on never --reports minimal -v
```

**What is checked:** the run names both resolved imports and the file each came from, and the engine

**Recorded result:** PASS — step 1 output contains '2 owl:imports resolved:', 'http://xmlns.com/foaf/0.1/  <-  ', 'http://www.w3.org/ns/org#  <-  ', '[verbose] engine: sparql'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_28/v --fail-on never --reports minimal -v
[verbose] fixtures/acme_robotics/acme-org-v1.ttl:
  2 owl:imports resolved:
    http://www.w3.org/ns/org#  <-  fixtures/acme_robotics/reference_vocab/org.ttl
    http://xmlns.com/foaf/0.1/  <-  fixtures/acme_robotics/reference_vocab/foaf.rdf
[verbose] engine: sparql
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C07_28/v
  - work/C07_28/v/findings.txt (start here -- what, where, and the source line)
  - work/C07_28/v/full_results.csv
[exit 0]
```

</details>

---

<a id="c07-29"></a>
### C07.29 — Each deliberate flaw produces exactly one finding

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-29) · [plain edition](../docs/07-the-toolchain.md#75-the-fixture-used-throughout-part-iii)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Each deliberate flaw produces **exactly one finding**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_29/own --fail-on never --reports minimal
python scripts/summarise_findings.py work/C07_29/own/full_results.csv
```

**What is checked:** LOG-001 on acme:Contractor, QUA-001 and QUA-004 on acme:hasSkill, STY-002 and STR-003 on acme:reports_to, each once; and QUA-009 and QUA-010 nine times each

**Recorded result:** PASS — LOG-001 on Contractor, QUA-001 and QUA-004 on hasSkill, STY-002 and STR-003 on reports_to; each exactly once; own/full_results.csv: {'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --out-dir work/C07_29/own --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C07_29/own
  - work/C07_29/own/findings.txt (start here -- what, where, and the source line)
  - work/C07_29/own/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C07_29/own/full_results.csv
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x QUA-001  Warning   Class or property missing rdfs:label
  1 x QUA-004  Warning   Resource missing skos:prefLabel
  9 x QUA-009  Warning   Class or property without one skos:prefLabel per language
  9 x QUA-010  Warning   Class or property without a skos:definition
  1 x STR-003  Warning   Property missing both domain and range
  1 x STY-002  Warning   Property name not lowerCamelCase
total 23: 1 Violation, 22 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c07-30"></a>
### C07.30 — v2 renames Engineer, with a migration annotation, and adds a class and a property

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-30) · [plain edition](../docs/07-the-toolchain.md#75-the-fixture-used-throughout-part-iii)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `acme-org-v2.ttl` is a plausible next release.

**Evidence:** the same as [C12.01 — version-diff: the verdict comes from the axioms](#c12-01), which reproduces it: step 1 output contains 'Removed classes [MAJOR]:\n  - https://acme.example.org/ns/Engineer', 'https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee', 'Added classes [minor]:\n  - https://acme.example.org/ns/ProductManager/n  - https://acme.example.org/ns/SoftwareEngineer', 'Added properties [minor]:\n  - https://acme.example.org/ns/hireDate', 'Added equivalentClass axioms [minor]:\n  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer', 'Suggested version bump: MAJOR'; step 2 output contains 'diff.json', 'diff.txt'; step 3 exits non-zero (1)

---

<a id="c07-31"></a>
### C07.31 — The testing repository: seventeen fixtures, a 38-question board

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-31) · [plain edition](../docs/07-the-toolchain.md#76-where-the-deeper-documentation-lives)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> holds seventeen deliberately broken ontologies, a 38-question competency board

**Evidence:** the same as [C09.19 — Seventeen fixtures; 58 of 61 checks pinned](#c09-19) (cited from upstream).

---

<a id="c07-32"></a>
### C07.32 — A lenient engine let a check pass in tests and fail in the field

**In the manual:** [Chapter 7, at the claim](manual/docs/07-the-toolchain.md#ev-c07-32) · [plain edition](../docs/07-the-toolchain.md#7-the-toolchain)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **A lenient engine let a check pass in the

**Evidence:** the same as [C07.07 — STR() of a blank node: lenient, conformant, and the guard](#c07-07), which reproduces it: unguarded: rdflib names an internal identifier; holosdb and pyoxigraph leave the message unbound; COALESCE: rdflib still names the identifier, the other two say '[a blank node]'; IF(isBlank(...)): all three say '[a blank node]'

---

<a id="chapter-08"></a>
## 8. Model and validate

Annotated chapter: [manual/docs/08-model-and-validate.md](manual/docs/08-model-and-validate.md) · plain chapter: [../docs/08-model-and-validate.md](../docs/08-model-and-validate.md)

<a id="c08-01"></a>
### C08.01 — Outline prompts resolve restriction names since 0.14.0

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-01) · [plain edition](../docs/08-model-and-validate.md#structure-you-can-see)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Since 0.14.0 a restriction typed into those prompts resolves its names

**Sources:**

- [extension CHANGELOG, 0.16.0: MAL-003, and Local Checks no longer fails on one](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L99-L107): “The statements that use a relative IRI are now reported” (quote found, checked 2026-10-22)
- [extension CHANGELOG, 0.14.0](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L235-L244): “search it for the regular expression `<[^:>]+>`” (quote found, checked 2026-10-22)
- [extension commit d480ace (first released in v0.14.0)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/d480ace5adc99616ca36ca563af8feb3cb2fb99d) (exists, checked 2026-10-22)

---

<a id="c08-02"></a>
### C08.02 — Run Local Checks reads 44 SPARQL and 6 SHACL files from the 61-check registry

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-02) · [plain edition](../docs/08-model-and-validate.md#live-diagnostics-including-one-shacl-cannot-give-you)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> *Run Local Checks* evaluates the 44 SPARQL and 6 SHACL check files

**Evidence:** the same as [C07.03 — One registry: 61 checks in ten categories, 44 SPARQL files and 6 shape files](#c07-03), which reproduces it: step 1 output contains 'registry entries: 61 in 10 categories', 'portable .rq checks: 44; SHACL shape files: 6'

The editor and the CLI read the same registry; C07.03 counts it in the installed suite package.

---

<a id="c08-03"></a>
### C08.03 — Six checks only the editor has: three MDL, and since 0.16.0 three MAL

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-03) · [plain edition](../docs/08-model-and-validate.md#live-diagnostics-including-one-shacl-cannot-give-you)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> It also runs **six checks the CLI does not have**.

**Sources:**

- [extension src/checks/modellingGuidance.test.ts](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/modellingGuidance.test.ts#L20-L24): “MDL-002: ex:Veterinarian owl:equivalentClass ex:AnimalDoctor” (quote found, checked 2026-10-22)
- [extension src/checks/malformed.ts (0.16.0)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/malformed.ts#L10-L15): “MAL-001: a qualified cardinality written with owl:cardinality (or min/max) beside owl:onClass.” (quote found, checked 2026-10-22)
- [extension CHANGELOG, 0.16.0](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L108-L113): “this extension's own rather than the registry's” (quote found, checked 2026-10-22)

Neither family is in the shared registry.json, which is why the CLI cannot produce them.

---

<a id="c08-04"></a>
### C08.04 — VOC-001 is declared in the registry but only the extension runs it

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-04) · [plain edition](../docs/08-model-and-validate.md#live-diagnostics-including-one-shacl-cannot-give-you)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> It is in the registry; the CLI still cannot produce it.

**Sources:**

- [suite tests/test_check_coverage.py, EXTENSION_ONLY_IDS](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/tests/test_check_coverage.py#L94-L97): “checks/vocabularyChecks.ts -- a closed-world scan of the axiom positions” (quote found, checked 2026-10-22)
- [extension src/checks/registryCoverage.test.ts](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/registryCoverage.test.ts#L25-L27): “the three checks only *this* extension can produce, VOC-001/REA-005/REA-006” (quote found, checked 2026-10-22)

C08.06 shows the consequence: the CLI reports the typo as STR-001, never as VOC-001.

---

<a id="c08-05"></a>
### C08.05 — Eleven checks the editor cannot produce, two held back explicitly

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-05) · [plain edition](../docs/08-model-and-validate.md#live-diagnostics-including-one-shacl-cannot-give-you)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **Eleven go the other way.**

**Sources:**

- [extension registryCoverage.test.ts, CLI_ONLY](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/registryCoverage.test.ts#L33-L61): “'TQL-004', 'TQL-005',” (quote found, checked 2026-10-22)
- [the same test: a query it cannot run is not counted](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/registryCoverage.test.ts#L99-L107): “make the CLI_ONLY list above assert something false while still passing” (quote found, checked 2026-10-22)

CLI_ONLY lists REA-020, REA-021, REA-022, REA-010, REA-011, REA-012, CNF-001, CNF-002, CNF-005, TQL-004 and TQL-005: eleven.

---

<a id="c08-06"></a>
### C08.06 — The CLI catches the typo as STR-001, not VOC-001

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-06) · [plain edition](../docs/08-model-and-validate.md#live-diagnostics-including-one-shacl-cannot-give-you)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Run against that file, the CLI reports `STR-001`; `VOC-001` is not among its findings.

**Inputs:** [`data/typo/typo-data.ttl`](data/typo/typo-data.ttl)

<details><summary><code>data/typo/typo-data.ttl</code></summary>

```turtle
# Chapter 8: a data graph with one transposed class name.
# acme:Empolyee is not declared anywhere; acme:Employee is.
@prefix acme: <https://acme.example.org/ns/> .
@prefix ex:   <https://acme.example.org/data/> .

ex:bob a acme:Empolyee .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --data data/typo/typo-data.ttl --engine sparql --out-dir work/C08_06/typo --fail-on never --reports minimal
python scripts/summarise_findings.py work/C08_06/typo/full_results.csv --by focus --check STR-001
```

**What is checked:** STR-001 fires once, on acme:Empolyee; VOC-001 does not appear

**Recorded result:** PASS — typo/full_results.csv: {'QUA-004': 2, 'QUA-005': 1, 'STR-001': 1}; step 2 output contains 'value=https://acme.example.org/ns/Empolyee'; no VOC-001 finding

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --data data/typo/typo-data.ttl --engine sparql --out-dir work/C08_06/typo --fail-on never --reports minimal
Findings: 4 total (1 Violation, 3 Warning, 0 Info)
Reports written to: ./work/C08_06/typo
  - work/C08_06/typo/findings.txt (start here -- what, where, and the source line)
  - work/C08_06/typo/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C08_06/typo/full_results.csv --by focus --check STR-001
STR-001  focus=https://acme.example.org/data/bob  path=-  value=https://acme.example.org/ns/Empolyee
total 1: 1 Violation, 0 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c08-07"></a>
### C08.07 — Sixteen checks offer a Quick Fix

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-07) · [plain edition](../docs/08-model-and-validate.md#quick-fix-with-the-diff-shown-first)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Sixteen checks offer a one-click lightbulb repair

**Sources:**

- [extension resources/checks-registry/repairs/manifest.json](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/resources/checks-registry/repairs/manifest.json): “PRJ-REQUIRED” (quote found, checked 2026-10-22)

The manifest's `checks` object has 16 keys: LOG-003, MDL-001, MDL-002, MDL-003, PRJ-REQUIRED, QUA-001, QUA-002, QUA-004, QUA-005, QUA-007, STR-001, STR-002, STR-005, STR-007, STR-008, STY-003.

---

<a id="c08-08"></a>
### C08.08 — Blank nodes cross the repair boundary as skolem IRIs

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-08) · [plain edition](../docs/08-model-and-validate.md#quick-fix-with-the-diff-shown-first)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **It nearly renamed every blank node in the file.**

**Sources:**

- [extension CHANGELOG, 0.13.11](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L362-L372): “Blank nodes now cross the boundary as IRIs and come back as blank nodes” (quote found, checked 2026-10-22)
- [extension commit e4583b9](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/e4583b9a9d47f678bba2e5efaba7b7d0b21ca504) (exists, checked 2026-10-22)

---

<a id="c08-09"></a>
### C08.09 — A literal's base direction survives a repair since 0.13.12

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-09) · [plain edition](../docs/08-model-and-validate.md#quick-fix-with-the-diff-shown-first)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **It dropped a literal's base direction.**

**Sources:**

- [extension CHANGELOG, 0.13.12](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L323-L328): “datatype from `rdf:dirLangString` to `rdf:langString` in the user's own file” (quote found, checked 2026-10-22)
- [extension commit e3364fc (first released in v0.13.12)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/e3364fc5bf6b7a7c5028d5e868b5b3c12164ae2c) (exists, checked 2026-10-22)

---

<a id="c08-10"></a>
### C08.10 — Refactoring masks comments since 0.13.5

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-10) · [plain edition](../docs/08-model-and-validate.md#refactoring-that-knows-what-is-a-comment)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> All three depend on one decision, *which text counts as code*

**Sources:**

- [extension commit 71981b4 (first released in v0.13.5)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/71981b41283528abbd6fa509a2ffa8c3bd231270): “Stop reading CURIEs out of comments” (quote found, checked 2026-10-22)
- [extension CHANGELOG, 0.13.5](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L497): “a line whose *first* non-space character was `#`” (quote found, checked 2026-10-22)

---

<a id="c08-11"></a>
### C08.11 — The unresolved-import warning names where it looked

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-11) · [plain edition](../docs/08-model-and-validate.md#a-warning-that-says-where-it-actually-looked)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> It now names the directory it searched and how

**Sources:**

- [extension CHANGELOG, 0.13.5](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L547): “It now names the directory it searched and how many ontology files it found” (quote found, checked 2026-10-22)

---

<a id="c08-12"></a>
### C08.12 — The DSL script type-checks and builds against the npm package

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-12) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified against the published 0.16.1 package.

**Commands** (from the `evidence/` folder):

```bash
node -p "require('./node_modules/ontology-suite/package.json').version"
node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/acme.ontology.ts
node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_12/acme.ttl
python scripts/query_file.py work/C08_12/acme.ttl "SELECT (COUNT(*) AS ?triples) WHERE { ?s ?p ?o }"
```

<details><summary><code>scripts/dsl/acme.ontology.ts</code></summary>

```typescript
// Chapter 8 §8.2: the Acme fixture's core, written with the ontology-suite DSL,
// deliberate contradiction included. Run with tsx; writes Turtle to argv[2].
//
//   node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_10/acme.ttl
import { ontology, defontology, defclass, defobjectproperty,
         defdatatypeproperty, datatype, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';
import { writeFileSync } from 'node:fs';

ontology('https://acme.example.org/ns/', 'acme');
defontology('https://acme.example.org/ns/1.0.0', { label: 'Acme Robotics org chart' });

const Department = defclass('Department', { label: [{ value: 'Department', language: 'en' }] });
const Employee   = defclass('Employee',   { label: [{ value: 'Employee',   language: 'en' }] });
defclass('Engineer', { subClassOf: [Employee] });

// The fixture's contradiction, written as code.
defclass('Contractor', { subClassOf: [Employee], disjointWith: [Employee] });

defobjectproperty('worksIn', { domain: Employee, range: Department });
defdatatypeproperty('hasEmployeeId', { domain: Employee, range: datatype('xsd:string') });

const { quads, prefixes } = build();
const w = new Writer({ prefixes });
// No cast: from 0.16.1 the bundled Quad type is n3's (C08.16). Up to 0.16.0
// this line needed `quads as any` to compile, though it ran.
w.addQuads(quads);
w.end((_e: unknown, ttl: string) => writeFileSync(process.argv[2], ttl));
```

</details>

**What is checked:** the installed package is 0.16.1; tsc reports no errors; the script runs and writes Turtle

**Recorded result:** PASS — step 1 output contains '0.16.1'; step 2 exits 0; step 3 exits 0; step 4 exits 0

<details><summary>Output, as recorded</summary>

```text
$ node -p "require('./node_modules/ontology-suite/package.json').version"
0.16.1
[exit 0]

$ node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/acme.ontology.ts

[exit 0]

$ node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_12/acme.ttl

[exit 0]

$ python scripts/query_file.py work/C08_12/acme.ttl "SELECT (COUNT(*) AS ?triples) WHERE { ?s ?p ?o }"
triples
17
[exit 0]
```

</details>

The script is the manual's listing plus four lines that write the Turtle to a file. Those lines hand build().quads to n3's Writer without a cast, which compiles from 0.16.1 (C08.16).

---

<a id="c08-13"></a>
### C08.13 — tsc refuses a bare string as a datatype range (TS2322)

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-13) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The type checker catches a mistake of kind.**

**Commands** (from the `evidence/` folder):

```bash
node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/bad-range.ontology.ts
```

<details><summary><code>scripts/dsl/bad-range.ontology.ts</code></summary>

```typescript
// Chapter 8 §8.2: a mistake of kind. Since 0.15.0 a datatype property's range
// is a datatype, made with datatype('xsd:string'), not a bare string. The type
// checker refuses this file; run without it, the DSL throws an internal TypeError.
import { ontology, defclass, defdatatypeproperty } from 'ontology-suite/dsl';

ontology('https://acme.example.org/ns/', 'acme');
const Employee = defclass('Employee');
defdatatypeproperty('hasEmployeeId', { domain: Employee, range: 'xsd:string' });
```

</details>

**What is checked:** tsc exits non-zero with TS2322, 'string' not assignable to 'DatatypeRef'

**Recorded result:** PASS — step 1 exits non-zero (1); step 1 output contains "error TS2322: Type 'string' is not assignable to type 'DatatypeRef'."

<details><summary>Output, as recorded</summary>

```text
$ node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/bad-range.ontology.ts
scripts/dsl/bad-range.ontology.ts(8,58): error TS2322: Type 'string' is not assignable to type 'DatatypeRef'.
[exit 1]
```

</details>

The manual quotes the error at line 16 of its first draft; this file is shorter, so the line and column differ.

---

<a id="c08-14"></a>
### C08.14 — The gate catches the contradiction in the script's output

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-14) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The gate catches a mistake of logic.**

**Commands** (from the `evidence/` folder):

```bash
node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_14/acme.ttl
PYTHONHASHSEED=0 ontology-quality-suite ontology --ontology work/C08_14/acme.ttl --out-dir work/C08_14/gate --fail-on Violation --reports minimal
```

**What is checked:** the ontology stage exits 1, with LOG-001 on acme:Contractor in findings.txt

**Recorded result:** PASS — step 2 exits 1; gate/full_results.csv: {'LOG-001': 1, 'REA-021': 1}; gate/findings.txt contains 'LOG-001   Violation Class https://acme.example.org/ns/Contractor'

<details><summary>Output, as recorded</summary>

```text
$ node node_modules/tsx/dist/cli.mjs scripts/dsl/acme.ontology.ts work/C08_14/acme.ttl

[exit 0]

$ ontology-quality-suite ontology --ontology work/C08_14/acme.ttl --out-dir work/C08_14/gate --fail-on Violation --reports minimal
Findings: 2 total (2 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C08_14/gate
  - work/C08_14/gate/findings.txt (start here -- what, where, and the source line)
  - work/C08_14/gate/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmppi07_c_p -Y
[exit 1]
```

</details>

---

<a id="c08-15"></a>
### C08.15 — Unchecked code: an internal TypeError up to 0.16.0, an error naming the mistake from 0.16.1

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-15) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Code the checker did not see still gets an error, and since 0.16.1 a useful

**Commands** (from the `evidence/` folder):

```bash
node node_modules/tsx/dist/cli.mjs scripts/dsl/bad-range.ontology.ts
```

**What is checked:** tsx exits non-zero. Up to 0.16.0 with 'TypeError: Cannot convert undefined or null to object'; from 0.16.1 with an error naming the function, the argument and what it was given

**Recorded result:** PASS — step 1 exits non-zero (1); npm ontology-suite 0.16.1: step 1 output contains "defdatatypeproperty('hasEmployeeId'): range takes a datatype, made with datatype('xsd:string') say, and was given the string"

<details><summary>Output, as recorded</summary>

```text
$ node node_modules/tsx/dist/cli.mjs scripts/dsl/bad-range.ontology.ts
./node_modules/ontology-suite/dsl/index.js:835
  throw new Error(`${where} takes ${expected}, and was given ${describe(value)}.`);
        ^
Error: defdatatypeproperty('hasEmployeeId'): range takes a datatype, made with datatype('xsd:string') say, and was given the string "xsd:string".
    at refuse (./node_modules/ontology-suite/dsl/index.js:835:9)
    at checkDatatype (./node_modules/ontology-suite/dsl/index.js:893:5)
    at defdatatypeproperty (./node_modules/ontology-suite/dsl/index.js:1083:30)
    at <anonymous> (./scripts/dsl/bad-range.ontology.ts:8:1)
    at Object.<anonymous> (./scripts/dsl/bad-range.ontology.ts:8:79)
    at Module._compile (node:internal/modules/cjs/loader:1521:14)
    at Object.transformer (./node_modules/tsx/dist/register-B1c7OH6V.cjs:22:2188)
    at Module.load (node:internal/modules/cjs/loader:1266:32)
    at Module._load (node:internal/modules/cjs/loader:1091:12)
    at cjsLoader (node:internal/modules/esm/translators:298:15)
Node.js v20.19.5
[exit 1]
```

</details>

**Sources:**

- [extension commit 2f1a6ce (0.16.1)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/2f1a6ce960f60b1d77bd16f5655cabcc43f78d42): “Check the DSL's arguments, so unchecked code gets an error that names its mistake” (quote found, checked 2026-10-22)

---

<a id="c08-16"></a>
### C08.16 — build().quads and n3's Writer: TS2345 up to 0.16.0, no cast needed from 0.16.1

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-16) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **`build().quads` goes straight to n3's `Writer` from 0.16.1**

**Commands** (from the `evidence/` folder):

```bash
node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/writer-types.ts
```

<details><summary><code>scripts/dsl/writer-types.ts</code></summary>

```typescript
// Chapter 8 §8.2 / Chapter 14 §14.4: the usage the package README suggests,
// build().quads handed to n3's Writer, without a cast. Under strict TypeScript with
// @types/n3 installed, the bundled Quad type is not assignable to n3's.
import { ontology, defclass, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';

ontology('https://acme.example.org/ns/', 'acme');
defclass('Employee');
const { quads, prefixes } = build();
new Writer({ prefixes }).addQuads(quads);
```

</details>

**What is checked:** the README's usage, without a cast, under strict TypeScript with @types/n3. Up to 0.16.0, tsc exits non-zero with TS2345, naming the missing termType; from 0.16.1 it compiles

**Recorded result:** PASS — npm ontology-suite 0.16.1: step 1 exits 0

<details><summary>Output, as recorded</summary>

```text
$ node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/writer-types.ts

[exit 0]
```

</details>

**Sources:**

- [extension commit dbb0cdf (0.16.1)](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/dbb0cdf74ed2180c58c05b8068311be2bc3e07c7): “Give the DSL's Quad the RDF/JS shape, so build().quads goes to n3's Writer uncast” (quote found, checked 2026-10-22)

---

<a id="c08-17"></a>
### C08.17 — ontology reports 2 findings, and findings.txt quotes the line

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-17) · [plain edition](../docs/08-model-and-validate.md#83-the-tightest-cli-loop-ontology)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> That first report is new since the last edition

When HermiT does not run, `ontology` reports LOG-001 and REA-022. findings.txt quotes line 47 and puts REA-022 under 'not located'.

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=0 python scripts/without_java.py ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C08_17/ontology
```

<details><summary><code>scripts/without_java.py</code></summary>

```python
"""Run a command with no Java runtime visible, so HermiT cannot start.

    python scripts/without_java.py ontology-quality-suite ontology --ontology ...

Removes every PATH entry holding a `java` executable and unsets JAVA_HOME, then
runs the command. Otherwise whether the DL reasoner runs depends on the hash seed (Chapter 14
§14.4); this takes Java away as well, to show that a missing Java gives a different message.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

env = dict(os.environ)
env.pop("JAVA_HOME", None)
exe = "java.exe" if os.name == "nt" else "java"
keep = [d for d in env.get("PATH", "").split(os.pathsep) if d and not (Path(d) / exe).is_file()]
env["PATH"] = os.pathsep.join(keep)
print(f"without_java: java on PATH now: {shutil.which('java', path=env['PATH']) or 'none'}", flush=True)
cmd = sys.argv[1:]
cmd[0] = shutil.which(cmd[0], path=env["PATH"]) or cmd[0]
sys.exit(subprocess.run(cmd, env=env).returncode)
```

</details>

**What is checked:** 2 findings (1 V, 1 I); findings.txt quotes lines 47–49 and lists REA-022 as not located; LOG-001's message and remediation read as the manual quotes them

**Recorded result:** PASS — step 1: 2 findings (1 V, 0 W, 1 I); step 1 output contains 'findings.txt (start here -- what, where, and the source line)'; ontology/findings.txt contains '2 finding(s): 1 Violation, 1 Info', '> 47 | acme:Contractor a owl:Class ;', '48 |     rdfs:subClassOf acme:Employee ;', '-- not located: 1 finding(s)', 'REA-022  Info  External DL reasoner unavailable'; LOG-001's message reads as quoted; and its remediation too

<details><summary>Output, as recorded</summary>

```text
$ python scripts/without_java.py ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C08_17/ontology
without_java: java on PATH now: none
Findings: 2 total (1 Violation, 0 Warning, 1 Info)
Reports written to: ./work/C08_17/ontology
  - work/C08_17/ontology/findings.txt (start here -- what, where, and the source line)
  - work/C08_17/ontology/report.html
  - work/C08_17/ontology/full_results.csv
[exit 1]
```

</details>

Java is hidden here so that the reasoner's failure is certain. With Java visible, whether HermiT runs depends on the hash seed: seed 0 gives this output nine runs in ten (C14.06, C14.08).

---

<a id="c08-18"></a>
### C08.18 — LOG-001's message is a model of what a message should be

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-18) · [plain edition](../docs/08-model-and-validate.md#83-the-tightest-cli-loop-ontology)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> No description-logic background is needed to act on that.

**Evidence:** the same as [C08.17 — ontology reports 2 findings, and findings.txt quotes the line](#c08-17), which reproduces it: step 1: 2 findings (1 V, 0 W, 1 I); step 1 output contains 'findings.txt (start here -- what, where, and the source line)'; ontology/findings.txt contains '2 finding(s): 1 Violation, 1 Info', '> 47 | acme:Contractor a owl:Class ;', '48 |     rdfs:subClassOf acme:Employee ;', '-- not located: 1 finding(s)', 'REA-022  Info  External DL reasoner unavailable'; LOG-001's message reads as quoted; and its remediation too

---

<a id="c08-19"></a>
### C08.19 — With HermiT running: REA-021, and up to 0.22.0 a false REA-020

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-19) · [plain edition](../docs/08-model-and-validate.md#83-the-tightest-cli-loop-ontology)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **You may see a different second finding.**

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=5 ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C08_19/seed5 --reports minimal
python scripts/summarise_findings.py work/C08_19/seed5/full_results.csv
```

**What is checked:** with HermiT running, at 0.22.0: 3 Violations, LOG-001, REA-020 and REA-021; from 0.23.0: 2, LOG-001 and REA-021. No REA-022 either way

**Recorded result:** PASS — suite 0.24.3: step 1: 2 findings (2 V, 0 W, 0 I); seed5/full_results.csv: {'LOG-001': 1, 'REA-021': 1}

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C08_19/seed5 --reports minimal
Findings: 2 total (2 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C08_19/seed5
  - work/C08_19/seed5/findings.txt (start here -- what, where, and the source line)
  - work/C08_19/seed5/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmp556lkcfo -Y
[exit 1]

$ python scripts/summarise_findings.py work/C08_19/seed5/full_results.csv
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x REA-021  Violation Class found unsatisfiable by an external DL reasoner
total 2: 2 Violation, 0 Warning, 0 Info
[exit 0]
```

</details>

C14.06 shows how the hash seed decides whether HermiT runs; C14.39 why REA-020 was wrong.

---

<a id="c08-20"></a>
### C08.20 — --profile is off by default and repeatable

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-20) · [plain edition](../docs/08-model-and-validate.md#83-the-tightest-cli-loop-ontology)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Want a specific OWL2 profile checked?**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite ontology --help
```

**What is checked:** `ontology --help` lists --profile

**Recorded result:** PASS — step 1 output contains '--profile'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite ontology --help
usage: ontology-quality-suite ontology [-h] --ontology ONTOLOGY
                                       [--import-dir IMPORT_DIR]
                                       [--exclude-imports] [--allow-network]
                                       [--registry REGISTRY] [--themes THEMES]
                                       [--sparql SPARQL] [--out-dir OUT_DIR]
                                       [--reports {all,minimal}]
                                       [--profile {EL,QL,RL}]
                                       [--reasoner {auto,owlrl-only,hermit,pellet,none}]
                                       [--fail-on {Violation,Warning,Info,never}]
                                       [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --registry REGISTRY
  --themes THEMES       a JSON or CSV map of check id to a question in your
                        own words, used to add a "by question" index to
                        findings.txt -- see docs/REPORTS.md
  --sparql SPARQL       a directory of .rq check queries, or @builtin for the
                        suite's own tree wherever this install put it.
                        Repeatable: pass it more than once to run a project's
                        own checks alongside the suite's, which is what you
                        almost always want. Given at all, it replaces the
                        built-in tree, so `--sparql mine` runs only yours --
… (18 lines omitted; full output in the outputs/ record)
                        reasoning backend: auto (owlrl + external if
                        available), owlrl-only, hermit, pellet, or none
  --fail-on {Violation,Warning,Info,never}
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

---

<a id="c08-21"></a>
### C08.21 — checks reports 479 findings against the fixture

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-21) · [plain edition](../docs/08-model-and-validate.md#84-the-full-registry-checks)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> this reports **479 findings** (55 Violations, 340 Warnings, 84 Infos),

**Evidence:** the same as [C09.02 — The unscoped run reports 479 findings, every time](#c09-02), which reproduces it: step 1: 479 findings (55 V, 340 W, 84 I); step 2: 479 findings (55 V, 340 W, 84 I); step 3: 479 findings (55 V, 340 W, 84 I)

---

<a id="c08-22"></a>
### C08.22 — A project tree alone now warns that 42 built-in checks did not run

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-22) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Point the CLI at that directory on its own and listen to what it says:

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C08_22/employees.ttl
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data work/C08_22/employees.ttl --registry fixtures/acme_robotics/custom_checks/registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --engine sparql --out-dir work/C08_22/acm001 --reports minimal
```

**What is checked:** 0 findings, and the warning names 1 project check and 42 built-in ones; from 0.24.0 it recommends @builtin and names no filesystem path, where up to 0.23.0 it recommended the installed tree's absolute site path

**Recorded result:** PASS — step 2: 0 findings (0 V, 0 W, 0 I); step 2 output contains "WARNING: --sparql replaced the suite's own query tree: 1 project check(s) ran and 42 built-in check(s) did not."; the warning recommends @builtin; step 2 output has none of 'site-packages'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C08_22/employees.ttl

[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data work/C08_22/employees.ttl --registry fixtures/acme_robotics/custom_checks/registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --engine sparql --out-dir work/C08_22/acm001 --reports minimal
Findings: 0 total (0 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C08_22/acm001
  - work/C08_22/acm001/findings.txt (start here -- what, where, and the source line)
  - work/C08_22/acm001/full_results.csv
WARNING: --sparql replaced the suite's own query tree: 1 project check(s) ran and 42 built-in check(s) did not. Pass --sparql @builtin as well to run both.
[exit 0]
```

</details>

---

<a id="c08-23"></a>
### C08.23 — Until 0.18.0 that run was silent; the testing repo's gate was in that state

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-23) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Until 0.18.0 that run was silent.

**Sources:**

- [suite commit cae9ef2 (first released in v0.18.0)](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/cae9ef21cf33ceb8eba33ef94da66b32bf810ded): “the separate testing repo's CI gate config named eight CMP-* queries, its merged registry declared 61 checks, and the gate reported a clean run” (quote found, checked 2026-10-22)

---

<a id="c08-24"></a>
### C08.24 — With @builtin and a one-entry registry, every built-in finding is UNMAPPED

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-24) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **But the registry still replaces rather than composes.**

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C08_24/employees.ttl
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data work/C08_24/employees.ttl --registry fixtures/acme_robotics/custom_checks/registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --sparql @builtin --engine sparql --out-dir work/C08_24/out --reports minimal --fail-on never
```

**What is checked:** 491 findings, every one with check id UNMAPPED; each keeps its severity and (all but two) its message; none has a title or remediation

**Recorded result:** PASS — step 2: 491 findings (54 V, 356 W, 81 I); all 491 findings have check id UNMAPPED; each keeps its severity; nearly all keep their message; none has a title or a remediation

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C08_24/employees.ttl

[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data work/C08_24/employees.ttl --registry fixtures/acme_robotics/custom_checks/registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --sparql @builtin --engine sparql --out-dir work/C08_24/out --reports minimal --fail-on never
Findings: 491 total (54 Violation, 356 Warning, 81 Info)
Reports written to: ./work/C08_24/out
  - work/C08_24/out/findings.txt (start here -- what, where, and the source line)
  - work/C08_24/out/full_results.csv
[exit 0]
```

</details>

---

<a id="c08-25"></a>
### C08.25 — A merged registry names every finding, and ACM-001 fires on its fault only

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-25) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> (the built-in entries plus your own) as a generated file, pass that to

**Inputs:** [`data/house-rule/missing-id.ttl`](data/house-rule/missing-id.ttl)

<details><summary><code>data/house-rule/missing-id.ttl</code></summary>

```turtle
# Chapter 8 §8.5: one employee with an ID and one without. ACM-001 must fire on
# the second and stay quiet on the first (the fault and its control).
@prefix acme: <https://acme.example.org/ns/> .
@prefix ex:   <https://acme.example.org/data/employee/> .

ex:E100 a acme:Employee ; acme:hasEmployeeId "E100" .
ex:E101 a acme:Employee .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/merge_registry.py fixtures/acme_robotics/custom_checks/registry.json work/C08_25/merged-registry.json
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data data/house-rule/missing-id.ttl --registry work/C08_25/merged-registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --sparql @builtin --engine sparql --out-dir work/C08_25/out --reports minimal --fail-on never
python scripts/summarise_findings.py work/C08_25/out/full_results.csv --by focus --check ACM-001
```

<details><summary><code>scripts/merge_registry.py</code></summary>

```python
"""Chapter 8 §8.5: build a merged registry, the built-in entries plus a project's own.

    python scripts/merge_registry.py fixtures/acme_robotics/custom_checks/registry.json work/C08_09/merged-registry.json

`--registry` replaces rather than composes, so a project that wants its house
rules *and* the suite's own checks named properly passes one merged file to
`--registry` and both query trees to `--sparql` (`my-checks/` and `@builtin`).
"""
import json
import sys
from importlib import resources
from pathlib import Path

project = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
builtin = json.loads((resources.files("ontology_suite") / "resources" / "registry.json").read_text(encoding="utf-8"))


def entries(reg):
    return reg["checks"] if isinstance(reg, dict) and "checks" in reg else reg


merged = {e["id"]: e for e in entries(builtin)}
for e in entries(project):
    merged[e["id"]] = e
out = builtin if isinstance(builtin, list) else dict(builtin)
if isinstance(builtin, dict) and "checks" in builtin:
    out["checks"] = list(merged.values())
else:
    out = list(merged.values())
Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
Path(sys.argv[2]).write_text(json.dumps(out, indent=1), encoding="utf-8", newline="\n")
print(f"{len(entries(builtin))} built-in + {len(entries(project))} project = {len(merged)} entries -> {sys.argv[2]}")
```

</details>

**What is checked:** the merged registry has 62 entries; ACM-001 fires on E101 and not on its control E100, with its own title and remediation; nothing is UNMAPPED

**Recorded result:** PASS — step 1 output contains '61 built-in + 1 project = 62 entries'; ACM-001 fires on E101 (no ID) and not on E100 (the control); with its title and remediation from the merged registry; and no finding is UNMAPPED

<details><summary>Output, as recorded</summary>

```text
$ python scripts/merge_registry.py fixtures/acme_robotics/custom_checks/registry.json work/C08_25/merged-registry.json
61 built-in + 1 project = 62 entries -> work/C08_25/merged-registry.json
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --data data/house-rule/missing-id.ttl --registry work/C08_25/merged-registry.json --sparql fixtures/acme_robotics/custom_checks/sparql --sparql @builtin --engine sparql --out-dir work/C08_25/out --reports minimal --fail-on never
Findings: 482 total (56 Violation, 342 Warning, 84 Info)
Reports written to: ./work/C08_25/out
  - work/C08_25/out/findings.txt (start here -- what, where, and the source line)
  - work/C08_25/out/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C08_25/out/full_results.csv --by focus --check ACM-001
ACM-001  focus=https://acme.example.org/data/employee/E101  path=-  value=https://acme.example.org/data/employee/E101
total 1: 1 Violation, 0 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c08-26"></a>
### C08.26 — The warning named the site path @builtin was made to avoid, until 0.24.0

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-26) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Up to 0.23.0 the warning above recommended passing the

**Evidence:** the same as [C08.22 — A project tree alone now warns that 42 built-in checks did not run](#c08-22), which reproduces it: step 2: 0 findings (0 V, 0 W, 0 I); step 2 output contains "WARNING: --sparql replaced the suite's own query tree: 1 project check(s) ran and 42 built-in check(s) did not."; the warning recommends @builtin; step 2 output has none of 'site-packages'

---

<a id="c08-27"></a>
### C08.27 — Checks are discovered by walking the directory

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-27) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **Checks are discovered by walking the directory**

**Sources:**

- [suite commit cae9ef2](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/cae9ef21cf33ceb8eba33ef94da66b32bf810ded): “Discovery is filesystem-based and consults the registry only afterwards, so a query with no entry still runs and reports UNMAPPED, and an entry with no file never fires at all.” (quote found, checked 2026-10-22)

C08.24 shows the first half: queries with no registry entry still ran, and reported UNMAPPED.

---

<a id="c08-28"></a>
### C08.28 — Every full run writes cucumber.json

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-28) · [plain edition](../docs/08-model-and-validate.md#alongside-the-built-in-checks-not-instead-of-them)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Fill in the cucumber fields.**

**Evidence:** the same as [C09.10 — Which reports a run writes, and --reports minimal](#c09-10), which reproduces it: default run writes findings.txt, full_results.csv, cucumber.json, report.html; and features/ and plots/; and none of the six retired summary files; --reports minimal writes exactly findings.txt and full_results.csv; full_results.csv has source_file and line columns

---

<a id="c08-29"></a>
### C08.29 — Guard a label with isBlank; COALESCE is the weaker fix

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-29) · [plain edition](../docs/08-model-and-validate.md#the-contract-a-check-has-to-satisfy)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Never build a message out of a label.**

**Evidence:** the same as [C07.07 — STR() of a blank node: lenient, conformant, and the guard](#c07-07), which reproduces it: unguarded: rdflib names an internal identifier; holosdb and pyoxigraph leave the message unbound; COALESCE: rdflib still names the identifier, the other two say '[a blank node]'; IF(isBlank(...)): all three say '[a blank node]'

---

<a id="c08-30"></a>
### C08.30 — CT-39 asserts that a finding names something findable

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-30) · [plain edition](../docs/08-model-and-validate.md#the-contract-a-check-has-to-satisfy)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> board row, CT-39, whose whole assertion is that a finding names something a

**Sources:**

- [testing repo CT-39 README](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/experiments/SpecificTests/CT-39-finding-names-something-findable/README.md#L1): “CT-39 — A finding names something a reader can find” (quote found, checked 2026-10-22)

---

<a id="c08-31"></a>
### C08.31 — sh:severity on a node shape does not reach its property shapes

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-31) · [plain edition](../docs/08-model-and-validate.md#writing-the-shacl-half-too)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Put `sh:severity` on the shape that produces the result.**

**Evidence:** the same as [C07.12 — Severity belongs to the shape that produces the result](#c07-12), which reproduces it: step 1 output contains 'sh:resultSeverity sh:Warning'; step 2 output contains 'sh:resultSeverity sh:Violation'; step 2 output has none of 'sh:resultSeverity sh:Warning'

---

<a id="c08-32"></a>
### C08.32 — Four checks shipped that matched nothing

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-32) · [plain edition](../docs/08-model-and-validate.md#prove-it-fires-before-you-trust-it)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The suite has shipped four checks

**Sources:**

- [suite commit 2f4950c](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/2f4950c4436868fb6ea203c0ce271727b256cfef): “matched nothing (REA-001's symmetry assumption, DAT-001's UNION of FILTER-only branches, EFF-002's unjoined $this, and DAT-001's boolean branch above)” (quote found, checked 2026-10-22)

---

<a id="c08-34"></a>
### C08.34 — inverse(p): the inline inverse, new in the DSL at 0.16.0

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-34) · [plain edition](../docs/08-model-and-validate.md#82-ontologies-as-code-literally)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> restriction builder also takes `inverse(p)`, the inline inverse that `MDL-001`

**Commands** (from the `evidence/` folder):

```bash
node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/inverse.ontology.ts
node node_modules/tsx/dist/cli.mjs scripts/dsl/inverse.ontology.ts work/C08_34/inverse.ttl
python scripts/query_file.py work/C08_34/inverse.ttl "PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?inverseOf ?filler WHERE { <https://example.org/cars/CarPart> rdfs:subClassOf ?r . ?r owl:onProperty ?p ; owl:someValuesFrom ?filler . ?p owl:inverseOf ?inverseOf }"
```

<details><summary><code>scripts/dsl/inverse.ontology.ts</code></summary>

```typescript
// Chapter 8 §8.2: the inline inverse, new in the DSL at 0.16.0. "A part of some
// Car" written without minting a named inverse property, as MDL-001 recommends.
// Run with tsx; writes Turtle to argv[2].
import { ontology, defclass, defobjectproperty, some, inverse, build } from 'ontology-suite/dsl';
import { Writer } from 'n3';
import { writeFileSync } from 'node:fs';

ontology('https://example.org/cars/', 'car');
const Car = defclass('Car');
const hasPart = defobjectproperty('hasPart');
defclass('CarPart', { subClassOf: [some(inverse(hasPart), Car)] });

const { quads, prefixes } = build();
const w = new Writer({ prefixes });
w.addQuads(quads);   // no cast from 0.16.1 (C08.16)
w.end((_e: unknown, ttl: string) => writeFileSync(process.argv[2], ttl));
```

</details>

**What is checked:** the script type-checks and builds; CarPart's restriction is on an anonymous [ owl:inverseOf car:hasPart ], with Car as the filler, and no named inverse property is minted

**Recorded result:** PASS — step 1 exits 0; step 2 exits 0; step 3 output contains 'https://example.org/cars/hasPart', 'https://example.org/cars/Car'

<details><summary>Output, as recorded</summary>

```text
$ node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext --moduleResolution nodenext --target es2022 --skipLibCheck scripts/dsl/inverse.ontology.ts

[exit 0]

$ node node_modules/tsx/dist/cli.mjs scripts/dsl/inverse.ontology.ts work/C08_34/inverse.ttl

[exit 0]

$ python scripts/query_file.py work/C08_34/inverse.ttl "PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?inverseOf ?filler WHERE { <https://example.org/cars/CarPart> rdfs:subClassOf ?r . ?r owl:onProperty ?p ; owl:someValuesFrom ?filler . ?p owl:inverseOf ?inverseOf }"
inverseOf,filler
https://example.org/cars/hasPart,https://example.org/cars/Car
[exit 0]
```

</details>

**Sources:**

- [extension CHANGELOG, 0.16.0](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L123-L127): “Manchester's `inverse p some C`, written as OWL 2 does with `[ owl:inverseOf p ]`” (quote found, checked 2026-10-22)

---

<a id="c08-33"></a>
### C08.33 — How the editor behaviour was established

**In the manual:** [Chapter 8, at the claim](manual/docs/08-model-and-validate.md#ev-c08-33) · [plain edition](../docs/08-model-and-validate.md#86-the-loop-drawn)  
**Kind:** Argument · **Result:** Argument

> **How the editor behaviour in this chapter was established.**

A statement of method. The extension's unit tests were run on a Windows checkout of [534ce51](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/534ce517f9aabc0c27d33f1af5eb85f88296a16f) (the 0.16.1 release), with core.autocrlf on: 56 files, 509 tests, all passing, which matches the release's own count ([CHANGELOG](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/CHANGELOG.md#L30)). At 0.16.0 ([02ffaf6](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/commit/02ffaf6c35dae3e2b47fff9f723e501d24dc26cf)) the same run gave 55 files and 466 tests, all passing. The DSL claims (C08.12–C08.16, C08.34) are reproduced here from the npm package.

---

<a id="chapter-09"></a>
## 9. Continuous integration

Annotated chapter: [manual/docs/09-continuous-integration.md](manual/docs/09-continuous-integration.md) · plain chapter: [../docs/09-continuous-integration.md](../docs/09-continuous-integration.md)

<a id="c09-01"></a>
### C09.01 — --fail-on Violation exits non-zero on the fixture

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-01) · [plain edition](../docs/09-continuous-integration.md#91-the-mechanism)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `--fail-on` takes `Violation`, `Warning`, `Info` or `never`.

The gate is one flag and an exit code: the fixture's deliberate contradiction is a Violation, so the ontology stage exits non-zero.

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=0 ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C09_01/gate --reports minimal --fail-on Violation
```

**What is checked:** the command exits non-zero, and reports one Violation

**Recorded result:** PASS — step 1 exits non-zero (1); step 1 output contains '1 Violation'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C09_01/gate --reports minimal --fail-on Violation
Findings: 2 total (1 Violation, 0 Warning, 1 Info)
Reports written to: ./work/C09_01/gate
  - work/C09_01/gate/findings.txt (start here -- what, where, and the source line)
  - work/C09_01/gate/full_results.csv
[exit 1]
```

</details>

---

<a id="c09-02"></a>
### C09.02 — The unscoped run reports 479 findings, every time

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-02) · [plain edition](../docs/09-continuous-integration.md#92-the-problem-479-findings)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> 479 every time, and 479 on a new engine.

The full registry, with org: and FOAF resolved, reports 479 findings (55 V, 340 W, 84 I), the same on repeated runs.

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run1 --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run2 --fail-on never --reports minimal
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run3 --fail-on never --reports minimal
```

**What is checked:** each of three identical runs prints 479 total, 55 Violation, 340 Warning, 84 Info

**Recorded result:** PASS — step 1: 479 findings (55 V, 340 W, 84 I); step 2: 479 findings (55 V, 340 W, 84 I); step 3: 479 findings (55 V, 340 W, 84 I)

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run1 --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C09_02/run1
  - work/C09_02/run1/findings.txt (start here -- what, where, and the source line)
  - work/C09_02/run1/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run2 --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C09_02/run2
  - work/C09_02/run2/findings.txt (start here -- what, where, and the source line)
  - work/C09_02/run2/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_02/run3 --fail-on never --reports minimal
Findings: 479 total (55 Violation, 340 Warning, 84 Info)
Reports written to: ./work/C09_02/run3
  - work/C09_02/run3/findings.txt (start here -- what, where, and the source line)
  - work/C09_02/run3/full_results.csv
[exit 0]
```

</details>

---

<a id="c09-03"></a>
### C09.03 — --exclude-imports gives 27 findings, four of them false

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-03) · [plain edition](../docs/09-continuous-integration.md#93-the-obvious-fix-is-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> 479 findings become **27**.

Not resolving the imports cuts 479 to 27, but four of the 27 are artefacts: FOAF terms that look dangling or unlabelled only because FOAF was not loaded.

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --exclude-imports --engine sparql --out-dir work/C09_03/excl --fail-on never --reports minimal
python scripts/summarise_findings.py work/C09_03/excl/full_results.csv
python scripts/summarise_findings.py work/C09_03/excl/full_results.csv --by focus --check DAT-002
python scripts/summarise_findings.py work/C09_03/excl/full_results.csv --by focus --check QUA-004
```

**What is checked:** 27 findings with exactly the breakdown in the manual; both DAT-002 findings point at FOAF; two of the three QUA-004 are about FOAF terms

**Recorded result:** PASS — step 1: 27 findings (1 V, 26 W, 0 I); excl/full_results.csv: {'DAT-002': 2, 'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 3, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}; step 3 output contains 'value=http://xmlns.com/foaf/0.1/', 'value=http://xmlns.com/foaf/0.1/Person'; step 4 output contains 'focus=http://xmlns.com/foaf/0.1/Person'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --exclude-imports --engine sparql --out-dir work/C09_03/excl --fail-on never --reports minimal
Findings: 27 total (1 Violation, 26 Warning, 0 Info)
Reports written to: ./work/C09_03/excl
  - work/C09_03/excl/findings.txt (start here -- what, where, and the source line)
  - work/C09_03/excl/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C09_03/excl/full_results.csv
  2 x DAT-002  Warning   Dangling IRI reference
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x QUA-001  Warning   Class or property missing rdfs:label
  3 x QUA-004  Warning   Resource missing skos:prefLabel
  9 x QUA-009  Warning   Class or property without one skos:prefLabel per language
  9 x QUA-010  Warning   Class or property without a skos:definition
  1 x STR-003  Warning   Property missing both domain and range
  1 x STY-002  Warning   Property name not lowerCamelCase
total 27: 1 Violation, 26 Warning, 0 Info
[exit 0]

$ python scripts/summarise_findings.py work/C09_03/excl/full_results.csv --by focus --check DAT-002
DAT-002  focus=https://acme.example.org/ns/1.0.0  path=http://www.w3.org/2002/07/owl#imports  value=http://xmlns.com/foaf/0.1/
DAT-002  focus=https://acme.example.org/ns/Employee  path=http://www.w3.org/2000/01/rdf-schema#subClassOf  value=http://xmlns.com/foaf/0.1/Person
total 2: 0 Violation, 2 Warning, 0 Info
[exit 0]

$ python scripts/summarise_findings.py work/C09_03/excl/full_results.csv --by focus --check QUA-004
QUA-004  focus=http://xmlns.com/foaf/0.1/  path=http://www.w3.org/2004/02/skos/core#prefLabel  value=http://xmlns.com/foaf/0.1/
QUA-004  focus=http://xmlns.com/foaf/0.1/Person  path=http://www.w3.org/2004/02/skos/core#prefLabel  value=http://xmlns.com/foaf/0.1/Person
QUA-004  focus=https://acme.example.org/ns/hasSkill  path=http://www.w3.org/2004/02/skos/core#prefLabel  value=https://acme.example.org/ns/hasSkill
total 3: 0 Violation, 3 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c09-04"></a>
### C09.04 — --own-namespace gives 23 findings, all Acme's

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-04) · [plain edition](../docs/09-continuous-integration.md#94-the-right-fix---own-namespace)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Twenty-three findings. All twenty-three are Acme's. None are artefacts.**

Keep the imports, filter the report by focus node: 23 findings, every one in Acme's namespace, 18 of them the documentation pair QUA-009/QUA-010.

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_04/own --fail-on never --reports minimal
python scripts/summarise_findings.py work/C09_04/own/full_results.csv
```

**What is checked:** 23 findings (1 V, 22 W), the per-check breakdown in the manual, and every focus node in https://acme.example.org/ns/

**Recorded result:** PASS — step 1: 23 findings (1 V, 22 W, 0 I); own/full_results.csv: {'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}; every focus node starts with https://acme.example.org/ns/

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_04/own --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C09_04/own
  - work/C09_04/own/findings.txt (start here -- what, where, and the source line)
  - work/C09_04/own/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C09_04/own/full_results.csv
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x QUA-001  Warning   Class or property missing rdfs:label
  1 x QUA-004  Warning   Resource missing skos:prefLabel
  9 x QUA-009  Warning   Class or property without one skos:prefLabel per language
  9 x QUA-010  Warning   Class or property without a skos:definition
  1 x STR-003  Warning   Property missing both domain and range
  1 x STY-002  Warning   Property name not lowerCamelCase
total 23: 1 Violation, 22 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c09-05"></a>
### C09.05 — The three runs compared: 479, 27, 23

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-05) · [plain edition](../docs/09-continuous-integration.md#94-the-right-fix---own-namespace)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | `--own-namespace` | **23** | 23 | 0 | 0 |

**Evidence:** the same as [C09.04 — --own-namespace gives 23 findings, all Acme's](#c09-04), which reproduces it: step 1: 23 findings (1 V, 22 W, 0 I); own/full_results.csv: {'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}; every focus node starts with https://acme.example.org/ns/

The table's three rows are C09.02 (479), C09.03 (27, four false) and C09.04 (23).

---

<a id="c09-06"></a>
### C09.06 — --themes groups findings under questions in your words

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-06) · [plain edition](../docs/09-continuous-integration.md#reading-the-23-as-questions-not-as-check-ids)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `--themes` takes a small file mapping check ids to

**Inputs:** [`data/themes/acme-themes.json`](data/themes/acme-themes.json)

<details><summary><code>data/themes/acme-themes.json</code></summary>

```json
{
  "Can a domain expert read what each term means?": ["QUA-001", "QUA-004", "QUA-009", "QUA-010"],
  "Is the model logically coherent?": ["LOG-001", "REA-021"],
  "Will our naming survive a code review?": ["STY-002"]
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --themes data/themes/acme-themes.json --out-dir work/C09_06/themes --fail-on never --reports minimal
python scripts/summarise_findings.py work/C09_06/themes/full_results.csv
```

**What is checked:** findings.txt opens with a 'by question' index: 20 under the documentation question, 1 under coherence, and STR-003 listed as not mapped rather than dropped

**Recorded result:** PASS — findings.txt has '-- by question'; findings.txt has 'Can a domain expert read what each term means?  (20)'; findings.txt has 'QUA-001 x1, QUA-004 x1, QUA-009 x9, QUA-010 x9'; findings.txt has 'Is the model logically coherent?  (1)'; findings.txt has 'not mapped to a question  (1)'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --themes data/themes/acme-themes.json --out-dir work/C09_06/themes --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C09_06/themes
  - work/C09_06/themes/findings.txt (start here -- what, where, and the source line)
  - work/C09_06/themes/full_results.csv
[exit 0]

$ python scripts/summarise_findings.py work/C09_06/themes/full_results.csv
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x QUA-001  Warning   Class or property missing rdfs:label
  1 x QUA-004  Warning   Resource missing skos:prefLabel
  9 x QUA-009  Warning   Class or property without one skos:prefLabel per language
  9 x QUA-010  Warning   Class or property without a skos:definition
  1 x STR-003  Warning   Property missing both domain and range
  1 x STY-002  Warning   Property name not lowerCamelCase
total 23: 1 Violation, 22 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c09-07"></a>
### C09.07 — A near-miss namespace warns, on stderr, and offers only real namespaces

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-07) · [plain edition](../docs/09-continuous-integration.md#a-real-mistake-worth-repeating)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The tool now says so.** Reported from that experience

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace http://example.org/acme# --out-dir work/C09_07/miss --fail-on never --reports minimal
```

**What is checked:** 0 findings; the warning 'matched none of the 479 findings' is on stderr and not stdout; and from 0.24.0 every entry in the 'Namespaces actually seen' list has a scheme, where up to 0.23.0 the list led with two blank-node identifiers with a slash appended

**Recorded result:** PASS — step 1: 0 findings (0 V, 0 W, 0 I); the warning is on stderr, not stdout; all 5 namespaces offered have a scheme

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace http://example.org/acme# --out-dir work/C09_07/miss --fail-on never --reports minimal
Findings: 0 total (0 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C09_07/miss
  - work/C09_07/miss/findings.txt (start here -- what, where, and the source line)
  - work/C09_07/miss/full_results.csv
WARNING: --own-namespace http://example.org/acme# matched none of the 479 findings, so this run reports nothing. It is a literal IRI-prefix match -- check the scheme, host and trailing separator against the ontology's own @prefix line. Namespaces actually seen: http://purl.org/dc/elements/1.1/, http://purl.org/dc/terms/, http://purl.org/goodrelations/v1#, http://schema.org/, http://www.asahi-net.or.jp/~ax2s-kmtn/ (+9 more)
[exit 0]
```

</details>

---

<a id="c09-08"></a>
### C09.08 — The warning fires only when there were findings to lose

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-08) · [plain edition](../docs/09-continuous-integration.md#a-real-mistake-worth-repeating)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The warning fires only when there were findings to lose.

**Sources:**

- [suite cli.py, _filter_own_namespace](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/ontology_suite/cli.py#L158-L229): “if rows and not matched:” (quote found, checked 2026-10-22)

The warning is emitted only when the filter removes everything from a non-empty set of rows; an empty run never reaches it. The condition tests `matched` rather than the returned `kept`: 0.24.0 keeps run-level findings such as REA-022 through the filter, and counting those as a match would switch this warning off on exactly the runs that most need it.

---

<a id="c09-09"></a>
### C09.09 — A scoped run keeps the 'reasoner did not run' finding, from 0.24.0

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-09) · [plain edition](../docs/09-continuous-integration.md#what-the-filter-could-not-see-until-0240)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> findings about the run survive the filter

REA-022's focus node is the synthetic oq:Graph, which starts with nobody's namespace, so until 0.24.0 --own-namespace removed it: the unscoped data run reported REA-022 and the scoped one said nothing about it. From 0.24.0 both report it. With HermiT unable to run (Java hidden, so that the outcome is certain), the scoped run's total is unchanged at 54 while its composition moves -- one Violation fewer, because a LOG-001 contradiction counted twice is now merged, and one Info more, because REA-022 survives. Two real changes that a gate watching only the total would miss.

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C09_09/employees.ttl
PYTHONHASHSEED=0 python scripts/without_java.py ontology-quality-suite data work/C09_09/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_09/unscoped --fail-on never --reports minimal
PYTHONHASHSEED=0 python scripts/without_java.py ontology-quality-suite data work/C09_09/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C09_09/scoped --fail-on never --reports minimal
```

<details><summary><code>scripts/without_java.py</code></summary>

```python
"""Run a command with no Java runtime visible, so HermiT cannot start.

    python scripts/without_java.py ontology-quality-suite ontology --ontology ...

Removes every PATH entry holding a `java` executable and unsets JAVA_HOME, then
runs the command. Otherwise whether the DL reasoner runs depends on the hash seed (Chapter 14
§14.4); this takes Java away as well, to show that a missing Java gives a different message.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

env = dict(os.environ)
env.pop("JAVA_HOME", None)
exe = "java.exe" if os.name == "nt" else "java"
keep = [d for d in env.get("PATH", "").split(os.pathsep) if d and not (Path(d) / exe).is_file()]
env["PATH"] = os.pathsep.join(keep)
print(f"without_java: java on PATH now: {shutil.which('java', path=env['PATH']) or 'none'}", flush=True)
cmd = sys.argv[1:]
cmd[0] = shutil.which(cmd[0], path=env["PATH"]) or cmd[0]
sys.exit(subprocess.run(cmd, env=env).returncode)
```

</details>

**What is checked:** REA-022 present in both runs and about oq:Graph in both; unscoped 548 (65 V, 363 W, 120 I); scoped 54 (11 V, 40 W, 3 I) -- the same total as 0.23.0's 54 (12 V, 40 W, 2 I), one Violation fewer and one Info more

**Recorded result:** PASS — unscoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; scoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; step 2: 548 findings (65 V, 363 W, 120 I); step 3: 54 findings (11 V, 40 W, 3 I)

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C09_09/employees.ttl

[exit 0]

$ python scripts/without_java.py ontology-quality-suite data work/C09_09/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C09_09/unscoped --fail-on never --reports minimal
without_java: java on PATH now: none
Findings: 548 total (65 Violation, 363 Warning, 120 Info)
Reports written to: ./work/C09_09/unscoped
  - work/C09_09/unscoped/findings.txt (start here -- what, where, and the source line)
  - work/C09_09/unscoped/full_results.csv
[exit 0]

$ python scripts/without_java.py ontology-quality-suite data work/C09_09/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C09_09/scoped --fail-on never --reports minimal
without_java: java on PATH now: none
Findings: 54 total (11 Violation, 40 Warning, 3 Info)
Reports written to: ./work/C09_09/scoped
  - work/C09_09/scoped/findings.txt (start here -- what, where, and the source line)
  - work/C09_09/scoped/full_results.csv
[exit 0]
```

</details>

---

<a id="c09-10"></a>
### C09.10 — Which reports a run writes, and --reports minimal

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-10) · [plain edition](../docs/09-continuous-integration.md#95-wiring-it-up)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | `findings.txt` | A person at a terminal, or an agent

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_10/default --fail-on never
ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_10/minimal --fail-on never --reports minimal
python scripts/list_files.py work/C09_10/default
python scripts/list_files.py work/C09_10/minimal
```

**What is checked:** the default run writes findings.txt, full_results.csv, cucumber.json, report.html, features/ and plots/, none of the retired summary files; --reports minimal writes exactly two files; full_results.csv has source_file and line columns

**Recorded result:** PASS — default run writes findings.txt, full_results.csv, cucumber.json, report.html; and features/ and plots/; and none of the six retired summary files; --reports minimal writes exactly findings.txt and full_results.csv; full_results.csv has source_file and line columns

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_10/default --fail-on never
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C09_10/default
  - work/C09_10/default/findings.txt (start here -- what, where, and the source line)
  - work/C09_10/default/report.html
  - work/C09_10/default/full_results.csv
[exit 0]

$ ontology-quality-suite checks --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ns/ --out-dir work/C09_10/minimal --fail-on never --reports minimal
Findings: 23 total (1 Violation, 22 Warning, 0 Info)
Reports written to: ./work/C09_10/minimal
  - work/C09_10/minimal/findings.txt (start here -- what, where, and the source line)
  - work/C09_10/minimal/full_results.csv
[exit 0]

$ python scripts/list_files.py work/C09_10/default
   79,141  cucumber.json
    1,232  features/conformance.feature
      958  features/data-quality.feature
    4,889  features/documentation-quality.feature
    2,149  features/logical-cogency.feature
    1,375  features/naming-style.feature
    3,214  features/reasoning.feature
      777  features/structural---runtime-efficiency.feature
    2,608  features/structural-integrity.feature
    1,318  features/tarql-query-consistency.feature
      263  features/vocabulary-integrity.feature
    6,312  findings.txt
   10,848  full_results.csv
   33,544  plots/category_breakdown.png
   15,966  plots/severity_distribution.png
   32,323  plots/top_offenders.png
  138,168  report.html
17 files, 335,085 bytes
[exit 0]

$ python scripts/list_files.py work/C09_10/minimal
    6,312  findings.txt
   10,848  full_results.csv
2 files, 17,160 bytes
[exit 0]
```

</details>

---

<a id="c09-11"></a>
### C09.11 — The report set changed in 0.17.0, though REPORTS.md says 0.15.0

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-11) · [plain edition](../docs/09-continuous-integration.md#95-wiring-it-up)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> (The suite's `REPORTS.md` dates the change to 0.15.0.

**Sources:**

- [suite commit f6ee897, 'Say where the finding is, and say each thing once'](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/f6ee897c7065569805c27cc7c8af0c2ff0738a8b): “Six files stopped being written: summary_by_category, summary_by_check and top_offenders” (quote found, checked 2026-10-22)
- [suite commit 1af2a2d, 'Bump to 0.17.0' (the first tag containing f6ee897)](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/1af2a2d5a77eaa7cb07b03ee75bf1ec282c35bfe): “Minor rather than patch: six report files are no longer written” (quote found, checked 2026-10-22)
- [suite docs/REPORTS.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/REPORTS.md#L18): “## What changed in 0.15.0” (quote found, checked 2026-10-22)

---

<a id="c09-12"></a>
### C09.12 — The suite pins shacl below 0.4

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-12) · [plain edition](../docs/09-continuous-integration.md#95-wiring-it-up)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The suite responded by pinning `shacl>=0.3.0,<0.4`

**Evidence:** the same as [C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries](#c07-05), which reproduces it: step 1 output contains 'commands installed: ontology-quality-suite', 'owlready2>=0.51', 'shacl 0.3.4/n    commands installed: none (library only)', 'tarka-rdf 0.1.1/n    commands installed: none (library only)', 'holosdb 0.25.0/n    commands installed: none (library only)'; suite 0.24.3: step 1 output contains 'shacl<0.4,>=0.3.3'; suite 0.24.3: step 1 output contains 'holosdb>=0.24'

The installed package's declared dependencies include `shacl<0.4,>=0.3.0`; the reason is in the [pyproject comment](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/pyproject.toml#L33-L37).

---

<a id="c09-13"></a>
### C09.13 — --reports minimal writes two files

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-13) · [plain edition](../docs/09-continuous-integration.md#95-wiring-it-up)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `--reports minimal` writes only `findings.txt` and `full_results.csv`.

**Evidence:** the same as [C09.10 — Which reports a run writes, and --reports minimal](#c09-10), which reproduces it: default run writes findings.txt, full_results.csv, cucumber.json, report.html; and features/ and plots/; and none of the six retired summary files; --reports minimal writes exactly findings.txt and full_results.csv; full_results.csv has source_file and line columns

---

<a id="c09-14"></a>
### C09.14 — run reports 26 findings, one contradiction once, from 0.24.0

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-14) · [plain edition](../docs/09-continuous-integration.md#96-the-one-command-version)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The two Violations are `LOG-001`, the deliberate

With HermiT able to run (PYTHONHASHSEED=5, see C14.06), `run` reports 26 findings with 2 Violations: LOG-001 once and REA-021; it exits 1. Up to 0.23.0 the same run reported 27 with 3, LOG-001 arriving twice -- once from the registry pass and once from the owlrl-closure pass, deduplicated within each but not across the join between them.

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=5 ontology-quality-suite run --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --queries fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --fail-on Violation --out-dir work/C09_14/out --reports minimal
python scripts/summarise_findings.py work/C09_14/out/full_results.csv --by focus --check LOG-001
```

**What is checked:** 26 total (2 V, 22 W, 2 I), exit 1, LOG-001 once and REA-021 once

**Recorded result:** PASS — step 1: 26 findings (2 V, 22 W, 2 I); step 1 exits 1; out/full_results.csv: {'CNF-005': 2, 'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'REA-021': 1, 'STR-003': 1, 'STY-002': 1}

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite run --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --queries fixtures/acme_robotics --own-namespace https://acme.example.org/ns/ --engine sparql --fail-on Violation --out-dir work/C09_14/out --reports minimal
Findings: 26 total (2 Violation, 22 Warning, 2 Info)
Reports written to: ./work/C09_14/out
  - work/C09_14/out/findings.txt (start here -- what, where, and the source line)
  - work/C09_14/out/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmp12tnrr9d -Y
[exit 1]

$ python scripts/summarise_findings.py work/C09_14/out/full_results.csv --by focus --check LOG-001
LOG-001  focus=https://acme.example.org/ns/Contractor  path=(http://www.w3.org/2000/01/rdf-schema#subClassOf)+  value=https://acme.example.org/ns/Employee
total 1: 1 Violation, 0 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="c09-15"></a>
### C09.15 — The testing repository: 165 passed, 10 skipped

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-15) · [plain edition](../docs/09-continuous-integration.md#the-pattern-a-fixture-per-error-category)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **165 passed, 10 skipped**, unchanged by the engine move.

**Commands** (from the `evidence/` folder):

```bash
(cd $EVIDENCE_TESTING_REPO && uv run pytest -q)
```

**What is checked:** pytest reports 165 passed, 10 skipped

**Recorded result:** PASS — step 1 output contains '165 passed, 10 skipped'

<details><summary>Output, as recorded</summary>

```text
$ uv run pytest -q
..........................................s............................. [ 41%]
.....ssssss.....sss..................................................... [ 82%]
...............................                                          [100%]
============================== warnings summary ===============================
competency_tests/test_competency.py::test_competency_test_is_evidenced[1]
  <tmp>/claude/c--repos-new-triplestore-sparql-engine/b99fbbab-4726-4455-92d7-013b56fb240e/scratchpad/semops-run/consolidated_ontology_suite_python/ontology_suite/sketch/prefix_alignment.py:211: DeprecationWarning: Dataset.default_context is deprecated, use Dataset.default_graph instead.
    default = getattr(dataset, "default_graph", None) or dataset.default_context
tests/test_detection.py::test_expected_checks_fire[06-datatype-conformance]
tests/test_detection.py::test_native_shacl_engine_reports_what_pyshacl_does[06-datatype-conformance]
tests/test_detection.py::test_datatype_errors_are_found_whatever_the_reasoner[auto]
tests/test_detection.py::test_every_finding_carries_a_message[06-datatype-conformance]
  <tmp>/claude/c--repos-new-triplestore-sparql-engine/b99fbbab-4726-4455-92d7-013b56fb240e/scratchpad/semops-run/testing/.venv/Lib/site-packages/rdflib/term.py:1862: UserWarning: Parsing weird boolean, 'yes' does not map to True or False
    warnings.warn(
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
165 passed, 10 skipped, 5 warnings in 81.10s (0:01:21)
Using CPython 3.12.13
Creating virtual environment at: .venv
   Building ontology-quality-suite @ file:///<tmp>/claude/c--repos-new-triplestore-sparql-engine/b99fbbab-4726-4455-92d7-013b56fb240e/scratchpad/semops-run/consolidated_ontology_suite_python
      Built ontology-quality-suite @ file:///<tmp>/claude/c--repos-new-triplestore-sparql-engine/b99fbbab-4726-4455-92d7-013b56fb240e/scratchpad/semops-run/consolidated_ontology_suite_python
Installed 26 packages in 19.12s
[exit 0]
```

</details>

Set EVIDENCE_TESTING_REPO to a clone of the testing repository at [6cdfb14](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/6cdfb14a3c2857b61dcb32f49f56a4829b0d0664). It installs the suite from a sibling checkout, `../consolidated_ontology_suite_python` (v0.23.0 here), and its competency tests triplify with oxi-gen, found through ONTOLOGY_SUITE_OXI_GEN_BIN (0.5.1 here). The run resolved holosdb 0.21.0 and shacl 0.3.3 from the testing repository's own lock. Without oxi-gen 40 of those tests error at setup, saying so.

---

<a id="c09-16"></a>
### C09.16 — The competency board: 27 green, 0 red

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-16) · [plain edition](../docs/09-continuous-integration.md#one-folder-per-question)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Re-run for this edition: **27 green, 0 red**, in two minutes.

**Commands** (from the `evidence/` folder):

```bash
(cd $EVIDENCE_TESTING_REPO && bash experiments/SpecificTests/run-all.sh)
```

**What is checked:** the board ends '27 green, 0 red', and CT-21's verdict reads as quoted

**Recorded result:** PASS — step 1 output contains '27 green, 0 red'; step 1 output contains 'litres measure volume, not force per unit area'

<details><summary>Output, as recorded</summary>

```text
$ bash experiments/SpecificTests/run-all.sh
STATUS TEST                               DETAIL
PASS   CT-01-iri-template-drift           TQL-001 reported for ?site_IRI -- sites.rq and readings.rq mint the
PASS   CT-02-one-iri-two-concepts         CMP-002 reported for node-A1 -- one IRI is both a site and a reading, so two mappings mean
PASS   CT-03-rename-not-propagated        :PumpStation reported as undeclared -- 2.0.0 renamed it and the
PASS   CT-04-taxonomy-term-missing        vocab:Resevoir reported -- the template hard-codes a term the taxonomy
PASS   CT-05-shared-concept-two-domains   TQL-001 reported for site_IRI -- two domains mint the shared concept differently, so their
PASS   CT-06-mapping-not-updated-for-new-version CNF-001 reported for PumpStation -- the mapping builds a class 2.0.0 does not declare.
PASS   CT-07-change-not-reflected         MAJOR reported for the breaking change -- a class was removed, so
PASS   CT-08-missing-definition           QUA-010 reported for #Asset -- the class is named and labelled
PASS   CT-09-class-outside-the-hierarchy  CMP-009 reported for Telemetry -- nothing is above it and nothing below, so it sits outsid
PASS   CT-10-missing-preferred-label      QUA-009 reported for #Asset -- it has an rdfs:label and no preferred label, so it is missi
PASS   CT-11-two-preferred-labels         QUA-009 reported for #Asset -- it carries two English preferred labels and nothing can cho
PASS   CT-12-label-minted-by-the-mapping  CMP-012 reported for Reservoir -- the taxonomy owns that term's name and the mapping state
PASS   CT-13-unused-ontology-term         CNF-005 reported for DecommissionedSite -- the ontology declares it and nothing in the dat
PASS   CT-14-construct-variable-unbound   TQL-002 reported for site_IRI -- it is used in the template and bound nowhere, so every tr
PASS   CT-17-required-link-missing        CMP-017 reported for asset-A2 -- the agreed pattern requires every pump station to stand s
PASS   CT-18-unexpected-modelling-pattern CMP-018 reported for reading-R2 -- the number is hung straight off the reading, so there i
PASS   CT-19-magnitude-without-value      CMP-019 reported for flow-S2 -- the node was built and the source cell was empty, so it is
PASS   CT-20-magnitude-without-unit       DAT-004 reported for flow-S2 -- it carries a number and no unit, so nothing can say 47 of 
PASS   CT-21-unit-wrong-for-quantity      CMP-021 reported for pressure-R1 -- litres measure volume, not force per unit area.
PASS   CT-22-datatype-never-given         TQL-005 reported for flow_DT -- the name promises a datatype and the expression never give
PASS   CT-29-iri-pattern-left-behind      CMP-029 reported for site_IRI -- the concept moved to the shared model and the mapping sti
PASS   CT-30-duplicate-business-key       CMP-030 reported for site-S1 -- one site was entered twice under two ids and only the shar
PASS   CT-31-single-valued-link-twice     CMP-031 reported for asset-A1 -- two mappings each contributed a site link and they disagr
PASS   CT-32-property-outside-its-domain  CMP-032 reported for other_site_IRI -- the property's domain is :PumpStation and the templ
PASS   CT-33-mapping-builds-deprecated-term CMP-033 reported for PumpStation -- the model deprecates it and the mapping builds it anyw
PASS   CT-37-prefix-disagreement          CMP-037 reported for prefix/gist -- one file ends the namespace with a slash and the other
PASS   CT-39-finding-names-something-findable STY-003 reported twice -- once for the anonymous restriction, once for :Chassis.
27 green, 0 red
[exit 0]
```

</details>

Needs the same sibling suite checkout as C09.15.

---

<a id="c09-17"></a>
### C09.17 — Fourteen of 38 questions need no data

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-17) · [plain edition](../docs/09-continuous-integration.md#one-folder-per-question)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Fourteen of the

**Sources:**

- [testing repo experiments/SpecificTests/REVIEW.md](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/experiments/SpecificTests/REVIEW.md#L32-L41): “Half the tests can be answered before a row of data exists.” (quote found, checked 2026-10-22)

---

<a id="c09-18"></a>
### C09.18 — A clean minimal ontology is not writable

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-18) · [plain edition](../docs/09-continuous-integration.md#one-folder-per-question)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **A clean minimal ontology is not writable.**

**Sources:**

- [testing repo commit fb24a3d](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/fb24a3d302409deea6b31da5d061a3edb54839a2): “A clean minimal ontology turns out not to be writable, which is worth knowing before a clean run is read as proof.” (quote found, checked 2026-10-22)

---

<a id="c09-19"></a>
### C09.19 — Seventeen fixtures; 58 of 61 checks pinned

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-19) · [plain edition](../docs/09-continuous-integration.md#the-pattern-a-fixture-per-error-category)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Seventeen fixtures, of which a sample:

**Sources:**

- [testing repo detect.py (17 fixtures declared)](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/detect.py) (exists, checked 2026-10-22)
- [testing repo README](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/README.md#L35-L37): “58 of the 61 checks are pinned by a test” (quote found, checked 2026-10-22)

---

<a id="c09-20"></a>
### C09.20 — The message assertion found EFF-001 within minutes

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-20) · [plain edition](../docs/09-continuous-integration.md#five-assertions-not-one)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> message read *"(reaching nced07cc7cad44c0499fd01e010fb1164b1)"*

**Sources:**

- [testing repo commit 34606a4](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/34606a42744cba730cc58944155549631225d621): “The second found EFF-001 immediately, on 10-efficiency” (quote found, checked 2026-10-22)
- [suite commit 5360394](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/5360394d1ac92537998116245662b15fee8636c7) (exists, checked 2026-10-22)

---

<a id="c09-21"></a>
### C09.21 — A gate as a config file

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-21) · [plain edition](../docs/09-continuous-integration.md#a-gate-as-a-config-file)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The testing repository carries a small `gate.py`

**Sources:**

- [testing repo ontology-suite.yml](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/ontology-suite.yml) (exists, checked 2026-10-22)
- [testing repo commit 3c5afbd](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/3c5afbdb2c5196ebd3f2c7c05be6ceb07c8e9c28): “the gate ran eight checks while its merged registry declared 61” (quote found, checked 2026-10-22)

---

<a id="c09-22"></a>
### C09.22 — An ignored gate dies

**In the manual:** [Chapter 9, at the claim](manual/docs/09-continuous-integration.md#ev-c09-22) · [plain edition](../docs/09-continuous-integration.md#92-the-problem-479-findings)  
**Kind:** Argument · **Result:** Argument

> **This is the commonest way a semantic quality gate dies.**

A judgement from experience, not a measurement. The mechanism it rests on is measurable: C09.02 (479 findings, one Violation in 55 the team's own) against C09.04 (23, all theirs).

---

<a id="chapter-10"></a>
## 10. Ingest and transform

Annotated chapter: [manual/docs/10-ingest-and-transform.md](manual/docs/10-ingest-and-transform.md) · plain chapter: [../docs/10-ingest-and-transform.md](../docs/10-ingest-and-transform.md)

<a id="c10-01"></a>
### C10.01 — sketch: 38 Infos, 8 triples and 7 entities from one query file

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-01) · [plain edition](../docs/10-ingest-and-transform.md#102-stage-1-sketch-before-any-csv-is-read)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The summary line is the useful part: **8 triples, 7 entities from 1 query

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_01/sketch
python scripts/summarise_findings.py work/C10_01/sketch/full_results.csv
python scripts/summarise_findings.py work/C10_01/sketch/full_results.csv --by focus --check TQL-003
```

**What is checked:** 38 Infos: 35 CNF-005 and 3 TQL-003 (?name, ?role, ?skill); 8 triples and 7 entities from 1 file

**Recorded result:** PASS — step 1: 38 findings (0 V, 0 W, 38 I); step 1 output contains 'Sketch used 1 query file(s); 8 triples, 7 entities.'; sketch/full_results.csv: {'CNF-005': 35, 'TQL-003': 3}; TQL-003 on ?name, ?role, ?skill

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_01/sketch
Findings: 38 total (0 Violation, 0 Warning, 38 Info)
Reports written to: ./work/C10_01/sketch
  - work/C10_01/sketch/findings.txt (start here -- what, where, and the source line)
  - work/C10_01/sketch/report.html
  - work/C10_01/sketch/full_results.csv
Sketch used 1 query file(s); 8 triples, 7 entities.
[exit 0]

$ python scripts/summarise_findings.py work/C10_01/sketch/full_results.csv
 35 x CNF-005  Info      Ontology class never populated
  3 x TQL-003  Info      CONSTRUCT variable not bound in the query
total 38: 0 Violation, 0 Warning, 38 Info
[exit 0]

$ python scripts/summarise_findings.py work/C10_01/sketch/full_results.csv --by focus --check TQL-003
TQL-003  focus=?name  path=employees.rq  value=-
TQL-003  focus=?role  path=employees.rq  value=-
TQL-003  focus=?skill  path=employees.rq  value=-
total 3: 0 Violation, 0 Warning, 3 Info
[exit 0]
```

</details>

---

<a id="c10-02"></a>
### C10.02 — The 38 Infos, and what TQL-003 says

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-02) · [plain edition](../docs/10-ingest-and-transform.md#102-stage-1-sketch-before-any-csv-is-read)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The 38 Infos are 35 × `CNF-005`

**Evidence:** the same as [C10.01 — sketch: 38 Infos, 8 triples and 7 entities from one query file](#c10-01), which reproduces it: step 1: 38 findings (0 V, 0 W, 38 I); step 1 output contains 'Sketch used 1 query file(s); 8 triples, 7 entities.'; sketch/full_results.csv: {'CNF-005': 35, 'TQL-003': 3}; TQL-003 on ?name, ?role, ?skill

---

<a id="c10-03"></a>
### C10.03 — --queries, --query-pattern (alias --file-pattern), four extensions

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-03) · [plain edition](../docs/10-ingest-and-transform.md#102-stage-1-sketch-before-any-csv-is-read)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `--queries` takes a file or a directory. Use `--query-pattern` to narrow or widen

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --help
```

**What is checked:** `sketch --help` gives --file-pattern as an alias of --query-pattern, defaulting to the four extensions

**Recorded result:** PASS — step 1 output contains '--query-pattern QUERY_PATTERN, --file-pattern QUERY_PATTERN', '*.sparql,*.rq,*.tarql,*.tq'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --help
usage: ontology-quality-suite sketch [-h] --queries QUERIES
                                     [--ontology ONTOLOGY]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--query-pattern QUERY_PATTERN]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--sparql SPARQL] [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [-v]
options:
  -h, --help            show this help message and exit
  --queries QUERIES
  --ontology ONTOLOGY   if given, diff the sketch's classes/properties against
                        the ontology's declarations
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --query-pattern QUERY_PATTERN, --file-pattern QUERY_PATTERN
                        comma-separated glob pattern(s) used to find query
                        files when --queries is a folder (default:
                        *.sparql,*.rq,*.tarql,*.tq). Also accepted as --file-
                        pattern, the older spelling.
  --registry REGISTRY
  --themes THEMES       a JSON or CSV map of check id to a question in your
                        own words, used to add a "by question" index to
… (13 lines omitted; full output in the outputs/ record)
                        -- and skips the plotting, which is most of the time a
                        small run spends
  --fail-on {Violation,Warning,Info,never}
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

---

<a id="c10-04"></a>
### C10.04 — TQL-004, with its position as fields

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-04) · [plain edition](../docs/10-ingest-and-transform.md#the-query-itself-is-checked)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Since 0.17.0 the TARQL checks carry their position as **fields**

**Inputs:** [`data/tql004/sites.rq`](data/tql004/sites.rq)

<details><summary><code>data/tql004/sites.rq</code></summary>

```sparql
PREFIX acme: <https://acme.example.org/ns/>

# Chapter 10: a defective mapping. ?site_IRI is built with CONCAT, which returns
# a string, and nothing turns it into an IRI. TQL-004 should report it, with the
# file and the line of the BIND as fields of the finding.
CONSTRUCT {
  ?site_IRI a acme:Department .
}
WHERE {
  BIND(CONCAT("https://acme.example.org/data/department/", ?department) AS ?site_IRI)
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --queries data/tql004/sites.rq --out-dir work/C10_04/tq --reports minimal --fail-on never
```

**What is checked:** TQL-004 fires once, with source_file sites.rq and line 10 as fields (not in the message), and findings.txt quotes line 10

**Recorded result:** PASS — tq/full_results.csv: {'TQL-004': 1}; TQL-004 carries source_file sites.rq and line 10 as fields; and not in the message text; its message says the triples are dropped; tq/findings.txt contains '> 10 |   BIND(CONCAT('

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --queries data/tql004/sites.rq --out-dir work/C10_04/tq --reports minimal --fail-on never
Findings: 1 total (1 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C10_04/tq
  - work/C10_04/tq/findings.txt (start here -- what, where, and the source line)
  - work/C10_04/tq/full_results.csv
Sketch used 1 query file(s); 1 triples, 1 entities.
[exit 0]
```

</details>

---

<a id="c10-05"></a>
### C10.05 — A CONCAT-built IRI: dropped as a subject, a literal as an object

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-05) · [plain edition](../docs/10-ingest-and-transform.md#the-query-itself-is-checked)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `TQL-004` repays reading twice.

**Inputs:** [`data/tql004/sites.rq`](data/tql004/sites.rq), [`data/tql004/works-in.rq`](data/tql004/works-in.rq), [`data/tql004/depts.csv`](data/tql004/depts.csv)

<details><summary><code>data/tql004/sites.rq</code></summary>

```sparql
PREFIX acme: <https://acme.example.org/ns/>

# Chapter 10: a defective mapping. ?site_IRI is built with CONCAT, which returns
# a string, and nothing turns it into an IRI. TQL-004 should report it, with the
# file and the line of the BIND as fields of the finding.
CONSTRUCT {
  ?site_IRI a acme:Department .
}
WHERE {
  BIND(CONCAT("https://acme.example.org/data/department/", ?department) AS ?site_IRI)
}
```

</details>

<details><summary><code>data/tql004/works-in.rq</code></summary>

```sparql
PREFIX acme: <https://acme.example.org/ns/>

# Chapter 10: the same defect with the CONCAT result as an object. Here it is
# not dropped but written as a string literal where an IRI was meant.
CONSTRUCT {
  ?employee_IRI acme:worksIn ?dept_IRI .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?department)) AS ?employee_IRI)
  BIND(CONCAT("https://acme.example.org/data/department/", ?department) AS ?dept_IRI)
}
```

</details>

<details><summary><code>data/tql004/depts.csv</code></summary>

```text
department
ENG
QA
```

</details>

**Commands** (from the `evidence/` folder):

```bash
tarka run -q data/tql004/sites.rq -i data/tql004/depts.csv --ntriples
tarka run -q data/tql004/works-in.rq -i data/tql004/depts.csv --ntriples
```

**What is checked:** both runs exit 0; the subject case writes nothing; the object case writes the department as a string literal

**Recorded result:** PASS — step 1 exits 0; as a subject: no triples at all; step 2 exits 0; step 2 output contains '<https://acme.example.org/ns/worksIn> "https://acme.example.org/data/department/ENG" .'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q data/tql004/sites.rq -i data/tql004/depts.csv --ntriples

[exit 0]

$ tarka run -q data/tql004/works-in.rq -i data/tql004/depts.csv --ntriples
<https://acme.example.org/data/employee/ENG> <https://acme.example.org/ns/worksIn> "https://acme.example.org/data/department/ENG" .
<https://acme.example.org/data/employee/QA> <https://acme.example.org/ns/worksIn> "https://acme.example.org/data/department/QA" .
[exit 0]
```

</details>

---

<a id="c10-06"></a>
### C10.06 — sketch writes bind-facts.ttl and bind-review.txt

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-06) · [plain edition](../docs/10-ingest-and-transform.md#the-query-itself-is-checked)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The stage also writes **`bind-facts.ttl`**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_06/sketch --reports minimal
python scripts/list_files.py work/C10_06/sketch
```

**What is checked:** both files are written; bind-review.txt answers its three questions

**Recorded result:** PASS — step 2 output contains 'bind-facts.ttl', 'bind-review.txt'; sketch/bind-review.txt contains '1 query file(s), 3 BIND statement(s)', '1. Variables bound differently across files (0)', '2. Constructed-IRI variables never bound (0)', '3. CONSTRUCT variables not bound in the query (3)', '?name, ?role, ?skill'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_06/sketch --reports minimal
Findings: 38 total (0 Violation, 0 Warning, 38 Info)
Reports written to: ./work/C10_06/sketch
  - work/C10_06/sketch/findings.txt (start here -- what, where, and the source line)
  - work/C10_06/sketch/full_results.csv
Sketch used 1 query file(s); 8 triples, 7 entities.
[exit 0]

$ python scripts/list_files.py work/C10_06/sketch
    3,841  bind-facts.ttl
      684  bind-review.txt
    4,448  findings.txt
   13,787  full_results.csv
      713  sketch.ttl
5 files, 23,473 bytes
[exit 0]
```

</details>

---

<a id="c10-07"></a>
### C10.07 — tarka's output for E004 is the block quoted in earlier editions

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-07) · [plain edition](../docs/10-ingest-and-transform.md#103-stage-2-produce-real-rdf-with-tarka)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The output is genuine RDF, and for this fixture it is the same, term for term

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_07/employees.ttl
```

**What is checked:** the E004 block in tarka's Turtle is byte-identical to the manual's listing

**Recorded result:** PASS — step 1 exits 0; employees.ttl contains '<https://acme.example.org/data/employee/E004> a acme:Employe'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_07/employees.ttl

[exit 0]
```

</details>

**Sources:**

- [the previous edition's oxi-gen listing](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/10-ingest-and-transform.md): “foaf:mbox <mailto:margaret.hamilton@acme.example.org> ;” (quote found, checked 2026-10-22)

---

<a id="c10-08"></a>
### C10.08 — tarka takes oxi-gen's options; --test N reads N rows

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-08) · [plain edition](../docs/10-ingest-and-transform.md#103-stage-2-produce-real-rdf-with-tarka)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> tarka takes `oxi-gen`'s options

**Commands** (from the `evidence/` folder):

```bash
tarka run --help
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples --test 2 -o work/C10_08/two.nt
python scripts/compare_ntriples.py work/C10_08/two.nt work/C10_08/two.nt
```

**What is checked:** --help lists the oxi-gen options; --test 2 gives 16 triples (2 rows × 8)

**Recorded result:** PASS — step 1 output contains '--ntriples', '--split', '--dedup', '--test', '--bind-empty-strings', '--gzip', '--no-header-row', '--delimiter', '--tab', '--header'; step 3 output contains '16 triples'

<details><summary>Output, as recorded</summary>

```text
$ tarka run --help
Map a CSV file to RDF with a TARQL query (-q) or an OTTR template (-l … -T …)
Usage: tarka.exe run [OPTIONS]
Options:
  -q, --query <QUERY>
          A TARQL query (SPARQL CONSTRUCT)
  -l, --library <LIBRARY>
          An OTTR template file or directory (repeat for more)
  -T, --template <TEMPLATE>
          A root template, by IRI or prefixed name; its parameters are CSV columns. Repeat it to instantiate several templates for every row
      --list <COLUMN> <SEPARATOR>
          The cells of a list-typed parameter are split on SEPARATOR
  -i, --input <INPUT>
          The input: a CSV file, or a Parquet or Arrow IPC file (default: the file the query names with FROM, else standard input)
  -d, --delimiter <DELIMITER>
          The field delimiter [default: ,]
  -t, --tab
          Fields are tab-separated
  -p, --escape-char <ESCAPE_CHAR>
          The escape character inside quoted fields [default: \]
      --quote-char <QUOTE_CHAR>
          The quote character [default: "]
  -n, --normalize
          Upper-case the column names
  -H, --no-header-row
          The file has no header row: columns are a…z, A…Z
      --split <ORIGINAL> <SPLIT> <DELIMITER>
          Repeat each row once per part of column ORIGINAL split on DELIMITER, with the part in column SPLIT
      --bind-empty-strings
          Bind empty cells as empty strings instead of leaving them unbound
      --test [<TEST>]
… (25 lines omitted; full output in the outputs/ record)
      --batch-size <BATCH_SIZE>
          Records to evaluate together [default: 512]
      --jobs <JOBS>
          Batches to work on at once (0: one per CPU) [default: 0]
      --stats
          Print what was read and made to standard error
  -h, --help
          Print help
[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples --test 2 -o work/C10_08/two.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_08/two.nt work/C10_08/two.nt
work/C10_08/two.nt: 16 triples
work/C10_08/two.nt: 16 triples
isomorphic: True
[exit 0]
```

</details>

---

<a id="c10-09"></a>
### C10.09 — 1.7× and 2.6× faster than oxi-gen, by tarka's own measurement

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-09) · [plain edition](../docs/10-ingest-and-transform.md#103-stage-2-produce-real-rdf-with-tarka)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Its own measurement, on a

**Sources:**

- [tarka README](https://github.com/pwin/tarka/blob/88fe6184ffc77ee2a46b676cbcb1190620b52c49/README.md#L41-L43): “tarka ran the TARQL query 1.7 times as fast as oxi-gen, and the OTTR templates 2.6 times as fast.” (quote found, checked 2026-10-22)

Not reproduced here: it needs oxi-gen and the 200,000-row file.

---

<a id="c10-10"></a>
### C10.10 — The OTTR template lints clean and gives the same 40 triples

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-10) · [plain edition](../docs/10-ingest-and-transform.md#tarql-or-ottr-two-ways-to-say-the-same-mapping)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Sorted, the 40 triples are identical to the TARQL query's. Verified.

**Inputs:** [`data/ottr/employees.stottr`](data/ottr/employees.stottr), [`data/ottr/employees-iri.csv`](data/ottr/employees-iri.csv)

<details><summary><code>data/ottr/employees.stottr</code></summary>

```text
@prefix mailto: <mailto:> .
@prefix acme: <https://acme.example.org/ns/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

acme:Employee [ ottr:IRI ?employee, xsd:string ?name, ottr:IRI ?mbox, xsd:string ?id,
                ottr:IRI ?dept, xsd:string ?role, xsd:string ?skill ] :: {
    ottr:Triple(?employee, rdf:type, acme:Employee),
    ottr:Triple(?employee, rdf:type, acme:Engineer),
    ottr:Triple(?employee, foaf:name, ?name),
    ottr:Triple(?employee, foaf:mbox, ?mbox),
    ottr:Triple(?employee, acme:hasEmployeeId, ?id),
    ottr:Triple(?employee, acme:worksIn, ?dept),
    ottr:Triple(?employee, acme:hasRole, ?role),
    ottr:Triple(?employee, acme:hasSkill, ?skill)
} .
```

</details>

<details><summary><code>data/ottr/employees-iri.csv</code></summary>

```text
employee,name,mbox,id,dept,role,skill
https://acme.example.org/data/employee/E001,Grace Hopper,mailto:grace.hopper@acme.example.org,E001,https://acme.example.org/data/department/ENG,Software Engineer,Rust
https://acme.example.org/data/employee/E002,Ada Lovelace,mailto:ada.lovelace@acme.example.org,E002,https://acme.example.org/data/department/ENG,Software Engineer,SPARQL
https://acme.example.org/data/employee/E003,Alan Turing,mailto:alan.turing@acme.example.org,E003,https://acme.example.org/data/department/ENG,Software Engineer,SHACL
https://acme.example.org/data/employee/E004,Margaret Hamilton,mailto:margaret.hamilton@acme.example.org,E004,https://acme.example.org/data/department/QA,Test Engineer,Automation
https://acme.example.org/data/employee/E005,Katherine Johnson,mailto:katherine.johnson@acme.example.org,E005,https://acme.example.org/data/department/MKT,Analyst,Forecasting
```

</details>

**Commands** (from the `evidence/` folder):

```bash
tarka lint -l data/ottr/employees.stottr
tarka run -l data/ottr/employees.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_10/ottr.nt
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples -o work/C10_10/tarql.nt
python scripts/compare_ntriples.py work/C10_10/ottr.nt work/C10_10/tarql.nt
```

**What is checked:** lint reports 0 errors and 0 warnings; the OTTR and TARQL outputs are the same 40 triples

**Recorded result:** PASS — step 1 output contains '1 template: 0 errors, 0 warnings'; step 4 output contains '40 triples', 'isomorphic: True'

<details><summary>Output, as recorded</summary>

```text
$ tarka lint -l data/ottr/employees.stottr
1 template: 0 errors, 0 warnings
[exit 0]

$ tarka run -l data/ottr/employees.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_10/ottr.nt

[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples -o work/C10_10/tarql.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_10/ottr.nt work/C10_10/tarql.nt
work/C10_10/ottr.nt: 40 triples
work/C10_10/tarql.nt: 40 triples
isomorphic: True
[exit 0]
```

</details>

The CSV for the template carries full IRIs, since an OTTR template receives IRIs rather than building them.

---

<a id="c10-11"></a>
### C10.11 — Without a mailto: prefix, run -l drops every row, silently

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-11) · [plain edition](../docs/10-ingest-and-transform.md#tarql-or-ottr-two-ways-to-say-the-same-mapping)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **One silent failure, found while checking this.**

**Inputs:** [`data/ottr/employees-no-mailto-prefix.stottr`](data/ottr/employees-no-mailto-prefix.stottr), [`data/ottr/employees-optional-mbox.stottr`](data/ottr/employees-optional-mbox.stottr), [`data/ottr/employees.bottr.ttl`](data/ottr/employees.bottr.ttl), [`data/ottr/employees-bad-id.bottr.ttl`](data/ottr/employees-bad-id.bottr.ttl)

<details><summary><code>data/ottr/employees-no-mailto-prefix.stottr</code></summary>

```text
@prefix acme: <https://acme.example.org/ns/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

acme:Employee [ ottr:IRI ?employee, xsd:string ?name, ottr:IRI ?mbox, xsd:string ?id,
                ottr:IRI ?dept, xsd:string ?role, xsd:string ?skill ] :: {
    ottr:Triple(?employee, rdf:type, acme:Employee),
    ottr:Triple(?employee, rdf:type, acme:Engineer),
    ottr:Triple(?employee, foaf:name, ?name),
    ottr:Triple(?employee, foaf:mbox, ?mbox),
    ottr:Triple(?employee, acme:hasEmployeeId, ?id),
    ottr:Triple(?employee, acme:worksIn, ?dept),
    ottr:Triple(?employee, acme:hasRole, ?role),
    ottr:Triple(?employee, acme:hasSkill, ?skill)
} .
```

</details>

<details><summary><code>data/ottr/employees-optional-mbox.stottr</code></summary>

```text
# Chapter 10 §10.3: the no-prefix template again, with ?mbox made optional (?).
# Now only the mailbox triple goes missing for each row, just as quietly.
@prefix acme: <https://acme.example.org/ns/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

acme:Employee [ ottr:IRI ?employee, xsd:string ?name, ? ottr:IRI ?mbox, xsd:string ?id,
                ottr:IRI ?dept, xsd:string ?role, xsd:string ?skill ] :: {
    ottr:Triple(?employee, rdf:type, acme:Employee),
    ottr:Triple(?employee, rdf:type, acme:Engineer),
    ottr:Triple(?employee, foaf:name, ?name),
    ottr:Triple(?employee, foaf:mbox, ?mbox),
    ottr:Triple(?employee, acme:hasEmployeeId, ?id),
    ottr:Triple(?employee, acme:worksIn, ?dept),
    ottr:Triple(?employee, acme:hasRole, ?role),
    ottr:Triple(?employee, acme:hasSkill, ?skill)
} .
```

</details>

<details><summary><code>data/ottr/employees.bottr.ttl</code></summary>

```turtle
# Chapter 10 §10.3: the same rows and template as `tarka run -l`, as a bOTTR
# instance map, with no `mailto:` prefix declared anywhere. Here a cell typed
# ottr:IRI is read as a full IRI, and mailto:… is one, so every row comes out.
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix acme: <https://acme.example.org/ns/> .

[] a ottr:InstanceMap ;
   ottr:template acme:Employee ;
   ottr:source [ a ottr:H2Source ] ;
   ottr:query """SELECT employee, name, mbox, id, dept, role, skill FROM CSVREAD('@@THIS_DIR@@/employees-iri.csv')""" ;
   ottr:argumentMaps ( [ ottr:type ottr:IRI ] [ ] [ ottr:type ottr:IRI ] [ ] [ ottr:type ottr:IRI ] [ ] [ ] ) .
```

</details>

<details><summary><code>data/ottr/employees-bad-id.bottr.ttl</code></summary>

```turtle
# Chapter 10 §10.3: a bOTTR map that cannot build any instance. The id column
# is mapped as xsd:integer, and 'E001' is not one. bOTTR leaves each instance
# out, names the row and the argument, and exits 1: the report `tarka run`
# does not give.
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix acme: <https://acme.example.org/ns/> .

[] a ottr:InstanceMap ;
   ottr:template acme:Employee ;
   ottr:source [ a ottr:H2Source ] ;
   ottr:query """SELECT employee, name, mbox, id, dept, role, skill FROM CSVREAD('@@THIS_DIR@@/employees-iri.csv')""" ;
   ottr:argumentMaps ( [ ottr:type ottr:IRI ] [ ] [ ottr:type ottr:IRI ] [ ottr:type xsd:integer ]
                       [ ottr:type ottr:IRI ] [ ] [ ] ) .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
tarka run -l data/ottr/employees-no-mailto-prefix.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_11/none.nt
python scripts/compare_ntriples.py work/C10_11/none.nt work/C10_11/none.nt
tarka run -l data/ottr/employees-optional-mbox.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_11/optional.nt
python scripts/compare_ntriples.py work/C10_11/optional.nt work/C10_11/optional.nt
tarka bottr -l data/ottr/employees.stottr data/ottr/employees-bad-id.bottr.ttl --ntriples -o work/C10_11/bad-id.nt
tarka bottr -l data/ottr/employees-no-mailto-prefix.stottr data/ottr/employees.bottr.ttl --ntriples -o work/C10_11/bottr.nt
python scripts/compare_ntriples.py work/C10_11/bottr.nt work/C10_11/bottr.nt
```

**What is checked:** run -l without the prefix: exit 0, no message, 0 triples; with ?mbox optional: exit 0, 35 triples; bOTTR with a cell it cannot build: each instance reported, exit 1; the same rows as a bOTTR map with no prefix: 40 triples

**Recorded result:** PASS — step 1 exits 0; run -l: no message at all; step 2 output contains ': 0 triples'; step 3 exits 0; step 4 output contains ': 35 triples'; step 4 output has none of 'mbox'; step 5 exits 1; step 5 output contains '5 instances left out; the other 0 were made', 'row 1: argument 4 (id)'; step 6 exits 0; step 7 output contains ': 40 triples'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -l data/ottr/employees-no-mailto-prefix.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_11/none.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_11/none.nt work/C10_11/none.nt
work/C10_11/none.nt: 0 triples
work/C10_11/none.nt: 0 triples
isomorphic: True
[exit 0]

$ tarka run -l data/ottr/employees-optional-mbox.stottr -T acme:Employee -i data/ottr/employees-iri.csv --ntriples -o work/C10_11/optional.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_11/optional.nt work/C10_11/optional.nt
work/C10_11/optional.nt: 35 triples
work/C10_11/optional.nt: 35 triples
isomorphic: True
[exit 0]

$ tarka bottr -l data/ottr/employees.stottr data/ottr/employees-bad-id.bottr.ttl --ntriples -o work/C10_11/bad-id.nt
tarka: left out: data/ottr/employees-bad-id.bottr.ttl: instance map 1 (acme:Employee), row 1: argument 4 (id): the value 'E001' is not in the lexical space of its datatype http://www.w3.org/2001/XMLSchema#integer
tarka: left out: data/ottr/employees-bad-id.bottr.ttl: instance map 1 (acme:Employee), row 2: argument 4 (id): the value 'E002' is not in the lexical space of its datatype http://www.w3.org/2001/XMLSchema#integer
tarka: left out: data/ottr/employees-bad-id.bottr.ttl: instance map 1 (acme:Employee), row 3: argument 4 (id): the value 'E003' is not in the lexical space of its datatype http://www.w3.org/2001/XMLSchema#integer
tarka: left out: data/ottr/employees-bad-id.bottr.ttl: instance map 1 (acme:Employee), row 4: argument 4 (id): the value 'E004' is not in the lexical space of its datatype http://www.w3.org/2001/XMLSchema#integer
tarka: left out: data/ottr/employees-bad-id.bottr.ttl: instance map 1 (acme:Employee), row 5: argument 4 (id): the value 'E005' is not in the lexical space of its datatype http://www.w3.org/2001/XMLSchema#integer
tarka: 5 instances left out; the other 0 were made
[exit 1]

$ tarka bottr -l data/ottr/employees-no-mailto-prefix.stottr data/ottr/employees.bottr.ttl --ntriples -o work/C10_11/bottr.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_11/bottr.nt work/C10_11/bottr.nt
work/C10_11/bottr.nt: 40 triples
work/C10_11/bottr.nt: 40 triples
isomorphic: True
[exit 0]
```

</details>

---

<a id="c10-12"></a>
### C10.12 — Parquet input, data frames, and typed literals from typed columns

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-12) · [plain edition](../docs/10-ingest-and-transform.md#data-frames-not-just-csv)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `-i` takes Parquet and Arrow IPC files as well as CSV, read with Polars, and the

**Inputs:** [`data/ottr/headcount.stottr`](data/ottr/headcount.stottr)

<details><summary><code>data/ottr/headcount.stottr</code></summary>

```text
# Chapter 10 §10.3: a template with a typed parameter. Fed from a Polars
# integer column, ?n arrives as an xsd:integer literal, with no STRDT anywhere.
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix acme: <https://acme.example.org/ns/> .

acme:Headcount [ ottr:IRI ?dept, xsd:integer ?n ] :: {
    ottr:Triple(?dept, acme:headcount, ?n)
} .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/tarka_python.py fixtures/acme_robotics data/ottr work/C10_12
tarka run -q fixtures/acme_robotics/employees.rq -i work/C10_12/employees.parquet --ntriples -o work/C10_12/parquet.nt
python scripts/compare_ntriples.py work/C10_12/parquet.nt work/C10_12/tarql.nt
```

<details><summary><code>scripts/tarka_python.py</code></summary>

```python
"""Chapter 10: tarka through the tarka-rdf package (no command line needed).

    python scripts/tarka_python.py fixtures/acme_robotics data/ottr work/C10_xx

  1. the acme TARQL mapping, run with Mapping.tarql_file(...).run_csv(...)
  2. the same mapping as OTTR templates, compared triple for triple
  3. the OTTR library without its `mailto:` prefix: the silent zero
  4. the acme CSV as a Polars data frame, written to Parquet, and mapped from it
  5. the shapes tarka derives from the TARQL mapping
  6. a Polars integer column into an xsd:integer OTTR parameter: a typed literal
"""
import sys
from pathlib import Path

import polars as pl
import tarka_rdf

sys.stdout.reconfigure(encoding="utf-8")
acme, ottr, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)


def lines(p: Path):
    return sorted(l for l in p.read_text(encoding="utf-8").splitlines() if l.strip())


tarql = tarka_rdf.Mapping.tarql_file(str(acme / "employees.rq"))
tarql.run_csv(str(acme / "employees.csv"), str(work / "tarql.nt"), format="ntriples")
t = lines(work / "tarql.nt")
print(f"1. TARQL mapping: {len(t)} triples")

o = tarka_rdf.Mapping.ottr([str(ottr / "employees.stottr")], ["acme:Employee"])
o.run_csv(str(ottr / "employees-iri.csv"), str(work / "ottr.nt"), format="ntriples")
ot = lines(work / "ottr.nt")
print(f"2. OTTR templates: {len(ot)} triples; identical to the TARQL output: {ot == t}")

bad = tarka_rdf.Mapping.ottr([str(ottr / "employees-no-mailto-prefix.stottr")], ["acme:Employee"])
try:
    ret = bad.run_csv(str(ottr / "employees-iri.csv"), str(work / "ottr-no-prefix.nt"), format="ntriples")
    n = len(lines(work / "ottr-no-prefix.nt"))
    print(f"3. OTTR without the mailto: prefix: returned {ret!r}, raised nothing, wrote {n} triples")
except Exception as exc:
    print(f"3. OTTR without the mailto: prefix: raised {type(exc).__name__}: {exc}")

df = pl.read_csv(acme / "employees.csv")
df.write_parquet(work / "employees.parquet")
frame = tarql.triplify(df)
print(f"4. Polars frame of {df.height} rows -> {frame.height} triples; "
      f"Parquet written to {(work / 'employees.parquet').as_posix()}")

shapes = tarql.shapes()
(work / "employees.shapes.ttl").write_text(shapes, encoding="utf-8")
print("5. shapes derived from the mapping:")
print("\n".join("   " + l for l in shapes.splitlines() if "sh:path" in l or "NodeShape" in l))

counts = pl.DataFrame({"dept": ["https://acme.example.org/data/department/ENG",
                                "https://acme.example.org/data/department/QA"], "n": [42, 7]})
typed = tarka_rdf.Mapping.ottr([str(ottr / "headcount.stottr")], ["acme:Headcount"]).triplify(counts)
print(f"6. a {counts.schema['n']} column through an xsd:integer parameter:")
for subject, predicate, obj in typed.iter_rows():
    print(f"   {subject} {predicate} {obj}")
```

</details>

**What is checked:** a Polars frame maps to 40 triples; an Int64 column through an xsd:integer parameter gives "42"^^xsd:integer; the CLI reads the Parquet file and gives the same 40 triples; the Python API shows the same silent zero as the CLI

**Recorded result:** PASS — step 1 output contains '4. Polars frame of 5 rows -> 40 triples', '"42"^^<http://www.w3.org/2001/XMLSchema#integer>', '2. OTTR templates: 40 triples; identical to the TARQL output: True', '3. OTTR without the mailto: prefix: returned None, raised nothing, wrote 0 triples'; step 3 output contains 'isomorphic: True'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/tarka_python.py fixtures/acme_robotics data/ottr work/C10_12
1. TARQL mapping: 40 triples
2. OTTR templates: 40 triples; identical to the TARQL output: True
3. OTTR without the mailto: prefix: returned None, raised nothing, wrote 0 triples
4. Polars frame of 5 rows -> 40 triples; Parquet written to work/C10_12/employees.parquet
5. shapes derived from the mapping:
   shape:EmployeeShape a sh:NodeShape ;
           [ sh:path foaf:mbox ; sh:nodeKind sh:IRI ] ,
           [ sh:path foaf:name ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasEmployeeId ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasRole ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasSkill ; sh:datatype xsd:string ] ,
           [ sh:path acme:worksIn ; sh:nodeKind sh:IRI ] .
   shape:EngineerShape a sh:NodeShape ;
           [ sh:path foaf:mbox ; sh:nodeKind sh:IRI ] ,
           [ sh:path foaf:name ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasEmployeeId ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasRole ; sh:datatype xsd:string ] ,
           [ sh:path acme:hasSkill ; sh:datatype xsd:string ] ,
           [ sh:path acme:worksIn ; sh:nodeKind sh:IRI ] .
6. a Int64 column through an xsd:integer parameter:
   <https://acme.example.org/data/department/ENG> <https://acme.example.org/ns/headcount> "42"^^<http://www.w3.org/2001/XMLSchema#integer>
   <https://acme.example.org/data/department/QA> <https://acme.example.org/ns/headcount> "7"^^<http://www.w3.org/2001/XMLSchema#integer>
[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i work/C10_12/employees.parquet --ntriples -o work/C10_12/parquet.nt

[exit 0]

$ python scripts/compare_ntriples.py work/C10_12/parquet.nt work/C10_12/tarql.nt
work/C10_12/parquet.nt: 40 triples
work/C10_12/tarql.nt: 40 triples
isomorphic: True
[exit 0]
```

</details>

---

<a id="c10-13"></a>
### C10.13 — Shapes from the mapping, and --validate conforms

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-13) · [plain edition](../docs/10-ingest-and-transform.md#shapes-from-the-mapping-and-what-they-cannot-tell-you)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> and `tarka run … --validate` checks the output against them. On the acme data

**Commands** (from the `evidence/` folder):

```bash
tarka shapes -q fixtures/acme_robotics/employees.rq -o work/C10_13/employees.shapes.ttl
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_13/employees.ttl --validate --report work/C10_13/report.ttl
```

**What is checked:** the shapes target acme:Employee with worksIn and mbox as IRIs; the validated run conforms

**Recorded result:** PASS — step 1 exits 0; step 2 exits 0; employees.shapes.ttl contains 'sh:targetClass acme:Employee', '[ sh:path acme:worksIn ; sh:nodeKind sh:IRI ]', '[ sh:path foaf:mbox ; sh:nodeKind sh:IRI ]'; report.ttl contains 'sh:conforms true'

<details><summary>Output, as recorded</summary>

```text
$ tarka shapes -q fixtures/acme_robotics/employees.rq -o work/C10_13/employees.shapes.ttl

[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_13/employees.ttl --validate --report work/C10_13/report.ttl

[exit 0]
```

</details>

---

<a id="c10-14"></a>
### C10.14 — Generated shapes accept the dangling departments

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-14) · [plain edition](../docs/10-ingest-and-transform.md#shapes-from-the-mapping-and-what-they-cannot-tell-you)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> That is useful, and it is worth being exact about why.

**Evidence:** the same as [C10.13 — Shapes from the mapping, and --validate conforms](#c10-13), which reproduces it: step 1 exits 0; step 2 exits 0; employees.shapes.ttl contains 'sh:targetClass acme:Employee', '[ sh:path acme:worksIn ; sh:nodeKind sh:IRI ]', '[ sh:path foaf:mbox ; sh:nodeKind sh:IRI ]'; report.ttl contains 'sh:conforms true'

The same run that conforms (C10.13) is the one in which `data` finds every `worksIn` target untyped and dangling (C10.19).

---

<a id="c10-15"></a>
### C10.15 — --post streams into holos-server: the graph arrives whole

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-15) · [plain edition](../docs/10-ingest-and-transform.md#straight-into-a-store)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified for this edition against `holos-server`: the

Started first, and stopped afterwards:

```bash
holos-server --listen 127.0.0.1:7899 --no-ui
```

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees
python scripts/endpoint_stats.py http://127.0.0.1:7899/query
```

**What is checked:** the post succeeds and the named graph holds 40 triples

**Recorded result:** PASS — step 1 exits 0; step 2 output contains 'https://acme.example.org/graph/triplified/employees', '40'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees

[exit 0]

$ python scripts/endpoint_stats.py http://127.0.0.1:7899/query
g,triples
https://acme.example.org/graph/triplified/employees,40
[exit 0]
```

</details>

---

<a id="c10-16"></a>
### C10.16 — tarka speaks the protocol, in RDF 1.1, with the engine built without RDF 1.2

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-16) · [plain edition](../docs/10-ingest-and-transform.md#straight-into-a-store)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> tarka speaks the protocol rather than linking any particular store in

**Sources:**

- [tarka commit 26f256a](https://github.com/pwin/tarka/commit/26f256a28f10d299a4cf1c5dd49ba52cd37122a7) (exists, checked 2026-10-22)
- [tarka README](https://github.com/pwin/tarka/blob/88fe6184ffc77ee2a46b676cbcb1190620b52c49/README.md#L45): “tarka works with RDF 1.1 and SPARQL 1.1.” (quote found, checked 2026-10-22)

---

<a id="c10-17"></a>
### C10.17 — The suite's triplify still needs oxi-gen, and says so

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-17) · [plain edition](../docs/10-ingest-and-transform.md#the-suites-triplify-for-now)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> If you have no `oxi-gen` build, `triplify` says so in a warning and

**Commands** (from the `evidence/` folder):

```bash
# with no oxi-gen configured
ONTOLOGY_SUITE_OXI_GEN_BIN= ontology-quality-suite triplify --csv-dir fixtures/acme_robotics --queries fixtures/acme_robotics --out-dir work/C10_17/out
```

**What is checked:** a warning that oxi-gen was not found, and nothing triplified

**Recorded result:** PASS — step 1 output contains 'WARNING: oxi-gen binary not found', 'Triplified 0 file(s)'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite triplify --csv-dir fixtures/acme_robotics --queries fixtures/acme_robotics --out-dir work/C10_17/out
Triplified 0 file(s) into ./work/C10_17/out
WARNING: oxi-gen binary not found. Build it with `cargo build --release` in the sibling ./.venv/Lib/oxi-gen checkout, or pass --oxi-gen-bin.
[exit 1]
```

</details>

---

<a id="c10-18"></a>
### C10.18 — data: 548 unscoped (549 at 0.23.0, 550 at 0.22.0), 54 scoped, with HermiT running

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-18) · [plain edition](../docs/10-ingest-and-transform.md#104-stage-3-data-assess-what-was-actually-produced)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Findings: 548 total (66 Violation, 363 Warning, 119 Info)

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_18/employees.ttl
PYTHONHASHSEED=5 ontology-quality-suite data work/C10_18/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C10_18/all --fail-on never --reports minimal
PYTHONHASHSEED=5 ontology-quality-suite data work/C10_18/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_18/own --fail-on never --reports minimal
python scripts/summarise_findings.py work/C10_18/own/full_results.csv
```

**What is checked:** unscoped 550 (68 V, 363 W, 119 I) at 0.22.0; 549 (67 V) from 0.23.0, without the false REA-020; 548 (66 V) from 0.24.0, which reports one contradiction once instead of twice. Scoped to https://acme.example.org/: 55 (13 V, 40 W, 2 I) up to 0.23.0 and 54 (12 V) from 0.24.0, with REA-021 throughout

**Recorded result:** PASS — suite 0.24.3: step 2: 548 findings (66 V, 363 W, 119 I); suite 0.24.3: step 3: 54 findings (12 V, 40 W, 2 I); REA-021 present; REA-022 absent

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_18/employees.ttl

[exit 0]

$ ontology-quality-suite data work/C10_18/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C10_18/all --fail-on never --reports minimal
Findings: 548 total (66 Violation, 363 Warning, 119 Info)
Reports written to: ./work/C10_18/all
  - work/C10_18/all/findings.txt (start here -- what, where, and the source line)
  - work/C10_18/all/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmpakcghi3n -Y
[exit 0]

$ ontology-quality-suite data work/C10_18/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_18/own --fail-on never --reports minimal
Findings: 54 total (12 Violation, 40 Warning, 2 Info)
Reports written to: ./work/C10_18/own
  - work/C10_18/own/findings.txt (start here -- what, where, and the source line)
  - work/C10_18/own/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmpdu2v0a26 -Y
[exit 0]

$ python scripts/summarise_findings.py work/C10_18/own/full_results.csv
  2 x CNF-005  Info      Ontology class never populated
 10 x DAT-002  Warning   Dangling IRI reference
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x QUA-001  Warning   Class or property missing rdfs:label
  9 x QUA-004  Warning   Resource missing skos:prefLabel
  9 x QUA-009  Warning   Class or property without one skos:prefLabel per language
  9 x QUA-010  Warning   Class or property without a skos:definition
  1 x REA-021  Violation Class found unsatisfiable by an external DL reasoner
  1 x STR-003  Warning   Property missing both domain and range
 10 x STR-006  Violation Untyped object of a triple
  1 x STY-002  Warning   Property name not lowerCamelCase
total 54: 12 Violation, 40 Warning, 2 Info
[exit 0]
```

</details>

---

<a id="c10-19"></a>
### C10.19 — 54 when HermiT does not run, and from 0.24.0 the scoped report says so

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-19) · [plain edition](../docs/10-ingest-and-transform.md#54-or-55-and-how-the-report-tells-you-which-from-0240)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> That run gave 55 three times running. The fourth time it gave 54.

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_19/employees.ttl
PYTHONHASHSEED=0 python scripts/without_java.py ontology-quality-suite data work/C10_19/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C10_19/all --fail-on never --reports minimal
PYTHONHASHSEED=0 python scripts/without_java.py ontology-quality-suite data work/C10_19/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_19/own --fail-on never --reports minimal
```

<details><summary><code>scripts/without_java.py</code></summary>

```python
"""Run a command with no Java runtime visible, so HermiT cannot start.

    python scripts/without_java.py ontology-quality-suite ontology --ontology ...

Removes every PATH entry holding a `java` executable and unsets JAVA_HOME, then
runs the command. Otherwise whether the DL reasoner runs depends on the hash seed (Chapter 14
§14.4); this takes Java away as well, to show that a missing Java gives a different message.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

env = dict(os.environ)
env.pop("JAVA_HOME", None)
exe = "java.exe" if os.name == "nt" else "java"
keep = [d for d in env.get("PATH", "").split(os.pathsep) if d and not (Path(d) / exe).is_file()]
env["PATH"] = os.pathsep.join(keep)
print(f"without_java: java on PATH now: {shutil.which('java', path=env['PATH']) or 'none'}", flush=True)
cmd = sys.argv[1:]
cmd[0] = shutil.which(cmd[0], path=env["PATH"]) or cmd[0]
sys.exit(subprocess.run(cmd, env=env).returncode)
```

</details>

**What is checked:** with HermiT unable to run: the unscoped run reports REA-022 on every version. The scoped run holds 54 findings on both sides of the fix, but differently -- up to 0.23.0 it had neither REA-021 nor REA-022 (54 = 12 V, 40 W, 2 I), and from 0.24.0 it reports REA-022 (54 = 11 V, 40 W, 3 I): one Violation fewer, because the duplicated LOG-001 is merged, and one Info more, because the reasoner's caveat survives the filter. The total is the same number for two different reasons, which is why a gate should assert on the severity split

**Recorded result:** PASS — suite 0.24.3: step 3: 54 findings (11 V, 40 W, 3 I); REA-022 present; REA-021 absent; suite 0.24.3: REA-022 present; REA-021 absent

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_19/employees.ttl

[exit 0]

$ python scripts/without_java.py ontology-quality-suite data work/C10_19/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --out-dir work/C10_19/all --fail-on never --reports minimal
without_java: java on PATH now: none
Findings: 548 total (65 Violation, 363 Warning, 120 Info)
Reports written to: ./work/C10_19/all
  - work/C10_19/all/findings.txt (start here -- what, where, and the source line)
  - work/C10_19/all/full_results.csv
[exit 0]

$ python scripts/without_java.py ontology-quality-suite data work/C10_19/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_19/own --fail-on never --reports minimal
without_java: java on PATH now: none
Findings: 54 total (11 Violation, 40 Warning, 3 Info)
Reports written to: ./work/C10_19/own
  - work/C10_19/own/findings.txt (start here -- what, where, and the source line)
  - work/C10_19/own/full_results.csv
[exit 0]
```

</details>

The manual's 'three times… the fourth time' describes unpinned runs. Java is hidden here so that the reasoner's failure is certain; C14.06 shows how the hash seed decides it when Java is present.

---

<a id="c10-20"></a>
### C10.20 — Real defects: every worksIn target is untyped and dangling

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-20) · [plain edition](../docs/10-ingest-and-transform.md#what-those-findings-actually-say)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Real data defects.** The largest group:

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_20/employees.ttl
PYTHONHASHSEED=5 ontology-quality-suite data work/C10_20/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_20/own --fail-on never --reports minimal
python scripts/summarise_findings.py work/C10_20/own/full_results.csv --by focus --check STR-006
python scripts/summarise_findings.py work/C10_20/own/full_results.csv --by focus --check CNF-005
```

**What is checked:** STR-006 and DAT-002 each fire 10 times, five on departments and five on mailboxes; CNF-005 on Contractor (and Department); the inherited schema findings on hasSkill and reports_to; REA-021's message as quoted

**Recorded result:** PASS — STR-006: 10, five departments and five mailboxes; DAT-002: 10, five departments and five mailboxes; CNF-005 on https://acme.example.org/ns/Contractor, https://acme.example.org/ns/Department; QUA-001 on https://acme.example.org/ns/hasSkill; STY-002 on https://acme.example.org/ns/reports_to; STR-003 on https://acme.example.org/ns/reports_to; REA-021's message reads as quoted

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C10_20/employees.ttl

[exit 0]

$ ontology-quality-suite data work/C10_20/employees.ttl --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --engine sparql --own-namespace https://acme.example.org/ --out-dir work/C10_20/own --fail-on never --reports minimal
Findings: 54 total (12 Violation, 40 Warning, 2 Info)
Reports written to: ./work/C10_20/own
  - work/C10_20/own/findings.txt (start here -- what, where, and the source line)
  - work/C10_20/own/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmpkpfcnjxt -Y
[exit 0]

$ python scripts/summarise_findings.py work/C10_20/own/full_results.csv --by focus --check STR-006
STR-006  focus=https://acme.example.org/data/employee/E001  path=https://acme.example.org/ns/worksIn  value=https://acme.example.org/data/department/ENG
STR-006  focus=https://acme.example.org/data/employee/E001  path=http://xmlns.com/foaf/0.1/mbox  value=mailto:grace.hopper@acme.example.org
STR-006  focus=https://acme.example.org/data/employee/E002  path=http://xmlns.com/foaf/0.1/mbox  value=mailto:ada.lovelace@acme.example.org
STR-006  focus=https://acme.example.org/data/employee/E002  path=https://acme.example.org/ns/worksIn  value=https://acme.example.org/data/department/ENG
STR-006  focus=https://acme.example.org/data/employee/E003  path=http://xmlns.com/foaf/0.1/mbox  value=mailto:alan.turing@acme.example.org
STR-006  focus=https://acme.example.org/data/employee/E003  path=https://acme.example.org/ns/worksIn  value=https://acme.example.org/data/department/ENG
STR-006  focus=https://acme.example.org/data/employee/E004  path=https://acme.example.org/ns/worksIn  value=https://acme.example.org/data/department/QA
STR-006  focus=https://acme.example.org/data/employee/E004  path=http://xmlns.com/foaf/0.1/mbox  value=mailto:margaret.hamilton@acme.example.org
STR-006  focus=https://acme.example.org/data/employee/E005  path=http://xmlns.com/foaf/0.1/mbox  value=mailto:katherine.johnson@acme.example.org
STR-006  focus=https://acme.example.org/data/employee/E005  path=https://acme.example.org/ns/worksIn  value=https://acme.example.org/data/department/MKT
total 10: 10 Violation, 0 Warning, 0 Info
[exit 0]

$ python scripts/summarise_findings.py work/C10_20/own/full_results.csv --by focus --check CNF-005
CNF-005  focus=https://acme.example.org/ns/Contractor  path=-  value=-
CNF-005  focus=https://acme.example.org/ns/Department  path=-  value=-
total 2: 0 Violation, 0 Warning, 2 Info
[exit 0]
```

</details>

---

<a id="c10-21"></a>
### C10.21 — Half the defects are mailboxes

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-21) · [plain edition](../docs/10-ingest-and-transform.md#what-those-findings-actually-say)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Read the list to the end, though. Of the ten of each, five are the departments.

**Evidence:** the same as [C10.20 — Real defects: every worksIn target is untyped and dangling](#c10-20), which reproduces it: STR-006: 10, five departments and five mailboxes; DAT-002: 10, five departments and five mailboxes; CNF-005 on https://acme.example.org/ns/Contractor, https://acme.example.org/ns/Department; QUA-001 on https://acme.example.org/ns/hasSkill; STY-002 on https://acme.example.org/ns/reports_to; STR-003 on https://acme.example.org/ns/reports_to; REA-021's message reads as quoted

---

<a id="c10-22"></a>
### C10.22 — CNF-005: Contractor never populated

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-22) · [plain edition](../docs/10-ingest-and-transform.md#what-those-findings-actually-say)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Nothing is wrong. `acme:Contractor` is declared and this extract has no

**Evidence:** the same as [C10.20 — Real defects: every worksIn target is untyped and dangling](#c10-20), which reproduces it: STR-006: 10, five departments and five mailboxes; DAT-002: 10, five departments and five mailboxes; CNF-005 on https://acme.example.org/ns/Contractor, https://acme.example.org/ns/Department; QUA-001 on https://acme.example.org/ns/hasSkill; STY-002 on https://acme.example.org/ns/reports_to; STR-003 on https://acme.example.org/ns/reports_to; REA-021's message reads as quoted

---

<a id="c10-23"></a>
### C10.23 — REA-021 confirms LOG-001 by a different route

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-23) · [plain edition](../docs/10-ingest-and-transform.md#the-reasoner-when-it-turns-up)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> When HermiT starts, the scoped run carries one extra finding:

**Evidence:** the same as [C10.20 — Real defects: every worksIn target is untyped and dangling](#c10-20), which reproduces it: STR-006: 10, five departments and five mailboxes; DAT-002: 10, five departments and five mailboxes; CNF-005 on https://acme.example.org/ns/Contractor, https://acme.example.org/ns/Department; QUA-001 on https://acme.example.org/ns/hasSkill; STY-002 on https://acme.example.org/ns/reports_to; STR-003 on https://acme.example.org/ns/reports_to; REA-021's message reads as quoted

---

<a id="c10-24"></a>
### C10.24 — The suite's walkthrough called it environment-flaky

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-24) · [plain edition](../docs/10-ingest-and-transform.md#the-reasoner-when-it-turns-up)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> Whether it turns up is decided by Python's hash seed.

**Sources:**

- [suite docs/ACME_ROBOTICS_WALKTHROUGH.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/ACME_ROBOTICS_WALKTHROUGH.md#L73): “occasionally environment-flaky” (quote found, checked 2026-10-22)

The seed mechanism is reproduced in C14.06.

---

<a id="c10-25"></a>
### C10.25 — --sample caps the reasoning pass

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-25) · [plain edition](../docs/10-ingest-and-transform.md#large-graphs)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> For a data graph too large to reason over in full, `--sample N` caps the

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite data --help
```

**What is checked:** `data --help` documents --sample as a cap on the reasoning pass

**Recorded result:** PASS — step 1 output contains '--sample SAMPLE', 'cap the reasoning pass to a CBD sample of this many'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite data --help
usage: ontology-quality-suite data [-h] [--ontology ONTOLOGY]
                                   [--import-dir IMPORT_DIR]
                                   [--exclude-imports] [--allow-network]
                                   [--data-pattern DATA_PATTERN]
                                   [--registry REGISTRY] [--themes THEMES]
                                   [--sparql SPARQL] [--shapes SHAPES]
                                   [--sample SAMPLE]
                                   [--engine {both,sparql,shacl,native,native+sparql}]
                                   [--out-dir OUT_DIR]
                                   [--reports {all,minimal}]
                                   [--reasoner {auto,owlrl-only,hermit,pellet,none}]
                                   [--fail-on {Violation,Warning,Info,never}]
                                   [--own-namespace OWN_NAMESPACE] [-v]
                                   data [data ...]
positional arguments:
  data                  turtle file(s) and/or folder(s) of them
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --data-pattern DATA_PATTERN, --file-pattern DATA_PATTERN
                        comma-separated glob pattern(s) used to find data
                        files when a `data` argument is a folder (default:
                        *.ttl,*.turtle). Also accepted as --file-pattern, the
… (50 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

---

<a id="c10-26"></a>
### C10.26 — CT-32 to CT-38: when every file is right and the set is wrong

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-26) · [plain edition](../docs/10-ingest-and-transform.md#106-when-every-file-is-right-and-the-set-is-wrong)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The testing repository's competency questions 32 to 38 are about exactly this:

**Sources:**

- [testing repo commit 1370f6c](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/1370f6c5362501c91a584bb1f3fe022720ed4357) (exists, checked 2026-10-22)
- [testing repo drift.py (CT-34, 35, 36, 38)](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/experiments/SpecificTests/AGGREGATE-mapping-drift/drift.py#L1-L9): “CT-34, CT-35, CT-36, CT-38 -- drift across a *set* of mappings.” (quote found, checked 2026-10-22)

---

<a id="c10-27"></a>
### C10.27 — CT-32's mapping is wired to no CSV

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-27) · [plain edition](../docs/10-ingest-and-transform.md#106-when-every-file-is-right-and-the-set-is-wrong)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> CT-32 taught me something.

**Sources:**

- [testing repo CT-32 README](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/experiments/SpecificTests/CT-32-property-outside-its-domain/README.md): “This mapping is wired to no CSV, which settles the argument.” (quote found, checked 2026-10-22)

---

<a id="c10-28"></a>
### C10.28 — tq:PrefixBinding and the per-file sketch dataset

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-28) · [plain edition](../docs/10-ingest-and-transform.md#106-when-every-file-is-right-and-the-set-is-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The suite now publishes two facts that make set-level questions a query rather

**Inputs:** [`data/mapping-set/people.rq`](data/mapping-set/people.rq), [`data/mapping-set/payroll.rq`](data/mapping-set/payroll.rq), [`data/mapping-set/legacy.rq`](data/mapping-set/legacy.rq), [`data/queries/prefix-conflicts.rq`](data/queries/prefix-conflicts.rq)

<details><summary><code>data/mapping-set/people.rq</code></summary>

```sparql
# Chapter 10 §10.6: one of two mappings, each correct on its own. This one
# binds acme: to the ontology's namespace and builds employees with a skill.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasSkill ?skill .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/payroll.rq</code></summary>

```sparql
# Chapter 10 §10.6: a second mapping, written later by someone else, using
# the same namespace, building the same class with a different property.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasEmployeeId ?id .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/legacy.rq</code></summary>

```sparql
# Chapter 10 §10.6: a third, older mapping. Internally consistent, but it binds
# acme: to a hash namespace, so its terms are not the ontology's.
PREFIX acme: <https://acme.example.org/ns#>
CONSTRUCT {
  ?unit_IRI a acme:Department .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/department/", ?dept)) AS ?unit_IRI)
}
```

</details>

<details><summary><code>data/queries/prefix-conflicts.rq</code></summary>

```sparql
# One prefix bound to two namespaces by two files: a GROUP BY over the
# tq:PrefixBinding facts that `sketch` writes to bind-facts.ttl.
PREFIX tq: <https://semantechs.co.uk/ontology-quality/tarql/>
SELECT ?prefix (COUNT(DISTINCT ?ns) AS ?namespaces) (GROUP_CONCAT(DISTINCT ?file; separator=", ") AS ?files)
WHERE { ?b a tq:PrefixBinding ; tq:prefix ?prefix ; tq:namespace ?ns ; tq:source ?file }
GROUP BY ?prefix
HAVING (COUNT(DISTINCT ?ns) > 1)
```

</details>

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --queries data/mapping-set --out-dir work/C10_28/ms --reports minimal --fail-on never
python scripts/query_file.py work/C10_28/ms/bind-facts.ttl @data/queries/prefix-conflicts.rq
python scripts/sketch_dataset.py data/mapping-set
```

<details><summary><code>scripts/sketch_dataset.py</code></summary>

```python
"""Chapter 10 §10.6: ask a per-file question of a set of mappings.

    python scripts/sketch_dataset.py data/mapping-set

Builds the suite's per-file sketch dataset (each query file's CONSTRUCT
template in a named graph named after the file; the union in the default
graph) and asks, for each class, which properties each file builds it with.
One class built with different properties by different files is invisible in
the merged sketch, where the two descriptions simply add up.
"""
import sys

from ontology_suite.sketch.prefix_alignment import build_sketch_dataset

sys.stdout.reconfigure(encoding="utf-8")

ds = build_sketch_dataset([sys.argv[1]])
q = """
SELECT ?file ?class ?property WHERE {
  GRAPH ?g { ?s a ?class ; ?property ?o . FILTER(?property != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) }
  BIND(REPLACE(STR(?g), "^.*/", "") AS ?file)
} ORDER BY ?class ?file ?property
"""
for row in ds.query(q):
    print(f"{row.file:14} {row['class']}  {row.property}")
print(f"named graphs: {sorted(str(g.identifier).rsplit('/', 1)[-1] for g in ds.graphs() if str(g.identifier).endswith('.rq'))}")
```

</details>

**What is checked:** a GROUP BY over the tq:PrefixBinding facts finds acme: bound to two namespaces across the three files; the per-file dataset shows acme:Employee built with hasEmployeeId by one file and hasSkill by another

**Recorded result:** PASS — step 2 output contains 'acme,2,legacy.rq, payroll.rq, people.rq'; step 3 output contains 'payroll.rq     https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasEmployeeId', 'people.rq      https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasSkill'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --queries data/mapping-set --out-dir work/C10_28/ms --reports minimal --fail-on never
Findings: 1 total (0 Violation, 0 Warning, 1 Info)
Reports written to: ./work/C10_28/ms
  - work/C10_28/ms/findings.txt (start here -- what, where, and the source line)
  - work/C10_28/ms/full_results.csv
Sketch used 3 query file(s); 4 triples, 4 entities.
warning: prefix 'acme:' means <https://acme.example.org/ns#> in an earlier file and <https://acme.example.org/ns/> in payroll.rq; each file is read with its own definition, and the legend below shows the first
warning: prefix 'acme:' means <https://acme.example.org/ns#> in an earlier file and <https://acme.example.org/ns/> in people.rq; each file is read with its own definition, and the legend below shows the first
[exit 0]

$ python scripts/query_file.py work/C10_28/ms/bind-facts.ttl @data/queries/prefix-conflicts.rq
prefix,namespaces,files
acme,2,legacy.rq, payroll.rq, people.rq
[exit 0]

$ python scripts/sketch_dataset.py data/mapping-set
payroll.rq     https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasEmployeeId
people.rq      https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasSkill
named graphs: ['legacy.rq', 'payroll.rq', 'people.rq']
[exit 0]
```

</details>

---

<a id="c10-29"></a>
### C10.29 — The merged sketch and one prefix bound two ways: odd file first

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-29) · [plain edition](../docs/10-ingest-and-transform.md#106-when-every-file-is-right-and-the-set-is-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **And one thing the merged sketch got wrong, until 0.23.0.**

**Inputs:** [`data/mapping-set/people.rq`](data/mapping-set/people.rq), [`data/mapping-set/payroll.rq`](data/mapping-set/payroll.rq), [`data/mapping-set/legacy.rq`](data/mapping-set/legacy.rq)

<details><summary><code>data/mapping-set/people.rq</code></summary>

```sparql
# Chapter 10 §10.6: one of two mappings, each correct on its own. This one
# binds acme: to the ontology's namespace and builds employees with a skill.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasSkill ?skill .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/payroll.rq</code></summary>

```sparql
# Chapter 10 §10.6: a second mapping, written later by someone else, using
# the same namespace, building the same class with a different property.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasEmployeeId ?id .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/legacy.rq</code></summary>

```sparql
# Chapter 10 §10.6: a third, older mapping. Internally consistent, but it binds
# acme: to a hash namespace, so its terms are not the ontology's.
PREFIX acme: <https://acme.example.org/ns#>
CONSTRUCT {
  ?unit_IRI a acme:Department .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/department/", ?dept)) AS ?unit_IRI)
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite sketch --queries data/mapping-set --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_29/three --reports minimal --fail-on never
python scripts/summarise_findings.py work/C10_29/three/full_results.csv --by focus --check CNF-001
python scripts/summarise_findings.py work/C10_29/three/full_results.csv --by focus --check CNF-002
ontology-quality-suite sketch --queries data/mapping-set --query-pattern people.rq,payroll.rq --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_29/two --reports minimal --fail-on never
```

**What is checked:** with legacy.rq sorting first. At 0.22.0 the merged sketch reports acme:Employee, hasSkill and hasEmployeeId as undeclared in the hash namespace and acme:Employee as never populated. From 0.23.0 it reports only legacy.rq's own acme:Department, in the hash namespace where it was written, and acme:Employee is populated. The two correct files on their own are clean on both

**Recorded result:** PASS — suite 0.24.3: the warning says each file is read with its own definition; step 2 output contains 'focus=https://acme.example.org/ns#Department'; step 2 output has none of 'ns#Employee'; step 3 output has none of 'ns#hasSkill', 'ns#hasEmployeeId'; three/full_results.csv: CNF-005 excludes https://acme.example.org/ns/Employee; two/full_results.csv: {'CNF-005': 36, 'TQL-003': 1}; two/full_results.csv: CNF-005 excludes https://acme.example.org/ns/Employee

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite sketch --queries data/mapping-set --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_29/three --reports minimal --fail-on never
Findings: 38 total (0 Violation, 1 Warning, 37 Info)
Reports written to: ./work/C10_29/three
  - work/C10_29/three/findings.txt (start here -- what, where, and the source line)
  - work/C10_29/three/full_results.csv
Sketch used 3 query file(s); 4 triples, 4 entities.
warning: prefix 'acme:' means <https://acme.example.org/ns#> in an earlier file and <https://acme.example.org/ns/> in payroll.rq; each file is read with its own definition, and the legend below shows the first
warning: prefix 'acme:' means <https://acme.example.org/ns#> in an earlier file and <https://acme.example.org/ns/> in people.rq; each file is read with its own definition, and the legend below shows the first
[exit 0]

$ python scripts/summarise_findings.py work/C10_29/three/full_results.csv --by focus --check CNF-001
CNF-001  focus=https://acme.example.org/ns#Department  path=-  value=-
total 1: 0 Violation, 1 Warning, 0 Info
[exit 0]

$ python scripts/summarise_findings.py work/C10_29/three/full_results.csv --by focus --check CNF-002
total 0: 0 Violation, 0 Warning, 0 Info
[exit 0]

$ ontology-quality-suite sketch --queries data/mapping-set --query-pattern people.rq,payroll.rq --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_29/two --reports minimal --fail-on never
Findings: 37 total (0 Violation, 0 Warning, 37 Info)
Reports written to: ./work/C10_29/two
  - work/C10_29/two/findings.txt (start here -- what, where, and the source line)
  - work/C10_29/two/full_results.csv
Sketch used 2 query file(s); 3 triples, 3 entities.
[exit 0]
```

</details>

---

<a id="c10-30"></a>
### C10.30 — The merged sketch and one prefix bound two ways: odd file last

**In the manual:** [Chapter 10, at the claim](manual/docs/10-ingest-and-transform.md#ev-c10-30) · [plain edition](../docs/10-ingest-and-transform.md#106-when-every-file-is-right-and-the-set-is-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> It cuts the other way too, which is worse.

**Inputs:** [`data/mapping-set/people.rq`](data/mapping-set/people.rq), [`data/mapping-set/payroll.rq`](data/mapping-set/payroll.rq), [`data/mapping-set/legacy.rq`](data/mapping-set/legacy.rq)

<details><summary><code>data/mapping-set/people.rq</code></summary>

```sparql
# Chapter 10 §10.6: one of two mappings, each correct on its own. This one
# binds acme: to the ontology's namespace and builds employees with a skill.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasSkill ?skill .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/payroll.rq</code></summary>

```sparql
# Chapter 10 §10.6: a second mapping, written later by someone else, using
# the same namespace, building the same class with a different property.
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT {
  ?employee_IRI a acme:Employee ;
    acme:hasEmployeeId ?id .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee_IRI)
}
```

</details>

<details><summary><code>data/mapping-set/legacy.rq</code></summary>

```sparql
# Chapter 10 §10.6: a third, older mapping. Internally consistent, but it binds
# acme: to a hash namespace, so its terms are not the ontology's.
PREFIX acme: <https://acme.example.org/ns#>
CONSTRUCT {
  ?unit_IRI a acme:Department .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/department/", ?dept)) AS ?unit_IRI)
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/copy_tree.py data/mapping-set/people.rq work/C10_30/last/people.rq
python scripts/copy_tree.py data/mapping-set/payroll.rq work/C10_30/last/payroll.rq
# the same older mapping, renamed so that it sorts last
python scripts/copy_tree.py data/mapping-set/legacy.rq work/C10_30/last/zz-legacy.rq
ontology-quality-suite sketch --queries work/C10_30/last --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_30/out --reports minimal --fail-on never
python scripts/summarise_findings.py work/C10_30/out/full_results.csv --by focus --check CNF-001
```

**What is checked:** with the hash-namespace file sorting last. At 0.22.0 the run reports no CNF-001 or CNF-002 at all: its acme:Department is read in the ontology's own namespace, and a warning on stderr is the only trace. From 0.23.0 its acme:Department is reported in the hash namespace, in this order as in the other, because the sketch re-declares each file's prefixes ahead of its triples

**Recorded result:** PASS — the warning names zz-legacy.rq, on stderr; suite 0.24.3: out/full_results.csv: CNF-001 includes https://acme.example.org/ns#Department; sketch.ttl re-declares acme: ahead of zz-legacy.rq's triples

<details><summary>Output, as recorded</summary>

```text
$ python scripts/copy_tree.py data/mapping-set/people.rq work/C10_30/last/people.rq
copied data/mapping-set/people.rq -> work/C10_30/last/people.rq
[exit 0]

$ python scripts/copy_tree.py data/mapping-set/payroll.rq work/C10_30/last/payroll.rq
copied data/mapping-set/payroll.rq -> work/C10_30/last/payroll.rq
[exit 0]

$ python scripts/copy_tree.py data/mapping-set/legacy.rq work/C10_30/last/zz-legacy.rq
copied data/mapping-set/legacy.rq -> work/C10_30/last/zz-legacy.rq
[exit 0]

$ ontology-quality-suite sketch --queries work/C10_30/last --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C10_30/out --reports minimal --fail-on never
Findings: 38 total (0 Violation, 1 Warning, 37 Info)
Reports written to: ./work/C10_30/out
  - work/C10_30/out/findings.txt (start here -- what, where, and the source line)
  - work/C10_30/out/full_results.csv
Sketch used 3 query file(s); 4 triples, 4 entities.
warning: prefix 'acme:' means <https://acme.example.org/ns/> in an earlier file and <https://acme.example.org/ns#> in zz-legacy.rq; each file is read with its own definition, and the legend below shows the first
[exit 0]

$ python scripts/summarise_findings.py work/C10_30/out/full_results.csv --by focus --check CNF-001
CNF-001  focus=https://acme.example.org/ns#Department  path=-  value=-
total 1: 0 Violation, 1 Warning, 0 Info
[exit 0]
```

</details>

---

<a id="chapter-11"></a>
## 11. Rules and inference

Annotated chapter: [manual/docs/11-rules-and-inference.md](manual/docs/11-rules-and-inference.md) · plain chapter: [../docs/11-rules-and-inference.md](../docs/11-rules-and-inference.md)

<a id="c11-01"></a>
### C11.01 — The suite and the extension do not run SHACL-AF rules

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-01) · [plain edition](../docs/11-rules-and-inference.md#111-the-engine-that-runs-the-rules)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The Ontology Quality Suite does not run SHACL-AF rules (there is no `--advanced`

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --help
ontology-quality-suite data --help
ontology-quality-suite ontology --help
ontology-quality-suite run --help
```

**What is checked:** none of checks, data, ontology or run offers --advanced

**Recorded result:** PASS — step 1 output has none of '--advanced'; step 2 output has none of '--advanced'; step 3 output has none of '--advanced'; step 4 output has none of '--advanced'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --help
usage: ontology-quality-suite checks [-h] [--ontology ONTOLOGY] [--data DATA]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--shapes SHAPES] [--sparql SPARQL]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--inference {none,rdfs}]
                                     [--engine {both,sparql,shacl,native,native+sparql}]
                                     [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [--own-namespace OWN_NAMESPACE] [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --data DATA
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --shapes SHAPES
  --sparql SPARQL       a directory of .rq check queries, or @builtin for the
                        suite's own tree wherever this install put it.
                        Repeatable: pass it more than once to run a project's
                        own checks alongside the suite's, which is what you
                        almost always want. Given at all, it replaces the
                        built-in tree, so `--sparql mine` runs only yours --
                        the run warns when that happens. See
… (48 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]

$ ontology-quality-suite data --help
usage: ontology-quality-suite data [-h] [--ontology ONTOLOGY]
                                   [--import-dir IMPORT_DIR]
                                   [--exclude-imports] [--allow-network]
                                   [--data-pattern DATA_PATTERN]
                                   [--registry REGISTRY] [--themes THEMES]
                                   [--sparql SPARQL] [--shapes SHAPES]
                                   [--sample SAMPLE]
                                   [--engine {both,sparql,shacl,native,native+sparql}]
                                   [--out-dir OUT_DIR]
                                   [--reports {all,minimal}]
                                   [--reasoner {auto,owlrl-only,hermit,pellet,none}]
                                   [--fail-on {Violation,Warning,Info,never}]
                                   [--own-namespace OWN_NAMESPACE] [-v]
                                   data [data ...]
positional arguments:
  data                  turtle file(s) and/or folder(s) of them
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --data-pattern DATA_PATTERN, --file-pattern DATA_PATTERN
                        comma-separated glob pattern(s) used to find data
                        files when a `data` argument is a folder (default:
                        *.ttl,*.turtle). Also accepted as --file-pattern, the
… (50 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]

$ ontology-quality-suite ontology --help
usage: ontology-quality-suite ontology [-h] --ontology ONTOLOGY
                                       [--import-dir IMPORT_DIR]
                                       [--exclude-imports] [--allow-network]
                                       [--registry REGISTRY] [--themes THEMES]
                                       [--sparql SPARQL] [--out-dir OUT_DIR]
                                       [--reports {all,minimal}]
                                       [--profile {EL,QL,RL}]
                                       [--reasoner {auto,owlrl-only,hermit,pellet,none}]
                                       [--fail-on {Violation,Warning,Info,never}]
                                       [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --registry REGISTRY
  --themes THEMES       a JSON or CSV map of check id to a question in your
                        own words, used to add a "by question" index to
                        findings.txt -- see docs/REPORTS.md
  --sparql SPARQL       a directory of .rq check queries, or @builtin for the
                        suite's own tree wherever this install put it.
                        Repeatable: pass it more than once to run a project's
                        own checks alongside the suite's, which is what you
                        almost always want. Given at all, it replaces the
                        built-in tree, so `--sparql mine` runs only yours --
… (18 lines omitted; full output in the outputs/ record)
                        reasoning backend: auto (owlrl + external if
                        available), owlrl-only, hermit, pellet, or none
  --fail-on {Violation,Warning,Info,never}
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]

$ ontology-quality-suite run --help
usage: ontology-quality-suite run [-h] [--ontology ONTOLOGY]
                                  [--import-dir IMPORT_DIR]
                                  [--exclude-imports] [--allow-network]
                                  [--docgen] [--instances INSTANCES]
                                  [--ref REF] [--doc-prefix DOC_PREFIX]
                                  [--doc-template DOC_TEMPLATE]
                                  [--no-class-diagrams] [--diagram-imports]
                                  [--queries QUERIES]
                                  [--query-pattern QUERY_PATTERN]
                                  [--csv-dir CSV_DIR] [--data [DATA ...]]
                                  [--data-pattern DATA_PATTERN]
                                  [--registry REGISTRY] [--themes THEMES]
                                  [--shapes SHAPES] [--sparql SPARQL]
                                  [--oxi-gen-bin OXI_GEN_BIN]
                                  [--sample SAMPLE]
                                  [--engine {both,sparql,shacl,native,native+sparql}]
                                  [--out-dir OUT_DIR]
                                  [--reports {all,minimal}]
                                  [--profile {EL,QL,RL}]
                                  [--reasoner {auto,owlrl-only,hermit,pellet,none}]
                                  [--fail-on {Violation,Warning,Info,never}]
                                  [--own-namespace OWN_NAMESPACE] [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
… (84 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

---

<a id="c11-02"></a>
### C11.02 — The Python surface: inference modes, and an unknown one is an error

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-02) · [plain edition](../docs/11-rules-and-inference.md#111-the-engine-that-runs-the-rules)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> From Python, rules are reached through the `inference` argument rather than a

**Inputs:** [`data/rules/triple.ttl`](data/rules/triple.ttl), [`data/rules/people.ttl`](data/rules/people.ttl)

<details><summary><code>data/rules/triple.ttl</code></summary>

```turtle
# Two triple rules on Person, and a shape that only exists to see what they made.
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:  <http://example.org/> .

ex:PersonShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate rdf:type ; sh:object ex:Agent ] ;
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate ex:contact ;
        sh:object [ sh:path ex:knows ] ] .

ex:AgentShape a sh:NodeShape ;
    sh:targetClass ex:Agent ;
    sh:property [ sh:path ex:contact ; sh:minCount 1 ;
                  sh:message "Agent has no contact" ] .
```

</details>

<details><summary><code>data/rules/people.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:alice a ex:Person ; ex:knows ex:bob, ex:carol .
ex:dave  a ex:Person .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/shacl_python.py data/shacl data/rules
```

<details><summary><code>scripts/shacl_python.py</code></summary>

```python
"""Chapter 11: the shacl package's Python surface.

    python scripts/shacl_python.py data/shacl data/rules

Prints, for the fixtures in those folders:
  - the one-shot validate() on data and shapes, and with the arguments swapped
  - the one-shot against a shapes graph that declares no shapes (refused)
  - the explicit Shapes API against the same (permissive by design)
  - a warnings-only graph, with and without allow_warnings
  - each inference mode, including one that does not exist
"""
import sys
from pathlib import Path

import shacl

sys.stdout.reconfigure(encoding="utf-8")
S, R = Path(sys.argv[1]), Path(sys.argv[2])
data = str(S / "data.ttl")


def one_shot(label, *args, **kw):
    try:
        rep = shacl.validate(*args, **kw)
        print(f"{label:44} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"{label:44} REFUSED: {type(exc).__name__}: {exc}")


print("shacl", shacl.__version__ if hasattr(shacl, "__version__") else "")
one_shot("validate(data, shapes)", data, str(S / "shapes-violation.ttl"))
one_shot("validate(shapes, data)  [swapped]", str(S / "shapes-violation.ttl"), data)
one_shot("validate(data, no-shapes)", data, str(S / "no-shapes.ttl"))
rep = shacl.Shapes.from_file(str(S / "no-shapes.ttl")).validate_file(data)
print(f"{'Shapes.from_file(no-shapes).validate_file':44} conforms={rep.conforms} results={len(rep.results)}")
one_shot("warnings only", data, str(S / "shapes-warning.ttl"))
one_shot("warnings only, allow_warnings=True", data, str(S / "shapes-warning.ttl"), allow_warnings=True)
one_shot("severity on the node shape (the trap)", data, str(S / "shapes-warning-on-node.ttl"),
         allow_warnings=True)

shapes = shacl.Shapes.from_file(str(R / "triple.ttl"))
for mode in ("none", "rdfs", "rules", "rules-iterated", "bogus"):
    try:
        rep = shapes.validate_file(str(R / "people.ttl"), inference=mode)
        print(f"inference={mode:16} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"inference={mode:16} ERROR: {exc}")
```

</details>

**What is checked:** rules and rules-iterated fire (one result, from the rule's output); none does not; an unknown mode is an error naming the accepted ones

**Recorded result:** PASS — step 1 output contains 'inference=none             conforms=True results=0', 'inference=rules            conforms=False results=1', 'inference=rules-iterated   conforms=False results=1', 'inference=bogus            ERROR: unknown inference "bogus"'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/shacl_python.py data/shacl data/rules
shacl 0.3.4
validate(data, shapes)                       conforms=False results=1
validate(shapes, data)  [swapped]            REFUSED: ValueError: the shapes graph declares no shapes, so this would report that the data conforms without having checked anything. Note the argument order is validate(data, shapes). To validate against an empty shapes graph deliberately, use Shapes.from_file and check len() yourself.
validate(data, no-shapes)                    REFUSED: ValueError: the shapes graph declares no shapes, so this would report that the data conforms without having checked anything. Note the argument order is validate(data, shapes). To validate against an empty shapes graph deliberately, use Shapes.from_file and check len() yourself.
Shapes.from_file(no-shapes).validate_file    conforms=True results=0
warnings only                                conforms=False results=1
warnings only, allow_warnings=True           conforms=True results=1
severity on the node shape (the trap)        conforms=False results=1
inference=none             conforms=True results=0
inference=rdfs             conforms=True results=0
inference=rules            conforms=False results=1
inference=rules-iterated   conforms=False results=1
inference=bogus            ERROR: unknown inference "bogus"; use "none", "rdfs", "rules" or "rules-iterated"
[exit 0]
```

</details>

---

<a id="c11-03"></a>
### C11.03 — Rules shipped in 0.1.8; the $this fix came with them

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-03) · [plain edition](../docs/11-rules-and-inference.md#111-the-engine-that-runs-the-rules)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> > **Check your version before believing any of this.**

**Sources:**

- [engine commit 8de05ba, 'Implement SHACL-AF rules' (after the v0.1.7 tag, version string still 0.1.7)](https://github.com/pwin/SHACL_Engine/commit/8de05bae23e410d97c040743f4ca7e0eb4ff6947): “`$this` was never substituted into a `CONSTRUCT` query.” (quote found, checked 2026-10-22)
- [engine commit 637ebf5, rules in both bindings (before v0.1.8)](https://github.com/pwin/SHACL_Engine/commit/637ebf5b0dc9715bc1af4102cb7cd964c92374f2): “Rules reach the WASM and Python bindings as inference modes” (quote found, checked 2026-10-22)
- [engine commit 2134124, v0.1.9](https://github.com/pwin/SHACL_Engine/commit/2134124fb3268ec4700f39ba66ad576e31fff004): “this version exists so all three channels carry the same number rather than leaving npm a release behind” (quote found, checked 2026-10-22)

`git tag --contains 8de05ba` begins at v0.1.8. The v0.1.7 tree has no `-a`/`--advanced` flag in the CLI; the commit that adds it still declares version 0.1.7 in Cargo.toml.

---

<a id="c11-04"></a>
### C11.04 — Warnings break conformance; --allow-warnings records the choice

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-04) · [plain edition](../docs/11-rules-and-inference.md#what-030-changed-what-conforms-means)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified on 0.3.4, with a shape whose only result is a Warning:

**Inputs:** [`data/shacl/data.ttl`](data/shacl/data.ttl), [`data/shacl/shapes-warning.ttl`](data/shacl/shapes-warning.ttl)

<details><summary><code>data/shacl/data.ttl</code></summary>

```turtle
# Chapter 11: two people, one of them with no name.
@prefix ex: <http://example.org/> .

ex:alice a ex:Person ; ex:name "Alice" .
ex:bob   a ex:Person .
```

</details>

<details><summary><code>data/shacl/shapes-warning.ttl</code></summary>

```turtle
# The same constraint, declared a Warning on the property shape that produces
# the result. Since engine 0.3.0 a Warning still breaks conformance.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:PersonShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:property [ sh:path ex:name ; sh:minCount 1 ; sh:severity sh:Warning ] .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl
shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl --allow-warnings -f turtle
shacl --help
```

**What is checked:** warnings only: conforms false, exit 1; with --allow-warnings: conforms true, exit 0, and the report records sh:conformanceDisallows sh:Violation; --help offers --allow-infos and --min-severity

**Recorded result:** PASS — step 1: conforms: false; step 1 exits 1; step 2 exits 0; step 2 output contains 'sh:conforms true', 'sh:conformanceDisallows sh:Violation'; step 3 output contains '--allow-warnings', '--allow-infos', '--min-severity'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl
conforms: false
  MinCountConstraintComponent | focus <http://example.org/bob> | value - | path <http://example.org/name>
[exit 1]

$ shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl --allow-warnings -f turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
_:r0 a sh:ValidationReport ;
	sh:conformanceDisallows sh:Violation ;
	sh:conforms true ;
	sh:result _:r1 .
_:r1 a sh:ValidationResult ;
	sh:focusNode <http://example.org/bob> ;
	sh:resultPath <http://example.org/name> ;
	sh:resultSeverity sh:Warning ;
	sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
	sh:sourceShape _:1_b0 .
[exit 0]

$ shacl --help
A high-performance SHACL validator
Usage: shacl.exe [OPTIONS] --data <DATA>...
Options:
  -d, --data <DATA>...
          The data graph to validate. A path, an `http(s)` URL, or `-` for standard input.
          Repeat it to merge several documents into one graph. Blank nodes stay separate per document, as they must: `_:a` in two files is two nodes.
  -s, --shapes <SHAPES>...
          The shapes graph, on the same terms as `--data` and likewise repeatable. Defaults to the data graph, matching the convention that a self-describing document carries its own shapes.
          Only one input in total may be `-`, since standard input can be read only once.
      --data-format <DATA_FORMAT>
          The data graph's RDF syntax. Guessed from the file extension, or over HTTP from the `Content-Type`, when omitted; required when `--data` is `-`, which has neither
          [alias: --df]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --shapes-format <SHAPES_FORMAT>
          The shapes graph's RDF syntax, on the same terms as `--data-format`
          [alias: --sf]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --build-index
          Cache the parsed data graph beside it as `<file>.shix`, so later runs skip parsing.
          Parsing is around three quarters of a run over a large graph, and a data graph that has not changed is parsed identically every time. The cache is checked against the source on every use, so a stale one is never read — see `--no-index`.
          Only for a single local `--data` file: a URL has nowhere to write, and merged documents have no one source to check against.
      --no-index
          Ignore any `<file>.shix` cache and parse the data graph
      --allow-no-shapes
          Validate against a shapes graph that declares no shapes, instead of refusing to.
          Validating against no shapes conforms, because there is nothing to violate. Without this flag that is an error rather than a pass: the usual cause is a forgotten `--shapes`, and reporting success for a graph nothing was checked against is the worst answer a validator can give. Pass it when an empty shapes graph is what you meant.
      --threads <N>
          Worker threads for validation. `0` uses every core; `1` runs sequentially.
          Only a SHACL Core shapes graph splits across threads. One using `sh:sparql`, a SPARQL-based constraint component or node expressions runs sequentially whatever this says, as does any run with `--max-results`. The report is the same either way, byte for byte.
          [default: 0]
… (55 lines omitted; full output in the outputs/ record)
          Report how long loading, compiling and validating each took
      --repeat <REPEAT>
          Validate `n` times, reporting the best wall time. For benchmarking
          [default: 1]
  -h, --help
          Print help (see a summary with '-h')
  -V, --version
          Print version
[exit 0]
```

</details>

**Sources:**

- [engine commit 2006c4e (0.3.0)](https://github.com/pwin/SHACL_Engine/commit/2006c4e5766f8145d025a118c0d96ec3c2bfcb74): “The harness had recomputed the expected report's conformance under the engine's own rule instead of reading the value the test wrote, so it agreed with itself.” (quote found, checked 2026-10-22)

---

<a id="c11-05"></a>
### C11.05 — The WebAssembly build agrees since 0.3.2

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-05) · [plain edition](../docs/11-rules-and-inference.md#what-030-changed-what-conforms-means)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The surfaces disagreed for two releases.**

**Commands** (from the `evidence/` folder):

```bash
node scripts/wasm_conforms.mjs data/shacl
```

<details><summary><code>scripts/wasm_conforms.mjs</code></summary>

```javascript
// Chapter 11 §11.1: what "conforms" means in the WebAssembly build.
//
//   node scripts/wasm_conforms.mjs data/shacl
//
// shacl-wasm-node 0.3.0 and 0.3.1 kept the old rule (only sh:Violation breaks
// conformance) after the CLI and Python bindings had moved to the specification's.
// 0.3.2 caught up. This validates a warnings-only graph through the package and
// prints the verdict.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const { Validator } = require('shacl-wasm-node');
const pkg = require('shacl-wasm-node/package.json');

const dir = process.argv[2];
const data = readFileSync(join(dir, 'data.ttl'), 'utf8');
for (const file of ['shapes-warning.ttl', 'shapes-violation.ttl']) {
  const v = Validator.fromTurtle(readFileSync(join(dir, file), 'utf8'));
  const report = v.validateTurtle(data, null, 'none');
  const severities = report.results.map((r) => String(r.severity ?? r.resultSeverity ?? '?'));
  console.log(`shacl-wasm-node ${pkg.version}  ${file.padEnd(22)} conforms=${report.conforms}  results=${report.results.length}  severities=${severities.join(',')}`);
}

// §11.7: rules through the same build, and a mode that does not exist.
const rules = Validator.fromTurtle(readFileSync(join(dir, '..', 'rules', 'triple.ttl'), 'utf8'));
const people = readFileSync(join(dir, '..', 'rules', 'people.ttl'), 'utf8');
for (const mode of ['none', 'rules', 'bogus']) {
  try {
    const r = rules.validateTurtle(people, null, mode);
    console.log(`inference=${mode.padEnd(6)} conforms=${r.conforms}  results=${r.results.length}`);
  } catch (e) {
    console.log(`inference=${mode.padEnd(6)} ERROR: ${e.message ?? e}`);
  }
}
```

</details>

**What is checked:** shacl-wasm-node 0.3.4 calls a warnings-only graph non-conforming (0.3.0 and 0.3.1 did not)

**Recorded result:** PASS — step 1 output contains 'shacl-wasm-node 0.3.4  shapes-warning.ttl     conforms=false'

<details><summary>Output, as recorded</summary>

```text
$ node scripts/wasm_conforms.mjs data/shacl
shacl-wasm-node 0.3.4  shapes-warning.ttl     conforms=false  results=1  severities=http://www.w3.org/ns/shacl#Warning
shacl-wasm-node 0.3.4  shapes-violation.ttl   conforms=false  results=1  severities=http://www.w3.org/ns/shacl#Violation
inference=none   conforms=true  results=0
inference=rules  conforms=false  results=1
inference=bogus  ERROR: unknown inference "bogus": expected "none", "rdfs", "rules" or "rules-iterated"
[exit 0]
```

</details>

**Sources:**

- [engine commit 2eea15d](https://github.com/pwin/SHACL_Engine/commit/2eea15d58b6a9bf277c13a9dfbef93d47f1d5aa3) (exists, checked 2026-10-22)

---

<a id="c11-06"></a>
### C11.06 — The one-shots refuse an empty shapes graph

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-06) · [plain edition](../docs/11-rules-and-inference.md#what-020-changed-and-the-one-surface-it-did-not-reach)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> So the one-shots now refuse a shapes graph that declares nothing.

**Commands** (from the `evidence/` folder):

```bash
python scripts/shacl_python.py data/shacl data/rules
```

<details><summary><code>scripts/shacl_python.py</code></summary>

```python
"""Chapter 11: the shacl package's Python surface.

    python scripts/shacl_python.py data/shacl data/rules

Prints, for the fixtures in those folders:
  - the one-shot validate() on data and shapes, and with the arguments swapped
  - the one-shot against a shapes graph that declares no shapes (refused)
  - the explicit Shapes API against the same (permissive by design)
  - a warnings-only graph, with and without allow_warnings
  - each inference mode, including one that does not exist
"""
import sys
from pathlib import Path

import shacl

sys.stdout.reconfigure(encoding="utf-8")
S, R = Path(sys.argv[1]), Path(sys.argv[2])
data = str(S / "data.ttl")


def one_shot(label, *args, **kw):
    try:
        rep = shacl.validate(*args, **kw)
        print(f"{label:44} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"{label:44} REFUSED: {type(exc).__name__}: {exc}")


print("shacl", shacl.__version__ if hasattr(shacl, "__version__") else "")
one_shot("validate(data, shapes)", data, str(S / "shapes-violation.ttl"))
one_shot("validate(shapes, data)  [swapped]", str(S / "shapes-violation.ttl"), data)
one_shot("validate(data, no-shapes)", data, str(S / "no-shapes.ttl"))
rep = shacl.Shapes.from_file(str(S / "no-shapes.ttl")).validate_file(data)
print(f"{'Shapes.from_file(no-shapes).validate_file':44} conforms={rep.conforms} results={len(rep.results)}")
one_shot("warnings only", data, str(S / "shapes-warning.ttl"))
one_shot("warnings only, allow_warnings=True", data, str(S / "shapes-warning.ttl"), allow_warnings=True)
one_shot("severity on the node shape (the trap)", data, str(S / "shapes-warning-on-node.ttl"),
         allow_warnings=True)

shapes = shacl.Shapes.from_file(str(R / "triple.ttl"))
for mode in ("none", "rdfs", "rules", "rules-iterated", "bogus"):
    try:
        rep = shapes.validate_file(str(R / "people.ttl"), inference=mode)
        print(f"inference={mode:16} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"inference={mode:16} ERROR: {exc}")
```

</details>

**What is checked:** validate(data, shapes) finds one result; the swapped call is refused with the quoted message

**Recorded result:** PASS — step 1 output contains 'validate(data, shapes)                       conforms=False results=1', 'validate(shapes, data)  [swapped]            REFUSED: ValueError: the shapes graph declares no shapes, so this would report that the data conforms without having checked anything'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/shacl_python.py data/shacl data/rules
shacl 0.3.4
validate(data, shapes)                       conforms=False results=1
validate(shapes, data)  [swapped]            REFUSED: ValueError: the shapes graph declares no shapes, so this would report that the data conforms without having checked anything. Note the argument order is validate(data, shapes). To validate against an empty shapes graph deliberately, use Shapes.from_file and check len() yourself.
validate(data, no-shapes)                    REFUSED: ValueError: the shapes graph declares no shapes, so this would report that the data conforms without having checked anything. Note the argument order is validate(data, shapes). To validate against an empty shapes graph deliberately, use Shapes.from_file and check len() yourself.
Shapes.from_file(no-shapes).validate_file    conforms=True results=0
warnings only                                conforms=False results=1
warnings only, allow_warnings=True           conforms=True results=1
severity on the node shape (the trap)        conforms=False results=1
inference=none             conforms=True results=0
inference=rdfs             conforms=True results=0
inference=rules            conforms=False results=1
inference=rules-iterated   conforms=False results=1
inference=bogus            ERROR: unknown inference "bogus"; use "none", "rdfs", "rules" or "rules-iterated"
[exit 0]
```

</details>

**Sources:**

- [engine commit a567c2e (0.2.0)](https://github.com/pwin/SHACL_Engine/commit/a567c2edfb93e8053058c8976eef8fd95388a292): “validating against no shapes conforms” (quote found, checked 2026-10-22)

---

<a id="c11-07"></a>
### C11.07 — The CLI and an empty shapes graph: conforms up to 0.3.3, refused from 0.3.4

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-07) · [plain edition](../docs/11-rules-and-inference.md#what-020-changed-and-the-one-surface-it-did-not-reach)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Until 0.3.4 the command line did not refuse.**

**Inputs:** [`data/shacl/no-shapes.ttl`](data/shacl/no-shapes.ttl)

<details><summary><code>data/shacl/no-shapes.ttl</code></summary>

```turtle
# A "shapes graph" that declares no shapes at all.
@prefix ex: <http://example.org/> .
ex:x ex:y ex:z .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/shacl/data.ttl -s data/shacl/no-shapes.ttl
shacl -d data/shacl/data.ttl
shacl -d data/shacl/data.ttl -s data/shacl/no-shapes.ttl --allow-no-shapes
shacl --version
```

**What is checked:** up to 0.3.3: both runs say conforms true and exit 0. From 0.3.4: both exit 2, one saying the shapes graph declares no shapes and the other that no --shapes was given, and --allow-no-shapes restores the old answer

**Recorded result:** PASS — shacl 0.3.4: step 1 exits 2; step 1 output contains 'the shapes graph declares no shapes'; step 2 exits 2; step 2 output contains 'no --shapes was given'; step 3: conforms: true; step 3 exits 0

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/shacl/data.ttl -s data/shacl/no-shapes.ttl
error: the shapes graph declares no shapes, so nothing would be checked and the report would say the data conforms. Check that data/shacl/no-shapes.ttl is the file you meant and that the engine recognises what it declares, or pass --allow-no-shapes.
[exit 2]

$ shacl -d data/shacl/data.ttl
error: no --shapes was given, so data/shacl/data.ttl was used as its own shapes graph, and it declares no shapes. Nothing would be checked and the report would say the data conforms. Pass --shapes, or --allow-no-shapes if an empty shapes graph is what you meant.
[exit 2]

$ shacl -d data/shacl/data.ttl -s data/shacl/no-shapes.ttl --allow-no-shapes
conforms: true
[exit 0]

$ shacl --version
shacl 0.3.4
[exit 0]
```

</details>

**Sources:**

- [engine commit 986c31b (0.3.4)](https://github.com/pwin/SHACL_Engine/commit/986c31ba4e071560d51fed36e99abd8cb3747a87): “Refuse to validate against no shapes on the command line” (quote found, checked 2026-10-22)
- [engine README, coming from pySHACL](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L279-L282): “reports `Conforms: True` and exits 0; this exits 2 unless you pass” (quote found, checked 2026-10-22)

---

<a id="c11-08"></a>
### C11.08 — 425 of 426 W3C tests, the exception named

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-08) · [plain edition](../docs/11-rules-and-inference.md#conformance-and-a-perfect-score-that-broke-things)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The engine passes **425 of the 426** W3C SHACL 1.0 and 1.2 tests

**Sources:**

- [engine README](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L292): “425 of 426” (quote found, checked 2026-10-22)
- [engine README, the subquery rule](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L316-L323): “0.3.0 briefly enforced the letter of the rule and passed all 426.” (quote found, checked 2026-10-22)
- [engine commit 1944802 (0.3.1)](https://github.com/pwin/SHACL_Engine/commit/1944802e9a33b0116d6b660045c9d2813f9ef2d5) (exists, checked 2026-10-22)
- [engine README, the EARL report](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L366-L369): “The W3C compiles a specification's implementation report from EARL files” (quote found, checked 2026-10-22)

---

<a id="c11-09"></a>
### C11.09 — holos rules materialises into a graph of its own

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-09) · [plain edition](../docs/11-rules-and-inference.md#112-four-ways-to-derive-a-triple)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified on the acme employees, with one rule typing every `acme:Employee` as a

**Inputs:** [`data/holos/rules.rq`](data/holos/rules.rq)

<details><summary><code>data/holos/rules.rq</code></summary>

```sparql
# Chapter 11: one materialising rule for `holos rules`. Plain CONSTRUCT, not SHACL-AF.
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX acme: <https://acme.example.org/ns/>
CONSTRUCT { ?e rdf:type foaf:Agent } WHERE { ?e rdf:type acme:Employee }
```

</details>

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples -o work/C11_09/employees.nt
holos stats --data work/C11_09/employees.nt --store work/C11_09/store
holos rules --store work/C11_09/store --rules data/holos/rules.rq
holos query --store work/C11_09/store --query "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"
```

**What is checked:** 5 facts derived in 2 rounds into holos:derived; the store goes from 40 to 45 quads; the derived graph holds the 5

**Recorded result:** PASS — step 3 exits 0; step 3 output contains 'derived 5 fact(s) into <https://holos.dev/ns#derived>', 'rounds  2', 'store   40 -> 45 quads'; step 4 output contains 'https://holos.dev/ns#derived', '"value":"5"'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --ntriples -o work/C11_09/employees.nt

[exit 0]

$ holos stats --data work/C11_09/employees.nt --store work/C11_09/store
quads            40
dictionary terms 31
named graphs     0
on disk          150.2 KiB
free here        88.9 GiB
room to compact  yes (needs up to 150.2 KiB)
predicates by frequency
          10  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
           5  <http://xmlns.com/foaf/0.1/name>
           5  <https://acme.example.org/ns/hasEmployeeId>
           5  <http://xmlns.com/foaf/0.1/mbox>
           5  <https://acme.example.org/ns/worksIn>
           5  <https://acme.example.org/ns/hasRole>
           5  <https://acme.example.org/ns/hasSkill>
loaded 40 quads in 0.26s (151 quads/s)
[exit 0]

$ holos rules --store work/C11_09/store --rules data/holos/rules.rq
1 rule(s) from data/holos/rules.rq:
  rule 1
derived 5 fact(s) into <https://holos.dev/ns#derived>
  rounds  2
  store   40 -> 45 quads
[exit 0]

$ holos query --store work/C11_09/store --query "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"
{"head":{"vars":["g","n"]},"results":{"bindings":[{"g":{"type":"uri","value":"https://holos.dev/ns#derived"},"n":{"type":"literal","value":"5","datatype":"http://www.w3.org/2001/XMLSchema#integer"}}]}}
[exit 0]
```

</details>

---

<a id="c11-10"></a>
### C11.10 — RDFS closure lets a shape see a sub-property

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-10) · [plain edition](../docs/11-rules-and-inference.md#why-rdfs-closure-is-not-optional-trivia)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> SHACL follows `rdfs:subClassOf` when deciding class membership, and **nothing

**Inputs:** [`data/shacl/rdfs/data.ttl`](data/shacl/rdfs/data.ttl), [`data/shacl/rdfs/shapes.ttl`](data/shacl/rdfs/shapes.ttl)

<details><summary><code>data/shacl/rdfs/data.ttl</code></summary>

```turtle
# ex:father is a sub-property of ex:parent; Bob has a father and no name.
@prefix ex:   <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:father rdfs:subPropertyOf ex:parent .
ex:bob ex:father ex:carl .
```

</details>

<details><summary><code>data/shacl/rdfs/shapes.ttl</code></summary>

```turtle
# Anyone who is somebody's child (has an ex:parent) must have a name.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:ChildShape a sh:NodeShape ; sh:targetSubjectsOf ex:parent ;
  sh:property [ sh:path ex:name ; sh:minCount 1 ] .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/shacl/rdfs/data.ttl -s data/shacl/rdfs/shapes.ttl
shacl -d data/shacl/rdfs/data.ttl -s data/shacl/rdfs/shapes.ttl --inference rdfs
```

**What is checked:** without inference the shape never targets bob (conforms); with --inference rdfs it does, and bob's missing name is reported

**Recorded result:** PASS — step 1: conforms: true; step 2: conforms: false; step 2 output contains 'focus <http://example.org/bob>'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/shacl/rdfs/data.ttl -s data/shacl/rdfs/shapes.ttl
conforms: true
[exit 0]

$ shacl -d data/shacl/rdfs/data.ttl -s data/shacl/rdfs/shapes.ttl --inference rdfs
conforms: false
  MinCountConstraintComponent | focus <http://example.org/bob> | value - | path <http://example.org/name>
[exit 1]
```

</details>

---

<a id="c11-30"></a>
### C11.30 — Since 0.3.3 the closure is handed out, minus what RDF cannot write

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-30) · [plain edition](../docs/11-rules-and-inference.md#why-rdfs-closure-is-not-optional-trivia)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Since 0.3.3 the engine also hands the closure out: `shacl.rdfs_closure` in Python,

**Inputs:** [`data/shacl/rdfs/data.ttl`](data/shacl/rdfs/data.ttl)

<details><summary><code>data/shacl/rdfs/data.ttl</code></summary>

```turtle
# ex:father is a sub-property of ex:parent; Bob has a father and no name.
@prefix ex:   <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:father rdfs:subPropertyOf ex:parent .
ex:bob ex:father ex:carl .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/rdfs_closure.py data/shacl/rdfs/data.ttl
```

<details><summary><code>scripts/rdfs_closure.py</code></summary>

```python
"""Chapter 11 §11.2: the RDFS closure, handed out by the SHACL engine (0.3.3).

    python scripts/rdfs_closure.py data/shacl/rdfs/data.ttl

1. Closes the given document with shacl.rdfs_closure and prints what it gained.
2. Closes a two-triple document in which a property with a declared range has a
   literal value. rdfs3 entails that the literal is an instance of the range,
   which RDF cannot write; the closure drops it.
3. Says whether anything was typed rdfs:Resource (the rule the engine leaves out).
"""
import sys

import shacl
from rdflib import RDF, RDFS, Graph, Literal

sys.stdout.reconfigure(encoding="utf-8")


def graph(text):
    g = Graph()
    g.parse(data=text, format="turtle")
    return g


source = open(sys.argv[1], encoding="utf-8").read()
before, after = graph(source), graph(shacl.rdfs_closure(source))
print(f"1. {sys.argv[1]}: {len(before)} triples, {len(after)} after the closure; gained:")
for s, p, o in sorted(set(after) - set(before)):
    print(f"   {s.n3()} {p.n3()} {o.n3()}")

ranged = """@prefix ex: <http://example.org/> . @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:email rdfs:range ex:Address . ex:dave ex:email "dave@example.com" ."""
closed = graph(shacl.rdfs_closure(ranged))
typed_literal = any(isinstance(s, Literal) for s, _, _ in closed.triples((None, RDF.type, None)))
print(f"2. a ranged property with a literal value: {len(closed)} triples after the closure; "
      f"literal typed as the range: {typed_literal}")
resource = len(list(after.triples((None, RDF.type, RDFS.Resource)))) + len(list(closed.triples((None, RDF.type, RDFS.Resource))))
print(f"3. triples typing something rdfs:Resource: {resource}")
```

</details>

**What is checked:** shacl.rdfs_closure adds the sub-property entailment (bob's parent); drops the rdfs3 entailment that would type a literal; and types nothing as rdfs:Resource

**Recorded result:** PASS — step 1 output contains '2 triples, 3 after the closure', '<http://example.org/bob> <http://example.org/parent> <http://example.org/carl>', 'literal typed as the range: False', 'triples typing something rdfs:Resource: 0'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/rdfs_closure.py data/shacl/rdfs/data.ttl
1. data/shacl/rdfs/data.ttl: 2 triples, 3 after the closure; gained:
   <http://example.org/bob> <http://example.org/parent> <http://example.org/carl>
2. a ranged property with a literal value: 2 triples after the closure; literal typed as the range: False
3. triples typing something rdfs:Resource: 0
[exit 0]
```

</details>

**Sources:**

- [engine commit 66eb9f9](https://github.com/pwin/SHACL_Engine/commit/66eb9f9e065615ea338723ef16e095aa7bd3cd79): “Entailments RDF cannot express are dropped rather than refused.” (quote found, checked 2026-10-22)

---

<a id="c11-11"></a>
### C11.11 — Triple rules are off by default and fire with -a

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-11) · [plain edition](../docs/11-rules-and-inference.md#113-triple-rules)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Rules are **off by default** and enabled with `-a`:

**Inputs:** [`data/rules/triple.ttl`](data/rules/triple.ttl), [`data/rules/people.ttl`](data/rules/people.ttl)

<details><summary><code>data/rules/triple.ttl</code></summary>

```turtle
# Two triple rules on Person, and a shape that only exists to see what they made.
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:  <http://example.org/> .

ex:PersonShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate rdf:type ; sh:object ex:Agent ] ;
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate ex:contact ;
        sh:object [ sh:path ex:knows ] ] .

ex:AgentShape a sh:NodeShape ;
    sh:targetClass ex:Agent ;
    sh:property [ sh:path ex:contact ; sh:minCount 1 ;
                  sh:message "Agent has no contact" ] .
```

</details>

<details><summary><code>data/rules/people.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:alice a ex:Person ; ex:knows ex:bob, ex:carol .
ex:dave  a ex:Person .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/people.ttl -s data/rules/triple.ttl
shacl -d data/rules/people.ttl -s data/rules/triple.ttl -a
```

**What is checked:** without -a nothing is typed ex:Agent, so the Agent shape has no targets; with -a both people become Agents, alice gets her contacts from the path rule and dave, who knows nobody, is reported

**Recorded result:** PASS — step 1: conforms: true; step 2: conforms: false; step 2 output contains 'focus <http://example.org/dave>'; step 2 output has none of 'focus <http://example.org/alice>'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/people.ttl -s data/rules/triple.ttl
conforms: true
[exit 0]

$ shacl -d data/rules/people.ttl -s data/rules/triple.ttl -a
conforms: false
  MinCountConstraintComponent | focus <http://example.org/dave> | value - | path <http://example.org/contact>
[exit 1]
```

</details>

---

<a id="c11-12"></a>
### C11.12 — One result per source instance, at 1,000 and 100,000

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-12) · [plain edition](../docs/11-rules-and-inference.md#verified-behaviour)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> inferred `ex:Party` instances against a shape requiring a property none of them

**Commands** (from the `evidence/` folder):

```bash
python scripts/rule_scale.py 1000 100000
```

<details><summary><code>scripts/rule_scale.py</code></summary>

```python
"""Chapter 11 §11.3: a rule's output, validated, gives one result per source instance.

    python scripts/rule_scale.py 1000 100000

For each size N, generates N instances of ex:Person, a rule typing every Person
as an ex:Party, and a shape requiring every Party to have an ex:partyId, which
none has. With rules applied there should be exactly N results, one per focus
node, with no misses and no duplicates; without them, none. Uses the shacl
package (the same engine as the CLI). Times are printed, not asserted.
"""
import os
import sys
import tempfile
import time

import shacl

sys.stdout.reconfigure(encoding="utf-8")

SHAPES = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex: <http://example.org/> .
ex:PersonRules a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:rule [ a sh:TripleRule ; sh:subject sh:this ; sh:predicate rdf:type ; sh:object ex:Party ] .
ex:PartyShape a sh:NodeShape ; sh:targetClass ex:Party ;
  sh:property [ sh:path ex:partyId ; sh:minCount 1 ] .
"""

with tempfile.TemporaryDirectory() as tmp:
    shapes_path = os.path.join(tmp, "shapes.ttl")
    with open(shapes_path, "w", encoding="utf-8") as f:
        f.write(SHAPES)
    shapes = shacl.Shapes.from_file(shapes_path)
    for n in (int(a) for a in sys.argv[1:]):
        data_path = os.path.join(tmp, f"people-{n}.nt")
        with open(data_path, "w", encoding="utf-8") as f:
            for i in range(n):
                f.write(f"<http://example.org/p{i}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                        f"<http://example.org/Person> .\n")
        t0 = time.perf_counter()
        with_rules = shapes.validate_file(data_path, inference="rules")
        t1 = time.perf_counter()
        without = shapes.validate_file(data_path)
        foci = {str(r.focus_node) for r in with_rules.results}
        print(f"N={n:>7,}  with rules: {len(with_rules.results):>7,} results on {len(foci):>7,} distinct focus nodes "
              f"({t1 - t0:.2f} s)  without rules: {len(without.results)} results")
```

</details>

**What is checked:** 1,000 results on 1,000 distinct focus nodes, and 100,000 on 100,000; none without rules

**Recorded result:** PASS — step 1 output contains 'N=  1,000  with rules:   1,000 results on   1,000 distinct focus nodes', 'N=100,000  with rules: 100,000 results on 100,000 distinct focus nodes', 'without rules: 0 results'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/rule_scale.py 1000 100000
N=  1,000  with rules:   1,000 results on   1,000 distinct focus nodes (0.12 s)  without rules: 0 results
N=100,000  with rules: 100,000 results on 100,000 distinct focus nodes (4.12 s)  without rules: 0 results
[exit 0]
```

</details>

---

<a id="c11-13"></a>
### C11.13 — A SPARQL rule computes the area, and validation sees it

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-13) · [plain edition](../docs/11-rules-and-inference.md#114-sparql-rules)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified at 0.3.4: with `width 3` and `height 4`, a shape asserting

**Inputs:** [`data/rules/sparql-rule.ttl`](data/rules/sparql-rule.ttl), [`data/rules/box.ttl`](data/rules/box.ttl)

<details><summary><code>data/rules/sparql-rule.ttl</code></summary>

```turtle
# A SPARQL rule computing an area; the shape asserts the result is 12.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:BoxShape a sh:NodeShape ; sh:targetClass ex:Box ;
    sh:rule [ a sh:SPARQLRule ; sh:construct """
        PREFIX ex: <http://example.org/>
        CONSTRUCT { $this ex:area ?a }
        WHERE { $this ex:width ?w ; ex:height ?h . BIND(?w * ?h AS ?a) }""" ] ;
    sh:property [ sh:path ex:area ; sh:minCount 1 ; sh:hasValue 12 ;
                  sh:message "area must be 12" ] .
```

</details>

<details><summary><code>data/rules/box.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:b a ex:Box ; ex:width 3 ; ex:height 4 .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl -a
shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl
```

**What is checked:** with -a the derived area 12 satisfies sh:hasValue 12; without it, the shape fails

**Recorded result:** PASS — step 1: conforms: true; step 1 exits 0; step 2: conforms: false

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl -a
conforms: true
[exit 0]

$ shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl
conforms: false
  HasValueConstraintComponent | focus <http://example.org/b> | value - | path <http://example.org/area>
  MinCountConstraintComponent | focus <http://example.org/b> | value - | path <http://example.org/area>
[exit 1]
```

</details>

---

<a id="c11-14"></a>
### C11.14 — Since 0.3.0 only sh:ShapesGraph declarations apply

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-14) · [plain edition](../docs/11-rules-and-inference.md#114-sparql-rules)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> `sh:declare`/`sh:prefixes` mechanism. Since 0.3.0, with no `sh:prefixes` on a

**Sources:**

- [engine commit d7769bf](https://github.com/pwin/SHACL_Engine/commit/d7769bfd0a310e78876976bf8ba7c69ad3fab61b): “With no sh:prefixes on a query, only declarations on nodes typed sh:ShapesGraph apply.” (quote found, checked 2026-10-22)

---

<a id="c11-15"></a>
### C11.15 — Rule compile errors are held on the rule

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-15) · [plain edition](../docs/11-rules-and-inference.md#114-sparql-rules)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> > **Fixed before 0.1.8 shipped.**

**Sources:**

- [engine commit 637ebf5](https://github.com/pwin/SHACL_Engine/commit/637ebf5b0dc9715bc1af4102cb7cd964c92374f2): “Rule compile errors are held on the rule now and raised only if that rule would have fired” (quote found, checked 2026-10-22)

---

<a id="c11-16"></a>
### C11.16 — Hazard 1: a rule on a shape with no target never fires

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-16) · [plain edition](../docs/11-rules-and-inference.md#115-four-ways-to-get-a-wrong-answer)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified: the rule never runs, nothing is inferred, and no message says so.

**Inputs:** [`data/rules/nested.ttl`](data/rules/nested.ttl), [`data/rules/nested-data.ttl`](data/rules/nested-data.ttl)

<details><summary><code>data/rules/nested.ttl</code></summary>

```turtle
# Hazard 1: a rule on a nested property shape, which has no target, never fires.
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:  <http://example.org/> .

ex:S a sh:NodeShape ; sh:targetClass ex:Person ;
    sh:property [ sh:path ex:name ;
        sh:rule [ a sh:TripleRule ;
            sh:subject sh:this ; sh:predicate rdf:type ; sh:object ex:Tagged ] ] .

ex:Check a sh:NodeShape ; sh:targetClass ex:Tagged ;
    sh:property [ sh:path ex:nope ; sh:minCount 1 ] .
```

</details>

<details><summary><code>data/rules/nested-data.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:p a ex:Person ; ex:name "x" .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/nested-data.ttl -s data/rules/nested.ttl -a
```

**What is checked:** conforms true, exit 0, no message: the Tagged check never had a target

**Recorded result:** PASS — step 1: conforms: true; step 1 exits 0; and nothing on stderr

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/nested-data.ttl -s data/rules/nested.ttl -a
conforms: true
[exit 0]
```

</details>

---

<a id="c11-17"></a>
### C11.17 — Hazard 2: one pass does not close a transitive rule

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-17) · [plain edition](../docs/11-rules-and-inference.md#115-four-ways-to-get-a-wrong-answer)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **One pass, so a transitive rule does not close.**

**Inputs:** [`data/rules/transitive.ttl`](data/rules/transitive.ttl), [`data/rules/chain.ttl`](data/rules/chain.ttl)

<details><summary><code>data/rules/transitive.ttl</code></summary>

```turtle
# Hazard 2: one pass. Deriving ex:sub from two hops of ex:sub reaches two hops.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:S a sh:NodeShape ; sh:targetClass ex:T ;
    sh:rule [ a sh:SPARQLRule ; sh:construct """
        PREFIX ex: <http://example.org/>
        CONSTRUCT { $this ex:sub ?z }
        WHERE { $this ex:sub ?y . ?y ex:sub ?z }""" ] ;
    sh:property [ sh:path ex:sub ;
        sh:qualifiedValueShape [ sh:hasValue ex:d ] ; sh:qualifiedMinCount 1 ;
        sh:message "should reach ex:d transitively" ] .
```

</details>

<details><summary><code>data/rules/chain.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:a a ex:T ; ex:sub ex:b . ex:b a ex:T ; ex:sub ex:c . ex:c a ex:T ; ex:sub ex:d .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/chain.ttl -s data/rules/transitive.ttl -a
shacl -d data/rules/chain.ttl -s data/rules/transitive.ttl -a --iterate-rules 10
```

**What is checked:** one pass: a does not reach d; --iterate-rules 10: it does

**Recorded result:** PASS — step 1: conforms: false; step 1 output contains 'focus <http://example.org/a>'; step 2: conforms: true

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/chain.ttl -s data/rules/transitive.ttl -a
conforms: false
  QualifiedMinCountConstraintComponent | focus <http://example.org/a> | value - | path <http://example.org/sub>
[exit 1]

$ shacl -d data/rules/chain.ttl -s data/rules/transitive.ttl -a --iterate-rules 10
conforms: true
[exit 0]
```

</details>

---

<a id="c11-18"></a>
### C11.18 — Hazard 3: equal sh:order cannot see each other's inferences

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-18) · [plain edition](../docs/11-rules-and-inference.md#115-four-ways-to-get-a-wrong-answer)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Rules at the same `sh:order` cannot see each other's inferences.**

**Inputs:** [`data/rules/order.ttl`](data/rules/order.ttl), [`data/rules/order-data.ttl`](data/rules/order-data.ttl)

<details><summary><code>data/rules/order.ttl</code></summary>

```turtle
# Hazard 3: rules at the same sh:order cannot see each other's inferences.
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex:  <http://example.org/> .

ex:A a sh:NodeShape ; sh:targetClass ex:Person ;
    sh:rule [ a sh:TripleRule ; sh:subject sh:this ;
              sh:predicate rdf:type ; sh:object ex:Step1 ] .
ex:B a sh:NodeShape ; sh:targetClass ex:Step1 ;
    sh:rule [ a sh:TripleRule ; sh:subject sh:this ;
              sh:predicate rdf:type ; sh:object ex:Step2 ] .
ex:C a sh:NodeShape ; sh:targetClass ex:Step2 ;
    sh:property [ sh:path ex:nope ; sh:minCount 1 ; sh:message "reached Step2" ] .
```

</details>

<details><summary><code>data/rules/order-data.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:p a ex:Person .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/order-data.ttl -s data/rules/order.ttl -a
shacl -d data/rules/order-data.ttl -s data/rules/order.ttl -a --iterate-rules 5
```

**What is checked:** one pass: Step2 is never reached (conforms); iterated: it is, and its check fails

**Recorded result:** PASS — step 1: conforms: true; step 2: conforms: false; step 2 output contains 'path <http://example.org/nope>'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/order-data.ttl -s data/rules/order.ttl -a
conforms: true
[exit 0]

$ shacl -d data/rules/order-data.ttl -s data/rules/order.ttl -a --iterate-rules 5
conforms: false
  MinCountConstraintComponent | focus <http://example.org/p> | value - | path <http://example.org/nope>
[exit 1]
```

</details>

---

<a id="c11-19"></a>
### C11.19 — Hazard 4: a conclusion from absence outlives the absence

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-19) · [plain edition](../docs/11-rules-and-inference.md#115-four-ways-to-get-a-wrong-answer)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Negation is not monotonic, and iteration exposes it.**

**Inputs:** [`data/rules/negation.ttl`](data/rules/negation.ttl), [`data/rules/negation-data.ttl`](data/rules/negation-data.ttl)

<details><summary><code>data/rules/negation.ttl</code></summary>

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

# Hazard 4: negation is not monotonic. The first rule marks a Person with no
# name as Unnamed; the second, at a later sh:order, gives every Person a name.
# Rules only add triples, so the mark stays after the name arrives.
ex:R a sh:NodeShape ; sh:targetClass ex:Person ;
    sh:rule [ a sh:SPARQLRule ; sh:order 0 ; sh:construct """
        PREFIX ex: <http://example.org/>
        CONSTRUCT { $this a ex:Unnamed } WHERE { FILTER NOT EXISTS { $this ex:name ?n } }""" ] ;
    sh:rule [ a sh:TripleRule ; sh:order 1 ;
        sh:subject sh:this ; sh:predicate ex:name ; sh:object "assigned later" ] .

# Anything still marked Unnamed must have no name. This is what fails.
ex:Check a sh:NodeShape ; sh:targetClass ex:Unnamed ;
    sh:property [ sh:path ex:name ; sh:maxCount 0 ;
                  sh:message "marked Unnamed, yet it has a name" ] .
```

</details>

<details><summary><code>data/rules/negation-data.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .

# One Person, with no name to begin with.
ex:a a ex:Person .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/negation-data.ttl -s data/rules/negation.ttl -a
shacl -d data/rules/negation-data.ttl -s data/rules/negation.ttl
```

**What is checked:** with rules, ex:a ends up both Unnamed and named, and the check reports it; without rules there is nothing to report

**Recorded result:** PASS — step 1: conforms: false; step 1 output contains 'MaxCountConstraintComponent | focus <http://example.org/a>'; step 2: conforms: true

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/negation-data.ttl -s data/rules/negation.ttl -a
conforms: false
  MaxCountConstraintComponent | focus <http://example.org/a> | value - | path <http://example.org/name>
[exit 1]

$ shacl -d data/rules/negation-data.ttl -s data/rules/negation.ttl
conforms: true
[exit 0]
```

</details>

Shown with two sh:order levels in one pass, which is the same mechanism iteration exposes: a later rule supplies what an earlier one tested for, and nothing withdraws the earlier conclusion.

---

<a id="c11-20"></a>
### C11.20 — Rules never modify the input graph

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-20) · [plain edition](../docs/11-rules-and-inference.md#115-four-ways-to-get-a-wrong-answer)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> > **And one that is not a hazard:** rules never modify the graph you passed in.

**Sources:**

- [engine commit 8de05ba](https://github.com/pwin/SHACL_Engine/commit/8de05bae23e410d97c040743f4ca7e0eb4ff6947): “Rules return a new graph rather than expanding the caller's.” (quote found, checked 2026-10-22)

---

<a id="c11-21"></a>
### C11.21 — The previous edition's timings, and 0.3.0's own measurement

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-21) · [plain edition](../docs/11-rules-and-inference.md#116-rules-at-scale)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> > These figures were measured for the previous edition, at engine 0.2.0, and have

**Sources:**

- [the previous edition's rules-at-scale table](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/11-rules-and-inference.md#L333): “| 100,000 | ~690,000 | 2.7s | **11.9s** |” (quote found, checked 2026-10-22)
- [the previous edition's pySHACL comparison](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/11-rules-and-inference.md#L346): “| 1,000 | 0.040s | 2.992s | 75× |” (quote found, checked 2026-10-22)
- [the previous edition's WebAssembly table](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/11-rules-and-inference.md#L371): “| 100,000 | 400,000 | **12,611 ms** | **3,119 ms** | 329 MB |” (quote found, checked 2026-10-22)
- [engine README, current timings](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L68-L71): “| cached index, all cores — the defaults | **0.23s** |” (quote found, checked 2026-10-22)
- [engine commit 6fa00e3 (0.3.0)](https://github.com/pwin/SHACL_Engine/commit/6fa00e3deb2e02b5b32e6a1a78f7360e33da31e8) (exists, checked 2026-10-22)

Recorded measurements, not reproduced here. C11.12 reproduces the result counts behind the first table, at 1,000 and 100,000.

---

<a id="c11-22"></a>
### C11.22 — The index holds the graph three times; results sorted by focus node

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-22) · [plain edition](../docs/11-rules-and-inference.md#116-rules-at-scale)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> And the index holds the graph **three times over**

**Sources:**

- [engine README](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L117-L118): “A graph is held three times over, once per permutation” (quote found, checked 2026-10-22)
- [engine README](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L101): “That order is by focus node” (quote found, checked 2026-10-22)

---

<a id="c11-23"></a>
### C11.23 — --build-index caches the parsed graph

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-23) · [plain edition](../docs/11-rules-and-inference.md#116-rules-at-scale)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> (The CLI now offers `--build-index`,

**Commands** (from the `evidence/` folder):

```bash
shacl --help
```

**What is checked:** `shacl --help` documents --build-index

**Recorded result:** PASS — step 1 output contains '--build-index', 'Cache the parsed data graph beside it as `<file>.shix`'

<details><summary>Output, as recorded</summary>

```text
$ shacl --help
A high-performance SHACL validator
Usage: shacl.exe [OPTIONS] --data <DATA>...
Options:
  -d, --data <DATA>...
          The data graph to validate. A path, an `http(s)` URL, or `-` for standard input.
          Repeat it to merge several documents into one graph. Blank nodes stay separate per document, as they must: `_:a` in two files is two nodes.
  -s, --shapes <SHAPES>...
          The shapes graph, on the same terms as `--data` and likewise repeatable. Defaults to the data graph, matching the convention that a self-describing document carries its own shapes.
          Only one input in total may be `-`, since standard input can be read only once.
      --data-format <DATA_FORMAT>
          The data graph's RDF syntax. Guessed from the file extension, or over HTTP from the `Content-Type`, when omitted; required when `--data` is `-`, which has neither
          [alias: --df]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --shapes-format <SHAPES_FORMAT>
          The shapes graph's RDF syntax, on the same terms as `--data-format`
          [alias: --sf]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --build-index
          Cache the parsed data graph beside it as `<file>.shix`, so later runs skip parsing.
          Parsing is around three quarters of a run over a large graph, and a data graph that has not changed is parsed identically every time. The cache is checked against the source on every use, so a stale one is never read — see `--no-index`.
          Only for a single local `--data` file: a URL has nowhere to write, and merged documents have no one source to check against.
      --no-index
          Ignore any `<file>.shix` cache and parse the data graph
      --allow-no-shapes
          Validate against a shapes graph that declares no shapes, instead of refusing to.
          Validating against no shapes conforms, because there is nothing to violate. Without this flag that is an error rather than a pass: the usual cause is a forgotten `--shapes`, and reporting success for a graph nothing was checked against is the worst answer a validator can give. Pass it when an empty shapes graph is what you meant.
      --threads <N>
          Worker threads for validation. `0` uses every core; `1` runs sequentially.
          Only a SHACL Core shapes graph splits across threads. One using `sh:sparql`, a SPARQL-based constraint component or node expressions runs sequentially whatever this says, as does any run with `--max-results`. The report is the same either way, byte for byte.
          [default: 0]
… (55 lines omitted; full output in the outputs/ record)
          Report how long loading, compiling and validating each took
      --repeat <REPEAT>
          Validate `n` times, reporting the best wall time. For benchmarking
          [default: 1]
  -h, --help
          Print help (see a summary with '-h')
  -V, --version
          Print version
[exit 0]
```

</details>

---

<a id="c11-24"></a>
### C11.24 — A SHACL function in a rule is an error, exit 2

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-24) · [plain edition](../docs/11-rules-and-inference.md#117-what-is-not-there)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | **SHACL functions** (`sh:SPARQLFunction`) | A rule calling one errors (exit 2) rather than returning

**Inputs:** [`data/rules/function.ttl`](data/rules/function.ttl), [`data/rules/function-data.ttl`](data/rules/function-data.ttl)

<details><summary><code>data/rules/function.ttl</code></summary>

```turtle
# Not implemented: a SHACL function used in a rule. Must be "could not validate".
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:  <http://example.org/> .

ex:double a sh:SPARQLFunction ;
    sh:parameter [ sh:path ex:n ; sh:datatype xsd:integer ] ;
    sh:returnType xsd:integer ;
    sh:select "SELECT ($n * 2 AS ?result) WHERE {}" .

ex:S a sh:NodeShape ; sh:targetClass ex:Thing ;
    sh:rule [ a sh:TripleRule ; sh:subject sh:this ;
        sh:predicate ex:twice ; sh:object [ ex:double ( 21 ) ] ] .
```

</details>

<details><summary><code>data/rules/function-data.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:t a ex:Thing .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/function-data.ttl -s data/rules/function.ttl -a
```

**What is checked:** exit 2, 'unsupported node expression'

**Recorded result:** PASS — step 1 exits 2; step 1 output contains 'unsupported node expression'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/function-data.ttl -s data/rules/function.ttl -a
error: applying SHACL-AF rules: invalid shapes graph: unsupported node expression
[exit 2]
```

</details>

**Sources:**

- [engine README, what does not work](https://github.com/pwin/SHACL_Engine/blob/986c31ba4e071560d51fed36e99abd8cb3747a87/README.md#L460-L469): “is vendored under `testsuite/shacl12/tests/rules/` but is not wired into the” (quote found, checked 2026-10-22)

---

<a id="c11-25"></a>
### C11.25 — Rules in WebAssembly, and an unknown mode is an error there too

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-25) · [plain edition](../docs/11-rules-and-inference.md#rules-in-the-browser-the-engine-can-the-editor-does-not)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Every binding runs rules, CLI, Python and WebAssembly alike, through the same

**Commands** (from the `evidence/` folder):

```bash
node scripts/wasm_conforms.mjs data/shacl
```

<details><summary><code>scripts/wasm_conforms.mjs</code></summary>

```javascript
// Chapter 11 §11.1: what "conforms" means in the WebAssembly build.
//
//   node scripts/wasm_conforms.mjs data/shacl
//
// shacl-wasm-node 0.3.0 and 0.3.1 kept the old rule (only sh:Violation breaks
// conformance) after the CLI and Python bindings had moved to the specification's.
// 0.3.2 caught up. This validates a warnings-only graph through the package and
// prints the verdict.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const require = createRequire(import.meta.url);
const { Validator } = require('shacl-wasm-node');
const pkg = require('shacl-wasm-node/package.json');

const dir = process.argv[2];
const data = readFileSync(join(dir, 'data.ttl'), 'utf8');
for (const file of ['shapes-warning.ttl', 'shapes-violation.ttl']) {
  const v = Validator.fromTurtle(readFileSync(join(dir, file), 'utf8'));
  const report = v.validateTurtle(data, null, 'none');
  const severities = report.results.map((r) => String(r.severity ?? r.resultSeverity ?? '?'));
  console.log(`shacl-wasm-node ${pkg.version}  ${file.padEnd(22)} conforms=${report.conforms}  results=${report.results.length}  severities=${severities.join(',')}`);
}

// §11.7: rules through the same build, and a mode that does not exist.
const rules = Validator.fromTurtle(readFileSync(join(dir, '..', 'rules', 'triple.ttl'), 'utf8'));
const people = readFileSync(join(dir, '..', 'rules', 'people.ttl'), 'utf8');
for (const mode of ['none', 'rules', 'bogus']) {
  try {
    const r = rules.validateTurtle(people, null, mode);
    console.log(`inference=${mode.padEnd(6)} conforms=${r.conforms}  results=${r.results.length}`);
  } catch (e) {
    console.log(`inference=${mode.padEnd(6)} ERROR: ${e.message ?? e}`);
  }
}
```

</details>

**What is checked:** through shacl-wasm-node, 'rules' fires and 'none' does not; an unknown mode is an error

**Recorded result:** PASS — step 1 output contains 'inference=none   conforms=true  results=0', 'inference=rules  conforms=false  results=1', 'inference=bogus  ERROR: unknown inference "bogus"'

<details><summary>Output, as recorded</summary>

```text
$ node scripts/wasm_conforms.mjs data/shacl
shacl-wasm-node 0.3.4  shapes-warning.ttl     conforms=false  results=1  severities=http://www.w3.org/ns/shacl#Warning
shacl-wasm-node 0.3.4  shapes-violation.ttl   conforms=false  results=1  severities=http://www.w3.org/ns/shacl#Violation
inference=none   conforms=true  results=0
inference=rules  conforms=false  results=1
inference=bogus  ERROR: unknown inference "bogus": expected "none", "rdfs", "rules" or "rules-iterated"
[exit 0]
```

</details>

---

<a id="c11-26"></a>
### C11.26 — The editor asks for inference 'none', deliberately

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-26) · [plain edition](../docs/11-rules-and-inference.md#rules-in-the-browser-the-engine-can-the-editor-does-not)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> `shacl-wasm-node` 0.3.2, so the capability is present, but its runner still asks

**Sources:**

- [extension src/checks/shaclRunner.ts](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/src/checks/shaclRunner.ts#L25-L31): “so this deliberately stays at `"none"`” (quote found, checked 2026-10-22)

---

<a id="c11-27"></a>
### C11.27 — Named graphs are flattened

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-27) · [plain edition](../docs/11-rules-and-inference.md#named-graphs-are-flattened-in-the-engine)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Worth repeating because rules make it sharper: quad syntaxes parse, and then every

**Evidence:** the same as [C14.07 — SHACL validates the union of the named graphs](#c14-07), which reproduces it: step 1 output contains 'focus <http://example.org/bob>', 'focus <http://example.org/carol>', 'focus <http://example.org/dave>'; the TriG and the flattened file give identical reports; step 3 output has none of '--graph'

---

<a id="c11-28"></a>
### C11.28 — Exit codes 0, 1 and 2

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-28) · [plain edition](../docs/11-rules-and-inference.md#exit-codes-make-this-gateable)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Verified across all three at 0.3.4.

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl -a
shacl -d data/shacl/data.ttl -s data/shacl/shapes-violation.ttl
shacl -d data/rules/function-data.ttl -s data/rules/function.ttl -a
```

**What is checked:** conforming: 0; not conforming: 1; could not validate: 2

**Recorded result:** PASS — step 1 exits 0; step 2 exits 1; step 3 exits 2

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/rules/box.ttl -s data/rules/sparql-rule.ttl -a
conforms: true
[exit 0]

$ shacl -d data/shacl/data.ttl -s data/shacl/shapes-violation.ttl
conforms: false
  MinCountConstraintComponent | focus <http://example.org/bob> | value - | path <http://example.org/name>
[exit 1]

$ shacl -d data/rules/function-data.ttl -s data/rules/function.ttl -a
error: applying SHACL-AF rules: invalid shapes graph: unsupported node expression
[exit 2]
```

</details>

---

<a id="c11-29"></a>
### C11.29 — holos validate: exit 0 whatever it found up to 0.21.1, a gate from 0.22.0

**In the manual:** [Chapter 11, at the claim](manual/docs/11-rules-and-inference.md#ev-c11-29) · [plain edition](../docs/11-rules-and-inference.md#exit-codes-make-this-gateable)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **`holos validate` became a gate in HOLOS 0.22.0.**

**Inputs:** [`data/shacl/shapes-sparql.ttl`](data/shacl/shapes-sparql.ttl), [`data/rules/nested-data.ttl`](data/rules/nested-data.ttl)

<details><summary><code>data/shacl/shapes-sparql.ttl</code></summary>

```turtle
# A SPARQL-based constraint: beyond SHACL Core. HOLOS's native validator must
# refuse it rather than skip it and answer "conforms".
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:NamedShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:sparql [ a sh:SPARQLConstraint ;
    sh:message "Person has no name" ;
    sh:select """PREFIX ex: <http://example.org/>
                 SELECT $this WHERE { FILTER NOT EXISTS { $this ex:name ?n } }""" ] .
```

</details>

<details><summary><code>data/rules/nested-data.ttl</code></summary>

```turtle
@prefix ex: <http://example.org/> .
ex:p a ex:Person ; ex:name "x" .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-violation.ttl
holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-violation.ttl --engine adapted
holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl
holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl --engine adapted
python scripts/holosdb_validate.py data/shacl/data.ttl data/shacl/shapes-violation.ttl data/shacl/shapes-sparql.ttl
holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl --engine native
# one Person, with a name, which conforms
holos validate --data data/rules/nested-data.ttl --shapes data/shacl/shapes-violation.ttl
holos --version
```

<details><summary><code>scripts/holosdb_validate.py</code></summary>

```python
"""Chapter 13 §13.2 and Chapter 11 §11.8: validation through holosdb.

    python scripts/holosdb_validate.py DATA SHAPES [SPARQL_SHAPES]

Store.validate() returns a dictionary, so a caller has a `conforms` key to test
rather than an exit code. Its native engine refuses a shapes graph that uses
anything beyond SHACL Core, rather than skipping the constraint.

Each validation here runs on a freshly loaded store, because up to 0.21.0
validate() wrote the shapes into the store it validated, so a second call on the
same store counted them twice (see holosdb_validate_repeat.py; fixed in 0.21.1).
"""
import sys

from holosdb import HolosError, Store

sys.stdout.reconfigure(encoding="utf-8")


def fresh() -> Store:
    store = Store()
    store.load(sys.argv[1])
    return store


print("adapted:", fresh().validate(sys.argv[2]))
print("native: ", fresh().validate(sys.argv[2], engine="native"))
if len(sys.argv) > 3:
    try:
        print("native, sh:sparql shapes:", fresh().validate(sys.argv[3], engine="native"))
    except HolosError as exc:
        print(f"native, sh:sparql shapes: HolosError: {exc}")
```

</details>

**What is checked:** both engines print conforms false. Up to 0.21.1 they exit 0 doing so, and the default (native) engine refuses sh:sparql. From 0.22.0 a non-conforming graph exits 1 and a conforming one 0, the default is adapted, which validates sh:sparql, and only --engine native refuses it, with exit 2. holosdb's Store.validate() returns a dictionary with conforms False either way

**Recorded result:** PASS — step 1 output contains 'conforms          false'; step 2 output contains 'conforms          false'; step 5 output contains "'conforms': False", 'HolosError: unsupported: sh:sparql is not implemented'; holos 0.25.0: step 1 exits 1; step 2 exits 1; step 3 exits 1; step 3 output contains 'conforms          false'; step 4 exits 1; step 6 exits 2; step 6 output contains 'sh:sparql'; step 7 exits 0

<details><summary>Output, as recorded</summary>

```text
$ holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-violation.ttl
bridged+compiled  3 triples, 2 shapes in 0.000s
validated         0.000s
conforms          false
results           1
loaded 3 quads in 0.00s (4313 quads/s)
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 1]

$ holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-violation.ttl --engine adapted
bridged+compiled  3 triples, 2 shapes in 0.000s
validated         0.000s
conforms          false
results           1
loaded 3 quads in 0.00s (3403 quads/s)
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 1]

$ holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl
bridged+compiled  3 triples, 1 shapes in 0.001s
validated         0.000s
conforms          false
results           1
loaded 3 quads in 0.00s (3063 quads/s)
read 6 shape quads from data/shacl/shapes-sparql.ttl, and kept none of them
[exit 1]

$ holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl --engine adapted
bridged+compiled  3 triples, 1 shapes in 0.000s
validated         0.000s
conforms          false
results           1
loaded 3 quads in 0.00s (4855 quads/s)
read 6 shape quads from data/shacl/shapes-sparql.ttl, and kept none of them
[exit 1]

$ python scripts/holosdb_validate.py data/shacl/data.ttl data/shacl/shapes-violation.ttl data/shacl/shapes-sparql.ttl
adapted: {'conforms': False, 'violations': 1, 'engine': 'adapted', 'results': [{'focus': 'http://example.org/bob', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:0_b0', 'message': None}]}
native:  {'conforms': False, 'violations': 1, 'engine': 'native', 'results': [{'focus': 'http://example.org/bob', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:f122f814b2947a51e211236be39576ca', 'message': None}]}
native, sh:sparql shapes: HolosError: unsupported: sh:sparql is not implemented by the incremental evaluator; validate                      through holos_shacl::engine::EngineRun instead
[exit 0]

$ holos validate --data data/shacl/data.ttl --shapes data/shacl/shapes-sparql.ttl --engine native
loaded 3 quads in 0.00s (4115 quads/s)
read 6 shape quads from data/shacl/shapes-sparql.ttl, and kept none of them
Error: unsupported: sh:sparql is not implemented by the incremental evaluator; validate                      through holos_shacl::engine::EngineRun instead
[exit 2]

$ holos validate --data data/rules/nested-data.ttl --shapes data/shacl/shapes-violation.ttl
bridged+compiled  2 triples, 2 shapes in 0.000s
validated         0.000s
conforms          true
results           0
loaded 2 quads in 0.00s (2787 quads/s)
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 0]

$ holos --version
holos 0.25.0 (b44aa1c)
[exit 0]
```

</details>

**Sources:**

- [HOLOS commit 462bb56 (0.22.0)](https://github.com/pwin/triplestore/commit/462bb56e66db312f7b49c29d6af2ef91c905c61c): “Make holos validate a gate: exit 1 on violations, and default to adapted” (quote found, checked 2026-10-22)

---

<a id="chapter-12"></a>
## 12. Release and change

Annotated chapter: [manual/docs/12-release-and-change.md](manual/docs/12-release-and-change.md) · plain chapter: [../docs/12-release-and-change.md](../docs/12-release-and-change.md)

<a id="c12-01"></a>
### C12.01 — version-diff: the verdict comes from the axioms

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-01) · [plain edition](../docs/12-release-and-change.md#121-evidence-based-semver-version-diff)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Real output (IRIs shortened to `acme:` here for width):

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/acme-org-v2.ttl --exclude-imports --out-dir work/C12_01/vd --json
python scripts/list_files.py work/C12_01/vd
ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/acme-org-v2.ttl --exclude-imports --out-dir work/C12_01/gate --fail-on major
```

**What is checked:** the diff lists exactly the manual's removals and additions and suggests MAJOR; --json writes diff.json beside diff.txt; --fail-on major exits non-zero

**Recorded result:** PASS — step 1 output contains 'Removed classes [MAJOR]:\n  - https://acme.example.org/ns/Engineer', 'https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee', 'Added classes [minor]:\n  - https://acme.example.org/ns/ProductManager/n  - https://acme.example.org/ns/SoftwareEngineer', 'Added properties [minor]:\n  - https://acme.example.org/ns/hireDate', 'Added equivalentClass axioms [minor]:\n  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer', 'Suggested version bump: MAJOR'; step 2 output contains 'diff.json', 'diff.txt'; step 3 exits non-zero (1)

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/acme-org-v2.ttl --exclude-imports --out-dir work/C12_01/vd --json
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
Written to: work/C12_01/vd/diff.txt
Written to: work/C12_01/vd/diff.json
[exit 0]

$ python scripts/list_files.py work/C12_01/vd
    1,274  diff.json
      922  diff.txt
2 files, 2,196 bytes
[exit 0]

$ ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/acme-org-v2.ttl --exclude-imports --out-dir work/C12_01/gate --fail-on major
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
Written to: work/C12_01/gate/diff.txt
[exit 1]
```

</details>

---

<a id="c12-02"></a>
### C12.02 — Reversed, the diff describes the inverse release

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-02) · [plain edition](../docs/12-release-and-change.md#121-evidence-based-semver-version-diff)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Note the argument order: **old first, then new**.

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v2.ttl fixtures/acme_robotics/acme-org-v1.ttl --exclude-imports --out-dir work/C12_02/rev
```

**What is checked:** v2 → v1 reports ProductManager, SoftwareEngineer and hireDate as removed

**Recorded result:** PASS — step 1 output contains 'Removed classes [MAJOR]:\n  - https://acme.example.org/ns/ProductManager/n  - https://acme.example.org/ns/SoftwareEngineer', 'Removed properties [MAJOR]:\n  - https://acme.example.org/ns/hireDate'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite version-diff fixtures/acme_robotics/acme-org-v2.ttl fixtures/acme_robotics/acme-org-v1.ttl --exclude-imports --out-dir work/C12_02/rev
Ontology version diff: fixtures/acme_robotics/acme-org-v2.ttl -> fixtures/acme_robotics/acme-org-v1.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Removed properties [MAJOR]:
  - https://acme.example.org/ns/hireDate
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/ProductManager no longer rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Removed equivalentClass axioms [MAJOR]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Added classes [minor]:
  - https://acme.example.org/ns/Engineer
Added subclass edges [minor]:
  - https://acme.example.org/ns/Engineer rdfs:subClassOf https://acme.example.org/ns/Employee
Suggested version bump: MAJOR
Written to: work/C12_02/rev/diff.txt
[exit 0]
```

</details>

---

<a id="c12-03"></a>
### C12.03 — Without FOAF resolved, consistency reports foaf:name and foaf:mbox

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-03) · [plain edition](../docs/12-release-and-change.md#121-evidence-based-semver-version-diff)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Note also `--exclude-imports` here, where §12.2 uses `--import-dir`.**

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --exclude-imports --out-dir work/C12_03/noimports
```

**What is checked:** with --exclude-imports, both FOAF properties are reported as undeclared

**Recorded result:** PASS — step 1 output contains '[undeclared_property] http://xmlns.com/foaf/0.1/mbox', '[undeclared_property] http://xmlns.com/foaf/0.1/name'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --exclude-imports --out-dir work/C12_03/noimports
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
2 propert(y/ies) used in TARQL but not declared in the ontology set:
  [undeclared_property] http://xmlns.com/foaf/0.1/mbox
  [undeclared_property] http://xmlns.com/foaf/0.1/name
2 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
  [insert_ontology_stub] fixtures/acme_robotics/acme-org-v2.ttl (confidence 70%)
    Declare 2 term(s) used in TARQL/oxi-gen queries but never declared: http://xmlns.com/foaf/0.1/mbox, http://xmlns.com/foaf/0.1/name
Written to: work/C12_03/noimports/consistency.txt
Wrote 2/2 suggested repair(s) as .patch files under work/C12_03/noimports/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]
```

</details>

---

<a id="c12-04"></a>
### C12.04 — consistency: what breaks, and a 100% repair

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-04) · [plain edition](../docs/12-release-and-change.md#122-change-impact-consistency)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `consistency` runs the version diff *and* checks every transformation query

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_04/consistency
python scripts/list_files.py work/C12_04/consistency
```

**What is checked:** MAJOR; acme:Engineer undeclared in the query; one rename at 100%, written as a .patch; no undeclared properties once imports are resolved

**Recorded result:** PASS — step 1 output contains 'Suggested version bump: MAJOR', '1 class(es) used in TARQL but not declared in the ontology set:\n  [undeclared_class] https://acme.example.org/ns/Engineer', 'employees.rq (confidence 100%)', 'Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer', 'Wrote 1/1 suggested repair(s) as .patch files', 'Re-run with --apply-repairs'; step 1 output has none of 'undeclared_property'; step 2 output contains 'repairs/01-rename_iri-employees.rq.patch'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_04/consistency
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_04/consistency/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_04/consistency/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]

$ python scripts/list_files.py work/C12_04/consistency
    1,274  consistency.txt
      419  repairs/01-rename_iri-employees.rq.patch
2 files, 1,693 bytes
[exit 0]
```

</details>

---

<a id="c12-05"></a>
### C12.05 — The tombstone is read in both directions; isReplacedBy in one

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-05) · [plain edition](../docs/12-release-and-change.md#123-the-migration-annotation-and-a-correction-about-its-direction)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | `acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer` | **57%**, below a 0.7 apply threshold |

**Commands** (from the `evidence/` folder):

```bash
python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/equivalent-reversed
python scripts/rewrite_tombstone.py work/C12_05/equivalent-reversed/acme-org-v2.ttl equivalent-reversed
ontology-quality-suite consistency --new work/C12_05/equivalent-reversed/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/equivalent-reversed-out
python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/replaced-by
python scripts/rewrite_tombstone.py work/C12_05/replaced-by/acme-org-v2.ttl replaced-by
ontology-quality-suite consistency --new work/C12_05/replaced-by/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/replaced-by-out
python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/replaced-by-reversed
python scripts/rewrite_tombstone.py work/C12_05/replaced-by-reversed/acme-org-v2.ttl replaced-by-reversed
ontology-quality-suite consistency --new work/C12_05/replaced-by-reversed/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/replaced-by-reversed-out
```

<details><summary><code>scripts/rewrite_tombstone.py</code></summary>

```python
"""Rewrite the migration tombstone in a copy of acme-org-v2.ttl.

    python scripts/rewrite_tombstone.py work/X/acme/acme-org-v2.ttl MODE

MODE is one of:
  equivalent-reversed   acme:SoftwareEngineer owl:equivalentClass acme:Engineer .
  replaced-by           acme:Engineer dcterms:isReplacedBy acme:SoftwareEngineer .
  replaced-by-reversed  acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer .

The fixture asserts `acme:Engineer owl:equivalentClass acme:SoftwareEngineer .`
(from the retiring IRI). Only that one line is changed.
"""
import sys
from pathlib import Path

ORIGINAL = "acme:Engineer owl:equivalentClass acme:SoftwareEngineer ."
DC = "@prefix dcterms: <http://purl.org/dc/terms/> .\n"
MODES = {
    "equivalent-reversed": "acme:SoftwareEngineer owl:equivalentClass acme:Engineer .",
    "replaced-by": DC + "acme:Engineer dcterms:isReplacedBy acme:SoftwareEngineer .",
    "replaced-by-reversed": DC + "acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer .",
}
path, mode = Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
lines = text.split("\n")
hits = [i for i, l in enumerate(lines) if l.strip() == ORIGINAL]
if len(hits) != 1:
    sys.exit(f"expected exactly one tombstone line, found {len(hits)}")
lines[hits[0]] = MODES[mode]
path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(f"line {hits[0] + 1} now reads: {MODES[mode].splitlines()[-1]}")
```

</details>

**What is checked:** equivalentClass reversed: 100%; dcterms:isReplacedBy from the old term: 100%; reversed: 57%. The fixture's own direction is C12.04 (100%)

**Recorded result:** PASS — step 3 output contains 'employees.rq (confidence 100%)'; step 6 output contains 'employees.rq (confidence 100%)'; step 9 output contains 'employees.rq (confidence 57%)'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/equivalent-reversed
copied fixtures/acme_robotics -> work/C12_05/equivalent-reversed
[exit 0]

$ python scripts/rewrite_tombstone.py work/C12_05/equivalent-reversed/acme-org-v2.ttl equivalent-reversed
line 71 now reads: acme:SoftwareEngineer owl:equivalentClass acme:Engineer .
[exit 0]

$ ontology-quality-suite consistency --new work/C12_05/equivalent-reversed/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/equivalent-reversed-out
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> work/C12_05/equivalent-reversed/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_05/equivalent-reversed-out/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_05/equivalent-reversed-out/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]

$ python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/replaced-by
copied fixtures/acme_robotics -> work/C12_05/replaced-by
[exit 0]

$ python scripts/rewrite_tombstone.py work/C12_05/replaced-by/acme-org-v2.ttl replaced-by
line 71 now reads: acme:Engineer dcterms:isReplacedBy acme:SoftwareEngineer .
[exit 0]

$ ontology-quality-suite consistency --new work/C12_05/replaced-by/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/replaced-by-out
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> work/C12_05/replaced-by/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_05/replaced-by-out/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_05/replaced-by-out/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]

$ python scripts/copy_tree.py fixtures/acme_robotics work/C12_05/replaced-by-reversed
copied fixtures/acme_robotics -> work/C12_05/replaced-by-reversed
[exit 0]

$ python scripts/rewrite_tombstone.py work/C12_05/replaced-by-reversed/acme-org-v2.ttl replaced-by-reversed
line 71 now reads: acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer .
[exit 0]

$ ontology-quality-suite consistency --new work/C12_05/replaced-by-reversed/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_05/replaced-by-reversed-out
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> work/C12_05/replaced-by-reversed/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 57%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_05/replaced-by-reversed-out/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_05/replaced-by-reversed-out/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]
```

</details>

---

<a id="c12-06"></a>
### C12.06 — Symmetric since suite 0.3.5, 12 August 2026

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-06) · [plain edition](../docs/12-release-and-change.md#123-the-migration-annotation-and-a-correction-about-its-direction)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **It is not true, and has not been since suite 0.3.5, released on 12 August

**Sources:**

- [suite commit 67513c4, 12 August 2026](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/67513c4ebd1cba9d2a67d204b363606bbb942650): “symmetric-direction rename-migration annotations” (quote found, checked 2026-10-22)
- [suite versioning/rename_detection.py](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/ontology_suite/versioning/rename_detection.py#L25-L30): “``dcterms:isReplacedBy`` is directional by definition and only recognized old -> new” (quote found, checked 2026-10-22)

---

<a id="c12-07"></a>
### C12.07 — The reversed equivalentClass at 100%

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-07) · [plain edition](../docs/12-release-and-change.md#123-the-migration-annotation-and-a-correction-about-its-direction)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> from. Verified again for this edition on the acme fixture, with the triple

**Evidence:** the same as [C12.05 — The tombstone is read in both directions; isReplacedBy in one](#c12-05), which reproduces it: step 3 output contains 'employees.rq (confidence 100%)'; step 6 output contains 'employees.rq (confidence 100%)'; step 9 output contains 'employees.rq (confidence 57%)'

---

<a id="c12-08"></a>
### C12.08 — --apply-repairs changes the one code line on line 14

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-08) · [plain edition](../docs/12-release-and-change.md#it-used-to-mangle-comments-and-the-fix-is-instructive)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> outside comments only**: re-verified for this edition, the diff of the repaired

**Commands** (from the `evidence/` folder):

```bash
python scripts/copy_tree.py fixtures/acme_robotics work/C12_08/acme
ontology-quality-suite consistency --new work/C12_08/acme/acme-org-v2.ttl --old work/C12_08/acme/acme-org-v1.ttl --queries work/C12_08/acme --import-dir work/C12_08/acme --apply-repairs --min-confidence 0.7 --out-dir work/C12_08/out
python scripts/diff_files.py fixtures/acme_robotics/employees.rq work/C12_08/acme/employees.rq
```

**What is checked:** the repair applies at 0.7; the diff is one hunk, line 14, the code line; the comment naming acme:Engineer is untouched

**Recorded result:** PASS — step 2 output contains 'Applied 1/1 suggested repair(s) directly to their target files (confidence >= 70%).'; step 3 output contains '@@ -14 +14 @@', '-  ?employee a acme:Employee, acme:Engineer ;', '+  ?employee a acme:Employee, acme:SoftwareEngineer ;'; and that is the only hunk

<details><summary>Output, as recorded</summary>

```text
$ python scripts/copy_tree.py fixtures/acme_robotics work/C12_08/acme
copied fixtures/acme_robotics -> work/C12_08/acme
[exit 0]

$ ontology-quality-suite consistency --new work/C12_08/acme/acme-org-v2.ttl --old work/C12_08/acme/acme-org-v1.ttl --queries work/C12_08/acme --import-dir work/C12_08/acme --apply-repairs --min-confidence 0.7 --out-dir work/C12_08/out
Ontology version diff: work/C12_08/acme/acme-org-v1.ttl -> work/C12_08/acme/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] work/C12_08/acme/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_08/out/consistency.txt
Applied 1/1 suggested repair(s) directly to their target files (confidence >= 70%).
[exit 0]

$ python scripts/diff_files.py fixtures/acme_robotics/employees.rq work/C12_08/acme/employees.rq
--- fixtures/acme_robotics/employees.rq
+++ work/C12_08/acme/employees.rq
@@ -14 +14 @@
-  ?employee a acme:Employee, acme:Engineer ;
+  ?employee a acme:Employee, acme:SoftwareEngineer ;
[exit 0]
```

</details>

---

<a id="c12-09"></a>
### C12.09 — Comments used to be rewritten too

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-09) · [plain edition](../docs/12-release-and-change.md#it-used-to-mangle-comments-and-the-fix-is-instructive)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> The repair was once a textual substitution across the whole file, comments

**Sources:**

- [suite commit 64e300a (first released in v0.14.1)](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/64e300a1c42f4822ab17018438c7cda327b938cf): “`--apply-repairs` rewrote comments as well as code.” (quote found, checked 2026-10-22)

---

<a id="c12-10"></a>
### C12.10 — String literals are still rewritten, deliberately

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-10) · [plain edition](../docs/12-release-and-change.md#it-used-to-mangle-comments-and-the-fix-is-instructive)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The judgement underneath is worth borrowing. String **literals** are still

**Inputs:** [`data/rename-literal/employees.rq`](data/rename-literal/employees.rq)

<details><summary><code>data/rename-literal/employees.rq</code></summary>

```sparql
PREFIX acme: <https://acme.example.org/ns/>

# Every row is typed acme:Engineer, the term v2 renames. (A comment: a repair
# must leave this line alone.)
CONSTRUCT {
  ?employee a acme:Employee, acme:Engineer ;
    acme:hasRole ?role .
}
WHERE {
  BIND(IRI(CONCAT("https://acme.example.org/data/employee/", ?id)) AS ?employee)
  BIND("acme:Engineer" AS ?role)
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/copy_tree.py data/rename-literal work/C12_10/q
ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries work/C12_10/q --import-dir fixtures/acme_robotics --apply-repairs --min-confidence 0.7 --out-dir work/C12_10/out
python scripts/diff_files.py data/rename-literal/employees.rq work/C12_10/q/employees.rq
```

**What is checked:** the code line and the string literal are both rewritten; the comment is not

**Recorded result:** PASS — step 3 output contains '+  BIND("acme:SoftwareEngineer" AS ?role)', '+  ?employee a acme:Employee, acme:SoftwareEngineer ;'; step 3 output has none of '+# Every row'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/copy_tree.py data/rename-literal work/C12_10/q
copied data/rename-literal -> work/C12_10/q
[exit 0]

$ ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries work/C12_10/q --import-dir fixtures/acme_robotics --apply-repairs --min-confidence 0.7 --out-dir work/C12_10/out
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] work/C12_10/q/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_10/out/consistency.txt
Applied 1/1 suggested repair(s) directly to their target files (confidence >= 70%).
[exit 0]

$ python scripts/diff_files.py data/rename-literal/employees.rq work/C12_10/q/employees.rq
--- data/rename-literal/employees.rq
+++ work/C12_10/q/employees.rq
@@ -6 +6 @@
-  ?employee a acme:Employee, acme:Engineer ;
+  ?employee a acme:Employee, acme:SoftwareEngineer ;
@@ -11 +11 @@
-  BIND("acme:Engineer" AS ?role)
+  BIND("acme:SoftwareEngineer" AS ?role)
[exit 0]
```

</details>

**Sources:**

- [suite commit 64e300a](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/64e300a1c42f4822ab17018438c7cda327b938cf): “String literals are deliberately still rewritten: a TARQL IRI template is built out of literals” (quote found, checked 2026-10-22)

---

<a id="c12-11"></a>
### C12.11 — The same defect in the editor

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-11) · [plain edition](../docs/12-release-and-change.md#it-used-to-mangle-comments-and-the-fix-is-instructive)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **The same defect existed in the editor, and neither side knew.**

**Evidence:** the same as [C08.10 — Refactoring masks comments since 0.13.5](#c08-10) (cited from upstream).

---

<a id="c12-12"></a>
### C12.12 — pattern-consistency catches MKT only from the output data

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-12) · [plain edition](../docs/12-release-and-change.md#125-the-taxonomy-layer-pattern-consistency)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Caught**, from tarka's output just as from `oxi-gen`'s.

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C12_12/employees.ttl
ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_12/employees.ttl --out-dir work/C12_12/with
ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --out-dir work/C12_12/without
ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_12/employees.ttl --out-dir work/C12_12/nofoaf
python scripts/query_file.py fixtures/acme_robotics/taxonomy.ttl "PREFIX skos: <http://www.w3.org/2004/02/skos/core#> SELECT ?c WHERE { ?c a skos:Concept } ORDER BY ?c"
```

**What is checked:** with --output-data, MKT is reported (and the run exits 0); without it, the run is clean; without foaf.rdf, foaf:name and foaf:mbox are undeclared; the taxonomy holds ENG, QA and SALES

**Recorded result:** PASS — step 2 output contains '[undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT'; step 2 exits 0; step 3 output contains 'No modelling-pattern inconsistencies found'; step 4 output contains '[undeclared_property] http://xmlns.com/foaf/0.1/mbox', '[undeclared_property] http://xmlns.com/foaf/0.1/name'; step 5 output contains 'department/ENG', 'department/QA', 'department/SALES'; step 5 output has none of 'MKT'

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C12_12/employees.ttl

[exit 0]

$ ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_12/employees.ttl --out-dir work/C12_12/with
== taxonomy <-> output data ==
  [undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT is used as the value of https://acme.example.org/ns/worksIn in the data graph but is not declared as an individual anywhere in the given taxonomy set.
Written to: work/C12_12/with/pattern-consistency.txt
[exit 0]

$ ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --out-dir work/C12_12/without
No modelling-pattern inconsistencies found across ontology, taxonomy, transformation, or output data.
Written to: work/C12_12/without/pattern-consistency.txt
[exit 0]

$ ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_12/employees.ttl --out-dir work/C12_12/nofoaf
== ontology <-> transformation ==
2 propert(y/ies) used in TARQL but not declared in the ontology set:
  [undeclared_property] http://xmlns.com/foaf/0.1/mbox
  [undeclared_property] http://xmlns.com/foaf/0.1/name
== ontology+taxonomy <-> output data ==
  [CNF-002] Property http://xmlns.com/foaf/0.1/mbox is used in the output-data graph but is never declared as a property in the ontology.
  [CNF-002] Property http://xmlns.com/foaf/0.1/name is used in the output-data graph but is never declared as a property in the ontology.
== taxonomy <-> output data ==
  [undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT is used as the value of https://acme.example.org/ns/worksIn in the data graph but is not declared as an individual anywhere in the given taxonomy set.
Written to: work/C12_12/nofoaf/pattern-consistency.txt
[exit 0]

$ python scripts/query_file.py fixtures/acme_robotics/taxonomy.ttl "PREFIX skos: <http://www.w3.org/2004/02/skos/core#> SELECT ?c WHERE { ?c a skos:Concept } ORDER BY ?c"
c
https://acme.example.org/data/department/ENG
https://acme.example.org/data/department/QA
https://acme.example.org/data/department/SALES
[exit 0]
```

</details>

---

<a id="c12-13"></a>
### C12.13 — Omit --output-data and it reports clean

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-13) · [plain edition](../docs/12-release-and-change.md#125-the-taxonomy-layer-pattern-consistency)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Omit `--output-data` and this run reports clean: correctly, and uselessly.

**Evidence:** the same as [C12.12 — pattern-consistency catches MKT only from the output data](#c12-12), which reproduces it: step 2 output contains '[undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT'; step 2 exits 0; step 3 output contains 'No modelling-pattern inconsistencies found'; step 4 output contains '[undeclared_property] http://xmlns.com/foaf/0.1/mbox', '[undeclared_property] http://xmlns.com/foaf/0.1/name'; step 5 output contains 'department/ENG', 'department/QA', 'department/SALES'; step 5 output has none of 'MKT'

---

<a id="c12-14"></a>
### C12.14 — Both consistency commands are report-only by default

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-14) · [plain edition](../docs/12-release-and-change.md#126-governance-what-the-tooling-does-and-does-not-do)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Look at the flags before you copy the commands into a pipeline.

**Commands** (from the `evidence/` folder):

```bash
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C12_14/employees.ttl
ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_14/employees.ttl --out-dir work/C12_14/a
ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_14/employees.ttl --out-dir work/C12_14/b --fail-on-anything
ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_14/c
ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_14/d --fail-on-anything
```

**What is checked:** each command exits 0 on its findings, and 1 with --fail-on-anything (which from 0.24.0 is the one name on both; --fail-on-anything and --fail-on-anything remain as aliases)

**Recorded result:** PASS — step 2 exits 0; step 3 exits 1; step 4 exits 0; step 5 exits 1

<details><summary>Output, as recorded</summary>

```text
$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv -o work/C12_14/employees.ttl

[exit 0]

$ ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_14/employees.ttl --out-dir work/C12_14/a
== taxonomy <-> output data ==
  [undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT is used as the value of https://acme.example.org/ns/worksIn in the data graph but is not declared as an individual anywhere in the given taxonomy set.
Written to: work/C12_14/a/pattern-consistency.txt
[exit 0]

$ ontology-quality-suite pattern-consistency --queries fixtures/acme_robotics --ontology fixtures/acme_robotics/acme-org-v1.ttl --ontology fixtures/acme_robotics/reference_vocab/foaf.rdf --taxonomy fixtures/acme_robotics/taxonomy.ttl --output-data work/C12_14/employees.ttl --out-dir work/C12_14/b --fail-on-anything
== taxonomy <-> output data ==
  [undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT is used as the value of https://acme.example.org/ns/worksIn in the data graph but is not declared as an individual anywhere in the given taxonomy set.
Written to: work/C12_14/b/pattern-consistency.txt
[exit 1]

$ ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_14/c
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_14/c/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_14/c/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 0]

$ ontology-quality-suite consistency --new fixtures/acme_robotics/acme-org-v2.ttl --old fixtures/acme_robotics/acme-org-v1.ttl --queries fixtures/acme_robotics --import-dir fixtures/acme_robotics --out-dir work/C12_14/d --fail-on-anything
Ontology version diff: fixtures/acme_robotics/acme-org-v1.ttl -> fixtures/acme_robotics/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] fixtures/acme_robotics/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C12_14/d/consistency.txt
Wrote 1/1 suggested repair(s) as .patch files under work/C12_14/d/repairs (confidence >= 50%). Re-run with --apply-repairs to apply them directly.
[exit 1]
```

</details>

---

<a id="c12-15"></a>
### C12.15 — The approval workflow is not implemented here

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-15) · [plain edition](../docs/12-release-and-change.md#126-governance-what-the-tooling-does-and-does-not-do)  
**Kind:** Argument · **Result:** Argument

> **The approval workflow is not implemented here, and no tool should claim

A statement about scope. The evidence the table lists is reproduced in C09.04, C12.01, C12.04, C12.08 and C12.12.

---

<a id="c12-16"></a>
### C12.16 — UPDATING.md as a governance playbook

**In the manual:** [Chapter 12, at the claim](manual/docs/12-release-and-change.md#ev-c12-16) · [plain edition](../docs/12-release-and-change.md#126-governance-what-the-tooling-does-and-does-not-do)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> suite's own `UPDATING.md` is the closest existing document to a governance

**Sources:**

- [suite docs/UPDATING.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/UPDATING.md#L1): “Updating the semantic specification ecosystem: a playbook” (quote found, checked 2026-10-22)

---

<a id="chapter-13"></a>
## 13. Operate and consume

Annotated chapter: [manual/docs/13-operate-and-consume.md](manual/docs/13-operate-and-consume.md) · plain chapter: [../docs/13-operate-and-consume.md](../docs/13-operate-and-consume.md)

<a id="c13-01"></a>
### C13.01 — consistency-remote against holos-server; the imports rule applies in the store

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-01) · [plain edition](../docs/13-operate-and-consume.md#the-manifest-is-the-interesting-part)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> will be reported as undeclared. Load the imports into a graph the manifest lists.

**Inputs:** [`data/remote/graphs-v1.json`](data/remote/graphs-v1.json)

<details><summary><code>data/remote/graphs-v1.json</code></summary>

```json
{
  "graphs": [
    {
      "graph_uri": "https://acme.example.org/graph/ontology/1.0.0",
      "role": "ontology"
    },
    {
      "graph_uri": "https://acme.example.org/graph/triplified/employees",
      "role": "triplified_data",
      "source_tarql": "fixtures/acme_robotics/employees.rq",
      "ontology_graph_uri": "https://acme.example.org/graph/ontology/1.0.0",
      "notes": "loaded by tarka --post"
    }
  ]
}
```

</details>

Started first, and stopped afterwards:

```bash
holos-server --listen 127.0.0.1:7899 --no-ui
```

**Commands** (from the `evidence/` folder):

```bash
python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/1.0.0 fixtures/acme_robotics/acme-org-v1.ttl
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees
python scripts/endpoint_stats.py http://127.0.0.1:7899/query
ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v1.json --out-dir work/C13_01/own-only --fail-on-anything
python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/1.0.0 fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf fixtures/acme_robotics/reference_vocab/org.ttl
ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v1.json --out-dir work/C13_01/with-imports --fail-on-anything
```

**What is checked:** with only Acme's own file in the ontology graph, the two FOAF properties are undeclared and the run exits 1; with FOAF and org: loaded into the same graph, it is clean and exits 0

**Recorded result:** PASS — step 3 output contains 'https://acme.example.org/graph/ontology/1.0.0,52', 'https://acme.example.org/graph/triplified/employees,40'; step 4 output contains 'live data vs ontology: 0 undeclared class(es), 2 undeclared propert(y/ies)'; step 4 exits 1; step 6 output contains 'template vs ontology: clean', 'live data vs ontology: 0 undeclared class(es), 0 undeclared propert(y/ies)'; step 6 exits 0

<details><summary>Output, as recorded</summary>

```text
$ python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/1.0.0 fixtures/acme_robotics/acme-org-v1.ttl
PUT acme-org-v1.ttl -> <https://acme.example.org/graph/ontology/1.0.0>: HTTP 201
[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees

[exit 0]

$ python scripts/endpoint_stats.py http://127.0.0.1:7899/query
g,triples
https://acme.example.org/graph/ontology/1.0.0,52
https://acme.example.org/graph/triplified/employees,40
[exit 0]

$ ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v1.json --out-dir work/C13_01/own-only --fail-on-anything
=== https://acme.example.org/graph/triplified/employees ===
  source_tarql: fixtures/acme_robotics/employees.rq
  ontology_graph_uri: https://acme.example.org/graph/ontology/1.0.0
  template vs ontology: 2 undeclared term(s)
  live data vs ontology: 0 undeclared class(es), 2 undeclared propert(y/ies)
  template vs live data: 0 discrepanc(y/ies) {'classes_only_in_template': [], 'classes_only_in_live_data': [], 'properties_only_in_template': [], 'properties_only_in_live_data': []}
Reports written to: ./work/C13_01/own-only
[exit 1]

$ python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/1.0.0 fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf fixtures/acme_robotics/reference_vocab/org.ttl
PUT acme-org-v1.ttl -> <https://acme.example.org/graph/ontology/1.0.0>: HTTP 204
POST foaf.rdf -> <https://acme.example.org/graph/ontology/1.0.0>: HTTP 204
POST org.ttl -> <https://acme.example.org/graph/ontology/1.0.0>: HTTP 204
[exit 0]

$ ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v1.json --out-dir work/C13_01/with-imports --fail-on-anything
=== https://acme.example.org/graph/triplified/employees ===
  source_tarql: fixtures/acme_robotics/employees.rq
  ontology_graph_uri: https://acme.example.org/graph/ontology/1.0.0
  template vs ontology: clean
  live data vs ontology: 0 undeclared class(es), 0 undeclared propert(y/ies)
  template vs live data: 0 discrepanc(y/ies) {'classes_only_in_template': [], 'classes_only_in_live_data': [], 'properties_only_in_template': [], 'properties_only_in_live_data': []}
Reports written to: ./work/C13_01/with-imports
[exit 0]
```

</details>

---

<a id="c13-02"></a>
### C13.02 — The manifest, as JSON or built in Python; the flags

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-02) · [plain edition](../docs/13-operate-and-consume.md#the-manifest-is-the-interesting-part)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Or build it in Python, which is worth doing if the URIs come from somewhere

**Commands** (from the `evidence/` folder):

```bash
python scripts/build_manifest.py work/C13_02/graphs.json
ontology-quality-suite consistency-remote --help
```

<details><summary><code>scripts/build_manifest.py</code></summary>

```python
"""Chapter 13 §13.1: build a live-store manifest in Python, as the manual shows.

    python scripts/build_manifest.py work/C13_02/graphs.json

Runs the manual's snippet unchanged apart from the output path, then prints the
file it wrote, which is the JSON form the manual gives above the snippet.
"""
import sys
from pathlib import Path

from ontology_suite.remote.manifest import GraphBinding, GraphManifest

sys.stdout.reconfigure(encoding="utf-8")
out = sys.argv[1]
Path(out).parent.mkdir(parents=True, exist_ok=True)

GraphManifest(bindings=[
    GraphBinding(graph_uri="https://acme.example.org/graph/ontology/2.0.0",
                 role="ontology"),
    GraphBinding(graph_uri="https://acme.example.org/graph/triplified/employees",
                 role="triplified_data",
                 source_tarql="queries/employees.rq",
                 ontology_graph_uri="https://acme.example.org/graph/ontology/2.0.0"),
]).save(out)

print(Path(out).read_text(encoding="utf-8"))
```

</details>

**What is checked:** the manual's Python snippet writes the manifest it describes; consistency-remote offers --auth-user, --auth-password, --sample-limit and --fail-on-anything -- and still advertises --fail-on-misalignment, so a CI config written against 0.23.0 keeps working

**Recorded result:** PASS — step 1 output contains '"role": "triplified_data"', '"source_tarql": "queries/employees.rq"', '"ontology_graph_uri": "https://acme.example.org/graph/ontology/2.0.0"'; step 2 output contains '--auth-user', '--auth-password', '--sample-limit', '--fail-on-anything', '--fail-on-misalignment'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/build_manifest.py work/C13_02/graphs.json
{
  "graphs": [
    {
      "graph_uri": "https://acme.example.org/graph/ontology/2.0.0",
      "role": "ontology",
      "source_tarql": null,
      "ontology_graph_uri": null,
      "notes": null
    },
    {
      "graph_uri": "https://acme.example.org/graph/triplified/employees",
      "role": "triplified_data",
      "source_tarql": "queries/employees.rq",
      "ontology_graph_uri": "https://acme.example.org/graph/ontology/2.0.0",
      "notes": null
    }
  ]
}
[exit 0]

$ ontology-quality-suite consistency-remote --help
usage: ontology-quality-suite consistency-remote [-h] --query-endpoint
                                                 QUERY_ENDPOINT
                                                 [--update-endpoint UPDATE_ENDPOINT]
                                                 [--auth-user AUTH_USER]
                                                 [--auth-password AUTH_PASSWORD]
                                                 --manifest MANIFEST
                                                 [--sample-limit SAMPLE_LIMIT]
                                                 [--out-dir OUT_DIR]
                                                 [--fail-on-anything]
options:
  -h, --help            show this help message and exit
  --query-endpoint QUERY_ENDPOINT
                        the dataset's SPARQL query service URL
  --update-endpoint UPDATE_ENDPOINT
                        the dataset's SPARQL update service URL (only needed
                        to apply repairs remotely)
  --auth-user AUTH_USER
  --auth-password AUTH_PASSWORD
  --manifest MANIFEST   a remote.manifest.GraphManifest JSON file binding
                        named graphs to their role/tarql source/ontology graph
  --sample-limit SAMPLE_LIMIT
                        cap how many triples are pulled per named graph (see
                        remote.fuseki.load_named_graph)
  --out-dir OUT_DIR
  --fail-on-anything, --fail-on-misalignment
                        exit non-zero if any misalignment was found (--fail-
                        on-misalignment is the older spelling)
[exit 0]
```

</details>

---

<a id="c13-03"></a>
### C13.03 — The store a version behind: --fail-on-anything exits 1

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-03) · [plain edition](../docs/13-operate-and-consume.md#the-manifest-is-the-interesting-part)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> That structure enables a genuine **three-way check**: the live data graph, the

**Inputs:** [`data/remote/graphs-v2-store-behind.json`](data/remote/graphs-v2-store-behind.json)

<details><summary><code>data/remote/graphs-v2-store-behind.json</code></summary>

```json
{
  "graphs": [
    {
      "graph_uri": "https://acme.example.org/graph/ontology/2.0.0",
      "role": "ontology"
    },
    {
      "graph_uri": "https://acme.example.org/graph/triplified/employees",
      "role": "triplified_data",
      "source_tarql": "work/C13_03/repaired/employees.rq",
      "ontology_graph_uri": "https://acme.example.org/graph/ontology/2.0.0",
      "notes": "the query was repaired for v2; the store still holds the v1-era data"
    }
  ]
}
```

</details>

Started first, and stopped afterwards:

```bash
holos-server --listen 127.0.0.1:7899 --no-ui
```

**Commands** (from the `evidence/` folder):

```bash
# the ontology graph is at v2
python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/2.0.0 fixtures/acme_robotics/acme-org-v2.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf fixtures/acme_robotics/reference_vocab/org.ttl
# the data graph is still the v1-era load
tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees
# the query, repaired for v2
python scripts/copy_tree.py fixtures/acme_robotics work/C13_03/repaired
ontology-quality-suite consistency --new work/C13_03/repaired/acme-org-v2.ttl --old work/C13_03/repaired/acme-org-v1.ttl --queries work/C13_03/repaired --import-dir work/C13_03/repaired --apply-repairs --min-confidence 0.7 --out-dir work/C13_03/repair
ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v2-store-behind.json --out-dir work/C13_03/remote --fail-on-anything
ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-role-typo.json --out-dir work/C13_03/typo --fail-on-anything
```

**What is checked:** the repaired query agrees with the v2 ontology, the live data does not (Engineer only in the store, SoftwareEngineer only in the template), and the run exits 1. With the role misspelt: up to 0.23.0 the same run compared nothing and exited 0; 0.24.0 refuses it, naming the unknown role, but as a traceback and exit 1; from 0.24.1 as one line with no traceback and exit 2

**Recorded result:** PASS — step 5 output contains 'template vs ontology: clean', 'live data vs ontology: 1 undeclared class(es)', "'classes_only_in_template': ['https://acme.example.org/ns/SoftwareEngineer']", "'classes_only_in_live_data': ['https://acme.example.org/ns/Engineer']"; step 5 exits 1; step 6 output has none of '==='; step 6 output contains 'unknown graph role'; suite 0.24.3: step 6 exits 2; suite 0.24.3: the refusal is one line on stderr, with no traceback

<details><summary>Output, as recorded</summary>

```text
$ python scripts/gsp_put.py http://127.0.0.1:7899/graph https://acme.example.org/graph/ontology/2.0.0 fixtures/acme_robotics/acme-org-v2.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf fixtures/acme_robotics/reference_vocab/org.ttl
PUT acme-org-v2.ttl -> <https://acme.example.org/graph/ontology/2.0.0>: HTTP 201
POST foaf.rdf -> <https://acme.example.org/graph/ontology/2.0.0>: HTTP 204
POST org.ttl -> <https://acme.example.org/graph/ontology/2.0.0>: HTTP 204
[exit 0]

$ tarka run -q fixtures/acme_robotics/employees.rq -i fixtures/acme_robotics/employees.csv --post http://127.0.0.1:7899/graph --graph https://acme.example.org/graph/triplified/employees

[exit 0]

$ python scripts/copy_tree.py fixtures/acme_robotics work/C13_03/repaired
copied fixtures/acme_robotics -> work/C13_03/repaired
[exit 0]

$ ontology-quality-suite consistency --new work/C13_03/repaired/acme-org-v2.ttl --old work/C13_03/repaired/acme-org-v1.ttl --queries work/C13_03/repaired --import-dir work/C13_03/repaired --apply-repairs --min-confidence 0.7 --out-dir work/C13_03/repair
Ontology version diff: work/C13_03/repaired/acme-org-v1.ttl -> work/C13_03/repaired/acme-org-v2.ttl
Removed classes [MAJOR]:
  - https://acme.example.org/ns/Engineer
Removed subclass edges [MAJOR]:
  - https://acme.example.org/ns/Engineer no longer rdfs:subClassOf https://acme.example.org/ns/Employee
Added classes [minor]:
  - https://acme.example.org/ns/ProductManager
  - https://acme.example.org/ns/SoftwareEngineer
Added properties [minor]:
  - https://acme.example.org/ns/hireDate
Added subclass edges [minor]:
  - https://acme.example.org/ns/ProductManager rdfs:subClassOf https://acme.example.org/ns/Employee
  - https://acme.example.org/ns/SoftwareEngineer rdfs:subClassOf https://acme.example.org/ns/Employee
Added equivalentClass axioms [minor]:
  - https://acme.example.org/ns/Engineer equivalentClass https://acme.example.org/ns/SoftwareEngineer
Suggested version bump: MAJOR
1 class(es) used in TARQL but not declared in the ontology set:
  [undeclared_class] https://acme.example.org/ns/Engineer
1 suggested repair(s):
  [rename_iri] work/C13_03/repaired/employees.rq (confidence 100%)
    Update to the renamed ontology term(s): https://acme.example.org/ns/Engineer -> https://acme.example.org/ns/SoftwareEngineer
Written to: work/C13_03/repair/consistency.txt
Applied 1/1 suggested repair(s) directly to their target files (confidence >= 70%).
[exit 0]

$ ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-v2-store-behind.json --out-dir work/C13_03/remote --fail-on-anything
=== https://acme.example.org/graph/triplified/employees ===
  source_tarql: work/C13_03/repaired/employees.rq
  ontology_graph_uri: https://acme.example.org/graph/ontology/2.0.0
  template vs ontology: clean
  live data vs ontology: 1 undeclared class(es), 0 undeclared propert(y/ies)
  template vs live data: 2 discrepanc(y/ies) {'classes_only_in_template': ['https://acme.example.org/ns/SoftwareEngineer'], 'classes_only_in_live_data': ['https://acme.example.org/ns/Engineer'], 'properties_only_in_template': [], 'properties_only_in_live_data': []}
Reports written to: ./work/C13_03/remote
[exit 1]

$ ontology-quality-suite consistency-remote --query-endpoint http://127.0.0.1:7899/query --manifest data/remote/graphs-role-typo.json --out-dir work/C13_03/typo --fail-on-anything
error: data/remote/graphs-role-typo.json: unknown graph role(s) ['triplified-data'] -- valid roles are ['ontology', 'triplified_data']. A role that matches neither is never compared, so the run would report nothing and succeed.
[exit 2]
```

</details>

---

<a id="c13-04"></a>
### C13.04 — A mistyped role is refused at load, from 0.24.0

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-04) · [plain edition](../docs/13-operate-and-consume.md#finding-out-what-your-graph-uris-actually-are)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **`role` was not validated, and a typo cost you the whole check.**

**Evidence:** the same as [C13.03 — The store a version behind: --fail-on-anything exits 1](#c13-03), which reproduces it: step 5 output contains 'template vs ontology: clean', 'live data vs ontology: 1 undeclared class(es)', "'classes_only_in_template': ['https://acme.example.org/ns/SoftwareEngineer']", "'classes_only_in_live_data': ['https://acme.example.org/ns/Engineer']"; step 5 exits 1; step 6 output has none of '==='; step 6 output contains 'unknown graph role'; suite 0.24.3: step 6 exits 2; suite 0.24.3: the refusal is one line on stderr, with no traceback

---

<a id="c13-05"></a>
### C13.05 — SHACL validation flattens named graphs

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-05) · [plain edition](../docs/13-operate-and-consume.md#named-graphs-are-a-decision-you-make-once)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **But SHACL validation itself does not see them.**

**Evidence:** the same as [C14.07 — SHACL validates the union of the named graphs](#c14-07), which reproduces it: step 1 output contains 'focus <http://example.org/bob>', 'focus <http://example.org/carol>', 'focus <http://example.org/dave>'; the TriG and the flattened file give identical reports; step 3 output has none of '--graph'

---

<a id="c13-06"></a>
### C13.06 — Policy at the scan: rows without the column, unless you are in HR

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-06) · [plain edition](../docs/13-operate-and-consume.md#132-access-policy-at-the-scan)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Here it is through the `holosdb` package from PyPI, on HOLOS's small HR example,

**Inputs:** [`data/policy/hr.trig`](data/policy/hr.trig)

<details><summary><code>data/policy/hr.trig</code></summary>

```turtle
@prefix ex:   <http://example.com/> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# The default graph: nothing sensitive.
ex:acme a ex:Company ; ex:name "Acme Ltd" .

ex:public {
    ex:alice a ex:Employee ; ex:name "Alice" ; ex:department "engineering" ; ex:salary 95000 .
    ex:bob   a ex:Employee ; ex:name "Bob"   ; ex:department "engineering" ; ex:salary 88000 .
    ex:carol a ex:Employee ; ex:name "Carol" ; ex:department "finance"     ; ex:salary 102000 .
    ex:alice ex:manages ex:bob .
}

# Classified: performance review notes.
ex:reviews {
    ex:alice ex:rating "exceeds" ; ex:reviewNote "Ready for promotion." .
    ex:bob   ex:rating "meets" .
}

# RDF 1.2: who asserted what, and when.
ex:provenance {
    ex:claim1 rdf:reifies <<( ex:carol ex:salary 102000 )>> ;
              ex:statedBy ex:payroll ;
              ex:statedOn "2026-08-01T09:00:00Z"^^xsd:dateTime .
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/holosdb_policy.py data/policy/hr.trig
```

<details><summary><code>scripts/holosdb_policy.py</code></summary>

```python
"""Chapter 13 §13.2: access policy at the index scan, through the holosdb package.

    python scripts/holosdb_policy.py data/policy/hr.trig

Runs the same few queries as different principals under different policies and
prints what each one gets back. Note the fluent API: every Policy method returns
a new policy, so the calls are chained or assigned, never made as statements.
"""
import sys

from holosdb import HolosError, Policy, Principal, Store

sys.stdout.reconfigure(encoding="utf-8")
store = Store()
store.load(sys.argv[1])

NAMES = """PREFIX ex: <http://example.com/>
SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name
                              OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name"""
COUNT = """PREFIX ex: <http://example.com/>
SELECT (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?e ex:salary ?s } }"""
GRAPHS = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g"

alice = Principal("urn:user:alice")
alice_hr = Principal("urn:user:alice", roles=["hr"])
alice_cleared = Principal("urn:user:alice", clearance=3)

deny_salary = Policy().deny_predicate("http://example.com/salary", except_role="hr")
label_reviews = Policy().label_graph("http://example.com/reviews", 3)
fail_closed = Policy().deny_predicate("http://example.com/salary").fail_closed()


def rows(q, **kw):
    return [{k: str(v) for k, v in r.to_dict().items()} for r in store.query(q, **kw)]


def show(label, q, **kw):
    try:
        print(f"{label}:")
        for r in rows(q, **kw):
            print("   ", ", ".join(f"{k}={v}" for k, v in r.items()))
    except HolosError as exc:
        print(f"    HolosError: {exc}")


show("1. names and salaries, no policy", NAMES)
show("2. salary denied except to role hr, asked by alice", NAMES, principal=alice, policy=deny_salary)
show("3. the same, asked by alice with role hr", NAMES, principal=alice_hr, policy=deny_salary)
show("4. COUNT of salaries without the role", COUNT, principal=alice, policy=deny_salary)
show("5. named graphs, reviews labelled at level 3, no clearance", GRAPHS, principal=alice, policy=label_reviews)
show("6. named graphs, with clearance 3", GRAPHS, principal=alice_cleared, policy=label_reviews)
show("7. salary denied with fail_closed()", NAMES, principal=alice, policy=fail_closed)

# The mistake the manual warns about: calling a Policy method as a statement.
p = Policy()
p.deny_predicate("http://example.com/salary")      # returns a new policy; p is unchanged
show("8. (mistake) policy method called as a statement", COUNT, principal=alice, policy=p)
```

</details>

**What is checked:** every row of the manual's table: no salaries without the role and all three with it; COUNT 0; the labelled graph absent without clearance and present with it; fail_closed raises a HolosError saying access denied by policy; and a policy method called as a statement leaves no policy (3 salaries counted)

**Recorded result:** PASS — step 1 output contains '2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None/n    name=Bob, salary=None/n    name=Carol, salary=None', '3. the same, asked by alice with role hr:\n    name=Alice, salary=95000/n    name=Bob, salary=88000/n    name=Carol, salary=102000', '4. COUNT of salaries without the role:\n    n=0', '5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance/n    g=http://example.com/public/n6.', '6. named graphs, with clearance 3:\n    g=http://example.com/provenance/n    g=http://example.com/public/n    g=http://example.com/reviews', '7. salary denied with fail_closed():\n    HolosError: ', 'access denied by policy/n8. (mistake)', '8. (mistake) policy method called as a statement:\n    n=3'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/holosdb_policy.py data/policy/hr.trig
1. names and salaries, no policy:
    name=Alice, salary=95000
    name=Bob, salary=88000
    name=Carol, salary=102000
2. salary denied except to role hr, asked by alice:
    name=Alice, salary=None
    name=Bob, salary=None
    name=Carol, salary=None
3. the same, asked by alice with role hr:
    name=Alice, salary=95000
    name=Bob, salary=88000
    name=Carol, salary=102000
4. COUNT of salaries without the role:
    n=0
5. named graphs, reviews labelled at level 3, no clearance:
    g=http://example.com/provenance
    g=http://example.com/public
6. named graphs, with clearance 3:
    g=http://example.com/provenance
    g=http://example.com/public
    g=http://example.com/reviews
7. salary denied with fail_closed():
    HolosError: query evaluation failed: access denied by policy
8. (mistake) policy method called as a statement:
    n=3
[exit 0]
```

</details>

---

<a id="c13-07"></a>
### C13.07 — The fluent API mistake

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-07) · [plain edition](../docs/13-operate-and-consume.md#132-access-policy-at-the-scan)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> fluent API: each `Policy` method returns a new policy. Calling them as statements

**Evidence:** the same as [C13.06 — Policy at the scan: rows without the column, unless you are in HR](#c13-06), which reproduces it: step 1 output contains '2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None/n    name=Bob, salary=None/n    name=Carol, salary=None', '3. the same, asked by alice with role hr:\n    name=Alice, salary=95000/n    name=Bob, salary=88000/n    name=Carol, salary=102000', '4. COUNT of salaries without the role:\n    n=0', '5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance/n    g=http://example.com/public/n6.', '6. named graphs, with clearance 3:\n    g=http://example.com/provenance/n    g=http://example.com/public/n    g=http://example.com/reviews', '7. salary denied with fail_closed():\n    HolosError: ', 'access denied by policy/n8. (mistake)', '8. (mistake) policy method called as a statement:\n    n=3'

---

<a id="c13-08"></a>
### C13.08 — The holos command gives the same answers

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-08) · [plain edition](../docs/13-operate-and-consume.md#132-access-policy-at-the-scan)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The `holos query` command from the release takes the same

**Inputs:** [`data/policy/hr.trig`](data/policy/hr.trig)

<details><summary><code>data/policy/hr.trig</code></summary>

```turtle
@prefix ex:   <http://example.com/> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# The default graph: nothing sensitive.
ex:acme a ex:Company ; ex:name "Acme Ltd" .

ex:public {
    ex:alice a ex:Employee ; ex:name "Alice" ; ex:department "engineering" ; ex:salary 95000 .
    ex:bob   a ex:Employee ; ex:name "Bob"   ; ex:department "engineering" ; ex:salary 88000 .
    ex:carol a ex:Employee ; ex:name "Carol" ; ex:department "finance"     ; ex:salary 102000 .
    ex:alice ex:manages ex:bob .
}

# Classified: performance review notes.
ex:reviews {
    ex:alice ex:rating "exceeds" ; ex:reviewNote "Ready for promotion." .
    ex:bob   ex:rating "meets" .
}

# RDF 1.2: who asserted what, and when.
ex:provenance {
    ex:claim1 rdf:reifies <<( ex:carol ex:salary 102000 )>> ;
              ex:statedBy ex:payroll ;
              ex:statedOn "2026-08-01T09:00:00Z"^^xsd:dateTime .
}
```

</details>

**Commands** (from the `evidence/` folder):

```bash
holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --except-role hr
holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --except-role hr --role hr
holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --fail-closed
holos query --data data/policy/hr.trig --query "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g" --label-graph http://example.com/reviews=3
holos query --data data/policy/hr.trig --query "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g" --label-graph http://example.com/reviews=3 --clearance 3
```

**What is checked:** the same five answers as the Python API

**Recorded result:** PASS — step 1 output has none of '95000'; step 2 output contains '95000', '88000', '102000'; step 3 exits non-zero (1); step 3 output contains 'access denied by policy'; step 4 output has none of 'http://example.com/reviews'; step 5 output contains 'http://example.com/reviews'

<details><summary>Output, as recorded</summary>

```text
$ holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --except-role hr
{"head":{"vars":["name","salary"]},"results":{"bindings":[{"name":{"type":"literal","value":"Alice"}},{"name":{"type":"literal","value":"Bob"}},{"name":{"type":"literal","value":"Carol"}}]}}
loaded 21 quads in 0.00s (27382 quads/s)
note: 3 quads withheld by policy
[exit 0]

$ holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --except-role hr --role hr
{"head":{"vars":["name","salary"]},"results":{"bindings":[{"name":{"type":"literal","value":"Alice"},"salary":{"type":"literal","value":"95000","datatype":"http://www.w3.org/2001/XMLSchema#integer"}},{"name":{"type":"literal","value":"Bob"},"salary":{"type":"literal","value":"88000","datatype":"http://www.w3.org/2001/XMLSchema#integer"}},{"name":{"type":"literal","value":"Carol"},"salary":{"type":"literal","value":"102000","datatype":"http://www.w3.org/2001/XMLSchema#integer"}}]}}
loaded 21 quads in 0.00s (30324 quads/s)
[exit 0]

$ holos query --data data/policy/hr.trig --query "PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name" --deny-predicate http://example.com/salary --fail-closed
loaded 21 quads in 0.00s (30973 quads/s)
Error: query evaluation failed: access denied by policy
Caused by:
    access denied by policy
[exit 1]

$ holos query --data data/policy/hr.trig --query "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g" --label-graph http://example.com/reviews=3
{"head":{"vars":["g"]},"results":{"bindings":[{"g":{"type":"uri","value":"http://example.com/provenance"}},{"g":{"type":"uri","value":"http://example.com/public"}}]}}
loaded 21 quads in 0.00s (17138 quads/s)
note: 3 quads withheld by policy
[exit 0]

$ holos query --data data/policy/hr.trig --query "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g" --label-graph http://example.com/reviews=3 --clearance 3
{"head":{"vars":["g"]},"results":{"bindings":[{"g":{"type":"uri","value":"http://example.com/provenance"}},{"g":{"type":"uri","value":"http://example.com/public"}},{"g":{"type":"uri","value":"http://example.com/reviews"}}]}}
loaded 21 quads in 0.00s (14899 quads/s)
[exit 0]
```

</details>

---

<a id="c13-09"></a>
### C13.09 — 8 ns per quad, by HOLOS's own measurement

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-09) · [plain edition](../docs/13-operate-and-consume.md#132-access-policy-at-the-scan)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> All verified at 0.25.0. HOLOS measures the cost at 8 ns per quad, about 1% of

**Sources:**

- [HOLOS ACCESS-CONTROL.md](https://github.com/pwin/triplestore/blob/b44aa1c508536220f1d0de4a9323cf4bbcc63563/ACCESS-CONTROL.md#L44): “It costs **8 ns per quad** — measured, and about 1% of what decoding the quad costs.” (quote found, checked 2026-10-22)

---

<a id="c13-10"></a>
### C13.10 — Validation and the store: written into it up to 0.21.0, untouched from 0.21.1

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-10) · [plain edition](../docs/13-operate-and-consume.md#132-access-policy-at-the-scan)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Two things to know before you validate a store you care about.

**Inputs:** [`data/shacl/two-unnamed.ttl`](data/shacl/two-unnamed.ttl), [`data/shacl/shapes-violation.ttl`](data/shacl/shapes-violation.ttl), [`data/shacl/shapes-sparql.ttl`](data/shacl/shapes-sparql.ttl)

<details><summary><code>data/shacl/two-unnamed.ttl</code></summary>

```turtle
# Chapter 13 §13.2: two people with no name and one with. Two violations,
# whichever validator counts them.
@prefix ex: <http://example.org/> .

ex:a a ex:Person .
ex:b a ex:Person .
ex:c a ex:Person ; ex:name "C" .
```

</details>

<details><summary><code>data/shacl/shapes-violation.ttl</code></summary>

```turtle
# Every Person needs a name. No severity is declared, so a missing name is a
# sh:Violation, the SHACL default.
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:PersonShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:property [ sh:path ex:name ; sh:minCount 1 ] .
```

</details>

<details><summary><code>data/shacl/shapes-sparql.ttl</code></summary>

```turtle
# A SPARQL-based constraint: beyond SHACL Core. HOLOS's native validator must
# refuse it rather than skip it and answer "conforms".
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:NamedShape a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:sparql [ a sh:SPARQLConstraint ;
    sh:message "Person has no name" ;
    sh:select """PREFIX ex: <http://example.org/>
                 SELECT $this WHERE { FILTER NOT EXISTS { $this ex:name ?n } }""" ] .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
python scripts/holosdb_validate.py data/shacl/two-unnamed.ttl data/shacl/shapes-violation.ttl data/shacl/shapes-sparql.ttl
python scripts/holosdb_validate_repeat.py data/shacl/two-unnamed.ttl data/shacl/shapes-violation.ttl work/C13_10/store
holos --version
holos stats --data data/shacl/two-unnamed.ttl --store work/C13_10/cli-store
holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
holos query --store work/C13_10/cli-store --query "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"
# plant what an earlier version would have left
holos update --store work/C13_10/cli-store --update "INSERT DATA { GRAPH <urn:holos:shapes> { <urn:x:s> <urn:x:p> <urn:x:o> } }"
holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
holos --help
```

<details><summary><code>scripts/holosdb_validate_repeat.py</code></summary>

```python
"""Chapter 13 §13.2: does validation leave the store as it found it?

    python scripts/holosdb_validate_repeat.py DATA SHAPES work/C13_10/store

Up to holosdb 0.21.0, Store.validate() loaded the shapes into a named graph of
the store it validated and never removed them. A shape's blank nodes are fresh
on every load, so each call added another copy and the count climbed; on a
persistent store the copies survived a restart. 0.21.1 loads them in a scope
that is always rolled back, and reports a shapes graph an earlier version left
behind, naming the DROP GRAPH that removes it, rather than reading or dropping it.

1. three calls with each engine on one in-memory store, and their counts;
2. the named graphs the store holds after one call;
3. the same on a persistent store, after reopening it;
4. a store already holding a leftover urn:holos:python:shapes graph: what the
   call warns, and whether the leftover is still there afterwards.
"""
import sys
import warnings
from importlib import metadata

from holosdb import Store

sys.stdout.reconfigure(encoding="utf-8")
data, shapes, path = sys.argv[1:4]
GRAPHS = "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g ORDER BY ?g"
LEFTOVER = "urn:holos:python:shapes"


def graphs(store):
    return [(r.to_dict()["g"], int(r.to_dict()["n"])) for r in store.query(GRAPHS)]


print(f"holosdb {metadata.version('holosdb')}")
for engine in ("adapted", "native"):
    store = Store()
    store.load(data)
    counts = [store.validate(shapes, engine=engine)["violations"] for _ in range(3)]
    print(f"1. {engine}, three calls on one store: violations {counts}")

store = Store()
store.load(data)
store.validate(shapes)
print(f"2. named graphs after one validate(): {graphs(store)}")

disk = Store(path=path)
disk.load(data)
disk.validate(shapes)
del disk
print(f"3. named graphs in the persistent store after reopening: {graphs(Store(path=path))}")

store = Store()
store.load(data)
store.update(f"INSERT DATA {{ GRAPH <{LEFTOVER}> {{ <urn:x:s> <urn:x:p> <urn:x:o> }} }}")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    result = store.validate(shapes)
said = [f"{w.category.__name__}: {w.message}" for w in caught] or ["no warning"]
print(f"4. with a leftover {LEFTOVER} graph: violations {result['violations']}; {' | '.join(said)}")
print(f"   named graphs afterwards: {graphs(store)}")
```

</details>

<details><summary><code>scripts/holosdb_validate.py</code></summary>

```python
"""Chapter 13 §13.2 and Chapter 11 §11.8: validation through holosdb.

    python scripts/holosdb_validate.py DATA SHAPES [SPARQL_SHAPES]

Store.validate() returns a dictionary, so a caller has a `conforms` key to test
rather than an exit code. Its native engine refuses a shapes graph that uses
anything beyond SHACL Core, rather than skipping the constraint.

Each validation here runs on a freshly loaded store, because up to 0.21.0
validate() wrote the shapes into the store it validated, so a second call on the
same store counted them twice (see holosdb_validate_repeat.py; fixed in 0.21.1).
"""
import sys

from holosdb import HolosError, Store

sys.stdout.reconfigure(encoding="utf-8")


def fresh() -> Store:
    store = Store()
    store.load(sys.argv[1])
    return store


print("adapted:", fresh().validate(sys.argv[2]))
print("native: ", fresh().validate(sys.argv[2], engine="native"))
if len(sys.argv) > 3:
    try:
        print("native, sh:sparql shapes:", fresh().validate(sys.argv[3], engine="native"))
    except HolosError as exc:
        print(f"native, sh:sparql shapes: HolosError: {exc}")
```

</details>

**What is checked:** on a fresh store both engines report the 2 true violations, and native refuses sh:sparql; the CLI's default engine is native. Then, by version. At 0.21.0: three calls on one store report 2, 4 and 6; one validate() leaves a 5-quad shapes graph, which survives reopening a persistent store; the CLI with --store does the same. From 0.21.1: 2, 2 and 2; no graph left, on disk or in memory; a leftover shapes graph is reported with the DROP GRAPH that removes it, by Python and by the CLI

**Recorded result:** PASS — holosdb 0.25.0, holos 0.25.0: step 1 output contains "adapted: {'conforms': False, 'violations': 2, 'engine': 'adapted', 'results': [", "native:  {'conforms': False, 'violations': 2, 'engine': 'native', 'results': [", "'focus': 'http://example.org/a'", "'focus': 'http://example.org/b'", 'HolosError: unsupported: sh:sparql is not implemented'; step 10 output contains '--engine <NAME>          adapted (default) or native'; step 2 output contains 'adapted, three calls on one store: violations [2, 2, 2]', 'native, three calls on one store: violations [2, 2, 2]', 'named graphs after one validate(): []', 'named graphs in the persistent store after reopening: []', 'store.update("DROP GRAPH <urn:holos:python:shapes>") removes them'; step 5 output contains 'results           2'; step 6 output contains 'results           2'; step 7 output has none of 'urn:holos:shapes'; step 9 output contains 'note: <urn:holos:shapes> holds 1 quads', 'DROP GRAPH <urn:holos:shapes>'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/holosdb_validate.py data/shacl/two-unnamed.ttl data/shacl/shapes-violation.ttl data/shacl/shapes-sparql.ttl
adapted: {'conforms': False, 'violations': 2, 'engine': 'adapted', 'results': [{'focus': 'http://example.org/a', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:0_b0', 'message': None}, {'focus': 'http://example.org/b', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:0_b0', 'message': None}]}
native:  {'conforms': False, 'violations': 2, 'engine': 'native', 'results': [{'focus': 'http://example.org/a', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:e61608972cdfeb94a3a2aae7d02ec445', 'message': None}, {'focus': 'http://example.org/b', 'path': 'http://example.org/name', 'value': None, 'severity': 'Violation', 'component': 'http://www.w3.org/ns/shacl#MinCountConstraintComponent', 'shape': '_:e61608972cdfeb94a3a2aae7d02ec445', 'message': None}]}
native, sh:sparql shapes: HolosError: unsupported: sh:sparql is not implemented by the incremental evaluator; validate                      through holos_shacl::engine::EngineRun instead
[exit 0]

$ python scripts/holosdb_validate_repeat.py data/shacl/two-unnamed.ttl data/shacl/shapes-violation.ttl work/C13_10/store
holosdb 0.25.0
1. adapted, three calls on one store: violations [2, 2, 2]
1. native, three calls on one store: violations [2, 2, 2]
2. named graphs after one validate(): []
3. named graphs in the persistent store after reopening: []
4. with a leftover urn:holos:python:shapes graph: violations 2; UserWarning: <urn:holos:python:shapes> holds 1 quads that an earlier Store.validate left in this store; they are not read, and store.update("DROP GRAPH <urn:holos:python:shapes>") removes them
   named graphs afterwards: [('urn:holos:python:shapes', 1)]
[exit 0]

$ holos --version
holos 0.25.0 (b44aa1c)
[exit 0]

$ holos stats --data data/shacl/two-unnamed.ttl --store work/C13_10/cli-store
quads            4
dictionary terms 5
named graphs     0
on disk          140.9 KiB
free here        88.9 GiB
room to compact  yes (needs up to 140.9 KiB)
predicates by frequency
           3  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
           1  <http://example.org/name>
loaded 4 quads in 0.26s (15 quads/s)
[exit 0]

$ holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
bridged+compiled  4 triples, 2 shapes in 0.000s
validated         0.000s
conforms          false
results           2
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 1]

$ holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
bridged+compiled  4 triples, 2 shapes in 0.000s
validated         0.000s
conforms          false
results           2
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 1]

$ holos query --store work/C13_10/cli-store --query "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"
{"head":{"vars":["g","n"]},"results":{"bindings":[]}}
[exit 0]

$ holos update --store work/C13_10/cli-store --update "INSERT DATA { GRAPH <urn:holos:shapes> { <urn:x:s> <urn:x:p> <urn:x:o> } }"
inserted 1 deleted 0 graphs +0 -0 in 0.182s
[exit 0]

$ holos validate --store work/C13_10/cli-store --shapes data/shacl/shapes-violation.ttl
bridged+compiled  4 triples, 2 shapes in 0.002s
validated         0.000s
conforms          false
results           2
note: <urn:holos:shapes> holds 1 quads that an earlier holos validate --shapes left in this store; they are not read, and `DROP GRAPH <urn:holos:shapes>` removes them
read 5 shape quads from data/shacl/shapes-violation.ttl, and kept none of them
[exit 1]

$ holos --help
holos — an RDF 1.2 store with SPARQL 1.2 and policy enforced at the scan
USAGE
    holos query    --data <FILE>... (--query <SPARQL> | --query-file <FILE>) [POLICY] [OPTIONS]
    holos update   --store <DIR> (--update <SPARQL> | --update-file <FILE>) [POLICY]
    holos stats    --data <FILE>...
    holos dump     --data <FILE>... [POLICY]
    holos validate --data <FILE>... [--shapes <FILE>]
    holos backup   --store <DIR> --to <DIR>
    holos compact  --store <DIR> --to <DIR>
    holos entail   --store <DIR> [--entail-graph <IRI>] [--entail-budget <N>]
    holos rules    --store <DIR> --rules <FILE> [--derived-graph <IRI>] [--max-derived <N>]
                   [--max-rounds <N>]
DATA
    --data <FILE>            Load a file. Repeatable. Format is taken from the extension:
                             .ttl .nt .trig .nq .rdf .jsonld .n3 — each also with .gz,
                             which is how large RDF dumps are normally distributed.
                             Decompression is streamed, so a 60 GB dump costs no more
                             memory than a small one.
    --base <IRI>             Base IRI for parsing.
    --store <DIR>            Use a persistent RocksDB store at DIR. Without this the store
                             is in memory and is discarded on exit.
    --bulk                   Buffer writes and skip the write-ahead log while loading. Much
                             faster; a load interrupted part-way must be discarded.
MAINTENANCE
    --entail-graph <IRI>     Where `entail` writes. Its own graph so it can be dropped again
                             and told apart from what was asserted. Default
                             <https://holos.dev/ns#entailed> -- an absolute IRI, because
                             `DROP GRAPH` needs the name the store actually holds.
    --entail-budget <N>      Refuse a closure larger than N new triples. Default 10,000,000.
    --force                  Run `compact` even when the headroom estimate says it will
… (81 lines omitted; full output in the outputs/ record)
                             refuses a shapes graph using anything beyond Core rather than
                             dropping the constraint and reporting conformance. Both pass
                             every W3C SHACL Core test.
                             Exit status, as the `shacl` CLI's: 0 the data conforms, 1 it
                             does not, 2 validation could not run -- including a shapes
                             graph the chosen engine refuses.
OPTIONS
    -h, --help               This text.
[exit 0]
```

</details>

**Sources:**

- [HOLOS commit cd5af4b](https://github.com/pwin/triplestore/commit/cd5af4b32082458ee087d92948020a1b77cd3e9d): “Engine::with_transient_graph loads input inside a commit scope that is always rolled back” (quote found, checked 2026-10-22)
- [HOLOS commit 82e4d66, 'Cut 0.21.1'](https://github.com/pwin/triplestore/commit/82e4d6686b3563db502ea68098a6f3fc9ce75d6b): “validation leaves nothing in the store it validates” (quote found, checked 2026-10-22)

The recorded run uses 0.25.0, so it shows the fix made in 0.21.1, and the results the dictionary carries from 0.23.0. The same steps against the published 0.21.0 gave: `violations [2, 4, 6]` for both engines; a 5-quad `urn:holos:python:shapes` graph after one call, still there after reopening a persistent store; no warning for a planted leftover; and from the CLI `results 2`, then `results 4`, with a `urn:holos:shapes` graph left behind. The Python method's default engine, adapted, is in its signature: [holos-python lib.rs](https://github.com/pwin/triplestore/blob/b44aa1c508536220f1d0de4a9323cf4bbcc63563/crates/holos-python/src/lib.rs#L647-L674).

---

<a id="c13-11"></a>
### C13.11 — docgen: 4 classes, 5 external terms, 3 resolved

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-11) · [plain edition](../docs/13-operate-and-consume.md#133-documentation-as-a-product-docgen)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> 2 object properties, 3 datatype properties, 1 sections,

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_11/docs
python scripts/list_files.py work/C13_11/docs
```

**What is checked:** the summary line as quoted; the HTML page, the JSON and the per-class diagrams are written

**Recorded result:** PASS — step 1 output contains "prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved)."; step 2 output contains 'ontology-documentation.html', 'ontology_doc_data.json', 'class-diagrams/'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_11/docs
Wrote work/C13_11/docs/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_11/docs/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_11/docs/ontology-documentation.html
4 class diagram(s) written to: work/C13_11/docs/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ python scripts/list_files.py work/C13_11/docs
    1,262  class-diagrams/Contractor.dot
   15,826  class-diagrams/Contractor.png
    4,741  class-diagrams/Contractor.svg
      384  class-diagrams/Contractor.ttl
    1,126  class-diagrams/Department.dot
   13,233  class-diagrams/Department.png
    4,101  class-diagrams/Department.svg
      396  class-diagrams/Department.ttl
      978  class-diagrams/Employee.dot
   11,778  class-diagrams/Employee.png
    3,694  class-diagrams/Employee.svg
      351  class-diagrams/Employee.ttl
    1,155  class-diagrams/Engineer.dot
   13,781  class-diagrams/Engineer.png
    4,197  class-diagrams/Engineer.svg
      363  class-diagrams/Engineer.ttl
   61,359  ontology-documentation.html
    5,923  ontology_doc_data.json
18 files, 144,648 bytes
[exit 0]
```

</details>

---

<a id="c13-12"></a>
### C13.12 — Three runs, three pages; pinned, one

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-12) · [plain edition](../docs/13-operate-and-consume.md#still-open-the-page-is-reshuffled-on-every-run)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Re-checked at 0.24.1: three identical runs, three different files.

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run1
ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run2
ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run3
PYTHONHASHSEED=0 ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/seed0-a
PYTHONHASHSEED=0 ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/seed0-b
python scripts/sha256.py work/C13_12/run1/ontology-documentation.html work/C13_12/run2/ontology-documentation.html work/C13_12/run3/ontology-documentation.html work/C13_12/seed0-a/ontology-documentation.html work/C13_12/seed0-b/ontology-documentation.html
```

**What is checked:** the three unpinned runs give at least two different pages (each run draws its own hash seed, so three matching by chance is possible but unlikely); the two pinned runs give the same page

**Recorded result:** PASS — three unpinned runs gave 3 different pages; two runs with PYTHONHASHSEED=0 gave the same page

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run1
Wrote work/C13_12/run1/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_12/run1/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_12/run1/ontology-documentation.html
4 class diagram(s) written to: work/C13_12/run1/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run2
Wrote work/C13_12/run2/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_12/run2/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_12/run2/ontology-documentation.html
4 class diagram(s) written to: work/C13_12/run2/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/run3
Wrote work/C13_12/run3/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_12/run3/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_12/run3/ontology-documentation.html
4 class diagram(s) written to: work/C13_12/run3/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/seed0-a
Wrote work/C13_12/seed0-a/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_12/seed0-a/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_12/seed0-a/ontology-documentation.html
4 class diagram(s) written to: work/C13_12/seed0-a/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ ontology-quality-suite docgen --ontology fixtures/acme_robotics/acme-org-v1.ttl --ref fixtures/acme_robotics/reference_vocab/org.ttl --ref fixtures/acme_robotics/reference_vocab/foaf.rdf --out-dir work/C13_12/seed0-b
Wrote work/C13_12/seed0-b/ontology_doc_data.json: prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, 5 external terms (3 resolved).
Wrote work/C13_12/seed0-b/ontology-documentation.html (4 classes, 2 object properties, 3 datatype properties, 5 external terms).
Reference documentation written to: work/C13_12/seed0-b/ontology-documentation.html
4 class diagram(s) written to: work/C13_12/seed0-b/class-diagrams
NOTE: 2 external term(s) referenced with no --ref file resolving a definition:
  - skos:ConceptScheme
  - skos:inScheme
[exit 0]

$ python scripts/sha256.py work/C13_12/run1/ontology-documentation.html work/C13_12/run2/ontology-documentation.html work/C13_12/run3/ontology-documentation.html work/C13_12/seed0-a/ontology-documentation.html work/C13_12/seed0-b/ontology-documentation.html
b7826f89bd7c84c1 work/C13_12/run1/ontology-documentation.html
7d814776706bd6f1 work/C13_12/run2/ontology-documentation.html
a3efe6505f47efe9 work/C13_12/run3/ontology-documentation.html
4b065806e5fca839 work/C13_12/seed0-a/ontology-documentation.html
4b065806e5fca839 work/C13_12/seed0-b/ontology-documentation.html
[exit 0]
```

</details>

**Sources:**

- [suite issue #3](https://github.com/pwin/consolidated-ontology-quality-suite-python/issues/3)

---

<a id="c13-13"></a>
### C13.13 — Every row carries source_file and line

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-13) · [plain edition](../docs/13-operate-and-consume.md#134-observability-not-covered)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> > **Every check run writes `full_results.csv`. Retain them, timestamped.**

**Evidence:** the same as [C09.10 — Which reports a run writes, and --reports minimal](#c09-10), which reproduces it: default run writes findings.txt, full_results.csv, cucumber.json, report.html; and features/ and plots/; and none of the six retired summary files; --reports minimal writes exactly findings.txt and full_results.csv; full_results.csv has source_file and line columns

---

<a id="c13-14"></a>
### C13.14 — HOLOS: embeddable, RDF 1.2, GeoSPARQL

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-14) · [plain edition](../docs/13-operate-and-consume.md#135-knowledge-products-and-apis-not-covered)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | Python · JS | HOLOS (`holosdb`, `holos-wasm`) | Policy at the scan, RDF 1.2, GeoSPARQL; early |

**Commands** (from the `evidence/` folder):

```bash
python scripts/holos_facts.py
```

<details><summary><code>scripts/holos_facts.py</code></summary>

```python
"""Chapter 13: two facts about the holosdb wheel.

    python scripts/holos_facts.py

How many GeoSPARQL functions this build registers, and whether the wheel
carries RocksDB persistence.
"""
import sys

import holosdb

sys.stdout.reconfigure(encoding="utf-8")
fns = holosdb.geosparql_functions()
print(f"GeoSPARQL functions registered: {len(fns)}")
print(f"includes geof:buffer and geof:boundary: "
      f"{any(f.endswith('buffer') for f in fns)} / {any(f.endswith('boundary') for f in fns)}")
print(f"persistence (RocksDB) in this wheel: {holosdb.has_rocksdb()}")
```

</details>

**What is checked:** the holosdb wheel registers 49 GeoSPARQL functions

**Recorded result:** PASS — step 1 output contains 'GeoSPARQL functions registered: 49', 'includes geof:buffer and geof:boundary: True / True'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/holos_facts.py
GeoSPARQL functions registered: 49
includes geof:buffer and geof:boundary: True / True
persistence (RocksDB) in this wheel: True
[exit 0]
```

</details>

---

<a id="c13-15"></a>
### C13.15 — The editor's checks run on holos-wasm-node

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-15) · [plain edition](../docs/13-operate-and-consume.md#135-knowledge-products-and-apis-not-covered)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> HOLOS appears in the editor too: the VS Code extension's checks run on

**Evidence:** the same as [C07.04 — The editor runs the same engines at the same versions](#c07-04) (cited from upstream).

---

<a id="c13-16"></a>
### C13.16 — Observability and APIs are not covered

**In the manual:** [Chapter 13, at the claim](manual/docs/13-operate-and-consume.md#ev-c13-16) · [plain edition](../docs/13-operate-and-consume.md#134-observability-not-covered)  
**Kind:** Argument · **Result:** Argument

> **None of this is in the toolchain.**

A statement of scope, checkable by its absence: no subcommand of the suite, and no command in the other releases, exports metrics or serves an API other than the SPARQL and Graph Store protocols of holos-server (C10.15, C13.01).

---

<a id="chapter-14"></a>
## 14. Coverage and gaps

Annotated chapter: [manual/docs/14-coverage-and-gaps.md](manual/docs/14-coverage-and-gaps.md) · plain chapter: [../docs/14-coverage-and-gaps.md](../docs/14-coverage-and-gaps.md)

<a id="c14-01"></a>
### C14.01 — A scoped run could not see that the reasoner did not run (fixed in 0.24.0)

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-01) · [plain edition](../docs/14-coverage-and-gaps.md#a-scoped-run-could-not-see-that-the-reasoner-did-not-run-fixed-in-0240)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> ### A scoped run could not see that the reasoner did not run (fixed in 0.24.0)

**Evidence:** the same as [C09.09 — A scoped run keeps the 'reasoner did not run' finding, from 0.24.0](#c09-09), which reproduces it: unscoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; scoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; step 2: 548 findings (65 V, 363 W, 120 I); step 3: 54 findings (11 V, 40 W, 3 I)

---

<a id="c14-02"></a>
### C14.02 — The shacl CLI reported conformance when it checked nothing, up to 0.3.3

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-02) · [plain edition](../docs/14-coverage-and-gaps.md#the-shacl-cli-reported-conformance-when-it-checked-nothing-fixed-in-034)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> The one-shot Python and JavaScript calls have refused a shapes graph that declares

**Evidence:** the same as [C11.07 — The CLI and an empty shapes graph: conforms up to 0.3.3, refused from 0.3.4](#c11-07), which reproduces it: shacl 0.3.4: step 1 exits 2; step 1 output contains 'the shapes graph declares no shapes'; step 2 exits 2; step 2 output contains 'no --shapes was given'; step 3: conforms: true; step 3 exits 0

---

<a id="c14-03"></a>
### C14.03 — holos validate exited 0 on a non-conforming graph, up to 0.21.1

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-03) · [plain edition](../docs/14-coverage-and-gaps.md#holos-validate-exited-0-on-a-non-conforming-graph-fixed-in-0220)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Up to 0.21.1 both of its validators printed `conforms false` and returned exit

**Evidence:** the same as [C11.29 — holos validate: exit 0 whatever it found up to 0.21.1, a gate from 0.22.0](#c11-29), which reproduces it: step 1 output contains 'conforms          false'; step 2 output contains 'conforms          false'; step 5 output contains "'conforms': False", 'HolosError: unsupported: sh:sparql is not implemented'; holos 0.25.0: step 1 exits 1; step 2 exits 1; step 3 exits 1; step 3 output contains 'conforms          false'; step 4 exits 1; step 6 exits 2; step 6 output contains 'sh:sparql'; step 7 exits 0

---

<a id="c14-04"></a>
### C14.04 — tarka drops instances it cannot build, silently, in the CLI and in Python

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-04) · [plain edition](../docs/14-coverage-and-gaps.md#tarka-drops-instances-it-cannot-build-silently)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> An OTTR template whose `ottr:IRI` parameter receives a cell tarka does not accept

**Evidence:** the same as [C10.11 — Without a mailto: prefix, run -l drops every row, silently](#c10-11), which reproduces it: step 1 exits 0; run -l: no message at all; step 2 output contains ': 0 triples'; step 3 exits 0; step 4 output contains ': 35 triples'; step 4 output has none of 'mbox'; step 5 exits 1; step 5 output contains '5 instances left out; the other 0 were made', 'row 1: argument 4 (id)'; step 6 exits 0; step 7 output contains ': 40 triples'

The Python half is in C10.12: `Mapping.ottr(...).run_csv(...)` returns None, raises nothing and writes 0 triples.

---

<a id="c14-05"></a>
### C14.05 — docgen reshuffles the page on every run

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-05) · [plain edition](../docs/14-coverage-and-gaps.md#docgen-reshuffles-the-page-on-every-run)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Still open at 0.24.1, re-checked rather than carried forward: three identical runs

**Evidence:** the same as [C13.12 — Three runs, three pages; pinned, one](#c13-12), which reproduces it: three unpinned runs gave 3 different pages; two runs with PYTHONHASHSEED=0 gave the same page

---

<a id="c14-06"></a>
### C14.06 — The reasoner's outcome follows the hash seed

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-06) · [plain edition](../docs/14-coverage-and-gaps.md#the-dl-reasoner-fails-on-some-hash-seeds-not-at-random)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> It is not random, and it is not HermiT.

**Commands** (from the `evidence/` folder):

```bash
python scripts/reasoner_seeds.py work/C14_06 10 0 5
```

<details><summary><code>scripts/reasoner_seeds.py</code></summary>

```python
"""Chapter 14 §14.4: whether HermiT runs is decided, almost entirely, by PYTHONHASHSEED.

    python scripts/reasoner_seeds.py work/C14_06 10 0 5

Runs the suite's `ontology` command on the acme fixture N times for each seed
given, each run in a fresh process with that PYTHONHASHSEED, and counts what
the reasoner did: REA-020 + REA-021 when HermiT ran, REA-022 when it did not.

"Almost": under a fixed seed the odd run still goes the other way, and fixing
the load path and rdflib's blank-node labels does not stop it. load_repeat.py
measures that.
"""
import collections
import csv
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
work, n, seeds = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
messages = collections.Counter()
for seed in seeds:
    tally = collections.Counter()
    for i in range(1, n + 1):
        out = work / f"seed{seed}-run{i}"
        env = dict(os.environ, PYTHONHASHSEED=seed)
        subprocess.run([sys.executable, "-m", "ontology_suite", "ontology",
                        "--ontology", "fixtures/acme_robotics/acme-org-v1.ttl",
                        "--import-dir", "fixtures/acme_robotics",
                        "--out-dir", str(out), "--reports", "minimal"],
                       env=env, capture_output=True, text=True)
        with open(out / "full_results.csv", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        ids = {r["check_id"] for r in rows}
        for r in rows:
            if r["check_id"] == "REA-022":
                messages[r["message"].split(". Only the always-on")[0]] += 1
        tally["ran" if "REA-021" in ids else "did not run" if "REA-022" in ids else "neither"] += 1
    print(f"PYTHONHASHSEED={seed}: HermiT ran {tally['ran']} of {n}, did not run {tally['did not run']} of {n}"
          + (f", neither {tally['neither']}" if tally["neither"] else ""))
print("REA-022 messages seen:")
for m, k in messages.most_common():
    print(f"  {k} x  {m}")
```

</details>

<details><summary><code>scripts/owlready2_probe.py</code></summary>

```python
"""Chapter 14 §14.4: where the reasoner's 'entity' error actually comes from.

    python scripts/owlready2_probe.py fixtures/acme_robotics/acme-org-v1.ttl \
        fixtures/acme_robotics/reference_vocab/org.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf

Does what the suite's reasoner bridge does (merge the files, write RDF/XML, load
it into owlready2), without the suite around it, and reports whether loading
succeeded. If it fails, prints the entity owlready2 was building and the last
frames of the traceback. Run it under different PYTHONHASHSEED values.

HermiT is not called at all: the failure, when it happens, is in loading.
"""
import os
import sys
import tempfile
import traceback
from pathlib import Path

import owlready2
from owlready2 import namespace as ns
from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
failed_on = []
original = ns.World._load_by_storid


def watched(self, storid, full_iri=None, *args, **kwargs):
    try:
        return original(self, storid, full_iri, *args, **kwargs)
    except UnboundLocalError:
        if not failed_on:
            failed_on.append(full_iri or self._unabbreviate(storid))
        raise


ns.World._load_by_storid = watched

# rdflib labels a parsed blank node "N" + uuid4().hex: random in every process,
# whatever the hash seed, and hashed like any other string. Set PROBE_FIXED_BNODES
# to number them instead (see load_repeat.py).
if os.environ.get("PROBE_FIXED_BNODES"):
    import itertools
    import uuid

    import rdflib.term
    _counter = itertools.count(1)
    rdflib.term.uuid4 = lambda: uuid.UUID(int=next(_counter))

g = Graph()
for f in sys.argv[1:]:
    g.parse(f)
seed = os.environ.get("PYTHONHASHSEED", "(unset)")
# The suite's bridge writes to a fresh temporary directory, as this does by
# default. Set PROBE_DIR to load from a fixed path instead (see load_repeat.py).
with tempfile.TemporaryDirectory() as tmp:
    path = Path(os.environ.get("PROBE_DIR") or tmp) / "ontology.owl"
    path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(path), format="xml")
    try:
        owlready2.World().get_ontology(str(path)).load()
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} loaded the merged ontology")
    except UnboundLocalError as exc:
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} failed while building <{failed_on[0]}>: {exc}")
        frames = traceback.extract_tb(exc.__traceback__)[-3:]
        for fr in frames:
            print(f"    {Path(fr.filename).name}:{fr.lineno} in {fr.name}: {fr.line}")
```

</details>

**What is checked:** ten runs per seed through the suite: seed 5 runs HermiT in at least 9, seed 0 fails in at least 7. The thresholds sit below the recorded tallies on purpose: C14.08 shows the one thing the seed does not control, and where the failure happens

**Recorded result:** PASS — seed 5: HermiT ran 10 of 10, did not run 0; seed 0: HermiT ran 0 of 10, did not run 10; step 1 output contains "could not be run: cannot access local variable 'entity' where it is not associated with a value"

<details><summary>Output, as recorded</summary>

```text
$ python scripts/reasoner_seeds.py work/C14_06 10 0 5
PYTHONHASHSEED=0: HermiT ran 0 of 10, did not run 10 of 10
PYTHONHASHSEED=5: HermiT ran 10 of 10, did not run 0 of 10
REA-022 messages seen:
  10 x  The external DL reasoner ('hermit') could not be run: cannot access local variable 'entity' where it is not associated with a value
[exit 0]
```

</details>

---

<a id="c14-07"></a>
### C14.07 — SHACL validates the union of the named graphs

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-07) · [plain edition](../docs/14-coverage-and-gaps.md#the-shacl-engine-cannot-scope-validation-to-a-named-graph)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Quad syntaxes parse, and then every named graph and the default graph are merged

**Inputs:** [`data/shacl/graphs.trig`](data/shacl/graphs.trig), [`data/shacl/graphs-flat.ttl`](data/shacl/graphs-flat.ttl)

<details><summary><code>data/shacl/graphs.trig</code></summary>

```turtle
# Chapter 14 §14.4: three nameless people, one in each of two named graphs and
# one in the default graph. SHACL validates the union.
@prefix ex: <http://example.org/> .

ex:bob a ex:Person .
ex:supplierA { ex:carol a ex:Person . }
ex:supplierB { ex:dave a ex:Person . }
```

</details>

<details><summary><code>data/shacl/graphs-flat.ttl</code></summary>

```turtle
# The same three people, flattened into one graph.
@prefix ex: <http://example.org/> .

ex:bob a ex:Person .
ex:carol a ex:Person .
ex:dave a ex:Person .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
shacl -d data/shacl/graphs.trig -s data/shacl/shapes-violation.ttl
shacl -d data/shacl/graphs-flat.ttl -s data/shacl/shapes-violation.ttl
shacl --help
```

**What is checked:** three results, one per person, whichever graph each was in; the same report as the flattened file; no graph-selection option in --help

**Recorded result:** PASS — step 1 output contains 'focus <http://example.org/bob>', 'focus <http://example.org/carol>', 'focus <http://example.org/dave>'; the TriG and the flattened file give identical reports; step 3 output has none of '--graph'

<details><summary>Output, as recorded</summary>

```text
$ shacl -d data/shacl/graphs.trig -s data/shacl/shapes-violation.ttl
conforms: false
  MinCountConstraintComponent | focus <http://example.org/bob> | value - | path <http://example.org/name>
  MinCountConstraintComponent | focus <http://example.org/carol> | value - | path <http://example.org/name>
  MinCountConstraintComponent | focus <http://example.org/dave> | value - | path <http://example.org/name>
[exit 1]

$ shacl -d data/shacl/graphs-flat.ttl -s data/shacl/shapes-violation.ttl
conforms: false
  MinCountConstraintComponent | focus <http://example.org/bob> | value - | path <http://example.org/name>
  MinCountConstraintComponent | focus <http://example.org/carol> | value - | path <http://example.org/name>
  MinCountConstraintComponent | focus <http://example.org/dave> | value - | path <http://example.org/name>
[exit 1]

$ shacl --help
A high-performance SHACL validator
Usage: shacl.exe [OPTIONS] --data <DATA>...
Options:
  -d, --data <DATA>...
          The data graph to validate. A path, an `http(s)` URL, or `-` for standard input.
          Repeat it to merge several documents into one graph. Blank nodes stay separate per document, as they must: `_:a` in two files is two nodes.
  -s, --shapes <SHAPES>...
          The shapes graph, on the same terms as `--data` and likewise repeatable. Defaults to the data graph, matching the convention that a self-describing document carries its own shapes.
          Only one input in total may be `-`, since standard input can be read only once.
      --data-format <DATA_FORMAT>
          The data graph's RDF syntax. Guessed from the file extension, or over HTTP from the `Content-Type`, when omitted; required when `--data` is `-`, which has neither
          [alias: --df]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --shapes-format <SHAPES_FORMAT>
          The shapes graph's RDF syntax, on the same terms as `--data-format`
          [alias: --sf]
          [possible values: turtle, n-triples, n-quads, tri-g, rdf-xml, json-ld, n3]
      --build-index
          Cache the parsed data graph beside it as `<file>.shix`, so later runs skip parsing.
          Parsing is around three quarters of a run over a large graph, and a data graph that has not changed is parsed identically every time. The cache is checked against the source on every use, so a stale one is never read — see `--no-index`.
          Only for a single local `--data` file: a URL has nowhere to write, and merged documents have no one source to check against.
      --no-index
          Ignore any `<file>.shix` cache and parse the data graph
      --allow-no-shapes
          Validate against a shapes graph that declares no shapes, instead of refusing to.
          Validating against no shapes conforms, because there is nothing to violate. Without this flag that is an error rather than a pass: the usual cause is a forgotten `--shapes`, and reporting success for a graph nothing was checked against is the worst answer a validator can give. Pass it when an empty shapes graph is what you meant.
      --threads <N>
          Worker threads for validation. `0` uses every core; `1` runs sequentially.
          Only a SHACL Core shapes graph splits across threads. One using `sh:sparql`, a SPARQL-based constraint component or node expressions runs sequentially whatever this says, as does any run with `--max-results`. The report is the same either way, byte for byte.
          [default: 0]
… (55 lines omitted; full output in the outputs/ record)
          Report how long loading, compiling and validating each took
      --repeat <REPEAT>
          Validate `n` times, reporting the best wall time. For benchmarking
          [default: 1]
  -h, --help
          Print help (see a summary with '-h')
  -V, --version
          Print version
[exit 0]
```

</details>

---

<a id="c14-08"></a>
### C14.08 — Almost: the seed decides most of owlready2's load, and not all of it

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-08) · [plain edition](../docs/14-coverage-and-gaps.md#the-dl-reasoner-fails-on-some-hash-seeds-not-at-random)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> *Almost*, because I had first written "every time", and the evidence for this

**Commands** (from the `evidence/` folder):

```bash
python scripts/load_repeat.py work/C14_08 15
```

<details><summary><code>scripts/load_repeat.py</code></summary>

```python
"""Chapter 14 §14.4: the seed decides most of owlready2's load, and not all of it.

    python scripts/load_repeat.py work/C14_08 15

Loads the merged acme ontology into owlready2 with owlready2_probe.py, N times
per condition, each in a fresh process, and counts the outcomes:

  1. PYTHONHASHSEED=0, each load from a fresh temporary directory, as the
     suite's bridge does.
  2. PYTHONHASHSEED=0 and 5, with two other sources of variation fixed: one
     load path for every run, and rdflib's blank-node labels numbered instead
     of random (PROBE_DIR and PROBE_FIXED_BNODES).

If the seed were the only input left in (2), each seed would give one outcome
every time. It does not quite: the remaining cause is not identified. Every
failure is reported with the entity owlready2 was building.
"""
import collections
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
work, n = Path(sys.argv[1]).resolve(), int(sys.argv[2])
files = ["fixtures/acme_robotics/acme-org-v1.ttl", "fixtures/acme_robotics/reference_vocab/org.ttl",
         "fixtures/acme_robotics/reference_vocab/foaf.rdf"]
failed_on = collections.Counter()


def load(seed, pinned):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    for k in ("PROBE_DIR", "PROBE_FIXED_BNODES"):
        env.pop(k, None)
    if pinned:
        env.update(PROBE_DIR=str(work / "fixed"), PROBE_FIXED_BNODES="1")
    out = subprocess.run([sys.executable, "scripts/owlready2_probe.py", *files], env=env,
                         capture_output=True, text=True, encoding="utf-8").stdout
    m = re.search(r"failed while building <([^>]+)>", out)
    if m:
        failed_on[m.group(1)] += 1
        return "failed"
    return "loaded" if "loaded the merged ontology" in out else "other"


def tally(seed, pinned):
    t = collections.Counter(load(seed, pinned) for _ in range(n))
    return f"loaded {t['loaded']} of {n}, failed {t['failed']} of {n}" + (f", other {t['other']}" if t["other"] else "")


print(f"1. PYTHONHASHSEED=0, fresh temporary directory: {tally(0, False)}")
print(f"2. PYTHONHASHSEED=0, fixed path and blank-node labels: {tally(0, True)}")
print(f"3. PYTHONHASHSEED=5, fixed path and blank-node labels: {tally(5, True)}")
print("failures were while building: " + (", ".join(f"<{k}> ({v})" for k, v in failed_on.items()) or "nothing"))
```

</details>

<details><summary><code>scripts/owlready2_probe.py</code></summary>

```python
"""Chapter 14 §14.4: where the reasoner's 'entity' error actually comes from.

    python scripts/owlready2_probe.py fixtures/acme_robotics/acme-org-v1.ttl \
        fixtures/acme_robotics/reference_vocab/org.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf

Does what the suite's reasoner bridge does (merge the files, write RDF/XML, load
it into owlready2), without the suite around it, and reports whether loading
succeeded. If it fails, prints the entity owlready2 was building and the last
frames of the traceback. Run it under different PYTHONHASHSEED values.

HermiT is not called at all: the failure, when it happens, is in loading.
"""
import os
import sys
import tempfile
import traceback
from pathlib import Path

import owlready2
from owlready2 import namespace as ns
from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
failed_on = []
original = ns.World._load_by_storid


def watched(self, storid, full_iri=None, *args, **kwargs):
    try:
        return original(self, storid, full_iri, *args, **kwargs)
    except UnboundLocalError:
        if not failed_on:
            failed_on.append(full_iri or self._unabbreviate(storid))
        raise


ns.World._load_by_storid = watched

# rdflib labels a parsed blank node "N" + uuid4().hex: random in every process,
# whatever the hash seed, and hashed like any other string. Set PROBE_FIXED_BNODES
# to number them instead (see load_repeat.py).
if os.environ.get("PROBE_FIXED_BNODES"):
    import itertools
    import uuid

    import rdflib.term
    _counter = itertools.count(1)
    rdflib.term.uuid4 = lambda: uuid.UUID(int=next(_counter))

g = Graph()
for f in sys.argv[1:]:
    g.parse(f)
seed = os.environ.get("PYTHONHASHSEED", "(unset)")
# The suite's bridge writes to a fresh temporary directory, as this does by
# default. Set PROBE_DIR to load from a fixed path instead (see load_repeat.py).
with tempfile.TemporaryDirectory() as tmp:
    path = Path(os.environ.get("PROBE_DIR") or tmp) / "ontology.owl"
    path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(path), format="xml")
    try:
        owlready2.World().get_ontology(str(path)).load()
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} loaded the merged ontology")
    except UnboundLocalError as exc:
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} failed while building <{failed_on[0]}>: {exc}")
        frames = traceback.extract_tb(exc.__traceback__)[-3:]
        for fr in frames:
            print(f"    {Path(fr.filename).name}:{fr.lineno} in {fr.name}: {fr.line}")
```

</details>

**What is checked:** loading the merged ontology straight into owlready2, with the load path and blank-node labels fixed: seed 0 fails in at least 9 of 15 and seed 5 loads in at least 13 of 15; every failure is while building foaf:primaryTopic. The exact tallies, including any loads that go the other way, are recorded rather than asserted

**Recorded result:** PASS — line 2. failed 15 times (at least 9); line 3. loaded 15 times (at least 13); every failure was owlready2 building foaf:primaryTopic

<details><summary>Output, as recorded</summary>

```text
$ python scripts/load_repeat.py work/C14_08 15
1. PYTHONHASHSEED=0, fresh temporary directory: loaded 0 of 15, failed 15 of 15
2. PYTHONHASHSEED=0, fixed path and blank-node labels: loaded 0 of 15, failed 15 of 15
3. PYTHONHASHSEED=5, fixed path and blank-node labels: loaded 15 of 15, failed 0 of 15
failures were while building: <http://xmlns.com/foaf/0.1/primaryTopic> (30)
[exit 0]
```

</details>

**Sources:**

- [suite reasoning/backends/external_backend.py: a fresh TemporaryDirectory, loaded by path](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/ontology_suite/reasoning/backends/external_backend.py#L140-L155): “onto = world.get_ontology(str(owl_path)).load()” (quote found, checked 2026-10-22)

HermiT is never called here: the failure, when it comes, is in loading.

---

<a id="c14-09"></a>
### C14.09 — Without Java the message is the operating system's

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-09) · [plain edition](../docs/14-coverage-and-gaps.md#the-dl-reasoner-fails-on-some-hash-seeds-not-at-random)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> "cannot find the file specified", so a genuinely missing Java *is*

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=5 python scripts/without_java.py ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C14_09/out --reports minimal
python scripts/summarise_findings.py work/C14_09/out/full_results.csv --by focus --check REA-022
```

<details><summary><code>scripts/without_java.py</code></summary>

```python
"""Run a command with no Java runtime visible, so HermiT cannot start.

    python scripts/without_java.py ontology-quality-suite ontology --ontology ...

Removes every PATH entry holding a `java` executable and unsets JAVA_HOME, then
runs the command. Otherwise whether the DL reasoner runs depends on the hash seed (Chapter 14
§14.4); this takes Java away as well, to show that a missing Java gives a different message.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

env = dict(os.environ)
env.pop("JAVA_HOME", None)
exe = "java.exe" if os.name == "nt" else "java"
keep = [d for d in env.get("PATH", "").split(os.pathsep) if d and not (Path(d) / exe).is_file()]
env["PATH"] = os.pathsep.join(keep)
print(f"without_java: java on PATH now: {shutil.which('java', path=env['PATH']) or 'none'}", flush=True)
cmd = sys.argv[1:]
cmd[0] = shutil.which(cmd[0], path=env["PATH"]) or cmd[0]
sys.exit(subprocess.run(cmd, env=env).returncode)
```

</details>

**What is checked:** with Java hidden and seed 5 (so owlready2 loads), REA-022's message names the missing file and not 'entity'

**Recorded result:** PASS — step 1 output contains 'without_java: java on PATH now: none'; REA-022 says 'cannot find the file specified'; and not 'entity'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/without_java.py ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C14_09/out --reports minimal
without_java: java on PATH now: none
Findings: 2 total (1 Violation, 0 Warning, 1 Info)
Reports written to: ./work/C14_09/out
  - work/C14_09/out/findings.txt (start here -- what, where, and the source line)
  - work/C14_09/out/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmp8e1ltl36 -Y
[exit 1]

$ python scripts/summarise_findings.py work/C14_09/out/full_results.csv --by focus --check REA-022
REA-022  focus=oq:Graph  path=-  value=-
total 1: 0 Violation, 0 Warning, 1 Info
[exit 0]
```

</details>

---

<a id="c14-39"></a>
### C14.39 — REA-020 said inconsistent when only a class was unsatisfiable; fixed in 0.23.0

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-39) · [plain edition](../docs/14-coverage-and-gaps.md#rea-020-said-inconsistent-when-one-class-was-unsatisfiable-fixed-in-0230)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> When HermiT does run on the fixture, suite 0.22.0 reports `REA-020`

**Inputs:** [`data/reasoner/clean.ttl`](data/reasoner/clean.ttl)

<details><summary><code>data/reasoner/clean.ttl</code></summary>

```turtle
# Chapter 14 §14.4: a clean ontology. HermiT finds nothing unsatisfiable, and
# the suite reports neither REA-020 nor REA-021.
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:   <http://example.org/> .

ex:o a owl:Ontology .
ex:A a owl:Class .
ex:B a owl:Class ; rdfs:subClassOf ex:A .
```

</details>

**Commands** (from the `evidence/` folder):

```bash
PYTHONHASHSEED=5 python scripts/hermit_verdict.py fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/reference_vocab/org.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf
PYTHONHASHSEED=5 ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C14_39/acme --reports minimal
python scripts/summarise_findings.py work/C14_39/acme/full_results.csv
python scripts/hermit_verdict.py data/reasoner/clean.ttl
ontology-quality-suite ontology --ontology data/reasoner/clean.ttl --out-dir work/C14_39/clean --reports minimal
python scripts/summarise_findings.py work/C14_39/clean/full_results.csv
```

<details><summary><code>scripts/hermit_verdict.py</code></summary>

```python
"""Chapter 14 §14.4: what HermiT itself says about an ontology, through owlready2.

    python scripts/hermit_verdict.py FILE [FILE ...]

Merges the files, loads them into owlready2 as the suite's bridge does, runs
HermiT, and prints whether it found the ontology inconsistent and which classes
it found unsatisfiable. Needs Java. The suite turns `owl:Nothing` in that list
into REA-020, "the ontology is inconsistent"; this shows what HermiT reported.
"""
import sys
import tempfile
from pathlib import Path

import owlready2
from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
g = Graph()
for f in sys.argv[1:]:
    g.parse(f)
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "ontology.owl"
    g.serialize(destination=str(path), format="xml")
    world = owlready2.World()
    onto = world.get_ontology(str(path)).load()
    try:
        with onto:
            owlready2.sync_reasoner(world, infer_property_values=True)
        print("HermiT: consistent (no OwlReadyInconsistentOntologyError)")
    except owlready2.OwlReadyInconsistentOntologyError:
        print("HermiT: INCONSISTENT")
        sys.exit()
    unsat = [getattr(c, "iri", str(c)) for c in world.inconsistent_classes()]
    print("unsatisfiable classes:", sorted(unsat) or "none")
    print("owl:Nothing among them:", "http://www.w3.org/2002/07/owl#Nothing" in unsat)
```

</details>

**What is checked:** on the fixture HermiT finds the ontology consistent, with Contractor and owl:Nothing unsatisfiable; suite 0.22.0 reports REA-020 as well as REA-021, and 0.23.0 REA-021 alone. On a clean ontology HermiT finds nothing and the suite reports neither

**Recorded result:** PASS — step 1 output contains 'HermiT: consistent', 'owl:Nothing among them: True', 'https://acme.example.org/ns/Contractor'; suite 0.24.3: step 3 output contains 'REA-021'; step 3 output has none of 'REA-020'; step 4 output contains 'HermiT: consistent', 'unsatisfiable classes: none'; step 6 output has none of 'REA-020', 'REA-021', 'REA-022'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/hermit_verdict.py fixtures/acme_robotics/acme-org-v1.ttl fixtures/acme_robotics/reference_vocab/org.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf
HermiT: consistent (no OwlReadyInconsistentOntologyError)
unsatisfiable classes: ['http://www.w3.org/2002/07/owl#Nothing', 'https://acme.example.org/ns/Contractor']
owl:Nothing among them: True
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmpq4y1u2d8 -Y
[exit 0]

$ ontology-quality-suite ontology --ontology fixtures/acme_robotics/acme-org-v1.ttl --import-dir fixtures/acme_robotics --out-dir work/C14_39/acme --reports minimal
Findings: 2 total (2 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C14_39/acme
  - work/C14_39/acme/findings.txt (start here -- what, where, and the source line)
  - work/C14_39/acme/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmp8ahpx12h -Y
[exit 1]

$ python scripts/summarise_findings.py work/C14_39/acme/full_results.csv
  1 x LOG-001  Violation Class disjoint with its own ancestor
  1 x REA-021  Violation Class found unsatisfiable by an external DL reasoner
total 2: 2 Violation, 0 Warning, 0 Info
[exit 0]

$ python scripts/hermit_verdict.py data/reasoner/clean.ttl
HermiT: consistent (no OwlReadyInconsistentOntologyError)
unsatisfiable classes: none
owl:Nothing among them: False
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmpdnrc8ivs -Y
[exit 0]

$ ontology-quality-suite ontology --ontology data/reasoner/clean.ttl --out-dir work/C14_39/clean --reports minimal
Findings: 0 total (0 Violation, 0 Warning, 0 Info)
Reports written to: ./work/C14_39/clean
  - work/C14_39/clean/findings.txt (start here -- what, where, and the source line)
  - work/C14_39/clean/full_results.csv
    java -Xmx2000M -cp ./.venv/Lib/site-packages/owlready2/hermit;./.venv/Lib/site-packages/owlready2/hermit/HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///<tmp>/tmprghbpc5y -Y
[exit 0]

$ python scripts/summarise_findings.py work/C14_39/clean/full_results.csv
total 0: 0 Violation, 0 Warning, 0 Info
[exit 0]
```

</details>

**Sources:**

- [suite external_backend.py at 0.22.0, the belt-and-braces rule](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/749af3e1be749ace3aab3ea4b492d72b3b21dbde/ontology_suite/reasoning/backends/external_backend.py#L128-L133): “thing_or_nothing = {owlready2.Thing, owlready2.owl.Nothing}” (quote found, checked 2026-10-22)
- [testing repo detect.py, 03b-unsatisfiable-class, at 6d078a1](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/6d078a118959760409e13076650c2d62a4f6dc90/detect.py#L115-L128): “forbidden=("REA-001", "CNF-001", "CNF-002"),” (quote found, checked 2026-10-22)
- [suite commit d7d7a98, the fix](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/d7d7a987cb754221b6c57a5997445628e219851b): “REA-020 said "inconsistent" for a merely unsatisfiable class” (quote found, checked 2026-10-22)
- [testing repo commit 6cdfb14: 03b now forbids REA-020](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/6cdfb14a3c2857b61dcb32f49f56a4829b0d0664): “Forbid REA-020 where the class is unsatisfiable but the ontology is not” (quote found, checked 2026-10-22)

Needs Java, and a hash seed under which owlready2 loads (5 here; see C14.06).

---

<a id="c14-10"></a>
### C14.10 — A mistyped manifest role compared nothing, successfully (fixed in 0.24.0)

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-10) · [plain edition](../docs/14-coverage-and-gaps.md#a-mistyped-manifest-role-compared-nothing-successfully-fixed-in-0240)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> `consistency-remote` accepted any string as a graph's `role` and ignored all but

**Evidence:** the same as [C13.03 — The store a version behind: --fail-on-anything exits 1](#c13-03), which reproduces it: step 5 output contains 'template vs ontology: clean', 'live data vs ontology: 1 undeclared class(es)', "'classes_only_in_template': ['https://acme.example.org/ns/SoftwareEngineer']", "'classes_only_in_live_data': ['https://acme.example.org/ns/Engineer']"; step 5 exits 1; step 6 output has none of '==='; step 6 output contains 'unknown graph role'; suite 0.24.3: step 6 exits 2; suite 0.24.3: the refusal is one line on stderr, with no traceback

---

<a id="c14-11"></a>
### C14.11 — --help offers owlrl; asking for it gives a traceback

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-11) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | At 0.22.0, `--help` offers `--inference owlrl` and `both`, and asking for one gives a Python traceback

**Evidence:** the same as [C07.26 — --inference owlrl is refused: a traceback at 0.22.0, a usage error from 0.23.0](#c07-26), which reproduces it: step 1 exits non-zero (2); suite 0.24.3: step 1 output contains "argument --inference: invalid choice: 'owlrl'"; step 1 output has none of 'Traceback'; step 2 output contains '--inference {none,rdfs}'

---

<a id="c14-12"></a>
### C14.12 — --inference is ignored under --engine sparql

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-12) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | At 0.22.0, `--inference` reaches the shapes only

**Evidence:** the same as [C07.27 — --inference rdfs: half the suite at 0.22.0, every engine from 0.23.0](#c07-27), which reproduces it: suite 0.24.3: step 1 exits non-zero (2); step 2: 489 findings (57 V, 339 W, 93 I); step 3: 479 findings (55 V, 340 W, 84 I); step 4: 489 findings (57 V, 339 W, 93 I); step 5 output contains 'gained 21:', 'STR-007 9', 'STY-003 9', 'STR-009 3', 'lost 11:', 'STR-006 1', 'DAT-002 1'

---

<a id="c14-13"></a>
### C14.13 — The near-miss warning listed blank-node identifiers, until 0.24.0

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-13) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | Up to 0.23.0, the `--own-namespace` near-miss warning lists two blank-node identifiers

**Evidence:** the same as [C09.07 — A near-miss namespace warns, on stderr, and offers only real namespaces](#c09-07), which reproduces it: step 1: 0 findings (0 V, 0 W, 0 I); the warning is on stderr, not stdout; all 5 namespaces offered have a scheme

---

<a id="c14-14"></a>
### C14.14 — --registry replaces, so @builtin with a house registry is UNMAPPED

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-14) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | `--sparql` composes but `--registry` replaces

**Evidence:** the same as [C08.24 — With @builtin and a one-entry registry, every built-in finding is UNMAPPED](#c08-24), which reproduces it: step 2: 491 findings (54 V, 356 W, 81 I); all 491 findings have check id UNMAPPED; each keeps its severity; nearly all keep their message; none has a title or a remediation

---

<a id="c14-15"></a>
### C14.15 — One contradiction, two LOG-001s, until 0.24.0

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-15) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | Up to 0.23.0, `data` and `run` report one contradiction as two `LOG-001`s

**Evidence:** the same as [C09.14 — run reports 26 findings, one contradiction once, from 0.24.0](#c09-14), which reproduces it: step 1: 26 findings (2 V, 22 W, 2 I); step 1 exits 1; out/full_results.csv: {'CNF-005': 2, 'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'REA-021': 1, 'STR-003': 1, 'STY-002': 1}

---

<a id="c14-16"></a>
### C14.16 — The DSL's TypeError and Quad type, up to 0.16.0

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-16) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | Up to 0.16.0, the DSL gives unchecked code an internal `TypeError`

**Evidence:** the same as [C08.15 — Unchecked code: an internal TypeError up to 0.16.0, an error naming the mistake from 0.16.1](#c08-15), which reproduces it: step 1 exits non-zero (1); npm ontology-suite 0.16.1: step 1 output contains "defdatatypeproperty('hasEmployeeId'): range takes a datatype, made with datatype('xsd:string') say, and was given the string"

---

<a id="c14-17"></a>
### C14.17 — triplify drives oxi-gen only

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-17) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | The suite's `triplify` and the extension's *Run Full Triplify* drive `oxi-gen` only

**Evidence:** the same as [C10.17 — The suite's triplify still needs oxi-gen, and says so](#c10-17), which reproduces it: step 1 output contains 'WARNING: oxi-gen binary not found', 'Triplified 0 file(s)'

---

<a id="c14-18"></a>
### C14.18 — consistency and pattern-consistency are report-only by default

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-18) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | `consistency` and `pattern-consistency` exit 0 whatever they find

**Evidence:** the same as [C12.14 — Both consistency commands are report-only by default](#c12-14), which reproduces it: step 2 exits 0; step 3 exits 1; step 4 exits 0; step 5 exits 1

---

<a id="c14-19"></a>
### C14.19 — The holos CLI and holosdb defaulted to different validators, up to 0.21.1

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-19) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | Up to 0.21.1, the `holos validate` command defaults to the `native` engine and `holosdb`'s

**Evidence:** the same as [C13.10 — Validation and the store: written into it up to 0.21.0, untouched from 0.21.1](#c13-10), which reproduces it: holosdb 0.25.0, holos 0.25.0: step 1 output contains "adapted: {'conforms': False, 'violations': 2, 'engine': 'adapted', 'results': [", "native:  {'conforms': False, 'violations': 2, 'engine': 'native', 'results': [", "'focus': 'http://example.org/a'", "'focus': 'http://example.org/b'", 'HolosError: unsupported: sh:sparql is not implemented'; step 10 output contains '--engine <NAME>          adapted (default) or native'; step 2 output contains 'adapted, three calls on one store: violations [2, 2, 2]', 'native, three calls on one store: violations [2, 2, 2]', 'named graphs after one validate(): []', 'named graphs in the persistent store after reopening: []', 'store.update("DROP GRAPH <urn:holos:python:shapes>") removes them'; step 5 output contains 'results           2'; step 6 output contains 'results           2'; step 7 output has none of 'urn:holos:shapes'; step 9 output contains 'note: <urn:holos:shapes> holds 1 quads', 'DROP GRAPH <urn:holos:shapes>'

---

<a id="c14-20"></a>
### C14.20 — sketch reads every file with the first file's prefixes

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-20) · [plain edition](../docs/14-coverage-and-gaps.md#smaller-ones-all-worth-a-line)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> | At 0.22.0, when two query files bind one prefix differently, `sketch` reads every file

**Evidence:** the same as [C10.29 — The merged sketch and one prefix bound two ways: odd file first](#c10-29), which reproduces it: suite 0.24.3: the warning says each file is read with its own definition; step 2 output contains 'focus=https://acme.example.org/ns#Department'; step 2 output has none of 'ns#Employee'; step 3 output has none of 'ns#hasSkill', 'ns#hasEmployeeId'; three/full_results.csv: CNF-005 excludes https://acme.example.org/ns/Employee; two/full_results.csv: {'CNF-005': 36, 'TQL-003': 1}; two/full_results.csv: CNF-005 excludes https://acme.example.org/ns/Employee

---

<a id="c14-21"></a>
### C14.21 — Documentation drift, upstream

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-21) · [plain edition](../docs/14-coverage-and-gaps.md#documentation-drift-upstream)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> None of these changes what a tool does. All of them change what a careful reader

**Commands** (from the `evidence/` folder):

```bash
ontology-quality-suite checks --help
```

**What is checked:** at 0.22.0 the suite's --engine help still says 'both' runs pyshacl and 'native' is not a default dependency; from 0.23.0 it says neither

**Recorded result:** PASS — suite 0.24.3: step 1 output has none of 'runs pyshacl', 'not a default dependency'

<details><summary>Output, as recorded</summary>

```text
$ ontology-quality-suite checks --help
usage: ontology-quality-suite checks [-h] [--ontology ONTOLOGY] [--data DATA]
                                     [--import-dir IMPORT_DIR]
                                     [--exclude-imports] [--allow-network]
                                     [--shapes SHAPES] [--sparql SPARQL]
                                     [--registry REGISTRY] [--themes THEMES]
                                     [--inference {none,rdfs}]
                                     [--engine {both,sparql,shacl,native,native+sparql}]
                                     [--out-dir OUT_DIR]
                                     [--reports {all,minimal}]
                                     [--fail-on {Violation,Warning,Info,never}]
                                     [--own-namespace OWN_NAMESPACE] [-v]
options:
  -h, --help            show this help message and exit
  --ontology ONTOLOGY
  --data DATA
  --import-dir IMPORT_DIR
                        searched recursively for local copies of imports
                        (default: the ontology file's own directory)
  --exclude-imports     evaluate the ontology file alone; owl:imports are
                        neither fetched nor merged
  --allow-network       fetch an unresolved owl:imports IRI over HTTP (off by
                        default)
  --shapes SHAPES
  --sparql SPARQL       a directory of .rq check queries, or @builtin for the
                        suite's own tree wherever this install put it.
                        Repeatable: pass it more than once to run a project's
                        own checks alongside the suite's, which is what you
                        almost always want. Given at all, it replaces the
                        built-in tree, so `--sparql mine` runs only yours --
                        the run warns when that happens. See
… (48 lines omitted; full output in the outputs/ record)
                        --exclude-imports, this does not introduce undeclared-
                        term noise; it just hides pre-existing findings that
                        belong to an imported vocabulary rather than your own.
  -v, --verbose         print what each input option actually resolved to
                        before running: which query/data files --query-
                        pattern/--data-pattern matched, which owl:imports
                        resolved (and from where) or failed to, and which
                        check engine ran
[exit 0]
```

</details>

**Sources:**

- [suite docs/REPORTS.md says 0.15.0 (see C09.11 for 0.17.0)](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/REPORTS.md#L18): “## What changed in 0.15.0” (quote found, checked 2026-10-22)
- [suite docs/REASONING.md](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/0a23055c4bf354287795b8da4155d99f8687423c/docs/REASONING.md#L107): “Uses `owlready2` (the `reasoner` extra: `uv sync --extra reasoner`)” (quote found, checked 2026-10-22)
- [suite pyproject.toml at its first commit: owlready2 a base dependency](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/d0ba3679644360c31118295f9ba8738c85111e95/pyproject.toml#L14): “"owlready2>=0.51",” (quote found, checked 2026-10-22)
- [extension README (0.15.0) names Oxigraph](https://github.com/pwin/consolidated-ontology-quality-suite-webapp/blob/a92175dfd1ec999c3b50fee886cc5b2d6ca3ee39/README.md#L86): “Oxigraph, `shacl-wasm`, and `eyereasoner` are all” (quote found, checked 2026-10-22)
- [testing repo README](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/README.md#L22): “18 Turtle files in 10 folders” (quote found, checked 2026-10-22)
- [testing repo README](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/README.md#L31): “All 16 fixtures pass” (quote found, checked 2026-10-22)
- [suite commit 5d59713, 'Bump to 0.18.0': main's head until it was fast-forwarded to 0.23.0, as recorded while drafting](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/5d597132779a19dbfb7ccf8891723ca19d49ced3): “Bump to 0.18.0” (quote found, checked 2026-10-22)

The testing repository's `ontologies/` holds 14 folders and 25 Turtle files at 6cdfb14; its detect.py declares 17 fixtures (C09.19). The suite's default branch on GitHub is `develop`.

---

<a id="c14-22"></a>
### C14.22 — The registry grew from 50 checks to 61

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-22) · [plain edition](../docs/14-coverage-and-gaps.md#145-the-cheapest-thing-you-are-not-doing)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> registry grows, as it did from 50 checks to 61, and the scoped run is the one whose

**Sources:**

- [suite registry.json at v0.8.0](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/v0.8.0/ontology_suite/resources/registry.json)
- [suite registry.json at v0.14.2](https://github.com/pwin/consolidated-ontology-quality-suite-python/blob/v0.14.2/ontology_suite/resources/registry.json)

Counted from the tagged files: 50 entries at v0.5.0 and v0.8.0, 56 at v0.10.0, 61 from v0.14.2.

---

<a id="c14-23"></a>
### C14.23 — Closed: the engines are the toolchain's own

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-23) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The engines are the toolchain's own.**

**Evidence:** the same as [C07.22 — --engine: native misses QUA-004; sparql and both give 23](#c07-22), which reproduces it: step 1: 22 findings (1 V, 21 W, 0 I); step 2: 22 findings (1 V, 21 W, 0 I); step 3: 23 findings (1 V, 22 W, 0 I); step 4: 23 findings (1 V, 22 W, 0 I); step 5: 23 findings (1 V, 22 W, 0 I); QUA-004 appears under sparql and not under native; and is the only difference between them

---

<a id="c14-24"></a>
### C14.24 — Closed: messages on blank nodes

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-24) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Messages on blank nodes.**

**Evidence:** the same as [C07.07 — STR() of a blank node: lenient, conformant, and the guard](#c07-07), which reproduces it: unguarded: rdflib names an internal identifier; holosdb and pyoxigraph leave the message unbound; COALESCE: rdflib still names the identifier, the other two say '[a blank node]'; IF(isBlank(...)): all three say '[a blank node]'

---

<a id="c14-25"></a>
### C14.25 — Closed: findings say where they are

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-25) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Findings say where they are.**

**Evidence:** the same as [C08.17 — ontology reports 2 findings, and findings.txt quotes the line](#c08-17), which reproduces it: step 1: 2 findings (1 V, 0 W, 1 I); step 1 output contains 'findings.txt (start here -- what, where, and the source line)'; ontology/findings.txt contains '2 finding(s): 1 Violation, 1 Info', '> 47 | acme:Contractor a owl:Class ;', '48 |     rdfs:subClassOf acme:Employee ;', '-- not located: 1 finding(s)', 'REA-022  Info  External DL reasoner unavailable'; LOG-001's message reads as quoted; and its remediation too

---

<a id="c14-26"></a>
### C14.26 — Closed: house rules compose with the built-ins

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-26) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **House rules compose with the built-ins.**

**Evidence:** the same as [C08.25 — A merged registry names every finding, and ACM-001 fires on its fault only](#c08-25), which reproduces it: step 1 output contains '61 built-in + 1 project = 62 entries'; ACM-001 fires on E101 (no ID) and not on E100 (the control); with its title and remediation from the merged registry; and no finding is UNMAPPED

---

<a id="c14-27"></a>
### C14.27 — Five suite defects found by the testing repository

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-27) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **Five suite defects found by the testing repository**

**Sources:**

- [suite commit cd72df1: language-tagged literals, and per-row entities](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/cd72df19132e76cb91d3f775943c054d3a1e617a): “Both found by the sibling fixture repo” (quote found, checked 2026-10-22)
- [suite commit 9defc24: the namespace legend](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/9defc24d331866420b6532f407612ed35089d834) (exists, checked 2026-10-22)
- [testing repo CT-01 README: the legend's false finding, until suite 0.20.0](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/blob/7deaf86a523fb313ccf47572df4e7276c779e28e/experiments/SpecificTests/CT-01-iri-template-drift/README.md#L50-L52): “It held one entry until suite 0.20.0.” (quote found, checked 2026-10-22)
- [suite commit def9038: the default namespace](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/def9038a8d43cfcf421c0c04b90ee0e400cd8df1): “Found while building an isolated fixture for CT-3” (quote found, checked 2026-10-22)
- [suite commit cae9ef2: --sparql replacing the built-ins](https://github.com/pwin/consolidated-ontology-quality-suite-python/commit/cae9ef21cf33ceb8eba33ef94da66b32bf810ded): “Found in exactly that state: the separate testing repo's CI gate config” (quote found, checked 2026-10-22)

---

<a id="c14-28"></a>
### C14.28 — Closed: sh:conforms follows the specification

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-28) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **`sh:conforms` means what the specification says**, from engine 0.3.0, and the

**Evidence:** the same as [C11.04 — Warnings break conformance; --allow-warnings records the choice](#c11-04), which reproduces it: step 1: conforms: false; step 1 exits 1; step 2 exits 0; step 2 output contains 'sh:conforms true', 'sh:conformanceDisallows sh:Violation'; step 3 output contains '--allow-warnings', '--allow-infos', '--min-severity'

---

<a id="c14-29"></a>
### C14.29 — Closed: the repair engine keeps blank nodes and base directions

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-29) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **The repair engine** keeps blank nodes and base directions intact when it writes

**Evidence:** the same as [C08.08 — Blank nodes cross the repair boundary as skolem IRIs](#c08-08) (cited from upstream).

---

<a id="c14-40"></a>
### C14.40 — Closed: HOLOS validation leaves the store as it found it, from 0.21.1

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-40) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **HOLOS validation leaves the store as it found it**, from 0.21.1.

**Evidence:** the same as [C13.10 — Validation and the store: written into it up to 0.21.0, untouched from 0.21.1](#c13-10), which reproduces it: holosdb 0.25.0, holos 0.25.0: step 1 output contains "adapted: {'conforms': False, 'violations': 2, 'engine': 'adapted', 'results': [", "native:  {'conforms': False, 'violations': 2, 'engine': 'native', 'results': [", "'focus': 'http://example.org/a'", "'focus': 'http://example.org/b'", 'HolosError: unsupported: sh:sparql is not implemented'; step 10 output contains '--engine <NAME>          adapted (default) or native'; step 2 output contains 'adapted, three calls on one store: violations [2, 2, 2]', 'native, three calls on one store: violations [2, 2, 2]', 'named graphs after one validate(): []', 'named graphs in the persistent store after reopening: []', 'store.update("DROP GRAPH <urn:holos:python:shapes>") removes them'; step 5 output contains 'results           2'; step 6 output contains 'results           2'; step 7 output has none of 'urn:holos:shapes'; step 9 output contains 'note: <urn:holos:shapes> holds 1 quads', 'DROP GRAPH <urn:holos:shapes>'

---

<a id="c14-41"></a>
### C14.41 — Closed: three suite defects this edition found, fixed in 0.23.0

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-41) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Three suite defects this edition found are fixed in 0.23.0**

**Evidence:** the same as [C07.27 — --inference rdfs: half the suite at 0.22.0, every engine from 0.23.0](#c07-27), which reproduces it: suite 0.24.3: step 1 exits non-zero (2); step 2: 489 findings (57 V, 339 W, 93 I); step 3: 479 findings (55 V, 340 W, 84 I); step 4: 489 findings (57 V, 339 W, 93 I); step 5 output contains 'gained 21:', 'STR-007 9', 'STY-003 9', 'STR-009 3', 'lost 11:', 'STR-006 1', 'DAT-002 1'

The other two are C14.39 (REA-020) and C10.29 and C10.30 (sketch).

---

<a id="c14-42"></a>
### C14.42 — Closed: gates that could not fail, and the DSL's two rough edges

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-42) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Gates that could not fail, now can**: the `shacl` CLI refuses to validate

**Evidence:** the same as [C11.29 — holos validate: exit 0 whatever it found up to 0.21.1, a gate from 0.22.0](#c11-29), which reproduces it: step 1 output contains 'conforms          false'; step 2 output contains 'conforms          false'; step 5 output contains "'conforms': False", 'HolosError: unsupported: sh:sparql is not implemented'; holos 0.25.0: step 1 exits 1; step 2 exits 1; step 3 exits 1; step 3 output contains 'conforms          false'; step 4 exits 1; step 6 exits 2; step 6 output contains 'sh:sparql'; step 7 exits 0

The shacl CLI's refusal is C11.07; the DSL's two fixes are C08.15 and C08.16.

---

<a id="c14-30"></a>
### C14.30 — Early, but real: policy, rules, a triplifier

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-30) · [plain edition](../docs/14-coverage-and-gaps.md#gaps-and-rough-edges-that-have-closed)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Early, but real:** read access policy at the index scan, with classification,

**Evidence:** the same as [C13.06 — Policy at the scan: rows without the column, unless you are in HR](#c13-06), which reproduces it: step 1 output contains '2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None/n    name=Bob, salary=None/n    name=Carol, salary=None', '3. the same, asked by alice with role hr:\n    name=Alice, salary=95000/n    name=Bob, salary=88000/n    name=Carol, salary=102000', '4. COUNT of salaries without the role:\n    n=0', '5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance/n    g=http://example.com/public/n6.', '6. named graphs, with clearance 3:\n    g=http://example.com/provenance/n    g=http://example.com/public/n    g=http://example.com/reviews', '7. salary denied with fail_closed():\n    HolosError: ', 'access denied by policy/n8. (mistake)', '8. (mistake) policy method called as a statement:\n    n=3'

---

<a id="c14-31"></a>
### C14.31 — Wrong: the migration annotation's direction

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-31) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The migration annotation's direction.** Every earlier edition said rename

**Evidence:** the same as [C12.05 — The tombstone is read in both directions; isReplacedBy in one](#c12-05), which reproduces it: step 3 output contains 'employees.rq (confidence 100%)'; step 6 output contains 'employees.rq (confidence 100%)'; step 9 output contains 'employees.rq (confidence 57%)'

---

<a id="c14-32"></a>
### C14.32 — Wrong: REA-022 as the tell in a scoped run

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-32) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **`REA-022` as the reasoner's tell in a scoped run.**

**Evidence:** the same as [C09.09 — A scoped run keeps the 'reasoner did not run' finding, from 0.24.0](#c09-09), which reproduces it: unscoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; scoped/full_results.csv: REA-022 present; REA-022's focus node is oq:Graph; step 2: 548 findings (65 V, 363 W, 120 I); step 3: 54 findings (11 V, 40 W, 3 I)

---

<a id="c14-33"></a>
### C14.33 — Wrong: the reasoner as flaky

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-33) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The reasoner as "flaky".**

**Evidence:** the same as [C14.06 — The reasoner's outcome follows the hash seed](#c14-06), which reproduces it: seed 5: HermiT ran 10 of 10, did not run 0; seed 0: HermiT ran 0 of 10, did not run 10; step 1 output contains "could not be run: cannot access local variable 'entity' where it is not associated with a value"

---

<a id="c14-34"></a>
### C14.34 — Wrong: the reasoner as an optional extra

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-34) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **The reasoner as an "optional extra".**

**Evidence:** the same as [C07.05 — Both engines are runtime dependencies; owlready2 too; the wheels are libraries](#c07-05), which reproduces it: step 1 output contains 'commands installed: ontology-quality-suite', 'owlready2>=0.51', 'shacl 0.3.4/n    commands installed: none (library only)', 'tarka-rdf 0.1.1/n    commands installed: none (library only)', 'holosdb 0.25.0/n    commands installed: none (library only)'; suite 0.24.3: step 1 output contains 'shacl<0.4,>=0.3.3'; suite 0.24.3: step 1 output contains 'holosdb>=0.24'

---

<a id="c14-35"></a>
### C14.35 — Wrong: stale numbers

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-35) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **Stale numbers in my own pages.**

**Sources:**

- [the previous edition's Chapter 8](https://github.com/pwin/SemOpsManual/blob/fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40/docs/08-model-and-validate.md#L326): “close to 300 findings” (quote found, checked 2026-10-22)

Today's figures are reproduced in C09.02 (479), C09.04 (23) and C07.22 (22 or 23).

---

<a id="c14-36"></a>
### C14.36 — Wrong: where a CONCAT-built IRI goes

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-36) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Where a `CONCAT`-built IRI goes.**

**Evidence:** the same as [C10.05 — A CONCAT-built IRI: dropped as a subject, a literal as an object](#c10-05), which reproduces it: step 1 exits 0; as a subject: no triples at all; step 2 exits 0; step 2 output contains '<https://acme.example.org/ns/worksIn> "https://acme.example.org/data/department/ENG" .'

---

<a id="c14-37"></a>
### C14.37 — Wrong: when rules arrived in the SHACL engine

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-37) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **When rules arrived in the SHACL engine.**

**Evidence:** the same as [C11.03 — Rules shipped in 0.1.8; the $this fix came with them](#c11-03) (cited from upstream).

---

<a id="c14-38"></a>
### C14.38 — Wrong: the SHACL engine's pass rate

**In the manual:** [Chapter 14, at the claim](manual/docs/14-coverage-and-gaps.md#ev-c14-38) · [plain edition](../docs/14-coverage-and-gaps.md#things-this-manual-had-wrong)  
**Kind:** Cited from upstream · **Result:** Cited from upstream

> **The pass rate of the SHACL engine**, which I would have written as 426 of 426.

**Evidence:** the same as [C11.08 — 425 of 426 W3C tests, the exception named](#c11-08) (cited from upstream).

---

<a id="chapter-15"></a>
## 15. Adoption roadmap

Annotated chapter: [manual/docs/15-adoption-roadmap.md](manual/docs/15-adoption-roadmap.md) · plain chapter: [../docs/15-adoption-roadmap.md](../docs/15-adoption-roadmap.md)

<a id="c15-01"></a>
### C15.01 — 479 unscoped, 23 scoped, four false with --exclude-imports

**In the manual:** [Chapter 15, at the claim](manual/docs/15-adoption-roadmap.md#ev-c15-01) · [plain edition](../docs/15-adoption-roadmap.md#week-2--scope-the-registry-then-add-it)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> **Do not skip `--own-namespace`.** Unscoped, the fixture in this manual produces 479

**Evidence:** the same as [C09.04 — --own-namespace gives 23 findings, all Acme's](#c09-04), which reproduces it: step 1: 23 findings (1 V, 22 W, 0 I); own/full_results.csv: {'LOG-001': 1, 'QUA-001': 1, 'QUA-004': 1, 'QUA-009': 9, 'QUA-010': 9, 'STR-003': 1, 'STY-002': 1}; every focus node starts with https://acme.example.org/ns/

479 is C09.02, the four false findings C09.03, the 23 every time C09.04.

---

<a id="c15-02"></a>
### C15.02 — --output-data is not optional

**In the manual:** [Chapter 15, at the claim](manual/docs/15-adoption-roadmap.md#ev-c15-02) · [plain edition](../docs/15-adoption-roadmap.md#week-3--the-pipeline-stages)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Two things are not optional in practice. `--output-data` is one: without it,

**Evidence:** the same as [C12.12 — pattern-consistency catches MKT only from the output data](#c12-12), which reproduces it: step 2 output contains '[undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT'; step 2 exits 0; step 3 output contains 'No modelling-pattern inconsistencies found'; step 4 output contains '[undeclared_property] http://xmlns.com/foaf/0.1/mbox', '[undeclared_property] http://xmlns.com/foaf/0.1/name'; step 5 output contains 'department/ENG', 'department/QA', 'department/SALES'; step 5 output has none of 'MKT'

---

<a id="c15-03"></a>
### C15.03 — PYTHONHASHSEED for docgen

**In the manual:** [Chapter 15, at the claim](manual/docs/15-adoption-roadmap.md#ev-c15-03) · [plain edition](../docs/15-adoption-roadmap.md#week-4--documentation-and-artefacts)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> Publish it. The `PYTHONHASHSEED` is a workaround, not decoration. Without it

**Evidence:** the same as [C13.12 — Three runs, three pages; pinned, one](#c13-12), which reproduces it: three unpinned runs gave 3 different pages; two runs with PYTHONHASHSEED=0 gave the same page

---

<a id="chapter-a"></a>
## Appendix A — Diagram and brand conventions

Annotated chapter: [manual/docs/diagram-style.md](manual/docs/diagram-style.md) · plain chapter: [../docs/diagram-style.md](../docs/diagram-style.md)

<a id="ca-01"></a>
### CA.01 — All six fills clear 12:1 against the text colour

**In the manual:** [Appendix A, at the claim](manual/docs/diagram-style.md#ev-ca-01) · [plain edition](../docs/diagram-style.md#a6-accessibility)  
**Kind:** Reproduced here · **Result:** **PASS** (2026-10-22)

> - Palette contrast: all six fills carry the `#14243A` text colour at a contrast

**Commands** (from the `evidence/` folder):

```bash
python scripts/contrast.py
```

<details><summary><code>scripts/contrast.py</code></summary>

```python
"""Appendix A §A.6: the contrast of the diagram text colour on each palette fill.

    python scripts/contrast.py

WCAG 2 contrast ratio, (L1 + 0.05) / (L2 + 0.05), using relative luminance.
"""
FILLS = {"human": "#FFE6DA", "ci": "#D9F4FA", "data": "#ECF7D5", "ops": "#D9F5EC",
         "govern": "#FFF0D6", "gap": "#F1F3F5"}
TEXT = "#14243A"


def lum(hex_colour: str) -> float:
    def ch(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


lowest = None
for name, fill in FILLS.items():
    ratio = (lum(fill) + 0.05) / (lum(TEXT) + 0.05)
    lowest = ratio if lowest is None else min(lowest, ratio)
    print(f"{name:7} {fill} with {TEXT}: {ratio:5.2f}:1")
print(f"lowest {lowest:.2f}:1")
```

</details>

**What is checked:** the lowest WCAG 2 contrast ratio of the six fills against #14243A is 13.09:1

**Recorded result:** PASS — step 1 output contains 'lowest 13.09:1'

<details><summary>Output, as recorded</summary>

```text
$ python scripts/contrast.py
human   #FFE6DA with #14243A: 13.09:1
ci      #D9F4FA with #14243A: 13.60:1
data    #ECF7D5 with #14243A: 14.02:1
ops     #D9F5EC with #14243A: 13.57:1
govern  #FFF0D6 with #14243A: 13.91:1
gap     #F1F3F5 with #14243A: 14.06:1
lowest 13.09:1
[exit 0]
```

</details>

---

<a id="ca-02"></a>
### CA.02 — FOAF is published as RDF/XML

**In the manual:** [Appendix A, at the claim](manual/docs/diagram-style.md#ev-ca-02) · [plain edition](../docs/diagram-style.md#a8-the-mark)  
**Kind:** Argument · **Result:** Argument

> real-world vocabularies (FOAF among them, as Chapters

The fixture's copy is `fixtures/acme_robotics/reference_vocab/foaf.rdf`, parsed as RDF/XML in C03.01 and C14.06.

---

