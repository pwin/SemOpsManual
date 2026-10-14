<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# Evidence for the SemOps Manual

This folder holds the proof behind the manual's claims, and a copy of the manual
that links to it.

| | |
|---|---|
| [**EVIDENCE.md**](EVIDENCE.md) | Every checkable claim in the manual: the command or code, the input data, the recorded output, and what was checked. Start here, or from the annotated manual |
| [**manual/**](manual/README.md) | The annotated edition: the manual, unchanged, with an *Evidence* link after each checked claim, and links back from each evidence entry |
| [`verify.py`](verify.py) | Runs the claims, checks the quoted sources against local clones, and regenerates both of the above |
| [`claims/`](claims/) | The claims, one module per chapter: where each sits in the manual, its commands, and the check applied to their output |
| [`scripts/`](scripts/) | Small, readable scripts the claims run, for the parts that need code rather than a command line |
| [`data/`](data/) | Input files written for particular claims, small enough to read in full |
| [`fixtures/acme_robotics/`](fixtures/acme_robotics/) | The suite's own fixture, copied unchanged ([provenance](fixtures/NOTICE.md)) |
| [`outputs/`](outputs/) | The recorded runs, one JSON file per claim, with machine-specific paths normalised |
| [`harness/`](harness/) | The runner and the renderer |
| [`tools/fetch_binaries.py`](tools/fetch_binaries.py) | Downloads and checksum-verifies the release binaries |
| [`tools/check_links.py`](tools/check_links.py) | Checks every relative link and anchor in EVIDENCE.md and the annotated manual |

## Setting up

```bash
cd evidence
python -m venv .venv
.venv/bin/pip install -r requirements.txt        # Windows: .venv\Scripts\pip install -r requirements.txt
python tools/fetch_binaries.py
npm ci
.venv/bin/python verify.py
```

What gets installed, and from where:

- **PyPI:** `ontology-quality-suite` 0.22.0, `shacl` 0.3.2, `holosdb` 0.21.0,
  `tarka-rdf` 0.1.1, and `pyoxigraph` 0.5.11 (a second SPARQL engine, used only as
  a witness in one claim).
- **GitHub releases:** the `shacl`, `tarka`, `holos` and `holos-server` commands,
  verified against each release's `SHA256SUMS`, unpacked under `bin/`.
- **npm:** `ontology-suite` (the DSL), `shacl-wasm-node`, `holos-wasm-node`,
  TypeScript and `tsx`, under `node_modules/`.

Nothing is installed outside this folder. `.venv/`, `bin/`, `node_modules/` and
`work/` (each run's scratch output) are not committed.

Some claims need more than this folder: a Java runtime (the DL reasoner), network
access (gist), port 7899 free (the live-store claims start `holos-server` there), a
clone of the testing repository (`EVIDENCE_TESTING_REPO`), and local clones of the
six repositories for the source checks (`EVIDENCE_REPOS`). `python verify.py --list`
says which claims can run here; the rest keep their recorded result. The
introduction to [EVIDENCE.md](EVIDENCE.md) has the details.

## Changing a claim

Edit the claim in `claims/chNN.py`, run `python verify.py --only 'CNN.*'`, and read
the regenerated entry in EVIDENCE.md. If a claim's text moves in the manual, update
its snippet: the renderer refuses to build if any snippet can no longer be found,
which is how the two documents are kept in step.
