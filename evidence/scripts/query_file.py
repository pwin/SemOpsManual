"""Run a SPARQL SELECT over local RDF files and print the rows (rdflib).

    python scripts/query_file.py fixtures/acme_robotics/reference_vocab/foaf.rdf \
        "SELECT ?d WHERE { <http://xmlns.com/foaf/0.1/name> <http://www.w3.org/2000/01/rdf-schema#domain> ?d }"

Any number of files may come before the query, which is the last argument.
Write @path to read the query from a file.
"""
import sys

from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
*files, query = sys.argv[1:]
if query.startswith("@"):
    query = open(query[1:], encoding="utf-8").read()
g = Graph()
for f in files:
    g.parse(f)
res = g.query(query)
print(",".join(str(v) for v in res.vars))
for row in res:
    print(",".join("" if v is None else str(v) for v in row))
