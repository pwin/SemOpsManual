"""Chapter 13: two facts about the holosdb wheel.

    python scripts/holos_facts.py

How many GeoSPARQL functions this build registers, and whether the wheel
carries RocksDB persistence.
"""
import sys

import holosdb

sys.stdout.reconfigure(encoding="utf-8")
fns = holosdb.geosparql_functions()
print(f"GeoSPARQL functions registered: {len(fns)}")
print(f"includes geof:buffer and geof:boundary: "
      f"{any(f.endswith('buffer') for f in fns)} / {any(f.endswith('boundary') for f in fns)}")
print(f"persistence (RocksDB) in this wheel: {holosdb.has_rocksdb()}")
