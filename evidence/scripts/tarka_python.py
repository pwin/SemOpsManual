"""Chapter 10: tarka through the tarka-rdf package (no command line needed).

    python scripts/tarka_python.py fixtures/acme_robotics data/ottr work/C10_xx

  1. the acme TARQL mapping, run with Mapping.tarql_file(...).run_csv(...)
  2. the same mapping as OTTR templates, compared triple for triple
  3. the OTTR library without its `mailto:` prefix (since 0.2.0, the mailboxes are full
     IRIs, as in bOTTR), and a mailbox that is not an IRI: a ValueError, the rest written
  4. the acme CSV as a Polars data frame, written to Parquet, and mapped from it
  5. the shapes tarka derives from the TARQL mapping
  6. a Polars integer column into an xsd:integer OTTR parameter: a typed literal
"""
import sys
from pathlib import Path

import polars as pl
import tarka_rdf

sys.stdout.reconfigure(encoding="utf-8")
acme, ottr, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)


def lines(p: Path):
    return sorted(l for l in p.read_text(encoding="utf-8").splitlines() if l.strip())


tarql = tarka_rdf.Mapping.tarql_file(str(acme / "employees.rq"))
tarql.run_csv(str(acme / "employees.csv"), str(work / "tarql.nt"), format="ntriples")
t = lines(work / "tarql.nt")
print(f"1. TARQL mapping: {len(t)} triples")

o = tarka_rdf.Mapping.ottr([str(ottr / "employees.stottr")], ["acme:Employee"])
o.run_csv(str(ottr / "employees-iri.csv"), str(work / "ottr.nt"), format="ntriples")
ot = lines(work / "ottr.nt")
print(f"2. OTTR templates: {len(ot)} triples; identical to the TARQL output: {ot == t}")

bad = tarka_rdf.Mapping.ottr([str(ottr / "employees-no-mailto-prefix.stottr")], ["acme:Employee"])
try:
    ret = bad.run_csv(str(ottr / "employees-iri.csv"), str(work / "ottr-no-prefix.nt"), format="ntriples")
    n = len(lines(work / "ottr-no-prefix.nt"))
    print(f"3. OTTR without the mailto: prefix: returned {ret!r}, raised nothing, wrote {n} triples")
except Exception as exc:
    print(f"3. OTTR without the mailto: prefix: raised {type(exc).__name__}: {exc}")
try:
    o.run_csv(str(ottr / "employees-bad-mbox.csv"), str(work / "ottr-bad-mbox.nt"), format="ntriples")
    print("   a mailbox that is not an IRI: raised nothing")
except ValueError as exc:
    n = len(lines(work / "ottr-bad-mbox.nt"))
    print(f"   a mailbox that is not an IRI: ValueError ({' / '.join(str(exc).splitlines())}); "
          f"the other rows written, {n} triples")

df = pl.read_csv(acme / "employees.csv")
df.write_parquet(work / "employees.parquet")
frame = tarql.triplify(df)
print(f"4. Polars frame of {df.height} rows -> {frame.height} triples; "
      f"Parquet written to {(work / 'employees.parquet').as_posix()}")

shapes = tarql.shapes()
(work / "employees.shapes.ttl").write_text(shapes, encoding="utf-8")
print("5. shapes derived from the mapping:")
print("\n".join("   " + l for l in shapes.splitlines() if "sh:path" in l or "NodeShape" in l))

counts = pl.DataFrame({"dept": ["https://acme.example.org/data/department/ENG",
                                "https://acme.example.org/data/department/QA"], "n": [42, 7]})
typed = tarka_rdf.Mapping.ottr([str(ottr / "headcount.stottr")], ["acme:Headcount"]).triplify(counts)
print(f"6. a {counts.schema['n']} column through an xsd:integer parameter:")
for subject, predicate, obj in typed.iter_rows():
    print(f"   {subject} {predicate} {obj}")
