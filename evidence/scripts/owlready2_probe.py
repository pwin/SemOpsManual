"""Chapter 14 §14.4: where the reasoner's 'entity' error actually comes from.

    python scripts/owlready2_probe.py fixtures/acme_robotics/acme-org-v1.ttl \
        fixtures/acme_robotics/reference_vocab/org.ttl fixtures/acme_robotics/reference_vocab/foaf.rdf

Does what the suite's reasoner bridge does (merge the files, write RDF/XML, load
it into owlready2), without the suite around it, and reports whether loading
succeeded. If it fails, prints the entity owlready2 was building and the last
frames of the traceback. Run it under different PYTHONHASHSEED values.

HermiT is not called at all: the failure, when it happens, is in loading.
"""
import os
import sys
import tempfile
import traceback
from pathlib import Path

import owlready2
from owlready2 import namespace as ns
from rdflib import Graph

sys.stdout.reconfigure(encoding="utf-8")
failed_on = []
original = ns.World._load_by_storid


def watched(self, storid, full_iri=None, *args, **kwargs):
    try:
        return original(self, storid, full_iri, *args, **kwargs)
    except UnboundLocalError:
        if not failed_on:
            failed_on.append(full_iri or self._unabbreviate(storid))
        raise


ns.World._load_by_storid = watched

# rdflib labels a parsed blank node "N" + uuid4().hex: random in every process,
# whatever the hash seed, and hashed like any other string. Set PROBE_FIXED_BNODES
# to number them instead (see load_repeat.py).
if os.environ.get("PROBE_FIXED_BNODES"):
    import itertools
    import uuid

    import rdflib.term
    _counter = itertools.count(1)
    rdflib.term.uuid4 = lambda: uuid.UUID(int=next(_counter))

g = Graph()
for f in sys.argv[1:]:
    g.parse(f)
seed = os.environ.get("PYTHONHASHSEED", "(unset)")
# The suite's bridge writes to a fresh temporary directory, as this does by
# default. Set PROBE_DIR to load from a fixed path instead (see load_repeat.py).
with tempfile.TemporaryDirectory() as tmp:
    path = Path(os.environ.get("PROBE_DIR") or tmp) / "ontology.owl"
    path.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(path), format="xml")
    try:
        owlready2.World().get_ontology(str(path)).load()
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} loaded the merged ontology")
    except UnboundLocalError as exc:
        print(f"PYTHONHASHSEED={seed}: owlready2 {owlready2.VERSION} failed while building <{failed_on[0]}>: {exc}")
        frames = traceback.extract_tb(exc.__traceback__)[-3:]
        for fr in frames:
            print(f"    {Path(fr.filename).name}:{fr.lineno} in {fr.name}: {fr.line}")
