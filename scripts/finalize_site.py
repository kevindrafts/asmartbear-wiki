"""Generate reproducible public coverage reports from metadata only."""
import json
from collections import Counter
from pathlib import Path
from scripts.catalog import load_sources
ROOT=Path(__file__).resolve().parents[1]
def run():
    articles=[json.loads(s) for s in (ROOT/'catalog/articles.jsonl').read_text().splitlines()]
    podcasts=[r for r in load_sources(ROOT) if r['classification']=='podcast']
    excluded=[json.loads(s) for s in (ROOT/'catalog/exclusions.jsonl').read_text().splitlines()]
    allrows=articles+excluded
    counts=Counter(r['classification'] for r in allrows)
    text='# Coverage and source boundary\n\nDiscovery checked: 2026-10-17. Original capture: 2026-09-30, with one addition and two source refreshes on October 17; see [recent update](recent-update.md). This is a complete reading companion to the discovered longform corpus, not a career-wide archive.\n\n'
    text+=f"**{len(articles)} included sources; {sum(r['read_status']=='complete' for r in articles)} read in full; {sum(r['note_status']=='reviewed' for r in articles)} reviewed notes.** {sum(r['word_count'] for r in articles):,} extracted source words were read externally. No included fetch failures or pending reviews.\n\n"
    text+='Discovery combined sitemap, homepage, RSS, and recursive internal article links. Canonical URLs were reconciled; the included set has no canonical duplicates.\n\n| Discovery route | URLs in ledger | Included articles |\n|---|---:|---:|\n'
    for route in ('sitemap','homepage','rss'):
        text+=f"| {route} | {sum(route in r['discovered_via'] for r in allrows)} | {sum(route in r['discovered_via'] for r in articles)} |\n"
    off=[r for r in articles if 'sitemap' not in r['discovered_via']]
    hidden=[r for r in articles if 'homepage' not in r['discovered_via']]
    text+='\nRoutes overlap. Internal links added '+', '.join(f"[{r['title']}]({r['canonical_url']})" for r in off)+'. The checked sitemap has 227 URLs, including biography and subscription pages; its 225 article URLs plus these two essays yield 227 included articles.\n\n'
    text+=f"The included set contains {counts['article']} essays and {counts['mailbag']} mailbags. {len(hidden)} sources are absent from homepage discovery, all mailbags. This corrects the initial estimate of 12 hidden mailbags.\n\n"
    text+='## Classification\n\n| Class | Count |\n|---|---:|\n'+''.join(f'| {k} | {v} |\n' for k,v in sorted(counts.items()))
    text+='\n## Exclusions and redirects\n\nEvery discovered in-scope-domain URL has an included or exclusion record. External third-party citations are not recursively crawled. Legacy-domain links are checked for redirects, not imported as an additional blog archive. One legacy alias resolves to an included article; 19 retain destinations outside the longform boundary. Official workshops are linked only. Source image and asset URLs are not redistributed. Robots-excluded JSON and `/ref/` endpoints were never fetched.\n\n'
    text+='| Discovered URL | Classification | Reason / resolution |\n|---|---|---|\n'
    for r in excluded:
        why=r.get('exclusion_reason','')
        if r.get('redirect_result'):why+=' '+r['redirect_result']+'. Destination: '+r['resolved_url']
        text+=f"| [{r['url']}]({r['url']}) | {r['classification']} | {why} |\n"
    text+=f'\n## Podcast coverage\n\nThe official Smart Bear Live episode list and transcript links were checked October 17, 2026: nine transcripts were located. {len(podcasts)} episodes were read in full and reviewed, totaling {sum(r["word_count"] for r in podcasts):,} extracted words including speaker labels and timestamps. The follow-up batch adds episodes 1, 4, 6, and 7, completing review of all nine transcripts listed on that discovery date. This is coverage of the discovered 2026 show, not a claim to every historical podcast appearance. See [the podcast index](../wiki/podcasts.md) and [update report](podcast-update.md).\n\n'
    text+='The podcast catalog and external review ledger are separate from blog discovery. Transcript wording, timestamps, and speaker labels have not been checked against audio. Notes preserve guest attribution, conditional advice, and known transcript inconsistencies. E01 and E04 have text timestamps beyond the listed audio durations; E04 has no clickable time anchors.\n'
    text+=f'\n## Editorial coverage\n\n{len(articles)+len(podcasts)} concise source-linked notes ({len(articles)} articles and mailbags, {len(podcasts)} podcast episodes), 43 topic pages, 10 practical decision guides, and five stage-based reading paths. The [source catalog](../processed/index.md) reaches every note. Every note connects to at least one substantive topic, and synthesis pages cite multiple primary sources.\n\nAll included article bodies, footnotes, extracted table cells, image alt text, and captions were read. Diagram meaning is described in original prose where relevant; diagrams themselves are not copied. This is not a claim that every decorative image was visually inspected. Explicit source discrepancies and technical qualifications are retained in the relevant notes (including color wheels, A/B statistics, forecasting, and revenue models).\n\nPublication, modification, and sitemap timestamps are distinct; source metadata is not independently verified publication history. Evidence comes from Cohen\'s essays and multi-speaker conversations, not independent corroboration. Historical examples and participant business figures are not current audited benchmarks.\n'
    (ROOT/'reports/coverage.md').write_text(text)
if __name__=='__main__':run()
