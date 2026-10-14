"""Chapter 5 — GenAI and agents."""
from ._common import Claim, file, src

F = "docs/05-genai-and-agents.md"

CLAIMS = [
    Claim("C05.01", "Grounding in graphs improves step-wise reasoning and recall", "05",
          (F, "- Grounding each individual reasoning *step* against graph-structured data, rather"), "argument",
          notes="Reported results from the literature in the chapter's references; not reproduced here."),
    Claim("C05.02", "findings.txt is addressed to a person or an agent", "05",
          (F, "addressed, in its own documentation, to \"a person at a terminal, or an agent\"."), "source",
          sources=[src("suite docs/REPORTS.md", file("suite", "docs/REPORTS.md", "8"),
                       "a person at a terminal, or an agent")],
          notes="The '[a blank node]' fix it mentions is C07.07 and C07.09."),
    Claim("C05.03", "Tombstones at 100% apply; guesses at 57% do not", "05",
          (F, "an explicit tombstone comes in at 100% and applies; the same rename guessed from"), "run",
          same_as="C12.05"),
    Claim("C05.04", "An agent as a principal with roles", "05",
          (F, "service account that reads and writes everything. A store that enforces policy at the"), "run",
          same_as="C13.06"),
]
