"""Chapter 2 §2.3: how many of gist's object properties constrain neither domain nor range.

    python scripts/gist_properties.py 14.1.0 13.0.0

Downloads each release's web-download zip from github.com/semanticarts/gist (cached
in work/gist/), reads gistCore<version>.ttl, and counts the gist object
properties by which of rdfs:domain and rdfs:range they declare. gist is published
by Semantic Arts under its own licence; nothing of it is copied into this folder.
"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph

sys.stdout.reconfigure(encoding="utf-8")
GIST = "https://w3id.org/semanticarts/ns/ontology/gist/"
cache = Path("work/gist")
cache.mkdir(parents=True, exist_ok=True)

for version in sys.argv[1:]:
    ttl = cache / f"gistCore{version}.ttl"
    if not ttl.is_file():
        url = f"https://github.com/semanticarts/gist/releases/download/v{version}/gist{version}_webDownload.zip"
        with urllib.request.urlopen(url) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        name = next(n for n in z.namelist() if n.endswith(f"gistCore{version}.ttl"))
        ttl.write_bytes(z.read(name))
    g = Graph()
    g.parse(ttl)
    ops = {p for p in g.subjects(RDF.type, OWL.ObjectProperty) if str(p).startswith(GIST)}
    dps = {p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if str(p).startswith(GIST)}
    dom = {p for p in ops if (p, RDFS.domain, None) in g}
    rng = {p for p in ops if (p, RDFS.range, None) in g}
    print(f"gist {version}: {len(ops)} object properties, {len(dps)} data properties; "
          f"domain only {len(dom - rng)}, range only {len(rng - dom)}, both {len(dom & rng)}, "
          f"neither {len(ops - dom - rng)}")
