"""Audit staged files and existing history without printing source or secret values."""
import argparse,json,re,subprocess
from pathlib import Path
from scripts.ingest import CACHE
from scripts.validate import inventory_errors

def git(*args):return subprocess.check_output(['git',*args])
def run(cache_audit=False):
    staged=git('diff','--cached','--name-only','--diff-filter=ACMR','-z').decode().split('\0')
    staged=[p for p in staged if p];errors=['forbidden staged path: '+p for p in inventory_errors(staged)]
    blobs={}
    for line in git('rev-list','--objects','--all').decode().splitlines():
        oid,_,name=line.partition(' ')
        if git('cat-file','-t',oid).strip()==b'blob':blobs['history:'+name+':'+oid[:8]]=git('cat-file','blob',oid)
    for p in staged:blobs['staged:'+p]=git('show',':'+p)
    patterns=[rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{40,}',rb'AKIA[A-Z0-9]{16}',rb'sk-(?:proj-)?[A-Za-z0-9_-]{40,}']
    grams=set();source_hashes=set()
    if cache_audit:
        rows=[json.loads(s) for s in Path('catalog/articles.jsonl').read_text().splitlines()]
        for r in rows:
            source=json.loads((CACHE/(r['id']+'.json')).read_text())
            words=re.findall(r'\w+',source['body'].lower())
            grams.update(tuple(words[i:i+30]) for i in range(max(0,len(words)-29)))
            source_hashes.add(r['html_sha256']);source_hashes.add(r['body_sha256'])
    import hashlib
    for name,data in blobs.items():
        if any(re.search(pattern,data) for pattern in patterns):errors.append('possible credential: '+name)
        if hashlib.sha256(data).hexdigest() in source_hashes:errors.append('source capture: '+name)
        if cache_audit:
            words=re.findall(r'\w+',data.decode('utf-8',errors='replace').lower())
            if any(tuple(words[i:i+30]) in grams for i in range(max(0,len(words)-29))):errors.append('source passage: '+name)
    print(json.dumps({'staged_files':len(staged),'checked_blobs':len(blobs),'cache_audit':cache_audit,'errors':errors},indent=2))
    return bool(errors)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache-audit',action='store_true');a=p.parse_args();raise SystemExit(run(a.cache_audit))
