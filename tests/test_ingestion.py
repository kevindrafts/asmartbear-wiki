import unittest
from scripts.ingest import normalize, extract, classify, allowed, validate_dates

BASE = 'https://longform.asmartbear.com/'


class DiscoveryTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize('/pricing/?utm_source=x#tiers'), BASE + 'pricing/')
        self.assertEqual(normalize('http://longform.asmartbear.com/pricing'), BASE + 'pricing/')
        self.assertIsNone(normalize('mailto:person@example.test'))

    def test_boundaries(self):
        self.assertFalse(allowed(BASE + 'pricing/index.json'))
        self.assertFalse(allowed(BASE + 'ref/something/'))
        self.assertFalse(allowed('https://other.test/article/'))
        self.assertEqual(classify(BASE), 'index')
        self.assertEqual(classify(BASE + 'bio/'), 'biography')
        self.assertEqual(classify(BASE + 'image.png'), 'asset')

    def test_date_validation(self):
        self.assertTrue(validate_dates('2020-01-03', '2025-02-05'))
        self.assertFalse(validate_dates('2025-02-30', None))


class ExtractionTests(unittest.TestCase):
    def test_complete_body_metadata_and_structure(self):
        html = '''<html><head><title>Fallback</title>
        <link rel="canonical" href="https://longform.asmartbear.com/example/">
        <meta property="article:published_time" content="2020-01-01T00:00:00Z">
        <meta property="article:modified_time" content="2024-02-03T00:00:00Z"></head>
        <body><nav>Do not capture navigation</nav><article><h1>Example</h1>
        <p>First synthetic paragraph.</p><h2 id="cost">Cost</h2>
        <table><tr><th>Case</th><th>Cost</th></tr><tr><td>A</td><td>12</td></tr></table>
        <figure><img src="diagram.svg" alt="Cost rises as volume falls"><figcaption>Scope matters</figcaption></figure>
        <p>Final synthetic paragraph with a qualification.</p></article><footer>Boilerplate</footer></body></html>'''
        data = extract(html, BASE + 'example/')
        self.assertEqual(data['title'], 'Example')
        self.assertEqual(data['published'], '2020-01-01T00:00:00Z')
        self.assertEqual(data['modified'], '2024-02-03T00:00:00Z')
        self.assertIn('Final synthetic paragraph', data['body'])
        self.assertNotIn('Do not capture navigation', data['body'])
        self.assertEqual(data['tables'][0][1], ['A', '12'])
        self.assertEqual(data['images'][0]['alt'], 'Cost rises as volume falls')
        self.assertEqual(data['headings'][1]['id'], 'cost')

    def test_missing_body_is_failure(self):
        with self.assertRaises(ValueError):
            extract('<html><nav>No article</nav></html>', BASE + 'broken/')

    def test_canonical_and_links(self):
        data = extract('<link rel="canonical" href="/new/"><article><h1>T</h1><p>Body <a href="/next/#x">next</a></p></article>', BASE + 'old/')
        self.assertEqual(data['canonical_url'], BASE + 'new/')
        self.assertIn(BASE + 'next/', data['links'])


if __name__ == '__main__':
    unittest.main()
