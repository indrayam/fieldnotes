"""Build docs.indrayam.com home: 4th sibling of indrayam.com / dailydiff / resume.
Shares v1 style.css (shipped verbatim as /style.css) + blog header/nav/copyright."""
import sys,html,shutil,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import src, SITE, ASSETS, BUILD
site=sys.argv[1] if len(sys.argv)>1 else SITE
V1=src('INDRAYAM_V1_SRC')
IMG=os.path.join(ASSETS,'images')
# PUBLIC allowlist only. Newest first. (slug,title,date ISO,topic,summary)
DOCS=[
("pstack","pstack","2026-10-21","AI tooling","Lauren Tan’s pack of agent skills for Cursor: one router, /poteto-mode, picks a playbook and pulls in skills and principles as needed."),
("diagram-design","Diagram Design","2026-10-20","AI tooling","An agent skill that draws diagrams as one self-contained HTML file with hand-placed inline SVG in a strict editorial style. 45 types shown."),
("illo","Illo","2026-10-20","AI tooling","Turns an idea into an editorial illustration, labelled explainer or transparent cutout, with pixels from an external image model."),
("drawio","Draw.io","2026-10-20","AI tooling","jgraph’s draw.io skill: one SKILL.md shared across four agent plugins, backed by the draw.io MCP servers."),
("pretty-mermaid","Pretty Mermaid","2026-10-20","AI tooling","Renders Mermaid diagrams to themed SVG/PNG with the beautiful-mermaid package. No headless browser needed."),
("excalidraw","Excalidraw","2026-10-20","AI tooling","An MCP server plus skill: a live Excalidraw canvas, REST and WebSocket sync, and headless PNG/SVG export."),
]
# Separate homepage section (Sutra's steer): one doc per skill from github.com/mattpocock/skills.
MP=[
("mattpocock-grill-with-docs","mattpocock/grill-with-docs","2026-10-23","Matt Pocock skills","A relentless design interview that writes a glossary and ADRs as you go. Two lines that load grilling and domain-modeling."),
("mattpocock-wayfinder","mattpocock/wayfinder","2026-10-23","Matt Pocock skills","Plans work too big for one session as a map of decision tickets on your issue tracker, resolved one ticket per session."),
("mattpocock-to-spec-to-tickets","mattpocock/to-spec → to-tickets","2026-10-23","Matt Pocock skills","Turns a finished conversation into a published spec, then a graph of tracer-bullet tickets that implement-spec builds."),
("mattpocock-handoff","mattpocock/handoff","2026-10-23","Matt Pocock skills","Compacts a conversation into a temp-folder note a fresh agent can pick up, with suggested skills and links instead of copies."),
("mattpocock-setup-matt-pocock-skills","mattpocock/setup-matt-pocock-skills","2026-10-23","Matt Pocock skills","A one-time interview that tells the engineering skills where your tracker, triage labels and glossary live."),
]
BLOCK={'ai-native-assessment','ai-harness-setup'}
assert not BLOCK & {d[0] for d in DOCS+MP}
import datetime
def fmt(d): return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
DOCS.sort(key=lambda d:d[2],reverse=True)
shutil.copy(V1+'/style.css',site+'/style.css')
os.makedirs(site+'/images',exist_ok=True)
for f in ('favicon.ico','me.gif','blue-dash.gif'): shutil.copy(f'{IMG}/{f}',site+'/images/'+f)
E=html.escape
HEADER=open(os.path.join(BUILD,'header.html')).read()
def li(s,t,d,tp,sm): return f'''<li class="doc-entry"><h4 class="doc-title"><a href="/{s}/">{E(t)}</a></h4>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time></p><p class="doc-summary">{E(sm)}</p></li>'''
POTETO=[d for d in DOCS if d[0]=='pstack']
STORY=[d for d in DOCS if d[0]!='pstack']
poteto_items="\n".join(li(*d) for d in POTETO)
story_items="\n".join(li(*d) for d in STORY)
items="\n".join(f'''<li class="doc-entry"><h4 class="doc-title"><a href="/{s}/">{E(t)}</a></h4>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time> &mdash; {E(tp)}</p><p class="doc-summary">{E(sm)}</p></li>''' for s,t,d,tp,sm in DOCS)
mp_items="\n".join(f'''<li class="doc-entry"><h4 class="doc-title"><a href="/{s}/">{E(t)}</a></h4>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time></p><p class="doc-summary">{E(sm)}</p></li>''' for s,t,d,tp,sm in MP)
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
.doc-entry{{padding:12px 0;margin:0 0 10px;background:var(--color-panel)}}
.doc-entry:hover{{background:var(--color-panel-alt)}}
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
<h2 id="poteto-skills" style="margin-top:28px">poteto Skills</h2>
<p class="docs-intro">Agent skills from Lauren Tan (poteto).</p>
<ul class="doc-list">
{poteto_items}
</ul>
<h2 id="matt-pocock-skills" style="margin-top:28px">Matt Pocock skills</h2>
<p class="docs-intro">One explainer per skill from <a href="https://github.com/mattpocock/skills">github.com/mattpocock/skills</a>, read at commit 5beb35b, with notes on pairing each with pstack.</p>
<ul class="doc-list">
{mp_items}
</ul>
<h2 id="storytelling-skills" style="margin-top:28px">Storytelling Skills</h2>
<p class="docs-intro">Skills for diagrams, illustrations and visual explanation.</p>
<ul class="doc-list">
{story_items}
</ul>
<p class="docs-topics">Topics: {", ".join(E(t) for t in ["poteto Skills","Matt Pocock skills","Storytelling Skills"])} &middot; {len(DOCS)+len(MP)} docs</p>
</main>
<p></p>
<div class="copyright">
    <a href="http://creativecommons.org/licenses/by-nd-nc/1.0/">Copyright</a> &copy; 2026 Anand Sharma. <a href="https://indrayam.com/disclaimer.html">Disclaimer</a>
</div>
</body>
</html>
'''
open(site+'/index.html','w').write(page)
