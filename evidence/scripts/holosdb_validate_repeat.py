"""Chapter 13 §13.2: does validation leave the store as it found it?

    python scripts/holosdb_validate_repeat.py DATA SHAPES work/C13_10/store

Up to holosdb 0.21.0, Store.validate() loaded the shapes into a named graph of
the store it validated and never removed them. A shape's blank nodes are fresh
on every load, so each call added another copy and the count climbed; on a
persistent store the copies survived a restart. 0.21.1 loads them in a scope
that is always rolled back, and reports a shapes graph an earlier version left
behind, naming the DROP GRAPH that removes it, rather than reading or dropping it.

1. three calls with each engine on one in-memory store, and their counts;
2. the named graphs the store holds after one call;
3. the same on a persistent store, after reopening it;
4. a store already holding a leftover urn:holos:python:shapes graph: what the
   call warns, and whether the leftover is still there afterwards.
"""
import sys
import warnings
from importlib import metadata

from holosdb import Store

sys.stdout.reconfigure(encoding="utf-8")
data, shapes, path = sys.argv[1:4]
GRAPHS = "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g ORDER BY ?g"
LEFTOVER = "urn:holos:python:shapes"


def graphs(store):
    return [(r.to_dict()["g"], int(r.to_dict()["n"])) for r in store.query(GRAPHS)]


print(f"holosdb {metadata.version('holosdb')}")
for engine in ("adapted", "native"):
    store = Store()
    store.load(data)
    counts = [store.validate(shapes, engine=engine)["violations"] for _ in range(3)]
    print(f"1. {engine}, three calls on one store: violations {counts}")

store = Store()
store.load(data)
store.validate(shapes)
print(f"2. named graphs after one validate(): {graphs(store)}")

disk = Store(path=path)
disk.load(data)
disk.validate(shapes)
del disk
print(f"3. named graphs in the persistent store after reopening: {graphs(Store(path=path))}")

store = Store()
store.load(data)
store.update(f"INSERT DATA {{ GRAPH <{LEFTOVER}> {{ <urn:x:s> <urn:x:p> <urn:x:o> }} }}")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    result = store.validate(shapes)
said = [f"{w.category.__name__}: {w.message}" for w in caught] or ["no warning"]
print(f"4. with a leftover {LEFTOVER} graph: violations {result['violations']}; {' | '.join(said)}")
print(f"   named graphs afterwards: {graphs(store)}")
