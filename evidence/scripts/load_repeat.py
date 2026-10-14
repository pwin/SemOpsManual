"""Chapter 14 §14.4: the seed decides most of owlready2's load, and not all of it.

    python scripts/load_repeat.py work/C14_08 15

Loads the merged acme ontology into owlready2 with owlready2_probe.py, N times
per condition, each in a fresh process, and counts the outcomes:

  1. PYTHONHASHSEED=0, each load from a fresh temporary directory, as the
     suite's bridge does.
  2. PYTHONHASHSEED=0 and 5, with two other sources of variation fixed: one
     load path for every run, and rdflib's blank-node labels numbered instead
     of random (PROBE_DIR and PROBE_FIXED_BNODES).

If the seed were the only input left in (2), each seed would give one outcome
every time. It does not quite: the remaining cause is not identified. Every
failure is reported with the entity owlready2 was building.
"""
import collections
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
work, n = Path(sys.argv[1]).resolve(), int(sys.argv[2])
files = ["fixtures/acme_robotics/acme-org-v1.ttl", "fixtures/acme_robotics/reference_vocab/org.ttl",
         "fixtures/acme_robotics/reference_vocab/foaf.rdf"]
failed_on = collections.Counter()


def load(seed, pinned):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    for k in ("PROBE_DIR", "PROBE_FIXED_BNODES"):
        env.pop(k, None)
    if pinned:
        env.update(PROBE_DIR=str(work / "fixed"), PROBE_FIXED_BNODES="1")
    out = subprocess.run([sys.executable, "scripts/owlready2_probe.py", *files], env=env,
                         capture_output=True, text=True, encoding="utf-8").stdout
    m = re.search(r"failed while building <([^>]+)>", out)
    if m:
        failed_on[m.group(1)] += 1
        return "failed"
    return "loaded" if "loaded the merged ontology" in out else "other"


def tally(seed, pinned):
    t = collections.Counter(load(seed, pinned) for _ in range(n))
    return f"loaded {t['loaded']} of {n}, failed {t['failed']} of {n}" + (f", other {t['other']}" if t["other"] else "")


print(f"1. PYTHONHASHSEED=0, fresh temporary directory: {tally(0, False)}")
print(f"2. PYTHONHASHSEED=0, fixed path and blank-node labels: {tally(0, True)}")
print(f"3. PYTHONHASHSEED=5, fixed path and blank-node labels: {tally(5, True)}")
print("failures were while building: " + (", ".join(f"<{k}> ({v})" for k, v in failed_on.items()) or "nothing"))
