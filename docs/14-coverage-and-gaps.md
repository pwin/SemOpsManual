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
| 5 | Knowledge Graph Observability | **No** | See [§14.5](#135-the-cheapest-thing-you-are-not-doing) |
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

### `STR-007` makes the unscoped run non-reproducible

Five consecutive identical `checks --import-dir` runs over the fixture returned
290, 292, 294, 294 and 295 findings. Warning (162) and Info (84) counts were
identical every time; the whole drift sat in Violations, and diffing two
divergent runs check by check found a single contributor — `STR-007`
("predicate has no declared `rdf:type`") returned 13 on one run and 18 on
another, accounting for the entire difference.

`STR-007`'s query does an undeduplicated `?s ?focus ?o` match with no
`DISTINCT`, over a merged graph carrying hundreds of blank-node OWL axioms from
`org:` and FOAF — a plausible source of parse-order sensitivity, offered as a
lead rather than a diagnosis. The suite's own walkthrough documents the effect
without fully explaining it either.

*Mitigation:* none needed for the recommended workflow — every scoped run in
this manual is exactly reproducible across repeated invocations. Do not build a
threshold, trend or regression test on the unscoped total.
([Ch. 9](09-continuous-integration.md))

### `--engine` changes the finding count, and one check is double-reported

The four engine modes do not agree, on the same ontology with the same registry
and the same `--own-namespace` filter: `native` returns 4, `sparql` 5,
`native+sparql` 6, `both` 6. `native` alone misses `QUA-004`, which exists only
as a SPARQL check; the two union modes report `LOG-001` twice, once from each
formulation, for the same focus node and value.

*Mitigation:* pin `--engine` in CI, and deduplicate on
(check_id, focus_node, value) when counting findings programmatically. Full
comparison in [Ch. 7](07-the-toolchain.md) §7.4.

### The WebAssembly build cannot run SHACL-AF rules

The WASM API exposes `inference: "none" | "rdfs"` and nothing else — no
`advanced`, no `iterateRules`. Rules are native-CLI and Python only.

The consequence is a genuine divergence, not just a missing feature. On a shapes
graph whose SPARQL rule the native engine rejects at compile time, the native CLI
exits 2 with an error while the WASM build returns `conforms = true` with zero
results — verified directly against the same file. One says *"I could not check
this"*, the other says *"this is fine"*, which is the distinction
[Ch. 4](04-from-research-to-industry.md) argues everything depends on.

*Mitigation:* treat browser and editor validation as validation-only. Run
anything rule-bearing through the CLI or the Python binding
([Ch. 11](11-rules-and-inference.md) §11.7).

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

### pySHACL ignores `sh:severity` inside SPARQL-based constraints

A confirmed upstream bug: severity declared inside `sh:sparql` constraints is
ignored and everything reports as `Violation`. The native Rust engine handles it
correctly.

Measured on the fixture, this is a 2.5× inflation of the Violation count:
`--engine both` reports **5 Violations / 1 Warning** where `native+sparql`
reports **2 Violations / 4 Warning** — same six findings, different severities.
With `--fail-on Violation` that is the difference between a green build and a
red one, on identical inputs.

*Mitigation:* `--engine native+sparql` where the native engine is available.
([Ch. 7](07-the-toolchain.md))

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

Worth recording, because the picture is not static. Two limitations documented in
an earlier draft of this material no longer hold:

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

The lesson generalises: **re-verify the gaps list against the tools you actually
have.** A limitation copied forward from an old document is indistinguishable
from a current one, right up until someone wastes a week working around
something that was fixed.

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
