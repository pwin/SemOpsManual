"""Chapter 10 §10.6: ask a per-file question of a set of mappings.

    python scripts/sketch_dataset.py data/mapping-set

Builds the suite's per-file sketch dataset (each query file's CONSTRUCT
template in a named graph named after the file; the union in the default
graph) and asks, for each class, which properties each file builds it with.
One class built with different properties by different files is invisible in
the merged sketch, where the two descriptions simply add up.
"""
import sys

from ontology_suite.sketch.prefix_alignment import build_sketch_dataset

sys.stdout.reconfigure(encoding="utf-8")

ds = build_sketch_dataset([sys.argv[1]])
q = """
SELECT ?file ?class ?property WHERE {
  GRAPH ?g { ?s a ?class ; ?property ?o . FILTER(?property != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) }
  BIND(REPLACE(STR(?g), "^.*/", "") AS ?file)
} ORDER BY ?class ?file ?property
"""
for row in ds.query(q):
    print(f"{row.file:14} {row['class']}  {row.property}")
print(f"named graphs: {sorted(str(g.identifier).rsplit('/', 1)[-1] for g in ds.graphs() if str(g.identifier).endswith('.rq'))}")
