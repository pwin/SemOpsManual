"""Chapter 14 §14.4: what HermiT itself says about an ontology, through owlready2.

    python scripts/hermit_verdict.py FILE [FILE ...]

Merges the files, loads them into owlready2 as the suite's bridge does, runs
HermiT, and prints whether it found the ontology inconsistent and which classes
it found unsatisfiable. Needs Java. The suite turns `owl:Nothing` in that list
into REA-020, "the ontology is inconsistent"; this shows what HermiT reported.
"""
import sys
import tempfile
from pathlib import Path

import owlready2
from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
g = Graph()
for f in sys.argv[1:]:
    g.parse(f)
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "ontology.owl"
    g.serialize(destination=str(path), format="xml")
    world = owlready2.World()
    onto = world.get_ontology(str(path)).load()
    try:
        with onto:
            owlready2.sync_reasoner(world, infer_property_values=True)
        print("HermiT: consistent (no OwlReadyInconsistentOntologyError)")
    except owlready2.OwlReadyInconsistentOntologyError:
        print("HermiT: INCONSISTENT")
        sys.exit()
    unsat = [getattr(c, "iri", str(c)) for c in world.inconsistent_classes()]
    print("unsatisfiable classes:", sorted(unsat) or "none")
    print("owl:Nothing among them:", "http://www.w3.org/2002/07/owl#Nothing" in unsat)
