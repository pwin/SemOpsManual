"""Chapter 11 §11.2: the RDFS closure, handed out by the SHACL engine (0.3.3).

    python scripts/rdfs_closure.py data/shacl/rdfs/data.ttl

1. Closes the given document with shacl.rdfs_closure and prints what it gained.
2. Closes a two-triple document in which a property with a declared range has a
   literal value. rdfs3 entails that the literal is an instance of the range,
   which RDF cannot write; the closure drops it.
3. Says whether anything was typed rdfs:Resource (the rule the engine leaves out).
"""
import sys

import shacl
from rdflib import RDF, RDFS, Graph, Literal

sys.stdout.reconfigure(encoding="utf-8")


def graph(text):
    g = Graph()
    g.parse(data=text, format="turtle")
    return g


source = open(sys.argv[1], encoding="utf-8").read()
before, after = graph(source), graph(shacl.rdfs_closure(source))
print(f"1. {sys.argv[1]}: {len(before)} triples, {len(after)} after the closure; gained:")
for s, p, o in sorted(set(after) - set(before)):
    print(f"   {s.n3()} {p.n3()} {o.n3()}")

ranged = """@prefix ex: <http://example.org/> . @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:email rdfs:range ex:Address . ex:dave ex:email "dave@example.com" ."""
closed = graph(shacl.rdfs_closure(ranged))
typed_literal = any(isinstance(s, Literal) for s, _, _ in closed.triples((None, RDF.type, None)))
print(f"2. a ranged property with a literal value: {len(closed)} triples after the closure; "
      f"literal typed as the range: {typed_literal}")
resource = len(list(after.triples((None, RDF.type, RDFS.Resource)))) + len(list(closed.triples((None, RDF.type, RDFS.Resource))))
print(f"3. triples typing something rdfs:Resource: {resource}")
