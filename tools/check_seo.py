"""Validate deployable SEO, local links, language pairs and structured-data references."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
import argparse
import json

class Head(HTMLParser):
    def __init__(self,text):
        super().__init__();self.meta={};self.links=[];self.title='';self.capture='';self.schemas=[];self.buffer='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link': self.links.append(a)
        if tag=='title': self.capture='title'
        if tag=='script' and a.get('type')=='application/ld+json': self.capture='schema'; self.buffer=''
    def handle_data(self,data):
        if self.capture=='title':self.title+=data
        if self.capture=='schema':self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='title':self.capture=''
        if tag=='script' and self.capture=='schema':self.schemas.append(json.loads(self.buffer));self.capture=''

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory',type=Path)
args=parser.parse_args()
root=args.directory.resolve()
pages={p.name:Head(p.read_text(encoding='utf-8')) for p in root.glob('*.html')}
errors=[];titles=set();descriptions=set();canonicals=set()
for name,page in pages.items():
    canonical=[a.get('href') for a in page.links if a.get('rel')=='canonical']
    if len(canonical)!=1: errors.append(name+': canonical missing or duplicated');continue
    canonical=canonical[0]
    parsed=urlsplit(canonical)
    if parsed.scheme!='https' or parsed.netloc!='orquivia.com':errors.append(name+': wrong production origin')
    expected='index.html' if parsed.path=='/' else parsed.path.lstrip('/')
    if expected!=name:errors.append(name+': canonical points to another page')
    if canonical in canonicals:errors.append(name+': duplicate canonical')
    canonicals.add(canonical)
    if page.title in titles:errors.append(name+': duplicate title')
    titles.add(page.title)
    desc=page.meta.get('description','')
    if not desc:errors.append(name+': missing description')
    if desc in descriptions:errors.append(name+': duplicate description')
    descriptions.add(desc)
    if 'noindex' in page.meta.get('robots','') or 'index' not in page.meta.get('robots',''):errors.append(name+': production is not indexable')
    if page.meta.get('og:url')!=canonical:errors.append(name+': social URL differs from canonical')
    for image_key in ('og:image','twitter:image'):
        image=urlsplit(page.meta.get(image_key,''))
        if image.netloc!='orquivia.com' or not (root/unquote(image.path.lstrip('/'))).is_file():errors.append(name+': missing '+image_key+' asset')
    alternates={a.get('hreflang'):a.get('href') for a in page.links if a.get('rel')=='alternate'}
    if set(alternates)!=set(('es','en','x-default')):errors.append(name+': incomplete language alternatives')
    for code,address in alternates.items():
        filename=urlsplit(address).path.lstrip('/') or 'index.html'
        other=pages.get(filename)
        if not other:errors.append(name+': alternate does not exist');continue
        reverse={a.get('hreflang'):a.get('href') for a in other.links if a.get('rel')=='alternate'}
        if reverse!=alternates:errors.append(name+': language links are not reciprocal')
    if len(page.schemas)!=1:errors.append(name+': structured data missing or duplicated');continue
    graph=page.schemas[0]['@graph']
    definitions={n['@id'] for n in graph}
    for node in graph:
        for field in ('publisher','provider','author','isPartOf','about','mainEntityOfPage','breadcrumb'):
            reference=node.get(field,{})
            if '@id' in reference and reference['@id'] not in definitions:errors.append(name+': dangling structured-data '+field)
    webpage=next((n for n in graph if n['@type']=='WebPage'),{})
    if webpage.get('url')!=canonical:errors.append(name+': schema page URL differs from canonical')
tree=ET.parse(root/'sitemap.xml')
locations={n.text for n in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
if locations!=canonicals:errors.append('sitemap does not match the generated pages')
if 'Disallow: /' in (root/'robots.txt').read_text():errors.append('robots blocks production')
print(f'Checked {len(pages)} production pages: titles, descriptions, canonical URLs, language pairs, sharing images, schemas and sitemap.')
for error in errors: print('ERROR',error)
raise SystemExit(bool(errors))
