"""Chapter 10 — Ingest and transform."""
from ._common import (ACME, HOLOS_URL, OWN, OWN_DATA, SUITE, V1, Claim, Service, Step, all_of, by_check, checks,
                      commit, counts, exit_code, file, has, lacks, nonzero, ok, rows, src, totals, by_version)

F = "docs/10-ingest-and-transform.md"
TRIPLIFY = f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"
DATA = f"{SUITE} data {{work}}/employees.ttl --ontology {V1} --import-dir {ACME} --engine sparql"
SKETCH = f"{SUITE} sketch --queries {ACME} --ontology {V1} --import-dir {ACME} --out-dir {{work}}/sketch"

E004 = """<https://acme.example.org/data/employee/E004> a acme:Employee , acme:Engineer ;
	foaf:mbox <mailto:margaret.hamilton@acme.example.org> ;
	foaf:name "Margaret Hamilton" ;
	acme:hasEmployeeId "E004" ;
	acme:hasRole "Test Engineer" ;
	acme:hasSkill "Automation" ;
	acme:worksIn <https://acme.example.org/data/department/QA> ."""


def _file_has(rel, *texts):
    def check(r):
        body = r.file(rel).read_text(encoding="utf-8")
        missing = [t for t in texts if t not in body]
        return ok(not missing, f"{rel} contains {', '.join(repr(t[:60]) for t in texts)}", f"{rel} lacks {missing}")
    return check


def _focus(csv_rel, check_id, expected):
    def check(r):
        got = sorted(x["focus_node"] for x in rows(r.file(csv_rel)) if x["check_id"] == check_id)
        return ok(got == sorted(expected), f"{check_id} on {', '.join(expected)}", f"{check_id} foci: {got}")
    return check


def _tql004(r):
    row = next((x for x in rows(r.file("tq/full_results.csv")) if x["check_id"] == "TQL-004"), None)
    if row is None:
        return False, "no TQL-004 finding"
    return all_of(ok(row["source_file"].replace(chr(92), "/").endswith("sites.rq") and row["line"] == "10",
                     "TQL-004 carries source_file sites.rq and line 10 as fields",
                     f"source_file={row['source_file']!r} line={row['line']!r}"),
                  ok("(sites.rq:" not in row["message"], "and not in the message text", "position in the message"),
                  ok("Every triple using it is dropped" in row["message"], "its message says the triples are dropped",
                     f"message: {row['message']!r}"))


def _mailbox_split(csv_rel):
    def check(r):
        rs = [x for x in rows(r.file(csv_rel)) if x["check_id"] in ("STR-006", "DAT-002")]
        out = []
        for cid in ("STR-006", "DAT-002"):
            mine = [x["message"] for x in rs if x["check_id"] == cid]
            dept = sum("/data/department/" in m for m in mine)
            mail = sum("mailto:" in m for m in mine)
            out.append(ok(len(mine) == 10 and dept == 5 and mail == 5, f"{cid}: 10, five departments and five mailboxes",
                          f"{cid}: {len(mine)} ({dept} departments, {mail} mailboxes)"))
        return all_of(*out)
    return check


def _rea(csv_rel, present, absent):
    def check(r):
        ids = by_check(r.file(csv_rel))
        return ok(all(p in ids for p in present) and not any(a in ids for a in absent),
                  f"{', '.join(present) or 'nothing'} present; {', '.join(absent)} absent",
                  f"checks present: {sorted(k for k in ids if k.startswith('REA'))}")
    return check


def _focus_includes(csv_rel, check_id, focus, present):
    def check(r):
        foci = {x["focus_node"] for x in rows(r.file(csv_rel)) if x["check_id"] == check_id}
        return ok((focus in foci) == present, f"{csv_rel}: {check_id} {'includes' if present else 'excludes'} {focus}",
                  f"{csv_rel}: {check_id} foci {sorted(foci)}")
    return check


CLAIMS = [
    Claim("C10.01", "sketch: 38 Infos, 8 triples and 7 entities from one query file", "10",
          (F, "The summary line is the useful part: **8 triples, 7 entities from 1 query"), "run",
          steps=[Step(SKETCH),
                 Step("python scripts/summarise_findings.py {work}/sketch/full_results.csv"),
                 Step("python scripts/summarise_findings.py {work}/sketch/full_results.csv --by focus --check TQL-003")],
          check=checks(totals(0, 38, 0, 0, 38), has(0, "Sketch used 1 query file(s); 8 triples, 7 entities."),
                       counts("sketch/full_results.csv", {"CNF-005": 35, "TQL-003": 3}),
                       _focus("sketch/full_results.csv", "TQL-003", ["?name", "?role", "?skill"])),
          checks="38 Infos: 35 CNF-005 and 3 TQL-003 (?name, ?role, ?skill); 8 triples and 7 entities from 1 file"),

    Claim("C10.02", "The 38 Infos, and what TQL-003 says", "10",
          (F, "The 38 Infos are 35 × `CNF-005`"), "run", same_as="C10.01"),

    Claim("C10.03", "--queries, --query-pattern (alias --file-pattern), four extensions", "10",
          (F, "`--queries` takes a file or a directory. Use `--query-pattern` to narrow or widen"), "run",
          steps=[Step(f"{SUITE} sketch --help")],
          check=has(0, "--query-pattern QUERY_PATTERN, --file-pattern QUERY_PATTERN", "*.sparql,*.rq,*.tarql,*.tq"),
          checks="`sketch --help` gives --file-pattern as an alias of --query-pattern, defaulting to the four "
                 "extensions"),

    Claim("C10.04", "TQL-004, with its position as fields", "10",
          (F, "Since 0.17.0 the TARQL checks carry their position as **fields**"), "run",
          data=["data/tql004/sites.rq"],
          steps=[Step(f"{SUITE} sketch --queries data/tql004/sites.rq --out-dir {{work}}/tq --reports minimal "
                      f"--fail-on never")],
          check=checks(counts("tq/full_results.csv", {"TQL-004": 1}, exact=False), _tql004,
                       _file_has("tq/findings.txt", "> 10 |   BIND(CONCAT(")),
          checks="TQL-004 fires once, with source_file sites.rq and line 10 as fields (not in the message), and "
                 "findings.txt quotes line 10"),

    Claim("C10.05", "A CONCAT-built IRI: dropped as a subject, a literal as an object", "10",
          (F, "`TQL-004` repays reading twice."), "run",
          data=["data/tql004/sites.rq", "data/tql004/works-in.rq", "data/tql004/depts.csv"],
          steps=[Step("tarka run -q data/tql004/sites.rq -i data/tql004/depts.csv --ntriples"),
                 Step("tarka run -q data/tql004/works-in.rq -i data/tql004/depts.csv --ntriples")],
          check=checks(exit_code(0, 0), lambda r: ok(not r[0].stdout.strip(), "as a subject: no triples at all",
                                                     f"output: {r[0].stdout[:100]!r}"),
                       exit_code(1, 0), has(1, '<https://acme.example.org/ns/worksIn> '
                                               '"https://acme.example.org/data/department/ENG" .')),
          checks="both runs exit 0; the subject case writes nothing; the object case writes the department as a "
                 "string literal",
          needs=["tarka-cli"]),

    Claim("C10.06", "sketch writes bind-facts.ttl and bind-review.txt", "10",
          (F, "The stage also writes **`bind-facts.ttl`**"), "run",
          steps=[Step(SKETCH + " --reports minimal"),
                 Step("python scripts/list_files.py {work}/sketch")],
          check=checks(has(1, "bind-facts.ttl", "bind-review.txt"),
                       _file_has("sketch/bind-review.txt", "1 query file(s), 3 BIND statement(s)",
                                 "1. Variables bound differently across files (0)",
                                 "2. Constructed-IRI variables never bound (0)",
                                 "3. CONSTRUCT variables not bound in the query (3)", "?name, ?role, ?skill")),
          checks="both files are written; bind-review.txt answers its three questions"),

    Claim("C10.07", "tarka's output for E004 is the block quoted in earlier editions", "10",
          (F, "The output is genuine RDF, and for this fixture it is the same, term for term"), "run",
          steps=[Step(TRIPLIFY)],
          check=checks(exit_code(0, 0), _file_has("employees.ttl", E004)),
          checks="the E004 block in tarka's Turtle is byte-identical to the manual's listing",
          needs=["tarka-cli"],
          sources=[src("the previous edition's oxi-gen listing", file("manual", "docs/10-ingest-and-transform.md",
                                                                       ref="fc6de6da90d54a57bbbd2163ebc5b5dfe246ec40"),
                       'foaf:mbox <mailto:margaret.hamilton@acme.example.org> ;')]),

    Claim("C10.08", "tarka takes oxi-gen's options; --test N reads N rows", "10",
          (F, "tarka takes `oxi-gen`'s options"), "run",
          steps=[Step("tarka run --help"),
                 Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv --ntriples --test 2 "
                      f"-o {{work}}/two.nt"),
                 Step("python scripts/compare_ntriples.py {work}/two.nt {work}/two.nt")],
          check=checks(has(0, "--ntriples", "--split", "--dedup", "--test", "--bind-empty-strings", "--gzip",
                           "--no-header-row", "--delimiter", "--tab", "--header"),
                       has(2, "16 triples")),
          checks="--help lists the oxi-gen options; --test 2 gives 16 triples (2 rows × 8)",
          needs=["tarka-cli"]),

    Claim("C10.09", "1.7× and 2.6× faster than oxi-gen, by tarka's own measurement", "10",
          (F, "Its own measurement, on a"), "source",
          sources=[src("tarka README", file("tarka", "README.md", "41-43"),
                       "tarka ran the TARQL query 1.7 times as fast as oxi-gen, and the OTTR templates 2.6 times as fast.")],
          notes="Not reproduced here: it needs oxi-gen and the 200,000-row file."),

    Claim("C10.10", "The OTTR template lints clean and gives the same 40 triples", "10",
          (F, "Sorted, the 40 triples are identical to the TARQL query's. Verified."), "run",
          data=["data/ottr/employees.stottr", "data/ottr/employees-iri.csv"],
          steps=[Step("tarka lint -l data/ottr/employees.stottr"),
                 Step("tarka run -l data/ottr/employees.stottr -T acme:Employee -i data/ottr/employees-iri.csv "
                      "--ntriples -o {work}/ottr.nt"),
                 Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv --ntriples -o {{work}}/tarql.nt"),
                 Step("python scripts/compare_ntriples.py {work}/ottr.nt {work}/tarql.nt")],
          check=checks(has(0, "1 template: 0 errors, 0 warnings"), has(3, "40 triples", "isomorphic: True")),
          checks="lint reports 0 errors and 0 warnings; the OTTR and TARQL outputs are the same 40 triples",
          needs=["tarka-cli"],
          notes="The CSV for the template carries full IRIs, since an OTTR template receives IRIs rather than "
                "building them."),

    Claim("C10.11", "Without a mailto: prefix, run -l dropped every row, silently, up to 0.1.1", "10",
          (F, "> **One silent failure, found while checking this, and fixed since.**"), "run",
          data=["data/ottr/employees-no-mailto-prefix.stottr", "data/ottr/employees-optional-mbox.stottr",
                "data/ottr/employees-bad-mbox.csv", "data/ottr/employees.bottr.ttl",
                "data/ottr/employees-bad-id.bottr.ttl"],
          steps=[Step("tarka run -l data/ottr/employees-no-mailto-prefix.stottr -T acme:Employee "
                      "-i data/ottr/employees-iri.csv --ntriples -o {work}/none.nt"),
                 Step("python scripts/compare_ntriples.py {work}/none.nt {work}/none.nt"),
                 Step("tarka run -l data/ottr/employees-optional-mbox.stottr -T acme:Employee "
                      "-i data/ottr/employees-iri.csv --ntriples -o {work}/optional.nt"),
                 Step("python scripts/compare_ntriples.py {work}/optional.nt {work}/optional.nt"),
                 Step("tarka run -l data/ottr/employees.stottr -T acme:Employee "
                      "-i data/ottr/employees-bad-mbox.csv --ntriples -o {work}/bad-mbox.nt"),
                 Step("python scripts/compare_ntriples.py {work}/bad-mbox.nt {work}/bad-mbox.nt"),
                 Step("tarka bottr -l data/ottr/employees.stottr data/ottr/employees-bad-id.bottr.ttl --ntriples "
                      "-o {work}/bad-id.nt"),
                 Step("tarka bottr -l data/ottr/employees-no-mailto-prefix.stottr data/ottr/employees.bottr.ttl "
                      "--ntriples -o {work}/bottr.nt"),
                 Step("python scripts/compare_ntriples.py {work}/bottr.nt {work}/bottr.nt")],
          check=checks(exit_code(0, 0), lambda r: ok(r[0].out.strip() == "", "run -l: no message",
                                                     f"run -l said: {r[0].out.strip()[:120]!r}"),
                       has(1, ": 40 triples"), exit_code(2, 0), has(3, ": 40 triples"),
                       exit_code(4, 1), has(4, "tarka: left out: row 3: column mbox: 'n/a' is not an IRI",
                                            "tarka: 1 of 5 rows left out"),
                       has(5, ": 32 triples"),
                       exit_code(6, 1), has(6, "5 of 5 instances left out; nothing was made",
                                            "row 1: argument 4 (id)"),
                       exit_code(7, 0), has(8, ": 40 triples")),
          checks="since 0.2.0, run -l without the prefix: exit 0, no message, all 40 triples, as with ?mbox "
                 "optional; a mailbox that is not an IRI: that row left out and named, the other 32 triples "
                 "written, exit 1; bOTTR with a cell it cannot build: each instance reported, exit 1; the same "
                 "rows as a bOTTR map with no prefix: 40 triples",
          notes="Up to 0.1.1 the first run wrote 0 triples, and with ?mbox optional 35, each with exit 0 and no "
                "message: the recorded run of the previous edition.",
          needs=["tarka-cli"]),

    Claim("C10.12", "Parquet input, data frames, and typed literals from typed columns", "10",
          (F, "`-i` takes Parquet and Arrow IPC files as well as CSV, read with Polars, and the"), "run",
          data=["data/ottr/headcount.stottr"],
          scripts=["scripts/tarka_python.py"],
          steps=[Step(f"python scripts/tarka_python.py {ACME} data/ottr {{work}}"),
                 Step(f"tarka run -q {ACME}/employees.rq -i {{work}}/employees.parquet --ntriples -o {{work}}/parquet.nt"),
                 Step("python scripts/compare_ntriples.py {work}/parquet.nt {work}/tarql.nt")],
          check=checks(has(0, "4. Polars frame of 5 rows -> 40 triples",
                           '"42"^^<http://www.w3.org/2001/XMLSchema#integer>',
                           "2. OTTR templates: 40 triples; identical to the TARQL output: True",
                           "3. OTTR without the mailto: prefix: returned None, raised nothing, wrote 40 triples",
                           "a mailbox that is not an IRI: ValueError (1 row left out: / row 3: column mbox: 'n/a' "
                           "is not an IRI); the other rows written, 32 triples"),
                       has(2, "isomorphic: True")),
          checks="a Polars frame maps to 40 triples; an Int64 column through an xsd:integer parameter gives "
                 '"42"^^xsd:integer; the CLI reads the Parquet file and gives the same 40 triples; the Python '
                 "API, like the CLI since 0.2.0, reads the mailboxes without the prefix, and raises a ValueError "
                 "naming a row it leaves out, once the rest is written",
          needs=["tarka-cli"]),

    Claim("C10.13", "Shapes from the mapping, and --validate conforms", "10",
          (F, "and `tarka run … --validate` checks the output against them. On the acme data"), "run",
          steps=[Step(f"tarka shapes -q {ACME}/employees.rq -o {{work}}/employees.shapes.ttl"),
                 Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl "
                      f"--validate --report {{work}}/report.ttl")],
          check=checks(exit_code(0, 0), exit_code(1, 0),
                       _file_has("employees.shapes.ttl", "sh:targetClass acme:Employee",
                                 "[ sh:path acme:worksIn ; sh:nodeKind sh:IRI ]",
                                 "[ sh:path foaf:mbox ; sh:nodeKind sh:IRI ]"),
                       _file_has("report.ttl", "sh:conforms true")),
          checks="the shapes target acme:Employee with worksIn and mbox as IRIs; the validated run conforms",
          needs=["tarka-cli"]),

    Claim("C10.14", "Generated shapes accept the dangling departments", "10",
          (F, "That is useful, and it is worth being exact about why."), "run",
          same_as="C10.13",
          notes="The same run that conforms (C10.13) is the one in which `data` finds every `worksIn` target "
                "untyped and dangling (C10.19)."),

    Claim("C10.15", "--post streams into holos-server: the graph arrives whole", "10",
          (F, "Verified for this edition against `holos-server`: the"), "run",
          services=[Service(f"holos-server --listen 127.0.0.1:7899 --no-ui", f"{HOLOS_URL}/health")],
          steps=[Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv --post {HOLOS_URL}/graph "
                      f"--graph https://acme.example.org/graph/triplified/employees"),
                 Step(f"python scripts/endpoint_stats.py {HOLOS_URL}/query")],
          check=checks(exit_code(0, 0), has(1, "https://acme.example.org/graph/triplified/employees", "40")),
          checks="the post succeeds and the named graph holds 40 triples",
          needs=["tarka-cli", "holos-cli"]),

    Claim("C10.16", "tarka speaks the protocol, in RDF 1.1, with the engine built without RDF 1.2", "10",
          (F, "tarka speaks the protocol rather than linking any particular store in"), "source",
          sources=[src("tarka commit 26f256a", commit("tarka", "26f256a28f10d299a4cf1c5dd49ba52cd37122a7")),
                   src("tarka README", file("tarka", "README.md", "45"), "tarka works with RDF 1.1 and SPARQL 1.1.")]),

    Claim("C10.17", "The suite's triplify still needs oxi-gen, and says so", "10",
          (F, "If you have no `oxi-gen` build, `triplify` says so in a warning and"), "run",
          steps=[Step(f"{SUITE} triplify --csv-dir {ACME} --queries {ACME} --out-dir {{work}}/out",
                      env={"ONTOLOGY_SUITE_OXI_GEN_BIN": ""}, note="with no oxi-gen configured")],
          check=checks(has(0, "WARNING: oxi-gen binary not found", "Triplified 0 file(s)")),
          checks="a warning that oxi-gen was not found, and nothing triplified"),

    Claim("C10.18", "data: 548 unscoped (549 at 0.23.0, 550 at 0.22.0), 54 scoped, with HermiT running", "10",
          (F, "Findings: 548 total (66 Violation, 363 Warning, 119 Info)"), "run",
          steps=[Step(TRIPLIFY),
                 Step(f"{DATA} --out-dir {{work}}/all --fail-on never --reports minimal", env={"PYTHONHASHSEED": "5"}),
                 Step(f'{DATA} --own-namespace {OWN_DATA} --out-dir {{work}}/own --fail-on never --reports minimal',
                      env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/own/full_results.csv")],
          check=checks(by_version((0, 24, 0), totals(1, 548, 66, 363, 119),
                                   by_version((0, 23, 0), totals(1, 549, 67, 363, 119),
                                              totals(1, 550, 68, 363, 119))),
                       by_version((0, 24, 0), totals(2, 54, 12, 40, 2), totals(2, 55, 13, 40, 2)),
                       _rea("own/full_results.csv", ["REA-021"], ["REA-022"])),
          checks="unscoped 550 (68 V, 363 W, 119 I) at 0.22.0; 549 (67 V) from 0.23.0, without the false REA-020; "
                 "548 (66 V) from 0.24.0, which reports one contradiction once instead of twice. Scoped to "
                 "https://acme.example.org/: 55 (13 V, 40 W, 2 I) up to 0.23.0 and 54 (12 V) from 0.24.0, with "
                 "REA-021 throughout",
          needs=["tarka-cli"]),

    Claim("C10.19", "54 when HermiT does not run, and from 0.24.0 the scoped report says so", "10",
          (F, "That run gave 55 three times running. The fourth time it gave 54."), "run",
          steps=[Step(TRIPLIFY),
                 Step(f"python scripts/without_java.py {DATA} --out-dir {{work}}/all --fail-on never --reports minimal",
                      env={"PYTHONHASHSEED": "0"}),
                 Step(f"python scripts/without_java.py {DATA} --own-namespace {OWN_DATA} --out-dir {{work}}/own "
                      f"--fail-on never --reports minimal", env={"PYTHONHASHSEED": "0"})],
          check=checks(by_version((0, 24, 0), totals(2, 54, 11, 40, 3), totals(2, 54, 12, 40, 2)),
                       _rea("all/full_results.csv", ["REA-022"], ["REA-021"]),
                       by_version((0, 24, 0), _rea("own/full_results.csv", ["REA-022"], ["REA-021"]),
                                  _rea("own/full_results.csv", [], ["REA-021", "REA-022"]))),
          checks="with HermiT unable to run: the unscoped run reports REA-022 on every version. The scoped run "
                 "holds 54 findings on both sides of the fix, but differently -- up to 0.23.0 it had neither "
                 "REA-021 nor REA-022 (54 = 12 V, 40 W, 2 I), and from 0.24.0 it reports REA-022 "
                 "(54 = 11 V, 40 W, 3 I): one Violation fewer, because the duplicated LOG-001 is merged, and one "
                 "Info more, because the reasoner's caveat survives the filter. The total is the same number for "
                 "two different reasons, which is why a gate should assert on the severity split",
          scripts=["scripts/without_java.py"],
          needs=["tarka-cli"],
          notes="The manual's 'three times… the fourth time' describes unpinned runs. Java is hidden here so that "
                "the reasoner's failure is certain; C14.06 shows how the hash seed decides it when Java is present."),

    Claim("C10.20", "Real defects: every worksIn target is untyped and dangling", "10",
          (F, "**Real data defects.** The largest group:"), "run",
          steps=[Step(TRIPLIFY),
                 Step(f'{DATA} --own-namespace {OWN_DATA} --out-dir {{work}}/own --fail-on never --reports minimal',
                      env={"PYTHONHASHSEED": "5"}),
                 Step("python scripts/summarise_findings.py {work}/own/full_results.csv --by focus --check STR-006"),
                 Step("python scripts/summarise_findings.py {work}/own/full_results.csv --by focus --check CNF-005")],
          check=checks(_mailbox_split("own/full_results.csv"),
                       _focus("own/full_results.csv", "CNF-005", [OWN + "Contractor", OWN + "Department"]),
                       _focus("own/full_results.csv", "QUA-001", [OWN + "hasSkill"]),
                       _focus("own/full_results.csv", "STY-002", [OWN + "reports_to"]),
                       _focus("own/full_results.csv", "STR-003", [OWN + "reports_to"]),
                       lambda r: ok(any("acme.example.org/ns/Contractor is unsatisfiable (equivalent to owl:Nothing) "
                                        "according to the hermit reasoner" in x["message"]
                                        for x in rows(r.file("own/full_results.csv"))),
                                    "REA-021's message reads as quoted", "REA-021 message differs")),
          checks="STR-006 and DAT-002 each fire 10 times, five on departments and five on mailboxes; CNF-005 on "
                 "Contractor (and Department); the inherited schema findings on hasSkill and reports_to; REA-021's "
                 "message as quoted",
          needs=["tarka-cli"]),

    Claim("C10.21", "Half the defects are mailboxes", "10",
          (F, "Read the list to the end, though. Of the ten of each, five are the departments."), "run",
          same_as="C10.20"),

    Claim("C10.22", "CNF-005: Contractor never populated", "10",
          (F, "Nothing is wrong. `acme:Contractor` is declared and this extract has no"), "run", same_as="C10.20"),

    Claim("C10.23", "REA-021 confirms LOG-001 by a different route", "10",
          (F, "When HermiT starts, the scoped run carries one extra finding:"), "run", same_as="C10.20"),

    Claim("C10.24", "The suite's walkthrough called it environment-flaky", "10",
          (F, "Whether it turns up is decided by Python's hash seed."), "source",
          sources=[src("suite docs/ACME_ROBOTICS_WALKTHROUGH.md", file("suite", "docs/ACME_ROBOTICS_WALKTHROUGH.md", "73"),
                       "occasionally environment-flaky")],
          notes="The seed mechanism is reproduced in C14.06."),

    Claim("C10.25", "--sample caps the reasoning pass", "10",
          (F, "For a data graph too large to reason over in full, `--sample N` caps the"), "run",
          steps=[Step(f"{SUITE} data --help")],
          check=has(0, "--sample SAMPLE", "cap the reasoning pass to a CBD sample of this many"),
          checks="`data --help` documents --sample as a cap on the reasoning pass"),

    Claim("C10.26", "CT-32 to CT-38: when every file is right and the set is wrong", "10",
          (F, "The testing repository's competency questions 32 to 38 are about exactly this:"), "source",
          sources=[src("testing repo commit 1370f6c", commit("testing", "1370f6c5362501c91a584bb1f3fe022720ed4357")),
                   src("testing repo drift.py (CT-34, 35, 36, 38)",
                       file("testing", "experiments/SpecificTests/AGGREGATE-mapping-drift/drift.py", "1-9"),
                       "CT-34, CT-35, CT-36, CT-38 -- drift across a *set* of mappings.")]),

    Claim("C10.27", "CT-32's mapping is wired to no CSV", "10",
          (F, "CT-32 taught me something."), "source",
          sources=[src("testing repo CT-32 README",
                       file("testing", "experiments/SpecificTests/CT-32-property-outside-its-domain/README.md"),
                       "This mapping is wired to no CSV, which settles the argument.")]),

    Claim("C10.28", "tq:PrefixBinding and the per-file sketch dataset", "10",
          (F, "The suite now publishes two facts that make set-level questions a query rather"), "run",
          data=["data/mapping-set/people.rq", "data/mapping-set/payroll.rq", "data/mapping-set/legacy.rq",
                "data/queries/prefix-conflicts.rq"],
          scripts=["scripts/sketch_dataset.py"],
          steps=[Step(f"{SUITE} sketch --queries data/mapping-set --out-dir {{work}}/ms --reports minimal --fail-on never"),
                 Step("python scripts/query_file.py {work}/ms/bind-facts.ttl @data/queries/prefix-conflicts.rq"),
                 Step("python scripts/sketch_dataset.py data/mapping-set")],
          check=checks(has(1, "acme,2,legacy.rq, payroll.rq, people.rq"),
                       has(2, "payroll.rq     https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasEmployeeId",
                           "people.rq      https://acme.example.org/ns/Employee  https://acme.example.org/ns/hasSkill")),
          checks="a GROUP BY over the tq:PrefixBinding facts finds acme: bound to two namespaces across the three "
                 "files; the per-file dataset shows acme:Employee built with hasEmployeeId by one file and hasSkill "
                 "by another"),

    Claim("C10.29", "The merged sketch and one prefix bound two ways: odd file first", "10",
          (F, "> **And one thing the merged sketch got wrong, until 0.23.0.**"), "run",
          data=["data/mapping-set/people.rq", "data/mapping-set/payroll.rq", "data/mapping-set/legacy.rq"],
          steps=[Step(f"{SUITE} sketch --queries data/mapping-set --ontology {V1} --import-dir {ACME} "
                      f"--out-dir {{work}}/three --reports minimal --fail-on never"),
                 Step("python scripts/summarise_findings.py {work}/three/full_results.csv --by focus --check CNF-001"),
                 Step("python scripts/summarise_findings.py {work}/three/full_results.csv --by focus --check CNF-002"),
                 Step(f"{SUITE} sketch --queries data/mapping-set --query-pattern people.rq,payroll.rq "
                      f"--ontology {V1} --import-dir {ACME} --out-dir {{work}}/two --reports minimal --fail-on never")],
          check=checks(
              by_version(
                  (0, 23, 0),
                  checks(lambda r: ok("each file is read with its own definition" in r[0].stderr,
                                      "the warning says each file is read with its own definition",
                                      "no such warning on stderr"),
                         has(1, "focus=https://acme.example.org/ns#Department"), lacks(1, "ns#Employee"),
                         lacks(2, "ns#hasSkill", "ns#hasEmployeeId"),
                         _focus_includes("three/full_results.csv", "CNF-005", OWN + "Employee", False)),
                  checks(lambda r: ok("prefix 'acme:' redefined" in r[0].stderr and "keeping first definition" in r[0].stderr,
                                      "the warning is on stderr", "no redefinition warning on stderr"),
                         has(1, "focus=https://acme.example.org/ns#Employee"),
                         has(2, "focus=https://acme.example.org/ns#hasSkill", "focus=https://acme.example.org/ns#hasEmployeeId"),
                         _focus_includes("three/full_results.csv", "CNF-005", OWN + "Employee", True))),
              counts("two/full_results.csv", {"CNF-001": None, "CNF-002": None}, exact=False),
              _focus_includes("two/full_results.csv", "CNF-005", OWN + "Employee", False)),
          checks="with legacy.rq sorting first. At 0.22.0 the merged sketch reports acme:Employee, hasSkill and "
                 "hasEmployeeId as undeclared in the hash namespace and acme:Employee as never populated. From 0.23.0 "
                 "it reports only legacy.rq's own acme:Department, in the hash namespace where it was written, and "
                 "acme:Employee is populated. The two correct files on their own are clean on both"),
    Claim("C10.30", "The merged sketch and one prefix bound two ways: odd file last", "10",
          (F, "It cuts the other way too, which is worse."), "run",
          data=["data/mapping-set/people.rq", "data/mapping-set/payroll.rq", "data/mapping-set/legacy.rq"],
          steps=[Step("python scripts/copy_tree.py data/mapping-set/people.rq {work}/last/people.rq"),
                 Step("python scripts/copy_tree.py data/mapping-set/payroll.rq {work}/last/payroll.rq"),
                 Step("python scripts/copy_tree.py data/mapping-set/legacy.rq {work}/last/zz-legacy.rq",
                      note="the same older mapping, renamed so that it sorts last"),
                 Step(f"{SUITE} sketch --queries {{work}}/last --ontology {V1} --import-dir {ACME} "
                      f"--out-dir {{work}}/out --reports minimal --fail-on never"),
                 Step("python scripts/summarise_findings.py {work}/out/full_results.csv --by focus --check CNF-001")],
          check=checks(
              lambda r: ok("zz-legacy.rq" in r[3].stderr, "the warning names zz-legacy.rq, on stderr",
                           "no warning about zz-legacy.rq"),
              by_version(
                  (0, 23, 0),
                  checks(_focus_includes("out/full_results.csv", "CNF-001", "https://acme.example.org/ns#Department", True),
                         lambda r: ok("@prefix acme: <https://acme.example.org/ns#> ." in
                                      r.file("out/sketch.ttl").read_text(encoding="utf-8").split("# source: zz-legacy.rq")[1],
                                      "sketch.ttl re-declares acme: ahead of zz-legacy.rq's triples",
                                      "no re-declaration ahead of zz-legacy.rq")),
                  checks(counts("out/full_results.csv", {"CNF-001": None, "CNF-002": None}, exact=False),
                         lambda r: ok("ns#" not in r.file("out/sketch.ttl").read_text(encoding="utf-8").split("# source")[1],
                                      "sketch.ttl reads zz-legacy.rq's acme:Department in the ontology's namespace",
                                      "sketch.ttl does not show the misreading")))),
          checks="with the hash-namespace file sorting last. At 0.22.0 the run reports no CNF-001 or CNF-002 at all: "
                 "its acme:Department is read in the ontology's own namespace, and a warning on stderr is the only "
                 "trace. From 0.23.0 its acme:Department is reported in the hash namespace, in this order as in the "
                 "other, because the sketch re-declares each file's prefixes ahead of its triples"),
]
