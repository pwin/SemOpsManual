"""Chapter 11 §11.3: a rule's output, validated, gives one result per source instance.

    python scripts/rule_scale.py 1000 100000

For each size N, generates N instances of ex:Person, a rule typing every Person
as an ex:Party, and a shape requiring every Party to have an ex:partyId, which
none has. With rules applied there should be exactly N results, one per focus
node, with no misses and no duplicates; without them, none. Uses the shacl
package (the same engine as the CLI). Times are printed, not asserted.
"""
import os
import sys
import tempfile
import time

import shacl

sys.stdout.reconfigure(encoding="utf-8")

SHAPES = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix ex: <http://example.org/> .
ex:PersonRules a sh:NodeShape ; sh:targetClass ex:Person ;
  sh:rule [ a sh:TripleRule ; sh:subject sh:this ; sh:predicate rdf:type ; sh:object ex:Party ] .
ex:PartyShape a sh:NodeShape ; sh:targetClass ex:Party ;
  sh:property [ sh:path ex:partyId ; sh:minCount 1 ] .
"""

with tempfile.TemporaryDirectory() as tmp:
    shapes_path = os.path.join(tmp, "shapes.ttl")
    with open(shapes_path, "w", encoding="utf-8") as f:
        f.write(SHAPES)
    shapes = shacl.Shapes.from_file(shapes_path)
    for n in (int(a) for a in sys.argv[1:]):
        data_path = os.path.join(tmp, f"people-{n}.nt")
        with open(data_path, "w", encoding="utf-8") as f:
            for i in range(n):
                f.write(f"<http://example.org/p{i}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                        f"<http://example.org/Person> .\n")
        t0 = time.perf_counter()
        with_rules = shapes.validate_file(data_path, inference="rules")
        t1 = time.perf_counter()
        without = shapes.validate_file(data_path)
        foci = {str(r.focus_node) for r in with_rules.results}
        print(f"N={n:>7,}  with rules: {len(with_rules.results):>7,} results on {len(foci):>7,} distinct focus nodes "
              f"({t1 - t0:.2f} s)  without rules: {len(without.results)} results")
