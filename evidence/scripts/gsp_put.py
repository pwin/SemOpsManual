"""Load RDF files into one named graph over the SPARQL Graph Store Protocol.

    python scripts/gsp_put.py http://127.0.0.1:7899/graph GRAPH_IRI FILE [FILE ...]

The first file replaces the graph (PUT); any further files are added to it
(POST). The same thing as `curl -X PUT -H "Content-Type: text/turtle"
--data-binary @FILE "<endpoint>?graph=<iri>"`, without needing curl.
"""
import sys
import urllib.parse
import urllib.request
from pathlib import Path

TYPES = {".ttl": "text/turtle", ".nt": "application/n-triples", ".rdf": "application/rdf+xml",
         ".owl": "application/rdf+xml", ".trig": "application/trig", ".nq": "application/n-quads"}

endpoint, graph, files = sys.argv[1], sys.argv[2], sys.argv[3:]
for i, f in enumerate(files):
    url = f"{endpoint}?{urllib.parse.urlencode({'graph': graph})}"
    method = "PUT" if i == 0 else "POST"
    req = urllib.request.Request(url, data=Path(f).read_bytes(), method=method,
                                 headers={"Content-Type": TYPES.get(Path(f).suffix, "text/turtle")})
    with urllib.request.urlopen(req) as r:
        print(f"{method} {Path(f).name} -> <{graph}>: HTTP {r.status}")
