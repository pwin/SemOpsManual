"""Chapter 6 — Stages and stories."""
from ._common import Claim

F = "docs/06-stages-and-stories.md"

CLAIMS = [
    Claim("C06.01", "One practice, three frameworks", "06",
          (F, "The SemOps strategy material describes the same practice three times, from three"), "argument",
          notes="A reading of the SemOps strategy material, which the manual takes as given. The mapping from each "
                "stage to commands is evidenced chapter by chapter in Part III."),
]
