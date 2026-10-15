"""Chapter 12 — Release and change."""
from ._common import (ACME, SUITE, V1, V2, Claim, Step, all_of, checks, commit, exit_code, file, has, lacks,
                      nonzero, ok, src)

F = "docs/12-release-and-change.md"
FOAF = f"{ACME}/reference_vocab/foaf.rdf"
NS = "https://acme.example.org/ns/"


def _tombstone(mode, conf):
    """Steps and a check for one variant of the migration annotation."""
    steps = [Step(f"python scripts/copy_tree.py {ACME} {{work}}/{mode}"),
             Step(f"python scripts/rewrite_tombstone.py {{work}}/{mode}/acme-org-v2.ttl {mode}"),
             Step(f"{SUITE} consistency --new {{work}}/{mode}/acme-org-v2.ttl --old {V1} --queries {ACME} "
                  f"--import-dir {ACME} --out-dir {{work}}/{mode}-out")]
    return steps, conf


_STEPS, _CHECKS = [], []
for i, (mode, conf) in enumerate((("equivalent-reversed", 100), ("replaced-by", 100),
                                   ("replaced-by-reversed", 57))):
    st, _ = _tombstone(mode, conf)
    _STEPS += st
    _CHECKS.append(has(3 * i + 2, f"employees.rq (confidence {conf}%)"))


CLAIMS = [
    Claim("C12.01", "version-diff: the verdict comes from the axioms", "12",
          (F, "Real output (IRIs shortened to `acme:` here for width):"), "run",
          steps=[Step(f"{SUITE} version-diff {V1} {V2} --exclude-imports --out-dir {{work}}/vd --json"),
                 Step("python scripts/list_files.py {work}/vd"),
                 Step(f"{SUITE} version-diff {V1} {V2} --exclude-imports --out-dir {{work}}/gate --fail-on major")],
          check=checks(has(0, f"Removed classes [MAJOR]:\n  - {NS}Engineer",
                           f"{NS}Engineer no longer rdfs:subClassOf {NS}Employee",
                           f"Added classes [minor]:\n  - {NS}ProductManager\n  - {NS}SoftwareEngineer",
                           f"Added properties [minor]:\n  - {NS}hireDate",
                           f"Added equivalentClass axioms [minor]:\n  - {NS}Engineer equivalentClass {NS}SoftwareEngineer",
                           "Suggested version bump: MAJOR"),
                       has(1, "diff.json", "diff.txt"), nonzero(2)),
          checks="the diff lists exactly the manual's removals and additions and suggests MAJOR; --json writes "
                 "diff.json beside diff.txt; --fail-on major exits non-zero"),

    Claim("C12.02", "Reversed, the diff describes the inverse release", "12",
          (F, "Note the argument order: **old first, then new**."), "run",
          steps=[Step(f"{SUITE} version-diff {V2} {V1} --exclude-imports --out-dir {{work}}/rev")],
          check=has(0, f"Removed classes [MAJOR]:\n  - {NS}ProductManager\n  - {NS}SoftwareEngineer",
                    f"Removed properties [MAJOR]:\n  - {NS}hireDate"),
          checks="v2 → v1 reports ProductManager, SoftwareEngineer and hireDate as removed"),

    Claim("C12.03", "Without FOAF resolved, consistency reports foaf:name and foaf:mbox", "12",
          (F, "**Note also `--exclude-imports` here, where §12.2 uses `--import-dir`.**"), "run",
          steps=[Step(f"{SUITE} consistency --new {V2} --old {V1} --queries {ACME} --exclude-imports "
                      f"--out-dir {{work}}/noimports")],
          check=has(0, "[undeclared_property] http://xmlns.com/foaf/0.1/mbox",
                    "[undeclared_property] http://xmlns.com/foaf/0.1/name"),
          checks="with --exclude-imports, both FOAF properties are reported as undeclared"),

    Claim("C12.04", "consistency: what breaks, and a 100% repair", "12",
          (F, "`consistency` runs the version diff *and* checks every transformation query"), "run",
          steps=[Step(f"{SUITE} consistency --new {V2} --old {V1} --queries {ACME} --import-dir {ACME} "
                      f"--out-dir {{work}}/consistency"),
                 Step("python scripts/list_files.py {work}/consistency")],
          check=checks(has(0, "Suggested version bump: MAJOR",
                           f"1 class(es) used in TARQL but not declared in the ontology set:\n  [undeclared_class] {NS}Engineer",
                           "employees.rq (confidence 100%)",
                           f"Update to the renamed ontology term(s): {NS}Engineer -> {NS}SoftwareEngineer",
                           "Wrote 1/1 suggested repair(s) as .patch files", "Re-run with --apply-repairs"),
                       lacks(0, "undeclared_property"), has(1, "repairs/01-rename_iri-employees.rq.patch")),
          checks="MAJOR; acme:Engineer undeclared in the query; one rename at 100%, written as a .patch; no "
                 "undeclared properties once imports are resolved"),

    Claim("C12.05", "The tombstone is read in both directions; isReplacedBy in one", "12",
          (F, "| `acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer` | **57%**, below a 0.7 apply threshold |"),
          "run",
          scripts=["scripts/rewrite_tombstone.py"],
          steps=_STEPS,
          check=checks(*_CHECKS),
          checks="equivalentClass reversed: 100%; dcterms:isReplacedBy from the old term: 100%; reversed: 57%. "
                 "The fixture's own direction is C12.04 (100%)"),

    Claim("C12.06", "Symmetric since suite 0.3.5, 12 August 2026", "12",
          (F, "**It is not true, and has not been since suite 0.3.5, released on 12 August"), "source",
          sources=[src("suite commit 67513c4, 12 August 2026", commit("suite", "67513c4ebd1cba9d2a67d204b363606bbb942650"),
                       "symmetric-direction rename-migration annotations"),
                   src("suite versioning/rename_detection.py", file("suite", "ontology_suite/versioning/rename_detection.py", "25-30"),
                       "``dcterms:isReplacedBy`` is directional by definition and only recognized old -> new")]),

    Claim("C12.07", "The reversed equivalentClass at 100%", "12",
          (F, "from. Verified again for this edition on the acme fixture, with the triple"), "run", same_as="C12.05"),

    Claim("C12.08", "--apply-repairs changes the one code line on line 14", "12",
          (F, "outside comments only**: re-verified for this edition, the diff of the repaired"), "run",
          steps=[Step(f"python scripts/copy_tree.py {ACME} {{work}}/acme"),
                 Step(f"{SUITE} consistency --new {{work}}/acme/acme-org-v2.ttl --old {{work}}/acme/acme-org-v1.ttl "
                      f"--queries {{work}}/acme --import-dir {{work}}/acme --apply-repairs --min-confidence 0.7 "
                      f"--out-dir {{work}}/out"),
                 Step(f"python scripts/diff_files.py {ACME}/employees.rq {{work}}/acme/employees.rq")],
          check=checks(has(1, "Applied 1/1 suggested repair(s) directly to their target files (confidence >= 70%)."),
                       has(2, "@@ -14 +14 @@", "-  ?employee a acme:Employee, acme:Engineer ;",
                           "+  ?employee a acme:Employee, acme:SoftwareEngineer ;"),
                       lambda r: ok(r[2].stdout.count("@@") == 2, "and that is the only hunk",
                                    f"{r[2].stdout.count('@@') // 2} hunks")),
          checks="the repair applies at 0.7; the diff is one hunk, line 14, the code line; the comment naming "
                 "acme:Engineer is untouched"),

    Claim("C12.09", "Comments used to be rewritten too", "12",
          (F, "The repair was once a textual substitution across the whole file, comments"), "source",
          sources=[src("suite commit 64e300a (first released in v0.14.1)",
                       commit("suite", "64e300a1c42f4822ab17018438c7cda327b938cf"),
                       "`--apply-repairs` rewrote comments as well as code.")]),

    Claim("C12.10", "String literals are still rewritten, deliberately", "12",
          (F, "The judgement underneath is worth borrowing. String **literals** are still"), "run",
          data=["data/rename-literal/employees.rq"],
          steps=[Step("python scripts/copy_tree.py data/rename-literal {work}/q"),
                 Step(f"{SUITE} consistency --new {V2} --old {V1} --queries {{work}}/q --import-dir {ACME} "
                      f"--apply-repairs --min-confidence 0.7 --out-dir {{work}}/out"),
                 Step("python scripts/diff_files.py data/rename-literal/employees.rq {work}/q/employees.rq")],
          check=checks(has(2, '+  BIND("acme:SoftwareEngineer" AS ?role)',
                           "+  ?employee a acme:Employee, acme:SoftwareEngineer ;"),
                       lacks(2, "+# Every row")),
          checks="the code line and the string literal are both rewritten; the comment is not",
          sources=[src("suite commit 64e300a", commit("suite", "64e300a1c42f4822ab17018438c7cda327b938cf"),
                       "String literals are deliberately still rewritten: a TARQL IRI template is built out of literals")]),

    Claim("C12.11", "The same defect in the editor", "12",
          (F, "**The same defect existed in the editor, and neither side knew.**"), "source", same_as="C08.10"),

    Claim("C12.12", "pattern-consistency catches MKT only from the output data", "12",
          (F, "**Caught**, from tarka's output just as from `oxi-gen`'s."), "run",
          steps=[Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"),
                 Step(f"{SUITE} pattern-consistency --queries {ACME} --ontology {V1} --ontology {FOAF} "
                      f"--taxonomy {ACME}/taxonomy.ttl --output-data {{work}}/employees.ttl --out-dir {{work}}/with"),
                 Step(f"{SUITE} pattern-consistency --queries {ACME} --ontology {V1} --ontology {FOAF} "
                      f"--taxonomy {ACME}/taxonomy.ttl --out-dir {{work}}/without"),
                 Step(f"{SUITE} pattern-consistency --queries {ACME} --ontology {V1} "
                      f"--taxonomy {ACME}/taxonomy.ttl --output-data {{work}}/employees.ttl --out-dir {{work}}/nofoaf"),
                 Step(f"python scripts/query_file.py {ACME}/taxonomy.ttl \"PREFIX skos: <http://www.w3.org/2004/02/skos/core#> "
                      f"SELECT ?c WHERE {{ ?c a skos:Concept }} ORDER BY ?c\"")],
          check=checks(has(1, "[undeclared_taxonomy_reference] https://acme.example.org/data/department/MKT"),
                       exit_code(1, 0),
                       has(2, "No modelling-pattern inconsistencies found"),
                       has(3, "[undeclared_property] http://xmlns.com/foaf/0.1/mbox",
                           "[undeclared_property] http://xmlns.com/foaf/0.1/name"),
                       has(4, "department/ENG", "department/QA", "department/SALES"), lacks(4, "MKT")),
          checks="with --output-data, MKT is reported (and the run exits 0); without it, the run is clean; "
                 "without foaf.rdf, foaf:name and foaf:mbox are undeclared; the taxonomy holds ENG, QA and SALES",
          needs=["tarka-cli"]),

    Claim("C12.13", "Omit --output-data and it reports clean", "12",
          (F, "Omit `--output-data` and this run reports clean: correctly, and uselessly."), "run", same_as="C12.12"),

    Claim("C12.14", "Both consistency commands are report-only by default", "12",
          (F, "Look at the flags before you copy the commands into a pipeline."), "run",
          steps=[Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"),
                 Step(f"{SUITE} pattern-consistency --queries {ACME} --ontology {V1} --ontology {FOAF} "
                      f"--taxonomy {ACME}/taxonomy.ttl --output-data {{work}}/employees.ttl --out-dir {{work}}/a"),
                 Step(f"{SUITE} pattern-consistency --queries {ACME} --ontology {V1} --ontology {FOAF} "
                      f"--taxonomy {ACME}/taxonomy.ttl --output-data {{work}}/employees.ttl --out-dir {{work}}/b "
                      f"--fail-on-anything"),
                 Step(f"{SUITE} consistency --new {V2} --old {V1} --queries {ACME} --import-dir {ACME} --out-dir {{work}}/c"),
                 Step(f"{SUITE} consistency --new {V2} --old {V1} --queries {ACME} --import-dir {ACME} --out-dir {{work}}/d "
                      f"--fail-on-anything")],
          check=checks(exit_code(1, 0), exit_code(2, 1), exit_code(3, 0), exit_code(4, 1)),
          checks="each command exits 0 on its findings, and 1 with --fail-on-anything (which from 0.24.0 is the "
                 "one name on both; --fail-on-anything and --fail-on-anything remain as aliases)",
          needs=["tarka-cli"]),

    Claim("C12.15", "The approval workflow is not implemented here", "12",
          (F, "**The approval workflow is not implemented here, and no tool should claim"), "argument",
          notes="A statement about scope. The evidence the table lists is reproduced in C09.04, C12.01, C12.04, "
                "C12.08 and C12.12."),

    Claim("C12.16", "UPDATING.md as a governance playbook", "12",
          (F, "suite's own `UPDATING.md` is the closest existing document to a governance"), "source",
          sources=[src("suite docs/UPDATING.md", file("suite", "docs/UPDATING.md", "1"),
                       "Updating the semantic specification ecosystem: a playbook")]),
]
