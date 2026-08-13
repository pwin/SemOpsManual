<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# 13. Coverage and gaps

> *Part IV — The ledger*

A manual that only describes what works is marketing. This chapter is the
counterweight: **what SemOps asks for, what the toolchain actually delivers, and
what it does not.**

Two kinds of entry appear below. *Gaps* are things SemOps requires that these
tools do not do at all — usually because they are somebody else's job. *Rough
edges* are things the tools do, with behaviour worth knowing before it costs you
an afternoon; every one of them was hit while writing this manual.

---

## 13.1 Coverage by pipeline stage

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

## 13.2 Coverage by operating-model layer

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

## 13.3 Coverage of the ten SemOps elements

| # | Element | Covered? | Where |
|---|---|---|---|
| 1 | Knowledge Lifecycle Management | **Yes** | [Ch. 11](11-release-and-change.md) |
| 2 | Automated Deployment & Packaging | **No** | — |
| 3 | Data Integration & ETL Orchestration | **Partial** | [Ch. 10](10-ingest-and-transform.md) — no orchestration |
| 4 | Reasoning & Inference Operations | **Partial** | Reasoning and regression tests yes; incremental reasoning and performance monitoring no |
| 5 | Knowledge Graph Observability | **No** | See [§13.5](#135-the-cheapest-thing-you-are-not-doing) |
| 6 | Semantic Governance & Access Control | **Partial** | Evidence yes; RBAC and workflow no |
| 7 | Semantic CI/CD Pipelines | **Partial** | Linting, SHACL, docs yes; packaging and deployment no |
| 8 | Tooling Integration | **Partial** | Validator, reasoner, CI yes; triple store, K8s, monitoring no |
| 9 | Knowledge Products & APIs | **No** | [Ch. 12](12-operate-and-consume.md) |
| 10 | Documentation & Semantic Literacy | **Yes** | `docgen`, generated docs, this manual |

---

## 13.4 Rough edges, all encountered while writing this manual

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
([Ch. 11](11-release-and-change.md))

### `docgen --ref` does not sniff serialisation format

Passing FOAF, published as RDF/XML, crashes with an rdflib **Turtle** parse
error on the file's XML comment header.

*Mitigation:* convert to Turtle, or pass only Turtle to `--ref`.
([Ch. 12](12-operate-and-consume.md))

### `docgen` external-term resolution did not engage

Even with `--ref reference_vocab/org.ttl`, output reported *"5 external terms
(0 resolved)"*. Terms are correctly *listed* as external — the documentation is
honest about what it does not know — but upstream definitions were not pulled in.
Reported as observed rather than diagnosed.
([Ch. 12](12-operate-and-consume.md))

### The DL reasoner behaved differently in two commands, same session

The `ontology` pass emitted `REA-022` — *external DL reasoner unavailable*, with
an internal `UnboundLocalError` from the bridge. The `data` pass, same machine,
same fixture, same session, ran HermiT successfully and emitted `REA-021`,
correctly finding `acme:Contractor` unsatisfiable.

No explanation established. What made it *safe* is that the failing path said so
loudly instead of reporting success — the pattern
[Chapter 4](04-from-research-to-industry.md) recommends for every research-lineage
dependency.

### pySHACL ignores `sh:severity` inside SPARQL-based constraints

A confirmed upstream bug: severity declared inside `sh:sparql` constraints is
ignored and everything reports as `Violation`. The native Rust engine handles it
correctly.

*Mitigation:* `--engine native+sparql` where the native engine is available.
([Ch. 7](07-the-toolchain.md))

---

## 13.5 The cheapest thing you are not doing

Worth isolating because it is nearly free and almost universally skipped:

> **Every check run writes `full_results.csv`. Keep them, timestamped.**

That is a time series of semantic quality, produced by CI runs you are already
paying for. Findings by severity and by check ID over time is a real data-quality
KPI — the closest thing to observability available without a Prometheus stack.

Watch the **Warning trend** specifically. Violations get fixed because they break
the build; Warnings accumulate silently, and an accumulating Warning count is the
observable signature of decay, visible in your own artefacts a year before anyone
notices the model has drifted.

---

## 13.6 Gaps that have closed

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
`SALES`, is correctly reported ([Ch. 11](11-release-and-change.md)).

The lesson generalises: **re-verify the gaps list against the tools you actually
have.** A limitation copied forward from an old document is indistinguishable
from a current one, right up until someone wastes a week working around
something that was fixed.

---

## 13.7 What to do about the real gaps

| Gap | Practical answer |
|---|---|
| Packaging and deployment | Standard container and Helm tooling. A triple store deploys like any stateful service |
| Orchestration | Airflow, Argo Workflows or Prefect, calling these commands as steps |
| Observability | Prometheus and Grafana — plus retained `full_results.csv` as the semantic-quality series |
| APIs and knowledge products | Application development. Embed the SPARQL engine in the service ([Ch. 12](12-operate-and-consume.md)) |
| Approval workflows, RBAC | Branch protection rules and your existing identity platform. The tools supply the evidence; the platform enforces the policy |
| Incremental and streaming ingestion | Your pipeline's responsibility. These commands are batch |
| Provenance capture | Named graphs at load time. Decide before your first production load |

None of these needs a semantic-specific product. That is the useful conclusion:
**the parts of SemOps that need specialist tooling are covered, and the parts
that are not covered do not need specialist tooling.**

---

| ← [12. Operate and consume](12-operate-and-consume.md) | [14. Adoption roadmap →](14-adoption-roadmap.md) |
|---|---|
