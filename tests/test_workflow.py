"""Preparation safety contracts, not a rerun of the AI video experiment."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('benchmark', Path(__file__).resolve().parents[1] / 'tools/benchmark.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

class WorkflowTest(unittest.TestCase):
    def test_original_and_portable_render_contract_are_distinct(self):
        original = b.prompt('M04', 'remotion', 'initial', True)
        portable = b.prompt('M04', 'remotion', 'initial')
        self.assertIn('等待 .render-results/<id>/result.json', original)
        self.assertNotIn('等待 .render-results/<id>/result.json', portable)
        self.assertIn('不提供原实验的外部渲染服务', portable)
        self.assertIn('CRF18', original)
        self.assertIn('CRF18', portable)

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            sentinel = Path(temp) / 'keep.txt'
            sentinel.write_text('keep')
            with self.assertRaises(ValueError):
                b.prepare(SimpleNamespace(scene='P03', framework='remotion', phase='initial', out=temp))
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_revision_requires_valid_own_baseline_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'out'
            with self.assertRaises(ValueError):
                b.prepare(SimpleNamespace(scene='P03', framework='remotion', phase='revision', out=str(out), baseline_dir=None))
            self.assertFalse(out.exists())

    def test_batch2_has_no_revision(self):
        with self.assertRaises(ValueError):
            b.prompt('M04', 'hyperframes', 'revision')

    def test_manifest_cannot_read_outside_input(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            (d / 'input-manifest.json').write_text(json.dumps({'files': [{'path': '../secret', 'included': True, 'sha256': 'fake'}]}))
            with self.assertRaises(ValueError):
                b.check_input(d)

    def test_missing_and_modified_inputs_are_visible(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            (d / 'data.json').write_text('{}')
            (d / 'input-manifest.json').write_text(json.dumps({'files': [
                {'path': 'data.json', 'included': True, 'sha256': 'wrong'},
                {'path': 'voice.wav', 'included': False, 'sha256': 'historical'}]}))
            result = b.check_input(d)
            self.assertFalse(result['ready'])
            self.assertEqual(result['changed'], ['data.json'])
            self.assertEqual(result['missing'], ['voice.wav'])

if __name__ == '__main__':
    unittest.main()
