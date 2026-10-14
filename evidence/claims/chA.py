"""Appendix A — Diagram and brand conventions."""
from ._common import Claim, Step, has

F = "docs/diagram-style.md"

CLAIMS = [
    Claim("CA.01", "All six fills clear 12:1 against the text colour", "A",
          (F, "- Palette contrast: all six fills carry the `#14243A` text colour at a contrast"), "run",
          scripts=["scripts/contrast.py"],
          steps=[Step("python scripts/contrast.py")],
          check=has(0, "lowest 13.09:1"),
          checks="the lowest WCAG 2 contrast ratio of the six fills against #14243A is 13.09:1"),
    Claim("CA.02", "FOAF is published as RDF/XML", "A",
          (F, "real-world vocabularies (FOAF among them, as Chapters"), "argument",
          notes="The fixture's copy is `fixtures/acme_robotics/reference_vocab/foaf.rdf`, parsed as RDF/XML in C03.01 "
                "and C14.06."),
]
