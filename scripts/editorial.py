"""Save manually authored notes after complete source reading, binding review to hash."""
import json
import sys
import yaml
from scripts.ingest import ROOT, CACHE, write_json, export


def save(entries):
    ledger = json.loads((CACHE / 'ledger.json').read_text())
    for slug, item in entries.items():
        source = json.loads((CACHE / (slug + '.json')).read_text())
        row = next(r for r in ledger.values() if r.get('id') == slug)
        meta = {'title': source['title'], 'source': source['canonical_url'], 'author': 'Jason Cohen',
                'published': source['published'], 'modified': source['modified'],
                'source_type': source['source_type'], 'status': 'reviewed',
                'source_sha256': source['body_sha256'], 'topics': item['topics']}
        note = '---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + '---\n\n'
        note += '# ' + source['title'] + '\n\n'
        note += '[Read Jason Cohen’s original](' + source['canonical_url'] + ') · Unofficial editorial note.\n\n'
        note += item['text'].strip() + '\n\n'
        note += 'Related: ' + ' · '.join('[' + t.replace('-', ' ').title() + '](../wiki/topics/' + t + '.md)' for t in item['topics']) + '\n'
        (ROOT / 'processed' / (slug + '.md')).write_text(note)
        row.update({'read_status': 'complete', 'note_status': 'reviewed', 'reviewed_body_sha256': source['body_sha256'],
                    'tags': item['topics'], 'synthesis_references': ['wiki/topics/' + t + '.md' for t in item['topics']]})
    write_json(CACHE / 'ledger.json', ledger)
    export(ledger)
    print('Saved', len(entries), 'reviewed notes')


if __name__ == '__main__':
    save(json.load(sys.stdin))
