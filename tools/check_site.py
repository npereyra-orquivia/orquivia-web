"""Validate internal navigation, assets and content invariants without third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[];self.links=[];self.assets=[];self.h1=0;self.lang='';self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang','')
        if tag=='h1':self.h1+=1
        if tag=='a':self.links.append(a.get('href',''))
        if tag in ('img','script'):self.assets.append(a.get('src',''))
        if tag=='link' and a.get('rel') in ('stylesheet','icon'):self.assets.append(a.get('href',''))

pages={p.name:Page(p.read_text(encoding='utf-8')) for p in ROOT.glob('*.html')}
errors=[]
for name,p in pages.items():
    if p.h1!=1:errors.append(f'{name}: expected one h1, got {p.h1}')
    if p.lang not in ('es','en'):errors.append(f'{name}: missing language')
    if len(p.ids)!=len(set(p.ids)):errors.append(f'{name}: duplicate IDs')
    for raw in p.links+p.assets:
        u=urlsplit(raw)
        if u.scheme or u.netloc:continue
        file=unquote(u.path) or name
        target=ROOT/file
        if not target.exists():errors.append(f'{name}: missing {raw}')
        elif u.fragment and file in pages and u.fragment not in pages[file].ids:errors.append(f'{name}: missing fragment {raw}')
    text=(ROOT/name).read_text(encoding='utf-8')
    if re.search(r'\bayud(?:amos|a|arte|ar)\b',text,re.I):errors.append(f'{name}: excluded copy')
    if 'noindex, nofollow' not in text:errors.append(f'{name}: missing preview noindex')
for sheet in [ROOT/'styles.css',ROOT/'assets/fonts/manrope.css']:
    for raw in re.findall(r'url\([\"\']?([^\)\"\']+)',sheet.read_text(encoding='utf-8')):
        if not raw.startswith(('http','data:')) and not (sheet.parent/raw).exists():errors.append(f'{sheet.name}: missing asset {raw}')
print(f'Checked {len(pages)} pages, internal links, fragments, assets, headings and copy.')
for error in errors: print('ERROR',error)
raise SystemExit(bool(errors))
