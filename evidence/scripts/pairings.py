"""Chapter 1 §1.1: point-to-point integration pairings for n systems, n(n-1)/2.

    python scripts/pairings.py 4 10 20
"""
import sys

for n in map(int, sys.argv[1:]):
    print(f"{n} systems: {n * (n - 1) // 2} potential point-to-point pairings; "
          f"{n} mappings to a shared model")
