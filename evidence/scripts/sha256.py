"""Print a SHA-256 for each file given.

    python scripts/sha256.py work/C13_05/run1/ontology_doc_data.json ...
"""
import hashlib
import sys
from pathlib import Path

for f in sys.argv[1:]:
    print(hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16], Path(f).as_posix())
