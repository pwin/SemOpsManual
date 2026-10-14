"""Chapter 13 §13.2: validation writes the shapes into the store, and leaves them.

    python scripts/holosdb_validate_repeat.py DATA SHAPES work/C13_10/store

1. On one in-memory store, validates three times with each engine and prints
   the violation counts. They grow, because each call loads another copy of
   the shapes: a shape's blank nodes are fresh every time.
2. Prints the named graphs the store holds after one validation.
3. On a persistent store at the given path, validates once, reopens the store
   and prints its named graphs again.
"""
import sys

from holosdb import Store

sys.stdout.reconfigure(encoding="utf-8")
data, shapes, path = sys.argv[1:4]
GRAPHS = "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g ORDER BY ?g"


def graphs(store):
    return [(r.to_dict()["g"], int(r.to_dict()["n"])) for r in store.query(GRAPHS)]


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
