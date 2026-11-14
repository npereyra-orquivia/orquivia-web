"""Transcode selected ImageGen files into responsive project assets without changing content."""
from pathlib import Path
from PIL import Image
import json
import argparse

ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('manifest',type=Path,help='JSON list of {key, source} for the selected original files.')
args=parser.parse_args()
items=json.loads(args.manifest.read_text(encoding='utf-8'))
target=ROOT/'assets/photography'
target.mkdir(parents=True,exist_ok=True)
photo_map=json.loads((ROOT/'content/photo-assets.json').read_text(encoding='utf-8'))
for item in items:
    with Image.open(item['source']) as original:
        full=original.convert('RGB')
        full.thumbnail((1920,1280),Image.Resampling.LANCZOS)
        full.save(target/(item['key']+'.webp'),'WEBP',quality=86,method=6)
        small=full.copy()
        small.thumbnail((768,768),Image.Resampling.LANCZOS)
        small.save(target/(item['key']+'-768.webp'),'WEBP',quality=82,method=6)
        for entry in photo_map.values():
            if entry['file']==item['key']:
                entry.update(width=full.width,height=full.height)
        print(item['key'],str(full.size),(target/(item['key']+'.webp')).stat().st_size)
(ROOT/'content/photo-assets.json').write_text(json.dumps(photo_map,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
