"""Chapter 13 — Operate and consume."""
import re

from ._common import (ACME, HOLOS_URL, SUITE, V1, V2, Claim, Service, Step, all_of, checks, commit, exit_code,
                      file, has, lacks, nonzero, ok, src)

F = "docs/13-operate-and-consume.md"
FOAF = f"{ACME}/reference_vocab/foaf.rdf"
ORG = f"{ACME}/reference_vocab/org.ttl"
SERVER = Service(f"holos-server --listen 127.0.0.1:7899 --no-ui", f"{HOLOS_URL}/health",
                 note="HOLOS's server, from the HOLOS release, on a spare port")
G_ONT1 = "https://acme.example.org/graph/ontology/1.0.0"
G_ONT2 = "https://acme.example.org/graph/ontology/2.0.0"
G_EMP = "https://acme.example.org/graph/triplified/employees"
POST = f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv --post {HOLOS_URL}/graph --graph {G_EMP}"
HR = "data/policy/hr.trig"
NAMES = ("PREFIX ex: <http://example.com/> SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name "
         "OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name")
GRAPHS = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g"
DOCGEN = f"{SUITE} docgen --ontology {V1} --ref {ORG} --ref {FOAF}"


def _distinct_hashes(at_least):
    """The first three lines of the hash listing are the unpinned runs."""
    def check(r):
        hashes = {line.split()[0] for line in r[-1].stdout.splitlines()[:3]}
        return ok(len(hashes) >= at_least, f"three unpinned runs gave {len(hashes)} different pages",
                  f"three unpinned runs gave only {len(hashes)} distinct page(s)")
    return check


def _pinned_equal(r):
    lines = r[-1].stdout.splitlines()
    a, b = lines[3].split()[0], lines[4].split()[0]
    return ok(a == b, "two runs with PYTHONHASHSEED=0 gave the same page", f"pinned runs differ: {a} vs {b}")


CLAIMS = [
    Claim("C13.01", "consistency-remote against holos-server; the imports rule applies in the store", "13",
          (F, "will be reported as undeclared. Load the imports into a graph the manifest lists."), "run",
          data=["data/remote/graphs-v1.json"],
          services=[SERVER],
          steps=[Step(f"python scripts/gsp_put.py {HOLOS_URL}/graph {G_ONT1} {V1}"),
                 Step(POST),
                 Step(f"python scripts/endpoint_stats.py {HOLOS_URL}/query"),
                 Step(f"{SUITE} consistency-remote --query-endpoint {HOLOS_URL}/query --manifest "
                      f"data/remote/graphs-v1.json --out-dir {{work}}/own-only --fail-on-misalignment"),
                 Step(f"python scripts/gsp_put.py {HOLOS_URL}/graph {G_ONT1} {V1} {FOAF} {ORG}"),
                 Step(f"{SUITE} consistency-remote --query-endpoint {HOLOS_URL}/query --manifest "
                      f"data/remote/graphs-v1.json --out-dir {{work}}/with-imports --fail-on-misalignment")],
          check=checks(has(2, f"{G_ONT1},52", f"{G_EMP},40"),
                       has(3, "live data vs ontology: 0 undeclared class(es), 2 undeclared propert(y/ies)"),
                       exit_code(3, 1),
                       has(5, "template vs ontology: clean",
                           "live data vs ontology: 0 undeclared class(es), 0 undeclared propert(y/ies)"),
                       exit_code(5, 0)),
          checks="with only Acme's own file in the ontology graph, the two FOAF properties are undeclared and the "
                 "run exits 1; with FOAF and org: loaded into the same graph, it is clean and exits 0",
          needs=["holos-cli", "tarka-cli"]),

    Claim("C13.02", "The manifest, as JSON or built in Python; the flags", "13",
          (F, "Or build it in Python, which is worth doing if the URIs come from somewhere"), "run",
          scripts=["scripts/build_manifest.py"],
          steps=[Step("python scripts/build_manifest.py {work}/graphs.json"),
                 Step(f"{SUITE} consistency-remote --help")],
          check=checks(has(0, '"role": "triplified_data"', '"source_tarql": "queries/employees.rq"',
                           f'"ontology_graph_uri": "{G_ONT2}"'),
                       has(1, "--auth-user", "--auth-password", "--sample-limit", "--fail-on-misalignment")),
          checks="the manual's Python snippet writes the manifest it describes; consistency-remote offers "
                 "--auth-user, --auth-password, --sample-limit and --fail-on-misalignment"),

    Claim("C13.03", "The store a version behind: --fail-on-misalignment exits 1", "13",
          (F, "That structure enables a genuine **three-way check**: the live data graph, the"), "run",
          data=["data/remote/graphs-v2-store-behind.json"],
          services=[SERVER],
          steps=[Step(f"python scripts/gsp_put.py {HOLOS_URL}/graph {G_ONT2} {V2} {FOAF} {ORG}",
                      note="the ontology graph is at v2"),
                 Step(POST, note="the data graph is still the v1-era load"),
                 Step(f"python scripts/copy_tree.py {ACME} {{work}}/repaired", note="the query, repaired for v2"),
                 Step(f"{SUITE} consistency --new {{work}}/repaired/acme-org-v2.ttl --old {{work}}/repaired/acme-org-v1.ttl "
                      f"--queries {{work}}/repaired --import-dir {{work}}/repaired --apply-repairs --min-confidence 0.7 "
                      f"--out-dir {{work}}/repair"),
                 Step(f"{SUITE} consistency-remote --query-endpoint {HOLOS_URL}/query --manifest "
                      f"data/remote/graphs-v2-store-behind.json --out-dir {{work}}/remote --fail-on-misalignment"),
                 Step(f"{SUITE} consistency-remote --query-endpoint {HOLOS_URL}/query --manifest "
                      f"data/remote/graphs-role-typo.json --out-dir {{work}}/typo --fail-on-misalignment")],
          check=checks(has(4, "template vs ontology: clean", "live data vs ontology: 1 undeclared class(es)",
                           "'classes_only_in_template': ['https://acme.example.org/ns/SoftwareEngineer']",
                           "'classes_only_in_live_data': ['https://acme.example.org/ns/Engineer']"),
                       exit_code(4, 1),
                       lacks(5, "==="), exit_code(5, 0)),
          checks="the repaired query agrees with the v2 ontology, the live data does not (Engineer only in the "
                 "store, SoftwareEngineer only in the template), and the run exits 1; with the role misspelt, "
                 "the same store reports no graph at all and exits 0",
          needs=["holos-cli", "tarka-cli"]),

    Claim("C13.04", "A mistyped role compares nothing, successfully", "13",
          (F, "> **`role` is not validated, and a typo costs you the whole check.**"), "run",
          data=["data/remote/graphs-role-typo.json"], same_as="C13.03"),

    Claim("C13.05", "SHACL validation flattens named graphs", "13",
          (F, "> **But SHACL validation itself does not see them.**"), "run", same_as="C14.07"),

    Claim("C13.06", "Policy at the scan: rows without the column, unless you are in HR", "13",
          (F, "Here it is through the `holosdb` package from PyPI, on HOLOS's small HR example,"), "run",
          data=[HR],
          scripts=["scripts/holosdb_policy.py"],
          steps=[Step(f"python scripts/holosdb_policy.py {HR}")],
          check=has(0, "2. salary denied except to role hr, asked by alice:\n    name=Alice, salary=None\n"
                       "    name=Bob, salary=None\n    name=Carol, salary=None",
                    "3. the same, asked by alice with role hr:\n    name=Alice, salary=95000\n"
                    "    name=Bob, salary=88000\n    name=Carol, salary=102000",
                    "4. COUNT of salaries without the role:\n    n=0",
                    "5. named graphs, reviews labelled at level 3, no clearance:\n    g=http://example.com/provenance\n"
                    "    g=http://example.com/public\n6.",
                    "6. named graphs, with clearance 3:\n    g=http://example.com/provenance\n"
                    "    g=http://example.com/public\n    g=http://example.com/reviews",
                    "7. salary denied with fail_closed():\n    HolosError: access denied by policy",
                    "8. (mistake) policy method called as a statement:\n    n=3"),
          checks="every row of the manual's table: no salaries without the role and all three with it; COUNT 0; "
                 "the labelled graph absent without clearance and present with it; fail_closed raises; and a "
                 "policy method called as a statement leaves no policy (3 salaries counted)"),

    Claim("C13.07", "The fluent API mistake", "13",
          (F, "fluent API: each `Policy` method returns a new policy. Calling them as statements"), "run",
          same_as="C13.06"),

    Claim("C13.08", "The holos command gives the same answers", "13",
          (F, "The `holos query` command from the release takes the same"), "run",
          data=[HR],
          steps=[Step(f'holos query --data {HR} --query "{NAMES}" --deny-predicate http://example.com/salary '
                      f'--except-role hr'),
                 Step(f'holos query --data {HR} --query "{NAMES}" --deny-predicate http://example.com/salary '
                      f'--except-role hr --role hr'),
                 Step(f'holos query --data {HR} --query "{NAMES}" --deny-predicate http://example.com/salary --fail-closed'),
                 Step(f'holos query --data {HR} --query "{GRAPHS}" --label-graph http://example.com/reviews=3'),
                 Step(f'holos query --data {HR} --query "{GRAPHS}" --label-graph http://example.com/reviews=3 --clearance 3')],
          check=checks(lacks(0, "95000"), has(1, "95000", "88000", "102000"),
                       nonzero(2), has(2, "access denied by policy"),
                       lacks(3, "http://example.com/reviews"), has(4, "http://example.com/reviews")),
          checks="the same five answers as the Python API", needs=["holos-cli"]),

    Claim("C13.09", "8 ns per quad, by HOLOS's own measurement", "13",
          (F, "All verified at 0.21.1. HOLOS measures the cost at 8 ns per quad, about 1% of"), "source",
          sources=[src("HOLOS ACCESS-CONTROL.md", file("holos", "ACCESS-CONTROL.md", "44"),
                       "It costs **8 ns per quad** — measured, and about 1% of what decoding the quad costs.")]),

    Claim("C13.10", "Validation and the store: written into it up to 0.21.0, untouched from 0.21.1", "13",
          (F, "Two things to know before you validate a store you care about."), "run",
          data=["data/shacl/two-unnamed.ttl", "data/shacl/shapes-violation.ttl", "data/shacl/shapes-sparql.ttl"],
          scripts=["scripts/holosdb_validate_repeat.py", "scripts/holosdb_validate.py"],
          steps=[Step("python scripts/holosdb_validate.py data/shacl/two-unnamed.ttl data/shacl/shapes-violation.ttl "
                      "data/shacl/shapes-sparql.ttl"),
                 Step("python scripts/holosdb_validate_repeat.py data/shacl/two-unnamed.ttl "
                      "data/shacl/shapes-violation.ttl {work}/store"),
                 Step("holos --version"),
                 Step("holos stats --data data/shacl/two-unnamed.ttl --store {work}/cli-store"),
                 Step("holos validate --store {work}/cli-store --shapes data/shacl/shapes-violation.ttl"),
                 Step("holos validate --store {work}/cli-store --shapes data/shacl/shapes-violation.ttl"),
                 Step('holos query --store {work}/cli-store --query "SELECT ?g (COUNT(*) AS ?n) WHERE '
                      '{ GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"'),
                 Step('holos update --store {work}/cli-store --update "INSERT DATA { GRAPH <urn:holos:shapes> '
                      '{ <urn:x:s> <urn:x:p> <urn:x:o> } }"', note="plant what an earlier version would have left"),
                 Step("holos validate --store {work}/cli-store --shapes data/shacl/shapes-violation.ttl"),
                 Step("holos --help")],
          check=lambda r: _validation_and_the_store(r),
          checks="on a fresh store both engines report the 2 true violations, and native refuses sh:sparql; the CLI's "
                 "default engine is native. Then, by version. At 0.21.0: three calls on one store report 2, 4 and 6; "
                 "one validate() leaves a 5-quad shapes graph, which survives reopening a persistent store; the CLI "
                 "with --store does the same. From 0.21.1: 2, 2 and 2; no graph left, on disk or in memory; a "
                 "leftover shapes graph is reported with the DROP GRAPH that removes it, by Python and by the CLI",
          needs=["holos-cli"],
          sources=[src("HOLOS commit cd5af4b", commit("holos", "cd5af4b32082458ee087d92948020a1b77cd3e9d"),
                       "Engine::with_transient_graph loads input inside a commit scope that is always rolled back"),
                   src("HOLOS commit 82e4d66, 'Cut 0.21.1'", commit("holos", "82e4d6686b3563db502ea68098a6f3fc9ce75d6b"),
                       "validation leaves nothing in the store it validates")],
          notes="The recorded run uses 0.21.1, so it shows the fix. The same steps against the published 0.21.0 "
                "gave: `violations [2, 4, 6]` for both engines; a 5-quad `urn:holos:python:shapes` graph after one "
                "call, still there after reopening a persistent store; no warning for a planted leftover; and from "
                "the CLI `results 2`, then `results 4`, with a `urn:holos:shapes` graph left behind. "
                "The Python method's default engine, adapted, is in its signature: "
                + f"[holos-python lib.rs]({file('holos', 'crates/holos-python/src/lib.rs', '647-674')})."),

    Claim("C13.11", "docgen: 4 classes, 5 external terms, 3 resolved", "13",
          (F, "2 object properties, 3 datatype properties, 1 sections,"), "run",
          steps=[Step(f"{DOCGEN} --out-dir {{work}}/docs"),
                 Step("python scripts/list_files.py {work}/docs")],
          check=checks(has(0, "prefix='acme', 4 classes, 2 object properties, 3 datatype properties, 1 sections, "
                              "5 external terms (3 resolved)."),
                       has(1, "ontology-documentation.html", "ontology_doc_data.json", "class-diagrams/")),
          checks="the summary line as quoted; the HTML page, the JSON and the per-class diagrams are written"),

    Claim("C13.12", "Three runs, three pages; pinned, one", "13",
          (F, "Re-checked at 0.22.0: three identical runs, three different files."), "run",
          steps=[Step(f"{DOCGEN} --out-dir {{work}}/run1"),
                 Step(f"{DOCGEN} --out-dir {{work}}/run2"),
                 Step(f"{DOCGEN} --out-dir {{work}}/run3"),
                 Step(f"{DOCGEN} --out-dir {{work}}/seed0-a", env={"PYTHONHASHSEED": "0"}),
                 Step(f"{DOCGEN} --out-dir {{work}}/seed0-b", env={"PYTHONHASHSEED": "0"}),
                 Step("python scripts/sha256.py {work}/run1/ontology-documentation.html "
                      "{work}/run2/ontology-documentation.html {work}/run3/ontology-documentation.html "
                      "{work}/seed0-a/ontology-documentation.html {work}/seed0-b/ontology-documentation.html")],
          check=checks(_distinct_hashes(2), _pinned_equal),
          checks="the three unpinned runs give at least two different pages (each run draws its own hash seed, "
                 "so three matching by chance is possible but unlikely); the two pinned runs give the same page",
          sources=[src("suite issue #3", "https://github.com/pwin/consolidated-ontology-quality-suite-python/issues/3")]),

    Claim("C13.13", "Every row carries source_file and line", "13",
          (F, "> **Every check run writes `full_results.csv`. Retain them, timestamped.**"), "run", same_as="C09.10"),

    Claim("C13.14", "HOLOS: embeddable, RDF 1.2, GeoSPARQL", "13",
          (F, "| Python · JS | HOLOS (`holosdb`, `holos-wasm`) | Policy at the scan, RDF 1.2, GeoSPARQL; early |"), "run",
          scripts=["scripts/holos_facts.py"],
          steps=[Step("python scripts/holos_facts.py")],
          check=has(0, "GeoSPARQL functions registered: 49", "includes geof:buffer and geof:boundary: True / True"),
          checks="the holosdb wheel registers 49 GeoSPARQL functions"),

    Claim("C13.15", "The editor's checks run on holos-wasm-node", "13",
          (F, "HOLOS appears in the editor too: the VS Code extension's checks run on"), "source", same_as="C07.04"),

    Claim("C13.16", "Observability and APIs are not covered", "13",
          (F, "**None of this is in the toolchain.**"), "argument",
          notes="A statement of scope, checkable by its absence: no subcommand of the suite, and no command in the "
                "other releases, exports metrics or serves an API other than the SPARQL and Graph Store protocols "
                "of holos-server (C10.15, C13.01)."),
]


def _version(text, prefix):
    m = re.search(rf"{prefix} (\d+)\.(\d+)\.(\d+)", text)
    return tuple(int(x) for x in m.groups()) if m else None


def _validation_and_the_store(r):
    common = [has(0, "adapted: {'conforms': False, 'violations': 2, 'engine': 'adapted'}",
                  "native:  {'conforms': False, 'violations': 2, 'engine': 'native'}",
                  "HolosError: unsupported: sh:sparql is not implemented")(r),
              has(9, "--engine <NAME>          native (default) or adapted")(r)]
    py, cli = _version(r[1].stdout, "holosdb"), _version(r[2].out, "holos")
    if py is None or cli is None:
        return False, "could not read the holosdb or holos version"
    if py >= (0, 21, 1):
        common.append(has(1, "adapted, three calls on one store: violations [2, 2, 2]",
                          "native, three calls on one store: violations [2, 2, 2]",
                          "named graphs after one validate(): []",
                          "named graphs in the persistent store after reopening: []",
                          'store.update("DROP GRAPH <urn:holos:python:shapes>") removes them')(r))
    else:
        common.append(has(1, "adapted, three calls on one store: violations [2, 4, 6]",
                          "native, three calls on one store: violations [2, 4, 6]",
                          "named graphs after one validate(): [('urn:holos:python:shapes', 5)]",
                          "named graphs in the persistent store after reopening: [('urn:holos:python:shapes', 5)]")(r))
    if cli >= (0, 21, 1):
        common += [has(4, "results           2")(r), has(5, "results           2")(r), lacks(6, "urn:holos:shapes")(r),
                   has(8, "note: <urn:holos:shapes> holds 1 quads", "DROP GRAPH <urn:holos:shapes>")(r)]
    else:
        common += [has(4, "results           2")(r), has(5, "results           4")(r), has(6, "urn:holos:shapes")(r)]
    passed, detail = all_of(*common)
    return passed, f"holosdb {'.'.join(map(str, py))}, holos {'.'.join(map(str, cli))}: {detail}"
