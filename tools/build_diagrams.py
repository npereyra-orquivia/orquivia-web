"""Render Orquivia's honest editorial workflow diagrams and sharing cards.

These drawings illustrate service categories. They are deliberately diagrams,
not screenshots of deployed software or photographs of client work.
Run from any directory: python tools/build_diagrams.py
"""
from html import escape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'assets' / 'diagrams'
PAPER = '#faf8f2'
INK = '#172531'
SAGE = '#dbe6de'
GOLD = '#d7b461'
TEAL = '#406c6c'
MUTED = '#57636a'
LINE = '#bdc9c3'


def text(x, y, label, size=36, color=INK, anchor='start', weight=500, spacing=0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}">{escape(label)}</text>')


def line(x1, y1, x2, y2, color=LINE, width=3, arrow=False):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" '
            f'{"marker-end=\"url(#arrow)\"" if arrow else ""}/>')


def document_icon(x, y, color=TEAL):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 0 H34 L48 14 V64 H0 Z"/><path d="M34 0 V14 H48"/>'
            '<path d="M12 31 H35 M12 42 H35 M12 53 H27"/></g>')


def target_icon(x, y, color=TEAL):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="26" cy="32" r="25"/><circle cx="26" cy="32" r="11"/>'
            '<path d="M26 7 V0 M26 64 V57 M1 32 H-6 M58 32 H51"/></g>')


def check_icon(x, y, color=TEAL):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="0" y="4" width="54" height="54" rx="12"/>'
            '<path d="M13 31 L23 41 L42 21"/></g>')


def time_icon(x, y, color=TEAL):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="27" cy="31" r="26"/><path d="M27 13 V31 L41 39"/></g>')


def connection_icon(x, y, color=TEAL):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="9" cy="32" r="8"/><circle cx="45" cy="8" r="8"/>'
            '<circle cx="45" cy="56" r="8"/><path d="M17 32 H29 V8 H37 M29 32 V56 H37"/></g>')


ICONS = {'document': document_icon, 'target': target_icon, 'check': check_icon,
         'time': time_icon, 'connection': connection_icon}


def node(x, y, label, number, icon='document', fill=PAPER, width=360, height=250):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="26" '
            f'fill="{fill}" stroke="{LINE}" stroke-width="2"/>'
            + text(x+width-30, y+44, number, 23, MUTED, 'end', spacing=2)
            + ICONS[icon](x+34, y+36)
            + text(x+34, y+height-36, label, 35))


def frame(kind, lang, title, contents):
    label = 'ESQUEMA DE TRABAJO' if lang == 'es' else 'WORKFLOW OUTLINE'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024" role="img" aria-labelledby="title description" lang="{lang}">
<title id="title">{escape(title)}</title>
<desc id="description">{escape(label)} · Orquivia</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M1 1 L7 4 L1 7" fill="none" stroke="{TEAL}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect width="1536" height="1024" fill="{PAPER}"/>
<g font-family="Manrope, Arial, sans-serif">
{text(120, 151, 'ORQUIVIA', 28, INK, spacing=4)}
{text(1416, 151, label, 22, MUTED, 'end', spacing=2)}
{line(120, 188, 1416, 188, LINE, 2)}
{text(120, 284, title, 43)}
{contents}
{line(120, 873, 1416, 873, LINE, 2)}
{text(120, 927, 'DOCUMENTACIÓN / COORDINACIÓN / HERRAMIENTAS' if lang=='es' else 'DOCUMENTATION / COORDINATION / TOOLS', 22, MUTED, spacing=1.4)}
</g></svg>'''


def sequence(labels, icons, fills=None):
    fills = fills or [PAPER, SAGE, PAPER]
    parts=[]
    for i, (label, icon, fill) in enumerate(zip(labels, icons, fills)):
        x=120+i*468
        parts.append(node(x, 414, label, f'0{i+1}', icon, fill))
        if i<2:
            parts.append(line(x+378, 539, x+444, 539, TEAL, 3, True))
    return ''.join(parts)


def diagram(kind, lang):
    en=lang=='en'
    if kind=='documents':
        title='A common standard.' if en else 'Un criterio común.'
        labels=['Standards','Documents','Reference'] if en else ['Criterio','Documentos','Consulta']
        content=sequence(labels, ['target','document','check'])
        content+=text(768, 755, 'Clear information, ready to use.' if en else 'Información clara, lista para utilizar.', 29, MUTED, 'middle')
    elif kind=='operations':
        title='From preparation to delivery.' if en else 'De la preparación a la entrega.'
        labels=['Preparation','Coordination','Delivery'] if en else ['Preparación','Coordinación','Entrega']
        content=sequence(labels,['document','time','check'],[PAPER,SAGE,'#eee5cd'])
        content+=line(300, 735, 1236, 735, LINE, 2)
        for x in [300,768,1236]:
            content+=f'<circle cx="{x}" cy="735" r="7" fill="{TEAL}"/>'
        content+=text(768, 803, 'Steps, people and timing.' if en else 'Pasos, personas y plazos.', 29, MUTED, 'middle')
    elif kind=='tools':
        title='Management tools that fit.' if en else 'Herramientas que encajan.'
        labels=['Quotes','Invoices','Expenses'] if en else ['Presupuestos','Facturas','Gastos']
        content=''
        for i,label in enumerate(labels):
            x=120+i*468
            content+=node(x, 366, label, f'0{i+1}', 'document', PAPER, height=194)
            content+=line(x+180, 560, x+180, 637, LINE, 2)
        content+=f'<path d="M300 637 H1236 M768 637 V685" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
        content+=f'<rect x="520" y="685" width="496" height="116" rx="24" fill="{SAGE}"/>'
        content+=text(768, 758, 'Your management' if en else 'Tu gestión', 38, INK, 'middle')
    elif kind=='connections':
        title='One connected workflow.' if en else 'Un recorrido conectado.'
        labels=['Source','Validation','Destination'] if en else ['Origen','Validación','Destino']
        content=sequence(labels,['document','check','connection'])
        content+=text(768, 755, 'Enter once. Keep working.' if en else 'Un dato se introduce. El trabajo continúa.', 29, MUTED, 'middle')
    elif kind=='workflow':
        title='A practical way to work.' if en else 'Una forma práctica de trabajar.'
        labels=['Documentation','Coordination','Tools'] if en else ['Documentación','Coordinación','Herramientas']
        content=sequence(labels,['document','time','connection'],[PAPER,SAGE,'#eee5cd'])
        content+=f'<path d="M1236 684 V755 H300 V684" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        content+=f'<circle cx="768" cy="755" r="7" fill="{GOLD}"/>'
    elif kind=='queries':
        title='Visual query tracking.' if en else 'Seguimiento visual de consultas.'
        content=(f'<rect x="120" y="370" width="750" height="410" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M470 370 V780 M470 570 H870" fill="none" stroke="{INK}" stroke-width="4"/>'
                 f'<rect x="335" y="368" width="90" height="7" fill="{PAPER}"/>'
                 f'<rect x="468" y="655" width="7" height="78" fill="{PAPER}"/>'
                 f'<rect x="868" y="425" width="7" height="74" fill="{PAPER}"/>'
                 f'<path d="M350 481 H915 V487 H1016" fill="none" stroke="{TEAL}" stroke-width="3" stroke-linecap="round"/>'
                 f'<rect x="1016" y="414" width="400" height="190" rx="24" fill="{SAGE}"/>'
                 + text(1048,465,'QUERY' if en else 'CONSULTA',23,TEAL,spacing=2)
                 + text(1048,529,'On the drawing' if en else 'Sobre el plano',34)
                 + text(1048,569,'Visual tracking' if en else 'Seguimiento visual',26,MUTED))
        for x,y,label in [(350,481,'01'),(666,670,'02')]:
            content+=f'<circle cx="{x}" cy="{y}" r="32" fill="{TEAL}" stroke="{PAPER}" stroke-width="6"/>'
            content+=text(x,y+10,label,25,PAPER,'middle',600)
    else:
        raise ValueError(kind)
    return frame(kind,lang,title,content)


def sharing(lang):
    font_path=ROOT/'assets/fonts/manrope-3.ttf'
    def font(size):return ImageFont.truetype(str(font_path),size)
    image=Image.new('RGB',(1200,630),INK)
    draw=ImageDraw.Draw(image)
    draw.text((84,62),'ORQUIVIA',font=font(55),fill=PAPER,stroke_width=0)
    draw.line((84,157,1116,157),fill='#5a6a6e',width=2)
    lines=['Organización,','coordinación y','herramientas a medida.'] if lang=='es' else ['Organisation,','coordination and','tailored tools.']
    y=208
    for label in lines:
        draw.text((84,y),label,font=font(58),fill=PAPER)
        y+=81
    draw.text((84,540),'ARQUITECTURA · PROJECT MANAGERS' if lang=='es' else 'ARCHITECTURE · PROJECT MANAGERS',font=font(22),fill=SAGE)
    for i,color in enumerate([SAGE,GOLD,PAPER]):
        x=956+i*62
        if i:draw.line((x-42,557,x-22,557),fill='#6f817e',width=2)
        draw.ellipse((x-16,541,x+16,573),fill=color)
    image.save(DEST/f'orquivia-share-{lang}.png',optimize=True)


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    for lang in ['es','en']:
        for kind in ['documents','operations','tools','connections','workflow','queries']:
            (DEST/f'process-{kind}-{lang}.svg').write_text(diagram(kind,lang),encoding='utf-8',newline='\n')
        sharing(lang)
    print(f'Created 12 workflow diagrams and 2 sharing cards in {DEST}.')


if __name__=='__main__':
    main()
