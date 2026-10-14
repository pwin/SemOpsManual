"""Write EVIDENCE.md and the annotated edition of the manual.

Both are generated, so they cannot drift from the claims or from the recorded
outputs. Edit `claims/` and the scripts, then run `python verify.py`.

The annotated edition is the manual, unchanged, with one line added after each
paragraph that makes a checked claim:

    Evidence: C09.02 · The unscoped run reports 479 findings, every time

linking to that claim's entry in EVIDENCE.md, which links back to the same line.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .model import EVIDENCE, REPO, Claim
from .runner import recorded

MANUAL_OUT = EVIDENCE / "manual"
KIND_LABEL = {"run": "Reproduced here", "source": "Cited from upstream", "argument": "Argument"}


# ---------------------------------------------------------------- manual structure

def manual_files() -> List[str]:
    return ["README.md"] + sorted(f"docs/{p.name}" for p in (REPO / "docs").glob("*.md"))


def chapter_code(rel: str) -> str:
    if rel == "README.md":
        return "00"
    name = Path(rel).name
    return "A" if name.startswith("diagram-style") else name[:2]


def chapter_title(rel: str) -> str:
    if rel == "README.md":
        return "Introduction (README)"
    for line in (REPO / rel).read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return rel


def gh_slug(heading: str) -> str:
    """GitHub's heading anchor: lower case, punctuation dropped, spaces to '-'."""
    s = heading.strip().lower()
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("`", "")
    out = []
    for ch in s:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
        elif unicodedata.category(ch).startswith("L"):
            out.append(ch)
    return "".join(out)


@dataclass
class Block:
    start: int        # first line index
    end: int          # last line index (inclusive)
    text: str         # normalised text
    heading: str      # nearest heading above


def _norm(s: str) -> str:
    s = re.sub(r"^\s*(>\s*)+", "", s, flags=re.M)
    return re.sub(r"\s+", " ", s).strip()


def blocks(lines: List[str]) -> List[Block]:
    out: List[Block] = []
    heading = ""
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        start = i
        if lines[i].lstrip().startswith(("```", "~~~")):
            fence = lines[i].lstrip()[:3]
            i += 1
            while i < n and not lines[i].lstrip().startswith(fence):
                i += 1
            end = min(i, n - 1)
            i += 1
        else:
            while i < n and lines[i].strip() and not lines[i].lstrip().startswith(("```", "~~~")):
                i += 1
            end = i - 1
        text = "\n".join(lines[start:end + 1])
        if lines[start].startswith("#"):
            heading = lines[start].lstrip("#").strip()
        out.append(Block(start, end, _norm(text), heading))
    return out


def locate(rel: str, snippet: str) -> Optional[Block]:
    lines = (REPO / rel).read_text(encoding="utf-8").splitlines()
    want = _norm(snippet)
    for b in blocks(lines):
        if want in b.text:
            return b
    return None


# ---------------------------------------------------------------- annotated manual

def _rewrite_links(rel: str, text: str) -> str:
    if rel == "README.md":
        up = "../../"
        for d in ("assets/", "notebooks/", "tools/"):
            text = text.replace(f"]({d}", f"]({up}{d}").replace(f'src="{d}', f'src="{up}{d}')
        text = text.replace("](LICENSE)", f"]({up}LICENSE)")
        # the manual's pointer to this folder, seen from evidence/manual/
        text = text.replace("](evidence/README.md)", "](../README.md)")
        return text
    up = "../../../"
    for d in ("assets/", "notebooks/", "tools/"):
        text = text.replace(f"](../{d}", f"]({up}{d}").replace(f'src="../{d}', f'src="{up}{d}')
    text = text.replace("](../LICENSE)", f"]({up}LICENSE)")
    return text


def _short_status(c: Claim) -> str:
    if c.kind == "argument":
        return "argument"
    target = BY_ID.get(c.same_as, c)
    if target.kind != "run":
        return "cited"
    rec = recorded(target)
    return f"reproduced: {rec['status']}" if rec else "not yet run"


def write_annotated(claims: List[Claim]) -> Dict[str, Tuple[str, str]]:
    """Returns {claim id: (annotated link target, plain-manual heading anchor)}."""
    targets: Dict[str, Tuple[str, str]] = {}
    BY_ID.clear()
    BY_ID.update({c.id: c for c in claims})
    missing = []
    for c in claims:
        if c.where[0] not in manual_files():
            missing.append(f"{c.id}: no such manual file {c.where[0]}")
        elif locate(c.where[0], c.where[1]) is None:
            missing.append(f"{c.id}: snippet not found in {c.where[0]}: {c.where[1]!r}")
    if missing:
        raise SystemExit("cannot place these claims in the manual:\n  " + "\n  ".join(missing))
    for rel in manual_files():
        src = (REPO / rel).read_text(encoding="utf-8")
        lines = src.splitlines()
        here = [c for c in claims if c.where[0] == rel]
        inserts: Dict[int, List[Claim]] = {}
        bl = blocks(lines)
        for c in here:
            want = _norm(c.where[1])
            hit = next((b for b in bl if want in b.text), None)
            if hit is None:
                raise SystemExit(f"{c.id}: snippet not found in {rel}: {c.where[1]!r}")
            inserts.setdefault(hit.end, []).append(c)
            out_rel = "manual/" + rel
            targets[c.id] = (f"{out_rel}#ev-{c.anchor}", f"../{rel}#{gh_slug(hit.heading)}")

        ev = "../EVIDENCE.md" if rel == "README.md" else "../../EVIDENCE.md"
        plain = "../../README.md" if rel == "README.md" else f"../../../{rel}"
        code = chapter_code(rel)
        out: List[str] = []
        banner_done = False
        for i, line in enumerate(lines):
            out.append(line)
            if not banner_done and (line.startswith("# ") or line.startswith('<h1 align="center">')):
                out += ["", f"> **Annotated edition.** After each claim that has been checked, an "
                            f"*Evidence* line links to the commands, data and output behind it in "
                            f"[EVIDENCE.md]({ev}#chapter-{code.lower()}), which links back here. "
                            f"The plain edition of this page is [here]({plain})."]
                banner_done = True
            if i in inserts:
                cs = inserts[i]
                anchors = "".join(f'<a id="ev-{c.anchor}"></a>' for c in cs)
                links = " · ".join(f"[{c.id} — {c.title}]({ev}#{c.anchor}) ({_short_status(c)})" for c in cs)
                out += ["", f"{anchors}*Evidence:* {links}"]
        text = _rewrite_links(rel, "\n".join(out) + "\n")
        dest = MANUAL_OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
    return targets


# ---------------------------------------------------------------- EVIDENCE.md

NOISE = re.compile(r"^\* Owlready|^\s*$")


def _trim(text: str, keep: int = 40) -> str:
    lines = [l for l in text.splitlines() if not NOISE.match(l)]
    if len(lines) <= keep:
        return "\n".join(lines)
    head, tail = lines[: keep - 10], lines[-8:]
    return "\n".join(head + [f"… ({len(lines) - len(head) - len(tail)} lines omitted; full output in the outputs/ record)"] + tail)


def _status(c: Claim, rec: Optional[dict]) -> str:
    if c.kind != "run":
        return KIND_LABEL[c.kind]
    if not rec:
        return "not yet run" + (f" (needs {', '.join(c.needs)})" if c.needs else "")
    return f"**{rec['status']}** ({rec['ran']})"


def _embed(rel: str, lang: str = "") -> str:
    p = EVIDENCE / rel
    body = p.read_text(encoding="utf-8").rstrip()
    if not lang:
        lang = {".py": "python", ".ttl": "turtle", ".trig": "turtle", ".rq": "sparql", ".json": "json",
                ".ts": "typescript", ".mjs": "javascript", ".csv": "text", ".stottr": "text",
                ".sh": "bash"}.get(p.suffix, "text")
    return (f"<details><summary><code>{rel}</code></summary>\n\n```{lang}\n{body}\n```\n\n</details>\n")


BY_ID: Dict[str, Claim] = {}
SOURCE_CHECKS: Dict[str, dict] = {}


def _record_for(c: Claim) -> Optional[dict]:
    if c.same_as:
        return recorded(BY_ID[c.same_as]) if BY_ID[c.same_as].kind == "run" else None
    return recorded(c) if c.kind == "run" else None


def render_claim(c: Claim, targets: Dict[str, Tuple[str, str]]) -> str:
    rec = _record_for(c)
    ann, plain = targets[c.id]
    rel = c.where[0]
    ch = chapter_code(rel)
    where = "README" if ch == "00" else ("Appendix A" if ch == "A" else f"Chapter {int(ch)}")
    out = [f'<a id="{c.anchor}"></a>', f"### {c.id} — {c.title}", ""]
    out.append(f"**In the manual:** [{where}, at the claim]({ann}) · "
               f"[plain edition]({plain})  ")
    out.append(f"**Kind:** {KIND_LABEL[c.kind]} · **Result:** {_status(c, rec)}")
    out.append("")
    quote = c.where[1].strip()
    # a quoted link is relative to its chapter; keep the words, drop the target
    quote = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", quote)
    out.append(f"> {quote}")
    out.append("")
    if c.claim:
        out += [c.claim, ""]
    if c.same_as:
        other = BY_ID[c.same_as]
        if other.kind == "run":
            out += [f"**Evidence:** the same as [{other.id} — {other.title}](#{other.anchor}), "
                    f"which reproduces it" + (f": {rec['detail']}" if rec else "."), ""]
        else:
            out += [f"**Evidence:** the same as [{other.id} — {other.title}](#{other.anchor}) "
                    f"({KIND_LABEL[other.kind].lower()}).", ""]
        if c.notes:
            out += [c.notes.strip(), ""]
        out += ["---", ""]
        return "\n".join(out)
    if c.data:
        out.append("**Inputs:** " + ", ".join(f"[`{d}`]({d})" for d in c.data))
        out.append("")
        for d in c.data:
            p = EVIDENCE / d
            if d.startswith("data/") and p.is_file() and p.stat().st_size < 4000:
                out.append(_embed(d))
    if c.steps:
        shown = [s for s in c.steps if s.show]
        if c.services:
            out.append("Started first, and stopped afterwards:")
            out.append("")
            out.append("```bash\n" + "\n".join(s.cmd.replace("{work}", f"work/{c.slug}") for s in c.services) + "\n```")
            out.append("")
        out.append("**Commands** (from the `evidence/` folder):")
        out.append("")
        lines = []
        for s in shown:
            if s.note:
                lines.append(f"# {s.note}")
            env = " ".join(f"{k}={v}".replace("{work}", f"work/{c.slug}") for k, v in s.env.items())
            line = (env + " " if env else "") + s.cmd.replace("{work}", f"work/{c.slug}")
            if s.cwd != ".":
                line = f"(cd {s.cwd} && {line})"
            lines.append(line)
        out.append("```bash\n" + "\n".join(lines) + "\n```")
        out.append("")
    for s in c.scripts:
        out.append(_embed(s))
    if c.checks:
        out += [f"**What is checked:** {c.checks}", ""]
    if rec:
        out.append(f"**Recorded result:** {rec['status']} — {rec['detail']}")
        out.append("")
        parts = []
        for i, st in enumerate(rec["steps"]):
            text = st["stdout"] + (("\n" + st["stderr"]) if st["stderr"].strip() else "")
            text = c.excerpt(i, text) if c.excerpt else _trim(text)
            parts.append(f"$ {st['cmd']}\n{text}\n[exit {st['rc']}]")
        out.append("<details><summary>Output, as recorded</summary>\n\n```text\n" +
                   "\n\n".join(parts) + "\n```\n\n</details>\n")
    if c.sources:
        out.append("**Sources:**")
        out.append("")
        for s in c.sources:
            line = f"- [{s.label}]({s.url})"
            if s.quote:
                line += f": “{s.quote}”"
            chk = SOURCE_CHECKS.get(s.url)
            if chk:
                what = "quote found" if s.quote else "exists"
                line += f" ({what}, checked {chk['checked']})" if chk["ok"] else f" (**check failed:** {chk['detail']})"
            out.append(line)
        out.append("")
    if c.notes:
        out += [c.notes.strip(), ""]
    out.append("---")
    out.append("")
    return "\n".join(out)


def write_evidence(claims: List[Claim], targets, environment: Dict[str, str], intro: str) -> None:
    by_ch: Dict[str, List[Claim]] = {}
    for c in claims:
        by_ch.setdefault(chapter_code(c.where[0]), []).append(c)

    n_run = sum(1 for c in claims if c.kind == "run" and not c.same_as)
    BY_ID.clear()
    BY_ID.update({c.id: c for c in claims})
    sc = EVIDENCE / "outputs" / "_sources.json"
    SOURCE_CHECKS.clear()
    if sc.is_file():
        SOURCE_CHECKS.update(json.loads(sc.read_text(encoding="utf-8")))
    n_src = sum(len(c.sources) for c in claims)
    n_src_ok = sum(1 for c in claims for s in c.sources if SOURCE_CHECKS.get(s.url, {}).get("ok"))
    recs = {c.id: _record_for(c) for c in claims if c.kind == "run"}
    n_pass = sum(1 for r in recs.values() if r and r["status"] == "PASS")
    n_fail = sum(1 for r in recs.values() if r and r["status"] == "FAIL")
    n_none = sum(1 for r in recs.values() if not r)

    out = [intro.strip(), ""]
    out += ["## Environment of the recorded run", "",
            "| | Version |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in environment.items()]
    out += ["", "## Summary", "",
            f"{len(claims)} claims: {len(recs)} reproduced here, by {n_run} distinct runs "
            f"({n_pass} pass, {n_fail} fail, {n_none} not yet run), "
            f"{sum(1 for c in claims if c.kind == 'source')} cited from upstream, "
            f"{sum(1 for c in claims if c.kind == 'argument')} arguments. "
            f"{n_src} source citations, {n_src_ok} of them checked against the cited commit "
            f"(the quoted words found in the commit message or in the file at the cited lines).", ""]

    order = sorted(by_ch, key=lambda k: (k == "A", k))
    for ch in order:
        rel = by_ch[ch][0].where[0]
        out.append(f"### {chapter_title(rel)}")
        out.append("")
        out.append("| Claim | Kind | Result |")
        out.append("|---|---|---|")
        for c in by_ch[ch]:
            out.append(f"| [{c.id} — {c.title}](#{c.anchor}) | {KIND_LABEL[c.kind]} | "
                       f"{_status(c, recs.get(c.id)).replace('**', '')} |")
        out.append("")
    out.append("---")
    out.append("")
    for ch in order:
        rel = by_ch[ch][0].where[0]
        ann = "manual/" + rel
        out.append(f'<a id="chapter-{ch.lower()}"></a>')
        out.append(f"## {chapter_title(rel)}")
        out.append("")
        out.append(f"Annotated chapter: [{ann}]({ann}) · plain chapter: [../{rel}](../{rel})")
        out.append("")
        for c in by_ch[ch]:
            out.append(render_claim(c, targets))
    (EVIDENCE / "EVIDENCE.md").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
