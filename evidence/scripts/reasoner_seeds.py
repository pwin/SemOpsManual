"""Chapter 14 §14.4: whether HermiT runs is decided, almost entirely, by PYTHONHASHSEED.

    python scripts/reasoner_seeds.py work/C14_06 10 0 5

Runs the suite's `ontology` command on the acme fixture N times for each seed
given, each run in a fresh process with that PYTHONHASHSEED, and counts what
the reasoner did: REA-020 + REA-021 when HermiT ran, REA-022 when it did not.

"Almost": under a fixed seed the odd run still goes the other way, and fixing
the load path and rdflib's blank-node labels does not stop it. load_repeat.py
measures that.
"""
import collections
import csv
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
work, n, seeds = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3:]
messages = collections.Counter()
for seed in seeds:
    tally = collections.Counter()
    for i in range(1, n + 1):
        out = work / f"seed{seed}-run{i}"
        env = dict(os.environ, PYTHONHASHSEED=seed)
        subprocess.run([sys.executable, "-m", "ontology_suite", "ontology",
                        "--ontology", "fixtures/acme_robotics/acme-org-v1.ttl",
                        "--import-dir", "fixtures/acme_robotics",
                        "--out-dir", str(out), "--reports", "minimal"],
                       env=env, capture_output=True, text=True)
        with open(out / "full_results.csv", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        ids = {r["check_id"] for r in rows}
        for r in rows:
            if r["check_id"] == "REA-022":
                messages[r["message"].split(". Only the always-on")[0]] += 1
        tally["ran" if "REA-021" in ids else "did not run" if "REA-022" in ids else "neither"] += 1
    print(f"PYTHONHASHSEED={seed}: HermiT ran {tally['ran']} of {n}, did not run {tally['did not run']} of {n}"
          + (f", neither {tally['neither']}" if tally["neither"] else ""))
print("REA-022 messages seen:")
for m, k in messages.most_common():
    print(f"  {k} x  {m}")
