"""Stage only approved public Markdown and generated metadata views."""
import json
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'site/docs'


def stage():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)
    for folder in ('processed', 'wiki', 'reports'):
        for p in (ROOT / folder).rglob('*.md'):
            if p == ROOT / 'wiki/INDEX.md':
                continue
            dest = DOCS / p.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dest)
    for name in ('ATTRIBUTION.md', 'CONTENT-LICENSE.md'):
        shutil.copyfile(ROOT / name, DOCS / name)
    (DOCS / 'assets').mkdir()
    shutil.copyfile(ROOT / 'site/wiki.css', DOCS / 'assets/wiki.css')
    shutil.copyfile(ROOT / 'site/wiki.js', DOCS / 'assets/wiki.js')
    rows = [json.loads(s) for s in (ROOT / 'catalog/articles.jsonl').read_text().splitlines()]
    topics = defaultdict(list)
    catalog = '# Article catalog\n\nOriginal commentary, with direct links to every source. Dates below are source metadata.\n\n'
    for row in rows:
        note = ROOT / 'processed' / (row['id'] + '.md')
        if note.exists():
            catalog += f"- [{row['title']}]({row['id']}.md) · Published {(row.get('published') or 'Unknown')[:10]} · Modified {(row.get('modified') or 'Unknown')[:10]} · {row['classification']}\n"
            staged = DOCS / 'processed' / (row['id']+'.md')
            text = staged.read_text()
            parts = text.split('---', 2)
            # `source` is reserved by the MkDocs theme for source-code links.
            parts[1] = parts[1].replace('\nsource:', '\noriginal_source:')
            prose = parts[2]
            heading_end = prose.index('\n', prose.index('# '))
            dates = f"\n\n*Source published: {row.get('published') or 'unknown'} · Modified: {row.get('modified') or 'unknown'} · Type: {row['classification']}*\n"
            staged.write_text('---'.join(parts[:2])+'---'+prose[:heading_end]+dates+prose[heading_end:])
            for topic in row.get('tags', []):
                topics[topic].append(row)
        else:
            raise ValueError('Missing reviewed note: '+row['id'])
    (DOCS / 'processed/index.md').write_text(catalog)
    for topic, sources in topics.items():
        p = DOCS / 'wiki/topics' / (topic + '.md')
        if not p.exists():
            raise ValueError('Missing authored topic: '+topic)
        with p.open('a') as out:
            out.write('\n## Article notes\n\n')
            for r in sources:
                out.write(f"- [{r['title']}](../../processed/{r['id']}.md)\n")
    for folder, heading in [('topics', 'Topics'), ('guides', 'Decision guides'), ('reading-paths', 'Reading paths')]:
        target = DOCS / 'wiki' / folder
        target.mkdir(parents=True, exist_ok=True)
        index = '# ' + heading + '\n\n'
        for p in sorted(target.glob('*.md')):
            if p.name != 'index.md':
                title = next((line[2:] for line in p.read_text().splitlines() if line.startswith('# ')), p.stem)
                index += f'- [{title}]({p.name})\n'
        (target / 'index.md').write_text(index)
    reports = DOCS / 'reports'
    (reports/'index.md').write_text('# Project reports\n\n'+'\n'.join(f'- [{p.stem.replace(chr(45), chr(32)).title()}]({p.name})' for p in sorted(reports.glob('*.md')) if p.name!='index.md')+'\n')
    shutil.copyfile(ROOT / 'wiki/INDEX.md', DOCS / 'index.md')
    # Exact-path backlinks are generated from public Markdown only.
    import re
    snapshots = {p: p.read_text() for p in DOCS.rglob('*.md')}
    import os
    incoming = defaultdict(list)
    for other, original in snapshots.items():
        title = next((s[2:] for s in original.splitlines() if s.startswith('# ')), other.stem)
        targets = {(other.parent / link).resolve() for link in re.findall(r'\]\(([^)]+\.md)(?:#[^)]*)?\)', original)}
        for target in targets:
            if target != other.resolve(): incoming[target].append((other,title))
    for p in snapshots:
        backlinks = [f'- [{title}]({os.path.relpath(other,p.parent)})' for other,title in incoming[p.resolve()]]
        if backlinks:
            with p.open('a') as out:
                out.write('\n## Linked from\n\n' + '\n'.join(backlinks) + '\n')


if __name__ == '__main__':
    stage()
