<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# 14. Coverage and gaps

> *Part IV — The ledger*

A manual that only describes what works is marketing. This chapter is the
counterweight: **what SemOps asks for, what the toolchain actually delivers, and
what it does not.**

Two kinds of entry appear below. *Gaps* are things SemOps requires that these
tools do not do at all — usually because they are somebody else's job. *Rough
edges* are things the tools do, with behaviour worth knowing before it costs you
an afternoon; every one of them was hit while writing this manual.

---

## 14.1 Coverage by pipeline stage

| Stage | SemOps wants | Covered? | By what |
|---|---|---|---|
| **1 · Source control** | Artefacts as code, semantic versioning | **Partial** | `version-diff` supplies the semver evidence; Git is Git |
| **2 · Modelling & local validation** | Model and validate before CI | **Yes** | VS Code extension; `ontology`, `checks` |
| **3 · CI checks** | Reject bad semantic changes automatically | **Yes** | `--fail-on`, `--own-namespace`, `sketch` |
| **4 · Build & packaging** | Containers, Helm charts, RDF bundles | **No** | Docker, Helm — not semantic work |
| **5 · CD to environments** | GitOps, environment promotion, IaC | **No** | Argo CD, Flux, Terraform |
| **6 · Ingestion & ETL** | Orchestration, incremental load, provenance | **Partial** | `sketch`/`triplify`/`data` do transformation and quality; **no orchestration** |
| **7 · Runtime validation** | Enforce constraints against the live store | **Yes** | `consistency-remote` |
| **8 · Observability** | Metrics, dashboards, log analysis, anomaly detection | **No** | Prometheus, Grafana, Loki |
| **9 · Consumption** | APIs, search, data products | **Partial** | `docgen` produces documentation; **no API layer** |

Five of nine substantially covered, two partially, two not at all. The two not
covered — packaging/deployment and observability — are the two that are *least*
semantic, and have mature general-purpose answers.

---

## 14.2 Coverage by operating-model layer

| Layer | Covered? | What is real | What is missing |
|---|---|---|---|
| **1 · Strategy & Governance** | **Partial** | Evidence for decisions: breaking-change detection, scoped findings, impact analysis | Approval workflows, RBAC, audit trails, stewardship registry |
| **2 · Semantic Development** | **Yes** | Authoring, validation, SHACL, custom checks, docs, versioning | Nothing significant |
| **3 · Semantic CI/CD** | **Partial** | Validation is comprehensive | Packaging and deployment entirely absent |
| **4 · Data Integration** | **Partial** | Transformation, quality checks, conformance | Scheduling, incremental load, retry, streaming, provenance stamping |
| **5 · Platform & Infrastructure** | **No** | — | All of it: K8s, triple-store ops, backup, search index, security |
| **6 · Knowledge Consumption** | **Partial** | Live-store checking, reference documentation | APIs, search, dashboards, self-service |

**Layer 1 deserves its caveat repeated.** No tool approves a change. What this
one does is ensure the approver is looking at evidence — *this removes a class,
therefore MAJOR; this query breaks; this repair is 100% confident* — rather than
at an assertion. The decision stays human, and should.

---

## 14.3 Coverage of the ten SemOps elements

| # | Element | Covered? | Where |
|---|---|---|---|
| 1 | Knowledge Lifecycle Management | **Yes** | [Ch. 12](12-release-and-change.md) |
| 2 | Automated Deployment & Packaging | **No** | — |
| 3 | Data Integration & ETL Orchestration | **Partial** | [Ch. 10](10-ingest-and-transform.md) — no orchestration |
| 4 | Reasoning & Inference Operations | **Partial** | [Ch. 11](11-rules-and-inference.md) — SHACL-AF rules, RDFS closure, rule versioning and regression tests yes; **incremental** reasoning and performance monitoring no |
| 5 | Knowledge Graph Observability | **No** | See [§14.5](#145-the-cheapest-thing-you-are-not-doing) |
| 6 | Semantic Governance & Access Control | **Partial** | Evidence yes; RBAC and workflow no |
| 7 | Semantic CI/CD Pipelines | **Partial** | Linting, SHACL, docs yes; packaging and deployment no |
| 8 | Tooling Integration | **Partial** | Validator, reasoner, CI yes; triple store, K8s, monitoring no |
| 9 | Knowledge Products & APIs | **No** | [Ch. 13](13-operate-and-consume.md) |
| 10 | Documentation & Semantic Literacy | **Yes** | `docgen`, generated docs, this manual |

---

## 14.4 Rough edges, all encountered while writing this manual

Each of these is real, reproducible, and cost time. None is a reason not to use
the tools; all are reasons to read this section first.

### `docgen` reshuffles the page on every run

Three identical runs produce three different files. The *content* is canonical —
hashing the JSON with every collection sorted gives one value across all three —
but the **order** of every top-level list varies per run: classes, properties,
imports, and the sections they are grouped under.

**The cause is one level below `docgen`, which is why sorting the inner
collections did not fix it.** The parser is an adapter over rdflib; rdflib's
in-memory store holds triples in a **`set`**, and `Memory.triples()` yields them
by iterating it. Set iteration order follows element hashes, rdflib's terms
subclass `str`, and Python randomises string hashing per process. Everything
downstream then faithfully preserves that arbitrary order — the extractor's
subject index is a plain dict, so it records the order it was given, and the
output lists are built by walking it.

*The proof, and the workaround:* with `PYTHONHASHSEED=0` set in the
environment, three runs produce one identical hash. Unpinned, three different
ones. Nothing else changes.

**It reaches the rendered page, not just the JSON.** On a fixture with three
`# Section:` headers, five identical runs put the sections in three different
orders, and `ontology-documentation.html` lists classes in a different reading
order each time — interleaved across sections rather than grouped by them. The
variable that feeds this is named `sections_in_order`, and the name is the only
thing asserting an order.

So the cost is not only that the page is undiffable — though it is, and
*"what changed in the reference page this release?"* is the question a reference
page most needs to answer. It is that **two readers of the same ontology, on the
same commit, are handed the terms in a different sequence.** For the artefact
[Chapter 2](02-people-and-cognition.md) nominates as the answer to the
priesthood problem, a random reading order is a poor property.

*Suggested improvement:* sort the three lists on the way out — and there is a
better key than alphabetical available for free. The extractor already computes
each subject's offset in the source text in order to assign its section, so
sorting on that yields **document order**: what the author intended, and the
only order under which the sections stay coherent.

*Still open at 0.14.2*, re-checked for this edition rather than carried forward,
and reported upstream as
[issue #3](https://github.com/pwin/consolidated-ontology-quality-suite-python/issues/3).
([Ch. 13](13-operate-and-consume.md))

### The DL reasoner starts, or does not, at random

The reasoner sometimes emits `REA-022` — *external DL reasoner unavailable*,
with an internal `UnboundLocalError` from the bridge — and sometimes runs
normally and emits `REA-021`, correctly finding `acme:Contractor` unsatisfiable.

An earlier draft of this manual reported this as a difference between the
`ontology` and `data` commands, on the strength of one run of each. That was
wrong, and running the same command repeatedly shows why: three consecutive
`ontology` runs gave `REA-021` (reasoner working) once and `REA-022` twice. It
is per-invocation flakiness, not a code path. The suite's own
`ACME_ROBOTICS_WALKTHROUGH.md` says so directly — HermiT is *"occasionally
environment-flaky in ways unrelated to this fixture (a transient internal error
rather than a real unsatisfiability finding)"*.

*Consequence for your gate:* a scoped `data` run reports 36 findings or 37
depending on whether the reasoner started. Check which of `REA-021`/`REA-022` is
present before investigating a changed count.

What makes this safe to depend on is that the failing path says so loudly
instead of reporting success — the pattern
[Chapter 4](04-from-research-to-industry.md) recommends for every
research-lineage dependency.

### SHACL validation cannot be scoped to a named graph

Quad syntaxes parse, and then every named graph and the default graph are merged
into one before validation — SHACL is defined over a single data graph. Verified:
a TriG file with subjects spread across two named graphs and the default graph
gives a report identical to the same triples flattened into one Turtle file.
There is no graph-selection option and no per-graph reporting.

*Mitigation:* named graphs remain the right call for provenance and lifecycle
([Ch. 3](03-across-the-boundary.md)); for per-graph validation, extract the
graph and validate it as its own document, which is what the
`consistency-remote` manifest model does ([Ch. 13](13-operate-and-consume.md)).

### `sh:severity` must sit on the shape, not inside `sh:sparql`

SHACL defines `sh:severity` as a property of the **shape**. Declared inside a
nested `sh:sparql [ … ]` constraint block it is in the wrong place: pyshacl
ignores it there and falls back to the spec default of `sh:Violation`, while the
native engine reads it anyway. Two engines, two answers, same file.

The suite's own shapes were authored that way, and the effect was not subtle —
`--engine both` reported 5 Violations where `native+sparql` reported 2, so with
`--fail-on Violation` a class named `person_record` failed CI exactly as hard as
a logical contradiction. Fixed by moving the declaration onto the enclosing
shape; both engines now match `registry.json`.

*Mitigation for your own shapes:* put `sh:severity` on the shape. If a gate is
failing on something you declared `Warning`, check the placement before blaming
the engine. ([Ch. 7](07-the-toolchain.md) §7.4)

### `STR-002` and `STR-007` disagreed about external vocabularies

`STR-002` exempted only `rdf:`, `rdfs:` and `owl:` by their individual namespace
IRIs, while seven sibling checks exempt `http://www.w3.org/` wholesale — so using
`skos:prefLabel` without redeclaring SKOS locally produced a Violation-severity
"undefined property", while `STR-007`, the strictly broader check, stayed quiet
about the same predicate on the same graph. Now consistent.

*The general lesson:* two checks in the same registry that disagree with each
other are worse than either rule alone, because the reader cannot tell which is
intended. Whichever policy you pick — "declare every external term you use" is
defensible — apply it uniformly.

---

## 14.5 The cheapest thing you are not doing

Worth isolating because it is nearly free and almost universally skipped:

> **Every check run writes `full_results.csv`. Keep them, timestamped.**

That is a time series of semantic quality, produced by CI runs you are already
paying for. Findings by severity and by check ID over time is a real data-quality
KPI — the closest thing to observability available without a Prometheus stack.

Watch the **Warning trend** specifically. Violations get fixed because they break
the build; Warnings accumulate silently, and an accumulating Warning count is the
observable signature of decay, visible in your own artefacts a year before anyone
notices the model has drifted.

**Trend the scoped runs, not the unscoped ones.** Per §14.4, the unscoped total
drifts by a few findings between identical invocations, which would put noise
into the series at roughly the magnitude of a year's real drift. The scoped runs
are exactly reproducible, so any movement in them is signal. Conveniently, the
Warning counts are the stable part even in the unscoped run — it is Violations
that wander — so a Warning trend survives either choice.

---

## 14.6 Gaps that have closed

Worth recording, because the picture is not static. Seven limitations documented in
earlier drafts of this material no longer hold:

**Filtering findings to your own namespace.** Previously there was no way to say
"only show findings in my own terms" on an import-inclusive run; the
recommendation was `--exclude-imports`, which — as
[Chapter 9](09-continuous-integration.md) demonstrates with real output — trades
291 irrelevant findings for 4 false ones. `--own-namespace` now does it properly:
5 findings, all genuine, imports still resolved.

**Per-row taxonomy values.** Previously, a controlled value that varied per data
row rather than being hard-coded in the query text was genuinely uncatchable —
`pattern-consistency` inspected the query template, and there was no literal to
find. Passing `--output-data` now catches it, by comparing values that actually
appeared in the produced graph against the declared taxonomy. Verified: the
fixture's `MKT` department, absent from a taxonomy declaring only `ENG`/`QA`/
`SALES`, is correctly reported ([Ch. 12](12-release-and-change.md)).

**Rules in the WebAssembly build.** The previous edition of this manual said
flatly that the WASM build could not run SHACL-AF rules, and that on one shapes
graph it reported `conforms = true` where the native CLI errored — *"this is
fine"* against *"I could not check this"*. Both are fixed. Every binding now
takes `inference: "rules"`/`"rules-iterated"`, and the engine's differential
harness reports **0 disagreements across all 473 documents** of the W3C corpus,
where it previously reported one. What remains is a *choice* rather than a
limitation: the editor asks for `"none"` ([§14.4](#144-rough-edges-all-encountered-while-writing-this-manual)).

**`sh:declare` without `sh:prefixes`.** A SPARQL rule relying on a
shapes-graph-level prefix declaration used to be rejected at compile time, taking
the whole shapes graph with it — including for callers who never asked for rules.
Rule compile errors are now held on the rule and raised only if it would have
fired.

**The unscoped run is reproducible.** Five identical invocations now return 479
findings every time. The drift documented at length in earlier editions — 289 to
298, traced to `STR-007` — was never in the check: several registry `CONSTRUCT`s
bind two values per result, and the merge step read an arbitrary one of them and
deduplicated on it. Values are sorted and joined now, and the report shows both
instead of half the finding ([Ch. 9](09-continuous-integration.md) §9.2).

**The engine modes agree.** `sparql`, `native+sparql` and `both` now return the
same 5 scoped findings at the same severities; `LOG-001` is no longer reported
twice. Only `--engine native` still differs, and for a stated reason — it runs
the SHACL shapes only, and `QUA-004` exists solely as a SPARQL check.

**`DAT-001` can detect an invalid `xsd:boolean`.** It could not: the check tests
the stored lexical form with a regex, and rdflib rewrites the lexical form of an
ill-typed boolean, so `"yes"^^xsd:boolean` is stored as `'false'` and matches.
The branch was unreachable. A Python-side pass over `Literal.ill_typed` now
supplements the two portable formulations, which also catches value-space
violations no lexical regex can express, such as `"2021-02-30"^^xsd:date`.

**Six rough edges at once, in 0.14.1.** Every entry §14.4 carried in the
previous edition has since been fixed — verified here, each in both directions:

| Was | Now |
|---|---|
| `--own-namespace` near-miss returned a silent `0 total` | Warns that the filter matched none of the findings, and **names the namespaces actually present** |
| `sketch --queries` rejected a file path | Accepts a file or a directory |
| `sketch` crashed on a `CONSTRUCT` with no trailing `.` | Terminates each block on the way out; three failure shapes, one cause |
| `--apply-repairs` rewrote comments as well as code | Substitutes outside comments — while still rewriting string literals, because a TARQL IRI template is built from them |
| `docgen --ref` crashed on RDF/XML | Resolves the serialisation from content as well as extension |
| `docgen` reported *"5 external terms (0 resolved)"* | *"(3 resolved)"* — the `--ref` vocabularies are read |

A seventh was fixed that this manual never caught: `docgen` chose an annotation
language by whichever literal the parser happened to yield first, so a `--ref`
at a multilingual vocabulary — W3C's `org.ttl` carries `rdfs:comment` in four
languages — produced definitions in a different language on different runs. It
now prefers the document language, then an untagged literal, then the first in
sorted order. Content is stable as a result; ordering is not, which is what
§14.4 still records.

Two details worth keeping, because they are the shape of a good fix rather than
just its existence. The `sketch` crash **never produced wrong triples** — Turtle
rejected the malformed output rather than splicing it into something plausible —
so it was always a crash and never bad data, which is the first question to ask
of any bug in a writer. And the `--own-namespace` warning fires *only when there
were findings to lose*: a filter matching nothing on a genuinely clean run is
not an error, and warning there would train people to ignore the message.

> **Version note.** All six landed in **0.14.1**, published a day after 0.14.0.
> On 0.14.0 you will still meet every one of them, so check which version you
> have before concluding the manual is wrong about your copy — and upgrade,
> since this is six fixes in one release. (0.14.2 adds tests only; nothing an
> installed CLI does changes between the two.)

**Two more in the editor, in 0.13.5 — one of them a twin of a CLI fix above.**
The same questions asked of the extension found the same comment-scanning defect
behind rename, find-references, go-to-definition and the undeclared-prefix
warning: a trailing comment was read as code, so renaming a term rewrote the
comment explaining the rename. Separately, the unresolved-import warning claimed
*"no workspace file declares this identity"* when resolution never searches the
workspace — it walks the document's own directory tree — and now names the
directory it searched and the candidate count. Both are in
[Chapter 8](08-model-and-validate.md) §8.1.

The twin is the interesting one. Two hand-written ports of one algorithm carried
one defect and were fixed independently, days apart, with nothing comparing
them; 0.13.6 and 0.14.2 add a shared sixteen-case fixture that both repositories
carry, which is the subject of [Chapter 7](07-the-toolchain.md) §7.1 and the
most transferable thing in this section. **A parity test over shared data cannot
see behaviour that was written twice** — and the gap is invisible precisely
while both copies agree about being wrong.

The lesson generalises, and this edition is its own evidence: **re-verify the
gaps list against the tools you actually have.** Six were corrected within a day
of being written down. A limitation copied forward from an old document is
indistinguishable from a current one, right up until someone wastes a week
working around something that was fixed.

The obligation runs both ways, which this edition also demonstrates. Re-checking
turned up a claim in [Chapter 7](07-the-toolchain.md) §7.1 that had gone the
*other* way: a check reported as having earned its way into CI had only been
declared there, and the CLI still cannot run it. **Verify the capabilities you
credit a tool with as carefully as the limitations** — an overstatement is the
harder error to catch, because nobody goes looking for a feature they have been
told they already have.

---

## 14.7 What to do about the real gaps

| Gap | Practical answer |
|---|---|
| Packaging and deployment | Standard container and Helm tooling. A triple store deploys like any stateful service |
| Orchestration | Airflow, Argo Workflows or Prefect, calling these commands as steps |
| Observability | Prometheus and Grafana — plus retained `full_results.csv` as the semantic-quality series |
| APIs and knowledge products | Application development. Embed the SPARQL engine in the service ([Ch. 13](13-operate-and-consume.md)) |
| Approval workflows, RBAC | Branch protection rules and your existing identity platform. The tools supply the evidence; the platform enforces the policy |
| Incremental and streaming ingestion | Your pipeline's responsibility. These commands are batch |
| Provenance capture | Named graphs at load time. Decide before your first production load |

None of these needs a semantic-specific product. That is the useful conclusion:
**the parts of SemOps that need specialist tooling are covered, and the parts
that are not covered do not need specialist tooling.**

---

| ← [13. Operate and consume](13-operate-and-consume.md) | [15. Adoption roadmap →](15-adoption-roadmap.md) |
|---|---|
