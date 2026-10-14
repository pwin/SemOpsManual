"""Chapter 8 — Model and validate."""
import re

from ._common import (ACME, OWN, SUITE, TSC, TSX, V1, Claim, Step, all_of, by_check, checks, commit, counts,
                      exit_code, file, has, lacks, nonzero, ok, rows, src, totals)

F = "docs/08-model-and-validate.md"
CUSTOM = f"--registry {ACME}/custom_checks/registry.json --sparql {ACME}/custom_checks/sparql"
TRIPLIFY = f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"


def _log001_message(csv_rel):
    def check(r):
        row = next((x for x in rows(r.file(csv_rel)) if x["check_id"] == "LOG-001"), None)
        if row is None:
            return False, "no LOG-001 row"
        want_msg = ("is asserted disjoint with its own (transitive) superclass https://acme.example.org/ns/Employee, "
                    "which makes https://acme.example.org/ns/Contractor logically unsatisfiable")
        want_rem = "Remove either the subclass axiom or the disjointness axiom; the two together are contradictory."
        return all_of(ok(want_msg in row["message"], "LOG-001's message reads as quoted",
                         f"LOG-001 message: {row['message']!r}"),
                      ok(row["remediation"].strip() == want_rem, "and its remediation too",
                         f"LOG-001 remediation: {row['remediation']!r}"))
    return check


def _findings_txt(rel, *texts):
    def check(r):
        body = r.file(rel).read_text(encoding="utf-8")
        missing = [t for t in texts if t not in body]
        return ok(not missing, f"{rel} contains {', '.join(repr(t) for t in texts)}", f"{rel} lacks {missing}")
    return check


def _unmapped(csv_rel, n):
    def check(r):
        rs = rows(r.file(csv_rel))
        unm = [x for x in rs if x["check_id"] == "UNMAPPED"]
        return all_of(
            ok(len(unm) == len(rs) == n, f"all {n} findings have check id UNMAPPED",
               f"{len(unm)} of {len(rs)} UNMAPPED, expected all {n}"),
            ok(all(x["severity"] for x in unm), "each keeps its severity", "some lost their severity"),
            ok(sum(1 for x in unm if x["message"].strip()) >= n - 2, "nearly all keep their message",
               "messages lost"),
            ok(not any(x["title"] or x["remediation"] for x in unm), "none has a title or a remediation",
               "some have a title or remediation"))
    return check


def _acm001_fault_and_control(csv_rel):
    def check(r):
        rs = rows(r.file(csv_rel))
        acm = [x for x in rs if x["check_id"] == "ACM-001"]
        foci = [x["focus_node"] for x in acm]
        return all_of(
            ok(foci == ["https://acme.example.org/data/employee/E101"],
               "ACM-001 fires on E101 (no ID) and not on E100 (the control)", f"ACM-001 foci: {foci}"),
            ok(bool(acm) and acm[0]["title"] == "Employee missing an employee ID" and
               acm[0]["remediation"].startswith('Add acme:hasEmployeeId "ACM-NNNN"'),
               "with its title and remediation from the merged registry", "title/remediation missing"),
            ok(not any(x["check_id"] == "UNMAPPED" for x in rs), "and no finding is UNMAPPED",
               "UNMAPPED findings present"))
    return check


def _site_path_advice(r):
    hit = re.search(r"Pass --sparql (\S+) as well to run both", r[1].stderr)
    path = hit.group(1).replace(chr(92), "/") if hit else ""
    return ok(path.endswith("site-packages/ontology_suite/resources/sparql"),
              f"the warning recommends the installed tree by path ({path})", "no site-path recommendation")


CLAIMS = [
    Claim("C08.01", "Outline prompts resolve restriction names since 0.14.0", "08",
          (F, "Since 0.14.0 a restriction typed into those prompts resolves its names"), "source",
          sources=[src("extension CHANGELOG, 0.14.0", file("webapp", "CHANGELOG.md", "90-99"),
                       "search it for the regular expression `<[^:>]+>`"),
                   src("extension commit d480ace (first released in v0.14.0)",
                       commit("webapp", "d480ace5adc99616ca36ca563af8feb3cb2fb99d"))]),

    Claim("C08.02", "Run Local Checks reads 44 SPARQL and 6 SHACL files from the 61-check registry", "08",
          (F, "*Run Local Checks* evaluates the 44 SPARQL and 6 SHACL check files"), "run", same_as="C07.03",
          notes="The editor and the CLI read the same registry; C07.03 counts it in the installed suite package."),

    Claim("C08.03", "Three modelling-guidance checks only the editor has", "08",
          (F, "It also runs **three checks the CLI does not have**"), "source",
          sources=[src("extension src/checks/modellingGuidance.test.ts", file("webapp", "src/checks/modellingGuidance.test.ts", "20-24"),
                       "MDL-002: ex:Veterinarian owl:equivalentClass ex:AnimalDoctor")]),

    Claim("C08.04", "VOC-001 is declared in the registry but only the extension runs it", "08",
          (F, "It is in the registry; the CLI still cannot produce it."), "source",
          sources=[src("suite tests/test_check_coverage.py, EXTENSION_ONLY_IDS",
                       file("suite", "tests/test_check_coverage.py", "94-97"),
                       "checks/vocabularyChecks.ts -- a closed-world scan of the axiom positions"),
                   src("extension src/checks/registryCoverage.test.ts", file("webapp", "src/checks/registryCoverage.test.ts", "25-27"),
                       "the three checks only *this* extension can produce, VOC-001/REA-005/REA-006")],
          notes="C08.06 shows the consequence: the CLI reports the typo as STR-001, never as VOC-001."),

    Claim("C08.05", "Eleven checks the editor cannot produce, two held back explicitly", "08",
          (F, "**Eleven go the other way.**"), "source",
          sources=[src("extension registryCoverage.test.ts, CLI_ONLY", file("webapp", "src/checks/registryCoverage.test.ts", "33-61"),
                       "'TQL-004', 'TQL-005',"),
                   src("the same test: a query it cannot run is not counted",
                       file("webapp", "src/checks/registryCoverage.test.ts", "99-107"),
                       "make the CLI_ONLY list above assert something false while still passing")],
          notes="CLI_ONLY lists REA-020, REA-021, REA-022, REA-010, REA-011, REA-012, CNF-001, CNF-002, CNF-005, "
                "TQL-004 and TQL-005: eleven."),

    Claim("C08.06", "The CLI catches the typo as STR-001, not VOC-001", "08",
          (F, "Run against that file, the CLI reports `STR-001`; `VOC-001` is not among its findings."), "run",
          data=["data/typo/typo-data.ttl"],
          steps=[Step(f"{SUITE} checks --data data/typo/typo-data.ttl --engine sparql --out-dir {{work}}/typo "
                      f"--fail-on never --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/typo/full_results.csv --by focus --check STR-001")],
          check=checks(counts("typo/full_results.csv", {"STR-001": 1}, exact=False),
                       has(1, "value=https://acme.example.org/ns/Empolyee"),
                       lambda r: ok("VOC-001" not in by_check(r.file("typo/full_results.csv")),
                                    "no VOC-001 finding", "VOC-001 present")),
          checks="STR-001 fires once, on acme:Empolyee; VOC-001 does not appear"),

    Claim("C08.07", "Sixteen checks offer a Quick Fix", "08",
          (F, "Sixteen checks offer a one-click lightbulb repair"), "source",
          sources=[src("extension resources/checks-registry/repairs/manifest.json",
                       file("webapp", "resources/checks-registry/repairs/manifest.json"), "PRJ-REQUIRED")],
          notes="The manifest's `checks` object has 16 keys: LOG-003, MDL-001, MDL-002, MDL-003, PRJ-REQUIRED, "
                "QUA-001, QUA-002, QUA-004, QUA-005, QUA-007, STR-001, STR-002, STR-005, STR-007, STR-008, STY-003."),

    Claim("C08.08", "Blank nodes cross the repair boundary as skolem IRIs", "08",
          (F, "**It nearly renamed every blank node in the file.**"), "source",
          sources=[src("extension CHANGELOG, 0.13.11", file("webapp", "CHANGELOG.md", "220-230"),
                       "Blank nodes now cross the boundary as IRIs and come back as blank nodes"),
                   src("extension commit e4583b9", commit("webapp", "e4583b9a9d47f678bba2e5efaba7b7d0b21ca504"))]),

    Claim("C08.09", "A literal's base direction survives a repair since 0.13.12", "08",
          (F, "**It dropped a literal's base direction.**"), "source",
          sources=[src("extension CHANGELOG, 0.13.12", file("webapp", "CHANGELOG.md", "179-184"),
                       "datatype from `rdf:dirLangString` to `rdf:langString` in the user's own file"),
                   src("extension commit e3364fc (first released in v0.13.12)",
                       commit("webapp", "e3364fc5bf6b7a7c5028d5e868b5b3c12164ae2c"))]),

    Claim("C08.10", "Refactoring masks comments since 0.13.5", "08",
          (F, "All three depend on one decision, *which text counts as code*"), "source",
          sources=[src("extension commit 71981b4 (first released in v0.13.5)",
                       commit("webapp", "71981b41283528abbd6fa509a2ffa8c3bd231270"),
                       "Stop reading CURIEs out of comments"),
                   src("extension CHANGELOG, 0.13.5", file("webapp", "CHANGELOG.md", "351"), "a line whose *first* non-space character was `#`")]),

    Claim("C08.11", "The unresolved-import warning names where it looked", "08",
          (F, "It now names the directory it searched and how"), "source",
          sources=[src("extension CHANGELOG, 0.13.5", file("webapp", "CHANGELOG.md", "401"),
                       "It now names the directory it searched and how many ontology files it found")]),

    Claim("C08.12", "The DSL script type-checks and builds against the npm package", "08",
          (F, "Verified against the published 0.15.0 package."), "run",
          scripts=["scripts/dsl/acme.ontology.ts"],
          steps=[Step("node -p \"require('./node_modules/ontology-suite/package.json').version\""),
                 Step(f"{TSC} scripts/dsl/acme.ontology.ts"),
                 Step(f"{TSX} scripts/dsl/acme.ontology.ts {{work}}/acme.ttl"),
                 Step('python scripts/query_file.py {work}/acme.ttl "SELECT (COUNT(*) AS ?triples) WHERE { ?s ?p ?o }"')],
          check=checks(has(0, "0.15.0"), exit_code(1, 0), exit_code(2, 0), exit_code(3, 0)),
          checks="the installed package is 0.15.0; tsc reports no errors; the script runs and writes Turtle",
          needs=["node"],
          notes="The script is the manual's listing plus four lines that write the Turtle to a file, and one "
                "`as any` explained in C08.16."),

    Claim("C08.13", "tsc refuses a bare string as a datatype range (TS2322)", "08",
          (F, "**The type checker catches a mistake of kind.**"), "run",
          scripts=["scripts/dsl/bad-range.ontology.ts"],
          steps=[Step(f"{TSC} scripts/dsl/bad-range.ontology.ts")],
          check=checks(nonzero(0), has(0, "error TS2322: Type 'string' is not assignable to type 'DatatypeRef'.")),
          checks="tsc exits non-zero with TS2322, 'string' not assignable to 'DatatypeRef'",
          needs=["node"],
          notes="The manual quotes the error at line 16 of its first draft; this file is shorter, so the line "
                "and column differ."),

    Claim("C08.14", "The gate catches the contradiction in the script's output", "08",
          (F, "**The gate catches a mistake of logic.**"), "run",
          steps=[Step(f"{TSX} scripts/dsl/acme.ontology.ts {{work}}/acme.ttl"),
                 Step(f"{SUITE} ontology --ontology {{work}}/acme.ttl --out-dir {{work}}/gate --fail-on Violation "
                      f"--reports minimal", env={"PYTHONHASHSEED": "0"})],
          check=checks(exit_code(1, 1), counts("gate/full_results.csv", {"LOG-001": 1}, exact=False),
                       _findings_txt("gate/findings.txt", "LOG-001   Violation Class https://acme.example.org/ns/Contractor")),
          checks="the ontology stage exits 1, with LOG-001 on acme:Contractor in findings.txt",
          needs=["node"]),

    Claim("C08.15", "Without the type check, the DSL fails with an internal TypeError", "08",
          (F, "**Code the checker did not see gets a blunter error.**"), "run",
          steps=[Step(f"{TSX} scripts/dsl/bad-range.ontology.ts")],
          check=checks(nonzero(0), has(0, "TypeError: Cannot convert undefined or null to object")),
          checks="tsx exits non-zero with 'TypeError: Cannot convert undefined or null to object'",
          needs=["node"]),

    Claim("C08.16", "build().quads is not assignable to n3's Writer under strict types", "08",
          (F, "**One type-level rough edge.**"), "run",
          scripts=["scripts/dsl/writer-types.ts"],
          steps=[Step(f"{TSC} scripts/dsl/writer-types.ts")],
          check=checks(nonzero(0), has(0, "error TS2345"), has(0, "termType")),
          checks="tsc exits non-zero with TS2345, naming the missing termType",
          needs=["node"]),

    Claim("C08.17", "ontology reports 2 findings, and findings.txt quotes the line", "08",
          (F, "That first report is new since the last edition"), "run",
          claim="When HermiT does not run, `ontology` reports LOG-001 and REA-022. findings.txt quotes line 47 and "
                "puts REA-022 under 'not located'.",
          scripts=["scripts/without_java.py"],
          steps=[Step(f"python scripts/without_java.py {SUITE} ontology --ontology {V1} --import-dir {ACME} "
                      f"--out-dir {{work}}/ontology", env={"PYTHONHASHSEED": "0"})],
          check=checks(totals(0, 2, 1, 0, 1),
                       has(0, "findings.txt (start here -- what, where, and the source line)"),
                       _findings_txt("ontology/findings.txt", "2 finding(s): 1 Violation, 1 Info",
                                     "> 47 | acme:Contractor a owl:Class ;", "48 |     rdfs:subClassOf acme:Employee ;",
                                     "-- not located: 1 finding(s)",
                                     "REA-022  Info  External DL reasoner unavailable"),
                       _log001_message("ontology/full_results.csv")),
          checks="2 findings (1 V, 1 I); findings.txt quotes lines 47–49 and lists REA-022 as not located; "
                 "LOG-001's message and remediation read as the manual quotes them",
          notes="Java is hidden here so that the reasoner's failure is certain. With Java visible, whether HermiT "
                "runs depends on the hash seed: seed 0 gives this output nine runs in ten (C14.06, C14.08)."),

    Claim("C08.18", "LOG-001's message is a model of what a message should be", "08",
          (F, "No description-logic background is needed to act on that."), "run", same_as="C08.17"),

    Claim("C08.19", "With HermiT running, three findings", "08",
          (F, "**You may see 3 findings here, not 2.**"), "run",
          steps=[Step(f"{SUITE} ontology --ontology {V1} --import-dir {ACME} --out-dir {{work}}/seed5 "
                      f"--reports minimal", env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/seed5/full_results.csv")],
          check=checks(totals(0, 3, 3, 0, 0),
                       counts("seed5/full_results.csv", {"LOG-001": 1, "REA-020": 1, "REA-021": 1})),
          checks="3 findings, all Violations: LOG-001, REA-020 and REA-021, and no REA-022",
          notes="C14.06 shows seeds 0–4 give two findings and 5 gives three, and why."),

    Claim("C08.20", "--profile is off by default and repeatable", "08",
          (F, "**Want a specific OWL2 profile checked?**"), "run",
          steps=[Step(f"{SUITE} ontology --help")],
          check=has(0, "--profile"), checks="`ontology --help` lists --profile"),

    Claim("C08.21", "checks reports 479 findings against the fixture", "08",
          (F, "this reports **479 findings** (55 Violations, 340 Warnings, 84 Infos),"), "run", same_as="C09.02"),

    Claim("C08.22", "A project tree alone now warns that 42 built-in checks did not run", "08",
          (F, "Point the CLI at that directory on its own and listen to what it says:"), "run",
          steps=[Step(TRIPLIFY),
                 Step(f"{SUITE} checks --ontology {V1} --data {{work}}/employees.ttl {CUSTOM} --engine sparql "
                      f"--out-dir {{work}}/acm001 --reports minimal")],
          check=checks(totals(1, 0, 0, 0, 0),
                       has(1, "WARNING: --sparql replaced the suite's own query tree: 1 project check(s) ran "
                              "and 42 built-in check(s) did not."),
                       _site_path_advice, lacks(1, "@builtin")),
          checks="0 findings, and the warning names 1 project check and 42 built-in ones; it recommends the "
                 "built-in tree by its site path, and does not mention @builtin",
          needs=["tarka-cli"]),

    Claim("C08.23", "Until 0.18.0 that run was silent; the testing repo's gate was in that state", "08",
          (F, "Until 0.18.0 that run was silent."), "source",
          sources=[src("suite commit cae9ef2 (first released in v0.18.0)",
                       commit("suite", "cae9ef21cf33ceb8eba33ef94da66b32bf810ded"),
                       "the separate testing repo's CI gate config named eight CMP-* queries, its merged registry "
                       "declared 61 checks, and the gate reported a clean run")]),

    Claim("C08.24", "With @builtin and a one-entry registry, every built-in finding is UNMAPPED", "08",
          (F, "**But the registry still replaces rather than composes.**"), "run",
          steps=[Step(TRIPLIFY),
                 Step(f"{SUITE} checks --ontology {V1} --data {{work}}/employees.ttl {CUSTOM} --sparql @builtin "
                      f"--engine sparql --out-dir {{work}}/out --reports minimal --fail-on never")],
          check=checks(totals(1, 491), _unmapped("out/full_results.csv", 491)),
          checks="491 findings, every one with check id UNMAPPED; each keeps its severity and (all but two) "
                 "its message; none has a title or remediation",
          needs=["tarka-cli"]),

    Claim("C08.25", "A merged registry names every finding, and ACM-001 fires on its fault only", "08",
          (F, "(the built-in entries plus your own) as a generated file, pass that to"), "run",
          data=["data/house-rule/missing-id.ttl"],
          scripts=["scripts/merge_registry.py"],
          steps=[Step(f"python scripts/merge_registry.py {ACME}/custom_checks/registry.json {{work}}/merged-registry.json"),
                 Step(f"{SUITE} checks --ontology {V1} --data data/house-rule/missing-id.ttl "
                      f"--registry {{work}}/merged-registry.json --sparql {ACME}/custom_checks/sparql --sparql @builtin "
                      f"--engine sparql --out-dir {{work}}/out --reports minimal --fail-on never"),
                 Step("python scripts/summarise_findings.py {work}/out/full_results.csv --by focus --check ACM-001")],
          check=checks(has(0, "61 built-in + 1 project = 62 entries"), _acm001_fault_and_control("out/full_results.csv")),
          checks="the merged registry has 62 entries; ACM-001 fires on E101 and not on its control E100, with its "
                 "own title and remediation; nothing is UNMAPPED"),

    Claim("C08.26", "The warning recommends the site path @builtin was made to avoid", "08",
          (F, "warning above recommends passing the built-in tree *by its absolute site"), "run", same_as="C08.22"),

    Claim("C08.27", "Checks are discovered by walking the directory", "08",
          (F, "**Checks are discovered by walking the directory**"), "source",
          sources=[src("suite commit cae9ef2", commit("suite", "cae9ef21cf33ceb8eba33ef94da66b32bf810ded"),
                       "Discovery is filesystem-based and consults the registry only afterwards, so a query with no "
                       "entry still runs and reports UNMAPPED, and an entry with no file never fires at all.")],
          notes="C08.24 shows the first half: queries with no registry entry still ran, and reported UNMAPPED."),

    Claim("C08.28", "Every full run writes cucumber.json", "08",
          (F, "**Fill in the cucumber fields.**"), "run", same_as="C09.10"),

    Claim("C08.29", "Guard a label with isBlank; COALESCE is the weaker fix", "08",
          (F, "**Never build a message out of a label.**"), "run", same_as="C07.07"),

    Claim("C08.30", "CT-39 asserts that a finding names something findable", "08",
          (F, "board row, CT-39, whose whole assertion is that a finding names something a"), "source",
          sources=[src("testing repo CT-39 README",
                       file("testing", "experiments/SpecificTests/CT-39-finding-names-something-findable/README.md", "1"),
                       "CT-39 — A finding names something a reader can find")]),

    Claim("C08.31", "sh:severity on a node shape does not reach its property shapes", "08",
          (F, "**Put `sh:severity` on the shape that produces the result.**"), "run", same_as="C07.12"),

    Claim("C08.32", "Four checks shipped that matched nothing", "08",
          (F, "The suite has shipped four checks"), "source",
          sources=[src("suite commit 2f4950c", commit("suite", "2f4950c4436868fb6ea203c0ce271727b256cfef"),
                       "matched nothing (REA-001's symmetry assumption, DAT-001's UNION of FILTER-only branches, "
                       "EFF-002's unjoined $this, and DAT-001's boolean branch above)")]),

    Claim("C08.33", "How the editor behaviour was established", "08",
          (F, "**How the editor behaviour in this chapter was established.**"), "argument",
          notes="A statement of method. The extension's tests were run on a Windows checkout of "
                f"[704d4ef]({commit('webapp', '704d4ef80fdbcbf614782fa9bf42dfa79962b18f')}) (the 0.15.0 release); "
                "the DSL claims (C08.12–C08.16) are reproduced here from the npm package."),
]
