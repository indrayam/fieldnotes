"""Build fieldnotes.indrayam.com home: 4th sibling of indrayam.com / dailydiff / resume.
Styled by build/style.css (shipped as /style.css); header.html holds the site nav."""
import sys,html,shutil,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import SITE, ASSETS, BUILD
site=sys.argv[1] if len(sys.argv)>1 else SITE
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
# Design Skills: one builder per project. Order fixed: Impeccable, Hallmark, UI/UX Pro Max.
DS=[
("pbakaus-impeccable","pbakaus/impeccable","2026-10-24","Design Skills","One skill, 24 commands and a no-LLM detector for app UI: PRODUCT.md, DESIGN.md, audit, critique, polish, bolder, quieter, animate."),
("nutlope-hallmark","nutlope/hallmark","2026-10-24","Design Skills","A landing-page skill with 48 themes, a 16-rule Floor and sloplint, a linter that fails AI tells before you ship."),
("nextlevelbuilder-ui-ux-pro-max","nextlevelbuilder/ui-ux-pro-max","2026-10-24","Design Skills","A searchable design reference, not a builder: when to search it and when to hand off to Impeccable or Hallmark."),
]
BLOCK={'ai-native-assessment','ai-harness-setup'}
assert not BLOCK & {d[0] for d in DOCS+MP+DS}
import datetime
def fmt(d): return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
DOCS.sort(key=lambda d:d[2],reverse=True)
shutil.copy(os.path.join(BUILD,'style.css'),site+'/style.css')
os.makedirs(site+'/images',exist_ok=True)
for f in ('favicon.ico','me.gif','blue-dash.gif'): shutil.copy(f'{IMG}/{f}',site+'/images/'+f)
# The icon shared by every indrayam.com site, served from the site root.
for f in ('favicon.ico','apple-touch-icon.png'): shutil.copy(f'{IMG}/{f}',site+'/'+f)
E=html.escape
HEADER=open(os.path.join(BUILD,'header.html')).read()
def li(s,t,d,tp,sm): return f'''<li class="doc-entry"><h3 class="doc-title"><a href="/{s}/">{E(t)}</a></h3>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time></p><p class="doc-summary">{E(sm)}</p></li>'''
POTETO=[d for d in DOCS if d[0]=='pstack']
STORY=[d for d in DOCS if d[0]!='pstack']
poteto_items="\n".join(li(*d) for d in POTETO)
story_items="\n".join(li(*d) for d in STORY)
ds_items="\n".join(li(*d) for d in DS)
items="\n".join(f'''<li class="doc-entry"><h3 class="doc-title"><a href="/{s}/">{E(t)}</a></h3>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time> &mdash; {E(tp)}</p><p class="doc-summary">{E(sm)}</p></li>''' for s,t,d,tp,sm in DOCS)
mp_items="\n".join(f'''<li class="doc-entry"><h3 class="doc-title"><a href="/{s}/">{E(t)}</a></h3>
<p class="doc-meta"><time datetime="{d}">{fmt(d)}</time></p><p class="doc-summary">{E(sm)}</p></li>''' for s,t,d,tp,sm in MP)
topics=sorted({d[3] for d in DOCS})
desc="Anand Sharma’s docs: long-form explainers on AI tooling, agent skills and whatever else I’m learning."
page=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Field Notes · Anand Sharma</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://fieldnotes.indrayam.com/">
<meta property="og:type" content="website"><meta property="og:title" content="Field Notes · Anand Sharma">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="https://fieldnotes.indrayam.com/">
<meta property="og:site_name" content="Field Notes · Anand Sharma">
<meta name="theme-color" content="#e7651a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300&amp;family=Lora:wght@400;700;900&amp;family=Newsreader:opsz,wght@6..72,400;6..72,700;6..72,900&amp;family=PT+Serif:wght@400;700&amp;family=Source+Sans+Pro:wght@400;700;900&amp;display=swap">
<link rel="stylesheet" href="/style.css">
</head>
<body>
{HEADER}

<main class="post archives-page">
<header class="page-masthead">
    <h1 class="page-masthead-name">Field Notes</h1>
</header>
<p class="docs-intro">Single-page explainers on things I’m using and learning: how they work, what they measure, where they fall short.</p>
<h2 id="poteto-skills">poteto Skills</h2>
<p class="docs-intro">Agent skills from Lauren Tan (poteto).</p>
<ul class="doc-list">
{poteto_items}
</ul>
<h2 id="matt-pocock-skills">Matt Pocock skills</h2>
<p class="docs-intro">One explainer per skill from <a href="https://github.com/mattpocock/skills">github.com/mattpocock/skills</a>, read at commit 5beb35b, with notes on pairing each with pstack.</p>
<ul class="doc-list">
{mp_items}
</ul>
<h2 id="storytelling-skills">Storytelling Skills</h2>
<p class="docs-intro">Skills for diagrams, illustrations and visual explanation.</p>
<ul class="doc-list">
{story_items}
</ul>
<h2 id="design-skills">Design Skills</h2>
<p class="docs-intro">Skills that build and review frontends. Pick one builder per project.</p>
<ul class="doc-list">
{ds_items}
</ul>
<p class="docs-topics">Topics: {", ".join(E(t) for t in ["poteto Skills","Matt Pocock skills","Storytelling Skills","Design Skills"])} &middot; {len(DOCS)+len(MP)+len(DS)} docs</p>
<p class="docs-companion">Field Notes are what I’ve studied up close. For things spotted in passing that may deserve a second look, see <a href="https://sightings.indrayam.com/">Sightings</a>.</p>
</main>
<p></p>
<footer class="copyright">
    <a href="https://creativecommons.org/licenses/by-nd-nc/1.0/">Copyright</a> &copy; 2026 Anand Sharma. <a href="https://blog.indrayam.com/disclaimer.html">Disclaimer</a>
</footer>
</body>
</html>
'''
open(site+'/index.html','w').write(page)
