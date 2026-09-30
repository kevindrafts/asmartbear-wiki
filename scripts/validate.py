"""Fail closed on incomplete coverage, invalid references, or source-text leakage."""
import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import markdown
import yaml
from bs4 import BeautifulSoup
from scripts.ingest import validate_dates, canonical_groups, CACHE
ROOT = Path(__file__).resolve().parents[1]
PRIMARY = re.compile(r'https://longform\.asmartbear\.com/[a-z0-9-]+/')

def validate_note(text, url):
    errors=[]
    if not re.search(r'\]\('+re.escape(url)+r'(?:#[^)]*)?\)',text): errors.append('missing source citation')
    if 'status: reviewed' not in text: errors.append('missing reviewed status')
    return errors

def overlapping_runs(note, source):
    words=lambda s:re.findall(r'\w+',s.lower())
    return max((m.size for m in difflib.SequenceMatcher(None,words(note),words(source),autojunk=False).get_matching_blocks()),default=0)

def validate_catalog(rows):
    errors=[];ids=set()
    for r in rows:
        slug=r.get('id','MISSING')
        if not re.fullmatch(r'[a-z0-9-]+',slug) or slug in ids: errors.append(slug+': invalid or duplicate ID')
        ids.add(slug)
        for key in ('title','canonical_url','url','tags','synthesis_references'):
            if not r.get(key): errors.append(slug+': missing '+key)
        if not validate_dates(r.get('published'),r.get('modified'),r.get('sitemap_lastmod')): errors.append(slug+': invalid date')
        if r.get('read_status')!='complete' or r.get('note_status')!='reviewed' or r.get('status')!='fetched': errors.append(slug+': incomplete review/fetch')
        if not re.fullmatch('[0-9a-f]{64}',r.get('body_sha256','')) or r.get('body_sha256')!=r.get('reviewed_body_sha256'): errors.append(slug+': review hash mismatch')
        if r.get('classification') not in ('article','mailbag'): errors.append(slug+': invalid included classification')
        if any(k in r for k in ('body','html','images','tables','text')): errors.append(slug+': source payload in catalog')
    for url, aliases in canonical_groups(rows).items():
        if len(aliases)>1: errors.append('duplicate canonical: '+url)
    return errors

def check_links(root):
    errors=[];anchors={}
    for p in root.rglob('*.md'):
        anchors[p.resolve()]={n.get('id') for n in BeautifulSoup(markdown.markdown(p.read_text(),extensions=['toc']), 'html.parser').select('[id]')}
    for p in root.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            link=link.split(' "')[0];u=urlsplit(link)
            if u.scheme or link.startswith('//'): continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
            if not target.is_file(): errors.append(str(p.relative_to(root))+': missing '+link)
            elif u.fragment and target in anchors and unquote(u.fragment) not in anchors[target]: errors.append(str(p.relative_to(root))+': missing anchor '+link)
    return errors

def check_reachability(root):
    pages={p.resolve():p for p in root.rglob('*.md')}
    seen=set();pending=[(root/'index.md').resolve()]
    while pending:
        p=pending.pop()
        if p in seen or p not in pages: continue
        seen.add(p)
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            u=urlsplit(link)
            if not u.scheme: pending.append((p.parent/unquote(u.path)).resolve())
    return sorted(str(p.relative_to(root)) for key,p in pages.items() if key not in seen)

def inventory_errors(paths):
    bad=[]
    for name in paths:
        p=Path(name)
        if any(part in ('raw','source-cache','captures','.venv','node_modules') for part in p.parts) or p.name=='.env' or p.suffix in ('.pem','.key','.html'):
            bad.append(name)
    return bad

def check_synthesis(text):
    return [] if len(set(PRIMARY.findall(text)))>=2 else ['synthesis needs at least two distinct primary sources']

def leak_findings(text, sources, minimum=30):
    # Exact normalized 30-word runs flag unattributed/reproduced passages efficiently.
    words=re.findall(r'\w+',text.lower());grams={tuple(words[i:i+minimum]) for i in range(max(0,len(words)-minimum+1))}
    findings=[]
    for slug,body in sources.items():
        sw=re.findall(r'\w+',body.lower())
        if any(tuple(sw[i:i+minimum]) in grams for i in range(max(0,len(sw)-minimum+1))): findings.append(slug)
    return findings

def run(require_complete=False, cache_audit=False):
    errors=[]
    rows=[json.loads(s) for s in (ROOT/'catalog/articles.jsonl').read_text().splitlines()]
    errors+=validate_catalog(rows)
    expected={r['id'] for r in rows};actual={p.stem for p in (ROOT/'processed').glob('*.md')}
    if require_complete and actual!=expected: errors.append('note coverage mismatch: '+repr(sorted(actual^expected)))
    for r in rows:
        p=ROOT/'processed'/(r['id']+'.md')
        if not p.exists(): continue
        text=p.read_text();errors += [r['id']+': '+e for e in validate_note(text,r['canonical_url'])]
        meta=yaml.safe_load(text.split('---',2)[1])
        for nk,rk in [('source_sha256','body_sha256'),('published','published'),('modified','modified'),('topics','tags'),('title','title')]:
            if meta.get(nk)!=r.get(rk): errors.append(r['id']+': note metadata mismatch '+nk)
        for ref in r['synthesis_references']:
            if not (ROOT/ref).is_file(): errors.append(r['id']+': missing synthesis '+ref)
        prose=text.split('---',2)[2]
        if '**Boundary:**' not in prose or '**Apply it:**' not in prose: errors.append(r['id']+': missing application/boundary')
    for folder in ('topics','guides','reading-paths'):
        for p in (ROOT/'wiki'/folder).glob('*.md'):
            errors += [str(p.relative_to(ROOT))+': '+e for e in check_synthesis(p.read_text())]
            for source in PRIMARY.findall(p.read_text()):
                if source not in {r['canonical_url'] for r in rows}: errors.append(str(p)+': unknown source '+source)
    docs=ROOT/'site/docs'
    if docs.exists():
        errors+=check_links(docs)
        errors += ['orphan: '+p for p in check_reachability(docs)]
    if cache_audit:
        sources={}
        for r in rows:
            p=CACHE/(r['id']+'.json')
            if not p.exists(): errors.append(r['id']+': missing external source');continue
            d=json.loads(p.read_text());body=d['body'];sources[r['id']]=body
            if hashlib.sha256(body.encode()).hexdigest()!=r['body_sha256']: errors.append(r['id']+': external body hash mismatch')
        # Build one index across every source; check every public prose file and build HTML.
        index={}
        for slug,body in sources.items():
            words=re.findall(r'\w+',body.lower())
            for i in range(max(0,len(words)-29)): index.setdefault(tuple(words[i:i+30]),slug)
        public=list((ROOT/'processed').glob('*.md'))+list((ROOT/'wiki').rglob('*.md'))+list((ROOT/'reports').glob('*.md'))
        public+=list((ROOT/'site/public').rglob('*.html'))
        for p in public:
            text=p.read_text()
            if p.suffix=='.html': text=BeautifulSoup(text,'html.parser').get_text(' ',strip=True)
            words=re.findall(r'\w+',text.lower())
            hits={index[tuple(words[i:i+30])] for i in range(max(0,len(words)-29)) if tuple(words[i:i+30]) in index}
            if hits: errors.append(str(p.relative_to(ROOT))+': source overlap '+','.join(sorted(hits)))
        search=ROOT/'site/public/search/search_index.json'
        if search.exists():
            for d in json.loads(search.read_text())['docs']:
                words=re.findall(r'\w+',d.get('text','').lower())
                if any(tuple(words[i:i+30]) in index for i in range(max(0,len(words)-29))): errors.append('search source overlap: '+d['location'])
    print(json.dumps({'articles':len(rows),'notes':len(actual),'topics':len(list((ROOT/'wiki/topics').glob('*.md'))),'guides':len(list((ROOT/'wiki/guides').glob('*.md'))),'errors':errors},indent=2))
    return bool(errors)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--require-complete',action='store_true');p.add_argument('--cache-audit',action='store_true');a=p.parse_args()
    raise SystemExit(run(a.require_complete,a.cache_audit))
