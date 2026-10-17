import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.catalog import load_sources
from scripts.validate import PRIMARY, validate_catalog, check_synthesis


class PodcastCatalogTests(unittest.TestCase):
    def row(self):
        return dict(id='synthetic-episode', title='Synthetic conversation',
                    url='https://smartbearlive.transistor.fm/99',
                    canonical_url='https://smartbearlive.transistor.fm/99/transcript',
                    episode=99, participants=['Synthetic host', 'Synthetic guest'],
                    classification='podcast', source_type='podcast', status='fetched',
                    published='2026-10-01', modified=None, tags=['strategy'],
                    synthesis_references=['wiki/topics/strategy.md'],
                    body_sha256='a'*64, reviewed_body_sha256='a'*64,
                    read_status='complete', note_status='reviewed')

    def test_reviewed_podcast_requires_participants_and_official_transcript(self):
        row=self.row()
        self.assertEqual(validate_catalog([row]), [])
        row['participants']=[]
        self.assertTrue(any('participants' in e for e in validate_catalog([row])))
        row=self.row(); row['canonical_url']='https://example.com/99/transcript'
        self.assertTrue(any('transcript' in e for e in validate_catalog([row])))
        row=self.row(); row['read_status']='pending'
        self.assertTrue(any('incomplete' in e for e in validate_catalog([row])))

    def test_primary_citations_count_episodes_not_timestamps(self):
        url=self.row()['canonical_url']
        self.assertEqual(PRIMARY.findall(url+'#t=3m10s'), [url])
        self.assertTrue(check_synthesis(f'[A]({url}#t=1m) [B]({url}#t=2m)'))
        self.assertFalse(check_synthesis(f'[A]({url}) [B](https://longform.asmartbear.com/test/)'))

    def test_separate_catalogs_are_combined_without_changing_blog_export(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            root=Path(directory); (root/'catalog').mkdir()
            (root/'catalog/articles.jsonl').write_text(json.dumps({'id':'essay'})+'\n')
            self.assertEqual(load_sources(root), [{'id':'essay'}])
            (root/'catalog/podcasts.jsonl').write_text(json.dumps(self.row())+'\n')
            self.assertEqual([r['id'] for r in load_sources(root)], ['essay','synthetic-episode'])


if __name__=='__main__':
    unittest.main()
