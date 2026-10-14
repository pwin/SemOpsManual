"""Chapter 14 — Coverage and gaps."""
import re

from ._common import (ACME, SUITE, V1, Claim, Step, all_of, checks, commit, file, has, lacks, ok, src)

F = "docs/14-coverage-and-gaps.md"
PREV = "fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40"
FILES = f"{V1} {ACME}/reference_vocab/org.ttl {ACME}/reference_vocab/foaf.rdf"


def _tally(seed, outcome, at_least, of):
    def check(r):
        m = re.search(rf"PYTHONHASHSEED={seed}: HermiT ran (\d+) of {of}, did not run (\d+) of {of}", r[0].stdout)
        if not m:
            return False, f"no tally for seed {seed}"
        ran, not_ran = int(m.group(1)), int(m.group(2))
        n = ran if outcome == "ran" else not_ran
        return ok(n >= at_least, f"seed {seed}: HermiT ran {ran} of {of}, did not run {not_ran}",
                  f"seed {seed}: {outcome} only {n} of {of}")
    return check


CLAIMS = [
    Claim("C14.01", "A scoped run cannot see that the reasoner did not run", "14",
          (F, "### A scoped run cannot see that the reasoner did not run"), "run", same_as="C09.09"),

    Claim("C14.02", "The shacl CLI reports conformance when it checked nothing", "14",
          (F, "The one-shot Python and JavaScript calls refuse a shapes graph that declares no"), "run",
          same_as="C11.07"),

    Claim("C14.03", "holos validate exits 0 on a non-conforming graph", "14",
          (F, "Both of its validators print `conforms false` and return exit status 0; a"), "run", same_as="C11.29"),

    Claim("C14.04", "tarka drops instances it cannot build, silently, in the CLI and in Python", "14",
          (F, "An OTTR template whose `ottr:IRI` parameter receives a cell tarka does not accept"), "run",
          same_as="C10.11",
          notes="The Python half is in C10.12: `Mapping.ottr(...).run_csv(...)` returns None, raises nothing and "
                "writes 0 triples."),

    Claim("C14.05", "docgen reshuffles the page on every run", "14",
          (F, "Still open at 0.22.0, re-checked rather than carried forward: three identical runs"), "run",
          same_as="C13.12"),

    Claim("C14.06", "The reasoner's outcome follows the hash seed", "14",
          (F, "It is not random, and it is not HermiT."), "run",
          scripts=["scripts/reasoner_seeds.py", "scripts/owlready2_probe.py"],
          steps=[Step("python scripts/reasoner_seeds.py {work} 10 0 5", timeout=1200)],
          check=checks(_tally("5", "ran", 9, 10), _tally("0", "did not run", 7, 10),
                       has(0, "could not be run: cannot access local variable 'entity' where it is not associated with a value")),
          checks="ten runs per seed through the suite: seed 5 runs HermiT in at least 9, seed 0 fails in at least 7. "
                 "The thresholds sit below the recorded tallies on purpose: C14.08 shows the one thing the seed does "
                 "not control, and where the failure happens"),

    Claim("C14.07", "SHACL validates the union of the named graphs", "14",
          (F, "Quad syntaxes parse, and then every named graph and the default graph are merged"), "run",
          data=["data/shacl/graphs.trig", "data/shacl/graphs-flat.ttl"],
          steps=[Step("shacl -d data/shacl/graphs.trig -s data/shacl/shapes-violation.ttl"),
                 Step("shacl -d data/shacl/graphs-flat.ttl -s data/shacl/shapes-violation.ttl"),
                 Step("shacl --help")],
          check=checks(has(0, "focus <http://example.org/bob>", "focus <http://example.org/carol>",
                           "focus <http://example.org/dave>"),
                       lambda r: ok(r[0].stdout == r[1].stdout, "the TriG and the flattened file give identical reports",
                                    "the two reports differ"),
                       lacks(2, "--graph")),
          checks="three results, one per person, whichever graph each was in; the same report as the flattened "
                 "file; no graph-selection option in --help",
          needs=["shacl-cli"]),

    Claim("C14.08", "Almost: the seed decides most of owlready2's load, and not all of it", "14",
          (F, "*Almost*, because I had first written \"every time\", and the evidence for this"), "run",
          scripts=["scripts/load_repeat.py", "scripts/owlready2_probe.py"],
          steps=[Step("python scripts/load_repeat.py {work} 15", timeout=1800)],
          check=checks(lambda r: _load_tally(r, "2.", "failed", 9),
                       lambda r: _load_tally(r, "3.", "loaded", 13),
                       lambda r: ok(re.search(r"failures were while building: <http://xmlns.com/foaf/0.1/primaryTopic> "
                                              r"\(\d+\)$", r[0].stdout.strip(), re.M) is not None,
                                    "every failure was owlready2 building foaf:primaryTopic",
                                    "a failure on some other entity, or none at all")),
          checks="loading the merged ontology straight into owlready2, with the load path and blank-node labels fixed: "
                 "seed 0 fails in at least 9 of 15 and seed 5 loads in at least 13 of 15; every failure is while "
                 "building foaf:primaryTopic. The exact tallies, including any loads that go the other way, are "
                 "recorded rather than asserted",
          sources=[src("suite reasoning/backends/external_backend.py: a fresh TemporaryDirectory, loaded by path",
                       file("suite", "ontology_suite/reasoning/backends/external_backend.py", "94-106"),
                       "onto = world.get_ontology(str(owl_path)).load()")],
          notes="HermiT is never called here: the failure, when it comes, is in loading."),

    Claim("C14.09", "Without Java the message is the operating system's", "14",
          (F, "\"cannot find the file specified\", so a genuinely missing Java *is*"), "run",
          scripts=["scripts/without_java.py"],
          steps=[Step(f"python scripts/without_java.py {SUITE} ontology --ontology {V1} --import-dir {ACME} "
                      f"--out-dir {{work}}/out --reports minimal", env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/out/full_results.csv --by focus --check REA-022")],
          check=checks(has(0, "without_java: java on PATH now: none"),
                       lambda r: _rea022_message(r, "cannot find the file specified", "entity")),
          checks="with Java hidden and seed 5 (so owlready2 loads), REA-022's message names the missing file and "
                 "not 'entity'"),

    Claim("C14.39", "REA-020 says inconsistent when only a class is unsatisfiable", "14",
          (F, "When HermiT does run on the fixture, the suite reports `REA-020`, *\"the ontology"), "run",
          data=["data/reasoner/clean.ttl"],
          scripts=["scripts/hermit_verdict.py"],
          steps=[Step(f"python scripts/hermit_verdict.py {FILES}", env={"PYTHONHASHSEED": "5"}),
                 Step(f"{SUITE} ontology --ontology {V1} --import-dir {ACME} --out-dir {{work}}/acme --reports minimal",
                      env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/acme/full_results.csv"),
                 Step("python scripts/hermit_verdict.py data/reasoner/clean.ttl"),
                 Step(f"{SUITE} ontology --ontology data/reasoner/clean.ttl --out-dir {{work}}/clean --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/clean/full_results.csv")],
          check=checks(has(0, "HermiT: consistent", "owl:Nothing among them: True",
                           "https://acme.example.org/ns/Contractor"),
                       has(2, "REA-020", "REA-021"),
                       has(3, "HermiT: consistent", "unsatisfiable classes: none"),
                       lacks(5, "REA-020", "REA-021", "REA-022")),
          checks="on the fixture HermiT finds the ontology consistent, with Contractor and owl:Nothing unsatisfiable, "
                 "and the suite reports REA-020 as well as REA-021; on a clean ontology HermiT finds nothing and the "
                 "suite reports neither",
          sources=[src("suite external_backend.py, the belt-and-braces rule",
                       file("suite", "ontology_suite/reasoning/backends/external_backend.py", "128-133"),
                       "thing_or_nothing = {owlready2.Thing, owlready2.owl.Nothing}"),
                   src("testing repo detect.py, 03b-unsatisfiable-class", file("testing", "detect.py", "115-128"),
                       'forbidden=("REA-001", "CNF-001", "CNF-002"),')],
          notes="Needs Java, and a hash seed under which owlready2 loads (5 here; see C14.06)."),

    Claim("C14.10", "A mistyped manifest role compares nothing, successfully", "14",
          (F, "`consistency-remote` accepts any string as a graph's `role` and ignores all but"), "run",
          same_as="C13.03"),

    # The "smaller ones" table: one claim per row, each pointing at its evidence.
    Claim("C14.11", "--help offers owlrl; asking for it gives a traceback", "14",
          (F, "| `--help` still offers `--inference owlrl` and `both`; asking for one gives a Python traceback"),
          "run", same_as="C07.26"),
    Claim("C14.12", "--inference is ignored under --engine sparql", "14",
          (F, "| Under `--engine sparql`, `--inference` is accepted and ignored"), "run", same_as="C07.27"),
    Claim("C14.13", "The near-miss warning lists blank-node identifiers", "14",
          (F, "| The `--own-namespace` near-miss warning lists two blank-node identifiers"), "run", same_as="C09.07"),
    Claim("C14.14", "--registry replaces, so @builtin with a house registry is UNMAPPED", "14",
          (F, "| `--sparql` composes but `--registry` replaces"), "run", same_as="C08.24"),
    Claim("C14.15", "One contradiction, two LOG-001s", "14",
          (F, "| `data` and `run` report one contradiction as two `LOG-001`s"), "run", same_as="C09.14"),
    Claim("C14.16", "The DSL's TypeError and Quad type", "14",
          (F, "| The DSL gives unchecked code an internal `TypeError`"), "run", same_as="C08.15"),
    Claim("C14.17", "triplify drives oxi-gen only", "14",
          (F, "| The suite's `triplify` and the extension's *Run Full Triplify* drive `oxi-gen` only"), "run",
          same_as="C10.17"),
    Claim("C14.18", "consistency and pattern-consistency are report-only by default", "14",
          (F, "| `consistency` and `pattern-consistency` exit 0 whatever they find"), "run", same_as="C12.14"),
    Claim("C14.19", "holosdb's native validator doubles the count", "14",
          (F, "| `holosdb`'s `Store.validate(…, engine=\"native\")` reports twice the violations"), "run",
          same_as="C13.10"),
    Claim("C14.20", "sketch reads every file with the first file's prefixes", "14",
          (F, "| When two query files bind one prefix differently, `sketch` reads every file"), "run",
          same_as="C10.29"),

    Claim("C14.21", "Documentation drift, upstream", "14",
          (F, "None of these changes what a tool does. All of them change what a careful reader"), "run",
          steps=[Step(f"{SUITE} checks --help")],
          check=has(0, "'both' runs pyshacl", "not a default dependency"),
          checks="the suite's --engine help still says 'both' runs pyshacl and 'native' is not a default dependency",
          sources=[src("suite docs/REPORTS.md says 0.15.0 (see C09.11 for 0.17.0)", file("suite", "docs/REPORTS.md", "18"),
                       "## What changed in 0.15.0"),
                   src("suite docs/REASONING.md", file("suite", "docs/REASONING.md", "107"),
                       "Uses `owlready2` (the `reasoner` extra: `uv sync --extra reasoner`)"),
                   src("suite pyproject.toml at its first commit: owlready2 a base dependency",
                       file("suite", "pyproject.toml", "14", ref="d0ba3679644360c31118295f9ba8738c85111e95"),
                       '"owlready2>=0.51",'),
                   src("extension README (0.15.0) names Oxigraph", file("webapp", "README.md", "86"),
                       "Oxigraph, `shacl-wasm`, and `eyereasoner` are all"),
                   src("testing repo README", file("testing", "README.md", "22"), "18 Turtle files in 10 folders"),
                   src("testing repo README", file("testing", "README.md", "31"), "All 16 fixtures pass"),
                   src("suite main branch, stopped at 0.18.0", file("suite", "pyproject.toml", "3", ref="main"),
                       'version = "0.18.0"')],
          notes="The testing repository's `ontologies/` holds 14 folders and 25 Turtle files at 6d078a1; its "
                "detect.py declares 17 fixtures (C09.19). The suite's default branch on GitHub is `develop`."),

    Claim("C14.22", "The registry grew from 50 checks to 61", "14",
          (F, "registry grows, as it did from 50 checks to 61, and the scoped run is the one whose"), "source",
          sources=[src("suite registry.json at v0.8.0", file("suite", "ontology_suite/resources/registry.json", ref="v0.8.0")),
                   src("suite registry.json at v0.14.2", file("suite", "ontology_suite/resources/registry.json", ref="v0.14.2"))],
          notes="Counted from the tagged files: 50 entries at v0.5.0 and v0.8.0, 56 at v0.10.0, 61 from v0.14.2."),

    Claim("C14.23", "Closed: the engines are the toolchain's own", "14",
          (F, "**The engines are the toolchain's own.**"), "run", same_as="C07.22"),
    Claim("C14.24", "Closed: messages on blank nodes", "14",
          (F, "**Messages on blank nodes.**"), "run", same_as="C07.07"),
    Claim("C14.25", "Closed: findings say where they are", "14",
          (F, "**Findings say where they are.**"), "run", same_as="C08.17"),
    Claim("C14.26", "Closed: house rules compose with the built-ins", "14",
          (F, "**House rules compose with the built-ins.**"), "run", same_as="C08.25"),

    Claim("C14.27", "Five suite defects found by the testing repository", "14",
          (F, "**Five suite defects found by the testing repository**"), "source",
          sources=[src("suite commit cd72df1: language-tagged literals, and per-row entities",
                       commit("suite", "cd72df19132e76cb91d3f775943c054d3a1e617a"), "Both found by the sibling fixture repo"),
                   src("suite commit 9defc24: the namespace legend", commit("suite", "9defc24d331866420b6532f407612ed35089d834")),
                   src("testing repo CT-01 README: the legend's false finding, until suite 0.20.0",
                       file("testing", "experiments/SpecificTests/CT-01-iri-template-drift/README.md", "50-52"),
                       "It held one entry until suite 0.20.0."),
                   src("suite commit def9038: the default namespace", commit("suite", "def9038a8d43cfcf421c0c04b90ee0e400cd8df1"),
                       "Found while building an isolated fixture for CT-3"),
                   src("suite commit cae9ef2: --sparql replacing the built-ins",
                       commit("suite", "cae9ef21cf33ceb8eba33ef94da66b32bf810ded"),
                       "Found in exactly that state: the separate testing repo's CI gate config")]),

    Claim("C14.28", "Closed: sh:conforms follows the specification", "14",
          (F, "**`sh:conforms` means what the specification says**, from engine 0.3.0, and the"), "run",
          same_as="C11.04"),
    Claim("C14.29", "Closed: the repair engine keeps blank nodes and base directions", "14",
          (F, "**The repair engine** keeps blank nodes and base directions intact when it writes"), "source",
          same_as="C08.08"),
    Claim("C14.30", "Early, but real: policy, rules, a triplifier", "14",
          (F, "**Early, but real:** read access policy at the index scan, with classification,"), "run",
          same_as="C13.06"),

    Claim("C14.31", "Wrong: the migration annotation's direction", "14",
          (F, "**The migration annotation's direction.** Every earlier edition said rename"), "run", same_as="C12.05"),
    Claim("C14.32", "Wrong: REA-022 as the tell in a scoped run", "14",
          (F, "**`REA-022` as the reasoner's tell in a scoped run.**"), "run", same_as="C09.09"),
    Claim("C14.33", "Wrong: the reasoner as flaky", "14",
          (F, "**The reasoner as \"flaky\".**"), "run", same_as="C14.06"),
    Claim("C14.34", "Wrong: the reasoner as an optional extra", "14",
          (F, "**The reasoner as an \"optional extra\".**"), "run", same_as="C07.05"),
    Claim("C14.35", "Wrong: stale numbers", "14",
          (F, "**Stale numbers in my own pages.**"), "source",
          sources=[src("the previous edition's Chapter 8", file("manual", "docs/08-model-and-validate.md", "326", ref=PREV),
                       "close to 300 findings")],
          notes="Today's figures are reproduced in C09.02 (479), C09.04 (23) and C07.22 (22 or 23)."),
    Claim("C14.36", "Wrong: where a CONCAT-built IRI goes", "14",
          (F, "**Where a `CONCAT`-built IRI goes.**"), "run", same_as="C10.05"),
    Claim("C14.37", "Wrong: when rules arrived in the SHACL engine", "14",
          (F, "**When rules arrived in the SHACL engine.**"), "source", same_as="C11.03"),
    Claim("C14.38", "Wrong: the SHACL engine's pass rate", "14",
          (F, "**The pass rate of the SHACL engine**, which I would have written as 426 of 426."), "source",
          same_as="C11.08"),
]


def _load_tally(r, line, outcome, at_least):
    m = re.search(rf"^{re.escape(line)}.*?loaded (\d+) of \d+, failed (\d+) of \d+", r[0].stdout, re.M)
    if not m:
        return False, f"no tally on line {line}"
    n = int(m.group(1) if outcome == "loaded" else m.group(2))
    return ok(n >= at_least, f"line {line} {outcome} {n} times (at least {at_least})",
              f"line {line} {outcome} only {n} times")


def _rea022_message(r, want, unwanted):
    import csv
    path = r.file("out/full_results.csv")
    with open(path, encoding="utf-8", newline="") as f:
        msgs = [x["message"] for x in csv.DictReader(f) if x["check_id"] == "REA-022"]
    if not msgs:
        return False, "no REA-022 finding"
    return all_of(ok(want in msgs[0], f"REA-022 says '{want}'", f"REA-022 message: {msgs[0][:160]!r}"),
                  ok(unwanted not in msgs[0], f"and not '{unwanted}'", f"REA-022 mentions '{unwanted}'"))
