<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# 11. Rules and inference

> *Part III — The practice · SemOps element 4 · Operating-model layer 2*

> **Stories answered here**
> *As a knowledge engineer, I want the model to derive what follows from the
> data, rather than making every consumer re-implement the same logic.*
> *As a SemOps engineer, I want to know what a rule will do to my gate before I
> turn it on.*

Every chapter so far has treated a graph as something to *check*. This one is
about deriving triples that were never asserted — and about the fact that the
moment you do, your gate is validating data that did not exist when the commit
was made.

SemOps names this as its own element — *Reasoning & Inference Operations*: rule
deployment and versioning, incremental strategies, validation of inferred
triples, regression tests for reasoning changes. It is the element most often
skipped, because inference feels like a modelling luxury until something
downstream re-implements it in application code for the fourth time.

---

## 11.1 A third tool

Rules need a tool the previous chapters have not used. The Ontology Quality
Suite does not run SHACL-AF rules — there is no `--advanced` flag on any of its
subcommands — and the VS Code extension does not either. Both validate.

| | **SHACL Engine** |
|---|---|
| Repository | [pwin/SHACL_Engine](https://github.com/pwin/SHACL_Engine) |
| Distribution | [PyPI: `shacl`](https://pypi.org/project/shacl/) · npm: `shacl-wasm`, `shacl-wasm-node` |
| What it is | A SHACL validator in Rust — CLI, Python bindings, and a WebAssembly build |
| Why it is here | It is the engine that runs **SHACL-AF rules**, and the native engine behind the suite's `--engine native+sparql` |

```bash
pip install shacl        # CLI + Python bindings
npm install shacl-wasm   # ESM build for bundlers
```

It is the same engine the suite already uses for validation, so adopting rules
does not add a second semantics — it exposes more of an engine you are running
already.

From Python, rules are reached through the `inference` argument rather than a
separate flag:

```python
import shacl
shapes = shacl.Shapes.from_file("shapes.ttl")          # compile once
report = shapes.validate_file("data.ttl",
                              inference="rules")        # or "rules-iterated"
print(report.conforms, len(report.results))
```

> **Check your version before believing any of this.** Rules are new, and the
> surface has moved twice in the space of writing this chapter. At **0.1.5** the
> Python binding had no rules at all:
>
> ```
> inference='rules' -> ERROR: unknown inference "rules"; use "none" or "rdfs"
> ```
>
> At **0.1.7** the CLI had them and the WebAssembly build did not. From
> **0.1.8/0.1.9** every binding has them, and 0.1.9 also fixes a real defect in
> which `$this` was not substituted into a CONSTRUCT-based rule — so a SPARQL
> rule ran for **every node in the graph** rather than for its focus node. If
> you wrote SPARQL rules against an earlier version, re-run them.
>
> The failure mode is at least the right one throughout: an unrecognised
> `inference` value is an error naming what is accepted, never a silent
> fallback that validates without applying the rules. Pin the version, and check
> with `shacl --version`.

---

## 11.2 Three ways to derive a triple

Before reaching for rules, be clear which of three mechanisms you want. They
overlap, and choosing wrongly is the usual cause of a pipeline nobody can debug.

```mermaid
%%{init: {'theme':'base','themeVariables':{
  'fontSize':'15px','fontFamily':'Segoe UI, Helvetica, Arial, sans-serif',
  'lineColor':'#14243A','primaryTextColor':'#14243A',
  'edgeLabelBackground':'#FFFFFF'}}}%%
flowchart TD
    SRC["Source data"]
    T["<b>Transformation</b><br/>TARQL · oxi-gen<br/><i>outside → RDF</i>"]
    R["<b>RDFS closure</b><br/>--inference rdfs<br/><i>subclass · domain · range</i>"]
    A["<b>SHACL-AF rules</b><br/>sh:rule<br/><i>domain logic</i>"]
    G["Validated graph"]

    SRC --> T --> R --> A --> G

    classDef data fill:#ECF7D5,stroke:#7CBA07,stroke-width:2px,color:#14243A;
    classDef ci fill:#D9F4FA,stroke:#02B7D4,stroke-width:2px,color:#14243A;
    classDef human fill:#FFE6DA,stroke:#FD5B1C,stroke-width:2px,color:#14243A;
    classDef ops fill:#D9F5EC,stroke:#0CB88E,stroke-width:2px,color:#14243A;
    class SRC,T data; class R ci; class A human; class G ops;
```

| Mechanism | Use it when | Chapter |
|---|---|---|
| **Transformation** (TARQL / oxi-gen) | The data is not RDF yet. One row in, some triples out | [10](10-ingest-and-transform.md) |
| **RDFS closure** (`--inference rdfs`) | You need `rdfs:subClassOf`/`subPropertyOf`/domain/range entailments, and nothing more | This chapter |
| **SHACL-AF rules** (`sh:rule`) | The derivation is *domain logic* — conditional, computed, or specific to your model | This chapter |

The distinction that matters in practice: **a transformation runs once, at
ingest, and its output is what you store. A rule runs at validation time, and
its output may never be stored at all.** If downstream consumers need the
derived triples, a rule alone does not give them to you — you need to
materialise and load them.

### Why RDFS closure is not optional trivia

SHACL follows `rdfs:subClassOf` when deciding class membership, and **nothing
else**. A shape targeting `ex:parent` via `sh:targetSubjectsOf` will not see a
subject that only has `ex:father`, however clearly `rdfs:subPropertyOf` says one
implies the other. Materialising the closure first closes that gap:

```bash
shacl -d data.ttl -s shapes.ttl --inference rdfs
```

It covers `rdfs2`, `rdfs3`, `rdfs5`, `rdfs7`, `rdfs9` and `rdfs11` — domain,
range, both hierarchies and their transitivity. The axiomatic and reflexive
rules are deliberately left out: they entail `rdf:type rdfs:Resource` for every
term, which no shape is improved by.

It is off by default because it changes the report — and a `sh:closed` shape in
particular starts seeing inferred predicates and failing on them.

---

## 11.3 Triple rules

`sh:subject`, `sh:predicate` and `sh:object` are node expressions evaluated per
focus node. Applied to the Acme fixture, the two most common shapes a rule
takes:

```turtle
acme:PersonRules a sh:NodeShape ;
    sh:targetClass acme:Employee ;

    # 1. Constant object: every Employee is also a foaf:Agent
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate rdf:type ; sh:object foaf:Agent ] ;

    # 2. Path object: one triple per value found
    sh:rule [ a sh:TripleRule ;
        sh:subject sh:this ; sh:predicate acme:colleague ;
        sh:object [ sh:path acme:worksIn/^acme:worksIn ] ] .
```

Rules are **off by default** and enabled with `-a`:

```bash
shacl -d data.ttl -s shapes.ttl --advanced
```

**The inferred triples are the cross product of the three expressions.** A path
yielding three values yields three triples — which is what you want for rule 2
and worth remembering before writing a rule whose subject expression is also a
path.

The node expressions available are SHACL-AF's: `sh:this`, a constant,
`[ sh:path P ]` with an optional `sh:nodes` operand,
`[ sh:filterShape S ; sh:nodes N ]`, `sh:union` and `sh:intersection`. Anything
else is an error rather than an empty result — see [§11.7](#117-what-is-not-there).

### Verified behaviour

Running a rule that types every `ex:Person` as `ex:Party`, then validating the
inferred `ex:Party` instances against a shape requiring a property none of them
have, gives **exactly one violation per source instance** — 1,000 violations on
the 1,000-instance dataset and 100,000 on the 100,000-instance one. Every focus
node, once each, no misses and no duplicates.

That is the check worth copying: **validate the derived data, so a rule that
silently does nothing shows up as a missing violation rather than as silence.**

---

## 11.4 SPARQL rules

`sh:construct` takes a `CONSTRUCT` query with `$this` pre-bound to the focus
node. This is where computation lives:

```turtle
acme:BoxRules a sh:NodeShape ;
    sh:targetClass acme:Box ;
    sh:rule [ a sh:SPARQLRule ; sh:construct """
        PREFIX acme: <https://acme.example.org/ns/>
        CONSTRUCT { $this acme:area ?a }
        WHERE { $this acme:width ?w ; acme:height ?h . BIND(?w * ?h AS ?a) }""" ] .
```

Verified: with `width 3` and `height 4`, a shape asserting
`sh:path acme:area ; sh:hasValue 12` conforms — the arithmetic runs and the
derived value is what validation sees.

Prefixes can come from an inline `PREFIX` line, as above, or from SHACL's own
`sh:declare`/`sh:prefixes` mechanism:

```turtle
acme: sh:declare [ sh:prefix "acme" ;
                   sh:namespace "https://acme.example.org/ns/"^^xsd:anyURI ] .

acme:Rules a sh:NodeShape ; sh:targetClass acme:Thing ;
    sh:rule [ a sh:SPARQLRule ; sh:prefixes acme: ;
              sh:construct """CONSTRUCT { $this acme:tagged true } WHERE { }""" ] .
```

Both forms work, and a rule that omits `sh:prefixes` entirely now falls back to
the shapes graph's own `sh:declare` — which is how the W3C 1.2 rules corpus
writes them.

> **Fixed in 0.1.8; broken before it.** At 0.1.7 a rule relying on a
> shapes-graph-level `sh:declare` alone was not resolved, and the engine
> rejected the **whole shapes graph** with a SPARQL prefix error at compile
> time, whether or not `-a` was passed — so a document that had validated fine
> before rules existed stopped validating at all. Rule compile errors are now
> held on the rule and raised only if that rule would have fired, which means
> validation that never asked for rules is unaffected and a broken rule is still
> not silently skipped. Another reason to check `shacl --version`.

---

## 11.5 Four ways to get a wrong answer

These produce silence, not errors. Every one reproduces exactly as described.

**A rule fires on its shape's targets, so a shape with no target does nothing.**
This is the most common mistake, because attaching a rule to a nested property
shape reads perfectly naturally:

```turtle
acme:S a sh:NodeShape ; sh:targetClass acme:Employee ;
    sh:property [ sh:path acme:name ;
        sh:rule [ … ] ] .        # never fires: this shape has no target
```

Verified: the rule never runs, nothing is inferred, and no message says so.

**One pass, so a transitive rule does not close.** SHACL-AF defines a single
iteration. A rule deriving `ex:sub` from two hops of `ex:sub` reaches two hops
and stops. On a chain `a→b→c→d`, one pass leaves `a` short of `d`:

```bash
shacl -d data.ttl -s shapes.ttl -a                    # one pass  -> a does not reach d
shacl -d data.ttl -s shapes.ttl -a --iterate-rules 10 # fixpoint  -> it does
```

`--iterate-rules` is outside the specification. A rule set with no fixpoint —
one minting a fresh term each round — stops with an error rather than running
until memory does.

**Rules at the same `sh:order` cannot see each other's inferences.** Two rules
both at the default order 0 each see the graph as it was before either ran.
Verified with a two-step chain (`Person → Step1 → Step2`): at equal order,
`Step2` is never reached; with `--iterate-rules 5`, it is. Give the consumer a
higher `sh:order`, or iterate.

**Negation is not monotonic, and iteration exposes it.** A conclusion drawn from
absence *outlives* the absence, because rules only ever add triples:

```turtle
# Round 1 marks ex:a as Unnamed. Round 2's rule then gives it a name.
# The mark stays. It is simply no longer true.
```

SHACL 1.2 Rules answers this by requiring a stratified rule set; SHACL-AF does
not, so it is the author's problem. If a rule tests for absence, either keep to
a single pass or ensure nothing later supplies what it tested for.

> **And one that is not a hazard:** rules never modify the graph you passed in.
> The expanded graph is a new one, so a report is always relative to an input
> you still have.

---

## 11.6 Rules at scale

Measured on this manual's own benchmark data, whole-process wall time, two rules
(one triple rule, one SPARQL rule) plus validation of the derived triples:

| instances | triples | validate only | rules + validate |
|---:|---:|---:|---:|
| 1,000 | ~6,900 | — | 0.9s |
| 10,000 | ~69,000 | — | 1.1s |
| 100,000 | ~690,000 | 2.7s | **11.9s** |
| 100,000, `--iterate-rules 5` | ~690,000 | — | 18.7s |

Rules cost roughly **4.5× validation alone** at 100k, and iterating to five
rounds roughly 7×. In absolute terms that is twelve seconds to derive and
validate over two-thirds of a million triples, which is comfortably inside a CI
budget.

For context on the validation half, the same engine against pySHACL on the same
data, with identical result counts at every size:

| instances | ours | pySHACL | speedup |
|---:|---:|---:|---:|
| 1,000 | 0.040s | 2.992s | 75× |
| 10,000 | 0.199s | 24.369s | 122× |
| 100,000 | 1.808s | 206.250s | 114× |

Two caveats the engine is candid about, and which matter more than the ratio.
**Loading dominates** — at 100k, validation is 0.46s of the 1.81s total, so the
first place to look for speed is the parser, not the validator. And the index
holds the graph **three times over**, once per permutation, with no streaming
path: budget roughly 3 × 12 bytes per triple plus the interned strings, and do
not reach for this on a graph too large to hold three sorted copies of.

### The WebAssembly build has a different cost model

Those figures are the native binary. The same engine compiled to WebAssembly —
what the editor runs, and what a browser would — behaves differently at size,
because wasm32 has a single linear memory that `memory.grow` may have to
relocate, copying the whole heap.

Measured on the engine's own scale probe, one compiled shapes graph against
growing data:

| instances | triples | first run | second run | resident |
|---:|---:|---:|---:|---:|
| 1,000 | 4,000 | 56 ms | 26 ms | 89 MB |
| 10,000 | 40,000 | 205 ms | 137 ms | 76 MB |
| 100,000 | 400,000 | **12,611 ms** | **3,119 ms** | 329 MB |

At ontology scale — hundreds to low thousands of triples, which is what an
editor validates — the difference is noise. At 400,000 triples the first run
costs four times the second, and roughly nine of those twelve seconds are the
heap being built rather than the graph being checked.

Two consequences:

- **Reuse the compiled validator.** A caller that validates one document per
  process pays the growth cost every time; one that holds a `Validator` and
  validates many pays it once. The API is shaped for the second, and the
  difference is the table above.
- **WebAssembly is not a drop-in for bulk data.** Editor validation, browser
  validation, a partner checking their own submission — all fine. A nightly pass
  over a production graph belongs on the native binary. This does not contradict
  [§11.6](#116-rules-at-scale)'s numbers; it says which build they apply to.

---

## 11.7 What is not there

Stated plainly, because a rule engine's gaps are where the silent wrong answers
live.

| Not implemented | Consequence |
|---|---|
| **SHACL functions** (`sh:SPARQLFunction`) | A rule calling one errors — `unsupported node expression`, exit 2 — rather than returning empty |
| **Result annotations** (`sh:resultAnnotation`) | Extra properties from a SPARQL constraint's solution are not copied onto results |
| **SHACL 1.2 Rules** (`RULE { } WHERE { }`) | A different design from SHACL-AF; its test corpus is vendored but not wired into the conformance harness |
| **OWL-RL pre-inference** | RDFS is available and opt-in; nothing beyond it |
| **Rules in the VS Code extension** | The engine supports them; the extension does not yet ask for them — see below |

### Rules in the browser: the engine can, the editor does not

Every binding runs rules — CLI, Python and WebAssembly alike — through the same
`inference` modes:

```js
import { Validator } from 'shacl-wasm';
const v = Validator.fromTurtle(shapesTurtle);
const report = v.validateTurtle(dataTurtle, null, 'rules');   // or 'rules-iterated'
```

Verified against the built package at 0.1.9: `"rules"` fires the rule and the
derived data is validated, while an unrecognised mode is an **error** rather
than a silent fallback to `"none"` — which is the failure behaviour that
matters, because a browser quietly validating without applying rules would
report conformance it never established.

> **This is recent, and the manual said the opposite one version ago.** At 0.1.7
> the WASM API exposed `"none"` and `"rdfs"` only. Worse, a shapes graph whose
> SPARQL rule the native engine rejected at compile time returned
> `conforms = true` from WASM — *"this is fine"* against *"I could not check
> this"*, which is the distinction
> [Chapter 4](04-from-research-to-industry.md) argues everything rests on. Both
> the missing modes and the divergence are fixed: the engine's differential
> harness now reports **0 disagreements across all 473 documents** of the W3C
> corpus, where it previously reported one.

**What has not changed is the editor.** The VS Code extension bundles the 0.1.9
engine, so the capability is present, but its runner asks for `inference: "none"`
deliberately — the reasoning being that inference belongs to the reasoner tier,
and a SHACL finding should be about what the document says rather than what a
second pass added underneath it. That is a defensible position and the manual
does not argue with it; it just means **rules in your shapes do not fire in the
editor today.** Use the CLI or the Python binding for anything rule-bearing, and
expect the editor's report to differ from CI's when rules are in play.

### Named graphs are flattened

Worth repeating here because rules make it sharper: quad syntaxes parse, and
then every named graph and the default graph are merged into one before
validation. A rule's inferences are not attributed to any graph. See
[Chapter 13](13-operate-and-consume.md) §13.1.

---

## 11.8 Rules are a governed artefact

Everything [Chapter 12](12-release-and-change.md) says about ontology change
applies to rules, with one addition: **a rule change alters the meaning of data
you have already validated.** Adding a rule that types every `Employee` as an
`Agent` retroactively brings every `Agent` shape to bear on your whole
employee table.

Four practices:

- **Version rules with the shapes, in the same repository.** They are not
  configuration.
- **Pin `--advanced` and `--iterate-rules` in CI**, exactly as
  [Chapter 9](09-continuous-integration.md) pins `--engine`. Same commit, same
  answer, on every machine.
- **Validate the derived triples, not just the source.** A rule that stops
  firing is invisible unless something downstream asserts it should have.
- **Treat `--iterate-rules > 1` as a deliberate, documented decision.** It is
  outside the specification, so another SHACL processor will not reproduce your
  results.

### Exit codes make this gateable

```
0   conforms
1   violations found
2   could not validate  (bad input, unsupported feature, compile error)
```

Verified across all three. That separation is what lets a CI job distinguish
*"the data is wrong"* from *"the rules did not compile"* — and a job that treats
them the same will eventually go green on a rule set that never ran.

---

> **Run it:** [notebook 2 — Rules and inference](../notebooks/02-rules-and-inference.ipynb)
> runs every rule form above and reproduces all four silent-failure hazards.

## 11.9 Maturity checkpoint

Rules run in CI, versioned alongside the shapes, with derived triples validated
and the flags pinned, is most of SemOps element 4 — *Reasoning & Inference
Operations*. It is the element
[Chapter 14](14-coverage-and-gaps.md) previously marked **partial** on the
strength of the suite's `owlrl` closure and reasoner checks alone.

What is still missing at Level 4 scale: incremental reasoning — every run here
is a full pass — and performance monitoring of inference jobs. Both remain
genuine gaps.

---

| ← [10. Ingest and transform](10-ingest-and-transform.md) | [12. Release and change →](12-release-and-change.md) |
|---|---|
