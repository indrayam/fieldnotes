"""Build cribsheets.indrayam.com home: 4th sibling of indrayam.com / dailydiff / resume.
Shares the blog's style.css (shipped verbatim as /style.css) and copyright; header.html holds the site nav."""
import sys,html,shutil,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from config import src, SITE, ASSETS, BUILD
site=sys.argv[1] if len(sys.argv)>1 else SITE
BLOG=src('INDRAYAM_BLOG_SRC')
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
shutil.copy(BLOG+'/style.css',site+'/style.css')
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
ds_items="\n".join(li(*d) for d in DS)
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
<title>Cribsheets · Anand Sharma</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://cribsheets.indrayam.com/">
<meta property="og:type" content="website"><meta property="og:title" content="Cribsheets · Anand Sharma">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="https://cribsheets.indrayam.com/">
<meta property="og:site_name" content="Cribsheets · Anand Sharma">
<meta name="theme-color" content="#e7651a">
<link rel="Shortcut Icon" href="/images/favicon.ico">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300&display=swap">
<link rel="stylesheet" href="/style.css">
<style>
/* cribsheets.indrayam.com: only additions; tokens come from shared style.css */
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
/* Home-style chrome, matching The Daily Diff: white page, no box, centered site links, masthead heading. */
body {{ background-image: none !important; background-color: #ffffff; }}
.site-header {{ max-width: 760px; margin: 18px auto 14px; }}
.site-nav ul {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 4px 22px; margin: 0; padding: 0; list-style: none; }}
.site-nav li {{ margin: 0; padding: 0; background: none; }}
.site-nav a {{ display: inline-block; padding: 4px 0; color: #111111; font-family: Fraunces, Georgia, "Times New Roman", serif; font-size: 1.05rem; font-weight: 300; line-height: 1.6; text-decoration: underline; text-decoration-color: transparent; text-decoration-thickness: 3px; text-underline-offset: 7px; transition: text-decoration-color 0.15s ease; }}
.site-nav a:hover, .site-nav a:focus-visible, .site-nav a[aria-current="page"] {{ text-decoration-color: #e7651a; }}
.site-nav a:focus-visible {{ outline: none; }}
.post {{ border: none !important; margin-top: 0 !important; }}
.page-masthead {{ text-align: center; padding-bottom: 0.45rem; }}
.page-masthead-name {{ font-family: "Source Sans Pro", Arial, sans-serif; font-weight: 900; font-size: clamp(2.5rem, 5vw, 3.85rem); letter-spacing: 0; line-height: 1.02; color: #333333; margin: 0; padding: 0; border: 0; }}
.page-masthead-tagline {{ font-family: Newsreader, Georgia, "Times New Roman", serif; font-size: 0.92rem; letter-spacing: 0.02em; line-height: 1.6; color: #555555; margin: 0.15rem 0 0; }}
.page-masthead-rule {{ height: 0; border: none; border-top: 4px double #808080; margin: 1.1rem 0 0.32rem; }}
@media screen and (max-width: 899px) {{ .site-header {{ max-width: none; margin-left: 10px; margin-right: 10px; }} }}
.docs-topics{{font-family:var(--font-ui);font-size:.85rem;color:var(--color-muted);margin-top:14px;border-top:1px dashed var(--color-border-light);padding-top:8px}}
</style>
</head>
<body>
{HEADER}

<main class="post archives-page">
<header class="page-masthead">
    <h1 class="page-masthead-name">Cribsheets</h1>
    <p class="page-masthead-tagline">Explainers on what I’m using and learning</p>
    <hr class="page-masthead-rule">
</header>
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
<h2 id="design-skills" style="margin-top:28px">Design Skills</h2>
<p class="docs-intro">Skills that build and review frontends. Pick one builder per project.</p>
<ul class="doc-list">
{ds_items}
</ul>
<p class="docs-topics">Topics: {", ".join(E(t) for t in ["poteto Skills","Matt Pocock skills","Storytelling Skills","Design Skills"])} &middot; {len(DOCS)+len(MP)+len(DS)} docs</p>
</main>
<p></p>
<div class="copyright">
    <a href="http://creativecommons.org/licenses/by-nd-nc/1.0/">Copyright</a> &copy; 2026 Anand Sharma. <a href="https://blog.indrayam.com/disclaimer.html">Disclaimer</a>
</div>
</body>
</html>
'''
open(site+'/index.html','w').write(page)
