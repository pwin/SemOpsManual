"""Copy a file or a folder, so that claims which modify their inputs (repairs)
never touch the originals.

    python scripts/copy_tree.py fixtures/acme_robotics work/C12_04/acme
"""
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
if src.is_dir():
    shutil.copytree(src, dst, dirs_exist_ok=True)
else:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
print(f"copied {src.as_posix()} -> {dst.as_posix()}")
