"""Chapter 3 — Across the boundary."""
from ._common import ACME, SUITE, V1, Claim, Step, checks, has, ok, rows

F = "docs/03-across-the-boundary.md"
FOAF = f"{ACME}/reference_vocab/foaf.rdf"


def _no_foaf_name_conformance(r):
    hits = [x["check_id"] for x in rows(r.file("data/full_results.csv"))
            if x["check_id"].startswith("CNF") and "xmlns.com/foaf/0.1/name" in (x["path"] + x["value"] + x["message"])]
    return ok(not hits, "no conformance finding concerns foaf:name", f"conformance findings on foaf:name: {hits}")


CLAIMS = [
    Claim("C03.01", "foaf:name has domain owl:Thing, and the suite has been taught it", "03",
          (F, "The classic case is FOAF, which deliberately declares `foaf:name` with"), "run",
          steps=[Step(f'python scripts/query_file.py {FOAF} "SELECT ?domain WHERE {{ <http://xmlns.com/foaf/0.1/name> '
                      f'<http://www.w3.org/2000/01/rdf-schema#domain> ?domain }}"'),
                 Step(f"tarka run -q {ACME}/employees.rq -i {ACME}/employees.csv -o {{work}}/employees.ttl"),
                 Step(f"python scripts/without_java.py {SUITE} data {{work}}/employees.ttl --ontology {V1} "
                      f"--import-dir {ACME} --engine sparql --out-dir {{work}}/data --fail-on never --reports minimal")],
          check=checks(has(0, "http://www.w3.org/2002/07/owl#Thing"), _no_foaf_name_conformance),
          checks="FOAF declares foaf:name's domain as owl:Thing; the unscoped data run over the acme employees reports "
                 "no conformance finding about foaf:name",
          needs=["tarka-cli"]),
    Claim("C03.02", "version-diff says MAJOR, with the machine-readable diff", "03",
          (F, "**The bump decision must be evidence-based, not a judgement call.**"), "run", same_as="C12.01"),
    Claim("C03.03", "The tombstone is read in both directions", "03",
          (F, "Earlier editions of this manual told you that the suite's rename detection read this"), "run",
          same_as="C12.05"),
    Claim("C03.04", "Policy at the scan for a consortium", "03",
          (F, "knowing even though the component is young. A store that enforces access policy **at"), "run",
          same_as="C13.06"),
    Claim("C03.05", "A registry is a distributable artefact", "03",
          (F, "- Publish your SHACL shapes and check registry as files, not as prose in a PDF. The"), "run",
          same_as="C08.25"),
    Claim("C03.06", "Speak the protocol, not the product", "03",
          (F, "One last design lesson, which I took from the triplifier rather than from a"), "run",
          same_as="C10.15",
          notes="tarka's own reasoning is in its commit "
                "[26f256a](https://github.com/pwin/tarka/commit/26f256a28f10d299a4cf1c5dd49ba52cd37122a7) (C10.16)."),
]
