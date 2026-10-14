"""Summarise a full_results.csv the way the manual's tables do.

    python scripts/summarise_findings.py work/C09_04/own/full_results.csv
    python scripts/summarise_findings.py FILE --by focus --check DAT-002

Prints one line per check id (count, severity, title), then the totals. With
--by focus, prints each finding's check, focus node, path and value instead,
optionally limited to one check id.
"""
import argparse
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8")

ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("--by", choices=["check", "focus"], default="check")
ap.add_argument("--check", help="only this check id")
args = ap.parse_args()

with open(args.csv, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
if args.check:
    rows = [r for r in rows if r["check_id"] == args.check]

if args.by == "focus":
    for r in rows:
        print(f"{r['check_id']}  focus={r['focus_node']}  path={r['path'] or '-'}  value={r['value'] or '-'}")
else:
    counts = collections.Counter((r["check_id"], r["severity"], r["title"]) for r in rows)
    for (cid, sev, title), n in sorted(counts.items()):
        print(f"{n:3} x {cid:8} {sev:9} {title}")
sev = collections.Counter(r["severity"] for r in rows)
print(f"total {len(rows)}: {sev.get('Violation', 0)} Violation, {sev.get('Warning', 0)} Warning, "
      f"{sev.get('Info', 0)} Info")
