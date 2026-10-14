"""Print the triples per named graph in an endpoint, by SPARQL, as the manual's
§13.1 recommends doing first against any store you did not load yourself.

    python scripts/endpoint_stats.py http://127.0.0.1:7899/query
"""
import json
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
endpoint = sys.argv[1]
q = """SELECT ?g (COUNT(*) AS ?triples)
WHERE { GRAPH ?g { ?s ?p ?o } }
GROUP BY ?g ORDER BY DESC(?triples)"""
req = urllib.request.Request(endpoint, data=urllib.parse.urlencode({"query": q}).encode(),
                             headers={"Accept": "application/sparql-results+json"}, method="POST")
with urllib.request.urlopen(req) as r:
    res = json.load(r)
print("g,triples")
for b in res["results"]["bindings"]:
    print(f"{b['g']['value']},{b['triples']['value']}")
