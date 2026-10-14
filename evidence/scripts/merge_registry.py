"""Chapter 8 §8.5: build a merged registry, the built-in entries plus a project's own.

    python scripts/merge_registry.py fixtures/acme_robotics/custom_checks/registry.json work/C08_09/merged-registry.json

`--registry` replaces rather than composes, so a project that wants its house
rules *and* the suite's own checks named properly passes one merged file to
`--registry` and both query trees to `--sparql` (`my-checks/` and `@builtin`).
"""
import json
import sys
from importlib import resources
from pathlib import Path

project = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
builtin = json.loads((resources.files("ontology_suite") / "resources" / "registry.json").read_text(encoding="utf-8"))


def entries(reg):
    return reg["checks"] if isinstance(reg, dict) and "checks" in reg else reg


merged = {e["id"]: e for e in entries(builtin)}
for e in entries(project):
    merged[e["id"]] = e
out = builtin if isinstance(builtin, list) else dict(builtin)
if isinstance(builtin, dict) and "checks" in builtin:
    out["checks"] = list(merged.values())
else:
    out = list(merged.values())
Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
Path(sys.argv[2]).write_text(json.dumps(out, indent=1), encoding="utf-8", newline="\n")
print(f"{len(entries(builtin))} built-in + {len(entries(project))} project = {len(merged)} entries -> {sys.argv[2]}")
