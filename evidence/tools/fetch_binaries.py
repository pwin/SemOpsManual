"""Download the three release binaries the evidence uses, and check them.

    python tools/fetch_binaries.py

For this machine's platform, fetches `shacl` (SHACL Engine 0.3.4), `tarka`
(0.1.1) and `holos` + `holos-server` (HOLOS 0.25.0) from their GitHub releases,
verifies each archive against the release's SHA256SUMS, and unpacks it under
evidence/bin/. Nothing is installed anywhere else. If a binary is already
there, it is left alone; a superseded version of it is removed.
"""
import hashlib
import io
import platform
import shutil
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "bin"
RELEASES = {
    "shacl": ("pwin/SHACL_Engine", "v0.3.4", "shacl-0.3.4-{target}"),
    "tarka": ("pwin/tarka", "v0.1.1", "tarka-0.1.1-{target}"),
    "holos": ("pwin/triplestore", "v0.25.0", "holos-0.25.0-{target}"),
}


def target() -> str:
    system, machine = platform.system(), platform.machine().lower()
    arm = machine in ("arm64", "aarch64")
    if system == "Windows":
        return "x86_64-pc-windows-msvc"
    if system == "Darwin":
        return "aarch64-apple-darwin" if arm else "x86_64-apple-darwin"
    return "aarch64-unknown-linux-gnu" if arm else "x86_64-unknown-linux-gnu"


def get(url: str) -> bytes:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as exc:  # transient network errors happen; retry a few times
            if attempt == 4:
                raise
            print(f"    retrying after {exc}")
            time.sleep(3)
    raise RuntimeError("unreachable")


def main() -> int:
    t = target()
    ext = ".zip" if "windows" in t else ".tar.gz"
    for tool, (repo, tag, stem) in RELEASES.items():
        dest = BIN / tool
        folder = dest / stem.format(target=t)
        if folder.is_dir() and any(folder.rglob(tool + (".exe" if "windows" in t else ""))):
            print(f"{tool}: {tag} already present under {folder}")
            continue
        asset = stem.format(target=t) + ext
        base = f"https://github.com/{repo}/releases/download/{tag}/"
        print(f"{tool}: fetching {asset}")
        sums = get(base + "SHA256SUMS").decode()
        want = next((l.split()[0] for l in sums.splitlines() if l.strip().endswith(asset)), None)
        if not want:
            print(f"    {asset} is not listed in SHA256SUMS; this platform may not be built for {tag}")
            return 1
        blob = get(base + asset)
        have = hashlib.sha256(blob).hexdigest()
        if have != want:
            print(f"    checksum mismatch: expected {want}, got {have}")
            return 1
        print(f"    sha256 {have[:16]}... matches SHA256SUMS")
        dest.mkdir(parents=True, exist_ok=True)
        if ext == ".zip":
            zipfile.ZipFile(io.BytesIO(blob)).extractall(dest)
        else:
            tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz").extractall(dest, filter="data")
            for p in dest.rglob("*"):
                if p.is_file() and p.name.startswith(tool):
                    p.chmod(0o755)
        # Only the pinned version stays: the harness takes the first binary it
        # finds, so a superseded one left beside it could be the one that runs.
        for old in dest.iterdir():
            if old.is_dir() and old != folder:
                shutil.rmtree(old)
                print(f"    removed the superseded {old.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
