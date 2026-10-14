"""Chapter 7: what the four PyPI packages actually install, and what the suite's
check registry holds.

    python scripts/inspect_packages.py

For each package: its version, the console commands it installs (if any) and
its declared runtime dependencies. Then, inside the installed suite: the
registry's entry count, how many portable .rq checks and SHACL shape files ship,
and how many .rq checks guard their message against blank nodes with
IF(isBlank(...)).
"""
import json
import sys
from importlib import metadata, resources
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

for pkg in ("ontology-quality-suite", "shacl", "tarka-rdf", "holosdb"):
    d = metadata.distribution(pkg)
    commands = [ep.name for ep in d.entry_points if ep.group == "console_scripts"]
    reqs = [r for r in (d.requires or []) if "extra ==" not in r]
    print(f"{pkg} {d.version}")
    print(f"    commands installed: {', '.join(commands) if commands else 'none (library only)'}")
    print(f"    runtime dependencies: {', '.join(reqs) if reqs else 'none'}")

res = Path(str(resources.files("ontology_suite") / "resources"))
reg = json.loads((res / "registry.json").read_text(encoding="utf-8"))
entries = reg["checks"] if isinstance(reg, dict) and "checks" in reg else reg
rq = sorted((res / "sparql").rglob("*.rq"))
shapes = sorted((res / "shapes").glob("*.ttl"))
guarded = [p for p in rq if "isBlank(" in p.read_text(encoding="utf-8")]
categories = sorted({e["category"] for e in entries})
print(f"registry entries: {len(entries)} in {len(categories)} categories ({', '.join(categories)})")
print(f"portable .rq checks: {len(rq)}; SHACL shape files: {len(shapes)}")
print(f".rq checks guarding a message with IF(isBlank(...)): {len(guarded)}")
bare = [p for p in rq if "STR(?" in p.read_text(encoding="utf-8") and p not in guarded]
print(f".rq checks building a message with STR(?...) and no isBlank guard: {len(bare)}")
