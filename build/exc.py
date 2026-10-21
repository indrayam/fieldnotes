import sys,os,html; sys.path.insert(0,'/workspace/dorothy-docs/_build')
from shell import *; from gal import *
E='/tmp/ex/'
U='<span class="unc">uncertain</span>'
def C(l): return f'<code>SKILL.md L{l}</code>'
nav=[('top','Overview'),('flow','Architecture'),('skill','The skill'),('server','The MCP server'),('look','The default look'),('gallery','Renders'),('findings','Findings'),('run','What I ran'),('risks','Side effects'),('sources','Sources')]
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A skill + MCP server reference · yctimlin/mcp_excalidraw @ 8084a1c (2026-10-09) · mcp-excalidraw-server 2.1.2 · read 20 Oct 2026</div>
<h1>Excalidraw</h1>
<p class="thesis">A <mark>local Excalidraw canvas server</mark> that agents drive element by element (CLI, MCP or REST), plus a 277-line skill that teaches the draw → screenshot → fix loop.</p>
<p class="lede">Two parts in one npm package. The server (<code>mcp-excalidraw-server</code>) runs the Excalidraw web UI, a REST API and WebSocket sync on <code>127.0.0.1:3000</code>, and since v2.1 renders PNG/SVG headless under Node with Excalidraw's own <code>exportToSvg</code> and resvg. The skill (<code>skills/excalidraw-skill/SKILL.md</code>) picks an interface, sets spacing and colour rules, lists layout anti-patterns, and requires a screenshot check after every batch. The look is Excalidraw's: hand-drawn strokes, hachure fills, Excalifont. <b>Anand finds that default too raw, which is why Disha rarely uses this skill.</b> The skill's own "professional look" advice (L68–71) only partly fixes it; see <a href="#look">The default look</a>.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>26</b><span>MCP tools (<code>src/core/mcp-tools.ts</code>, counted <code>name:</code> entries; README L483)</span></div>
<div class="fact" role="listitem"><b>3</b><span>interfaces on one canvas: MCP tools, CLI, REST ({C('8–20')})</span></div>
<div class="fact" role="listitem"><b>20</b><span>CLI commands (<code>--help</code>), JSON on stdout, exit codes 0–4 ({C('24')})</span></div>
<div class="fact" role="listitem"><b>277</b><span>lines in SKILL.md; <code>references/cheatsheet.md</code> 193; 5 evals</span></div>
<div class="fact" role="listitem"><b>2</b><span>things still need a browser tab: Mermaid conversion and viewport ({C('20')})</span></div>
<div class="fact" role="listitem"><b>116</b><span>commits; first 2025-03-16; many outside contributors in Oct 2026 (<code>git log</code>)</span></div>
</div>
<div class="where">
<div class="note"><h4>Where it lives</h4><p>Clone <code>/home/box/mcp_excalidraw</code>, remote <code>https://github.com/yctimlin/mcp_excalidraw</code>, 443 tracked files, built <code>dist/</code> present. Canonical skill in <code>skills/</code>, synced to <code>.agents/skills/</code> (and a <code>.claude/skills</code> symlink) by <code>scripts/sync-skills.mjs</code>; <code>install-skill --dir</code> copies it anywhere.</p></div>
<div class="note"><h4>Not the official one</h4><p>Excalidraw has an official MCP (a chat widget, two tools, one-shot). This project is a persistent workbench with element CRUD, layout tools, snapshots and file I/O; README L61–81 has the comparison table.</p></div>
<div class="note"><h4>Why Disha skips it</h4><p>Output reads as a whiteboard sketch. Fine for brainstorming, out of place next to the diagram-design or draw.io output Anand prefers. The skill can't change Excalidraw's renderer; it can only set <code>fillStyle</code>, colours, <code>roughness</code> and fonts per element.</p></div>
</div></header>'''
fig='''<section id="flow"><div class="sec-head"><div class="eyebrow">README L50–59, L244–254</div><h2>Architecture</h2></div>
<div class="figure"><svg viewBox="0 0 1000 270" role="img" aria-labelledby="xT xD"><title id="xT">mcp_excalidraw architecture</title><desc id="xD">CLI, MCP stdio server and REST clients drive one canvas server, which holds state, syncs to browser tabs, renders headless, and optionally persists and shares.</desc>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="20" width="200" height="60" rx="8"/><text class="t" x="24" y="46">CLI</text><text class="tm" x="24" y="66">npx mcp-excalidraw-server …</text>
<rect class="bx" x="10" y="100" width="200" height="60" rx="8"/><text class="t" x="24" y="126">MCP stdio server</text><text class="tm" x="24" y="146">26 tools · src/core/mcp-*.ts</text>
<rect class="bx" x="10" y="180" width="200" height="60" rx="8"/><text class="t" x="24" y="206">REST client</text><text class="tm" x="24" y="226">stricter label/start/end</text>
<rect class="bx-hot" x="290" y="40" width="300" height="180" rx="10"/><text class="t" x="306" y="68">Canvas server  127.0.0.1:3000</text><text class="tm" x="306" y="92">src/server.ts (1626) · auto-started</text><text class="tm" x="306" y="114">in-memory scene; snapshots</text><text class="tm" x="306" y="136">normalize + bound-arrow routing</text><text class="tm" x="306" y="158">headless render: exportToSvg</text><text class="tm" x="306" y="176">under jsdom → resvg PNG</text><text class="tm" x="306" y="198">WebSocket sync to tabs</text>
<rect class="bx" x="660" y="20" width="330" height="60" rx="8"/><text class="t" x="674" y="46">Browser tab (optional)</text><text class="tm" x="674" y="66">watch; needed for mermaid + viewport</text>
<rect class="bx" x="660" y="100" width="330" height="60" rx="8"/><text class="t" x="674" y="126">EXCALIDRAW_DATA_DIR (opt-in)</text><text class="tm" x="674" y="146">atomic checkpoints, blobs, lock</text>
<rect class="bx-skin" x="660" y="180" width="330" height="60" rx="8"/><text class="t" x="674" y="206">share → json.excalidraw.com</text><text class="tm" x="674" y="226">AES-GCM, key in URL fragment</text>
<path class="ar" d="M210 50 L288 90" marker-end="url(#m1)"/><path class="ar" d="M210 130 H288" marker-end="url(#m1)"/><path class="ar" d="M210 210 L288 170" marker-end="url(#m1)"/>
<path class="ar" d="M590 80 L658 52" marker-end="url(#m1)"/><path class="ar-d" d="M590 130 H658" marker-end="url(#m1)"/><path class="ar-d" d="M590 180 L658 208" marker-end="url(#m1)"/>
<text class="ts" x="10" y="262">Offline: render file.excalidraw --out file.png needs no server (src/cli/commands/render.ts).</text>
</svg></div></section>'''
skill=f'''<section id="skill"><div class="sec-head"><div class="eyebrow">skills/excalidraw-skill/SKILL.md</div><h2>The skill</h2></div>
<div class="tablewrap"><table class="dense fx"><colgroup><col style="width:22%"><col><col style="width:12%"></colgroup><thead><tr><th>Section</th><th>What it says</th><th>Lines</th></tr></thead><tbody>
<tr><td>Pick an interface</td><td>MCP tools if present; else CLI via <code>npx -y</code> (auto-starts the server; first run downloads the package); REST last</td><td>8–20</td></tr>
<tr><td>Element format</td><td>Agent shorthand: <code>"text"</code> on shapes, <code>startElementId</code>/<code>endElementId</code> on arrows, font names, both point forms. REST needs <code>label.text</code> and <code>start.id</code></td><td>43–53</td></tr>
<tr><td>Coordinates and spacing</td><td>Tiers 80–120 px apart, siblings 40–60, width <code>max(160, chars×12)</code>, height 60/80, zone padding 50</td><td>57–66</td></tr>
<tr><td>"Professional look"</td><td><code>fillStyle: solid</code>, pastel fill + darker stroke, dashed zones</td><td>68–71</td></tr>
<tr><td>Anti-patterns</td><td>No label on zone rectangles (it centres over the children), no cross-zone arrows, few arrow labels ≤12 chars</td><td>75–110</td></tr>
<tr><td>Quality checklist</td><td>After every batch: screenshot, check truncation, overlap, arrow crossings, label overlap, 40 px gaps, font ≥16/20, zone labels; "stop, fix it, re-screenshot"</td><td>114–130</td></tr>
<tr><td>Workflows</td><td>New diagram, arrow routing (curved / elbowed), describe + screenshot loop, refine, Mermaid, file I/O, Obsidian <code>.excalidraw.md</code>, snapshots, duplication</td><td>134–261</td></tr>
<tr><td>Error recovery</td><td>Exit 3/4, off-screen elements, locked elements, duplicate bound texts from the tab's auto-sync</td><td>263–271</td></tr>
</tbody></table></div></section>'''
server=f'''<section id="server"><div class="sec-head"><div class="eyebrow">src/ · README</div><h2>The MCP server</h2><p>26 tools in <code>src/core/mcp-tools.ts</code>, dispatched in <code>mcp-dispatch.ts</code> (745 lines) to the canvas over HTTP (<code>canvas-client.ts</code>).</p></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Group</th><th>Tools</th></tr></thead><tbody>
<tr><td>Elements</td><td><code>create_element update_element delete_element get_element query_elements batch_create_elements duplicate_elements</code></td></tr>
<tr><td>Layout</td><td><code>align_elements distribute_elements group_elements ungroup_elements lock_elements unlock_elements</code></td></tr>
<tr><td>See it</td><td><code>describe_scene get_canvas_screenshot export_to_image set_viewport</code></td></tr>
<tr><td>Scene</td><td><code>clear_canvas export_scene import_scene snapshot_scene restore_snapshot get_resource</code></td></tr>
<tr><td>Other</td><td><code>create_from_mermaid read_diagram_guide export_to_excalidraw_url</code></td></tr>
</tbody></table></div>
<p class="figcap">Env (README L260–275): <code>EXPRESS_SERVER_URL</code>, <code>ENABLE_CANVAS_SYNC</code>, <code>EXCALIDRAW_NO_AUTOSTART</code>, <code>EXCALIDRAW_EXPORT_DIR</code> (write sandbox, default cwd), <code>EXCALIDRAW_RENDER_MAX_DIM</code> 8192, <code>EXCALIDRAW_DATA_DIR</code>, <code>PORT/HOST</code>, logging. Headless fonts: Excalifont, Virgil, Cascadia Code, Liberation Sans bundled in <code>assets/fonts</code> (OFL).</p></section>'''
def I(f,n,d,dark=None,mw=900,tag='',bg=None): 
    o={'n':n,'il':uri(E+f,mw,76),'d':d,'meta':'/tmp/ex/'+f,'cap':n,'tag':tag}
    if dark: o['id']=uri(E+dark,mw,76)
    return o
look=f'''<section id="look"><div class="sec-head"><div class="eyebrow">Why "too raw"</div><h2>The default look</h2><p>Same four-box CI/CD diagram (eval 0 in <code>evals/evals.json</code>), drawn on the live canvas and screenshotted headless. Top: the shapes as an agent would send them with no styling. Bottom: the skill's own polish advice applied (solid pastel fills, darker strokes, <code>roughness: 0</code>, rounded corners, a title).</p></div>
{gallery('lookgal',[I('c-p-raw.png','Default','Hand-drawn outlines, Excalifont, no fill.',tag='raw'),I('c-p-pol.png','With the skill\'s styling','Cleaner, but the lettering is still Excalifont and the arrows still sketch.',tag='styled')],'wide')}
<div class="note" style="margin-top:16px"><h4>What can and can't change</h4><p>Per element you can set <code>fillStyle</code>, colours, <code>strokeStyle</code>, <code>roughness</code> (0 = straight lines) and <code>fontFamily</code> (helvetica/cascadia/excalifont…, {C('49')}). You can't change the renderer, so it will never look like a typeset diagram. The skill only suggests <code>fillStyle: solid</code> (L68–71). It never mentions <code>roughness</code> or a non-hand font, so a by-the-book run still comes out sketchy. That fits Anand's "too raw".</p></div></section>'''
gitems=[I('c-raw.png','Skill example, default','The 4-node load-balancer example from SKILL.md L148–159, as given.',tag='default'),
I('c-hachure.png','Fill, default hachure','Same with a blue fill and no fillStyle: the sketchy hachure pattern.',tag='default'),
I('c-styled.png','Styled, light / dark','Solid pastels, roughness 0, helvetica requested; screenshot --dark for the pair.',dark='c-styled-dark.png',tag='styled'),
I('rt.png','Export → offline render','The styled scene exported to .excalidraw and rendered with <code>render</code> (no server). Labels come out in Helvetica here.',tag='offline'),
I('c-z-wrong.png','Anti-pattern 1: label on the zone','"VPC" label bound to the zone rectangle lands in the middle, under the arrow (L79–86).',tag='anti-pattern'),
I('c-z-right.png','Anti-pattern 1, fixed','Free-standing text at the top of the zone (L88–94).',dark='c-z-right-dark.png',tag='fixed'),
I('raw.png','Offline render of shorthand JSON','<code>render</code> on REST-shaped JSON (label/start/end) without the server: labels appear, arrows are not routed and sit at 0,0.',tag='finding'),
I('demo-mid.png','Repo demo.gif (frame 160 of 320)','The README demo: agent drawing on the live canvas.',tag='repo'),
I('demo-last.png','Repo demo.gif (last frame)','Finished demo diagram.',tag='repo')]
gal_=f'''<section id="gallery"><div class="sec-head"><div class="eyebrow">Rendered on the box, 20 Oct 2026 · port 3917, stopped after</div><h2>Renders</h2><p>All but the two demo frames are mine, made with the package's own CLI against a temporary canvas server, at <code>--scale 2</code>.</p></div>{gallery('xgal',gitems,'wide')}</section>'''
findings=f'''<section id="findings"><div class="sec-head"><div class="eyebrow">Observed while running it</div><h2>Findings</h2></div><div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Offline <code>render</code> isn't the canvas.</b> The SKILL's own example JSON (L148–159, arrows without <code>id</code>) fails offline with "Scene contains an invalid or duplicate element ID". With ids added, CLI shorthand (<code>text</code>, <code>startElementId</code>) renders bare boxes with no labels. REST shorthand gets labels but arrows stay unrouted at 0,0. The <code>render.ts</code> comment says "agent-format … accepted", which held only for labels. Bound-arrow routing happens in the server's <code>add</code> path. <code>render</code> is safe for exported <code>.excalidraw</code> files, which is what L237 actually says.</p></div>
<div class="callout"><span class="n">2</span><p><b>Screenshot and export disagree on label font.</b> With <code>fontFamily: "helvetica"</code> on shapes, the live <code>screenshot</code> drew labels in Excalifont. The exported scene has <code>fontFamily: 2</code> on the bound texts, and <code>render</code> of that export shows Helvetica. Cause not traced {U}.</p></div>
<div class="callout"><span class="n">3</span><p><b>Mermaid needs a tab.</b> <code>mermaid</code> exited 4 ("requires the canvas to be open in a browser"), as documented; eval 1 can't pass headless.</p></div>
<div class="callout"><span class="n">4</span><p><b>Tests pass.</b> <code>scripts/check-render.mjs</code>: "All headless renderer checks passed" (incl. warm render &lt; 500 ms). <code>scripts/check-mcp-stdio.mjs</code>: 5/5 wire checks. I ran these against the existing <code>dist/</code>, skipping <code>npm run build:server</code>, which would rewrite it.</p></div></div></section>'''
run=f'''<section id="run"><div class="sec-head"><div class="eyebrow">Run 20 Oct 2026</div><h2>What I ran</h2></div>
{code("""export EXPRESS_SERVER_URL=http://127.0.0.1:3917 EXCALIDRAW_DATA_DIR=/tmp/ex/data XDG_STATE_HOME=/tmp/ex/state
B="timeout 120 nice node /home/box/mcp_excalidraw/dist/bin.js"
$B start                        # spawned pid, detached
$B add raw-id.json; $B screenshot --out c-raw.png --scale 2; $B describe
$B clear --yes; $B add styled-id.json; $B screenshot --out c-styled.png --scale 2 [--dark]
$B export --out c-styled.excalidraw          # 12 elements (4 bound labels added)
echo 'graph TD\\nA-->B' | $B mermaid            # exit 4: needs a browser tab
$B stop                         # "Canvas server (pid …) stopped."   status → running:false
$B render c-styled.excalidraw --out rt.png --scale 2      # offline, no server
timeout 300 nice node scripts/check-render.mjs           # all passed
timeout 120 nice node scripts/check-mcp-stdio.mjs        # 5 wire checks passed""","Non-default port and state dirs so nothing touched a default install. Both server runs were stopped with the CLI's own <code>stop</code>, which works by pidfile.")}</section>'''
risks=f'''<section id="risks"><div class="sec-head"><div class="eyebrow">Side effects</div><h2>Side effects</h2></div><div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Auto-started server.</b> Any canvas-touching CLI command, and the MCP server on launch, spawns a detached canvas server on :3000 that keeps running after the agent finishes. Opt out with <code>EXCALIDRAW_NO_AUTOSTART=1</code>; stop with <code>stop</code>.</p></div>
<div class="callout"><span class="n">2</span><p><b><code>npx -y</code></b> downloads and runs the latest npm release on first use, unpinned ({C('15–17')}).</p></div>
<div class="callout"><span class="n">3</span><p><b>Network.</b> The canvas page loads fonts from esm.sh; <code>share</code> / <code>export_to_excalidraw_url</code> uploads the encrypted scene to <code>json.excalidraw.com</code> (<code>share-url.ts</code> L81). Anyone with the link can read it.</p></div>
<div class="callout"><span class="n">4</span><p><b>Durable state</b> (opt-in) writes diagrams and image blobs to <code>EXCALIDRAW_DATA_DIR</code>; README asks you to keep it out of repos.</p></div></div></section>'''
srcs='''<section id="sources"><div class="sec-head"><div class="eyebrow">Sources</div><h2>Sources</h2></div><div class="srcs"><ul>
<li><code>skills/excalidraw-skill/SKILL.md</code> (277) · <code>references/cheatsheet.md</code> (193) · <code>evals/evals.json</code></li>
<li><code>README.md</code> (680) · <code>package.json</code> (v2.1.2) · <code>src/core/mcp-tools.ts</code> · <code>src/cli/commands/render.ts</code>, <code>server.ts</code> · <code>src/core/config.ts</code>, <code>normalize.ts</code>, <code>share-url.ts</code>, <code>render/index.ts</code></li>
<li><code>scripts/check-render.mjs</code>, <code>check-mcp-stdio.mjs</code>, <code>sync-skills.mjs</code> · <code>demo.gif</code></li>
<li><code>git log</code>: 116 commits, 860e905 2025-03-16 → 8084a1c 2026-10-09</li><li>Renders: <code>/tmp/ex/</code></li></ul></div></section>'''
foot='Built 20 Oct 2026 from <code>/home/box/mcp_excalidraw</code> @ 8084a1c. Renders made with the package\'s own CLI and embedded as WebP; demo frames from the repo\'s demo.gif.'
h=page('Inside Excalidraw','Inside Excalidraw',nav,GCSS+hero+fig+skill+server+look+gal_+findings+run+risks+srcs+LB,footer=foot,extra_js=GJS)
open('/workspace/dorothy-docs/excalidraw/index.html','w').write(h);print(len(h))
