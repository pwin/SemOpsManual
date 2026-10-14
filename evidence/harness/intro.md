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
  at `6d078a1`, lets C09.15 and C09.16 run its test suite and competency board.
  Use a clone you do not mind it writing into: both rewrite generated files. That
  repository installs the suite from a sibling checkout,
  `../consolidated_ontology_suite_python` (at `v0.22.0` for the recorded run), and
  its competency tests triplify with oxi-gen, which the suite finds through
  `ONTOLOGY_SUITE_OXI_GEN_BIN`.
- `EVIDENCE_REPOS`, the folder holding local clones of the six repositories
  (default: the folder above the manual), lets `verify.py` check the quoted
  sources. `verify.py --sources` checks them without running anything else.

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
