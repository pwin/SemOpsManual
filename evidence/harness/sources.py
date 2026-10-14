"""Check that each cited source says what the claim quotes it as saying.

A source is a GitHub permalink: a commit, or a file at a fixed commit, perhaps
with a line range. Given local clones of the repositories, this reads the commit
message or the file at that commit and looks for the quoted words (whitespace
and Markdown emphasis ignored), within the cited lines when lines are given.

Clones are found under EVIDENCE_REPOS (default: the folder above the manual),
by the directory names in LOCAL, or each by its own environment variable.
Sources without a quote are checked only for existence.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .model import REPO, Claim

# GitHub repository name -> (local directory name, environment variable)
LOCAL = {
    "consolidated-ontology-quality-suite-python": ("consolidated_ontology_suite_python", "EVIDENCE_SUITE_REPO"),
    "consolidated-ontology-quality-suite-webapp": ("consolidated_ontology_suite_webapp", "EVIDENCE_WEBAPP_REPO"),
    "SHACL_Engine": ("New_SHACL_Engine", "EVIDENCE_SHACL_REPO"),
    "triplestore": ("new_triplestore_sparql_engine", "EVIDENCE_HOLOS_REPO"),
    "tarka": ("tarka", "EVIDENCE_TARKA_REPO"),
    "SemOpsManual": ("SemOps_Manual", "EVIDENCE_MANUAL_REPO"),
    "consolidated-ontology-quality-suite-python-testing": ("consolidated-ontology-suite-python-testing",
                                                           "EVIDENCE_TESTING_REPO"),
}

URL = re.compile(r"https://github\.com/pwin/([^/]+)/(commit|blob)/([0-9a-f]{7,40})(?:/([^#]+))?(?:#L(\d+)(?:-L(\d+))?)?$")


def _clone(name: str) -> Optional[Path]:
    if name not in LOCAL:
        return None
    d, var = LOCAL[name]
    p = Path(os.environ.get(var) or Path(os.environ.get("EVIDENCE_REPOS", REPO.parent)) / d)
    return p if (p / ".git").exists() else None


def _git(repo: Path, *args: str) -> Optional[str]:
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.stdout if p.returncode == 0 else None


def _flat(s: str) -> str:
    # a quote may run across comment lines: drop each line's comment marker
    s = re.sub(r"(?m)^\s*(#+|//+|\*|>)[ \t]?", "", s)
    s = re.sub(r"[*_`]", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def check_source(url: str, quote: str) -> Tuple[Optional[bool], str]:
    """(True|False, detail), or (None, reason) when it cannot be checked here."""
    m = URL.match(url)
    if not m:
        return None, "not a commit or file permalink"
    name, kind, sha, path, a, b = m.groups()
    repo = _clone(name)
    if repo is None:
        return None, f"no local clone of {name}"
    if kind == "commit":
        text = _git(repo, "show", "-s", "--format=%B", sha)
        if text is None:
            return False, f"commit {sha[:7]} not found in {name}"
        if quote and _flat(quote) not in _flat(text):
            # a commit quote may also come from its diff
            diff = _git(repo, "show", "--format=", sha) or ""
            if _flat(quote) not in _flat(diff):
                return False, f"commit {sha[:7]}: quote not found in message or diff"
        return True, f"commit {sha[:7]}"
    text = _git(repo, "show", f"{sha}:{path}")
    if text is None:
        return False, f"{path} not found at {sha[:7]}"
    if a:
        lines = text.splitlines()
        lo, hi = int(a), int(b or a)
        if hi > len(lines):
            return False, f"{path} has {len(lines)} lines; cited L{lo}-L{hi}"
        if quote:
            # allow a line either side, for a quote that wraps across the boundary
            window = "\n".join(lines[max(0, lo - 2):hi + 1])
            if _flat(quote) not in _flat(window):
                where = "elsewhere in the file" if _flat(quote) in _flat(text) else "not in the file"
                return False, f"{path}: quote not within L{lo}-L{hi} ({where})"
    elif quote and _flat(quote) not in _flat(text):
        return False, f"{path}: quote not found"
    return True, f"{path}" + (f" L{a}" + (f"-L{b}" if b else "") if a else "")


def check_all(claims: List[Claim]) -> Dict[str, List[Tuple[str, Optional[bool], str]]]:
    out: Dict[str, List[Tuple[str, Optional[bool], str]]] = {}
    for c in claims:
        for s in c.sources:
            res, detail = check_source(s.url, s.quote)
            out.setdefault(c.id, []).append((s.url, res, detail))
    return out
