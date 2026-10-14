"""Chapter 11 — Rules and inference."""
from ._common import (ACME, Claim, Step, all_of, checks, commit, exit_code, file, has, lacks, nonzero, ok, src)

F = "docs/11-rules-and-inference.md"
S = "data/shacl"
R = "data/rules"
PREV = "fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40"   # the previous edition


def _conforms(step, value):
    def check(r):
        out = r[step].out
        want = f"conforms: {'true' if value else 'false'}"
        return ok(want in out, f"step {step + 1}: {want}", f"step {step + 1}: expected '{want}'")
    return check


CLAIMS = [
    Claim("C11.01", "The suite and the extension do not run SHACL-AF rules", "11",
          (F, "The Ontology Quality Suite does not run SHACL-AF rules (there is no `--advanced`"), "run",
          steps=[Step(f"ontology-quality-suite {c} --help") for c in ("checks", "data", "ontology", "run")],
          check=checks(*[lacks(i, "--advanced") for i in range(4)]),
          checks="none of checks, data, ontology or run offers --advanced"),

    Claim("C11.02", "The Python surface: inference modes, and an unknown one is an error", "11",
          (F, "From Python, rules are reached through the `inference` argument rather than a"), "run",
          data=[f"{R}/triple.ttl", f"{R}/people.ttl"],
          scripts=["scripts/shacl_python.py"],
          steps=[Step(f"python scripts/shacl_python.py {S} {R}")],
          check=has(0, "inference=none             conforms=True results=0",
                    "inference=rules            conforms=False results=1",
                    "inference=rules-iterated   conforms=False results=1",
                    'inference=bogus            ERROR: unknown inference "bogus"'),
          checks="rules and rules-iterated fire (one result, from the rule's output); none does not; an "
                 "unknown mode is an error naming the accepted ones"),

    Claim("C11.03", "Rules shipped in 0.1.8; the $this fix came with them", "11",
          (F, "> **Check your version before believing any of this.**"), "source",
          sources=[src("engine commit 8de05ba, 'Implement SHACL-AF rules' (after the v0.1.7 tag, version string "
                       "still 0.1.7)", commit("shacl", "8de05bae23e410d97c040743f4ca7e0eb4ff6947"),
                       "`$this` was never substituted into a `CONSTRUCT` query."),
                   src("engine commit 637ebf5, rules in both bindings (before v0.1.8)",
                       commit("shacl", "637ebf5b0dc9715bc1af4102cb7cd964c92374f2"),
                       "Rules reach the WASM and Python bindings as inference modes"),
                   src("engine commit 2134124, v0.1.9", commit("shacl", "2134124fb3268ec4700f39ba66ad576e31fff004"),
                       "this version exists so all three channels carry the same number rather than leaving npm a "
                       "release behind")],
          notes="`git tag --contains 8de05ba` begins at v0.1.8. The v0.1.7 tree has no `-a`/`--advanced` flag in "
                "the CLI; the commit that adds it still declares version 0.1.7 in Cargo.toml."),

    Claim("C11.04", "Warnings break conformance; --allow-warnings records the choice", "11",
          (F, "Verified on 0.3.2, with a shape whose only result is a Warning:"), "run",
          data=[f"{S}/data.ttl", f"{S}/shapes-warning.ttl"],
          steps=[Step(f"shacl -d {S}/data.ttl -s {S}/shapes-warning.ttl"),
                 Step(f"shacl -d {S}/data.ttl -s {S}/shapes-warning.ttl --allow-warnings -f turtle"),
                 Step("shacl --help")],
          check=checks(_conforms(0, False), exit_code(0, 1), exit_code(1, 0), has(1, "sh:conforms true",
                                                                                   "sh:conformanceDisallows sh:Violation"),
                       has(2, "--allow-warnings", "--allow-infos", "--min-severity")),
          checks="warnings only: conforms false, exit 1; with --allow-warnings: conforms true, exit 0, and the "
                 "report records sh:conformanceDisallows sh:Violation; --help offers --allow-infos and --min-severity",
          needs=["shacl-cli"],
          sources=[src("engine commit 2006c4e (0.3.0)", commit("shacl", "2006c4e5766f8145d025a118c0d96ec3c2bfcb74"),
                       "The harness had recomputed the expected report's conformance under the engine's own rule "
                       "instead of reading the value the test wrote, so it agreed with itself.")]),

    Claim("C11.05", "The WebAssembly build agrees since 0.3.2", "11",
          (F, "**The surfaces disagreed for two releases.**"), "run",
          scripts=["scripts/wasm_conforms.mjs"],
          steps=[Step(f"node scripts/wasm_conforms.mjs {S}")],
          check=has(0, "shacl-wasm-node 0.3.2  shapes-warning.ttl     conforms=false"),
          checks="shacl-wasm-node 0.3.2 calls a warnings-only graph non-conforming",
          needs=["node"],
          sources=[src("engine commit 2eea15d", commit("shacl", "2eea15d58b6a9bf277c13a9dfbef93d47f1d5aa3"))]),

    Claim("C11.06", "The one-shots refuse an empty shapes graph", "11",
          (F, "So the one-shots now refuse a shapes graph that declares nothing."), "run",
          scripts=["scripts/shacl_python.py"],
          steps=[Step(f"python scripts/shacl_python.py {S} {R}")],
          check=has(0, "validate(data, shapes)                       conforms=False results=1",
                    "validate(shapes, data)  [swapped]            REFUSED: ValueError: the shapes graph declares no "
                    "shapes, so this would report that the data conforms without having checked anything"),
          checks="validate(data, shapes) finds one result; the swapped call is refused with the quoted message",
          sources=[src("engine commit a567c2e (0.2.0)", commit("shacl", "a567c2edfb93e8053058c8976eef8fd95388a292"),
                       "validating against no shapes conforms")]),

    Claim("C11.07", "The CLI does not refuse: no shapes, or no -s, conforms", "11",
          (F, "**The command line does not refuse.**"), "run",
          data=[f"{S}/no-shapes.ttl"],
          steps=[Step(f"shacl -d {S}/data.ttl -s {S}/no-shapes.ttl"),
                 Step(f"shacl -d {S}/data.ttl")],
          check=checks(_conforms(0, True), exit_code(0, 0), _conforms(1, True), exit_code(1, 0)),
          checks="both runs: conforms true, exit 0",
          needs=["shacl-cli"]),

    Claim("C11.08", "425 of 426 W3C tests, the exception named", "11",
          (F, "The engine passes **425 of the 426** W3C SHACL 1.0 and 1.2 tests"), "source",
          sources=[src("engine README", file("shacl", "README.md", "289"), "425 of 426"),
                   src("engine README, the subquery rule", file("shacl", "README.md", "316-323"),
                       "0.3.0 briefly enforced the letter of the rule and passed all 426."),
                   src("engine commit 1944802 (0.3.1)", commit("shacl", "1944802e9a33b0116d6b660045c9d2813f9ef2d5")),
                   src("engine README, the EARL report", file("shacl", "README.md", "364-367"),
                       "The W3C compiles a specification's implementation report from EARL files")]),

    Claim("C11.09", "holos rules materialises into a graph of its own", "11",
          (F, "Verified on the acme employees, with one rule typing every `acme:Employee` as a"), "run",
          data=["data/holos/rules.rq"],
          steps=[Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv --ntriples -o {{work}}/employees.nt"),
                 Step("holos stats --data {work}/employees.nt --store {work}/store"),
                 Step("holos rules --store {work}/store --rules data/holos/rules.rq"),
                 Step("holos query --store {work}/store --query \"SELECT ?g (COUNT(*) AS ?n) WHERE "
                      "{ GRAPH ?g { ?s ?p ?o } } GROUP BY ?g\"")],
          check=checks(exit_code(2, 0), has(2, "derived 5 fact(s) into <https://holos.dev/ns#derived>",
                                            "rounds  2", "store   40 -> 45 quads"),
                       has(3, "https://holos.dev/ns#derived", '"value":"5"')),
          checks="5 facts derived in 2 rounds into holos:derived; the store goes from 40 to 45 quads; the "
                 "derived graph holds the 5",
          needs=["tarka-cli", "holos-cli"]),

    Claim("C11.10", "RDFS closure lets a shape see a sub-property", "11",
          (F, "SHACL follows `rdfs:subClassOf` when deciding class membership, and **nothing"), "run",
          data=[f"{S}/rdfs/data.ttl", f"{S}/rdfs/shapes.ttl"],
          steps=[Step(f"shacl -d {S}/rdfs/data.ttl -s {S}/rdfs/shapes.ttl"),
                 Step(f"shacl -d {S}/rdfs/data.ttl -s {S}/rdfs/shapes.ttl --inference rdfs")],
          check=checks(_conforms(0, True), _conforms(1, False), has(1, "focus <http://example.org/bob>")),
          checks="without inference the shape never targets bob (conforms); with --inference rdfs it does, and "
                 "bob's missing name is reported",
          needs=["shacl-cli"]),

    Claim("C11.11", "Triple rules are off by default and fire with -a", "11",
          (F, "Rules are **off by default** and enabled with `-a`:"), "run",
          data=[f"{R}/triple.ttl", f"{R}/people.ttl"],
          steps=[Step(f"shacl -d {R}/people.ttl -s {R}/triple.ttl"),
                 Step(f"shacl -d {R}/people.ttl -s {R}/triple.ttl -a")],
          check=checks(_conforms(0, True), _conforms(1, False), has(1, "focus <http://example.org/dave>"),
                       lacks(1, "focus <http://example.org/alice>")),
          checks="without -a nothing is typed ex:Agent, so the Agent shape has no targets; with -a both people "
                 "become Agents, alice gets her contacts from the path rule and dave, who knows nobody, is reported",
          needs=["shacl-cli"]),

    Claim("C11.12", "One result per source instance, at 1,000 and 100,000", "11",
          (F, "inferred `ex:Party` instances against a shape requiring a property none of them"), "run",
          scripts=["scripts/rule_scale.py"],
          steps=[Step("python scripts/rule_scale.py 1000 100000")],
          check=has(0, "N=  1,000  with rules:   1,000 results on   1,000 distinct focus nodes",
                    "N=100,000  with rules: 100,000 results on 100,000 distinct focus nodes",
                    "without rules: 0 results"),
          checks="1,000 results on 1,000 distinct focus nodes, and 100,000 on 100,000; none without rules"),

    Claim("C11.13", "A SPARQL rule computes the area, and validation sees it", "11",
          (F, "Verified at 0.3.2: with `width 3` and `height 4`, a shape asserting"), "run",
          data=[f"{R}/sparql-rule.ttl", f"{R}/box.ttl"],
          steps=[Step(f"shacl -d {R}/box.ttl -s {R}/sparql-rule.ttl -a"),
                 Step(f"shacl -d {R}/box.ttl -s {R}/sparql-rule.ttl")],
          check=checks(_conforms(0, True), exit_code(0, 0), _conforms(1, False)),
          checks="with -a the derived area 12 satisfies sh:hasValue 12; without it, the shape fails",
          needs=["shacl-cli"]),

    Claim("C11.14", "Since 0.3.0 only sh:ShapesGraph declarations apply", "11",
          (F, "`sh:declare`/`sh:prefixes` mechanism. Since 0.3.0, with no `sh:prefixes` on a"), "source",
          sources=[src("engine commit d7769bf", commit("shacl", "d7769bfd0a310e78876976bf8ba7c69ad3fab61b"),
                       "With no sh:prefixes on a query, only declarations on nodes typed sh:ShapesGraph apply.")]),

    Claim("C11.15", "Rule compile errors are held on the rule", "11",
          (F, "> **Fixed before 0.1.8 shipped.**"), "source",
          sources=[src("engine commit 637ebf5", commit("shacl", "637ebf5b0dc9715bc1af4102cb7cd964c92374f2"),
                       "Rule compile errors are held on the rule now and raised only if that rule would have fired")]),

    Claim("C11.16", "Hazard 1: a rule on a shape with no target never fires", "11",
          (F, "Verified: the rule never runs, nothing is inferred, and no message says so."), "run",
          data=[f"{R}/nested.ttl", f"{R}/nested-data.ttl"],
          steps=[Step(f"shacl -d {R}/nested-data.ttl -s {R}/nested.ttl -a")],
          check=checks(_conforms(0, True), exit_code(0, 0), lambda r: ok(r[0].stderr.strip() == "",
                                                                         "and nothing on stderr", "stderr output")),
          checks="conforms true, exit 0, no message: the Tagged check never had a target",
          needs=["shacl-cli"]),

    Claim("C11.17", "Hazard 2: one pass does not close a transitive rule", "11",
          (F, "**One pass, so a transitive rule does not close.**"), "run",
          data=[f"{R}/transitive.ttl", f"{R}/chain.ttl"],
          steps=[Step(f"shacl -d {R}/chain.ttl -s {R}/transitive.ttl -a"),
                 Step(f"shacl -d {R}/chain.ttl -s {R}/transitive.ttl -a --iterate-rules 10")],
          check=checks(_conforms(0, False), has(0, "focus <http://example.org/a>"), _conforms(1, True)),
          checks="one pass: a does not reach d; --iterate-rules 10: it does",
          needs=["shacl-cli"]),

    Claim("C11.18", "Hazard 3: equal sh:order cannot see each other's inferences", "11",
          (F, "**Rules at the same `sh:order` cannot see each other's inferences.**"), "run",
          data=[f"{R}/order.ttl", f"{R}/order-data.ttl"],
          steps=[Step(f"shacl -d {R}/order-data.ttl -s {R}/order.ttl -a"),
                 Step(f"shacl -d {R}/order-data.ttl -s {R}/order.ttl -a --iterate-rules 5")],
          check=checks(_conforms(0, True), _conforms(1, False), has(1, "path <http://example.org/nope>")),
          checks="one pass: Step2 is never reached (conforms); iterated: it is, and its check fails",
          needs=["shacl-cli"]),

    Claim("C11.19", "Hazard 4: a conclusion from absence outlives the absence", "11",
          (F, "**Negation is not monotonic, and iteration exposes it.**"), "run",
          data=[f"{R}/negation.ttl", f"{R}/negation-data.ttl"],
          steps=[Step(f"shacl -d {R}/negation-data.ttl -s {R}/negation.ttl -a"),
                 Step(f"shacl -d {R}/negation-data.ttl -s {R}/negation.ttl")],
          check=checks(_conforms(0, False), has(0, "MaxCountConstraintComponent | focus <http://example.org/a>"),
                       _conforms(1, True)),
          checks="with rules, ex:a ends up both Unnamed and named, and the check reports it; without rules there "
                 "is nothing to report",
          needs=["shacl-cli"],
          notes="Shown with two sh:order levels in one pass, which is the same mechanism iteration exposes: a later "
                "rule supplies what an earlier one tested for, and nothing withdraws the earlier conclusion."),

    Claim("C11.20", "Rules never modify the input graph", "11",
          (F, "> **And one that is not a hazard:** rules never modify the graph you passed in."), "source",
          sources=[src("engine commit 8de05ba", commit("shacl", "8de05bae23e410d97c040743f4ca7e0eb4ff6947"),
                       "Rules return a new graph rather than expanding the caller's.")]),

    Claim("C11.21", "The previous edition's timings, and 0.3.0's own measurement", "11",
          (F, "> These figures were measured for the previous edition, at engine 0.2.0, and have"), "source",
          sources=[src("the previous edition's rules-at-scale table", file("manual", "docs/11-rules-and-inference.md",
                                                                             "333", ref=PREV),
                       "| 100,000 | ~690,000 | 2.7s | **11.9s** |"),
                   src("the previous edition's pySHACL comparison", file("manual", "docs/11-rules-and-inference.md",
                                                                          "346", ref=PREV),
                       "| 1,000 | 0.040s | 2.992s | 75× |"),
                   src("the previous edition's WebAssembly table", file("manual", "docs/11-rules-and-inference.md",
                                                                         "371", ref=PREV),
                       "| 100,000 | 400,000 | **12,611 ms** | **3,119 ms** | 329 MB |"),
                   src("engine README, current timings", file("shacl", "README.md", "68-71"),
                       "| cached index, all cores — the defaults | **0.23s** |"),
                   src("engine commit 6fa00e3 (0.3.0)", commit("shacl", "6fa00e3deb2e02b5b32e6a1a78f7360e33da31e8"))],
          notes="Recorded measurements, not reproduced here. C11.12 reproduces the result counts behind the first "
                "table, at 1,000 and 100,000."),

    Claim("C11.22", "The index holds the graph three times; results sorted by focus node", "11",
          (F, "And the index holds the graph **three times over**"), "source",
          sources=[src("engine README", file("shacl", "README.md", "117-118"),
                       "A graph is held three times over, once per permutation"),
                   src("engine README", file("shacl", "README.md", "101"), "That order is by focus node")]),

    Claim("C11.23", "--build-index caches the parsed graph", "11",
          (F, "(The CLI now offers `--build-index`,"), "run",
          steps=[Step("shacl --help")],
          check=has(0, "--build-index", "Cache the parsed data graph beside it as `<file>.shix`"),
          checks="`shacl --help` documents --build-index", needs=["shacl-cli"]),

    Claim("C11.24", "A SHACL function in a rule is an error, exit 2", "11",
          (F, "| **SHACL functions** (`sh:SPARQLFunction`) | A rule calling one errors (exit 2) rather than returning"),
          "run",
          data=[f"{R}/function.ttl", f"{R}/function-data.ttl"],
          steps=[Step(f"shacl -d {R}/function-data.ttl -s {R}/function.ttl -a")],
          check=checks(exit_code(0, 2), has(0, "unsupported node expression")),
          checks="exit 2, 'unsupported node expression'", needs=["shacl-cli"],
          sources=[src("engine README, what does not work", file("shacl", "README.md", "457-466"),
                       "is vendored under `testsuite/shacl12/tests/rules/` but is not wired into the")]),

    Claim("C11.25", "Rules in WebAssembly, and an unknown mode is an error there too", "11",
          (F, "Every binding runs rules, CLI, Python and WebAssembly alike, through the same"), "run",
          scripts=["scripts/wasm_conforms.mjs"],
          steps=[Step(f"node scripts/wasm_conforms.mjs {S}")],
          check=has(0, "inference=none   conforms=true  results=0", "inference=rules  conforms=false  results=1",
                    'inference=bogus  ERROR: unknown inference "bogus"'),
          checks="through shacl-wasm-node, 'rules' fires and 'none' does not; an unknown mode is an error",
          needs=["node"]),

    Claim("C11.26", "The editor asks for inference 'none', deliberately", "11",
          (F, "`shacl-wasm-node` 0.3.2, so the capability is present, but its runner still asks"), "source",
          sources=[src("extension src/checks/shaclRunner.ts", file("webapp", "src/checks/shaclRunner.ts", "25-31"),
                       "so this deliberately stays at `\"none\"`")]),

    Claim("C11.27", "Named graphs are flattened", "11",
          (F, "Worth repeating because rules make it sharper: quad syntaxes parse, and then every"), "run",
          same_as="C14.07"),

    Claim("C11.28", "Exit codes 0, 1 and 2", "11",
          (F, "Verified across all three at 0.3.2."), "run",
          steps=[Step(f"shacl -d {R}/box.ttl -s {R}/sparql-rule.ttl -a"),
                 Step(f"shacl -d {S}/data.ttl -s {S}/shapes-violation.ttl"),
                 Step(f"shacl -d {R}/function-data.ttl -s {R}/function.ttl -a")],
          check=checks(exit_code(0, 0), exit_code(1, 1), exit_code(2, 2)),
          checks="conforming: 0; not conforming: 1; could not validate: 2", needs=["shacl-cli"]),

    Claim("C11.29", "holos validate exits 0 on a non-conforming graph", "11",
          (F, "> **Do not gate on `holos validate`'s exit code.**"), "run",
          data=[f"{S}/shapes-sparql.ttl"],
          scripts=["scripts/holosdb_validate.py"],
          steps=[Step(f"holos validate --data {S}/data.ttl --shapes {S}/shapes-violation.ttl"),
                 Step(f"holos validate --data {S}/data.ttl --shapes {S}/shapes-violation.ttl --engine adapted"),
                 Step(f"holos validate --data {S}/data.ttl --shapes {S}/shapes-sparql.ttl"),
                 Step(f"holos validate --data {S}/data.ttl --shapes {S}/shapes-sparql.ttl --engine adapted"),
                 Step(f"python scripts/holosdb_validate.py {S}/data.ttl {S}/shapes-violation.ttl {S}/shapes-sparql.ttl")],
          check=checks(has(0, "conforms          false"), exit_code(0, 0), has(1, "conforms          false"),
                       exit_code(1, 0), nonzero(2), has(2, "sh:sparql"), exit_code(3, 0),
                       has(4, "'conforms': False", "HolosError: unsupported: sh:sparql is not implemented")),
          checks="both engines print conforms false and exit 0; the native engine refuses sh:sparql with a "
                 "non-zero exit, the adapted one validates it; holosdb returns a dictionary with conforms False and "
                 "raises HolosError for sh:sparql under native",
          needs=["holos-cli"]),
]
