"""Save authored synthesis with explicit, validated source references."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def save(entries):
    rows={r['id']:r for r in map(json.loads,(ROOT/'catalog/articles.jsonl').read_text().splitlines())}
    for path,item in entries.items():
        p=ROOT/'wiki'/path
        if p.parent.name not in ('topics','guides','reading-paths') or p.suffix!='.md':raise ValueError(path)
        refs=[]
        def expand(m):
            slug,label=m.group(1).split('|',1);r=rows[slug]
            if slug not in refs:refs.append(slug)
            return '['+label+']('+r['canonical_url']+')'
        text=re.sub(r'\{\{([^}]+)\}\}',expand,item['text'])
        if len(refs)<2:raise ValueError('Need cross-article grounding: '+path)
        text='# '+item['title']+'\n\n'+text+'\n\n## Source notes\n\n'
        text+='\n'.join('- ['+rows[s]['title']+'](../../processed/'+s+'.md)' for s in refs)+'\n'
        p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    print('Saved',len(entries),'synthesis pages')
if __name__=='__main__':save(json.load(sys.stdin))
