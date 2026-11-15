#!/usr/bin/env python3
"""Assemble frames produced by render_scene.mjs. Requires Pillow."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        from PIL import Image
    except ImportError:
        parser.error('Pillow is required: python -m pip install Pillow')
    root = args.frames.resolve()
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if args.output.exists():
        parser.error('Output already exists; choose another filename.')
    fps, length = manifest['fps'], len(manifest['frames'])
    if not 1 <= fps <= 50 or length < 2 or manifest['duration'] <= 0:
        parser.error('Expected a multi-frame animation with fps in [1, 50].')
    images = []
    for entry in manifest['frames']:
        file = (root / entry['file']).resolve()
        if not file.is_relative_to(root):
            parser.error('Frame path is outside the input directory.')
        with Image.open(file) as im:
            if im.size != (manifest['width'], manifest['height']):
                parser.error('Frame dimensions differ from the manifest.')
            images.append(im.convert('RGB'))
    # Sample the whole timeline so a late scene's colors are also represented.
    samples = images[::max(1, length // 12)]
    atlas = Image.new('RGB', (160 * len(samples), 100), 'white')
    for index, im in enumerate(samples):
        thumb = im.copy()
        thumb.thumbnail((160, 100))
        atlas.paste(thumb, (index * 160, 0))
    palette = atlas.quantize(colors=192)
    frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images]
    # GIF stores centiseconds. Rounded boundaries avoid accumulated timing drift.
    total_cs = round(manifest['duration'] * 100)
    boundaries = [round(min(i / fps, manifest['duration']) * 100) for i in range(length)] + [total_cs]
    durations = [(boundaries[i + 1] - boundaries[i]) * 10 for i in range(length)]
    if min(durations) <= 0:
        parser.error('Frame timestamps cannot be represented at GIF precision.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(args.output, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=True, disposal=1)
    with Image.open(args.output) as result:
        actual_ms = 0
        for index in range(result.n_frames):
            result.seek(index)
            actual_ms += result.info.get('duration', 0)
        print(json.dumps({'output': str(args.output.resolve()), 'width': result.width,
                          'height': result.height, 'frames': result.n_frames,
                          'duration_ms': actual_ms, 'bytes': args.output.stat().st_size}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, KeyError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
