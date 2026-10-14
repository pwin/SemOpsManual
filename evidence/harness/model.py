"""The shape of a claim, a step, and the result of running one.

A *claim* is one checkable statement in the manual. It points at the place in
the manual where the statement is made (a file and a short, verbatim snippet of
the text), says what kind of evidence backs it, and -- for claims that can be
reproduced here -- lists the commands that reproduce it and a check that decides
whether the output still supports the statement.

Three kinds:

  run       reproduced by the commands in `steps`; `check` decides PASS/FAIL
  source    backed by an upstream file, commit or document, cited in `sources`
  argument  a judgement or recommendation; `notes` says what it rests on

Nothing here knows about any particular tool. The claims live in `claims/`.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

EVIDENCE = Path(__file__).resolve().parent.parent
REPO = EVIDENCE.parent


@dataclass
class Step:
    """One command, as a reader would type it from the evidence/ folder.

    `cmd` is POSIX shell syntax without pipes or redirection, so the same text
    can be shown in the document and split into an argument list to run.
    `{work}` is replaced by this claim's scratch directory, `work/<claim id>`.
    """
    cmd: str
    note: str = ""
    env: dict = field(default_factory=dict)
    cwd: str = "."          # relative to evidence/
    show: bool = True       # print it in EVIDENCE.md
    timeout: int = 600


@dataclass
class Service:
    """A process started before the claim's steps and stopped after them,
    such as the small SPARQL endpoint used for the live-store claims."""
    cmd: str
    ready_url: str
    note: str = ""


@dataclass
class Source:
    label: str
    url: str
    quote: str = ""


@dataclass
class Claim:
    id: str                         # e.g. "C09.02"
    title: str
    chapter: str                    # "00" for the README, "01".."15", "A"
    where: Tuple[str, str]          # (manual file, verbatim snippet)
    kind: str                       # run | source | argument
    claim: str = ""                 # the statement, in a sentence
    steps: List[Step] = field(default_factory=list)
    services: List[Service] = field(default_factory=list)
    check: Optional[Callable[["RunResult"], Tuple[bool, str]]] = None
    checks: str = ""                # what `check` asserts, in words
    data: List[str] = field(default_factory=list)      # input files, relative to evidence/
    scripts: List[str] = field(default_factory=list)   # scripts to print in full
    sources: List[Source] = field(default_factory=list)
    notes: str = ""
    needs: List[str] = field(default_factory=list)     # tools that must be present
    excerpt: Optional[Callable[[int, str], str]] = None  # trims a step's output for the document
    same_as: str = ""               # the id of a claim whose evidence also covers this one

    @property
    def anchor(self) -> str:
        return self.id.lower().replace(".", "-")

    @property
    def slug(self) -> str:
        return self.id.replace(".", "_")


@dataclass
class StepResult:
    cmd: str
    rc: int
    stdout: str
    stderr: str
    seconds: float

    @property
    def out(self) -> str:
        return self.stdout + ("\n" + self.stderr if self.stderr.strip() else "")


@dataclass
class RunResult:
    claim: Claim
    steps: List[StepResult]
    work: Path

    def __getitem__(self, i: int) -> StepResult:
        return self.steps[i]

    def file(self, rel: str) -> Path:
        return self.work / rel


# ---------------------------------------------------------------- helpers for checks

FINDINGS = re.compile(r"Findings: (\d+) total \((\d+) Violation, (\d+) Warning, (\d+) Info\)")


def findings(text: str) -> Optional[Tuple[int, int, int, int]]:
    """The last 'Findings: N total (V Violation, W Warning, I Info)' line."""
    hits = FINDINGS.findall(text)
    return tuple(int(x) for x in hits[-1]) if hits else None


def rows(csv_path: Path) -> List[dict]:
    with open(csv_path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_check(csv_path: Path) -> dict:
    out: dict = {}
    for r in rows(csv_path):
        out[r["check_id"]] = out.get(r["check_id"], 0) + 1
    return out


def ok(cond: bool, good: str, bad: str = "") -> Tuple[bool, str]:
    return (True, good) if cond else (False, bad or ("not " + good))


def all_of(*parts: Tuple[bool, str]) -> Tuple[bool, str]:
    failed = [m for (c, m) in parts if not c]
    if failed:
        return False, "; ".join(failed)
    return True, "; ".join(m for (_, m) in parts)
