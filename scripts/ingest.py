"""Sequential, resumable ingestion. Copyrighted bodies never leave external cache."""
import argparse
import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path('/Users/mordecai/.hermes/data/jason-cohen-source-cache')
BASE = 'https://longform.asmartbear.com/'
AGENT = 'ASmartBearUnofficialWiki/1.0 (+https://github.com/kevindrafts/asmartbear-wiki)'


def normalize(url, base=BASE):
    p = urlsplit(urljoin(base, url))
    if p.scheme not in ('http', 'https'):
        return None
    path = re.sub('/+', '/', p.path) or '/'
    if '.' not in path.rsplit('/', 1)[-1] and not path.endswith('/'):
        path += '/'
    return urlunsplit(('https', p.netloc.lower(), path, '', ''))


def allowed(url):
    p = urlsplit(url)
    return p.hostname == 'longform.asmartbear.com' and '.json' not in p.path.lower() and not p.path.startswith('/ref/')


def classify(url):
    p = urlsplit(url)
    if p.hostname != 'longform.asmartbear.com':
        if p.hostname == 'skills.asmartbear.com':
            return 'official-resource'
        if p.hostname == 'public.asmartbear.com':
            return 'external-asset'
        return 'legacy' if p.hostname in ('blog.asmartbear.com', 'asmartbear.com', 'www.asmartbear.com') else 'external'
    path = p.path
    if not allowed(url):
        return 'robots-excluded'
    if path == '/':
        return 'index'
    if path in ('/bio/', '/about/', '/jason-cohen/'):
        return 'biography'
    if path in ('/subscribe/', '/unsubscribe/', '/search/', '/tags/', '/404.html'):
        return 'utility'
    if '.' in path.rsplit('/', 1)[-1]:
        return 'feed' if path.endswith('.xml') else 'asset'
    return 'candidate'


def canonical_groups(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row["canonical_url"], []).append(row["url"])
    return groups


def validate_dates(*dates):
    try:
        for value in dates:
            if value:
                datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def extract(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.select_one('article')
    if not article:
        raise ValueError('missing article element')
    title = article.select_one('h1') or soup.select_one('h1')
    canonical = soup.select_one('link[rel="canonical"]')
    body = article.select_one('.e-content') or article
    for node in body.select('script,style,nav,.print-end-of-content,.sr-only,.newsletter-signup,picture-disabled,img[aria-hidden="true"]'):
        node.decompose()
    def meta(key):
        tag = soup.find('meta', attrs={'property': key})
        return tag.get('content') if tag else None
    images = []
    for img in body.select('img'):
        fig = img.find_parent('figure')
        cap = fig.select_one('figcaption') if fig else None
        images.append({'src': urljoin(url, img.get('src', '')), 'alt': img.get('alt', ''),
                       'caption': cap.get_text(' ', strip=True) if cap else ''})
    tables = [[[c.get_text(' ', strip=True) for c in row.select('th,td')]
               for row in table.select('tr')] for table in body.select('table')]
    headings = [{'text': h.get_text(' ', strip=True), 'id': h.get('id')} for h in article.select('h1,h2,h3,h4')]
    links = sorted({normalize(a['href'], url) for a in body.select('a[href]') if normalize(a['href'], url)})
    # Preserve block boundaries and all inline text; never length-limit a body.
    for br in body.select('br'):
        br.replace_with('\n')
    for block in body.select('p,h1,h2,h3,h4,li,blockquote,tr,figcaption,div.footnotes'):
        block.insert_before('\n')
        block.insert_after('\n')
    text = re.sub(r'[ \t]+', ' ', body.get_text(' ', strip=False))
    text = re.sub(r' *\n *', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return {'title': title.get_text(' ', strip=True) if title else '',
            'canonical_url': normalize(canonical['href'], url) if canonical else normalize(url),
            'published': meta('article:published_time'), 'modified': meta('article:modified_time'),
            'source_type': 'mailbag' if 'From the mailbag' in text else 'article',
            'body': text, 'word_count': len(text.split()), 'images': images, 'tables': tables,
            'headings': headings, 'links': links, 'body_sha256': hashlib.sha256(text.encode()).hexdigest()}


class Fetcher:
    def __init__(self):
        CACHE.mkdir(parents=True, exist_ok=True)
        self.last_request = 0
        self.session = requests.Session()
        self.session.headers['User-Agent'] = AGENT
        self.robots = RobotFileParser()
        robots = self.get(BASE + 'robots.txt', robots_check=False)
        (CACHE / 'robots.txt').write_text(robots)
        self.robots.parse(robots.splitlines())

    def get(self, url, robots_check=True, seen=None):
        seen = set() if seen is None else seen
        if url in seen or len(seen) >= 10:
            raise ValueError("redirect loop or limit: " + url)
        seen.add(url)
        if not allowed(url) or (robots_check and not self.robots.can_fetch(AGENT, url)):
            raise ValueError('robots or domain exclusion: ' + url)
        for attempt in range(4):
            time.sleep(max(0, 2.1 - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            response = self.session.get(url, timeout=60, allow_redirects=False)
            if response.is_redirect:
                return self.get(urljoin(url, response.headers['Location']), seen=seen)
            if response.status_code == 429 or response.status_code >= 500:
                time.sleep(min(45, 3 ** (attempt + 1)))
                continue
            response.raise_for_status()
            self.final_url = url
            response.encoding = 'utf-8'
            return response.text
        raise RuntimeError('retry limit: ' + url)


def write_json(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)


def run(limit=None):
    fetcher = Fetcher()
    state_path = CACHE / 'ledger.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    def discover(url, via, lastmod=None):
        url = normalize(url)
        if not url or classify(url) == 'external':
            return
        row = state.setdefault(url, {'url': url, 'classification': classify(url), 'discovered_via': [], 'status': 'pending'})
        if via not in row['discovered_via']:
            row['discovered_via'].append(via)
        if row['classification'] not in ('article', 'mailbag', 'unavailable'):
            row['classification'] = classify(url)
        if lastmod:
            row['sitemap_lastmod'] = lastmod
    for name in ['sitemap.xml', 'index.xml', '']:
        path = CACHE / ('homepage.html' if not name else name)
        if not path.exists():
            path.write_text(fetcher.get(BASE + name))
        raw = path.read_text()
        if name == 'sitemap.xml':
            tree = ET.fromstring(raw)
            ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for entry in tree.findall('s:url', ns):
                discover(entry.findtext('s:loc', namespaces=ns), 'sitemap', entry.findtext('s:lastmod', namespaces=ns))
        elif name == 'index.xml':
            for link in ET.fromstring(raw).findall('.//item/link'):
                discover(link.text, 'rss')
        else:
            for a in BeautifulSoup(raw, 'html.parser').select('a[href]'):
                discover(a['href'], 'homepage')
    write_json(state_path, state)
    count = 0
    # Pilot priority covers mailbag, pricing, long strategy, older essays, and diagrams.
    priority = ['pricing','slc','advice-first-time-manager','bootstrapped-beats-vc','icp','customer-interviews','product-market-fit','strategy','wpengine','impostor','prioritization','churn']
    while True:
        pending = [r for r in state.values() if r['classification'] == 'candidate' and r['status'] in ('pending', 'failed')]
        pending.sort(key=lambda r: (next((i for i, s in enumerate(priority) if s in r['url']), 99), r['url']))
        if not pending or (limit is not None and count >= limit):
            break
        row = pending[0]
        url = row['url']
        slug = urlsplit(url).path.strip('/').replace('/', '--')
        raw_path = CACHE / (slug + '.html')
        try:
            if not raw_path.exists():
                raw_path.write_text(fetcher.get(url))
                row['resolved_url'] = fetcher.final_url
            data = extract(raw_path.read_text(), url)
            if data['word_count'] < 80:
                raise ValueError('suspiciously short body')
            if not validate_dates(data['published'], data['modified']):
                raise ValueError('malformed publication/modification metadata')
            data['fetched_at'] = datetime.now(timezone.utc).isoformat()
            data['html_sha256'] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
            write_json(CACHE / (slug + '.json'), data)
            for link in data['links']:
                discover(link, 'article:' + slug)
            row.update({k: v for k, v in data.items() if k not in ('body', 'images', 'tables', 'headings', 'links')})
            row.update({'id': slug, 'status': 'fetched', 'classification': data['source_type'],
                        'image_count': len(data['images']), 'table_count': len(data['tables']),
                        'read_status': 'pending', 'note_status': 'pending', 'synthesis_references': []})
            print('FETCHED', slug, data['word_count'], 'words', flush=True)
        except Exception as error:
            row.update({'status': 'failed', 'error': str(error), 'classification': 'unavailable'})
            print('FAILED', url, str(error), flush=True)
        count += 1
        # Preserve editorial checkpoints saved while a sequential crawl is running.
        latest = json.loads(state_path.read_text())
        for saved_url, saved in latest.items():
            current = state.get(saved_url, {})
            if saved.get('reviewed_body_sha256') == current.get('body_sha256') and saved.get('note_status') == 'reviewed':
                for key in ('read_status', 'note_status', 'reviewed_body_sha256', 'tags', 'synthesis_references'):
                    current[key] = saved[key]
        write_json(state_path, state)
        export(state)
    export(state)


def export(state):
    included = [r for r in state.values() if r['classification'] in ('article', 'mailbag')]
    excluded = [r for r in state.values() if r['classification'] not in ('article', 'mailbag')]
    for name, rows in [('articles', included), ('exclusions', excluded)]:
        (ROOT / 'catalog' / (name + '.jsonl')).write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n' for r in sorted(rows, key=lambda x: x['url'])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    run(args.limit)
