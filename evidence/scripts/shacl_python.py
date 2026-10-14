"""Chapter 11: the shacl package's Python surface.

    python scripts/shacl_python.py data/shacl data/rules

Prints, for the fixtures in those folders:
  - the one-shot validate() on data and shapes, and with the arguments swapped
  - the one-shot against a shapes graph that declares no shapes (refused)
  - the explicit Shapes API against the same (permissive by design)
  - a warnings-only graph, with and without allow_warnings
  - each inference mode, including one that does not exist
"""
import sys
from pathlib import Path

import shacl

sys.stdout.reconfigure(encoding="utf-8")
S, R = Path(sys.argv[1]), Path(sys.argv[2])
data = str(S / "data.ttl")


def one_shot(label, *args, **kw):
    try:
        rep = shacl.validate(*args, **kw)
        print(f"{label:44} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"{label:44} REFUSED: {type(exc).__name__}: {exc}")


print("shacl", shacl.__version__ if hasattr(shacl, "__version__") else "")
one_shot("validate(data, shapes)", data, str(S / "shapes-violation.ttl"))
one_shot("validate(shapes, data)  [swapped]", str(S / "shapes-violation.ttl"), data)
one_shot("validate(data, no-shapes)", data, str(S / "no-shapes.ttl"))
rep = shacl.Shapes.from_file(str(S / "no-shapes.ttl")).validate_file(data)
print(f"{'Shapes.from_file(no-shapes).validate_file':44} conforms={rep.conforms} results={len(rep.results)}")
one_shot("warnings only", data, str(S / "shapes-warning.ttl"))
one_shot("warnings only, allow_warnings=True", data, str(S / "shapes-warning.ttl"), allow_warnings=True)
one_shot("severity on the node shape (the trap)", data, str(S / "shapes-warning-on-node.ttl"),
         allow_warnings=True)

shapes = shacl.Shapes.from_file(str(R / "triple.ttl"))
for mode in ("none", "rdfs", "rules", "rules-iterated", "bogus"):
    try:
        rep = shapes.validate_file(str(R / "people.ttl"), inference=mode)
        print(f"inference={mode:16} conforms={rep.conforms} results={len(rep.results)}")
    except Exception as exc:
        print(f"inference={mode:16} ERROR: {exc}")
