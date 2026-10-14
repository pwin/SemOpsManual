"""Count the Mermaid diagrams in the manual's chapters (the PDF renders these).

    python scripts/count_mermaid.py ..
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1])
total = 0
for p in sorted((repo / "docs").glob("*.md")):
    n = p.read_text(encoding="utf-8").count("```mermaid")
    total += n
    print(f"{n}  docs/{p.name}")
print(f"{total} diagrams in the chapters; README has {(repo / 'README.md').read_text(encoding='utf-8').count('```mermaid')} more")
