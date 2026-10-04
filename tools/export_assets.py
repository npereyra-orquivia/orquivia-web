"""Copy only public assets referenced by generated HTML and stylesheets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import shutil
import re

def copy_assets(source_root, destination):
    pending = [source_root/'styles.css', source_root/'script.js']
    class Assets(HTMLParser):
        def handle_starttag(self, tag, attrs):
            a=dict(attrs)
            raw=a.get('src') if tag in ('img','script') else a.get('href') if tag=='link' and a.get('rel') in ('stylesheet','icon') else None
            if raw and not urlsplit(raw).scheme:
                pending.append(source_root/urlsplit(raw).path)
    for page in destination.glob('*.html'):
        Assets().feed(page.read_text(encoding='utf-8'))
    copied=set()
    while pending:
        source=pending.pop().resolve()
        if source in copied: continue
        relative=source.relative_to(source_root.resolve())
        target=destination/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        copied.add(source)
        if source.suffix=='.css':
            for raw in re.findall(r'url\([\"\']?([^\)\"\']+)',source.read_text(encoding='utf-8')):
                if not raw.startswith(('http','data:')): pending.append(source.parent/raw)
