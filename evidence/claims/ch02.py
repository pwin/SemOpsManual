"""Chapter 2 — People and cognition."""
from ._common import Claim, Step, has

F = "docs/02-people-and-cognition.md"

CLAIMS = [
    Claim("C02.01", "Building the vocabulary exposes fracture lines", "02",
          (F, "exposes fracture lines that were already in the organisation"), "argument",
          notes="From the author's Semantic Arts article 'Team Building — The Importance of an Ontology', cited in the "
                "chapter's references. Experience, not measurement."),
    Claim("C02.02", "Organisations move from labels to verbs", "02",
          (F, "There is a pattern across whole organisations, not just individuals, and it is worth"), "argument",
          notes="From the author's Semantic Arts article 'From Labels to Verbs — Child's Play!', cited in the "
                "chapter's references."),
    Claim("C02.03", "gist 14.1.0: 42 of 66 object properties constrain neither; gist 13: 40 of 63", "02",
          (F, "current release, gist 14.1.0, 42 of its 66 object properties constrain neither;"), "run",
          scripts=["scripts/gist_properties.py"],
          steps=[Step("python scripts/gist_properties.py 14.1.0 13.0.0")],
          check=has(0, "gist 14.1.0: 66 object properties", "neither 42", "gist 13.0.0: 63 object properties",
                    "neither 40"),
          checks="gist 14.1.0 has 66 object properties, 42 with neither domain nor range; gist 13.0.0 has 63, 40",
          needs=["network"],
          notes="Downloads the two releases from Semantic Arts' GitHub; nothing of gist is copied into this folder."),
    Claim("C02.04", "479 findings, 23 once scoped", "02",
          (F, "FOAF imports resolved produces **479 findings**. Adding a single flag that scopes"), "run",
          same_as="C09.04"),
]
