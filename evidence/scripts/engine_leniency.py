"""Chapter 7 §7.1: why the suite stopped evaluating on rdflib.

    python scripts/engine_leniency.py

SPARQL 1.1 §17.4.2.5 defines STR() for literals and IRIs. STR() of a blank node
is a type error, so CONCAT errors and BIND leaves the variable unbound. This asks
three engines the question STY-003 used to ask: build a message from a labelled
anonymous restriction.

  rdflib      lenient: returns the blank node's internal identifier
  holosdb     conformant: the message is unbound
  pyoxigraph  conformant: the message is unbound (optional; skipped if absent)

Then two repairs. COALESCE(STR(?e), ...) only helps where STR() raises, so the
lenient engine still prints the internal identifier (Chapter 8 §8.5). The form
the registry now uses, IF(isBlank(...)), every engine answers the same way.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = """@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:   <http://example.org/> .
ex:Thing a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty ex:p ; owl:someValuesFrom ex:Thing ;
                    rdfs:label "an anonymous restriction" ] .
"""
UNGUARDED = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?msg WHERE { ?e rdfs:label ?l . FILTER(isBlank(?e))
  BIND(CONCAT("A label on ", STR(?e), " has no language tag.") AS ?msg) }"""
COALESCED = UNGUARDED.replace('STR(?e)', 'COALESCE(STR(?e), "[a blank node]")')
GUARDED = UNGUARDED.replace('STR(?e)', 'IF(isBlank(?e), "[a blank node]", STR(?e))')


def rdflib_answer(q):
    from rdflib import Graph
    g = Graph()
    g.parse(data=DATA, format="turtle")
    return [str(r.msg) if r.msg is not None else "(unbound)" for r in g.query(q)]


def holosdb_answer(q):
    import tempfile, os
    from holosdb import Store
    with tempfile.NamedTemporaryFile("w", suffix=".ttl", delete=False, encoding="utf-8") as f:
        f.write(DATA)
    try:
        s = Store()
        s.load(f.name)
        out = []
        for r in s.query(q):
            d = r.to_dict()
            out.append(str(d["msg"]) if d.get("msg") is not None else "(unbound)")
        return out
    finally:
        os.unlink(f.name)


def pyoxigraph_answer(q):
    import io
    import pyoxigraph as ox
    st = ox.Store()
    st.load(io.BytesIO(DATA.encode()), format=ox.RdfFormat.TURTLE)
    return [(r["msg"].value if r["msg"] is not None else "(unbound)") for r in st.query(q)]


for label, q in (("unguarded STR(?e)", UNGUARDED), ("COALESCE(STR(?e), ...)", COALESCED),
                 ("guarded IF(isBlank(?e), ...)", GUARDED)):
    print(f"== {label}")
    for name, fn in (("rdflib", rdflib_answer), ("holosdb", holosdb_answer), ("pyoxigraph", pyoxigraph_answer)):
        try:
            print(f"   {name:11} {fn(q)}")
        except ImportError:
            print(f"   {name:11} (not installed)")
