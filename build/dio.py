import sys,os,html,re; sys.path.insert(0,'/workspace/dorothy-docs/_build')
from shell import *; from gal import *
R='/home/box/drawio-skill/'; G=R+'docs/images/gallery/'
U='<span class="unc">uncertain</span>'
def C(l): return f'<code>SKILL.md L{l}</code>'
nav=[('top','Overview'),('flow','Pipeline'),('copies','Four plugin copies'),('layout','ELK layout and repair'),('mine','My renders'),('gallery','Repo gallery'),('output','Output modes'),('findings','Findings'),('run','What I ran'),('risks','Side effects'),('sources','Sources')]
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A skill reference · jgraph/drawio-mcp @ 27126ad (2026-10-18) · plugins/cursor/skills/drawio · read 20 Oct 2026</div>
<h1>Draw.io</h1>
<p class="thesis">An agent writes <mark>Mermaid or mxGraph XML</mark>; the draw.io desktop CLI turns it into an editable <code>.drawio</code> and a PNG/SVG/PDF that still carries the diagram.</p>
<p class="lede">The skill is one 474-line SKILL.md, copied byte-for-byte into four agent plugins (Claude Code, Codex, Copilot, Cursor). It lives inside jgraph's <code>drawio-mcp</code> monorepo, which also holds the hosted MCP app server (<code>https://mcp.draw.io/mcp</code>), an npm tool server (<code>@drawio/mcp</code>), shared XML/Mermaid references, and the gallery shown below. Mermaid is preferred when the desktop CLI is installed; XML is for anything Mermaid can't express or when exact layout matters.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>4</b><span>identical SKILL.md copies (md5 54ecbaea…); CI <code>check-skill-sync.yml</code> <code>cmp</code>s each against the Claude copy</span></div>
<div class="fact" role="listitem"><b>474</b><span>lines in SKILL.md</span></div>
<div class="fact" role="listitem"><b>6</b><span>ELK <code>--layout</code> presets + custom JSON + <code>libavoid</code> routing ({C('51–101')})</span></div>
<div class="fact" role="listitem"><b>44</b><span>gallery images in <code>docs/images/gallery/</code> (repo)</span></div>
<div class="fact" role="listitem"><b>16</b><span>renders I made with draw.io Desktop 32.5.5 via the skill's own commands</span></div>
<div class="fact" role="listitem"><b>349</b><span>commits in drawio-mcp (<code>git log</code>)</span></div>
</div>
<div class="where">
<div class="note"><h4>Where it lives</h4><p>Clone <code>/home/box/drawio-skill</code>, remote <code>https://github.com/jgraph/drawio-mcp</code>. Cursor copy: <code>plugins/cursor/skills/drawio/SKILL.md</code>. Siblings: <code>plugins/claude-code/skills/drawio/</code>, <code>plugins/codex/drawio/skills/drawio/</code>, <code>plugins/copilot/skills/drawio/</code>.</p></div>
<div class="note"><h4>The MCP exception</h4><p>The description (L3, L10) says: in VS Code/Cursor chat, Claude.ai and ChatGPT, use the MCP <code>create_diagram</code> tool to show the diagram inline instead of files. The root README lists the app-server tools: <code>create_diagram</code> (28 Mermaid types), <code>search_shapes</code> (10,000+ shapes), <code>get_drawio_reference</code>.</p></div>
<div class="note"><h4>Needs</h4><p>draw.io Desktop for anything beyond URL mode. Not installed on the box, so I unpacked the v32.5.5 .deb into <code>/home/box/opt/drawio</code> (user dir, no system install) and ran it under <code>xvfb-run</code>.</p></div>
</div></header>'''
fig=f'''<section id="flow"><div class="sec-head"><div class="eyebrow">SKILL.md L12–49</div><h2>Pipeline</h2></div>
<div class="figure"><svg viewBox="0 0 1000 260" role="img" aria-labelledby="dT dD"><title id="dT">draw.io skill pipeline</title><desc id="dD">Mermaid or XML source; Mermaid converts to drawio via CLI; XML gets a repair pass and optional ELK layout; then export with embedded diagram, or a browser URL.</desc>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="30" width="170" height="70" rx="8"/><text class="t" x="24" y="56">d.mmd</text><text class="tm" x="24" y="78">preferred if CLI present</text>
<rect class="bx" x="10" y="150" width="170" height="70" rx="8"/><text class="t" x="24" y="176">d.drawio (XML)</text><text class="tm" x="24" y="198">exact layout, any shape</text>
<rect class="bx-skin" x="230" y="30" width="200" height="70" rx="8"/><text class="t" x="244" y="56">drawio -x -f xml</text><text class="tm" x="244" y="78">Mermaid → native shapes</text>
<rect class="bx-skin" x="230" y="150" width="200" height="70" rx="8"/><text class="t" x="244" y="176">repair pass + --layout</text><text class="tm" x="244" y="198">L426–444 · ELK L51–101</text>
<rect class="bx-hot" x="490" y="90" width="230" height="80" rx="8"/><text class="t" x="504" y="118">drawio -x -f png -e -b 10</text><text class="tm" x="504" y="140">-e embeds the XML (zTXt)</text><text class="tm" x="504" y="158">png · svg · pdf · jpg</text>
<rect class="bx" x="780" y="30" width="210" height="70" rx="8"/><text class="t" x="794" y="56">d.drawio.png</text><text class="tm" x="794" y="78">opens back in draw.io</text>
<rect class="bx" x="780" y="150" width="210" height="70" rx="8"/><text class="t" x="794" y="176">URL mode, no CLI</text><text class="tm" x="794" y="198">deflate+b64 → #R… L147</text>
<path class="ar" d="M180 65 H228" marker-end="url(#m1)"/><path class="ar" d="M180 185 H228" marker-end="url(#m1)"/><path class="ar" d="M430 65 L488 112" marker-end="url(#m1)"/><path class="ar" d="M430 185 L488 150" marker-end="url(#m1)"/><path class="ar" d="M720 118 L778 72" marker-end="url(#m1)"/><path class="ar-d" d="M720 150 L778 180" marker-end="url(#m1)"/>
</svg></div>
{code("""drawio -x -f xml -o d.drawio d.mmd                  # Mermaid → editable .drawio
drawio -x -f png -e -b 10 -o d.drawio.png d.drawio   # export, diagram embedded
drawio -x -f xml --layout verticalFlow -o out.drawio in.drawio   # ELK pass on XML""","SKILL.md L27–49, L323–362. Filenames keep the double extension (<code>.drawio.png</code>) so the file reopens as a diagram (L391–398).")}</section>'''
copies=f'''<section id="copies"><div class="sec-head"><div class="eyebrow">plugins/ · root marketplace manifests</div><h2>Four plugin copies: same skill, different wrappers</h2><p>The SKILL.md body is identical in all four; only packaging differs.</p></div>
<div class="tablewrap"><table class="dense fx"><colgroup><col style="width:14%"><col style="width:30%"><col style="width:20%"><col></colgroup><thead><tr><th>Agent</th><th>Path</th><th>Bundles MCP?</th><th>Packaging notes</th></tr></thead><tbody>
<tr><td>Claude Code</td><td><code>plugins/claude-code/skills/drawio/</code></td><td>Yes: <code>.mcp.json</code>, http <code>https://mcp.draw.io/mcp</code> (since 1.2.3)</td><td><code>.claude-plugin/plugin.json</code> v1.2.3; canonical copy for CI; README L116 privacy note</td></tr>
<tr><td>Codex</td><td><code>plugins/codex/drawio/skills/drawio/</code></td><td>No</td><td><code>.codex-plugin/plugin.json</code> with <code>interface.defaultPrompt</code>; extra <code>drawio/</code> level because Codex normalises the plugin root name</td></tr>
<tr><td>Copilot</td><td><code>plugins/copilot/skills/drawio/</code></td><td>No</td><td><code>plugin.json</code> with a <code>skills</code> array</td></tr>
<tr><td>Cursor</td><td><code>plugins/cursor/skills/drawio/</code></td><td>Yes: <code>mcp.json</code> → hosted app server</td><td><code>.cursor-plugin/plugin.json</code>, <code>assets/</code>; marketplace listing in review</td></tr>
<tr><td>OpenCode</td><td>none</td><td>n/a</td><td>Reads the skill directly; no plugin needed</td></tr>
</tbody></table></div>
<p class="figcap">Root manifests: <code>.claude-plugin/</code>, <code>.agents/plugins/</code>, <code>.github/plugin/</code>, <code>.cursor-plugin/</code>. <b>Contradiction:</b> <code>plugins/README.md</code> calls the Cursor port "Unlike the other ports" for bundling MCP, but the root README and <code>plugins/claude-code/README.md</code> say Claude Code bundles it too. The manifests side with the latter.</p></section>'''
L=[('nolayout','No layout','Nodes all at 0,0 after repair; what the CLI exports with no --layout'),('xml-verticalFlow','verticalFlow','ELK layered, top-down'),('xml-horizontalTree','horizontalTree','ELK mrtree, left-right'),('xml-organic','organic','ELK force')]
litems=[{'n':n,'tag':'--layout' if k!='nolayout' else 'raw','il':uri(f'/tmp/dio/{k}.drawio.png',700,76,bg=(255,255,255,255)),'d':d,'meta':f'/tmp/dio/{k}.drawio.png','cap':k} for k,n,d in L]
layout=f'''<section id="layout"><div class="sec-head"><div class="eyebrow">SKILL.md L51–101, L426–444</div><h2>ELK layout and the repair pass</h2><p>I wrote a deliberately broken XML file (inside a ```xml fence, <code>&lt;mxCell id="1" parent="1"/&gt;</code>, a raw <code>&amp;</code> in "Orders & R&D", every vertex at 0,0) and ran it through the SKILL's Node repair one-liner. It stripped the fence, fixed the root parent to <code>"0"</code> and escaped the ampersands. Then each preset:</p></div>
{gallery('lgal',litems,'wide')}
<div class="tablewrap" style="margin-top:18px"><table class="dense"><thead><tr><th>Preset</th><th>SKILL.md L69–76</th></tr></thead><tbody><tr><td>verticalFlow / horizontalFlow</td><td>Layered, top-to-bottom / left-to-right (flowcharts, pipelines)</td></tr><tr><td>verticalTree / horizontalTree</td><td>Tree (hierarchies, org charts)</td></tr><tr><td>radialTree</td><td>Radial tree</td></tr><tr><td>organic</td><td>Force-directed (networks)</td></tr><tr><td>custom JSON</td><td>Array of <code>{{"layout": elkLayered|elkTree|elkRadial|elkOrganic|elkStress|elkBox, "config": {{elk.*, edgeStyle, corners}}}}</code> (L78–89)</td></tr><tr><td>libavoid</td><td>Orthogonal edge routing only; vertices stay put (L91–99)</td></tr></tbody></table></div><p class="figcap">L101: Mermaid-authored diagrams are already laid out; don't add <code>--layout</code>.</p></section>'''
M=[('flowchart','Flowchart'),('seq','Sequence'),('class','Class'),('state','State'),('er','ER'),('gantt','Gantt'),('mindmap','Mindmap'),('pie','Pie'),('timeline','Timeline'),('quadrant','Quadrant'),('git','Git graph'),('journey','User journey')]
mitems=[{'n':n,'tag':'mermaid','il':uri(f'/tmp/dio/{k}.drawio.png',640,74,bg=(255,255,255,255)),'d':f'<code>{k}.mmd</code> → <code>.drawio</code> → <code>.drawio.png</code>','meta':'drawio 32.5.5 · -e -b 10 -s 2','cap':f'{k}.drawio.png'} for k,n in M]
mine=f'''<section id="mine"><div class="sec-head"><div class="eyebrow">Rendered on the box, 20 Oct 2026</div><h2>My renders: 12 Mermaid types through the real CLI</h2><p>Each is a small <code>.mmd</code> I wrote, converted with <code>-f xml</code> and exported with <code>-f png -e -b 10 -s 2</code>. All 12 converted to native draw.io shapes (not an embedded Mermaid image) and every PNG carries an <code>mxGraphModel</code> zTXt chunk, so it reopens editable.</p></div>{gallery('mgal',mitems)}</section>'''
gf=sorted(os.listdir(G))
def nm(f): return re.sub(r'^gallery-([a-z]\d+-)?','',f[:-5]).replace('-',' ').replace('blog er','blog ER').title().replace('Cicd','CI/CD').replace('Er','ER').replace('Dfd','DFD').replace('Bpmn','BPMN').replace('Gcp','GCP').replace('Aws','AWS').replace('K8S','K8s').replace('Xy','XY').replace('C4','C4').replace('3Tier','3-tier').replace('Zenuml','ZenUML').replace('Ridedark','Ride (dark)')
gitems=[{'n':nm(f),'il':uri(G+f,560,70),'meta':'docs/images/gallery/'+f,'cap':f} for f in gf]
gallery_=f'''<section id="gallery"><div class="sec-head"><div class="eyebrow">docs/images/gallery/ · 44 WebP, 2.3 MB in repo</div><h2>Repo gallery</h2><p>jgraph's own showcase for the MCP/skill: cloud (AWS, Azure, GCP, K8s), BPMN, C4, UML, data-flow, mockups, charts. Names from filenames; I did not regenerate these, and the repo does not say which path (skill, app server or tool server) produced each {U}. Re-encoded at 560 px.</p></div>{gallery('ggal',gitems)}</section>'''
output=f'''<section id="output"><div class="sec-head"><div class="eyebrow">SKILL.md L111–216</div><h2>Output modes</h2></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Mode</th><th>How</th><th>Notes</th></tr></thead><tbody>
<tr><td>.drawio only</td><td>write XML / convert Mermaid</td><td>Default when no format asked</td></tr>
<tr><td>png / svg / pdf / jpg</td><td><code>-x -f &lt;fmt&gt; -e -b 10</code></td><td><code>-e</code> embeds the diagram (png, svg, pdf); jpg can't embed</td></tr>
<tr><td>Browser URL</td><td>deflateRaw + base64 → <code>https://app.diagrams.net/?grid=0&amp;pv=0&amp;border=10&amp;edit=_blank#R…</code></td><td>No CLI needed. My 6,684-byte login XML became a 1,653-char URL. Opens a browser (L163–204), Windows <code>.url</code> workaround</td></tr>
</tbody></table></div>
<p class="figcap">CLI locating chain (L224–321): WSL2 (Windows paths, other drives, registry), macOS app bundle, Linux <code>drawio</code> on PATH (snap/apt/flatpak), Windows native.</p></section>'''
findings=f'''<section id="findings"><div class="sec-head"><div class="eyebrow">Checked against the files and the binary</div><h2>Findings</h2></div><div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Direct .mmd → png didn't crash.</b> L47 and L459 say to convert Mermaid to <code>.drawio</code> first because direct export fails. On 32.5.5, <code>drawio -x -f png -e d.mmd</code> worked and embedded XML. Probably fixed in a newer desktop build; keep the two-step path for older installs {U}.</p></div>
<div class="callout"><span class="n">2</span><p><b>Runtime fetch.</b> For Mermaid syntax and the XML reference, the skill tells the agent to fetch <code>raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/…</code> at use time (L105–107, L448–452). Local copies exist in <code>shared/</code> (xml-reference.md 535, mermaid-reference.md 498 lines) but the skill doesn't point at them.</p></div>
<div class="callout"><span class="n">3</span><p><b>Opens apps.</b> With no format requested the skill writes <code>.drawio</code> and opens it in draw.io (L121); "Opening the result" (L364–390) opens it in a VS Code/Cursor tab if the hediet.vscode-drawio extension is installed, else with the platform opener.</p></div>
<div class="callout"><span class="n">4</span><p><b>README contradiction</b> on which ports bundle MCP (see Copies).</p></div></div></section>'''
run=f'''<section id="run"><div class="sec-head"><div class="eyebrow">Run 20 Oct 2026</div><h2>What I ran</h2></div>
{code("""D=/home/box/opt/drawio/opt/drawio/drawio      # v32.5.5 from the GitHub .deb, extracted, not installed
X="timeout 120 nice xvfb-run -a $D --no-sandbox --disable-gpu -x"
for m in flowchart seq class state er gantt mindmap pie timeline quadrant git journey; do
  $X -f xml -o /tmp/dio/$m.drawio /tmp/dio/$m.mmd
  $X -f png -e -b 10 -s 2 -o /tmp/dio/$m.drawio.png /tmp/dio/$m.drawio
done
node -e '<SKILL.md L430–442 repair one-liner>' raw.drawio      # fence, parent, & fixed
for L in verticalFlow organic horizontalTree; do $X -f xml --layout $L -o xml-$L.drawio raw.drawio; …png; done
python3 -c 'zTXt chunk check'      # mxGraphModel present in every -e PNG""")}</section>'''
risks=f'''<section id="risks"><div class="sec-head"><div class="eyebrow">Side effects</div><h2>Side effects</h2></div><div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Hosted MCP.</b> Installing the Claude Code or Cursor plugin also adds the remote MCP server <code>https://mcp.draw.io/mcp</code> (a Cloudflare worker). Diagram content sent to <code>create_diagram</code> leaves the machine; see the root README "Data Residency" (L132) and the Claude README L116.</p></div>
<div class="callout"><span class="n">2</span><p><b>Network at use time</b> for the references (finding 2), and URL mode opens app.diagrams.net in a browser. The diagram itself is in the URL fragment.</p></div>
<div class="callout"><span class="n">3</span><p><b>Electron under xvfb.</b> Headless Linux needs <code>xvfb-run</code> and <code>--no-sandbox</code>; the skill's troubleshooting (L454–468) covers this. Every run exited; nothing left running.</p></div></div></section>'''
srcs='''<section id="sources"><div class="sec-head"><div class="eyebrow">Sources</div><h2>Sources</h2></div><div class="srcs"><ul>
<li><code>plugins/*/skills/drawio/SKILL.md</code> (474, ×4 identical) · <code>plugins/README.md</code> · <code>plugins/*/README.md</code> · plugin manifests</li>
<li>Root <code>README.md</code> ("Four ways", Data Residency L132) · <code>.github/workflows/check-skill-sync.yml</code></li>
<li><code>shared/xml-reference.md</code> 535 · <code>mermaid-reference.md</code> 498 · <code>style-reference</code> 1000 · <code>repair-xml.js</code></li>
<li><code>docs/images/gallery/</code> (44) · <code>git log</code> 349 commits, head 27126ad 2026-10-18</li><li>Renders: <code>/tmp/dio/</code></li></ul></div></section>'''
foot='Built 20 Oct 2026 from <code>/home/box/drawio-skill</code> @ 27126ad. Repo gallery images and my own draw.io Desktop 32.5.5 renders, embedded as WebP.'
h=page('Inside Draw.io','Inside Draw.io',nav,GCSS+hero+fig+copies+layout+mine+gallery_+output+findings+run+risks+srcs+LB,footer=foot,extra_js=GJS)
open('/workspace/dorothy-docs/drawio/index.html','w').write(h);print(len(h))
