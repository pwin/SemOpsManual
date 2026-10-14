"""Run a claim's steps, check the result, and record what happened.

Each run writes outputs/<claim id>.json: the commands exactly as shown, their
exit codes, their output with machine-specific paths replaced, the check's
verdict and the date. Those files are the record the evidence document is built
from, so a claim that cannot run here (a missing tool, no network) keeps the
last recorded result rather than losing it.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import List, Optional

from . import env
from .model import EVIDENCE, REPO, Claim, RunResult, StepResult

OUTPUTS = EVIDENCE / "outputs"
WORK = EVIDENCE / "work"


def _normalise(text: str) -> str:
    """Replace the paths that differ between machines, so a recorded output can
    be compared with yours."""
    subs = [
        (str(EVIDENCE), "."),
        (str(EVIDENCE).replace("\\", "/"), "."),
        (str(REPO), "<repo>"),
        (str(REPO).replace("\\", "/"), "<repo>"),
        (tempfile.gettempdir(), "<tmp>"),
        (tempfile.gettempdir().replace("\\", "/"), "<tmp>"),
        (str(Path.home()), "~"),
        (str(Path.home()).replace("\\", "/"), "~"),
        (str(Path(sys.executable).parent), "<venv>"),
    ]
    for a, b in subs:
        if a:
            text = text.replace(a, b)
    # Windows separators inside relative paths read more easily as '/'.
    text = re.sub(r"(?<=[\w.>])\\(?=[\w.<])", "/", text)
    return text.replace("\r\n", "\n")


def _split(cmd: str) -> List[str]:
    return shlex.split(cmd, posix=True)


def _start(cmd: str, path: str) -> subprocess.Popen:
    argv = _split(cmd)
    argv[0] = env.resolve(argv[0], path)
    e = dict(os.environ, PATH=path, PYTHONIOENCODING="utf-8")
    return subprocess.Popen(argv, cwd=EVIDENCE, env=e, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)


def _wait_ready(url: str, seconds: float = 30) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2):
                return
        except Exception:
            time.sleep(0.3)
    raise RuntimeError(f"service did not become ready at {url}")


def run_claim(claim: Claim) -> dict:
    work_rel = f"work/{claim.slug}"
    work = EVIDENCE / work_rel
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    path = env.search_path()

    services: List[subprocess.Popen] = []
    results: List[StepResult] = []
    try:
        for s in claim.services:
            services.append(_start(s.cmd.replace("{work}", work_rel), path))
            _wait_ready(s.ready_url)
        for step in claim.steps:
            shown = step.cmd.replace("{work}", work_rel)
            argv = _split(shown)
            argv[0] = env.resolve(argv[0], path)
            e = dict(os.environ, PATH=path, PYTHONIOENCODING="utf-8")
            e.update({k: v.replace("{work}", work_rel) for k, v in step.env.items()})
            cwd = Path(os.path.expandvars(step.cwd))
            if not cwd.is_absolute():
                cwd = EVIDENCE / cwd
            t0 = time.perf_counter()
            try:
                p = subprocess.run(argv, cwd=cwd, env=e, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace",
                                   timeout=step.timeout)
                rc, so, se = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired as exc:
                rc, so, se = -1, exc.stdout or "", f"timed out after {step.timeout}s"
            results.append(StepResult(shown, rc, so, se, time.perf_counter() - t0))
    finally:
        for p in services:
            p.terminate()
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()

    rr = RunResult(claim, results, work)
    try:
        passed, detail = claim.check(rr) if claim.check else (True, "ran")
    except Exception as exc:  # a check that crashes is a failure, with the reason
        passed, detail = False, f"check raised {type(exc).__name__}: {exc}"

    record = {
        "id": claim.id,
        "status": "PASS" if passed else "FAIL",
        "detail": _normalise(detail),
        "ran": dt.date.today().isoformat(),
        "steps": [
            {"cmd": r.cmd, "rc": r.rc, "seconds": round(r.seconds, 1),
             "stdout": _normalise(r.stdout), "stderr": _normalise(r.stderr)}
            for r in results
        ],
    }
    OUTPUTS.mkdir(exist_ok=True)
    (OUTPUTS / f"{claim.slug}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False),
                                                encoding="utf-8", newline="\n")
    return record


def recorded(claim: Claim) -> Optional[dict]:
    p = OUTPUTS / f"{claim.slug}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
