"""Check every relative link in EVIDENCE.md and the annotated manual.

    python tools/check_links.py

A link must point at a file that exists, and an anchor at a heading or an
explicit <a id="…"> in that file. External links (http, https, mailto) are
not fetched. Prints each broken link and exits 1 if there are any.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from harness.render import gh_slug  # noqa: E402

EVIDENCE = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)|href=\"([^\"]+)\"|src=\"([^\"]+)\"")
FENCE = re.compile(r"^\s*(```|~~~)")
_anchors = {}


def anchors(path: Path) -> set:
    if path not in _anchors:
        found, in_fence = set(), False
        counts = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            found.update(re.findall(r'<a id="([^"]+)"', line))
            if line.startswith("#"):
                slug = gh_slug(line.lstrip("#").strip())
                n = counts.get(slug, 0)
                counts[slug] = n + 1
                found.add(slug if n == 0 else f"{slug}-{n}")
        _anchors[path] = found
    return _anchors[path]


def links(path: Path):
    in_fence = False
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK.finditer(line):
            yield no, next(g for g in m.groups() if g)


def main() -> int:
    files = [EVIDENCE / "EVIDENCE.md"] + sorted((EVIDENCE / "manual").rglob("*.md"))
    bad = 0
    checked = 0
    for f in files:
        for no, target in links(f):
            if re.match(r"^(https?|mailto):", target):
                continue
            checked += 1
            path, _, anchor = target.partition("#")
            dest = (f.parent / path).resolve() if path else f
            if not dest.exists():
                print(f"{f.relative_to(EVIDENCE)}:{no}: no such file: {target}")
                bad += 1
            elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                print(f"{f.relative_to(EVIDENCE)}:{no}: no anchor #{anchor} in {dest.name}")
                bad += 1
    print(f"{checked} relative links checked in {len(files)} files, {bad} broken")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
