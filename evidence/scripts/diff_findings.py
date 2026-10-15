"""Compare two full_results.csv files finding by finding.

    python scripts/diff_findings.py BEFORE.csv AFTER.csv

A finding is its check id, focus node, path and value. Prints how many findings
AFTER has that BEFORE lacks, and the reverse, each broken down by check id. Used
in Chapter 7 §7.4 to show that an RDFS closure moves findings in both directions.
"""
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8")


def findings(path):
    with open(path, encoding="utf-8", newline="") as f:
        return collections.Counter((r["check_id"], r["focus_node"], r["path"], r["value"]) for r in csv.DictReader(f))


before, after = findings(sys.argv[1]), findings(sys.argv[2])
for label, delta in (("gained", after - before), ("lost", before - after)):
    by_check = collections.Counter(k[0] for k in delta.elements())
    parts = ", ".join(f"{c} {n}" for c, n in sorted(by_check.items(), key=lambda kv: (-kv[1], kv[0])))
    print(f"{label} {sum(delta.values())}: {parts or 'nothing'}")
print(f"before {sum(before.values())}, after {sum(after.values())}")
