"""Build docs.indrayam.com home: 4th sibling of indrayam.com / dailydiff / resume.
Shares v1 style.css (shipped verbatim as /style.css) + blog header/nav/copyright."""
import sys,html,shutil,os
site=sys.argv[1]
V1='/workspace/dorothy-docs/_src/indrayam-site/v1'
IMG='/tmp/iv1/images' if os.path.isdir('/tmp/iv1/images') else '/workspace/dorothy-docs/_build/assets/images'
# PUBLIC allowlist only. Newest first. (slug,title,date ISO,topic,summary)
DOCS=[
("pstack","pstack","2026-10-21","AI tooling","Lauren Tan’s pack of agent skills for Cursor: one router, /poteto-mode, picks a playbook and pulls in skills and principles as needed."),
("diagram-design","Diagram Design","2026-10-20","AI tooling","An agent skill that draws diagrams as one self-contained HTML file with hand-placed inline SVG in a strict editorial style. 45 types shown."),
("illo","Illo","2026-10-20","AI tooling","Turns an idea into an editorial illustration, labelled explainer or transparent cutout, with pixels from an external image model."),
("drawio","Draw.io","2026-10-20","AI tooling","jgraph’s draw.io skill: one SKILL.md shared across four agent plugins, backed by the draw.io MCP servers."),
("pretty-mermaid","Pretty Mermaid","2026-10-20","AI tooling","Renders Mermaid diagrams to themed SVG/PNG with the beautiful-mermaid package. No headless browser needed."),
("excalidraw","Excalidraw","2026-10-20","AI tooling","An MCP server plus skill: a live Excalidraw canvas, REST and WebSocket sync, and headless PNG/SVG export."),
]
BLOCK={'ai-native-assessment','ai-harness-setup'}
assert not BLOCK & {d[0] for d in DOCS}
import datetime
def fmt(d): return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
DOCS.sort(key=lambda d:d[2],reverse=True)
shutil.copy(V1+'/style.css',site+'/style.css')
os.makedirs(site+'/images',exist_ok=True)
for f in ('favicon.ico','me.gif','blue-dash.gif'): shutil.copy(f'{IMG}/{f}',site+'/images/'+f)
E=html.escape
HEADER=open('/workspace/dorothy-docs/_build/header.html').read()
items="\n".join(f'''<li class="doc-entry"><h4 class="doc-title"><a href="/{s}/">{E(t)}</a></h4>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time> &mdash; {E(tp)}</p><p class="doc-summary">{E(sm)}</p></li>''' for s,t,d,tp,sm in DOCS)
topics=sorted({d[3] for d in DOCS})
desc="Anand Sharma’s docs: long-form explainers on AI tooling, agent skills and whatever else I’m learning."
page=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anand Sharma's Docs</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://docs.indrayam.com/">
<meta property="og:type" content="website"><meta property="og:title" content="Anand Sharma&#x27;s Docs">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="https://docs.indrayam.com/">
<meta property="og:site_name" content="Anand Sharma&#x27;s Docs">
<meta name="theme-color" content="#e7651a">
<link rel="Shortcut Icon" href="/images/favicon.ico">
<link rel="stylesheet" href="/style.css">
<style>
/* docs.indrayam.com: only additions; tokens come from shared style.css */
.docs-brand{{margin:0 0 4px}}
.docs-masthead-name{{font-family:"monotype corsiva",var(--font-heading);font-style:italic;font-size:2.1em;font-weight:700;margin:0;line-height:1.1;color:var(--color-heading)}}
.docs-tagline{{font-family:var(--font-ui);font-size:.8rem;letter-spacing:.09em;text-transform:uppercase;color:var(--color-accent);font-weight:700;margin:0 0 10px}}
.docs-intro{{margin:0 0 14px;color:var(--color-content)}}
.post ul.doc-list{{margin:0;padding:0}}
.doc-entry{{padding:12px 0 12px 14px;border-left:4px solid var(--color-quote-border);margin:0 0 10px;background:var(--color-panel)}}
.doc-entry:hover{{border-left-color:var(--color-accent);background:var(--color-panel-alt)}}
.doc-title{{font-family:var(--font-heading);font-size:1.2em;font-weight:700;color:var(--color-heading);margin:0}}
.doc-title a{{color:var(--color-link)}}
.doc-meta{{font-family:var(--font-ui);font-size:.82rem;color:var(--color-muted);margin:2px 0 4px}}
.doc-summary{{margin:0;font-size:.95em;line-height:1.45}}
.docs-topics{{font-family:var(--font-ui);font-size:.85rem;color:var(--color-muted);margin-top:14px;border-top:1px dashed var(--color-border-light);padding-top:8px}}
</style>
</head>
<body>
{HEADER}

<main class="post archives-page">
<h2>Notes &amp; Explainers</h2>
<p class="docs-intro">Single-page explainers on things I’m using and learning: how they work, what they measure, where they fall short.</p>
<ul class="doc-list">
{items}
</ul>
<p class="docs-topics">Topics: {", ".join(E(t) for t in topics)} &middot; {len(DOCS)} docs</p>
</main>
<p></p>
<div class="copyright">
    <a href="http://creativecommons.org/licenses/by-nd-nc/1.0/">Copyright</a> &copy; 2026 Anand Sharma. <a href="https://indrayam.com/disclaimer.html">Disclaimer</a>
</div>
</body>
</html>
'''
open(site+'/index.html','w').write(page)
