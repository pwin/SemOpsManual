<p align="center">
  <img src="../assets/semantechs-logo-320.png" alt="Semantechs" width="120">
</p>

# Notebooks

Three runnable notebooks covering the parts of the manual where *watching* the
tool behave teaches more than reading about it — particularly the failure modes,
which are only convincing when you see a command report success on work it never
did.

| Notebook | Chapters | What you see happen |
|---|---|---|
| [1 — Validation and the gate](01-validation-and-the-gate.ipynb) | [8](../docs/08-model-and-validate.md), [9](../docs/09-continuous-integration.md) | An unscoped gate drowning in other people's findings, the one flag that fixes it, and the near-miss that returns a confidently empty report |
| [2 — Rules and inference](02-rules-and-inference.ipynb) | [11](../docs/11-rules-and-inference.md) | SHACL-AF rules deriving triples, and all four ways a rule silently does nothing |
| [3 — Release and change](03-release-and-change.ipynb) | [12](../docs/12-release-and-change.md) | Evidence-based semver, change impact, and a repair applying itself — including the comment it mangles |

## Running them

```bash
pip install ontology-quality-suite shacl jupyterlab
jupyter lab
```

Each notebook is **self-contained**: it writes its own fixtures into a temporary
directory, so nothing needs to exist on disk first and nothing outside that
directory is touched. The setup cell reports which tools it found, and any cell
needing something you do not have says so and skips rather than raising.

Notebook 2 needs the `shacl` CLI on `PATH`, and **0.1.8 or later**. It uses the
CLI for most of its work because the CLI shows the exit code, which is what a CI
job branches on; its last section does the same thing through the Python
binding.

Rules moved twice while this manual was being written — absent from the Python
binding at 0.1.5, CLI-only at 0.1.7, in every binding from 0.1.8. On an older
build the rule cells report:

```
inference='rules' -> ERROR: unknown inference "rules"; use "none" or "rdfs"
```

which is the right failure — it names what it accepts rather than quietly
validating without applying the rules. Check yours with `shacl --version`.

## Why the numbers here are small

The manual reports figures from a real fixture importing the W3C Organization
Ontology and FOAF, where the unscoped run returns close to 300 findings. These
notebooks build a miniature version — one small upstream vocabulary, one
ontology with three deliberate flaws — so the same lesson arrives with numbers
you can check by eye. The shape is identical; only the magnitude differs.

## Editing them

They are generated, not hand-maintained:

```bash
node ../tools/make-notebooks.mjs
```

Edit [`tools/make-notebooks.mjs`](../tools/make-notebooks.mjs) and regenerate.
`.ipynb` is JSON with a lot of required per-cell boilerplate, and three notebooks
sharing a preamble is exactly where hand-edited JSON drifts.

Verify a change actually runs by extracting the code cells and executing them in
order — they use no magics, so this is equivalent to running the notebook:

```bash
python -c "
import json,pathlib,sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
print('\n\n'.join(''.join(c['source']) for c in d['cells'] if c['cell_type']=='code'))
" 02-rules-and-inference.ipynb > /tmp/nb.py && python /tmp/nb.py
```
