import unittest
from scripts.validate import validate_note, overlapping_runs


class ValidationTests(unittest.TestCase):
    def test_missing_citation_rejected(self):
        self.assertIn('missing source citation', validate_note('An assertion', 'https://example.test/a'))

    def test_unreviewed_rejected(self):
        self.assertIn('missing reviewed status', validate_note('Source: https://example.test/a', 'https://example.test/a'))

    def test_copied_passage_detected(self):
        passage = ' '.join('word' + str(i) for i in range(60))
        self.assertGreaterEqual(overlapping_runs(passage, passage), 60)
        self.assertEqual(overlapping_runs('different original prose', passage), 0)


if __name__ == '__main__':
    unittest.main()
