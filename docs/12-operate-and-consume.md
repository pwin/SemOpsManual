<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# 12. Operate and consume

> *Part III — The practice · SemOps stages 7–9 · Operating-model layer 6*

> **Stories answered here**
> *As a platform owner, I want the same checks that guard the repository to run
> against what is actually in the triple store.*
> *As an application developer or an agent, I need documentation of what the
> terms mean and a guarantee they will not change under me.*

The last three pipeline stages — runtime validation, observability, and
consumption — are where a knowledge graph either earns its keep or quietly
becomes a cost centre. This is also where the toolchain's coverage is thinnest,
and this chapter is explicit about which parts are real and which are grey.

```mermaid
%%{init: {'theme':'base','themeVariables':{
  'fontSize':'15px','fontFamily':'Segoe UI, Helvetica, Arial, sans-serif',
  'lineColor':'#14243A','primaryTextColor':'#14243A'}}}%%
flowchart TD
    S7["<b>7 · Runtime validation</b><br/>consistency-remote<br/><i>covered</i>"]
    S8["<b>8 · Observability</b><br/>metrics · dashboards · logs<br/><i>not covered</i>"]
    S9A["<b>9a · Documentation</b><br/>docgen<br/><i>covered</i>"]
    S9B["<b>9b · APIs &amp; products</b><br/>SPARQL · GraphQL · REST<br/><i>not covered</i>"]

    S7 --> S8 --> S9A --> S9B

    classDef ci fill:#D9F4FA,stroke:#02B7D4,stroke-width:2px,color:#14243A;
    classDef ops fill:#D9F5EC,stroke:#0CB88E,stroke-width:2px,color:#14243A;
    classDef gap fill:#F1F3F5,stroke:#8A93A0,stroke-width:2px,color:#14243A,stroke-dasharray:4 3;
    class S7 ci; class S9A ops; class S8,S9B gap;
```

---

## 12.1 Runtime validation against a live store

Everything so far has run against files in a repository. The moment the org
chart moves from Git-tracked Turtle into a real triplestore, a new question
appears: **is what is actually loaded still consistent with what we think we
shipped?**

Repository checks cannot answer that. A store drifts through partial loads,
manual fixes, an update applied to one environment and not another, or a graph
someone forgot to reload.

```bash
python -m ontology_suite consistency-remote \
  --query-endpoint http://localhost:3030/acme/sparql \
  --manifest examples/acme_robotics/manifest.json \
  --auth-user admin --auth-password secret \
  --out-dir out/consistency-remote
```

### The manifest is the interesting part

A triplestore holds triples, not project metadata. Fuseki has no built-in link
from a named graph back to the transformation query that produced it, nor from a
data graph to the ontology graph it is supposed to conform to. The manifest is
where a project records that binding explicitly:

```python
from ontology_suite.remote.manifest import GraphManifest, GraphBinding

manifest = GraphManifest(bindings=[
    GraphBinding(
        graph_uri="https://acme.example.org/graph/ontology/2.0.0",
        role="ontology",
    ),
    GraphBinding(
        graph_uri="https://acme.example.org/graph/triplified/employees",
        role="triplified_data",
        source_tarql="queries/employees.rq",
        ontology_graph_uri="https://acme.example.org/graph/ontology/2.0.0",
    ),
])
manifest.save("graphs.json")
```

That structure enables a genuine **three-way check**: the live data graph, the
ontology graph it claims to conform to, and the local query file that produced
it — all compared together. It catches the specific and common failure where the
repository is perfectly consistent and the store is a version behind.

`--sample-limit` caps how many triples are pulled per named graph, which is what
makes this viable against a production-sized store.

### Named graphs are a decision you make once

[Chapter 3](03-across-the-boundary.md) argued that per-partner named graphs are
the highest-value cross-boundary decision, and this is where it pays off. The
manifest model assumes named graphs; a store where everything was merged into the
default graph cannot express these bindings at all, and cannot answer "which
supplier asserted this?" either.

It is nearly free at load time and effectively impossible to retrofit.

---

## 12.2 Documentation as a product: `docgen`

SemOps lists documentation as a first-class element — *"without it, semantic
systems become opaque"* — and it is the artefact
[Chapter 2](02-people-and-cognition.md) identified as the answer to the
priesthood problem.

```bash
python -m ontology_suite docgen \
  --ontology examples/acme_robotics/acme-org-v1.ttl \
  --out-dir out/docgen
```

Real output:

```
Wrote out/docgen/ontology_doc_data.json: prefix='acme', 4 classes,
  2 object properties, 3 datatype properties, 1 sections,
  5 external terms (0 resolved).
Wrote out/docgen/ontology-documentation.html
4 class diagram(s) written to: out/docgen/class-diagrams
```

You get a self-contained `ontology-documentation.html` — class and property
tables, diagrams, and one concise-bounded-description diagram per class — plus
`ontology_doc_data.json`, which is the machine-readable version. That JSON is
easy to overlook and is the more strategically useful of the two: it is what you
feed a documentation portal, a catalogue, or — per
[Chapter 5](05-genai-and-agents.md) — an agent that needs to know what your terms
mean.

### Two rough edges found while running it

**`--ref` does not sniff serialisation format.** Passing the FOAF vocabulary,
which is published as RDF/XML:

```bash
python -m ontology_suite docgen --ontology acme-org-v1.ttl \
  --ref reference_vocab/foaf.rdf --out-dir out/docgen
```

fails with an rdflib Turtle parse error — the RDF/XML comment header is read as
Turtle:

```
rdflib.plugins.parsers.notation3.BadSyntax: at line 4 of <>:
Bad syntax (expected '.' or '}' or ']' at end of statement)
```

Convert the vocabulary to Turtle first, or pass only Turtle files to `--ref`.
This is a small thing that costs ten confusing minutes, and it is worth knowing
before it happens to you rather than after.

**External-term resolution did not engage in this run.** Even with
`--ref reference_vocab/org.ttl` supplied, the output still reported
*"5 external terms (0 resolved)"*. `foaf:Person` and `org:OrganizationalUnit`
are correctly *listed* as external terms in both cases — the documentation is
accurate about what it does and does not know — but their upstream definitions
were not pulled into the page. Reported as observed; the behaviour may be
sensitive to how the reference file declares its terms.

Neither undermines the command. The generated page is genuinely the artefact to
put in front of a domain expert, and being explicit about unresolved external
terms is better than silently omitting them.

### Make it automatic

The maturity model expects documentation *"auto-generated on every commit"* at
Level 3. That is one CI step:

```yaml
- name: Reference documentation
  run: |
    uv run ontology-quality-suite docgen \
      --ontology ontology/acme-org.ttl --out-dir docs/reference
- uses: actions/upload-pages-artifact@v3
  with:
    path: docs/reference
```

Documentation that regenerates itself is documentation that stays true.
Documentation maintained by hand is documentation that was true once.

---

## 12.3 Observability: not covered

SemOps stage 8 wants graph size and growth metrics, query-performance
dashboards, SPARQL log analysis, data-quality KPIs, provenance tracking and
anomaly detection. **None of this is in either tool.** Prometheus, Grafana and
Loki are the right answers, exactly as the pipeline blueprint says.

There is one thing worth doing that costs almost nothing, though, and it is the
bridge between what you have and what you need:

> **Every check run writes `full_results.csv`. Retain them, timestamped.**

That file is a time series of your semantic quality. Findings-by-severity over
time, per check ID, is a genuine data-quality KPI, and it comes free from
artefacts CI is already producing. Most teams delete them with the build.

The specific signal to watch is not the absolute count but the **trend in
Warnings**. Violations get fixed because they fail the build. Warnings
accumulate silently, and an accumulating Warning count is the observable
signature of [Chapter 1](01-the-business-case.md)'s decay — visible in your own
CI artefacts a year before anyone notices the model has drifted.

---

## 12.4 Knowledge products and APIs: not covered

SemOps stage 9 wants SPARQL endpoints, GraphQL and REST APIs, search indexes,
and data products. Neither tool serves an API, and neither should — that is
application development, not quality tooling.

The SemOps material's own microservices guidance is the reference here, and its
core architectural point is sound: for low-latency semantic APIs, embed the
SPARQL engine **in** the service rather than putting a service in front of a
remote triplestore.

| Language | Engine | Best at |
|---|---|---|
| Rust | Oxigraph | Highest throughput, lowest latency |
| Python | RDFLib | Analytics, AI/LLM integration |
| Node.js | Comunica | Streaming, web-native, federated |
| Prolog | SWI `semweb` | Rule-heavy, expert-system style |
| Java | Jena / Fuseki | Enterprise-standard, stable |

Note that Oxigraph appears twice in this manual's world — as the recommended
Rust API engine here, and as the WASM engine the VS Code extension already runs
in-process ([Chapter 7](07-the-toolchain.md)). That is not a coincidence so much
as a signal: the same embeddable engine serves the editor and the endpoint.

### What consumption demands from everything upstream

Whether the consumer is a React application, a dashboard, or an agent
([Chapter 5](05-genai-and-agents.md)), it needs four things — and all four are
produced by earlier chapters, not by the API layer:

| Consumer needs | Produced by | Chapter |
|---|---|---|
| Stable IRIs that do not change meaning | Evidence-based semver, migration annotations | [11](11-release-and-change.md) |
| To know what a term means | `docgen`, `rdfs:label` coverage (`QUA-001`) | This chapter, [8](08-model-and-validate.md) |
| Confidence the data conforms | `data`, `consistency-remote` | [10](10-ingest-and-transform.md), this chapter |
| To know who asserted what | Named graphs | [3](03-across-the-boundary.md), §12.1 |

An API built on a graph that lacks these is an API that will be wrong
occasionally and unpredictably — which is worse than being wrong reliably,
because consumers stop being able to calibrate their trust.

---

## 12.5 Maturity checkpoint

`consistency-remote` against a live store, plus `docgen` on every commit, covers
part of Level 4's *"semantic APIs managed and monitored"* — the *managed* half.

The *monitored* half needs an observability stack this toolchain does not
provide, and Level 4 also expects Kubernetes deployment, automated environment
promotion, and continuous ingestion with retry logic. Those are real gaps, and
[Chapter 13](13-coverage-and-gaps.md) is where they are counted honestly rather
than glossed.

---

| ← [11. Release and change](11-release-and-change.md) | [13. Coverage and gaps →](13-coverage-and-gaps.md) |
|---|---|
