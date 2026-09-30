"""Reconcile classifications and legacy redirect headers, without importing legacy bodies."""
import json,time
from urllib.parse import urlsplit,urljoin
from urllib.robotparser import RobotFileParser
import requests
from scripts.ingest import CACHE,BASE,AGENT,normalize,classify,write_json,export

def run():
    ledger=json.loads((CACHE/'ledger.json').read_text());session=requests.Session();session.headers['User-Agent']=AGENT
    robots={};last=0
    def request(url,method='HEAD'):
        nonlocal last
        time.sleep(max(0,2.1-(time.monotonic()-last)));last=time.monotonic()
        return session.request(method,url,timeout=30,allow_redirects=False)
    def can_fetch(url):
        host=urlsplit(url).netloc
        if host not in robots:
            r=request('https://'+host+'/robots.txt','GET');parser=RobotFileParser()
            if r.status_code==200:
                parser.parse(r.text.splitlines());(CACHE/('robots-'+host+'.txt')).write_text(r.text)
            elif r.status_code==404: parser.parse([])
            else: return False
            robots[host]=parser
        return robots[host].can_fetch(AGENT,url)
    reasons={'biography':'Author biography; not an article.','index':'Homepage discovery index.','utility':'Subscription utility; not an article.','feed':'Discovery feed, not a separate article.','asset':'Source image/asset; metadata preserved externally; no image redistribution.','external-asset':'Publisher asset outside article scope; not downloaded.','official-resource':'Official workshop or skill; link only, no content imported.','robots-excluded':'Excluded by robots policy or explicit source endpoint restriction.'}
    for url,r in ledger.items():
        if r['classification'] in ('article','mailbag'):continue
        r['classification']=classify(url);r['status']='excluded';r['exclusion_reason']=reasons.get(r['classification'],'Legacy-domain content outside the longform article boundary.')
        if r['classification']!='legacy' or r.get('redirect_checked'):continue
        current=url;chain=[]
        try:
            for _ in range(10):
                kind=classify(current)
                if kind in ('external','robots-excluded','asset','external-asset','official-resource'):
                    r['redirect_result']='Excluded redirect target';break
                if not can_fetch(current):r['redirect_result']='Robots denied or unavailable';break
                response=request(current);chain.append({'url':current,'http_status':response.status_code})
                if response.is_redirect:
                    target=normalize(urljoin(current,response.headers['Location']))
                    if not target or any(c['url']==target for c in chain):r['redirect_result']='Invalid or cyclic redirect';break
                    current=target;continue
                r['redirect_result']='Included canonical alias' if current in ledger and ledger[current]['classification'] in ('article','mailbag') else ('Legacy retained outside scope' if kind=='legacy' else 'Unresolved destination')
                break
            r.update({'redirect_checked':True,'redirect_chain':chain,'resolved_url':current})
        except requests.RequestException as e:r.update({'redirect_checked':True,'redirect_result':type(e).__name__,'redirect_chain':chain,'resolved_url':current})
        print(r['redirect_result'],url,current,flush=True)
        write_json(CACHE/'ledger.json',ledger)
    # Re-merge editorial changes if performed while checking headers.
    current=json.loads((CACHE/'ledger.json').read_text())
    for url,r in current.items():
        if r['classification'] in ('article','mailbag'):ledger[url]=r
    write_json(CACHE/'ledger.json',ledger);export(ledger)
if __name__=='__main__':run()
