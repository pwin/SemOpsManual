"""Chapter 7's versions box: what this machine actually has.

    python scripts/versions.py

Prints the PyPI package versions, the release binaries' own --version output and
the npm package versions, the same way the harness records them.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from harness.env import versions  # noqa: E402

for k, v in versions().items():
    print(f"{k:28} {v}")
