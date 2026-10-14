"""Chapter 4 — From research to industry."""
from ._common import Claim, file, src

F = "docs/04-from-research-to-industry.md"

CLAIMS = [
    Claim("C04.01", "REA-022 carries owlready2's internal error", "04",
          (F, "> The external DL reasoner ('hermit') could not be run: `cannot access local"), "run",
          same_as="C14.06",
          notes="C14.06's record lists the REA-022 messages its seed-0 runs produced. 'Five runs of ten' describes "
                "this edition's unpinned runs."),
    Claim("C04.02", "The failure is in owlready2's loader, not HermiT", "04",
          (F, "Reading the traceback for this edition showed something else: owlready2's *loader*"), "run",
          same_as="C14.08"),
    Claim("C04.03", "Without Java, the operating system's message; LOG-001 regardless", "04",
          (F, "**Java runtime** HermiT runs in. Hide Java and `REA-022` says so in different"), "run",
          same_as="C14.09",
          notes="That owlready2 installs with the suite is C07.05; LOG-001 without any reasoner is C08.17."),
    Claim("C04.04", "A perfect SHACL score broke production; 0.3.1 took 425", "04",
          (F, "The SHACL engine passed all 426 W3C tests for a few days at 0.3.0, by enforcing one"), "source",
          same_as="C11.08"),
    Claim("C04.05", "HOLOS reports correctness and coverage: 512 of 512, 82%", "04",
          (F, "HOLOS reports its W3C results as **two numbers, because either alone misleads**:"), "source",
          sources=[src("HOLOS README, conformance table", file("holos", "README.md", "122"),
                       "| SPARQL 1.1 | **512/512** · 100% | 512/625 · **82%** |"),
                   src("HOLOS README, tests not yet run", file("holos", "README.md", "155"),
                       "| SPARQL 1.1 | **512 / 512** | 0 | 113 | **0** |"),
                   src("HOLOS README, the withdrawn target", file("holos", "README.md", "106"),
                       "it was written before anything was measured")]),
    Claim("C04.06", "A research artefact's implicit expiry date", "04",
          (F, "an implicit expiry date that does not appear anywhere in its README."), "argument",
          notes="A judgement about maintenance models, not a measurement."),
]
