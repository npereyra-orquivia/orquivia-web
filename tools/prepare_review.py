"""Prepare only public website files for a separate GitHub Pages review site."""
from pathlib import Path
import re
import shutil
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / '.publish' / 'orquivia-revision'
DEST.mkdir(parents=True, exist_ok=True)
pending = list(ROOT.glob('*.html')) + [ROOT / 'styles.css', ROOT / 'script.js']
pending.extend((ROOT / 'assets/diagrams').glob('orquivia-share-*.png'))
copied = set()

class Assets(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        source = a.get('src') if tag in ('img', 'script') else a.get('href') if tag == 'link' and a.get('rel') in ('stylesheet', 'icon') else None
        if source and not urlsplit(source).scheme:
            pending.append(ROOT / urlsplit(source).path)
        if tag=='img':
            for entry in a.get('srcset','').split(','):
                image_path=entry.strip().split(' ')[0]
                if image_path and not urlsplit(image_path).scheme:
                    pending.append(ROOT / urlsplit(image_path).path)

while pending:
    source = pending.pop()
    if source in copied:
        continue
    copied.add(source)
    relative = source.relative_to(ROOT)
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix in ('.html', '.css'):
        text = source.read_text(encoding='utf-8')
        if source.suffix == '.html':
            Assets().feed(text)
            # A separate review site must not advertise production canonical URLs.
            text = re.sub(r'<link\b[^>]*rel="(?:canonical|alternate)"[^>]*>', '', text)
            text = re.sub(r'<script type="application/ld\+json">.*?</script>', '', text, flags=re.S)
            text = text.replace('https://orquivia.com/assets/', 'https://thepulsestation.github.io/orquivia-revision/assets/')
            text = re.sub(r'(<meta property="og:url" content=")[^"]+', r'\1https://thepulsestation.github.io/orquivia-revision/'+('' if source.name=='index.html' else source.name), text)
        else:
            for asset in re.findall(r'url\([\"\']?([^\)\"\']+)', text):
                if not asset.startswith(('http', 'data:')):
                    pending.append(source.parent / asset)
        target.write_text(text, encoding='utf-8')
    else:
        shutil.copy2(source, target)

(DEST / '.nojekyll').write_text('', encoding='utf-8')
(DEST / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
(DEST / 'README.md').write_text('# Orquivia · Revisión de contenido\n\nVista independiente para valorar el nuevo sitio. No reemplaza la web principal.\n\nEl formulario prepara un correo; no envía datos a un servidor.\n', encoding='utf-8')
print(f'Prepared {len(copied)} website files in {DEST}')
