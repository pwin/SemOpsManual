"""Chapter 13 §13.2 and Chapter 11 §11.8: validation through holosdb.

    python scripts/holosdb_validate.py DATA SHAPES [SPARQL_SHAPES]

Store.validate() returns a dictionary, so a caller has a `conforms` key to test
rather than an exit code. Its native engine refuses a shapes graph that uses
anything beyond SHACL Core, rather than skipping the constraint.

Each validation here runs on a freshly loaded store, because validate() writes
the shapes into the store it validates (see holosdb_validate_repeat.py).
"""
import sys

from holosdb import HolosError, Store

sys.stdout.reconfigure(encoding="utf-8")


def fresh() -> Store:
    store = Store()
    store.load(sys.argv[1])
    return store


print("adapted:", fresh().validate(sys.argv[2]))
print("native: ", fresh().validate(sys.argv[2], engine="native"))
if len(sys.argv) > 3:
    try:
        print("native, sh:sparql shapes:", fresh().validate(sys.argv[3], engine="native"))
    except HolosError as exc:
        print(f"native, sh:sparql shapes: HolosError: {exc}")
