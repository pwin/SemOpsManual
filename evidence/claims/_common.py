"""Shared constants, permalinks and checks for the claim modules."""
from harness.model import Claim, Service, Source, Step, all_of, by_check, findings, ok, rows  # noqa: F401

ACME = "fixtures/acme_robotics"
V1 = f"{ACME}/acme-org-v1.ttl"
V2 = f"{ACME}/acme-org-v2.ttl"
FOAF = f"{ACME}/reference_vocab/foaf.rdf"
ORG = f"{ACME}/reference_vocab/org.ttl"
OWN = "https://acme.example.org/ns/"
OWN_DATA = "https://acme.example.org/"
SUITE = "ontology-quality-suite"
TSC = ("node node_modules/typescript/bin/tsc --noEmit --strict --module nodenext "
       "--moduleResolution nodenext --target es2022 --skipLibCheck")
TSX = "node node_modules/tsx/dist/cli.mjs"
HOLOS_PORT = 7899
HOLOS_URL = f"http://127.0.0.1:{HOLOS_PORT}"

# ---------------------------------------------------------------- permalinks (fixed commits)

_GH = "https://github.com/pwin"
REPOS = {
    "suite": (f"{_GH}/consolidated-ontology-quality-suite-python", "a24d3456c3329fe93b31cadefdfdf05329e82442"),   # v0.24.1
    "webapp": (f"{_GH}/consolidated-ontology-quality-suite-webapp", "534ce517f9aabc0c27d33f1af5eb85f88296a16f"),   # v0.16.1
    "shacl": (f"{_GH}/SHACL_Engine", "986c31ba4e071560d51fed36e99abd8cb3747a87"),   # v0.3.4
    "holos": (f"{_GH}/triplestore", "4d1ad30da6848feaea6e28713b99a2defd69d859"),   # v0.22.0
    "tarka": (f"{_GH}/tarka", "88fe6184ffc77ee2a46b676cbcb1190620b52c49"),
    "testing": (f"{_GH}/consolidated-ontology-quality-suite-python-testing", "6cdfb14a3c2857b61dcb32f49f56a4829b0d0664"),
    "manual": (f"{_GH}/SemOpsManual", ""),
}


def commit(repo: str, sha: str) -> str:
    return f"{REPOS[repo][0]}/commit/{sha}"


def file(repo: str, path: str, lines: str = "", ref: str = "") -> str:
    base, pinned = REPOS[repo]
    anchor = ""
    if lines:
        a, _, b = lines.partition("-")
        anchor = f"#L{a}" + (f"-L{b}" if b else "")
    return f"{base}/blob/{ref or pinned}/{path}{anchor}"


def src(label: str, url: str, quote: str = "") -> Source:
    return Source(label, url, quote)


# ---------------------------------------------------------------- checks

def has(step: int, *texts: str):
    """Every text appears in step `step`'s combined output."""
    def check(r):
        out = r[step].out
        missing = [t for t in texts if t not in out]
        return ok(not missing, f"step {step + 1} output contains {', '.join(repr(t) for t in texts)}",
                  f"step {step + 1} output lacks {', '.join(repr(t) for t in missing)}")
    return check


def lacks(step: int, *texts: str):
    def check(r):
        out = r[step].out
        present = [t for t in texts if t in out]
        return ok(not present, f"step {step + 1} output has none of {', '.join(repr(t) for t in texts)}",
                  f"step {step + 1} output contains {', '.join(repr(t) for t in present)}")
    return check


def exit_code(step: int, code: int):
    def check(r):
        return ok(r[step].rc == code, f"step {step + 1} exits {code}", f"step {step + 1} exits {r[step].rc}, not {code}")
    return check


def nonzero(step: int):
    def check(r):
        return ok(r[step].rc != 0, f"step {step + 1} exits non-zero ({r[step].rc})", f"step {step + 1} exits 0")
    return check


def totals(step: int, total: int, v: int = None, w: int = None, i: int = None):
    """'Findings: N total (V Violation, W Warning, I Info)' as stated."""
    def check(r):
        f = findings(r[step].out)
        if not f:
            return False, f"step {step + 1}: no Findings line"
        want = (total, v, w, i)
        good = all(x is None or x == y for x, y in zip(want, f))
        return ok(good, f"step {step + 1}: {f[0]} findings ({f[1]} V, {f[2]} W, {f[3]} I)",
                  f"step {step + 1}: got {f}, expected {want}")
    return check


def counts(csv_rel: str, expected: dict, exact: bool = True):
    """Per-check counts in a full_results.csv under the claim's work dir."""
    def check(r):
        got = by_check(r.file(csv_rel))
        if exact:
            good = got == expected
        else:
            good = all(got.get(k) == v for k, v in expected.items())
        return ok(good, f"{csv_rel}: {dict(sorted(got.items()))}",
                  f"{csv_rel}: got {dict(sorted(got.items()))}, expected {expected}")
    return check


def suite_at_least(*version: int) -> bool:
    """Whether the installed ontology-quality-suite is at least this version.

    Checks run in the same environment as the steps, so this is the suite the
    commands just used. Claims whose expected output changed in a release test
    for it, so that the evidence passes on either side of the change and says
    which side it was run on."""
    from importlib import metadata
    installed = tuple(int(x) for x in metadata.version("ontology-quality-suite").split(".")[:3])
    return installed >= version


def by_version(newer: tuple, if_newer, otherwise):
    """A check that applies `if_newer` from suite version `newer`, else `otherwise`."""
    def check(r):
        passed, detail = (if_newer if suite_at_least(*newer) else otherwise)(r)
        from importlib import metadata
        return passed, f"suite {metadata.version('ontology-quality-suite')}: {detail}"
    return check


def _parse(text: str, name: str):
    import re
    m = re.search(rf"\b{re.escape(name)} (\d+)\.(\d+)\.(\d+)", text)
    return tuple(int(x) for x in m.groups()) if m else None


def by_tool(step: int, name: str, newer: tuple, if_newer, otherwise):
    """Like by_version, for a release binary: step `step` printed '<name> X.Y.Z'
    (its --version), and `if_newer` applies from version `newer`."""
    def check(r):
        found = _parse(r[step].out, name)
        if found is None:
            return False, f"step {step + 1}: no '{name} X.Y.Z' version line"
        passed, detail = (if_newer if found >= newer else otherwise)(r)
        return passed, f"{name} {'.'.join(map(str, found))}: {detail}"
    return check


def by_npm(package: str, newer: tuple, if_newer, otherwise):
    """Like by_version, for an npm package installed under node_modules/."""
    def check(r):
        import json
        from harness.model import EVIDENCE
        pj = EVIDENCE / "node_modules" / package / "package.json"
        found = tuple(int(x) for x in json.loads(pj.read_text(encoding="utf-8"))["version"].split(".")[:3])
        passed, detail = (if_newer if found >= newer else otherwise)(r)
        return passed, f"npm {package} {'.'.join(map(str, found))}: {detail}"
    return check


def checks(*fns):
    def check(r):
        return all_of(*(f(r) for f in fns))
    return check
