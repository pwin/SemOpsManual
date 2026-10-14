"""Where the tools are, and what versions they report.

The harness runs under the Python interpreter that has the four PyPI packages
installed (see requirements.txt), so `python` and `ontology-quality-suite`
resolve from that interpreter's environment. The three release binaries
(`shacl`, `tarka`, `holos`) are looked for, in order:

  1. an environment variable naming the executable: SHACL_BIN, TARKA_BIN, HOLOS_BIN
  2. evidence/bin/<tool>/..., where tools/fetch_binaries.py puts them
  3. PATH

Node tooling (the DSL, the WebAssembly engine) runs from evidence/node_modules,
installed with `npm ci` from package.json.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path
from typing import Dict, Optional

from .model import EVIDENCE

BIN = EVIDENCE / "bin"
NODE_MODULES = EVIDENCE / "node_modules"
EXE = ".exe" if os.name == "nt" else ""


def _scripts_dir() -> Path:
    return Path(sys.executable).parent


def release_binary(tool: str) -> Optional[str]:
    env = os.environ.get(f"{tool.upper()}_BIN")
    if env and Path(env).is_file():
        return env
    if BIN.is_dir():
        for p in sorted(BIN.rglob(f"{tool}{EXE}")):
            if p.is_file():
                return str(p)
    return shutil.which(tool)


def node() -> Optional[str]:
    return shutil.which("node")


def search_path() -> str:
    """PATH for child processes: this interpreter's scripts, the release
    binaries' folders, then whatever the caller already had."""
    parts = [str(_scripts_dir())]
    for tool in ("shacl", "tarka", "holos"):
        b = release_binary(tool)
        if b:
            parts.append(str(Path(b).parent))
    parts.append(os.environ.get("PATH", ""))
    return os.pathsep.join(parts)


def resolve(argv0: str, path: str) -> str:
    """Turn the first word of a command into an executable path. On Windows a
    child process does not search a PATH you pass it, so this has to happen
    here."""
    if argv0 == "python":
        return sys.executable
    if argv0 in ("shacl", "tarka", "holos"):
        b = release_binary(argv0)
        if b:
            return b
    found = shutil.which(argv0, path=path)
    return found or argv0


def available() -> Dict[str, bool]:
    def has_pkg(name: str) -> bool:
        try:
            metadata.version(name)
            return True
        except metadata.PackageNotFoundError:
            return False

    return {
        "suite": has_pkg("ontology-quality-suite"),
        "shacl-py": has_pkg("shacl"),
        "holosdb": has_pkg("holosdb"),
        "tarka-py": has_pkg("tarka-rdf"),
        "pyoxigraph": has_pkg("pyoxigraph"),
        "shacl-cli": release_binary("shacl") is not None,
        "tarka-cli": release_binary("tarka") is not None,
        "holos-cli": release_binary("holos") is not None,
        "node": node() is not None and (NODE_MODULES / "ontology-suite").is_dir(),
        "network": os.environ.get("EVIDENCE_OFFLINE") != "1",
        "testing-repo": bool(os.environ.get("EVIDENCE_TESTING_REPO"))
        and Path(os.environ["EVIDENCE_TESTING_REPO"]).is_dir(),
        # Semantic Arts' TARQL engine, which the testing repository's competency
        # tests triplify with; the suite finds it through this variable.
        "oxi-gen": bool(os.environ.get("ONTOLOGY_SUITE_OXI_GEN_BIN"))
        and Path(os.environ["ONTOLOGY_SUITE_OXI_GEN_BIN"]).is_file(),
    }


def versions() -> Dict[str, str]:
    out: Dict[str, str] = {
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()} ({platform.machine()})",
    }
    for pkg in ("ontology-quality-suite", "shacl", "holosdb", "tarka-rdf", "rdflib", "pyoxigraph", "polars"):
        try:
            out[f"PyPI {pkg}"] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            pass
    for tool in ("shacl", "tarka", "holos"):
        b = release_binary(tool)
        if b:
            try:
                v = subprocess.run([b, "--version"], capture_output=True, text=True, timeout=30)
                out[f"release {tool}"] = (v.stdout or v.stderr).strip().splitlines()[0]
            except Exception as exc:  # pragma: no cover - reported, not fatal
                out[f"release {tool}"] = f"unavailable ({exc})"
    n = node()
    if n:
        out["node"] = subprocess.run([n, "--version"], capture_output=True, text=True).stdout.strip()
        for pkg in ("ontology-suite", "shacl-wasm-node", "holos-wasm-node", "typescript"):
            pj = NODE_MODULES / pkg / "package.json"
            if pj.is_file():
                out[f"npm {pkg}"] = json.loads(pj.read_text(encoding="utf-8"))["version"]
    for name, cmd in (("java (for HermiT)", ["java", "-version"]),
                      ("oxi-gen (testing repo only)", [os.environ.get("ONTOLOGY_SUITE_OXI_GEN_BIN", ""), "--version"])):
        exe = shutil.which(cmd[0], path=search_path()) if cmd[0] else None
        if exe:
            v = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=60)
            out[name] = ((v.stderr or v.stdout).strip().splitlines() or ["?"])[0]
    return out
