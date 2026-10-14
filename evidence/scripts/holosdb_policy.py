"""Chapter 13 §13.2: access policy at the index scan, through the holosdb package.

    python scripts/holosdb_policy.py data/policy/hr.trig

Runs the same few queries as different principals under different policies and
prints what each one gets back. Note the fluent API: every Policy method returns
a new policy, so the calls are chained or assigned, never made as statements.
"""
import sys

from holosdb import HolosError, Policy, Principal, Store

sys.stdout.reconfigure(encoding="utf-8")
store = Store()
store.load(sys.argv[1])

NAMES = """PREFIX ex: <http://example.com/>
SELECT ?name ?salary WHERE { GRAPH ?g { ?e ex:name ?name
                              OPTIONAL { ?e ex:salary ?salary } } } ORDER BY ?name"""
COUNT = """PREFIX ex: <http://example.com/>
SELECT (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?e ex:salary ?s } }"""
GRAPHS = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } ORDER BY ?g"

alice = Principal("urn:user:alice")
alice_hr = Principal("urn:user:alice", roles=["hr"])
alice_cleared = Principal("urn:user:alice", clearance=3)

deny_salary = Policy().deny_predicate("http://example.com/salary", except_role="hr")
label_reviews = Policy().label_graph("http://example.com/reviews", 3)
fail_closed = Policy().deny_predicate("http://example.com/salary").fail_closed()


def rows(q, **kw):
    return [{k: str(v) for k, v in r.to_dict().items()} for r in store.query(q, **kw)]


def show(label, q, **kw):
    try:
        print(f"{label}:")
        for r in rows(q, **kw):
            print("   ", ", ".join(f"{k}={v}" for k, v in r.items()))
    except HolosError as exc:
        print(f"    HolosError: {exc}")


show("1. names and salaries, no policy", NAMES)
show("2. salary denied except to role hr, asked by alice", NAMES, principal=alice, policy=deny_salary)
show("3. the same, asked by alice with role hr", NAMES, principal=alice_hr, policy=deny_salary)
show("4. COUNT of salaries without the role", COUNT, principal=alice, policy=deny_salary)
show("5. named graphs, reviews labelled at level 3, no clearance", GRAPHS, principal=alice, policy=label_reviews)
show("6. named graphs, with clearance 3", GRAPHS, principal=alice_cleared, policy=label_reviews)
show("7. salary denied with fail_closed()", NAMES, principal=alice, policy=fail_closed)

# The mistake the manual warns about: calling a Policy method as a statement.
p = Policy()
p.deny_predicate("http://example.com/salary")      # returns a new policy; p is unchanged
show("8. (mistake) policy method called as a statement", COUNT, principal=alice, policy=p)
