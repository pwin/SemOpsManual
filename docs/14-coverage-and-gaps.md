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

### `--own-namespace` fails silently on a near-miss

`--own-namespace "http://example.org/acme#"` against a fixture whose namespace is
`https://acme.example.org/ns/` returned:

```
Findings: 0 total (0 Violation, 0 Warning, 0 Info)
```

It is a **literal IRI-prefix string match**. A wrong scheme, host or trailing
separator produces silence, and silence is indistinguishable from success.

*Mitigation:* copy the namespace from the ontology's `@prefix` line, and keep one
deliberately-failing fixture in CI so a gate that cannot fail is detectable.
*Suggested improvement:* warn when `--own-namespace` matches zero focus nodes
while unfiltered findings exist. ([Ch. 9](09-continuous-integration.md))

### `sketch --queries` requires a directory, not a file

```
FileNotFoundError: No files matching '*.sparql,*.rq,*.tarql,*.tq' found in
examples/acme_robotics/employees.rq
```

The flag reads like it accepts a file. It scans a folder.

*Mitigation:* pass the containing folder; narrow with `--file-pattern`.
([Ch. 10](10-ingest-and-transform.md))

### `--apply-repairs` rewrites comments as well as code

The rename repair is a textual substitution across the whole file. A comment
reading *"every row is typed `acme:Engineer`, which v2.0.0 renames to
`acme:SoftwareEngineer`"* became *"every row is typed `acme:SoftwareEngineer`,
which v2.0.0 renames to `acme:SoftwareEngineer`"* — harmless, and nonsense.

*Mitigation:* prefer the default dry-run `.patch` output in automation; review
before applying. `--apply-repairs` suits a developer who will read the diff, not
an unattended job that commits its own output.
([Ch. 12](12-release-and-change.md))

### `docgen --ref` does not sniff serialisation format

Passing FOAF, published as RDF/XML, crashes with an rdflib **Turtle** parse
error on the file's XML comment header.

*Mitigation:* convert to Turtle, or pass only Turtle to `--ref`.
([Ch. 13](13-operate-and-consume.md))

### `docgen` external-term resolution did not engage

Even with `--ref reference_vocab/org.ttl`, output reported *"5 external terms
(0 resolved)"*. Terms are correctly *listed* as external — the documentation is
honest about what it does not know — but upstream definitions were not pulled in.
Reported as observed rather than diagnosed.
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

**The unscoped run is reproducible.** Five identical invocations now return 301
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

The lesson generalises, and this edition is its own evidence: **re-verify the
gaps list against the tools you actually have.** Two of the four above were
corrected within a day of being written down. A limitation copied forward from an
old document is indistinguishable from a current one, right up until someone
wastes a week working around something that was fixed.

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
