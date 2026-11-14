"""Human-readable bilingual directory of the site's actual generated routes."""
from html import escape

PAGE_GROUPS = [
    ('principales', ('Páginas principales', 'Main pages'), [
        ('home', ('Inicio', 'Home')),
        ('consulting', ('Consultoría', 'Consulting')),
        ('applications', ('Para quién', 'Who it is for')),
        ('value-retail', ('Caso real · Value Retail', 'Case study · Value Retail')),
        ('about', ('Sobre Orquivia', 'About Orquivia')),
        ('ideas', ('Ideas', 'Insights')),
        ('contact', ('Contacto', 'Contact')),
    ]),
    ('servicios', ('Servicios', 'Services'), [
        ('documents', ('Procesos y documentación', 'Processes and documents')),
        ('operations', ('Coordinación de actuaciones', 'Project coordination')),
        ('coordination', ('Aplicaciones a medida', 'Custom applications')),
        ('integrations', ('Automatizaciones y conexiones', 'Automation and integrations')),
    ]),
    ('ideas', ('Artículos de Ideas', 'Insight articles'), [
        ('article-onboarding', None), ('article-status', None),
        ('article-app', None), ('article-documents', None),
        ('article-changes', None), ('article-milestone', None),
        ('article-process', None), ('article-step', None),
    ]),
    ('informacion', ('Información legal y navegación', 'Legal information and navigation'), [
        ('legal', ('Aviso legal', 'Legal notice')),
        ('terms', ('Condiciones de uso', 'Terms of use')),
        ('cookies', ('Privacidad y cookies', 'Privacy and cookies')),
        ('site-map', ('Mapa web', 'Site map')),
    ]),
]

def render_directory(lang, routes, titles):
    jump = ''.join(f'<a href="#{group}">{escape(label[lang])}</a>' for group, label, _ in PAGE_GROUPS)
    output = [f'<nav class="directory-jump" aria-label="{("Grupos de páginas", "Page groups")[lang]}">{jump}</nav>']
    number = 0
    for group, label, entries in PAGE_GROUPS:
        rows = []
        for key, names in entries:
            if key not in routes:
                continue
            number += 1
            names = names or titles[key]
            rows.append(f'<li class="directory-row"><span class="directory-number">{number:02}</span><a class="directory-title" href="{escape(routes[key][lang], quote=True)}">{escape(names[lang])}<span aria-hidden="true">↗</span></a><div class="directory-languages"><a href="{escape(routes[key][0], quote=True)}" lang="es" aria-label="Español: {escape(names[0], quote=True)}">ES</a><a href="{escape(routes[key][1], quote=True)}" lang="en" aria-label="English: {escape(names[1], quote=True)}">EN</a></div></li>')
        output.append(f'<section class="directory-group" id="{group}"><div class="directory-group-heading"><h2>{escape(label[lang])}</h2><span>{len(rows):02}</span></div><ol class="directory-list">{"".join(rows)}</ol></section>')
    return '<div class="section page-directory">' + ''.join(output) + '</div>'
