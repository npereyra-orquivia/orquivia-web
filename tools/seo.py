"""SEO for the actual bilingual static pages, with separate preview/indexable output."""
from html import escape
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
import json

DESCRIPTIONS = {
 'home': ('Organización, coordinación y herramientas a medida para arquitectura y gestión de proyectos, con experiencia también en pequeñas empresas.', 'Organisation, coordination and tailored tools for architecture and project management, with experience in small businesses too.'),
 'consulting': ('Consultoría para organizar el trabajo de tu empresa: documentación, coordinación y herramientas a medida que encajan con tus procesos actuales.', 'Consulting to organise your business workflows: documentation, coordination and tailored tools that fit your existing processes.'),
 'applications': ('Organización y herramientas a medida para arquitectura y gestores de proyectos. Experiencia también en pequeñas empresas y equipos de postventa.', 'Organisation and tailored tools for architecture practices and project managers. Experience also includes small businesses and after-sales teams.'),
 'documents': ('Organización de documentación y procesos: criterios comunes, información localizable y pasos claros para preparar, revisar y compartir el trabajo.', 'Document and workflow organisation: shared standards, accessible information and clear steps for preparing, reviewing and sharing work.'),
 'operations': ('Coordinación de actuaciones concretas: tareas, materiales, responsables y tiempos organizados para llevar una intervención a término.', 'Coordination of specific assignments: tasks, materials, responsibilities and timing organised to carry an intervention through.'),
 'coordination': ('Apps a medida para presupuestos, facturas, gastos y consultas de proyectos, incluido seguimiento visual desde un plano para project managers.', 'Custom apps for quotations, invoices, expenses and project queries, including visual tracking from a drawing for project managers.'),
 'integrations': ('Conexión de plataformas y automatizaciones para que la información circule entre las herramientas que ya utiliza tu empresa.', 'Platform integrations and automation that let information move between the tools your business already uses.'),
 'value-retail': ('Caso real de Value Retail: análisis de planos existentes y definición de un estándar gráfico común para leer y compartir proyectos con clientes.', 'Value Retail case study: analysing existing drawings and establishing a shared graphic standard for reading and sharing projects with clients.'),
 'about': ('Nicole Pereyra, fundadora de Orquivia. Organización del trabajo, coordinación de actuaciones y herramientas de gestión adaptadas a cada empresa.', 'Meet Nicole Pereyra, founder of Orquivia. Workflow organisation, coordination and management tools tailored to each business.'),
 'ideas': ('Ideas prácticas para arquitectura: automatizar altas, controlar documentación, conectar plataformas y diseñar apps para el seguimiento de proyectos.', 'Practical insights for architecture: automate intake, track documents, connect platforms and design apps for project tracking.'),
 'contact': ('Cuéntanos qué necesitas organizar o gestionar en tu empresa. Primera conversación sobre documentación, coordinación o herramientas a medida.', 'Tell us what you need to organise or manage in your business. An initial conversation about documentation, coordination or tailored tools.'),
 'legal': ('Identificación y datos de contacto de Orquivia Global SL, titular del sitio orquivia.com. Información legal sobre su actividad y el uso de la web.', 'Identity and contact details of Orquivia Global SL, owner of orquivia.com. Legal information about its activity and this website.'),
 'terms': ('Condiciones de uso de la web de Orquivia: consultas, propuestas de servicios, propiedad intelectual, enlaces y legislación aplicable.', 'Terms of use for the Orquivia website: enquiries, service proposals, intellectual property, links and applicable law.'),
 'cookies': ('Información sobre consultas, datos personales, derechos, proveedores y cookies en la web de Orquivia Global SL.', 'Information about enquiries, personal data, rights, providers and cookies on the Orquivia Global SL website.'),
}
SEO_TITLES = {
 'home': ('Organización y herramientas de gestión a medida', 'Workflow organisation and tailored management tools'),
 'consulting': ('Consultoría de organización y procesos', 'Organisation and process consulting'),
 'applications': ('Organización y gestión para cada empresa', 'Organisation and management for each business'),
 'documents': ('Organización de documentación y procesos', 'Document and workflow organisation'),
 'operations': ('Coordinación de actuaciones y tareas', 'Coordination of assignments and tasks'),
 'coordination': ('Apps y herramientas de gestión a medida', 'Custom apps and management tools'),
 'integrations': ('Automatizaciones y conexión de plataformas', 'Automation and platform integrations'),
 'about': ('Nicole Pereyra, fundadora de Orquivia', 'Nicole Pereyra, founder of Orquivia'),
 'ideas': ('Ideas de automatización y apps para arquitectura', 'Automation and app insights for architecture'),
 'contact': ('Contacto y primera llamada de consultoría', 'Contact and initial consulting call'),
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
    image_alt = ('Orquivia · Organización, coordinación y herramientas a medida', 'Orquivia · Organisation, coordination and tailored tools')[lang]
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
