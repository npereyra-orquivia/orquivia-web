"""SEO for the actual bilingual static pages, with separate preview/indexable output."""
from html import escape
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
import json

DESCRIPTIONS = {
 'home': ('Consultoría de procesos para despachos de arquitectura. Automatizaciones, apps a medida y conexión de plataformas para coordinar proyectos y entregas.', 'Process consulting for architecture practices. Automation, custom apps and platform integrations for project coordination and delivery.'),
 'consulting': ('Analizamos el proceso de tu despacho de arquitectura y desarrollamos automatizaciones o apps para avanzar hacia entregas, hitos y más capacidad.', 'We analyse your architecture practice’s workflow and build automation or custom apps to improve delivery, milestones and capacity.'),
 'applications': ('Procesos que se repiten en despachos y gestión de proyectos de arquitectura: altas de encargos, documentación pendiente, cambios y seguimiento de hitos.', 'Recurring architecture practice and project management workflows: commission intake, outstanding documents, change requests and milestone tracking.'),
 'documents': ('Automatización documental para arquitectura: recogida de información, documentos desde datos validados y avisos para avanzar hacia la siguiente entrega.', 'Document automation for architecture: information collection, documents from validated data and reminders that move the next delivery forward.'),
 'coordination': ('Apps a medida para despachos de arquitectura: expedientes, solicitudes, estados, responsables e hitos en una aplicación adaptada a vuestro proceso.', 'Custom apps for architecture practices: project records, requests, status, owners and milestones in an application designed around your workflow.'),
 'integrations': ('Conectamos las plataformas de tu despacho de arquitectura para sincronizar datos, documentos y estados con validaciones y seguimiento de incidencias.', 'Connect your architecture practice’s platforms to synchronise data, documents and status with validation and issue monitoring.'),
 'value-retail': ('Caso real de Value Retail: análisis de planos existentes y definición de un estándar gráfico común para leer y compartir proyectos con clientes.', 'Value Retail case study: analysing existing drawings and establishing a shared graphic standard for reading and sharing projects with clients.'),
 'about': ('Nicole Pereyra, fundadora de Orquivia. Consultoría de procesos, automatizaciones y soluciones a medida para despachos de arquitectura.', 'Meet Nicole Pereyra, founder of Orquivia. Process consulting, automation and tailored solutions for architecture practices.'),
 'ideas': ('Ideas prácticas para arquitectura: automatizar altas, controlar documentación, conectar plataformas y diseñar apps para el seguimiento de proyectos.', 'Practical insights for architecture: automate intake, track documents, connect platforms and design apps for project tracking.'),
 'contact': ('Cuéntanos un proceso de tu despacho de arquitectura. Primera conversación sobre automatizaciones, aplicaciones a medida o conexión de plataformas.', 'Tell us about a workflow in your architecture practice. An initial conversation about automation, custom applications or platform integrations.'),
 'legal': ('Identificación y datos de contacto de Orquivia Global SL, titular del sitio orquivia.com. Información legal sobre su actividad y el uso de la web.', 'Identity and contact details of Orquivia Global SL, owner of orquivia.com. Legal information about its activity and this website.'),
 'terms': ('Condiciones de uso de la web de Orquivia: consultas, propuestas de servicios, propiedad intelectual, enlaces y legislación aplicable.', 'Terms of use for the Orquivia website: enquiries, service proposals, intellectual property, links and applicable law.'),
 'cookies': ('Información sobre consultas, datos personales, derechos, proveedores y cookies en la web de Orquivia Global SL.', 'Information about enquiries, personal data, rights, providers and cookies on the Orquivia Global SL website.'),
}
SEO_TITLES = {
 'home': ('Automatización para despachos de arquitectura', 'Automation for architecture practices'),
 'consulting': ('Consultoría de procesos para arquitectura', 'Process consulting for architecture'),
 'applications': ('Procesos de despachos y proyectos de arquitectura', 'Architecture practice and project workflows'),
 'documents': ('Automatización documental para arquitectura', 'Document automation for architecture'),
 'coordination': ('Apps a medida para despachos de arquitectura', 'Custom apps for architecture practices'),
 'integrations': ('Integración de plataformas para arquitectura', 'Platform integrations for architecture'),
 'ideas': ('Ideas de automatización y apps para arquitectura', 'Automation and app insights for architecture'),
 'contact': ('Contacto y primera llamada de consultoría', 'Contact and initial consulting call'),
}
IMAGES = {'documents': 'automatizacion-documental-v2', 'coordination': 'app-seguimiento-v2', 'integrations': 'plataformas-conectadas-v2', 'contact': 'studio', 'about': 'studio', 'value-retail': 'documents'}

def page_url(origin, key, lang, routes):
    return urljoin(origin, '' if key == 'home' and lang == 0 else routes[key][lang])

def metadata(key, lang, routes, titles, articles, origin, indexable=False):
    title = SEO_TITLES.get(key, titles[key])[lang] + ' | Orquivia'
    desc = articles[key]['summary'][lang] if key in articles else DESCRIPTIONS[key][lang]
    image_name = articles[key]['image'] if key in articles else IMAGES.get(key, 'hero')
    image_url = urljoin(origin, 'assets/editorial/' + image_name + '.webp')
    # Head metadata escapes once; JSON-LD is serialized separately.
    title, desc = escape(title, quote=True), escape(desc, quote=True)
    canonical = page_url(origin, key, lang, routes)
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{page_url(origin,key,i,routes)}">' for code,i in [('es',0),('en',1),('x-default',0)])
    robots = 'index, follow, max-image-preview:large' if indexable else 'noindex, nofollow'
    image_alt = ('Composición editorial de procesos y tecnología para arquitectura', 'Editorial composition of architecture workflows and technology')[lang]
    return f'''<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">{alternates}
<meta property="og:site_name" content="Orquivia"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="{'article' if key in articles else 'website'}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{'es_ES' if lang==0 else 'en_GB'}"><meta property="og:locale:alternate" content="{'en_GB' if lang==0 else 'es_ES'}"><meta property="og:image" content="{image_url}"><meta property="og:image:alt" content="{image_alt}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{image_url}"><meta name="twitter:image:alt" content="{image_alt}">'''

def structured_data(key, lang, routes, titles, articles, settings):
    origin = settings['site_url']
    current = page_url(origin,key,lang,routes)
    language = ('es','en')[lang]
    org_id, site_id = origin+'#organization', origin+'#website'
    organization = {'@type':'Organization','@id':org_id,'name':'Orquivia','legalName':settings['company'],'url':origin,'logo':urljoin(origin,'assets/logo-completo.svg'),'email':settings['email'],'telephone':settings['phone']}
    website = {'@type':'WebSite','@id':site_id,'url':origin,'name':'Orquivia','publisher':{'@id':org_id},'inLanguage':['es','en']}
    description = articles[key]['summary'][lang] if key in articles else DESCRIPTIONS[key][lang]
    page = {'@type':'WebPage','@id':current+'#webpage','url':current,'name':titles[key][lang],'description':description,'inLanguage':language,'isPartOf':{'@id':site_id},'about':{'@id':org_id}}
    graph = [organization,website,page]
    if key != 'home':
        crumbs=[{'@type':'ListItem','position':1,'name':('Inicio','Home')[lang],'item':page_url(origin,'home',lang,routes)}]
        if key in articles:
            crumbs.append({'@type':'ListItem','position':2,'name':('Ideas','Insights')[lang],'item':page_url(origin,'ideas',lang,routes)})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':titles[key][lang],'item':current})
        graph.append({'@type':'BreadcrumbList','@id':current+'#breadcrumb','itemListElement':crumbs})
        page['breadcrumb']={'@id':current+'#breadcrumb'}
    if key in articles:
        item=articles[key]
        graph.append({'@type':'Article','@id':current+'#article','headline':item['title'][lang],'description':item['summary'][lang],'image':urljoin(origin,'assets/editorial/'+item['image']+'.webp'),'inLanguage':language,'mainEntityOfPage':{'@id':current+'#webpage'},'author':{'@id':org_id},'publisher':{'@id':org_id}})
    if key in ('consulting','documents','coordination','integrations'):
        graph.append({'@type':'Service','@id':current+'#service','name':titles[key][lang],'description':description,'serviceType':SEO_TITLES[key][lang],'url':current,'provider':{'@id':org_id}})
    data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    return '<script type="application/ld+json">'+data+'</script>'

def sitemap(routes, origin):
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml='http://www.w3.org/1999/xhtml'
    ET.register_namespace('',ns); ET.register_namespace('xhtml',xhtml)
    root=ET.Element('{'+ns+'}urlset')
    for key in routes:
        for lang in (0,1):
            entry=ET.SubElement(root,'{'+ns+'}url')
            ET.SubElement(entry,'{'+ns+'}loc').text=page_url(origin,key,lang,routes)
            for code,i in [('es',0),('en',1),('x-default',0)]:
                ET.SubElement(entry,'{'+xhtml+'}link',{'rel':'alternate','hreflang':code,'href':page_url(origin,key,i,routes)})
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'
