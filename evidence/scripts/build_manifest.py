"""Chapter 13 §13.1: build a live-store manifest in Python, as the manual shows.

    python scripts/build_manifest.py work/C13_02/graphs.json

Runs the manual's snippet unchanged apart from the output path, then prints the
file it wrote, which is the JSON form the manual gives above the snippet.
"""
import sys
from pathlib import Path

from ontology_suite.remote.manifest import GraphBinding, GraphManifest

sys.stdout.reconfigure(encoding="utf-8")
out = sys.argv[1]
Path(out).parent.mkdir(parents=True, exist_ok=True)

GraphManifest(bindings=[
    GraphBinding(graph_uri="https://acme.example.org/graph/ontology/2.0.0",
                 role="ontology"),
    GraphBinding(graph_uri="https://acme.example.org/graph/triplified/employees",
                 role="triplified_data",
                 source_tarql="queries/employees.rq",
                 ontology_graph_uri="https://acme.example.org/graph/ontology/2.0.0"),
]).save(out)

print(Path(out).read_text(encoding="utf-8"))
