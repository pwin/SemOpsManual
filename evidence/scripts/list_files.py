"""List the files a run wrote, with sizes, so the report set can be checked.

    python scripts/list_files.py work/C09_10/default
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
total = 0
for p in sorted(root.rglob("*")):
    if p.is_file():
        total += p.stat().st_size
        print(f"{p.stat().st_size:9,}  {p.relative_to(root).as_posix()}")
print(f"{sum(1 for p in root.rglob('*') if p.is_file())} files, {total:,} bytes")
