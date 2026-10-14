"""Compare two RDF files as sets of triples (any syntax rdflib reads).

    python scripts/compare_ntriples.py A.ttl B.nt
"""
import sys

from rdflib import Graph
from rdflib.compare import isomorphic

sys.stdout.reconfigure(encoding="utf-8")
a, b = Graph(), Graph()
a.parse(sys.argv[1])
b.parse(sys.argv[2])
print(f"{sys.argv[1]}: {len(a)} triples")
print(f"{sys.argv[2]}: {len(b)} triples")
print("isomorphic:", isomorphic(a, b))
