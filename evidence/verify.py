"""Check the SemOps Manual's claims, and rebuild EVIDENCE.md and the annotated manual.

    python verify.py                  run every claim this machine can run, then render
    python verify.py --only C09.*     run matching claims only (glob), then render
    python verify.py --render         render from the recorded outputs, run nothing
    python verify.py --list           list the claims and whether each can run here
    python verify.py --sources        check the cited sources' quotes only, then render

Run it with the Python that has requirements.txt installed. See README.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from claims import ALL  # noqa: E402
from harness import env, render, runner, sources  # noqa: E402
from harness.model import EVIDENCE  # noqa: E402


def check_sources() -> int:
    """Check every cited quote against local clones; keep the last result for
    sources that cannot be checked on this machine."""
    path = EVIDENCE / "outputs" / "_sources.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    today = dt.date.today().isoformat()
    new, bad, checked = {}, 0, 0
    for cid, results in sources.check_all(ALL).items():
        for url, res, detail in results:
            if res is None:
                if url in old:
                    new[url] = old[url]
                continue
            checked += 1
            new[url] = {"ok": res, "detail": detail, "checked": today, "claim": cid}
            if not res:
                bad += 1
                print(f"FAIL  {cid:8} source: {detail}\n      {url}")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(new, indent=1, sort_keys=True), encoding="utf-8", newline="\n")
    print(f"sources: {checked} checked, {bad} failed")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", default=[], help="glob over claim ids, e.g. 'C09.*'")
    ap.add_argument("--render", action="store_true", help="render only; run nothing")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--sources", action="store_true", help="check cited sources only; run no commands")
    args = ap.parse_args()

    ids = [c.id for c in ALL]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        print("duplicate claim ids:", ", ".join(sorted(dupes)))
        return 2

    have = env.available()
    if args.list:
        for c in ALL:
            missing = [n for n in c.needs if not have.get(n)]
            state = c.kind if c.kind != "run" else ("runnable" if not missing else f"needs {', '.join(missing)}")
            print(f"{c.id:8} {state:28} {c.title}")
        return 0

    failures = 0
    if not args.render:
        failures += check_sources()
    if not args.render and not args.sources:
        chosen = [c for c in ALL if c.kind == "run" and not c.same_as
                  and (not args.only or any(fnmatch.fnmatch(c.id, pat) for pat in args.only))]
        ran = 0
        for c in chosen:
            missing = [n for n in c.needs if not have.get(n)]
            if missing:
                print(f"skip  {c.id:8} needs {', '.join(missing)} (keeping any recorded result)")
                continue
            rec = runner.run_claim(c)
            ran += 1
            mark = "ok  " if rec["status"] == "PASS" else "FAIL"
            print(f"{mark}  {c.id:8} {c.title}" + ("" if rec["status"] == "PASS" else f"\n      {rec['detail']}"))
            failures += rec["status"] != "PASS"
        if ran:
            # Merge rather than replace: a partial run on a machine without, say,
            # oxi-gen must not drop the row that earlier records were made with.
            path = EVIDENCE / "outputs" / "_environment.json"
            path.parent.mkdir(exist_ok=True)
            old = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
            path.write_text(json.dumps({**old, **env.versions()}, indent=1), encoding="utf-8", newline="\n")

    envfile = EVIDENCE / "outputs" / "_environment.json"
    environment = json.loads(envfile.read_text(encoding="utf-8")) if envfile.is_file() else {}
    targets = render.write_annotated(ALL)
    intro = (EVIDENCE / "harness" / "intro.md").read_text(encoding="utf-8")
    render.write_evidence(ALL, targets, environment, intro)
    print(f"wrote EVIDENCE.md and manual/ ({len(ALL)} claims)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
