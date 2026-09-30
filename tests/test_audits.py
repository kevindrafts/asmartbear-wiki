import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from scripts.ingest import BASE, Fetcher, classify, canonical_groups
from scripts.validate import validate_catalog, check_links, check_synthesis, leak_findings

class HardenedIngestionTests(unittest.TestCase):
    def test_classification_boundaries(self):
        self.assertEqual(classify(BASE+'jason-cohen/'), 'biography')
        self.assertEqual(classify('https://skills.asmartbear.com/workshops/find-your-carol/'), 'official-resource')
        self.assertEqual(classify('https://public.asmartbear.com/book.pdf'), 'external-asset')
        self.assertEqual(classify('https://notasmartbear.com/post/'), 'external')
    def test_duplicate_canonical_group(self):
        rows=[{'url':BASE+'old/','canonical_url':BASE+'new/'},{'url':BASE+'new/','canonical_url':BASE+'new/'}]
        self.assertEqual(len(canonical_groups(rows)[BASE+'new/']), 2)
    @patch('scripts.ingest.time.sleep')
    def test_redirect_loop_and_exclusion(self, sleep):
        f=Fetcher.__new__(Fetcher);f.last_request=0;f.session=Mock();f.robots=Mock()
        f.robots.can_fetch.return_value=True
        response=Mock(is_redirect=True, headers={'Location':'/loop/'})
        f.session.get.return_value=response
        with self.assertRaisesRegex(ValueError,'redirect'):
            f.get(BASE+'loop/')
        response.headers={'Location':'/ref/blocked/'}
        with self.assertRaisesRegex(ValueError,'exclusion'):
            f.get(BASE+'start/')
        self.assertTrue(all('/ref/' not in c.args[0] for c in f.session.get.call_args_list))
    @patch('scripts.ingest.time.sleep')
    def test_robots_denial_prevents_network(self,sleep):
        f=Fetcher.__new__(Fetcher);f.session=Mock();f.robots=Mock();f.robots.can_fetch.return_value=False
        with self.assertRaises(ValueError): f.get(BASE+'private/')
        f.session.get.assert_not_called()

class AuditTests(unittest.TestCase):
    def test_bad_hash_dates_status(self):
        row={'id':'test','url':BASE+'test/','canonical_url':BASE+'test/','title':'Test','classification':'article','status':'fetched','published':'bad','body_sha256':'a'*64,'reviewed_body_sha256':'b'*64,'read_status':'pending','note_status':'pending','tags':['strategy'],'synthesis_references':['wiki/topics/strategy.md']}
        errors=validate_catalog([row])
        self.assertTrue(any('date' in e for e in errors))
        self.assertTrue(any('hash' in e for e in errors))
        self.assertTrue(any('review' in e for e in errors))
    def test_broken_links_and_fragments(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as d:
            root=Path(d);(root/'a.md').write_text('# A\n\n[ok](b.md#there) [broken](missing.md) [anchor](b.md#absent)')
            (root/'b.md').write_text('# There\n')
            errors=check_links(root)
            self.assertEqual(len(errors),2)
    def test_synthesis_requires_multiple_primary_sources(self):
        self.assertTrue(check_synthesis('# Topic\n\nOnly a claim.'))
        self.assertFalse(check_synthesis('# Topic\n\nA. [First](https://longform.asmartbear.com/one/)\n\nB. [Second](https://longform.asmartbear.com/two/)'))
    def test_leak_scanner_excludes_no_body(self):
        body=' '.join('synthetic'+str(i) for i in range(100))
        self.assertTrue(leak_findings(body, {'synthetic':body}))
        self.assertFalse(leak_findings('Original explanation of a different idea.', {'synthetic':body}))

if __name__=='__main__': unittest.main()
