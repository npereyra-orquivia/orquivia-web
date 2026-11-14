"""Small semantic diagrams for editorial pages; no invented product screenshots."""
from html import escape

def workflow_figure(story, lang, compact=False):
    steps = ''.join(f'<li><span class="flow-node-number" aria-hidden="true">{i+1:02}</span><div><h3>{escape(title[lang])}</h3><p>{escape(description[lang])}</p></div></li>' for i, (title, description) in enumerate(story['steps']))
    return f'<figure class="workflow-figure {"workflow-compact" if compact else ""}"><div class="workflow-caption"><span class="eyebrow">{("El recorrido, de un vistazo", "The workflow at a glance")[lang]}</span><h2>{escape(story["title"][lang])}</h2></div><ol class="flow-nodes">{steps}</ol><figcaption>{escape(story["note"][lang])}</figcaption></figure>'
