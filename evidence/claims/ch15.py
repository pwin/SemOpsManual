"""Chapter 15 — Adoption roadmap."""
from ._common import Claim

F = "docs/15-adoption-roadmap.md"

CLAIMS = [
    Claim("C15.01", "479 unscoped, 23 scoped, four false with --exclude-imports", "15",
          (F, "**Do not skip `--own-namespace`.** Unscoped, the fixture in this manual produces 479"), "run",
          same_as="C09.04",
          notes="479 is C09.02, the four false findings C09.03, the 23 every time C09.04."),
    Claim("C15.02", "--output-data is not optional", "15",
          (F, "Two things are not optional in practice. `--output-data` is one: without it,"), "run",
          same_as="C12.12"),
    Claim("C15.03", "PYTHONHASHSEED for docgen", "15",
          (F, "Publish it. The `PYTHONHASHSEED` is a workaround, not decoration. Without it"), "run",
          same_as="C13.12"),
]
