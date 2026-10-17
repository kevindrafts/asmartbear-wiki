"""Read public source metadata without merging distinct discovery ledgers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_sources(root=ROOT):
    rows = []
    for name in ('articles', 'podcasts'):
        path = root / 'catalog' / (name + '.jsonl')
        if name == 'podcasts' and not path.exists():
            continue
        rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    return rows
