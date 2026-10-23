<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# 14. Coverage and gaps

> *Part IV — The ledger*

A manual that only describes what works is marketing. This chapter is the
counterweight: **what SemOps asks for, what the toolchain actually delivers, and
what it does not.**

Three kinds of entry appear below. *Gaps* are things SemOps requires that these
tools do not do at all, usually because they are somebody else's job. *Rough
edges* are things the tools do, with behaviour worth knowing before it costs you
an afternoon; every one was hit while preparing this edition. And, new this time,
*early* capabilities: things that exist, run and were verified, but that the
component providing them calls early and lists gaps for, openly. I would rather
you knew which is which.

---

## 14.1 Coverage by pipeline stage

| Stage | SemOps wants | Covered? | By what |
|---|---|---|---|
| **1 · Source control** | Artefacts as code, semantic versioning | **Partial** | `version-diff` supplies the semver evidence; the DSL makes an ontology literally source code; Git is Git |
| **2 · Modelling & local validation** | Model and validate before CI | **Yes** | VS Code extension and its DSL; `ontology`, `checks` |
| **3 · CI checks** | Reject bad semantic changes automatically | **Yes** | `--fail-on`, `--own-namespace`, `sketch`, `--themes` |
| **4 · Build & packaging** | Containers, Helm charts, RDF bundles | **No** | Docker, Helm: not semantic work |
| **5 · CD to environments** | GitOps, environment promotion, IaC | **No** | Argo CD, Flux, Terraform |
| **6 · Ingestion & ETL** | Orchestration, incremental load, provenance | **Partial** | `sketch`/`tarka`/`data` for transformation and quality, `--graph` for per-source graphs; **no orchestration** |
| **7 · Runtime validation** | Enforce constraints against the live store | **Yes** | `consistency-remote` |
| **8 · Observability** | Metrics, dashboards, log analysis, anomaly detection | **No** | Prometheus, Grafana, Loki |
| **9 · Consumption** | APIs, search, data products | **Partial** | `docgen`; an embeddable store that answers each caller per policy (**early**); **no API layer** |

Three of nine covered, three partially, three not at all. The last edition's
sentence said "five of nine substantially covered" while its own table said three;
this one matches its table. The three not covered (packaging, deployment and
observability) are still the *least* semantic, and have mature general-purpose
answers.

---

## 14.2 Coverage by operating-model layer

| Layer | Covered? | What is real | What is missing |
|---|---|---|---|
| **1 · Strategy & Governance** | **Partial** | Evidence for decisions; read access policy and classification enforced by an embeddable store (**early**) | Approval workflows, stewardship registry, audit trails |
| **2 · Semantic Development** | **Yes** | Authoring (Turtle or script), validation, SHACL, custom checks, docs, versioning | Nothing significant |
| **3 · Semantic CI/CD** | **Partial** | Validation is comprehensive | Packaging and deployment entirely absent |
| **4 · Data Integration** | **Partial** | Transformation (TARQL and OTTR), quality checks, conformance, per-load named graphs | Scheduling, incremental load, retry, streaming, provenance stamping |
| **5 · Platform & Infrastructure** | **No** | Only the access policy an embedded store enforces | Triple-store operations, Kubernetes, backup, search index |
| **6 · Knowledge Consumption** | **Partial** | Live-store checking, reference documentation, an embeddable store with per-caller answers | APIs, search, dashboards, self-service |

**Layer 1's caveat stands, with one addition.** No tool approves a change. What
the suite does is make sure the approver is looking at evidence: *this removes a
class, therefore MAJOR; this query breaks; this repair is 100% confident.* What
an embeddable store with policy adds is enforcement of *who may see what*, for
every query anyone could write. The decision stays human, and should.

---

## 14.3 Coverage of the ten SemOps elements

| # | Element | Covered? | Where |
|---|---|---|---|
| 1 | Knowledge Lifecycle Management | **Yes** | [Ch. 12](12-release-and-change.md) |
| 2 | Automated Deployment & Packaging | **No** | — |
| 3 | Data Integration & ETL Orchestration | **Partial** | [Ch. 10](10-ingest-and-transform.md): no orchestration |
| 4 | Reasoning & Inference Operations | **Partial** | [Ch. 11](11-rules-and-inference.md): rules, RDFS closure, rule versioning and tests, materialisation into a droppable graph (`holos rules`); **incremental** reasoning and performance monitoring no |
| 5 | Knowledge Graph Observability | **No** | See [§14.5](#145-the-cheapest-thing-you-are-not-doing) |
| 6 | Semantic Governance & Access Control | **Partial** | Evidence yes; read policy at the scan and classification (**early**, [Ch. 13](13-operate-and-consume.md)); workflow no |
| 7 | Semantic CI/CD Pipelines | **Partial** | Linting, SHACL, docs yes; packaging and deployment no |
| 8 | Tooling Integration | **Partial** | Validator, reasoner, CI, triplifier, embeddable store (**early**) yes; triple-store operations, Kubernetes and monitoring no |
| 9 | Knowledge Products & APIs | **No** | No API layer; `holosdb` is an engine to build one with ([Ch. 13](13-operate-and-consume.md)) |
| 10 | Documentation & Semantic Literacy | **Yes** | `docgen`, generated docs, this manual |

Two partials grew since the last edition: access control (6), which now has an
enforcement mechanism as well as evidence, and reasoning operations (4), which
gained materialisation. Both rest on HOLOS, the youngest component here. Read them
as "possible now, and worth piloting", not "solved".

---

## 14.4 Rough edges, all met while preparing this edition

Each of these is real and reproducible at the versions in
[Chapter 7](07-the-toolchain.md), and none is a reason not to use the tools. All
are reasons to read this section first. The first four are new, and they share a
shape I have come to look for everywhere: **a run that checked nothing, or lost
the evidence that it could not check, reporting success.**

### A scoped run could not see that the reasoner did not run (fixed in 0.24.0)

`--own-namespace` keeps findings whose focus node starts with your prefix.
`REA-022`, "the DL reasoner could not run", is about the synthetic `oq:Graph`,
so up to 0.23.0 a scoped `data` or `run` silently dropped it. Three scoped
`data` runs on the fixture reported 54 findings with neither `REA-021` nor
`REA-022` present: the report could not distinguish *"HermiT found nothing"*
from *"HermiT never started"*. Earlier editions told you `REA-022`'s presence
would tell you; in a scoped run on those versions it never could.

It was worse than one missing finding. `oq:Graph` is the suite's anchor for any
check with no natural focus node, so scoping also dropped `EFF-002`,
`STY-005`, `REA-020` and `QUA-005`. `QUA-005` is the sharpest of them: it fires
when an ontology has no identifying IRI, and an ontology with no IRI has no
namespace of its own to match, so scoping removed the finding that says so.

**Fixed in 0.24.0**, which was this edition's *suggested improvement* taken up:
findings about the run survive the filter. They are kept without counting as
*matches*, so the near-miss warning still fires on a run where nothing of yours
was found. The scoped fixture run stayed at 54 findings while its composition
changed -- see [Chapter 10](10-ingest-and-transform.md) §10.4, which is also
where the mitigation for 0.23.0 and earlier still lives.

### The `shacl` CLI reported conformance when it checked nothing (fixed in 0.3.4)

The one-shot Python and JavaScript calls have refused a shapes graph that declares
no shapes since 0.2.0. Up to 0.3.3 the CLI did not: it printed `conforms: true` and
exited 0, and because `-s` defaults to the data graph, `shacl -d data.ttl` with the
`-s` forgotten did the same. *Fixed in engine 0.3.4*, which refuses both with exit 2
and a message for each, and keeps the old answer behind `--allow-no-shapes`
([Chapter 11](11-rules-and-inference.md) §11.1). Pass `-s` in automation anyway.

### `holos validate` exited 0 on a non-conforming graph (fixed in 0.22.0)

Up to 0.21.1 both of its validators printed `conforms false` and returned exit
status 0, a non-zero status being reserved for "could not validate". So a CI step
built on it passed on the violations it was there to stop. *Fixed in HOLOS 0.22.0*,
which exits 0, 1 or 2 as the `shacl` CLI does, and defaults to the same `adapted`
validator as `Store.validate()`. On 0.21.x, gate with the `shacl` CLI, or use
`Store.validate()` from Python, which returns a dictionary with a `conforms` key.

### tarka dropped instances it could not build, silently (fixed in 0.2.0)

Up to 0.1.1, an OTTR template whose `ottr:IRI` parameter received a cell tarka
did not accept as an IRI (a `mailto:…` value, with no `mailto:` prefix declared)
dropped the instance if the parameter was mandatory, or the triple if it was
optional. No message, exit 0. On the acme mapping, that was every row, and
`Mapping.ottr(...).run_csv(...)` in the Python package wrote 0 triples and raised
nothing. *Fixed in tarka 0.2.0*, which was this edition's *suggested
improvement* taken up: `run` reads a cell typed `ottr:IRI` as bOTTR does, so
`mailto:…` needs no prefix, and leaves out a row with a cell its parameter cannot
take, naming the row and the column, writing the others and exiting 1, as bOTTR
does. In Python, `triplify`, `write` and `run_csv` raise a `ValueError` listing
the rows left out, once the rest is written, unless `strict=False` is given
([Chapter 10](10-ingest-and-transform.md) §10.3).

### `docgen` reshuffles the page on every run

Still open at 0.24.1, re-checked rather than carried forward: three identical runs
produce three different files. The *content* is canonical; the **order** of every
top-level list varies per run.

**The cause is one level below `docgen`.** The parser is an adapter over rdflib;
rdflib's in-memory store holds triples in a **`set`**, set iteration follows
element hashes, rdflib's terms subclass `str`, and Python randomises string
hashing per process. Everything downstream faithfully preserves that arbitrary
order. The suite's move to holosdb changed who *evaluates* and left rdflib
*parsing*, so it did not touch this.

It reaches the rendered page, not just the JSON, so **two readers of the same
ontology on the same commit are handed the terms in a different sequence.** For
the artefact [Chapter 2](02-people-and-cognition.md) nominates as the answer to the
priesthood problem, a random reading order is a poor property.

*Workaround:* `PYTHONHASHSEED=0`, re-verified: two runs, one hash. *Suggested
improvement:* sort on the way out, by each subject's offset in the source, which
the extractor already computes, giving **document order**. Reported upstream as
[issue #3](https://github.com/pwin/consolidated-ontology-quality-suite-python/issues/3),
still open, with no comments yet ([Ch. 13](13-operate-and-consume.md)).

### The DL reasoner fails on some hash seeds, not at random

Every edition of this manual, this one included until the last week of writing it,
said the DL reasoner "starts, or does not, at random". On the fixture it did seem
to: across this edition's runs HermiT ran five times in ten from `ontology`. When it
failed, the suite emitted `REA-022` carrying an internal error, *cannot access local
variable 'entity'*; when it worked, `REA-020` and `REA-021` (only `REA-021` from
0.23.0, below).

It is not random, and it is not HermiT. Building the evidence for this edition, I
replayed the suite's reasoner bridge on its own and read the traceback. The failure
happens in **owlready2's loader**, before HermiT or Java is ever called. Loading the
merged ontology, owlready2 0.51 builds a Python class for FOAF's
`foaf:primaryTopic`, which is typed both functional and object property and is a
sub-property of `foaf:topic`. In some orders those types give Python an inconsistent
class hierarchy. owlready2 catches the resulting `TypeError`, handles it only if its
message starts with "metaclass conflict", and otherwise drops it, leaving a variable
unassigned. Hence `'entity'`.

The order comes from iterating a `set`, which follows Python's per-process string
hashing: the same cause as `docgen`'s reshuffled pages, one entry down. So the
outcome is set, almost entirely, by `PYTHONHASHSEED`. On this fixture seed 5 ran
HermiT in ten runs out of ten, and seed 0 failed in eighteen of twenty.

*Almost*, because I had first written "every time", and the evidence for this
edition caught me out twice. Loaded straight into owlready2 under seed 0, the
merged file fails about seven times in eight, every failure on
`foaf:primaryTopic`, and under seed 5 it loads every time I have tried. So the
seed decides most of it, and something else decides the rest. My first
explanation was the random name of the temporary directory the bridge loads from;
my second was rdflib's blank-node labels, which are random in every process. Fixing
both left the odd load still going the other way. I have not found the remaining
cause, and I would rather say so than offer a third guess. With Java hidden as
well, the message changes to the operating system's "cannot find the file
specified", so a genuinely missing Java *is* distinguishable from this.

*Mitigation:* set `PYTHONHASHSEED` for the whole CI job. That doesn't make HermiT
work, but it turns a coin someone tosses for you on every push into one that lands
the same way nine times in ten, and it pins `docgen` completely. Have the job
record which verdict it got, `REA-021` or `REA-022`, rather than assume one.
*Suggested improvements:* in owlready2, handle or re-raise the `TypeError` rather
than drop it, which is the real fix, since a load that cannot fail cannot fail at
random either; and in the suite's bridge, name the entity that failed to load, so
`REA-022` says something a reader can act on.

What made it safe to depend on throughout is that the failing path said so loudly
instead of reporting success. Combine that with the first entry above, though:
loud only helps if the filter lets you hear it. And the episode is a lesson I
should have learned from the first: **"random" is usually a cause nobody has found
yet.**

### `REA-020` said "inconsistent" when one class was unsatisfiable (fixed in 0.23.0)

When HermiT does run on the fixture, suite 0.22.0 reports `REA-020`, *"the
ontology … is logically inconsistent … no model satisfies every axiom
simultaneously"*, beside `REA-021` for `acme:Contractor`. The ontology is not
inconsistent. Nothing is asserted to be a Contractor, so a model exists, and
HermiT agrees: run through owlready2 directly, it raises no inconsistency. What it
reports is two unsatisfiable classes, `acme:Contractor` and `owl:Nothing`, which
is unsatisfiable by definition. The suite's bridge had a belt-and-braces rule that
read `owl:Nothing` in that list as an inconsistent ontology, and owlready2 lists it
whenever any class is unsatisfiable. A clean ontology gives an empty list and no
`REA-020`; one unsatisfiable class gave both findings.

The exit status never changed, since `REA-021` is a Violation too. What changed was
where the finding sent a reader: inconsistency means hunting for the individual
that asserts the contradiction, unsatisfiability means reading one class's own
axioms. Two different searches, and it named the wrong one.

*Fixed in suite 0.23.0*, which reports inconsistency only when `owl:Thing` is
unsatisfiable. That narrowing is safe because a genuinely inconsistent ontology
never reaches the rule: owlready2 raises, and the bridge reports `REA-020` on its
own. The testing repository's fixture for the case, `03b-unsatisfiable-class`,
expected `REA-021` and forbade three other ids but not `REA-020`, so the false
finding passed the test written for it; it now forbids `REA-020` too
([6cdfb14](https://github.com/pwin/consolidated-ontology-quality-suite-python-testing/commit/6cdfb14a3c2857b61dcb32f49f56a4829b0d0664)),
with fixture `13`, which does assert an individual into an impossible class, as the
contrast. *On 0.22.0:* read `REA-020` as real only when it arrives without
`REA-021`.

### The SHACL engine cannot scope validation to a named graph

Quad syntaxes parse, and then every named graph and the default graph are merged
into one before validation, because SHACL is defined over a single data graph.
There is no graph-selection option and no per-graph report.

*Mitigation:* named graphs remain the right call for provenance and lifecycle
([Ch. 3](03-across-the-boundary.md)). For per-graph validation, extract the graph
and validate it on its own, as `consistency-remote`'s manifest model does
([Ch. 13](13-operate-and-consume.md) §13.1).

### A mistyped manifest `role` compared nothing, successfully (fixed in 0.24.0)

`consistency-remote` accepted any string as a graph's `role` and ignored all but
`"ontology"` and `"triplified_data"`. A hyphen for an underscore yielded a run
that compared nothing and exited 0, even with `--fail-on-misalignment`. The role
is declared as a typing `Literal`, which nothing enforces at runtime, so the typo
loaded happily and then matched neither list. Re-verified at 0.23.0.

**Fixed in 0.24.0**: an unknown role is refused when the manifest loads, and the
message names every bad role in the file at once together with the valid set.
The mitigation is still worth doing on any version -- point it at a graph you
know is wrong, once, and watch it complain
([Ch. 13](13-operate-and-consume.md) §13.1).

### Smaller ones, all worth a line

| What | Where you meet it |
|---|---|
| At 0.22.0, `--help` offers `--inference owlrl` and `both`, and asking for one gives a Python traceback rather than a one-line error. *Fixed in 0.23.0* | [Ch. 7](07-the-toolchain.md) §7.4 |
| At 0.22.0, `--inference` reaches the shapes only: ignored under `--engine sparql`, and under the default engine the two arms check different graphs. *Fixed in 0.23.0*, with engine 0.3.3's `shacl.rdfs_closure` | [Ch. 7](07-the-toolchain.md) §7.4 |
| Up to 0.23.0, the `--own-namespace` near-miss warning lists two blank-node identifiers among the "namespaces actually seen". The guard meant to stop it tested for a `_:` prefix, which `rdflib`'s blank-node labels do not carry, so it never fired. *Fixed in 0.24.0*: every namespace offered has a scheme | [Ch. 9](09-continuous-integration.md) §9.4 |
| `--sparql` composes but `--registry` replaces, so adding `@builtin` with a house registry turns every built-in finding `UNMAPPED`. Up to 0.23.0 the warning also recommended an absolute path rather than `@builtin`, in the release that added `@builtin` because a committed path is wrong on every other machine -- *that half fixed in 0.24.0*; the `--registry` half is open | [Ch. 8](08-model-and-validate.md) §8.5 |
| Up to 0.23.0, `data` and `run` report one contradiction as two `LOG-001`s, one from the registry pass and one from the `owlrl` closure. *Fixed in 0.24.0* by deduplicating across the join, which merged two pairs on the fixture rather than the one reported | [Ch. 9](09-continuous-integration.md) §9.6 |
| At 0.24.0, a manifest with an unknown graph `role` is refused -- correctly -- but as a Python traceback rather than a one-line error, the same shape `--inference owlrl` had until 0.23.0. *Fixed in 0.24.1*, which reports it as one line and exits 2 rather than 1; the exit is non-zero on both | [Ch. 13](13-operate-and-consume.md) §13.1 |
| Up to 0.16.0, the DSL gives unchecked code an internal `TypeError`, and its bundled `Quad` type is not assignable to `@types/n3`'s. *Fixed in 0.16.1* | [Ch. 8](08-model-and-validate.md) §8.2 |
| The suite's `triplify` and the extension's *Run Full Triplify* drive `oxi-gen` only; neither knows tarka | [Ch. 10](10-ingest-and-transform.md) §10.3 |
| `consistency` and `pattern-consistency` exit 0 whatever they find unless told otherwise. Up to 0.23.0 that meant `--fail-on-misalignment` or `--fail-on-mismatch`, two names for one idea, neither of them the `--fail-on` every other subcommand takes. *Fixed in 0.24.0*: `--fail-on-anything` on all three, with the old names kept as aliases | [Ch. 12](12-release-and-change.md) §12.6 |
| Up to 0.21.1, the `holos validate` command defaults to the `native` engine and `holosdb`'s `Store.validate()` to `adapted`, so the same words run different validators. *Fixed in 0.22.0* | [Ch. 13](13-operate-and-consume.md) §13.2 |
| At 0.22.0, when two query files bind one prefix differently, `sketch` reads every file with the first file's binding: the others' terms are reported as undeclared, or, if the odd file sorts last, its mistake is not reported at all. *Fixed in 0.23.0* | [Ch. 10](10-ingest-and-transform.md) §10.6 |

### Documentation drift, upstream

None of these changes what a tool does. All of them change what a careful reader
believes, which is how I came to carry one false claim for two months
(§14.6).

- The suite's `REPORTS.md` dates the report-set change to 0.15.0; it shipped in
  0.17.0.
- At 0.22.0 the suite's `--engine` help still describes pyshacl: `both` "runs
  pyshacl", and `native` is "not a default dependency". Rewritten in 0.23.0.
- The suite's `REASONING.md` calls `owlready2` the `reasoner` extra; it has been a
  base dependency since the first commit. What is optional is Java.
- The extension's `README.md` still names Oxigraph among its engines; it went in
  0.13.11.
- The testing repository's README says sixteen fixtures and "18 Turtle files in 10
  folders"; there are seventeen fixtures in fourteen folders.
- The suite's `main` branch stopped at 0.18.0 while releases were tagged on
  `develop`, now the default branch, until it caught up with 0.23.0. This manual
  links `develop`.

---

## 14.5 The cheapest thing you are not doing

Worth isolating because it is nearly free and almost universally skipped:

> **Every check run writes `full_results.csv`. Keep them, timestamped.**

That is a time series of semantic quality, produced by CI runs you are already
paying for. Findings by severity and by check id over time is a real data-quality
KPI, the closest thing to observability available without a Prometheus stack.
Since 0.17.0 each row carries `source_file` and `line`, so you can also see
*where* the findings are accumulating.

Watch the **Warning trend** specifically. Violations get fixed because they break
the build; Warnings accumulate quietly, and an accumulating Warning count is the
observable signature of decay, visible in your own artefacts a year before anyone
notices the model has drifted.

**Trend the scoped runs, and note your suite version beside each point.** The
unscoped total is now reproducible run to run, but it still moves when the
registry grows, as it did from 50 checks to 61, and the scoped run is the one whose
movement is about *your* model. A jump that coincides with an upgrade is the rules
moving, not the model decaying.

---

## 14.6 What has changed since the last edition

The picture is not static, and this edition has two lists to give you: what got
better, and what I had wrong.

### Gaps and rough edges that have closed

**The engines are the toolchain's own.** The suite's 44 portable checks run on
holosdb and its shapes on the native SHACL engine; the extension runs the same two
engines compiled to WebAssembly. On the suite's stress fixture every engine mode
reports the same findings as the old rdflib-and-pyshacl baseline, and on this
manual's fixture every count in [Chapter 9](09-continuous-integration.md) came out
unchanged. Third-party engines stay as test-time witnesses
([Ch. 7](07-the-toolchain.md) §7.1).

**Messages on blank nodes.** `STY-003` and `EFF-001` built messages out of blank-node
labels, which rdflib rendered as gibberish and conformant engines dropped
altogether. Both are fixed, in both repositories, along with the cross-engine dedup
of anonymous findings.

**Findings say where they are.** `findings.txt` quotes the source line;
`full_results.csv` carries `source_file` and `line`; the TARQL checks carry their
position as fields rather than prose; and six report files that restated each
other are gone.

**House rules compose with the built-ins.** `--sparql` is repeatable, `@builtin`
names the suite's own tree on any install, and a run that leaves the built-ins out
says so. `--reports minimal` and `--themes` are new. Query and data globs have one
name everywhere.

**Five suite defects found by the testing repository**: a crash on
language-tagged literals against an `xsd:` range, per-row entities misreported as
taxonomy references, the tool's own namespace legend landing in the project's
namespace, an ontology's own default namespace reported as undeclared, and
`--sparql` silently replacing the built-in tree.

**`sh:conforms` means what the specification says**, from engine 0.3.0, and the
WebAssembly build agrees from 0.3.2 ([Ch. 11](11-rules-and-inference.md) §11.1).

**Three suite defects this edition found are fixed in 0.23.0**: `REA-020` no
longer reports an inconsistent ontology for an unsatisfiable class (§14.4);
`--inference rdfs` reaches every engine, through one closure made by the SHACL
engine ([Ch. 7](07-the-toolchain.md) §7.4); and `sketch` reads each mapping with
its own prefixes ([Ch. 10](10-ingest-and-transform.md) §10.6). Engine 0.3.3 was
cut for the second, to hand the closure out.

**Six more are fixed in 0.24.0**, and they share a shape worth naming: every one
of them made a run look cleaner, or more complete, than it was, and none of them
raised an error. Findings about the run survive `--own-namespace`, so a scoped
gate can see that the reasoner did not run -- this edition's own suggested
improvement, and four graph-wide checks besides `REA-022` were being dropped the
same way (§14.4). `REA-022` now quotes the line of the ontology that defeated the
loader, instead of a position in a temporary file deleted before you read the
report. An unknown graph `role` is refused when a manifest loads, rather than
comparing nothing and exiting 0 (§14.4). `data` and `run` report one
contradiction once ([Ch. 9](09-continuous-integration.md) §9.6). The
`--own-namespace` near-miss warning no longer offers blank-node labels as
namespaces, and the `--sparql` warning names `@builtin` rather than an absolute
path. And `--fail-on-anything` is one name on `consistency`,
`consistency-remote` and `pattern-consistency`, with the old two kept as aliases
([Ch. 12](12-release-and-change.md) §12.6).

Two of those six were defects in 0.23.0's own fixes, found by re-reading them
rather than by running anything: the blank-node guard tested for a `_:` prefix
that rdflib's labels do not carry, so it never fired, and it was pinned by a test
feeding it a string the suite never produces -- the test passed while the code
did nothing. The lesson is the one [Chapter 9](09-continuous-integration.md) §9.4
already draws about gates: a check you have never seen fail is not yet a check.

**Gates that could not fail, now can**: the `shacl` CLI refuses to validate
against no shapes from engine 0.3.4 ([Ch. 11](11-rules-and-inference.md) §11.1),
and `holos validate` exits 1 on a non-conforming graph from HOLOS 0.22.0, with
the same default validator as Python (§11.8). And the DSL's two rough edges are
fixed in 0.16.1: unchecked code gets an error that names its mistake, and
`build().quads` goes to n3's `Writer` without a cast
([Ch. 8](08-model-and-validate.md) §8.2).

**HOLOS validation leaves the store as it found it**, from 0.21.1. Up to 0.21.0 it
wrote the shapes into the store it validated, a copy per call, and on disk for
good. This edition's evidence found it and the fix was cut the same day, with a
note naming the `DROP GRAPH` for anything an earlier version left
([Ch. 13](13-operate-and-consume.md) §13.2).

**The repair engine** keeps blank nodes and base directions intact when it writes
back into your file ([Ch. 8](08-model-and-validate.md) §8.1).

**Early, but real:** read access policy at the index scan, with classification,
in an embeddable store (`holosdb`); rule materialisation into a droppable graph
(`holos rules`); and a triplifier of the toolchain's own, with OTTR and data
frames (`tarka-rdf`).

### Things this manual had wrong

**The migration annotation's direction.** Every earlier edition said rename
detection reads `owl:equivalentClass` in one direction only, and that writing it the
other way silently drops confidence. It has read both directions at full confidence
since suite 0.3.5, released the day before this manual's first commit. Only
`dcterms:isReplacedBy` is directional, as its meaning requires
([Ch. 12](12-release-and-change.md) §12.3). The notebook cell I wrote to demonstrate
the drop printed 100% both ways every time it ran.

**`REA-022` as the reasoner's tell in a scoped run.** It was filtered out of
scoped runs up to 0.23.0 (§14.4), so its absence there said nothing. The advice
was right in principle and wrong about the tool, which is the more awkward way
to be wrong: 0.24.0 keeps the finding, so on that version the original advice
holds. Check what you are running before relying on it.

**The reasoner as "flaky".** Every edition called HermiT's failures random and blamed
the bridge to it. They are deterministic for a given `PYTHONHASHSEED`, and they
happen in owlready2's loader before HermiT runs (§14.4).

**The reasoner as an "optional extra".** `owlready2` installs with the suite. What
is optional, and what the graceful fallback covers, is the Java runtime HermiT
needs ([Ch. 4](04-from-research-to-industry.md)).

**Stale numbers in my own pages.** The last edition's [Chapter 8](08-model-and-validate.md),
this chapter and the roadmap still said the unscoped run gave "close to 300
findings, of which 5 are yours", and that it drifted between runs; and §7.4's engine
table showed 4 and 5 findings. All four had been true at some point and none was
true when published. The figures throughout are now 479, 23, and 22 or 23, and the
unscoped run does not drift.

**`REA-020` as a third confirmation.** Every edition counted it, with `LOG-001`
and `REA-021`, as one more witness to the fixture's contradiction. The ontology is
consistent; `REA-020` is an artefact of how the bridge reads owlready2 (§14.4).

**Where a `CONCAT`-built IRI goes.** Earlier editions said it becomes a string
literal while "the counts look right". That is true only where it is an object. As
a subject it produces nothing at all, because every triple built on it is dropped
([Ch. 10](10-ingest-and-transform.md) §10.2).

**When rules arrived in the SHACL engine.** The last edition's version history
described builds from source rather than releases. Rules first shipped in 0.1.8,
and the `$this` fix I credited to 0.1.9 came with them, before any release had
rules at all ([Ch. 11](11-rules-and-inference.md) §11.1).

**The pass rate of the SHACL engine**, which I would have written as 426 of 426.
It is 425, deliberately ([Ch. 11](11-rules-and-inference.md) §11.1).

The lesson of the last edition still holds and has teeth: **re-verify the gaps list
against the tools you actually have.** This edition adds its mirror image, which is
harder: **re-verify the warnings you give, not only the capabilities and the
limitations.** A warning that has stopped being true costs readers effort they did
not need to spend, and nobody goes looking to disprove a warning they have been
given.

---

## 14.7 What to do about the real gaps

| Gap | Practical answer |
|---|---|
| Packaging and deployment | Standard container and Helm tooling. A triple store deploys like any stateful service |
| Orchestration | Airflow, Argo Workflows or Prefect, calling these commands as steps |
| Observability | Prometheus and Grafana, plus retained `full_results.csv` as the semantic-quality series |
| APIs and knowledge products | Application development. Embed the engine in the service; `holosdb` brings access policy with it ([Ch. 13](13-operate-and-consume.md)) |
| Approval workflows, RBAC | Branch protection rules and your existing identity platform; read policy in the store where you embed one. The tools supply the evidence; the platform enforces the policy |
| Incremental and streaming ingestion | Your pipeline's responsibility. These commands are batch |
| Provenance capture | Named graphs at load time (`tarka --graph`). Decide before your first production load |
| The suite's `triplify` needs `oxi-gen` | Triplify with tarka and point `data` at its output |

Earlier editions ended this chapter with a tidy sentence: **the parts of SemOps that
need specialist tooling are covered, and the parts that are not covered do not need
specialist tooling.** It is still mostly true. The honest amendment is that the
toolchain now includes a specialist store, and specialist stores are exactly where
a young component needs the most patience. Pilot it where its guarantee matters to
you, answers that respect who is asking, and keep a mature store where it doesn't.

---

| ← [13. Operate and consume](13-operate-and-consume.md) | [15. Adoption roadmap →](15-adoption-roadmap.md) |
|---|---|
