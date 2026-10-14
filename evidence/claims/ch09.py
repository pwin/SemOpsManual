"""Chapter 9 — Continuous integration."""
import re

from ._common import (ACME, OWN, OWN_DATA, SUITE, V1, Claim, Step, all_of, by_check, checks, commit, counts,
                      exit_code, file, has, lacks, nonzero, ok, rows, src, totals)

F = "docs/09-continuous-integration.md"
CHECKS = f"{SUITE} checks --ontology {V1} --import-dir {ACME} --engine sparql"


def _all_focus_own(csv_rel):
    def check(r):
        bad = [x["focus_node"] for x in rows(r.file(csv_rel)) if not x["focus_node"].startswith(OWN)]
        return ok(not bad, f"every focus node starts with {OWN}", f"focus nodes outside {OWN}: {bad[:3]}")
    return check


def _blank_label_namespaces(r):
    hit = re.findall(r"Namespaces actually seen: (.*)", r[0].stderr)
    labels = re.findall(r"N[0-9a-f]{32}/", hit[0]) if hit else []
    return ok(bool(labels), f"the 'namespaces actually seen' list includes blank-node labels, e.g. {labels[:1]}",
              "no blank-node-shaped entries in the namespace list")


def _warning_on_stderr(r):
    return ok("matched none of the 479 findings" in r[0].stderr and "matched none" not in r[0].stdout,
              "the warning is on stderr, not stdout", "warning not where expected")


def _rea022(csv_rel, present):
    def check(r):
        ids = by_check(r.file(csv_rel))
        cond = ("REA-022" in ids) == present
        return ok(cond, f"{csv_rel}: REA-022 {'present' if present else 'absent'}",
                  f"{csv_rel}: REA-022 {'missing' if present else 'present'}")
    return check


def _rea022_focus(csv_rel):
    def check(r):
        foci = {x["focus_node"] for x in rows(r.file(csv_rel)) if x["check_id"] == "REA-022"}
        return ok(foci == {"oq:Graph"}, "REA-022's focus node is oq:Graph", f"REA-022 focus nodes: {foci}")
    return check


def _report_files(r):
    default = r[2].stdout
    names = ["findings.txt", "full_results.csv", "cucumber.json", "report.html"]
    missing = [n for n in names if n not in default]
    stale = [f"{n}.{x}" for n in ("summary_by_check", "summary_by_category", "top_offenders")
             for x in ("csv", "md") if f"{n}.{x}" in default]
    minimal_files = re.findall(r"^\s*[\d,]+\s+(\S+)$", r[3].stdout, re.M)
    header = open(r.file("minimal/full_results.csv"), encoding="utf-8").readline()
    return all_of(
        ok(not missing, "default run writes findings.txt, full_results.csv, cucumber.json, report.html",
           f"default run lacks {missing}"),
        ok("features/" in default and "plots/" in default, "and features/ and plots/", "no features/ or plots/"),
        ok(not stale, "and none of the six retired summary files", f"retired files present: {stale}"),
        ok(sorted(minimal_files) == ["findings.txt", "full_results.csv"],
           "--reports minimal writes exactly findings.txt and full_results.csv", f"minimal wrote {minimal_files}"),
        ok("source_file" in header and "line" in header, "full_results.csv has source_file and line columns",
           f"header: {header.strip()}"),
    )


CLAIMS = [
    Claim("C09.01", "--fail-on Violation exits non-zero on the fixture", "09",
          (F, "`--fail-on` takes `Violation`, `Warning`, `Info` or `never`."), "run",
          claim="The gate is one flag and an exit code: the fixture's deliberate contradiction is a Violation, "
                "so the ontology stage exits non-zero.",
          steps=[Step(f"{SUITE} ontology --ontology {V1} --import-dir {ACME} --out-dir {{work}}/gate "
                      f"--reports minimal --fail-on Violation", env={"PYTHONHASHSEED": "0"})],
          check=checks(nonzero(0), has(0, "1 Violation")),
          checks="the command exits non-zero, and reports one Violation"),

    Claim("C09.02", "The unscoped run reports 479 findings, every time", "09",
          (F, "479 every time, and 479 on a new engine."), "run",
          claim="The full registry, with org: and FOAF resolved, reports 479 findings (55 V, 340 W, 84 I), "
                "the same on repeated runs.",
          steps=[Step(f"{CHECKS} --out-dir {{work}}/run{i} --fail-on never --reports minimal") for i in (1, 2, 3)],
          check=checks(totals(0, 479, 55, 340, 84), totals(1, 479, 55, 340, 84), totals(2, 479, 55, 340, 84)),
          checks="each of three identical runs prints 479 total, 55 Violation, 340 Warning, 84 Info"),

    Claim("C09.03", "--exclude-imports gives 27 findings, four of them false", "09",
          (F, "479 findings become **27**."), "run",
          claim="Not resolving the imports cuts 479 to 27, but four of the 27 are artefacts: FOAF terms that "
                "look dangling or unlabelled only because FOAF was not loaded.",
          steps=[Step(f"{SUITE} checks --ontology {V1} --exclude-imports --engine sparql "
                      f"--out-dir {{work}}/excl --fail-on never --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/excl/full_results.csv"),
                 Step("python scripts/summarise_findings.py {work}/excl/full_results.csv --by focus --check DAT-002"),
                 Step("python scripts/summarise_findings.py {work}/excl/full_results.csv --by focus --check QUA-004")],
          check=checks(totals(0, 27, 1, 26, 0),
                       counts("excl/full_results.csv", {"DAT-002": 2, "LOG-001": 1, "QUA-001": 1, "QUA-004": 3,
                                                        "QUA-009": 9, "QUA-010": 9, "STR-003": 1, "STY-002": 1}),
                       has(2, "value=http://xmlns.com/foaf/0.1/", "value=http://xmlns.com/foaf/0.1/Person"),
                       has(3, "focus=http://xmlns.com/foaf/0.1/Person")),
          checks="27 findings with exactly the breakdown in the manual; both DAT-002 findings point at FOAF; "
                 "two of the three QUA-004 are about FOAF terms"),

    Claim("C09.04", "--own-namespace gives 23 findings, all Acme's", "09",
          (F, "**Twenty-three findings. All twenty-three are Acme's. None are artefacts.**"), "run",
          claim="Keep the imports, filter the report by focus node: 23 findings, every one in Acme's namespace, "
                "18 of them the documentation pair QUA-009/QUA-010.",
          steps=[Step(f"{CHECKS} --own-namespace {OWN} --out-dir {{work}}/own --fail-on never --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/own/full_results.csv")],
          check=checks(totals(0, 23, 1, 22, 0),
                       counts("own/full_results.csv", {"LOG-001": 1, "QUA-001": 1, "QUA-004": 1, "QUA-009": 9,
                                                       "QUA-010": 9, "STR-003": 1, "STY-002": 1}),
                       _all_focus_own("own/full_results.csv")),
          checks="23 findings (1 V, 22 W), the per-check breakdown in the manual, and every focus node in "
                 "https://acme.example.org/ns/"),

    Claim("C09.05", "The three runs compared: 479, 27, 23", "09",
          (F, "| `--own-namespace` | **23** | 23 | 0 | 0 |"), "run", same_as="C09.04",
          notes="The table's three rows are C09.02 (479), C09.03 (27, four false) and C09.04 (23)."),

    Claim("C09.06", "--themes groups findings under questions in your words", "09",
          (F, "`--themes` takes a small file mapping check ids to"), "run",
          steps=[Step(f"{CHECKS} --own-namespace {OWN} --themes data/themes/acme-themes.json "
                      f"--out-dir {{work}}/themes --fail-on never --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/themes/full_results.csv")],
          data=["data/themes/acme-themes.json"],
          check=lambda r: all_of(*[ok(t in open(r.file("themes/findings.txt"), encoding="utf-8").read(),
                                      f"findings.txt has '{t}'", f"findings.txt lacks '{t}'")
                                   for t in ("-- by question", "Can a domain expert read what each term means?  (20)",
                                             "QUA-001 x1, QUA-004 x1, QUA-009 x9, QUA-010 x9",
                                             "Is the model logically coherent?  (1)",
                                             "not mapped to a question  (1)")]),
          checks="findings.txt opens with a 'by question' index: 20 under the documentation question, 1 under "
                 "coherence, and STR-003 listed as not mapped rather than dropped"),

    Claim("C09.07", "A near-miss namespace warns, on stderr, and lists blank-node labels", "09",
          (F, "**The tool now says so.** Reported from that experience"), "run",
          steps=[Step(f"{CHECKS} --own-namespace http://example.org/acme# --out-dir {{work}}/miss "
                      f"--fail-on never --reports minimal")],
          check=checks(totals(0, 0, 0, 0, 0), _warning_on_stderr, _blank_label_namespaces),
          checks="0 findings; the warning 'matched none of the 479 findings' is on stderr and not stdout; and "
                 "the 'Namespaces actually seen' list contains blank-node identifiers with a slash appended"),

    Claim("C09.08", "The warning fires only when there were findings to lose", "09",
          (F, "The warning fires only when there were findings to lose."), "source",
          sources=[src("suite cli.py, _filter_own_namespace", file("suite", "ontology_suite/cli.py", "158-200"),
                       "kept = [r for r in rows if r.focus_node.startswith(own_namespace)]")],
          notes="The warning is emitted only when the filter removes everything from a non-empty set of rows; "
                "an empty run never reaches it."),

    Claim("C09.09", "A scoped run drops the 'reasoner did not run' finding", "09",
          (F, "it means a scoped gate cannot tell"), "run",
          claim="REA-022's focus node is oq:Graph, so --own-namespace removes it. With HermiT unable to run (Java "
                "hidden, so that the outcome is certain), the unscoped data run reports REA-022 and the scoped one "
                "says nothing about it.",
          scripts=["scripts/without_java.py"],
          steps=[Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"),
                 Step(f"python scripts/without_java.py {SUITE} data {{work}}/employees.ttl --ontology {V1} "
                      f"--import-dir {ACME} --engine sparql --out-dir {{work}}/unscoped --fail-on never --reports minimal",
                      env={"PYTHONHASHSEED": "0"}),
                 Step(f"python scripts/without_java.py {SUITE} data {{work}}/employees.ttl --ontology {V1} "
                      f"--import-dir {ACME} --engine sparql --own-namespace {OWN_DATA} --out-dir {{work}}/scoped "
                      f"--fail-on never --reports minimal", env={"PYTHONHASHSEED": "0"})],
          check=checks(_rea022("unscoped/full_results.csv", True), _rea022_focus("unscoped/full_results.csv"),
                       _rea022("scoped/full_results.csv", False), totals(2, 54)),
          checks="unscoped: REA-022 present, about oq:Graph; scoped: REA-022 absent, 54 findings",
          needs=["tarka-cli"]),

    Claim("C09.10", "Which reports a run writes, and --reports minimal", "09",
          (F, "| `findings.txt` | A person at a terminal, or an agent"), "run",
          steps=[Step(f"{CHECKS} --own-namespace {OWN} --out-dir {{work}}/default --fail-on never"),
                 Step(f"{CHECKS} --own-namespace {OWN} --out-dir {{work}}/minimal --fail-on never --reports minimal"),
                 Step("python scripts/list_files.py {work}/default"),
                 Step("python scripts/list_files.py {work}/minimal")],
          check=_report_files,
          checks="the default run writes findings.txt, full_results.csv, cucumber.json, report.html, features/ "
                 "and plots/, none of the retired summary files; --reports minimal writes exactly two files; "
                 "full_results.csv has source_file and line columns"),

    Claim("C09.11", "The report set changed in 0.17.0, though REPORTS.md says 0.15.0", "09",
          (F, "(The suite's `REPORTS.md` dates the change to 0.15.0."), "source",
          sources=[src("suite commit f6ee897, 'Say where the finding is, and say each thing once'",
                       commit("suite", "f6ee897c7065569805c27cc7c8af0c2ff0738a8b"),
                       "Six files stopped being written: summary_by_category, summary_by_check and top_offenders"),
                   src("suite commit 1af2a2d, 'Bump to 0.17.0' (the first tag containing f6ee897)",
                       commit("suite", "1af2a2d5a77eaa7cb07b03ee75bf1ec282c35bfe"),
                       "Minor rather than patch: six report files are no longer written"),
                   src("suite docs/REPORTS.md", file("suite", "docs/REPORTS.md", "18"), "## What changed in 0.15.0")]),

    Claim("C09.12", "The suite pins shacl below 0.4", "09",
          (F, "The suite responded by pinning `shacl>=0.3.0,<0.4`"), "run", same_as="C07.05",
          notes="The installed package's declared dependencies include `shacl<0.4,>=0.3.0`; the reason is in the "
                f"[pyproject comment]({file('suite', 'pyproject.toml', '33-37')})."),

    Claim("C09.13", "--reports minimal writes two files", "09",
          (F, "`--reports minimal` writes only `findings.txt` and `full_results.csv`."), "run", same_as="C09.10"),

    Claim("C09.14", "run reports 27 findings, one contradiction twice", "09",
          (F, "Two of those Violations are the same `LOG-001`"), "run",
          claim="With HermiT able to run (PYTHONHASHSEED=5, see C14.06), `run` reports 27 findings with 3 "
                "Violations: LOG-001 twice (registry pass and owlrl-closure pass) and REA-021; it exits 1.",
          steps=[Step(f"{SUITE} run --ontology {V1} --import-dir {ACME} --queries {ACME} --own-namespace {OWN} "
                      f"--engine sparql --fail-on Violation --out-dir {{work}}/out --reports minimal",
                      env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/out/full_results.csv --by focus --check LOG-001")],
          check=checks(totals(0, 27, 3, 22, 2), exit_code(0, 1),
                       counts("out/full_results.csv", {"LOG-001": 2, "REA-021": 1}, exact=False)),
          checks="27 total (3 V, 22 W, 2 I), exit 1, LOG-001 twice and REA-021 once"),

    Claim("C09.15", "The testing repository: 165 passed, 10 skipped", "09",
          (F, "**165 passed, 10 skipped**, unchanged by the engine move."), "run",
          steps=[Step("uv run pytest -q", cwd="$EVIDENCE_TESTING_REPO", timeout=900)],
          check=has(0, "165 passed, 10 skipped"), checks="pytest reports 165 passed, 10 skipped",
          needs=["testing-repo", "oxi-gen"],
          notes="Set EVIDENCE_TESTING_REPO to a clone of the testing repository at "
                f"[6d078a1]({commit('testing', '6d078a118959760409e13076650c2d62a4f6dc90')}). It installs the suite "
                "from a sibling checkout, `../consolidated_ontology_suite_python` (v0.22.0 here), and its competency "
                "tests triplify with oxi-gen, found through ONTOLOGY_SUITE_OXI_GEN_BIN (0.5.1 here). Without oxi-gen "
                "40 of those tests error at setup, saying so."),

    Claim("C09.16", "The competency board: 27 green, 0 red", "09",
          (F, "Re-run for this edition: **27 green, 0 red**, in two minutes."), "run",
          steps=[Step("bash experiments/SpecificTests/run-all.sh", cwd="$EVIDENCE_TESTING_REPO", timeout=900)],
          check=checks(has(0, "27 green, 0 red"), has(0, "litres measure volume, not force per unit area")),
          checks="the board ends '27 green, 0 red', and CT-21's verdict reads as quoted",
          needs=["testing-repo"],
          notes="Needs the same sibling suite checkout as C09.15."),

    Claim("C09.17", "Fourteen of 38 questions need no data", "09",
          (F, "Fourteen of the"), "source",
          sources=[src("testing repo experiments/SpecificTests/REVIEW.md",
                       file("testing", "experiments/SpecificTests/REVIEW.md", "32-41"),
                       "Half the tests can be answered before a row of data exists.")]),

    Claim("C09.18", "A clean minimal ontology is not writable", "09",
          (F, "**A clean minimal ontology is not writable.**"), "source",
          sources=[src("testing repo commit fb24a3d", commit("testing", "fb24a3d302409deea6b31da5d061a3edb54839a2"),
                       "A clean minimal ontology turns out not to be writable, which is worth knowing before a "
                       "clean run is read as proof.")]),

    Claim("C09.19", "Seventeen fixtures; 58 of 61 checks pinned", "09",
          (F, "Seventeen fixtures, of which a sample:"), "source",
          sources=[src("testing repo detect.py (17 fixtures declared)", file("testing", "detect.py")),
                   src("testing repo README", file("testing", "README.md", "35-37"),
                       "58 of the 61 checks are pinned by a test")]),

    Claim("C09.20", "The message assertion found EFF-001 within minutes", "09",
          (F, "message read *\"(reaching nced07cc7cad44c0499fd01e010fb1164b1)\"*"), "source",
          sources=[src("testing repo commit 34606a4", commit("testing", "34606a42744cba730cc58944155549631225d621"),
                       "The second found EFF-001 immediately, on 10-efficiency"),
                   src("suite commit 5360394", commit("suite", "5360394d1ac92537998116245662b15fee8636c7"))]),

    Claim("C09.21", "A gate as a config file", "09",
          (F, "The testing repository carries a small `gate.py`"), "source",
          sources=[src("testing repo ontology-suite.yml", file("testing", "ontology-suite.yml")),
                   src("testing repo commit 3c5afbd", commit("testing", "3c5afbdb2c5196ebd3f2c7c05be6ceb07c8e9c28"),
                       "the gate ran eight checks while its merged registry declared 61")]),

    Claim("C09.22", "An ignored gate dies", "09",
          (F, "**This is the commonest way a semantic quality gate dies.**"), "argument",
          notes="A judgement from experience, not a measurement. The mechanism it rests on is measurable: "
                "C09.02 (479 findings, one Violation in 55 the team's own) against C09.04 (23, all theirs)."),
]
