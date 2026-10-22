import sys,os,re,json
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
from config import src, asset
R=src('DRAWIO_SRC')
D=Doc('drawio',R,'https://github.com/jgraph/drawio-mcp/blob/05c1747/')
S='plugins/cursor/skills/drawio/SKILL.md'; T='mcp-tool-server/src/index.js'
OLD=json.load(open(asset('drawio','gallery.json')))
gi=[]
for j,o in enumerate(OLD):
    k='layout' if j<4 else 'mmd' if j<16 else 'gal'
    d={'layout':'ELK layout, box render','mmd':'Mermaid → .drawio → PNG, box render','gal':'Repo gallery (docs/images/gallery)'}[k]
    gi.append(dict(id=f'g{j}',n=o['n'],il=o['il'],d=d,k=k,dark=o.get('dark') in (True,'True')))
GK=[('layout','Layouts'),('mmd','Mermaid types'),('gal','Repo gallery')]
def Q(s): return D.Q(s,S)
def row(name):
    m=re.search(r'^\| `%s` \| ([^|]+) \|$'%re.escape(name),D.rd(S),re.M); return m.group(1).strip()
# --- pipeline explorer
P=[]
P.append(dict(id='mermaid',name='Mermaid',group='Author',small='preferred',pills=['needs desktop CLI','.mmd → .drawio'],tag=Q('The desktop CLI converts Mermaid to a native `.drawio` file and lays it out automatically, which is far more reliable than hand-positioning cells in XML.'),
 invoke='/drawio:drawio create a flowchart',how=[Q('**Prefer Mermaid** when the desktop CLI is available and the request is one of the standard types above.'),Q('Delete the `.mmd` afterward — the `.drawio` is the artifact.')],
 quotes=[[Q('**Always convert Mermaid to `.drawio` first, then export** — direct Mermaid → PNG export with `-e` is broken in current draw.io Desktop (the embedded-XML step crashes); the two-step path is reliable and produces an editable embed.'),S]],
 lesson='Let a real layout engine place nodes; ask the model only for structure.',files=[S,'shared/mermaid-reference.md'],src=D.blob+S,img='g4'))
P.append(dict(id='xml',name='draw.io XML',group='Author',small='fallback',pills=['no CLI needed','repair pass'],tag=Q('**Use XML** for precise control, or as the universal fallback'),
 invoke='/drawio:drawio pdf AWS architecture overview',how=[Q('Cell `id="0"` is the root layer'),Q('Cell `id="1"` is the default parent layer'),Q('Every edge needs a child `<mxGeometry relative="1" as="geometry" />` — a self-closing edge `mxCell` doesn\'t render')],
 quotes=[[Q('**NEVER include ANY XML comments (`<!-- -->`) in the output.**'),S]],
 extra='<div class="d-sec"><h4>What happened when I ran it</h4><p>I fed the SKILL.md repair one-liner a reply wrapped in prose and a code fence, with <code>R&amp;D &lt;b&gt;</code> in a label and layer 1 parented to itself. It stripped the text, escaped the attribute and re-parented the layer.</p></div>',
 lesson='Ship a deterministic repair step for the mistakes models make every time.',files=[S,'shared/xml-essentials.md'],src=D.blob+S,img='g16'))
LI={'verticalFlow':'g1','horizontalTree':'g2','organic':'g3'}
for n in ['verticalFlow','horizontalFlow','verticalTree','horizontalTree','radialTree','organic']:
    P.append(dict(id=n,name=n,group='Layout',small='ELK preset',pills=['--layout '+n,'XML only'],tag=Q(row(n)),invoke=f'drawio -x -f xml --layout {n} -o diagram.drawio diagram.drawio',
     how=[Q('Generate the cells with approximate (or even `0,0`) positions and get the graph *structure* — nodes and edges — right.'),Q("Mermaid-authored diagrams are already laid out — don't add `--layout`.")],quotes=[[Q('(reading and overwriting the same path is supported)'),S]],
     lesson='Presets name intent (flow, tree, network), not algorithms.',files=[S],src=D.blob+S,img=LI.get(n,'')))
P.append(dict(id='libavoid',name='libavoid',group='Layout',small='edge routing',pills=['--layout libavoid','moves no vertex'],tag=Q('`--layout libavoid` routes the **edges** orthogonally around the shapes (*Arrange ▸ Layout ▸ Orthogonal Routing*) without moving any vertex.'),
 invoke='drawio -x -f xml --layout libavoid -o diagram.drawio diagram.drawio',how=[Q("skip it after a flow/tree preset, which already routes its edges")],quotes=[],lesson='Separate placing nodes from routing edges, so hand layouts can still get clean wires.',files=[S,'mcp-tool-server/src/libavoid-pass.js'],src=D.blob+S,img=''))
P.append(dict(id='custom',name='Custom JSON',group='Layout',small='advanced',pills=['elkLayered','elkTree','elkRadial','…'],tag=Q('For finer control, pass a JSON **array** (starting with `[`) instead of a preset name'),
 invoke="""drawio -x -f xml --layout '[{"layout":"elkLayered","config":{"elk.direction":"RIGHT"}}]' -o diagram.drawio diagram.drawio""",how=[Q('Algorithms: `elkLayered`, `elkTree`, `elkRadial`, `elkOrganic`, `elkStress`, `elkBox`.')],quotes=[],lesson='Expose the escape hatch in the same format as the editor dialog.',files=[S],src=D.blob+S,img=''))
OUT=[('drawio','.drawio','If no format is mentioned, produce the `.drawio` file and open it; the user can ask to export later.','/drawio:drawio create a flowchart','g16'),
 ('png','PNG','PNG, SVG and PDF are exported with `-e` (`--embed-diagram`): the file contains the full diagram XML, so opening it in draw.io recovers the editable diagram.','/drawio:drawio png flowchart for login','g4'),
 ('svg','SVG','Exports use double extensions — `name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf` — to signal the embedded diagram XML','/drawio:drawio svg: ER diagram','g8'),
 ('pdf','PDF','`-a` / `--all-pages`: export all pages (PDF only)','/drawio:drawio pdf AWS architecture overview',''),
 ('url','Browser URL','For `url` format, keep the `.drawio` file on disk as the user\'s local copy','/drawio:drawio url flowchart for user login','')]
for i,n,t,inv,img in OUT:
    ex=''
    if i=='url': ex='<div class="d-sec"><h4>What happened when I ran it</h4><p>The SKILL.md one-liner turned a small diagram into a 247-character <code>#R</code> link; inflating it gave back the original XML.</p></div>'
    P.append(dict(id='o'+i,name=n,group='Output',small='format',pills=['deliver'],tag=Q(t),invoke=inv,how=[Q('If the open command fails, print the absolute path (or URL) so the user can open it manually.')],
     quotes=[[Q("Don't use a `#create=` URL for XML"),S]] if i=='url' else [[Q('`jpg` is lossy and can\'t embed the XML.'),S]] if i=='png' else [],extra=ex,
     lesson='Every export stays editable: the diagram travels inside the image.',files=[S],src=D.blob+S,img=img))
# --- modules explorer
def hdr(p):
    for l in D.rd(p).split('\n'):
        x=l[2:].strip()
        if x and not set(x)<=set('─ ') and '──' not in x: return x
RAN={'repair-xml':'Fixed a prose-wrapped reply: “text around the diagram removed”, “layer re-parented to the root”, “attribute values escaped”; it also returned the stray <code>&lt;/content&gt;</code> as trailing text.',
 'normalize-model':'An edge between two cells in a swimlane, written with parent="1", came back with parent="c".',
 'mermaid-elk':'withElkLayout added the <code>config: layout: elk</code> frontmatter to a flowchart; a sequence diagram was detected as sequencediagram.',
 'shape-search':'Index holds 10,800 shapes. “aws lambda” → Lambda; “kubernetes pod” → Pod; “cisco router” ranked a stencil titled “10700” first.',
 'icon-search':'Not called: it queries icons.diagrams.net over the network.'}
M=[]
for f in ['repair-xml','normalize-model','mermaid-elk','shape-search','icon-search','label-perimeter','mx-xml','mx-model']:
    p=f'shared/{f}.js'
    M.append(dict(id=f,name=f+'.js',group='Shared modules',small=f'{D.lines(p)} l',pills=['shared',f'{D.lines(p)} lines'],tag=D.Q(hdr(p),p),invoke=f'import … from "./shared/{f}.js"',how=[],quotes=[],
     extra=f'<div class="d-sec"><h4>What happened when I ran it</h4><p>{RAN[f]}</p></div>' if f in RAN else '',lesson='One copy of each pass, copied into both servers by npm run copy-shared.',files=[p],src=D.blob+p,img=''))
TL=[('open_drawio_xml','Opens the draw.io editor with a diagram from draw.io XML. '),('open_drawio_csv','Opens the draw.io editor with a diagram generated from CSV data. '),
 ('open_drawio_mermaid','Opens the draw.io editor with a diagram generated from Mermaid.js syntax, '),('get_drawio_reference','Returns a full draw.io diagram generation reference as Markdown. '),
 ('list_pages','Lists the pages (diagrams) in a local .drawio file without loading full page content. '),('get_page','Reads one page (diagram) from a local .drawio file and returns its raw mxGraphModel '),
 ('set_page','Replaces the content of one page (diagram) in a local .drawio file with new '),('search_shapes','Search the draw.io shape library by keywords. ')]
for n,t in TL:
    M.append(dict(id=n,name=n,group='MCP tools',small='tool',pills=['@drawio/mcp 1.10.0'],tag=D.Q(t.strip(),T),invoke=f'{n}(…)',how=[],quotes=[],lesson='The skill and the MCP server share modules; the skill is the file-writing path.',files=[T],src=D.blob+T,img=''))
# --- sections
hro=hero('Skill explainer · jgraph/drawio-mcp','Draw.io',4,
 'Every diagram becomes a <mark>native .drawio file first</mark>, then whatever format you asked for.',
 f'The official draw.io skill, shipped byte-identical to Claude Code, Codex, Copilot, Cursor and Antigravity. Author as Mermaid or XML, repair it, lay it out with ELK, and export with the XML embedded so every PNG stays editable. I read the skill, ran both servers’ test suites and the shared modules. {Q("Every diagram becomes a native `.drawio` file first, then is delivered in the requested output format, whether you authored Mermaid or XML.")}',
 [('05c1747','commit, 22 Oct 2026'),('5','byte-identical ports'),('6','ELK presets'),('5','output formats'),('8','MCP tools'),('201/201','tests pass')],
 [('Who it is for','Agents in terminals (Claude Code, Codex, Copilot CLI) where diagrams cannot render inline.'),('What you get','A .drawio, an embedded-XML PNG/SVG/PDF, or an app.diagrams.net link.')])
s_how=sec('how','How It Works','Author, Repair, Lay Out, Deliver','The skill is one pipeline with two ways in.',
 callouts([f'<b>Inline first.</b> {Q("**Inline viewer first.**")} In chats that render diagrams, the MCP create_diagram tool wins.',
  f'<b>Author.</b> Mermaid when the desktop CLI exists; XML otherwise. {Q("If Mermaid was requested but no desktop CLI is available, author the same diagram as XML.")}',
  f'<b>Repair.</b> {Q("It changes nothing in a well-formed file, and needs only Node.js")}.',
  f'<b>Lay out.</b> {Q("The CLI\'s `--layout` step auto-positions XML-authored diagrams with the same ELK layouts as the editor\'s *Arrange ▸ Layout* menu and the draw.io MCP app server.")}',
  f'<b>Deliver.</b> {Q("Exports use double extensions")} so the name says the XML is inside.']))
s_pipe=f'<section id="pipeline">{head("The Pipeline","Fifteen Choices, One Artifact","Pick an authoring route, a layout or an output. Quotes are checked against SKILL.md at build time.")}{explorer("pp","pipeline")}</section>'
s_gal=sec('gallery','Gallery','60 Renders','ELK layouts and Mermaid conversions rendered on this box, plus the repo’s own gallery. Click to enlarge.',gchips('gdr',GK)+gal('gdr',gi))
s_mod=f'<section id="modules">{head("Under The Hood","Eight Shared Modules Feed Two Servers","The skill’s inline repair step is a small version of repair-xml.js. I imported each module and ran it on test input.")}{explorer("md","modules")}</section>'
s_find=sec('findings','What I Found Running It','Thoroughly Tested; The CLI Is The Dependency','All runs used a copy of the repo in /tmp, with nice and timeout, at commit 05c1747.',
 table(['Run','Result','Note'],[
  ['mcp-tool-server npm test','125/125 pass','About 1 s.'],['mcp-app-server npm test','76 pass, 2 skipped','Skipped tests need a live Worker (EDGE_COMPARE_URL).'],
  ['SKILL.md repair one-liner','fixed','Prose, fence, unescaped label and self-parented layer.'],['SKILL.md URL one-liner','round-trips','247-character link for a tiny diagram.'],
  ['Shared modules','work','repair, normalize, mermaid-elk and shape search all behaved as documented.'],['5 SKILL.md ports','byte-identical','A CI workflow enforces it.'],
  ['draw.io Desktop CLI','not on the box','Mermaid conversion, layout and export need it.']])+
 verdict([('Gap','Mermaid, layouts and export all need the desktop app','Without it the skill can only write XML and a URL. The skill says so and falls back cleanly.'),
  ('Gap','References load from main, unpinned','SKILL.md tells the agent to fetch xml-essentials.md and mermaid-reference.md from raw.githubusercontent.com/…/main, so a skill pinned at one commit reads rules from another.'),
  ('Cost','Two repair implementations','The inline one-liner and repair-xml.js do overlapping work; only the module reports what it changed or handles leaked tool-call tags.'),
  ('Bug','Shape search ranks a number first','“cisco router” returns a stencil titled “10700” above “ATM Router”.'),
  ('Copy','Editable exports','<code>-e</code> embeds the XML, and the double extension tells people it is there.'),
  ('Copy','Port parity in CI','One workflow fails the build if any port’s SKILL.md drifts from the Claude Code copy.')]))
s_steal=sec('yours','Build Your Own','What To Steal','',steal([('One native artifact, many deliveries.','Write the source format first; derive the rest.'),('Prefer a layout engine to model coordinates.','Ask for structure, not positions.'),
 ('Measure the model’s mistakes, then fix them in code.','repair-xml.js says its three fixes covered all 15 broken diagrams out of 473.'),('Detect the environment exhaustively.','The Windows chain checks PATH, install paths, registry and other drives before giving up.'),('Keep ports identical by CI.','')]))
s_src=sec('sources','Sources','Everything Here Is Checked','Each quote on this page is compared with its source file at build time; the build fails on any mismatch.',
 srcs([D.L(S),D.L(T),D.L('shared/repair-xml.js'),D.L('.github/workflows/check-skill-sync.yml'),'<a href="https://github.com/jgraph/drawio-mcp">github.com/jgraph/drawio-mcp</a>']))
nav=[('top','Overview'),('how','How it works'),('pipeline','Pipeline'),('gallery','Gallery'),('modules','Under the hood'),('findings','Findings'),('yours','Build your own'),('sources','Sources')]
JS=explorer_js('pp','dr-pp',P,['Author','Layout','Output'])+explorer_js('md','dr-md',M,['Shared modules','MCP tools'])
D.finish()
n=build('drawio','Inside Draw.io',nav,hro+s_how+s_pipe+s_gal+s_mod+s_find+s_steal+s_src,
 'Compiled 22 Oct 2026 from jgraph/drawio-mcp @ 05c1747 · every quote is checked against its source file at build time · not affiliated with draw.io Ltd.',JS)
print('built',n,len(P),len(M),len(gi))
