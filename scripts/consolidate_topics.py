"""One-time editorial taxonomy reconciliation; safe to rerun."""
import json,re,yaml
from scripts.ingest import ROOT,CACHE,write_json,export
MAP={
'acquisition-channels':'marketing-channels','acquisition-economics':'saas-economics','advice-and-judgment':'uncertainty','ai-strategy':'innovation','brand':'authenticity','change-management':'leadership','communication':'writing','conversion':'sales','creativity':'innovation','culture':'company-culture','customer-discovery':'validation','customer-love':'customer-support','customer-service':'customer-support','defensibility':'moats','engineering':'technical-debt','enterprise-sales':'sales','founder-fit':'founder-market-fit','founder-lessons':'founder-psychology','funding':'fundraising','growth':'forecasting','growth-limits':'expansion','growth-models':'forecasting','management':'leadership','mental-models':'decision-making','optionality':'uncertainty','partnerships':'distribution','personal-effectiveness':'sustainable-work','platform-risk':'moats','purpose':'fulfillment','resilience':'scaling','services-business':'saas-economics','startup-risk':'validation','team-dynamics':'company-culture','unfair-advantages':'moats','unit-economics':'saas-economics','word-of-mouth':'distribution'}
def run():
    ledger=json.loads((CACHE/'ledger.json').read_text())
    for row in ledger.values():
        if row['classification'] not in ('article','mailbag'):continue
        tags=list(dict.fromkeys(MAP.get(t,t) for t in row['tags']))
        for t in tags:
            if not (ROOT/'wiki/topics'/(t+'.md')).exists():raise ValueError(t)
        p=ROOT/'processed'/(row['id']+'.md');parts=p.read_text().split('---',2);meta=yaml.safe_load(parts[1]);meta['topics']=tags
        body=re.sub(r'\nRelated:.*','\nRelated: '+' · '.join('['+t.replace('-',' ').title()+'](../wiki/topics/'+t+'.md)' for t in tags),parts[2])
        p.write_text('---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---'+body)
        row['tags']=tags;row['synthesis_references']=['wiki/topics/'+t+'.md' for t in tags]
    write_json(CACHE/'ledger.json',ledger);export(ledger)
if __name__=='__main__':run()
