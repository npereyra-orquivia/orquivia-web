"""SEO for the actual bilingual static pages, with separate preview/indexable output."""
from html import escape
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
import json

DESCRIPTIONS = {
 'home': ('Organización de documentación, coordinación y herramientas de gestión a medida para despachos de arquitectura y project managers.', 'Document organisation, coordination and tailored management tools for architecture practices and project managers.'),
 'consulting': ('Consultoría para despachos de arquitectura y gestores de proyectos: documentación, coordinación y herramientas que encajan con sus procesos actuales.', 'Consulting for architecture practices and project managers: documentation, coordination and tools that fit their existing workflows.'),
 'applications': ('Soluciones para despachos de arquitectura y project managers: organizar información, coordinar actuaciones y crear herramientas de gestión a medida.', 'Solutions for architecture practices and project managers: organise information, coordinate assignments and build tailored management tools.'),
 'documents': ('Documentación y procesos para arquitectura: criterios comunes, información localizable y pasos claros para preparar, revisar y compartir el trabajo.', 'Documents and workflows for architecture: shared standards, accessible information and clear steps for preparing, reviewing and sharing work.'),
 'operations': ('Coordinación de actuaciones para arquitectura y project managers: tareas, materiales, responsables y tiempos organizados para una intervención concreta.', 'Coordination for architecture practices and project managers: tasks, materials, responsibilities and timing organised for a specific intervention.'),
 'coordination': ('Apps para arquitectura y project managers: presupuestos, facturas, gastos y consultas de proyectos, con seguimiento visual desde un plano.', 'Apps for architecture practices and project managers: quotations, invoices, expenses and project queries, with visual tracking from a drawing.'),
 'integrations': ('Automatizaciones y conexión de plataformas para despachos de arquitectura y project managers, a partir de las herramientas que ya utilizan.', 'Automation and platform integrations for architecture practices and project managers, built around the tools they already use.'),
 'value-retail': ('Caso real de Value Retail: análisis de planos existentes y definición de un estándar gráfico común para leer y compartir proyectos con clientes.', 'Value Retail case study: analysing existing drawings and establishing a shared graphic standard for reading and sharing projects with clients.'),
 'about': ('Nicole Pereyra, fundadora de Orquivia. Organización, coordinación y herramientas de gestión a medida para arquitectura y project managers.', 'Meet Nicole Pereyra, founder of Orquivia. Organisation, coordination and tailored management tools for architecture practices and project managers.'),
 'ideas': ('Ideas prácticas para arquitectura: automatizar altas, controlar documentación, conectar plataformas y diseñar apps para el seguimiento de proyectos.', 'Practical insights for architecture: automate intake, track documents, connect platforms and design apps for project tracking.'),
 'contact': ('Hablemos de la gestión de tu despacho o proyecto de arquitectura: documentación, coordinación y herramientas a medida para vuestro proceso.', 'Discuss the management of your architecture practice or project: documentation, coordination and tools tailored to your workflow.'),
 'legal': ('Identificación y datos de contacto de Orquivia Global SL, titular del sitio orquivia.com. Información legal sobre su actividad y el uso de la web.', 'Identity and contact details of Orquivia Global SL, owner of orquivia.com. Legal information about its activity and this website.'),
 'terms': ('Condiciones de uso de la web de Orquivia: consultas, propuestas de servicios, propiedad intelectual, enlaces y legislación aplicable.', 'Terms of use for the Orquivia website: enquiries, service proposals, intellectual property, links and applicable law.'),
 'cookies': ('Información sobre consultas, datos personales, derechos, proveedores y cookies en la web de Orquivia Global SL.', 'Information about enquiries, personal data, rights, providers and cookies on the Orquivia Global SL website.'),
}
SEO_TITLES = {
 'home': ('Consultoría de gestión para arquitectura', 'Management consulting for architecture'),
 'consulting': ('Consultoría para arquitectura y project managers', 'Consulting for architecture and project managers'),
 'applications': ('Soluciones para arquitectura y project managers', 'Solutions for architecture and project managers'),
 'documents': ('Documentación y procesos para arquitectura', 'Documents and workflows for architecture'),
 'operations': ('Coordinación operativa para arquitectura', 'Operational coordination for architecture'),
 'coordination': ('Apps de gestión para arquitectura y project managers', 'Management apps for architecture and project managers'),
 'integrations': ('Automatización e integraciones para arquitectura', 'Automation and integrations for architecture'),
 'about': ('Nicole Pereyra, fundadora de Orquivia', 'Nicole Pereyra, founder of Orquivia'),
 'ideas': ('Ideas de automatización y apps para arquitectura', 'Automation and app insights for architecture'),
 'contact': ('Hablemos de tu despacho o proyecto de arquitectura', 'Discuss your architecture practice or project'),
}

def share_image(origin, lang):
    return urljoin(origin, 'assets/diagrams/orquivia-share-' + ('es', 'en')[lang] + '.png')

def page_url(origin, key, lang, routes):
    return urljoin(origin, '' if key == 'home' and lang == 0 else routes[key][lang])

def metadata(key, lang, routes, titles, articles, origin, indexable=False):
    title = SEO_TITLES.get(key, titles[key])[lang] + ' | Orquivia'
    desc = articles[key]['summary'][lang] if key in articles else DESCRIPTIONS[key][lang]
    image_url = share_image(origin, lang)
    # Head metadata escapes once; JSON-LD is serialized separately.
    title, desc = escape(title, quote=True), escape(desc, quote=True)
    canonical = page_url(origin, key, lang, routes)
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{page_url(origin,key,i,routes)}">' for code,i in [('es',0),('en',1),('x-default',0)])
    robots = 'index, follow, max-image-preview:large' if indexable else 'noindex, nofollow'
    image_alt = ('Orquivia · Organización, coordinación y herramientas para arquitectura', 'Orquivia · Organisation, coordination and tools for architecture')[lang]
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
        graph.append({'@type':'Article','@id':current+'#article','headline':item['title'][lang],'description':item['summary'][lang],'image':share_image(origin,lang),'inLanguage':language,'mainEntityOfPage':{'@id':current+'#webpage'},'author':{'@id':org_id},'publisher':{'@id':org_id}})
    if key in ('consulting','documents','operations','coordination','integrations'):
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
