"""Check every built content page and search asset at the deployed Pages URL."""
import json,time
from pathlib import Path
import requests
BASE='https://kevindrafts.github.io/asmartbear-wiki/'
def run():
    root=Path('site/public')
    paths=sorted(p.relative_to(root).as_posix() for p in root.rglob('*.html') if p.name!='404.html')
    paths += ['search/search_index.json','search/main.js','search/worker.js','assets/wiki.js','assets/wiki.css']
    session=requests.Session();session.headers['User-Agent']='ASmartBearWikiDeploymentCheck/1.0'
    failures=[]
    for index,path in enumerate(paths):
        url=BASE+(path[:-10] if path.endswith('index.html') else path)
        try:
            r=session.head(url,timeout=30,allow_redirects=True)
            if r.status_code!=200:failures.append({'url':url,'status':r.status_code})
        except requests.RequestException as error:failures.append({'url':url,'error':type(error).__name__})
        time.sleep(.25)
    # Confirm the content and search index are the expected corpus, not an old shell.
    response=session.get(BASE,timeout=30);response.raise_for_status()
    for marker in ('226 articles read and reviewed','43 topics','10 decision guides','5 reading paths'):
        if marker not in response.text:failures.append({'homepage_missing':marker})
    response=session.get(BASE+'search/search_index.json',timeout=30);response.raise_for_status()
    data=response.json();indexed={d['location'].split('#')[0] for d in data['docs']}
    for path in paths[:-5]:
        location=path[:-10] if path.endswith('index.html') else path
        if location not in indexed:failures.append({'not_search_indexed':location})
    result={'base_url':BASE,'content_pages':len(paths)-5,'search_and_style_assets':5,'http_checks':len(paths),'search_entries':len(data['docs']),'indexed_pages':len(indexed),'errors':failures}
    Path('reports/deployment-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return bool(failures)
if __name__=='__main__':raise SystemExit(run())
