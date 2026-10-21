"""The README."""
from ._common import Claim, Step, has

F = "README.md"

CLAIMS = [
    Claim("C00.01", "A 61-check registry", "00",
          (F, "The gate: a Python CLI and library with the 61-check registry"), "run", same_as="C07.03"),
    Claim("C00.02", "Every Part III command was executed, and re-run for this edition", "00",
          (F, "Every command shown in Part III was **executed for real**"), "argument",
          notes="A statement of method. This folder is the re-run: each `run` claim records the date it last ran, "
                "and the environment table at the top of EVIDENCE.md gives the versions."),
    Claim("C00.03", "Twenty diagrams", "00",
          (F, "numbers, all twenty diagrams rendered, and an index of commands, flags and check"), "run",
          scripts=["scripts/count_mermaid.py"],
          steps=[Step("python scripts/count_mermaid.py ..")],
          check=has(0, "19 diagrams in the chapters; README has 1 more"),
          checks="19 Mermaid blocks across the chapters and the appendix, and the README's own, which the PDF "
                 "keeps in its introduction: twenty",
          notes="The previous wording said nineteen, which counted the chapters and not the PDF."),
    Claim("C00.04", "pip install shacl gives the library only", "00",
          (F, "`pip install shacl`"), "run", same_as="C07.05"),
    Claim("C00.05", "54 or 55, and REA-021 or REA-022", "00",
          (F, "**Two outputs move unless you pin one variable, and both are labelled where they"), "run",
          same_as="C10.18",
          notes="The 54 is C10.19; the hash seed's part, and the residual it does not control, are C14.06 and C14.08; "
                "docgen's reshuffling is C13.12."),
    Claim("C00.06", "Everything else is exactly reproducible", "00",
          (F, "Everything else is exactly reproducible across repeated runs, and survived a change of the engine"),
          "run", same_as="C09.02",
          notes="C09.02 runs the unscoped gate three times; C07.02 compares the figures with the previous edition's, "
                "measured on rdflib and pyshacl."),
]
