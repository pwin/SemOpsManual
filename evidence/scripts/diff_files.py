"""Show a unified diff of two text files (no output means identical).

    python scripts/diff_files.py fixtures/acme_robotics/employees.rq work/C12_04/acme/employees.rq
"""
import difflib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
a, b = Path(sys.argv[1]), Path(sys.argv[2])
diff = list(difflib.unified_diff(a.read_text(encoding="utf-8").splitlines(),
                                 b.read_text(encoding="utf-8").splitlines(),
                                 a.as_posix(), b.as_posix(), lineterm="", n=0))
print("\n".join(diff) if diff else "identical")
