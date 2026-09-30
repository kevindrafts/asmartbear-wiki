import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from scripts.validate import check_reachability, inventory_errors

class PublicationTests(unittest.TestCase):
    def test_orphan_is_detected(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as d:
            root=Path(d)
            (root/'index.md').write_text('# Home\n[Read](note.md)')
            (root/'note.md').write_text('# Note')
            (root/'orphan.md').write_text('# Lost')
            self.assertEqual(check_reachability(root), ['orphan.md'])
    def test_sensitive_and_raw_paths_rejected(self):
        self.assertTrue(inventory_errors(['raw/article.html','private.pem','.env']))
        self.assertFalse(inventory_errors(['processed/pricing.md','catalog/articles.jsonl','site/wiki.css']))
