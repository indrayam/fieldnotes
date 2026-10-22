import sys,os,re,json
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
R='/home/box/pretty-mermaid-skills'
D=Doc('pretty-mermaid',R,'https://github.com/imxv/Pretty-mermaid-skills/blob/e234ab7/')
S='SKILL.md'; DT='references/DIAGRAM_TYPES.md'; TH='references/THEMES.md'; RM='scripts/render.mjs'
OLD=json.load(open('/workspace/dorothy-docs/_old/pretty-mermaid.json'))
TC=json.loads('''{"zinc-light":{"bg":"#FFFFFF","fg":"#27272A"},"zinc-dark":{"bg":"#18181B","fg":"#FAFAFA"},"tokyo-night":{"bg":"#1a1b26","fg":"#a9b1d6","line":"#3d59a1","accent":"#7aa2f7","muted":"#565f89"},"tokyo-night-storm":{"bg":"#24283b","fg":"#a9b1d6","line":"#3d59a1","accent":"#7aa2f7","muted":"#565f89"},"tokyo-night-light":{"bg":"#d5d6db","fg":"#343b58","line":"#34548a","accent":"#34548a","muted":"#9699a3"},"catppuccin-mocha":{"bg":"#1e1e2e","fg":"#cdd6f4","line":"#585b70","accent":"#cba6f7","muted":"#6c7086"},"catppuccin-latte":{"bg":"#eff1f5","fg":"#4c4f69","line":"#9ca0b0","accent":"#8839ef","muted":"#9ca0b0"},"nord":{"bg":"#2e3440","fg":"#d8dee9","line":"#4c566a","accent":"#88c0d0","muted":"#616e88"},"nord-light":{"bg":"#eceff4","fg":"#2e3440","line":"#aab1c0","accent":"#5e81ac","muted":"#7b88a1"},"dracula":{"bg":"#282a36","fg":"#f8f8f2","line":"#6272a4","accent":"#bd93f9","muted":"#6272a4"},"github-light":{"bg":"#ffffff","fg":"#1f2328","line":"#d1d9e0","accent":"#0969da","muted":"#59636e"},"github-dark":{"bg":"#0d1117","fg":"#e6edf3","line":"#3d444d","accent":"#4493f8","muted":"#9198a1"},"solarized-light":{"bg":"#fdf6e3","fg":"#657b83","line":"#93a1a1","accent":"#268bd2","muted":"#93a1a1"},"solarized-dark":{"bg":"#002b36","fg":"#839496","line":"#586e75","accent":"#268bd2","muted":"#586e75"},"one-dark":{"bg":"#282c34","fg":"#abb2bf","line":"#4b5263","accent":"#c678dd","muted":"#5c6370"}}''')
gi=[];tid={}
for j,o in enumerate(OLD):
    k='theme' if j<15 else 'type'
    gi.append(dict(id=f'g{j}',n=o['n'],il=o['il'],d='Theme preview, source.mmd' if k=='theme' else 'Example diagram, box render',k=k,dark=False)); tid[o['n']]=f'g{j}'
GK=[('theme','Themes'),('type','Diagram types')]
def Q(s,f=S): return D.Q(s,f)
# themes explorer
REC={'tokyo-night':'General dark documentation','github-dark':'GitHub dark or light surfaces','github-light':'GitHub dark or light surfaces','zinc-light':'Print and presentations','dracula':'High-contrast color','nord':'Cool, restrained palette','nord-light':'Cool, restrained palette'}
th=[]
def bgq(n):
    m=re.search(r'^### `%s`.*?^(  bg: .+)$'%re.escape(n),D.rd(TH),re.M|re.S)
    return m.group(1).strip() if m else ''
for n,c in TC.items():
    t=D.rd(TH); lt=re.search(r'^\| `%s` \| ([^|]+) \| ([^|]+) \|'%re.escape(n),t,re.M)
    dark=int(c['bg'][1:3],16)<128
    sw=''.join(f'<span title="{k} {v}" style="display:inline-block;width:34px;height:34px;border-radius:6px;margin-right:6px;background:{v};border:1px solid rgba(127,127,127,.35)"></span>' for k,v in c.items())
    tbl=f'{esc(lt.group(1).strip())} / {esc(lt.group(2).strip())}' if lt else ''
    ex=f'<div class="d-sec"><h4>Colors in code (beautiful-mermaid THEMES)</h4><p>{sw}</p><p><code>{esc(json.dumps(c))}</code></p></div>'
    if lt and lt.group(2).strip() not in (c['fg'],c['fg'].lower()) : ex+=f'<div class="d-sec"><h4>Doc vs code</h4><p>THEMES.md’s quick table lists bg/fg as {tbl}; the code’s fg is {c["fg"]}.</p></div>'
    th.append(dict(id=n,name=n,group='Dark' if dark else 'Light',small='recommended' if n in REC else '',pills=['dark' if dark else 'light',f'{len(c)} colors'],
     tag=esc(f'{"Dark" if dark else "Light"} theme with bg {c["bg"]}.'),
     invoke=f'node scripts/render.mjs --input diagram.mmd --output diagram.svg --theme {n}',how=[f'SKILL.md recommends it for: {esc(REC[n])}.'] if n in REC else [],
     quotes=[[Q(bgq(n),TH),TH]] if bgq(n) else [],extra=ex,lesson='Two required colors derive the rest; extra colors are optional refinements.',files=[TH],src=D.blob+TH,img=tid.get(n,'')))
# types + outputs explorer
TY=[('Flowchart','flowchart LR','Process, decision tree, architecture','Flowchart / Graph','flowchart'),('Sequence','sequenceDiagram','API calls, messages, interactions','Sequence Diagram','sequence'),
 ('State','stateDiagram-v2','Lifecycle or finite-state machine','State Diagram','state'),('Class','classDiagram','Classes, modules, relationships','Class Diagram','class'),
 ('ER','erDiagram','Database entities and cardinality','ER Diagram','er'),('XY chart','xychart-beta','Bars, lines, trends, comparisons','XY Chart','xychart')]
tw=[]
t=D.rd(DT)
for n,st,need,sec_,f in TY:
    m=re.search(r'^## %s\n(.*?)(?=^## )'%re.escape(sec_),t,re.M|re.S).group(1)
    bp=re.search(r'^### Best Practices\n(.*?)(?=^#|\Z)',m,re.M|re.S)
    bl=re.findall(r'^- (.+)$',bp.group(1),re.M) if bp else []
    tw.append(dict(id=f,name=n,group='Diagram types',small=st,pills=['starter: '+st],tag=Q(need),invoke=f'node scripts/render.mjs --input assets/example_diagrams/{f}.mmd --output {f}.svg --theme tokyo-night',
     how=[Q(b,DT) for b in bl[:5]],quotes=[],extra='<div class="d-sec"><h4>What happened when I ran it</h4><p>Rendered as SVG, PNG (1200 px) and Unicode text; all exit 0.</p></div>',
     lesson='Keep a starter file per type; the agent edits a working diagram instead of writing syntax from memory.',files=[DT,f'assets/example_diagrams/{f}.mmd'],src=D.blob+DT,img=tid.get(n,'')))
OU=[('SVG','READMEs, docs, slides, websites','Scalable, themed, supports transparency','--format svg'),('PNG','Chats, previews, raster-only tools','Set `--format png`; no external converter required','--format png --width 1200'),
 ('Unicode','Modern terminals and readable text previews','Default ASCII renderer output','--format ascii'),('Plain ASCII','Logs and restricted terminals','Add `--use-ascii`','--format ascii --use-ascii'),('ANSI-colored text','Interactive terminals','Set `--color-mode`','--format ascii --color-mode truecolor')]
RO={'PNG':'Widths below 100 are rejected: “PNG width must be an integer from 100 to 10000.” PNG is drawn with resvg, no browser.','Unicode':'The flowchart example rendered cleanly, with one stray ├ after the Valid? diamond.'}
for n,b,no,fl in OU:
    tw.append(dict(id='o'+re.sub(r'\W','',n.lower()),name=n,group='Outputs',small='output',pills=[fl.split()[1]],tag=Q(b),invoke=f'node scripts/render.mjs --input diagram.mmd --output out {fl}',how=[Q(no)],quotes=[],
     extra=f'<div class="d-sec"><h4>What happened when I ran it</h4><p>{esc(RO[n])}</p></div>' if n in RO else '',lesson='One CLI, three renderers; the format flag is the only switch.',files=[S,RM],src=D.blob+S,img=''))
# scripts explorer
SC=[('render.mjs','Render one diagram','node scripts/render.mjs --input diagram.mmd --output diagram.svg --theme tokyo-night','Exit 0 on the 6 examples in 3 formats. Unknown theme exits 1 with the list command. A pie chart exits 1: “Invalid mermaid header”. A broken edge (<code>A --&gt;</code>) rendered anyway, exit 0. It overwrote an existing file without asking.','Rendering one diagram'),
 ('batch.mjs','Render a directory in parallel','node scripts/batch.mjs --input-dir ./diagrams --output-dir ./rendered --format svg --theme github-dark --workers 4','6/6 diagrams rendered with 4 workers.','Rendering a directory in parallel'),
 ('themes.mjs','List themes','node scripts/themes.mjs','Printed 15 themes.','Listing installed themes'),
 ('png.mjs','SVG to PNG with resvg','import { renderSvgToPng } from "./png.mjs"','A library, not a CLI: <code>--help</code> prints nothing. It resolves CSS variables to hex so resvg can rasterize them.',None),
 ('smoke-test.mjs','npm test','npm test','“Smoke tests passed: 6 diagrams x 3 formats, 15 themes, CLI named/custom colors and interactive coverage.”',None),
 ('validate-docs.mjs','npm run validate','npm run validate','“Documentation valid: 14 Markdown files, 205 Skill lines, 15 theme previews.”',None),
 ('generate-theme-gallery.mjs','npm run gallery','npm run gallery','Not run: it rewrites assets/theme_gallery in place.',None)]
sc=[]
for n,tg,inv,ran,rt in SC:
    p='scripts/'+n
    sc.append(dict(id=n.split('.')[0],name=n,group='Scripts',small=f'{D.lines(p)} l',pills=[f'{D.lines(p)} lines'],tag=Q(rt) if rt else esc(tg),invoke=inv,how=[],quotes=[],
     extra=f'<div class="d-sec"><h4>What happened when I ran it</h4><p>{ran}</p></div>',lesson='Ship the smoke test with the skill so a change can be checked in one command.',files=[p],src=D.blob+p,img=''))
# sections
hro=hero('Skill explainer · imxv/Pretty-mermaid-skills','Pretty Mermaid',7,
 'Mermaid to <mark>themed SVG, PNG or terminal text</mark>, with no browser in the loop.',
 f'A small Node skill over the beautiful-mermaid renderer: six diagram types, fifteen themes, three output formats and a batch runner. I read the skill, ran its smoke test and doc validator, and rendered every example in every format. {Q("Runs locally without a browser or DOM, with 15 built-in themes and custom colors.")}',
 [('e234ab7','commit, 23 Aug 2026'),('6','diagram types'),('15','themes'),('3','formats'),('7','scripts'),('18/18','example renders')],
 [('Who it is for','Anyone putting diagrams in READMEs, PRs, chats or terminals.'),('What you get','A .mmd source plus an SVG, PNG or text render in the place you asked.')])
s_how=sec('how','How It Works','Write The Source, Render, Then Look At It','A seven-step loop, from SKILL.md.',
 callouts([f'<b>Source first.</b> {Q("Save new source as a `.mmd` file, preserving user terminology and relationships.")}',
  f'<b>Render.</b> {Q("Render with a named theme or explicit colors.")}',f'<b>Inspect.</b> {Q("Inspect the result. Fix syntax, clipping, crowded layout, or unclear labels and render again.")}',
  f'<b>Don’t clobber.</b> {Q("Do not overwrite an existing source or output file unless the user asked for replacement.")}',
  f'<b>Be honest about limits.</b> {Q("Report any renderer limitation instead of silently dropping unsupported syntax.")}']))
s_ty=f'<section id="types">{head("Types And Outputs","Six Types, Five Outputs","Each type’s How it works lists the best practices from DIAGRAM_TYPES.md, checked at build time.")}{explorer("ty","types and outputs")}</section>'
s_th=f'<section id="themes">{head("The Themes","Fifteen Themes, Two Required Colors","Swatches are the colors in the renderer’s code. Where THEMES.md’s quick table disagrees, it says so.")}{explorer("th","themes")}</section>'
s_gal=sec('gallery','Gallery','21 Renders','The repo’s 15 theme previews and the six examples rendered on this box. Click to enlarge.',gchips('gpm',GK)+gal('gpm',gi))
s_sc=f'<section id="scripts">{head("The Scripts","Seven Scripts, All Run","Run on a copy of the repo in /tmp with nice and timeout.")}{explorer("sc","scripts")}</section>'
s_find=sec('findings','What I Found Running It','It Renders Well; The Guard Rails Are In Prose','All runs at commit e234ab7, Node 20.',
 table(['Run','Result','Note'],[['npm test','pass','6 diagrams × 3 formats, 15 themes.'],['npm run validate','pass','14 Markdown files.'],['18 example renders','18/18 exit 0','SVG, PNG and Unicode for each type.'],
  ['batch, 4 workers','6/6',''],['First run without node_modules','crash','ERR_MODULE_NOT_FOUND for @resvg/resvg-js; no auto-install.'],['git status of the original','clean','All runs were on copies.']])+
 verdict([('Bug','The first-run auto-install never runs','render.mjs statically imports png.mjs, which imports @resvg/resvg-js. Without node_modules, Node fails at load time, before <code>loadBeautifulMermaid()</code> can run <code>npm install</code>. SKILL.md says “the CLI also attempts a first-run install”.'),
  ('Gap','No overwrite guard in the CLI','SKILL.md forbids overwriting; render.mjs overwrites silently. The rule depends on the agent.'),
  ('Gap','Bad syntax can render','<code>A --&gt;</code> with no target produced an SVG and exit 0, so “confirm the command exits successfully” is not enough.'),
  ('Gap','THEMES.md is Chinese, and its table is off','The routed theme reference is in Chinese, and its quick table lists the accent as the foreground for several themes (e.g. tokyo-night-light #34548a vs fg #343b58 in code).'),
  ('Copy','No browser','resvg rasterizes the SVG, so PNG works in CI and sandboxes.'),('Copy','A validator for the docs','validate-docs checks the Markdown, the SKILL.md length and that every theme has a preview.')]))
s_steal=sec('yours','Build Your Own','What To Steal','',steal([('Route by need, then by output.','Two small tables pick the type and the format.'),('Make the agent look at the render.','Inspection is a step, not an afterthought.'),
 ('Ship starters.','One working example per type.'),('Keep the loader lazy.','If you promise auto-install, import heavy dependencies after the check.')]))
s_src=sec('sources','Sources','Everything Here Is Checked','Each quote on this page is compared with its source file at build time; the build fails on any mismatch.',
 srcs([D.L(S),D.L(DT),D.L(TH),D.L(RM),'<a href="https://github.com/imxv/Pretty-mermaid-skills">github.com/imxv/Pretty-mermaid-skills</a>']))
nav=[('top','Overview'),('how','How it works'),('types','Types & outputs'),('themes','Themes'),('gallery','Gallery'),('scripts','Scripts'),('findings','Findings'),('yours','Build your own'),('sources','Sources')]
JS=explorer_js('ty','pm-ty',tw,['Diagram types','Outputs'])+explorer_js('th','pm-th',th,['Light','Dark'])+explorer_js('sc','pm-sc',sc,['Scripts'])
D.finish()
n=build('pretty-mermaid','Inside Pretty Mermaid',nav,hro+s_how+s_ty+s_th+s_gal+s_sc+s_find+s_steal+s_src,
 'Compiled 22 Oct 2026 from imxv/Pretty-mermaid-skills @ e234ab7 · every quote is checked against its source file at build time · not affiliated with the author.',JS)
print('built',n,len(tw),len(th),len(sc),len(gi))
