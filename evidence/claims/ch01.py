"""Chapter 1 — The business case."""
from ._common import Claim, Step, has

F = "docs/01-the-business-case.md"

CLAIMS = [
    Claim("C01.01", "Ten systems, forty-five pairings; twenty, a hundred and ninety", "01",
          (F, "mappings. Ten systems is forty-five potential pairings; twenty is a hundred and"), "run",
          scripts=["scripts/pairings.py"],
          steps=[Step("python scripts/pairings.py 10 20")],
          check=has(0, "10 systems: 45 potential point-to-point pairings",
                    "20 systems: 190 potential point-to-point pairings"),
          checks="n(n−1)/2 gives 45 for 10 systems and 190 for 20"),
    Claim("C01.02", "An ontology decays without deliberate maintenance", "01",
          (F, "**An ontology is most accurate the day it ships. Every day after that, without"), "argument",
          notes="A judgement from practice. Chapter 14 §14.5 gives the observable form, the Warning trend in retained "
                "full_results.csv files, and C09.10 shows the file each run writes."),
]
