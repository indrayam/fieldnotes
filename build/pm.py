import sys,os,html; sys.path.insert(0,'/workspace/dorothy-docs/_build')
from shell import *; from gal import *
R='/home/box/pretty-mermaid-skills/'
U='<span class="unc">uncertain</span>'
def C(f,l): return f'<code>{f} L{l}</code>'
TH=['zinc-light','zinc-dark','tokyo-night','tokyo-night-storm','tokyo-night-light','catppuccin-mocha','catppuccin-latte','nord','nord-light','dracula','github-light','github-dark','solarized-light','solarized-dark','one-dark']
dark=lambda t: not any(x in t for x in ['light','latte'])
nav=[('top','Overview'),('flow','Pipeline'),('cli','Commands and flags'),('themes','Theme gallery'),('types','Diagram types'),('ascii','Terminal output'),('bugs','Bugs found'),('run','What I ran'),('risks','Side effects'),('sources','Sources')]
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A skill reference · imxv/Pretty-mermaid-skills @ e234ab7 (2026-08-23) · read 20 Oct 2026</div>
<h1>Pretty Mermaid</h1>
<p class="thesis">A thin CLI wrapper around the <mark>beautiful-mermaid</mark> library: Mermaid in, themed SVG / PNG / Unicode out, no browser.</p>
<p class="lede">The skill is a 204-line SKILL.md plus four Node scripts. <code>render.mjs</code> renders one file, <code>batch.mjs</code> a directory, <code>themes.mjs</code> lists themes, <code>png.mjs</code> rasterises SVG with resvg. Layout and drawing are done by the <code>beautiful-mermaid</code> npm package (^1.1.3), not by Mermaid.js, so no headless Chromium is involved. It supports six diagram types, not all of Mermaid.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>15</b><span>built-in themes (<code>node scripts/themes.mjs</code>; <code>THEMES</code> from beautiful-mermaid)</span></div>
<div class="fact" role="listitem"><b>6</b><span>diagram types: flowchart, sequence, state, class, ER, xychart (SKILL.md L33–44)</span></div>
<div class="fact" role="listitem"><b>3</b><span>output formats: svg, png, ascii (Unicode, <code>--use-ascii</code>, ANSI via <code>--color-mode</code>) (L46–54)</span></div>
<div class="fact" role="listitem"><b>2</b><span>runtime deps: beautiful-mermaid ^1.1.3, @resvg/resvg-js ^2.6.2 (<code>package.json</code>)</span></div>
<div class="fact" role="listitem"><b>pass</b><span><code>npm test</code>: "6 diagrams x 3 formats, 15 themes" smoke test; <code>npm run validate</code>: docs valid</span></div>
<div class="fact" role="listitem"><b>1</b><span>verified bug: color flags are silently dropped when <code>--theme</code> is set ({C('render.mjs',204)})</span></div>
</div>
<div class="where">
<div class="note"><h4>Where it lives</h4><p>Clone at <code>/home/box/pretty-mermaid-skills</code>, remote <code>https://github.com/imxv/Pretty-mermaid-skills</code>, 26 commits, 54 tracked files. SKILL.md sits at the repo root. Scripts: render.mjs 243, batch.mjs 286, png.mjs 325, themes.mjs 55; tests: smoke-test 237, validate-docs 86, generate-theme-gallery 44.</p></div>
<div class="note"><h4>References</h4><p><code>references/DIAGRAM_TYPES.md</code> (384), <code>THEMES.md</code> (487, written in Chinese), <code>api_reference.md</code> (54). <code>assets/example_diagrams/</code> has 6 <code>.mmd</code> files; <code>assets/theme_gallery/</code> 15 SVGs + <code>source.mmd</code>. README in EN, CN, JA.</p></div>
<div class="note"><h4>Lineage</h4><p>Renamed from a beautiful-mermaid skill on 2026-01-30 (authors sunmozong, imxv per <code>git log</code>). Latest commit "feat: add native PNG output (#9)" replaced an external converter with resvg.</p></div>
</div></header>'''
fig='''<section id="flow"><div class="sec-head"><div class="eyebrow">Pipeline</div><h2>One file through render.mjs</h2></div>
<div class="figure"><svg viewBox="0 0 1000 220" role="img" aria-labelledby="pT pD"><title id="pT">render.mjs pipeline</title><desc id="pD">Read .mmd, resolve theme or colors, call renderMermaidSVG or renderMermaidASCII, optional resvg to PNG, write file.</desc>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="40" width="170" height="90" rx="8"/><text class="t" x="24" y="66">.mmd input</text><text class="tm" x="24" y="88">--input file or stdin</text><text class="tm" x="24" y="106">auto npm install L33–59</text>
<rect class="bx-skin" x="210" y="40" width="190" height="90" rx="8"/><text class="t" x="224" y="66">theme / colors</text><text class="tm" x="224" y="88">THEMES[--theme] L178</text><text class="tm" x="224" y="106">else --bg/--fg/… L204</text>
<rect class="bx-hot" x="430" y="20" width="200" height="60" rx="8"/><text class="t" x="444" y="46">renderMermaidSVG</text><text class="tm" x="444" y="66">beautiful-mermaid L214</text>
<rect class="bx" x="430" y="100" width="200" height="60" rx="8"/><text class="t" x="444" y="126">renderMermaidASCII</text><text class="tm" x="444" y="146">L189 · Unicode/ASCII/ANSI</text>
<rect class="bx" x="660" y="20" width="160" height="60" rx="8"/><text class="t" x="674" y="46">resvg → PNG</text><text class="tm" x="674" y="66">png.mjs L71 · width 800</text>
<rect class="bx" x="850" y="40" width="140" height="90" rx="8"/><text class="t" x="864" y="66">--output</text><text class="tm" x="864" y="88">.svg .png .txt</text><text class="tm" x="864" y="106">or stdout</text>
<path class="ar" d="M180 85 H208" marker-end="url(#m1)"/><path class="ar" d="M400 75 L428 52" marker-end="url(#m1)"/><path class="ar" d="M400 95 L428 128" marker-end="url(#m1)"/><path class="ar" d="M630 50 H658" marker-end="url(#m1)"/><path class="ar" d="M820 50 L848 70" marker-end="url(#m1)"/><path class="ar-d" d="M630 130 H848" marker-end="url(#m1)"/>
<text class="ts" x="10" y="196">Defaults: font Inter · padding 40 · nodeSpacing 24 · layerSpacing 40 · componentSpacing 24 · PNG width 800</text>
</svg></div></section>'''
cli=f'''<section id="cli"><div class="sec-head"><div class="eyebrow">SKILL.md L56–160</div><h2>Commands and flags</h2></div>
{code("""node scripts/themes.mjs
node scripts/render.mjs -i diagram.mmd -o diagram.svg -t tokyo-night
node scripts/render.mjs -i diagram.mmd -o diagram.png -f png -t github-light --width 1600
node scripts/render.mjs -i diagram.mmd -f ascii [--use-ascii] [--color-mode truecolor]
node scripts/batch.mjs -i diagrams/ -o out/ -f svg -t nord --workers 4""")}
<div class="tablewrap"><table class="dense"><thead><tr><th>Group</th><th>Flags</th><th>Note</th></tr></thead><tbody>
<tr><td>Colors</td><td><code>--bg --fg --line --accent --muted --surface --border</code></td><td>Ignored for SVG/PNG when <code>--theme</code> is set (see Bugs)</td></tr>
<tr><td>Layout (SVG)</td><td><code>--font --padding --node-spacing --layer-spacing --component-spacing --transparent</code></td><td>Passed to renderMermaidSVG</td></tr>
<tr><td>PNG</td><td><code>--width</code></td><td>100–10000, default 800 (png.mjs)</td></tr>
<tr><td>Terminal</td><td><code>--use-ascii --padding-x --padding-y --box-border-padding --color-mode</code></td><td>ASCII colors use only bg/fg/line/accent/border; <code>--muted</code>/<code>--surface</code> dropped</td></tr>
<tr><td>Batch</td><td><code>--input-dir --output-dir --workers</code></td><td>"Workers" = chunk size for <code>Promise.allSettled</code> in one process (batch.mjs L84–87), not threads</td></tr>
</tbody></table></div>
<p class="figcap">Theme picks the skill suggests (L111–119): tokyo-night for dark docs, github-dark/-light for GitHub, zinc-light for print, dracula for high contrast, nord / nord-light for restrained.</p></section>'''
titems=[{'n':t,'tag':'dark' if dark(t) else 'light','k':'dark' if dark(t) else 'light','il':uri(f'/tmp/pm/th-{t}.png',600,74),'d':'','meta':f'render.mjs -f png -t {t} --width 700','cap':f'{t} · assets/theme_gallery/source.mmd'} for t in TH]
themes=f'''<section id="themes"><div class="sec-head"><div class="eyebrow">Rendered on the box with render.mjs</div><h2>Theme gallery: all 15</h2><p>Same input (<code>assets/theme_gallery/source.mmd</code>), one PNG per theme at width 700. The repo also ships these as SVGs in <code>assets/theme_gallery/</code>; these are fresh renders.</p></div>
{chips('tgal',[('light','Light (6)'),('dark','Dark (9)')])}{gallery('tgal',titems)}</section>'''
TY=[('flowchart','Flowchart','flowchart LR: process, decisions, architecture'),('sequence','Sequence','sequenceDiagram: API calls and messages'),('state','State','stateDiagram-v2: lifecycles, FSMs'),('class','Class','classDiagram: classes and relations'),('er','ER','erDiagram: entities and cardinality'),('xychart','XY chart','xychart-beta: bars and lines')]
yitems=[{'n':n,'tag':s,'il':uri(f'/tmp/pm/{s}.png',760,74),'id':uri(f'/tmp/pm/{s}-dark.png',760,74),'d':d,'meta':f'assets/example_diagrams/{s}.mmd · github-light / tokyo-night','cap':f'{s}.mmd'} for s,n,d in TY]
types=f'''<section id="types"><div class="sec-head"><div class="eyebrow">assets/example_diagrams/*.mmd</div><h2>The six diagram types</h2><p>Each repo example rendered twice: <code>github-light</code> and <code>tokyo-night</code>, PNG width 1000. The card follows the page theme; the lightbox has a light/dark toggle. Anything else Mermaid supports (gantt, pie, mindmap, gitGraph…) is not in the skill's table, and I did not test whether beautiful-mermaid rejects it {U}.</p></div>
{gallery('ygal',yitems,'wide')}</section>'''
asc=''.join(f'<div class="card"><h3>{n}</h3><pre class="ascii">{html.escape(open(f"/tmp/pm/{s}.txt").read())}</pre></div>' for s,n,_ in TY[:4])
ascii_=f'''<section id="ascii"><div class="sec-head"><div class="eyebrow">-f ascii</div><h2>Terminal output</h2><p>Unicode box drawing by default; <code>--use-ascii</code> for plain ASCII. Real output for four of the examples. Note the small junction glitch in the flowchart's "Valid?" branch (<code>│ ├─Yes─►</code>).</p></div><div class="twocol">{asc}</div></section>'''
bugs=f'''<section id="bugs"><div class="sec-head"><div class="eyebrow">Verified on the box</div><h2>Bugs found</h2></div>
<div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Theme + colors.</b> SKILL.md L119: "A named theme can be refined with explicit color flags." The code says otherwise: {C('render.mjs',204)} <code>const colors = theme || {{bg, fg, …}}</code>, same in {C('batch.mjs',208)}. With a theme, the flags never reach the renderer. Checked: SVG output with <code>-t tokyo-night</code> and with <code>-t tokyo-night --bg '#ff0000'</code> had the same md5. Fix is a spread: <code>{{...theme, ...custom}}</code>.</p></div>
<div class="callout"><span class="n">2</span><p><b>ASCII palette.</b> <code>customColors</code> for ASCII (L186) ignores <code>--muted</code> and <code>--surface</code>, though the flags parse.</p></div>
<div class="callout"><span class="n">3</span><p><b>"Workers".</b> Not parallel processes, just batches awaited with <code>Promise.allSettled</code> (batch.mjs L84–87). Fine for I/O, no CPU gain.</p></div>
<div class="callout"><span class="n">4</span><p><b>ASCII junctions.</b> Flowchart branch from a diamond draws <code>│ ├─Yes</code> with a stray vertical; cosmetic, from beautiful-mermaid {U}.</p></div>
<div class="callout"><span class="n">5</span><p><b>Line count drift.</b> <code>validate-docs</code> reports 205 SKILL lines; <code>wc -l</code> gives 204 (trailing-newline counting). Harmless.</p></div>
</div></section>'''
run=f'''<section id="run"><div class="sec-head"><div class="eyebrow">Run 20 Oct 2026 · node v20.19.2</div><h2>What I ran</h2></div>
{code("""cd /home/box/pretty-mermaid-skills
timeout 120 nice node scripts/themes.mjs                 # 15 themes
timeout 600 nice npm test     # Smoke tests passed: 6 diagrams x 3 formats, 15 themes…
timeout 120 nice npm run validate  # Documentation valid: 14 Markdown files, 205 Skill lines, 15 theme previews.
for t in $(themes); do timeout 120 nice node scripts/render.mjs -i assets/theme_gallery/source.mmd -o /tmp/pm/th-$t.png -f png -t $t --width 700; done
for d in assets/example_diagrams/*.mmd; do …  -t github-light / -t tokyo-night --width 1000; … -f ascii; done
# bug check
node scripts/render.mjs -i x.mmd -o a.svg -t tokyo-night; node scripts/render.mjs -i x.mmd -o b.svg -t tokyo-night --bg '#ff0000'; md5sum a.svg b.svg   # identical""")}</section>'''
risks=f'''<section id="risks"><div class="sec-head"><div class="eyebrow">Side effects</div><h2>Side effects</h2></div>
<div class="callouts"><div class="callout"><span class="n">1</span><p><b>Auto <code>npm install</code>.</b> If beautiful-mermaid is missing, render.mjs runs <code>npm install</code> in the skill dir via <code>execSync</code> (L33–59): network plus writes to <code>node_modules</code>, without asking. node_modules was already present here.</p></div>
<div class="callout"><span class="n">2</span><p><b>Overwrites.</b> The script writes <code>--output</code> unconditionally; the "do not overwrite" rule (SKILL L31) is on the agent, not enforced.</p></div>
<div class="callout"><span class="n">3</span><p><b>Fonts.</b> SVG asks for Inter by name; if the viewer lacks it, the fallback font changes text widths {U}.</p></div></div></section>'''
srcs='''<section id="sources"><div class="sec-head"><div class="eyebrow">Sources</div><h2>Sources</h2></div><div class="srcs"><ul>
<li><code>SKILL.md</code> (204) · <code>scripts/render.mjs</code> (243) · <code>batch.mjs</code> (286) · <code>png.mjs</code> (325) · <code>themes.mjs</code> (55)</li>
<li><code>references/DIAGRAM_TYPES.md</code> (384) · <code>THEMES.md</code> (487) · <code>api_reference.md</code> (54) · <code>docs/THEME_GALLERY.md</code> · <code>package.json</code></li>
<li><code>git log</code>: 26 commits, head e234ab7 2026-08-23</li><li>Renders: <code>/tmp/pm/</code> on the box</li></ul></div></section>'''
foot='Built 20 Oct 2026 from <code>/home/box/pretty-mermaid-skills</code> @ e234ab7. All diagrams rendered locally with the skill\'s own scripts and embedded as WebP.'
h=page('Inside Pretty Mermaid','Inside Pretty Mermaid',nav,GCSS+hero+fig+cli+themes+types+ascii_+bugs+run+risks+srcs+LB,footer=foot,extra_js=GJS)
open('/workspace/dorothy-docs/pretty-mermaid/index.html','w').write(h);print(len(h))
