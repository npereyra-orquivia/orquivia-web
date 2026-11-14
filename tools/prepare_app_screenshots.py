"""Convert reviewed anonymised screenshots into responsive WebP assets.

The input manifest is a local JSON list of {key, source}. Only already anonymised
ImageGen outputs are accepted; private source captures must never enter public assets.
This script only resizes/encodes images and discards metadata; it does not edit content.
"""
import argparse
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('manifest', type=Path)
args = parser.parse_args()
selected = json.loads(args.manifest.read_text(encoding='utf-8'))
target = ROOT / 'assets/mockups'
target.mkdir(parents=True, exist_ok=True)
entries = json.loads((ROOT / 'content/app-mockups.json').read_text(encoding='utf-8'))
by_key = {item['key']: item for item in entries}
for item in selected:
    entry = by_key[item['key']]
    with Image.open(item['source']) as source:
        full = source.convert('RGB')
        full.save(target / (entry['image'] + '.webp'), 'WEBP', lossless=True, method=6)
        for width in (768, 1280):
            small = full.copy()
            small.thumbnail((width, width), Image.Resampling.LANCZOS)
            small.save(target / f"{entry['image']}-{width}.webp", 'WEBP', quality=94, method=6)
        entry.update(width=full.width, height=full.height)
        print(entry['image'], full.size)
(ROOT / 'content/app-mockups.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
