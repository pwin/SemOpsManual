"""Chapter 7 — The toolchain."""
from ._common import (ACME, OWN, SUITE, V1, Claim, Step, all_of, by_check, checks, commit, counts, exit_code,
                      file, has, lacks, nonzero, ok, rows, src, totals, by_version)

F = "docs/07-the-toolchain.md"
SCOPED = f"{SUITE} checks --ontology {V1} --import-dir {ACME} --own-namespace {OWN}"
UNSCOPED = f"{SUITE} checks --ontology {V1} --import-dir {ACME}"
MANUAL_PREV = "fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40"   # the previous edition, suite 0.14.2


def _flaw_foci(csv_rel):
    want = {("LOG-001", OWN + "Contractor"), ("QUA-001", OWN + "hasSkill"), ("QUA-004", OWN + "hasSkill"),
            ("STY-002", OWN + "reports_to"), ("STR-003", OWN + "reports_to")}

    def check(r):
        got = {(x["check_id"], x["focus_node"]) for x in rows(r.file(csv_rel)) if x["check_id"] in dict(want)}
        n = by_check(r.file(csv_rel))
        once = all(n.get(c) == 1 for c, _ in want)
        return all_of(ok(got == want, "LOG-001 on Contractor, QUA-001 and QUA-004 on hasSkill, STY-002 and STR-003 "
                                      "on reports_to", f"got {sorted(got)}"),
                      ok(once, "each exactly once", f"counts {[(c, n.get(c)) for c, _ in want]}"))
    return check


def _engine_table(r):
    sp = by_check(r.file("sparql/full_results.csv"))
    na = by_check(r.file("native/full_results.csv"))
    return all_of(ok("QUA-004" in sp and "QUA-004" not in na, "QUA-004 appears under sparql and not under native",
                     "QUA-004 presence differs from the manual"),
                  ok({k: v for k, v in sp.items() if k != "QUA-004"} == na,
                     "and is the only difference between them", f"sparql {sp} vs native {na}"))


CLAIMS = [
    Claim("C07.01", "The versions every Part III number was measured against", "07",
          (F, "> **Versions this edition was measured against.**"), "run",
          scripts=["scripts/versions.py"],
          steps=[Step("python scripts/versions.py")],
          check=has(0, "PyPI ontology-quality-suite  0.24.1", "PyPI shacl                   0.3.4",
                    "PyPI holosdb                 0.22.0", "PyPI tarka-rdf               0.1.1",
                    "release shacl                shacl 0.3.4", "release tarka                tarka 0.1.1",
                    "release holos                holos 0.22.0", "npm ontology-suite           0.16.1",
                    "npm shacl-wasm-node          0.3.4", "npm holos-wasm-node          0.22.0"),
          checks="the installed packages, release binaries and npm packages are the versions in the table",
          needs=["node"],
          notes="The testing repository was used at "
                f"[6cdfb14]({commit('testing', '6cdfb14a3c2857b61dcb32f49f56a4829b0d0664')}); see C09.15."),

    Claim("C07.02", "The engine changed and Chapter 9's figures did not", "07",
          (F, "every figure in [Chapter 9](09-continuous-integration.md) came out the"), "source",
          sources=[src("the previous edition of Chapter 9 (suite 0.14.2, rdflib and pyshacl)",
                       file("manual", "docs/09-continuous-integration.md", "56", ref=MANUAL_PREV),
                       "Findings: 479 total (55 Violation, 340 Warning, 84 Info)")],
          notes="Today's figures, on holosdb and the shacl engine, are reproduced in C09.02 (479: 55/340/84), "
                "C09.03 (27) and C09.04 (23)."),

    Claim("C07.03", "One registry: 61 checks in ten categories, 44 SPARQL files and 6 shape files", "07",
          (F, "The suite's quality rules are not code. They are **data**"), "run",
          scripts=["scripts/inspect_packages.py"],
          steps=[Step("python scripts/inspect_packages.py")],
          check=has(0, "registry entries: 61 in 10 categories", "portable .rq checks: 44; SHACL shape files: 6"),
          checks="the installed suite's registry has 61 entries in 10 categories, 44 .rq checks and 6 shape files"),

    Claim("C07.04", "The editor runs the same engines at the same versions", "07",
          (F, "the 44 portable checks run on **holosdb** in Python and on"), "source",
          sources=[src("extension package.json (0.16.1)", file("webapp", "package.json", "489-493"),
                       '"holos-wasm-node": "^0.21.0",'),
                   src("extension package-lock.json (0.16.1): the holos-wasm-node it bundles",
                       file("webapp", "package-lock.json"), '"node_modules/holos-wasm-node"')],
          notes="Below 1.0 a caret admits patch releases only, so `^0.21.0` means 0.21.x. The 0.16.1 release's "
                "lock file still resolves it to 0.21.0; C07.01 shows holosdb 0.22.0 under the CLI. What 0.21.1 and "
                "0.22.0 changed, the store fix in C13.10 and the validate gate in C11.29, is in a part of HOLOS the "
                "extension does not call: it validates with shacl-wasm-node."),

    Claim("C07.05", "Both engines are runtime dependencies; owlready2 too; the wheels are libraries", "07",
          (F, "That one line now brings both engines: `holosdb` and `shacl` are runtime"), "run",
          scripts=["scripts/inspect_packages.py"],
          steps=[Step("python scripts/inspect_packages.py")],
          check=checks(has(0, "commands installed: ontology-quality-suite", "holosdb>=0.15", "owlready2>=0.51",
                           "shacl 0.3.4\n    commands installed: none (library only)",
                           "tarka-rdf 0.1.1\n    commands installed: none (library only)",
                           "holosdb 0.22.0\n    commands installed: none (library only)"),
                       by_version((0, 23, 0), has(0, "shacl<0.4,>=0.3.3"), has(0, "shacl<0.4,>=0.3.0"))),
          checks="ontology-quality-suite declares holosdb, shacl (below 0.4; from 0.3.3 since suite 0.23.0, which "
                 "needs shacl.rdfs_closure) and owlready2 as runtime dependencies and installs the only command; "
                 "shacl, tarka-rdf and holosdb install none"),

    Claim("C07.06", "STY-003's message vanished on 60 of 65 findings", "07",
          (F, "On the suite's stress fixture, 60 of 65 findings had no message at"), "source",
          sources=[src("suite commit 9e6f99c", commit("suite", "9e6f99c420699294917b608a36869500150933e9"),
                       "BIND left the variable unbound and the template dropped the message -- 60 of 65 findings on "
                       "the stress fixture")]),

    Claim("C07.07", "STR() of a blank node: lenient, conformant, and the guard", "07",
          (F, "What happened next depended on the engine:"), "run",
          scripts=["scripts/engine_leniency.py"],
          steps=[Step("python scripts/engine_leniency.py")],
          check=lambda r: _leniency(r[0].stdout),
          checks="unguarded: rdflib prints an internal identifier, holosdb and pyoxigraph leave the message "
                 "unbound; COALESCE: rdflib still prints the identifier; IF(isBlank(...)): all three print "
                 "'[a blank node]'"),

    Claim("C07.08", "pyshacl stays as a witness because it caught a real regression", "07",
          (F, "| `shacl` (SHACL) | pyshacl | pyshacl caught a real regression"), "source",
          sources=[src("suite commit 9e6f99c", commit("suite", "9e6f99c420699294917b608a36869500150933e9"),
                       "pyshacl is what caught the isIRI($this) blank-node regression in shacl 0.1.5")]),

    Claim("C07.09", "Positional dedup, '[a blank node]' in both repositories, owlrl leaves the checks path", "07",
          (F, "The move had costs, and the suite is candid about them."), "source",
          sources=[src("suite commit 9e6f99c", commit("suite", "9e6f99c420699294917b608a36869500150933e9"),
                       "merge._anonymous_key matches anonymous findings positionally within (check, path, value)"),
                   src("extension commit 7198f91", commit("webapp", "7198f91e256b613503ad385f666460006c4631fe"),
                       'The text "[a blank node]" is deliberately identical to the queries\'')]),

    Claim("C07.10", "The extension adds six checks of its own: three MDL, three MAL", "07",
          (F, "Then it adds six of its own with no CLI"), "source", same_as="C08.03"),

    Claim("C07.11", "VOC-001 is declared, not runnable, by the CLI", "07",
          (F, "Nothing in the Python package implements it; only `registry.json` mentions the id."), "source",
          same_as="C08.04"),

    Claim("C07.12", "Severity belongs to the shape that produces the result", "07",
          (F, "**Severity belongs to the shape that produces the result.**"), "run",
          data=["data/shacl/data.ttl", "data/shacl/shapes-warning.ttl", "data/shacl/shapes-warning-on-node.ttl"],
          steps=[Step("shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning.ttl -f turtle"),
                 Step("shacl -d data/shacl/data.ttl -s data/shacl/shapes-warning-on-node.ttl -f turtle")],
          check=checks(has(0, "sh:resultSeverity sh:Warning"), has(1, "sh:resultSeverity sh:Violation"),
                       lacks(1, "sh:resultSeverity sh:Warning")),
          checks="sh:severity on the property shape gives a Warning; the same declaration on the node shape "
                 "leaves the property shape's result a Violation",
          needs=["shacl-cli"]),

    Claim("C07.13", "The registry declares; the directories decide", "07",
          (F, "suite's own docs now put it in five words:"), "source",
          sources=[src("suite docs/EXTENDING.md", file("suite", "docs/EXTENDING.md", "29"),
                       "The registry declares; the directories decide.")],
          notes="C08.24 shows a query with no registry entry running and reporting as UNMAPPED."),

    Claim("C07.14", "Eleven CLI-only checks, three extension-only", "07",
          (F, "Neither side runs all sixty-one."), "source", same_as="C08.05"),

    Claim("C07.15", "A sixteen-case comment fixture both repositories carry", "07",
          (F, "The fix is a fixture of sixteen cases that **both repositories carry**"), "source",
          sources=[src("suite commit 6295588", commit("suite", "629558887b2d7fd378229e736be841de8e68ae28"),
                       "The cases are hand-written, not generated from either implementation."),
                   src("extension commit 6489c1a", commit("webapp", "6489c1ae0c17a4cf7c30c2571dd6a605dbd90383"),
                       "A fixture of 16 cases now states that, and both repos carry it.")]),

    Claim("C07.16", "--extra native-shacl parses but installs nothing", "07",
          (F, "(`uv sync --extra native-shacl` still parses but"), "source",
          sources=[src("suite pyproject.toml (0.22.0)", file("suite", "pyproject.toml", "53-58"),
                       "It installs nothing: `shacl` is a runtime dependency now, not an opt-in.")]),

    Claim("C07.17", "A locked dependency does not move with pip --upgrade", "07",
          (F, "> **Upgrading a checkout.**"), "source",
          sources=[src("suite commit 1b6000a", commit("suite", "1b6000aa96742b04b2e70f29d07298bad3770a2d"),
                       "uv pip install --upgrade does not move it: uv run re-syncs from uv.lock, so uv lock "
                       "--upgrade-package is the step."),
                   src("suite commit 091e0e4", commit("suite", "091e0e4effe1a9cbaddccc63436851decac09035"),
                       "The committed uv.lock had gone stale at 0.14.3"),
                   src("suite uv.lock at the 0.22.0 release", file("suite", "uv.lock", "167-168", ref="749af3e1be749ace3aab3ea4b492d72b3b21dbde"), 'version = "0.15.0"')]),

    Claim("C07.18", "Oxigraph went in 0.13.11; the .vsix shrank from 20.2 to 17.5 MB", "07",
          (F, "went in 0.13.11, and the `.vsix` dropped from 20.2 MB to 17.5 MB with it."), "source",
          sources=[src("extension commit e4583b9", commit("webapp", "e4583b9a9d47f678bba2e5efaba7b7d0b21ca504"),
                       "The vsix goes from 20.22 MB to 17.52 MB.")]),

    Claim("C07.19", "vsce --no-dependencies packages an extension with no engines", "07",
          (F, "`vsce package --no-dependencies`"), "source",
          sources=[src("extension commit ec96b93", commit("webapp", "ec96b93b163f8c11b85cf90ecc5c9151f927c0b6"),
                       "contains none of the engines")]),

    Claim("C07.20", "Only ontology-quality-suite installs a command", "07",
          (F, "**The wheels are libraries only.**"), "run", same_as="C07.05"),

    Claim("C07.21", "Each release carries SHA256SUMS", "07",
          (F, "Windows, each release with a `SHA256SUMS` file. Check it."), "source",
          sources=[src("SHACL Engine v0.3.4 release", "https://github.com/pwin/SHACL_Engine/releases/tag/v0.3.4"),
                   src("HOLOS v0.22.0 release", "https://github.com/pwin/triplestore/releases/tag/v0.22.0"),
                   src("tarka v0.1.1 release", "https://github.com/pwin/tarka/releases/tag/v0.1.1")],
          scripts=["tools/fetch_binaries.py"],
          notes="`tools/fetch_binaries.py` downloads each archive and refuses one whose SHA-256 does not match "
                "the release's SHA256SUMS; the binaries used throughout this evidence came through it."),

    Claim("C07.22", "--engine: native misses QUA-004; sparql and both give 23", "07",
          (F, "All modes, against this manual's fixture with `--own-namespace`, same ontology,"), "run",
          steps=[Step(f"{SCOPED} --engine {e} --out-dir {{work}}/{d} --fail-on never --reports minimal")
                 for e, d in (("native", "native"), ("shacl", "shacl"), ("sparql", "sparql"),
                              ("native+sparql", "nativesparql"), ("both", "both"))],
          check=checks(totals(0, 22, 1, 21, 0), totals(1, 22, 1, 21, 0), totals(2, 23, 1, 22, 0),
                       totals(3, 23, 1, 22, 0), totals(4, 23, 1, 22, 0), _engine_table),
          checks="native and shacl: 22 (1 V, 21 W); sparql, native+sparql and both: 23 (1 V, 22 W); QUA-004 is "
                 "the only difference"),

    Claim("C07.23", "The engine choice is not about speed at this size", "07",
          (F, "On the unscoped run the three take about 1.7 s (`native`), 2.0 s (`sparql`) and"), "run",
          steps=[Step(f"{UNSCOPED} --engine {e} --out-dir {{work}}/{d} --fail-on never --reports minimal")
                 for e, d in (("native", "native"), ("native+sparql", "both"), ("sparql", "sparql"))],
          check=lambda r: (all(s.rc == 0 for s in r.steps),
                           "whole-process times: " + ", ".join(f"{s.cmd.split('--engine ')[1].split()[0]} "
                                                               f"{s.seconds:.1f} s" for s in r.steps)),
          checks="nothing is asserted about the times; they are recorded. Each run must succeed",
          notes="Times vary by machine. Three repeated runs here gave native 1.7 s, sparql 2.0–2.1 s and "
                "native+sparql 2.1–2.3 s."),

    Claim("C07.24", "Until 0.6.0 the shapes put sh:severity in the wrong place", "07",
          (F, "**The severity lesson is about shape authoring, not engines.**"), "source",
          sources=[src("this manual's earlier edition (14 August 2026, suite 0.5.x), measured then",
                       file("manual", "docs/07-the-toolchain.md", "197-198", ref="aba4679abe7456c70fd638ae18e0084e07f2f3b1"),
                       "`both` reports **five Violations where `native+sparql` reports two**"),
                   src("suite commit 2f4950c (0.6.0)", commit("suite", "2f4950c4436868fb6ea203c0ce271727b256cfef"),
                       "sh:severity was declared inside each sh:sparql [...] SPARQLConstraint block rather than on "
                       "the enclosing shape, where SHACL defines it.")],
          notes="The commit gives its own measurement on a different fixture: 17 V / 1 W / 0 I under pyshacl "
                "against 1 / 15 / 2 under the native engine, for the same 18 findings."),

    Claim("C07.25", "My own node-shape severity mistake", "07",
          (F, "I tripped over the same thing myself while testing the engine for this"), "run", same_as="C07.12"),

    Claim("C07.26", "--inference owlrl is refused: a traceback at 0.22.0, a usage error from 0.23.0", "07",
          (F, "> **`--inference owlrl` and `both` are gone from the checks path.**"), "run",
          steps=[Step(f"{UNSCOPED} --inference owlrl --out-dir {{work}}/owlrl --fail-on never --reports minimal"),
                 Step(f"{SUITE} checks --help")],
          check=checks(nonzero(0), by_version(
              (0, 23, 0),
              checks(has(0, "argument --inference: invalid choice: 'owlrl'"), lacks(0, "Traceback"),
                     has(1, "--inference {none,rdfs}")),
              checks(has(0, "Traceback (most recent call last)",
                         "ValueError: --inference 'owlrl' is not available (none/rdfs are)"),
                     has(1, "--inference {none,rdfs,owlrl,both}")))),
          checks="--inference owlrl exits non-zero. At 0.22.0, with a Python traceback ending in the ValueError, and "
                 "--help lists owlrl and both; from 0.23.0, with a one-line usage error, and --help offers none and "
                 "rdfs only"),

    Claim("C07.27", "--inference rdfs: half the suite at 0.22.0, every engine from 0.23.0", "07",
          (F, "**And `--inference rdfs` reached only half the suite until 0.23.0.**"), "run",
          steps=[Step(f"{UNSCOPED} --engine sparql --inference {i} --out-dir {{work}}/{i} --fail-on never "
                      f"--reports minimal") for i in ("owlrl", "rdfs", "none")]
                + [Step(f"{UNSCOPED} --inference rdfs --out-dir {{work}}/both-rdfs --fail-on never --reports minimal"),
                   Step("python scripts/diff_findings.py {work}/none/full_results.csv {work}/rdfs/full_results.csv")],
          check=by_version(
              (0, 23, 0),
              checks(nonzero(0), totals(1, 489, 57, 339, 93), totals(2, 479, 55, 340, 84), totals(3, 489, 57, 339, 93),
                     has(4, "gained 21:", "STR-007 9", "STY-003 9", "STR-009 3", "lost 11:", "STR-006 1", "DAT-002 1")),
              checks(exit_code(0, 0), totals(0, 479, 55, 340, 84), totals(1, 479, 55, 340, 84),
                     totals(2, 479, 55, 340, 84), totals(3, 497))),
          checks="at 0.22.0: under --engine sparql, owlrl, rdfs and none give 479 each, exit 0, and the default "
                 "engine with rdfs gives 497. From 0.23.0: owlrl is refused; rdfs gives 489 under sparql and under "
                 "the default engine alike, against 479 without it; the closure gains 21 findings (STR-007 9, "
                 "STY-003 9, STR-009 3) and loses 11 (STR-007 9, STR-006, DAT-002)",
          sources=[src("suite pipeline.py at 0.22.0: inference applied inside `if uses_shacl:`",
                       file("suite", "ontology_suite/pipeline.py", "141-168", ref="749af3e1be749ace3aab3ea4b492d72b3b21dbde"), "if inference not in (\"none\", \"rdfs\"):"),
                   src("suite commit d7d7a98, the fix", commit("suite", "d7d7a987cb754221b6c57a5997445628e219851b"),
                       "The closure is now materialised once, centrally, and both arms read the result.")]),

    Claim("C07.28", "--verbose shows what each input resolved to", "07",
          (F, "Every subcommand takes `-v`/`--verbose`, which prints what each input option"), "run",
          steps=[Step(f"{SCOPED} --engine sparql --out-dir {{work}}/v --fail-on never --reports minimal -v")],
          check=has(0, "2 owl:imports resolved:", "http://xmlns.com/foaf/0.1/  <-  ",
                    "http://www.w3.org/ns/org#  <-  ", "[verbose] engine: sparql"),
          checks="the run names both resolved imports and the file each came from, and the engine"),

    Claim("C07.29", "Each deliberate flaw produces exactly one finding", "07",
          (F, "Each deliberate flaw produces **exactly one finding**"), "run",
          steps=[Step(f"{SCOPED} --engine sparql --out-dir {{work}}/own --fail-on never --reports minimal"),
                 Step("python scripts/summarise_findings.py {work}/own/full_results.csv")],
          check=checks(_flaw_foci("own/full_results.csv"),
                       counts("own/full_results.csv", {"QUA-009": 9, "QUA-010": 9}, exact=False)),
          checks="LOG-001 on acme:Contractor, QUA-001 and QUA-004 on acme:hasSkill, STY-002 and STR-003 on "
                 "acme:reports_to, each once; and QUA-009 and QUA-010 nine times each"),

    Claim("C07.30", "v2 renames Engineer, with a migration annotation, and adds a class and a property", "07",
          (F, "`acme-org-v2.ttl` is a plausible next release."), "run", same_as="C12.01"),

    Claim("C07.31", "The testing repository: seventeen fixtures, a 38-question board", "07",
          (F, "holds seventeen deliberately broken ontologies, a 38-question competency board"), "source",
          same_as="C09.19"),

    Claim("C07.32", "A lenient engine let a check pass in tests and fail in the field", "07",
          (F, "**A lenient engine let a check pass in the"), "run", same_as="C07.07"),
]


def _leniency(out: str):
    sections = out.split("== ")
    un = next(s for s in sections if s.startswith("unguarded"))
    co = next(s for s in sections if s.startswith("COALESCE"))
    gu = next(s for s in sections if s.startswith("guarded"))
    import re
    internal = re.compile(r"rdflib\s+\['A label on n[0-9a-f]{20,}")
    return all_of(
        ok(bool(internal.search(un)), "unguarded: rdflib names an internal identifier", "rdflib unguarded differs"),
        ok(un.count("['(unbound)']") == 2, "holosdb and pyoxigraph leave the message unbound",
           "conformant engines did not both leave it unbound"),
        ok(bool(internal.search(co)) and co.count("[a blank node]") == 2,
           "COALESCE: rdflib still names the identifier, the other two say '[a blank node]'", "COALESCE differs"),
        ok(gu.count("[a blank node]") == 3, "IF(isBlank(...)): all three say '[a blank node]'", "guard differs"))
