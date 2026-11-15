"""Observable timing and frame-content checks for the optional GIF renderer."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HAS_PIL = importlib.util.find_spec('PIL') is not None
SCRIPT = Path(__file__).resolve().parents[1] / 'skills/readme-atelier/scripts/assemble_gif.py'


@unittest.skipUnless(HAS_PIL, 'Optional Pillow dependency is not installed')
class GifAssemblyTests(unittest.TestCase):
    def test_preserves_pixels_timing_and_existing_output(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            colors = [(140, 20, 35), (20, 60, 90), (210, 165, 75)]
            entries = []
            for i in range(12):
                file = f'frame-{i:05d}.png'
                Image.new('RGB', (32, 24), colors[i % 3]).save(root / file)
                entries.append({'file': file, 'time': i / 12})
            (root / 'manifest.json').write_text(json.dumps({'fps': 12, 'duration': 1,
                'width': 32, 'height': 24, 'frames': entries}), encoding='utf-8')
            output = root / 'result.gif'
            run = subprocess.run([sys.executable, str(SCRIPT), str(root), str(output)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            with Image.open(output) as gif:
                self.assertEqual(gif.n_frames, 12)
                duration = 0
                for i in range(12):
                    gif.seek(i)
                    duration += gif.info['duration']
                    self.assertEqual(gif.convert('RGB').getpixel((16, 12)), colors[i % 3])
                self.assertEqual(duration, 1000)
            before = output.read_bytes()
            repeated = subprocess.run([sys.executable, str(SCRIPT), str(root), str(output)], capture_output=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual(output.read_bytes(), before)

    def test_rejects_inconsistent_frame_size(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Image.new('RGB', (10, 10)).save(root / 'frame.png')
            (root / 'manifest.json').write_text(json.dumps({'fps': 2, 'duration': 1,
                'width': 20, 'height': 20, 'frames': [{'file': 'frame.png'}] * 2}), encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(root), str(root / 'bad.gif')], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'bad.gif').exists())


if __name__ == '__main__':
    unittest.main()
