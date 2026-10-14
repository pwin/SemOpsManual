"""Rewrite the migration tombstone in a copy of acme-org-v2.ttl.

    python scripts/rewrite_tombstone.py work/X/acme/acme-org-v2.ttl MODE

MODE is one of:
  equivalent-reversed   acme:SoftwareEngineer owl:equivalentClass acme:Engineer .
  replaced-by           acme:Engineer dcterms:isReplacedBy acme:SoftwareEngineer .
  replaced-by-reversed  acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer .

The fixture asserts `acme:Engineer owl:equivalentClass acme:SoftwareEngineer .`
(from the retiring IRI). Only that one line is changed.
"""
import sys
from pathlib import Path

ORIGINAL = "acme:Engineer owl:equivalentClass acme:SoftwareEngineer ."
DC = "@prefix dcterms: <http://purl.org/dc/terms/> .\n"
MODES = {
    "equivalent-reversed": "acme:SoftwareEngineer owl:equivalentClass acme:Engineer .",
    "replaced-by": DC + "acme:Engineer dcterms:isReplacedBy acme:SoftwareEngineer .",
    "replaced-by-reversed": DC + "acme:SoftwareEngineer dcterms:isReplacedBy acme:Engineer .",
}
path, mode = Path(sys.argv[1]), sys.argv[2]
text = path.read_text(encoding="utf-8")
lines = text.split("\n")
hits = [i for i, l in enumerate(lines) if l.strip() == ORIGINAL]
if len(hits) != 1:
    sys.exit(f"expected exactly one tombstone line, found {len(hits)}")
lines[hits[0]] = MODES[mode]
path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(f"line {hits[0] + 1} now reads: {MODES[mode].splitlines()[-1]}")
