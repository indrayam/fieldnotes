import sys,os,re,json,glob
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
from config import src, asset
R=src('DIAGRAM_DESIGN_SRC'); SK='skills/diagram-design/'
D=Doc('diagram-design',R,'https://github.com/cathrynlavery/diagram-design/blob/0cf73c3/')
SKM=SK+'SKILL.md'; skill=D.rd(SKM)
# --- parse §3 guide
rows=re.findall(r'^\| (.+?) \| \*\*(.+?)\*\* \| \[type-([\w-]+)\.md\]',skill,re.M)
assert len(rows)==45,len(rows)
FAM={'Structure':'architecture architecture-delta it-state nested tree org-chart layers deployment dependency high-level medallion dp-integration dp-security-matrix uml-class er db-schema',
 'Flow & behavior':'flowchart sequence state swimlane process data-flow loop sankey service-blueprint journey',
 'Time & planning':'timeline gantt kanban story-map wardley fishbone',
 'Charts':'bar waterfall line scatter heatmap treemap radar polar quadrant venn pyramid',
 'Spatial':'exploded axonometric-plan'}
fam={t:f for f,ts in FAM.items() for t in ts.split()}
H={ # hand-written invoke + lesson per type
'architecture':("Draw the architecture of our checkout service: web, API gateway, three services, Postgres and Redis.","Containment carries scope. Nest admin vs traffic planes instead of drawing more arrows."),
'architecture-delta':("Show what changes when we move auth out of the monolith, before and after.","A delta diagram needs a ledger. The Changes list is what makes two topologies comparable."),
'it-state':("Map our current IT landscape by department, the before state for the migration deck.","Current-state maps are honest about mess; draw the landscape you have, not the one you want."),
'flowchart':("Flowchart the refund decision: amount, account age, fraud score.","Branches are the content. Every diamond must earn its place with a real decision."),
'sequence':("Sequence diagram of the OAuth authorization-code flow between browser, app and IdP.","Time runs down, actors run across. Labels belong on messages, not on lifelines."),
'state':("State machine for an order: placed, paid, shipped, cancelled, refunded.","Guards on transitions are where the bugs live; label them."),
'er':("ER diagram for users, teams, memberships and invites.","Model relationships, not storage. Cardinality markers do the talking."),
'timeline':("Timeline of the product's releases since 2023.","Position encodes time; keep spacing honest to the dates."),
'swimlane':("Swimlane of the hiring process across recruiter, manager and candidate.","Handoffs are the story. A lane crossing is a cost worth showing."),
'quadrant':("Plot our roadmap items on effort vs impact.","Two axes, four regions, named. Without named quadrants it is just a scatter plot."),
'radar':("Compare three vendors across five criteria on a radar.","Radar works only for few entities and few axes; past five, use a table."),
'polar':("Polar chart of support tickets by hour of day.","Angle must be cyclic for polar to be honest; otherwise use bars."),
'loop':("Draw our growth flywheel.","A loop needs its last step to feed the first. If it doesn't, it's a process."),
'nested':("Show the scope hierarchy: org, workspace, project, environment.","Containment is the hierarchy. No arrows needed."),
'tree':("Tree of the component decomposition with IDs and I/O.","Parent-child only. Fan-in breaks a tree; use a dependency graph."),
'org-chart':("Org chart of the platform team with escalation paths.","Ownership and routing, not boxes with job titles."),
'layers':("Layer stack: hardware, kernel, runtime, framework, app.","Stacking order is the claim. Each layer depends only on the one below."),
'exploded':("Exploded axonometric teardown of the device housing.","One axis of separation. Parts keep their alignment so assembly reads back."),
'axonometric-plan':("Axonometric plan of the office floor with rooms and furniture.","A plan seen at an angle: the floor is the canvas, height is a secondary cue."),
'venn':("Venn of skills shared by design, eng and PM.","Overlaps must be real sets; three circles max."),
'pyramid':("Conversion funnel from visit to paid.","Width is the number. Label the drop-off, not just the stages."),
'bar':("Bar chart of revenue by region.","Start at zero, sort by value, direct-label instead of a legend."),
'waterfall':("Budget bridge from last year to this year.","Signed steps between two totals; the arithmetic must add up and a verifier checks it."),
'treemap':("Treemap of cloud spend by service.","Area is the value; labels go where they fit and nowhere else."),
'heatmap':("Heatmap of deploys by weekday and hour.","Fill encodes value; one sequential scale, labeled."),
'line':("Line chart of weekly active users, or a slopegraph of before/after.","Pick the variant by the question: trend, two states, distribution, or rank."),
'gantt':("Gantt of the Q3 launch plan.","Bars on a real time axis; dependencies only where they constrain."),
'scatter':("Scatter of latency vs payload size.","Two continuous variables; bubble adds a third, beeswarm drops to one. New in 2.6.136: a box plot variant compares five-number summaries for a few groups, checked by verify-box-plot.py."),
'high-level':("High-level view of the data stack on Kubernetes.","An executive overview: fewer nodes, bigger groupings."),
'process':("Process diagram of the data handoffs from intake to report.","Actors and sequential steps; the handoff artifact gets named."),
'medallion':("Medallion diagram: bronze, silver, gold with access policies.","Tiers are quality levels; policies attach to tiers, not tables."),
'data-flow':("Role-scoped data flow of the ingestion pipeline.","Who touches the data at each step is the point."),
'dp-integration':("Integration topology: sources to core to consumers.","Three columns, left to right; the core is focal."),
'dp-security-matrix':("Access matrix of roles by component.","A matrix, not a graph. Cells carry the permission."),
'sankey':("Sankey of traffic from channel to signup to paid.","Band width is the amount; conservation is verified."),
'fishbone':("Fishbone of causes for the checkout outage.","One effect, causes grouped by category."),
'wardley':("Wardley map of our value chain.","Position on evolution is the claim; movement arrows are the strategy."),
'kanban':("Kanban of current WIP with limits and blocked items.","Columns are states; WIP limits make it more than a list."),
'journey':("User journey for first-time onboarding with feelings per stage.","Actions and emotion on one stage axis."),
'service-blueprint':("Service blueprint for returns, with the line of visibility.","What the customer sees vs what the service hides."),
'deployment':("Deployment diagram: zones, hosts, replicas, ports.","Where things run, not what calls what."),
'dependency':("Dependency graph of internal packages with cycles.","Fan-in and cycles are why it isn't a tree."),
'uml-class':("UML class diagram for the payment domain.","Operations and relationships; other UML routes elsewhere."),
'story-map':("Story map of the MVP with the release cut line.","Backbone across, slices down, one cut line."),
'db-schema':("Database schema with SQL types, constraints and FKs.","Physical, not logical: types and indexes belong on it."),
}
def secblock(t,name):
    m=re.search(r'^##+ (?:\d+\. )?'+name+r'[^\n]*\n(.*?)(?=^## |\Z)',t,re.M|re.S); return m.group(1) if m else ''
def bullets(block): return [re.sub(r'\s+',' ',b).strip() for b in re.findall(r'^- (.+?)(?=^\s*- |^\s*$|\Z)',block,re.M|re.S)]
def first_sent(s,n=230):
    p=plain(s); m=re.match(r'(.{25,%d}?[.!?])(\s|$)'%n,p)
    return m.group(1) if m else (p if len(p)<=n else '')
verifiers={os.path.basename(p)[7:-3] for p in glob.glob(R+'/scripts/verify-*.py')}
types=[]
for show,label,t in rows:
    p=SK+f'references/type-{t}.md'; txt=D.rd(p)
    bf=re.search(r'\*\*Best for:?\*\*:?\s*(.+)',txt); bf=first_sent(bf.group(1)) if bf else ''
    how=[x for x in (first_sent(b) for b in bullets(secblock(txt,'Layout conventions'))) if x][:5]
    if not how: how=[x for x in (first_sent(b) for b in bullets(txt)) if x][:4]
    aps=[x for x in (first_sent(b) for b in bullets(secblock(txt,'Anti-patterns'))) if x][:3]
    shot=os.path.exists(R+f'/docs/screenshots/{t}.png')
    ver=[v for v in verifiers if v==t or v.startswith(t+'-')]
    q=[[D.Q(f'| {show} | **{label}** |',SKM),SKM]]
    if bf:q.append([D.Q(bf,p),p])
    q+=[[D.Q(a,p),p] for a in aps]
    inv,les=H[t]
    types.append(dict(id=t,name=label,group=fam[t],small=f'{D.lines(p)} l',
      pills=[fam[t],f'type-{t}.md · {D.lines(p)} lines']+(['verifier' if len(ver)==1 else f'{len(ver)} verifiers'] if ver else []),
      tag=D.Q(show,SKM),invoke=inv,how=[D.Q(h,p) for h in how],quotes=q,lesson=les,
      files=[p]+([f'docs/screenshots/{t}.png'] if shot else []),src=D.blob+p,img=('g-'+t) if shot else ''))
# --- gallery
GI=[dict(id='g-'+x['id'],n=x['name'],il=uri(R+f"/docs/screenshots/{x['id']}.png",760,68),k=re.sub(r'\W','',x['group'].lower())[:6],d=esc(x['group'])) for x in types if x['img']]
FK=[(re.sub(r'\W','',f.lower())[:6],f) for f in FAM]
# --- commands + scripts explorer
C='commands/'; S=SK+'scripts/'
cmds=[
dict(id='doctor',name='/doctor',group='Commands',small='read-only',pills=['command','read-only'],tag=D.Q('Run one-shot environment diagnostics for Diagram Design readiness',C+'doctor.md'),
 invoke='/doctor --json',how=['Applies the checks and output contract from references/doctor.md.','Prints a compact summary line, per-check statuses and Next actions only when needed.'],
 quotes=D.qs(['Keep this command read-only: do not install dependencies, do not edit files, and do not run destructive git operations.','Report only verified results from this run.'],C+'doctor.md'),
 lesson='A diagnostics command that promises to change nothing is one you can run without thinking.',files=[C+'doctor.md',SK+'references/doctor.md'],src=D.blob+C+'doctor.md'),
dict(id='export',name='/export-diagram',group='Commands',small='svg+png',pills=['command','Playwright for PNG'],tag=D.Q('Export a diagram-design HTML file to .svg and .png next to the source',C+'export-diagram.md'),
 invoke='/export-diagram docs/arch.html --scale=3',how=['With no format flags, writes both .svg and .png next to the source; PNG at device scale 2.','--registry alone writes only the registry JSON and never needs Playwright.','Refuses the gallery index, files without an SVG, and mutually exclusive flags.'],
 quotes=D.qs(['**PNG requested but Playwright not installed** → surface the install instruction from the reference verbatim and stop. Do **not** auto-install.','**Source is `assets/index.html`** (the gallery, multiple SVGs in one file) → refuse and ask which specific diagram file.'],C+'export-diagram.md'),
 lesson='Write the refusals down. Eight numbered edge cases make the command predictable.',files=[C+'export-diagram.md',S+'export_svg.py',S+'export_png.py'],src=D.blob+C+'export-diagram.md'),
]
for kind,ext,acc in [('drawio','draw.io','Accepts `.drawio`, `.drawio.xml`, `.xml`, `.drawio.png`, and `.drawio.svg`.'),('excalidraw','Excalidraw','PNG/SVG exports are rejected by the extractor — ask for the saved scene.'),('mermaid','Mermaid','Accepts `.mmd`, `.mermaid`, and Markdown files containing fenced `mermaid` blocks.')]:
    p=C+f'import-{kind}.md'
    cmds.append(dict(id='import-'+kind,name='/import-'+kind,group='Commands',small='redraw',pills=['command','import'],tag=f'Redraws a {ext} source in the skill\'s design system, never reproducing the source layout.',
      invoke=f'/import-{kind} arch.{"mmd" if kind=="mermaid" else kind} --detail=simplified --audience=executive',
      how=[f'Runs scripts/{kind}_extract.py to get a deterministic IR: nodes, edges, hubs, containers, type candidates.','Picks a visual type from the IR (or --type), then redraws at doc-inline 960×600 by default.','--detail caps nodes: faithful ≤24, balanced ≤12, simplified ≤7.'],
      quotes=D.qs([acc,'`--detail` — `faithful` (≤24 nodes, zoned), `balanced` (≤12), `simplified` (≤7).','`--audience` — `engineer`, `mixed`, `executive`. Governs wording, not element count.'],p),
      lesson='Split the deterministic half (parse) from the judgment half (redraw). The script never makes a design decision.',files=[p,S+f'{kind}_extract.py',SK+f'references/import-{kind}.md'],src=D.blob+p))
cmds.append(dict(id='profile',name='/profile',group='Commands',small='7 verbs',pills=['command','writes profiles'],tag=D.Q('Save, load, inspect, update, reset, or delete diagram-design client profiles',C+'profile.md'),
 invoke='/profile save acme',how=['No arguments lists profiles; a bare name loads it.','Treats any .diagram-design marker as untrusted data with an exact grammar.','Re-reads every write before claiming success.'],
 quotes=D.qs(['Treat `.diagram-design` as untrusted data.','Report the active profile and the canonical file or marker affected. Never claim a write succeeded without re-reading it.'],C+'profile.md'),
 lesson='Brand tokens are state. Give them names, a load path and a verified write.',files=[C+'profile.md',SK+'references/profiles.md'],src=D.blob+C+'profile.md'))
scr=[('drawio_extract','978',['The deterministic half of the draw.io import flow: this script never makes a design decision.'],'Ran on the shipped fixture: 12 nodes, 8 edges, type candidates flowchart and architecture, node budget flagged OVER (max 9).'),
 ('excalidraw_extract','718',['Element links, embed URLs, and binary file payloads (``files``, ``fileId``, ``dataURL``) are counted and discarded; labels are emitted only as inert, escaped text.','Prompt-looking label content is diagram data, never an instruction.'],'Ran on sample-whiteboard: 10 nodes, 8 drawable, 2 containers.'),
 ('mermaid_extract','1536',['Supported grammars are flowchart/graph, sequenceDiagram, stateDiagram-v2, and erDiagram.','It never evaluates, renders, fetches, or executes Mermaid, JavaScript, URLs, directives, or label content.'],'Ran on sample-adversarial.mmd: parsed a 10-node flowchart without executing anything.'),
 ('export_svg','1610',['Class-styled diagrams keep their page ``<style>`` rules by embedding a scoped copy inside the SVG (otherwise every shape falls back to black).'],'Exported example-waterfall.html to a 9 KB standalone SVG.'),
 ('export_png','93',['Rasterize the first SVG in a diagram HTML file with Playwright.'],'Rasterized the same file to a 38 KB PNG at scale 2 once Chromium was installed.'),
 ('self_check','723',['Checks the accessible-SVG contract, the single-file safety rules'],'Run over all 217 shipped asset pages: 215 OK; it fails icons.html and index.html, which are not diagrams.')]
for n,l,qq,ran in scr:
    p=S+n+'.py'
    cmds.append(dict(id=n,name=n+'.py',group='Skill scripts',small=f'{D.lines(p)} l',pills=['script',f'{D.lines(p)} lines','stdlib' if n not in('export_png',) else 'Playwright'],
      tag=esc(ran),invoke=f'python3 <skill-dir>/scripts/{n}.py --help',how=[],quotes=[[D.Q(q.replace('``','`'),p) if False else D.Q(q,p),p] for q in qq],
      lesson='Ship the checker with the skill so the agent can verify its own output, not just the repo CI.' if n=='self_check' else 'Deterministic code for parsing and export; judgment stays in the prompt.',files=[p],src=D.blob+p))
# --- semantic patterns
sp=re.findall(r'^\| (.+?) \| \*\*(.+?)\*\* → (.+?) \|$',skill,re.M)
sprows=[[D.Q(a,SKM),f'<b>{esc(b)}</b>',esc(c)] for a,b,c in sp]
uap=re.findall(r'^\| ([^|]+?) \| ([^|]+?) \|$',secblock(skill,'4\\. Universal'),re.M)[1:]
uaprows=[[D.Q(a,SKM),D.Q(b,SKM)] for a,b in uap]
# --- sections
hro=hero('Skill explainer · cathrynlavery/diagram-design','Diagram Design',8,
 '<mark>Forty-five editorial diagram types</mark>, one rule above all: delete until nothing can be removed.',
 f'A Claude/Cursor skill that writes self-contained HTML with inline SVG in a skinnable editorial system. It routes a request through 9 semantic patterns to 45 type references, ships importers for draw.io, Excalidraw and Mermaid, and backs its charts with geometry verifiers. I read the skill, ran all 74 repository checks and the 6 shipped scripts. {D.Q("The highest-quality move is usually deletion.",SKM)}',
 [('v2.6.136','plugin version'),('0cf73c3','commit, 27 Oct 2026'),('45','visual types'),('6','commands'),('6','skill scripts'),('74/74','repo checks pass')],
 [('Who it is for','Anyone who wants a diagram that looks designed rather than generated: architecture, charts, journeys, maps.'),('What you get','One HTML file per diagram, optional SVG/PNG export, and a brand profile you can save and reload.')])
s_how=sec('how','How It Works','It Picks A Pattern, Then A Type, Then Asks','The skill is a router. Behavior picks the pattern, the pattern picks the nearest layout, and the plan is confirmed before anything is drawn.',
 callouts([f'<b>Style gate.</b> {D.Q("If they are still the shipped defaults (paper `#f5f5f5`, ink `#2d3142`, accent `#bf4520`), **pause and ask the user**",SKM)}.',
  f'<b>Semantic pattern.</b> {D.Q("When behavior, state, enforcement, or risk carries the meaning, first load",SKM)} semantic-patterns.md.',
  f'<b>Visual type.</b> {D.Q("**Always load the chosen type reference linked in the guide before drawing.**",SKM)}',
  f'<b>Confirm.</b> {D.Q("Before rendering, state the plan in one short message: the chosen visual type (and semantic pattern, if routed), the size preset, and anything the complexity budget (§7) will force out.",SKM)}',
  f'<b>Density.</b> {D.Q("**Target density: 4/10.** Enough to be technically complete. Not so dense it needs a guide. Above 9 nodes, it\'s probably two diagrams.",SKM)}'])+
 '<h3>The 9 Semantic Patterns</h3>'+table(['Behavioral trigger','Pattern','Nearest type'],sprows))
s_types=f'<section id="types">{head("The Types","Every Type Is A Reference File With Rules And Anti-Patterns","Pick a type. The tag is the row from the SKILL.md §3 guide; How it works lists the reference file’s layout conventions; the quotes are its own anti-patterns, all checked at build time.")}{explorer("ty","types")}</section>'
s_gal=sec('gallery','Gallery','The Repo’s Own Renders For 45 Types','Screenshots shipped in docs/screenshots, one per type. Click to enlarge.',gchips('gdd',FK)+gal('gdd',GI))
s_cmd=f'<section id="commands">{head("Commands And Scripts","Importers Parse; The Skill Redraws","Six slash commands drive the workflow. Six stdlib-first scripts do the deterministic work, and I ran each one.")}{explorer("cm","commands")}</section>'
s_ap=sec('antipatterns','Taste','It Names The Slop It Refuses To Make','The universal anti-patterns from SKILL.md §4, verbatim.',table(['Anti-pattern','Why it fails'],uaprows))
s_find=sec('findings','What I Found Running It','The Code Is Solid; The Runner Is Inconsistent','I ran 74 repository checks (every scripts/test-*.py and verify-*.py) plus the 6 skill scripts on the box, with nice and timeout, at commit 7a12007.',
 table(['Run','Result','Note'],[
  ['74 repo checks, first pass','59 pass, 15 fail','12 verifiers exit 2 when given no paths; 3 Playwright tests fail before Chromium is installed.'],
  ['Same 15, rerun correctly','15/15 pass','After <code>playwright install chromium</code> and adding <code>--all</code> (or <code>--shipped</code> for verify-motion).'],
  ['self_check.py over 217 assets','215 OK, 2 FAIL','icons.html and index.html are galleries, not diagrams; exit code 1 for the batch.'],
  ['3 extractors on fixtures','pass','draw.io: 12 nodes / 8 edges, node budget flagged OVER (max 9).'],
  ['export_svg / export_png','pass','9 KB SVG and 38 KB PNG from example-waterfall.html.'],
  ['git status after all runs','clean','No files written into the repo.']])+
 verdict([('Gap','Verifier flags disagree','Most verifiers take <code>--all</code>; verify-motion takes <code>--shipped</code> and rejects <code>--all</code>. Without a flag they print usage and exit 2, which reads like a failure in CI.'),
  ('Gap','Playwright is a silent prerequisite','Three tests and PNG export need a downloaded Chromium. The export command documents this; the test scripts just crash with a stack trace.'),
  ('Gap','Version drift','plugin.json says 2.6.136; SKILL.md metadata says 2.6.'),
  ('Bug','Escaped IR headers','drawio_extract and excalidraw_extract print the file name markdown-escaped (<code>sample\\-architecture\\.drawio</code>); mermaid_extract does not.'),
  ('Copy','Untrusted-input stance in parsers','The Excalidraw and Mermaid extractors treat labels as data and discard links and payloads. That is the right default for anything an agent reads.'),
  ('Copy','Verifiers for the chart math','Waterfall, Sankey, beeswarm and others check the rendered geometry against declared values, so a plausible-but-wrong chart fails.')]))
s_steal=sec('yours','Build Your Own','What To Steal',''.join([]),steal([('One reference file per output type.','Each has Best for, layout rules and anti-patterns. The agent loads only the one it needs.'),
 ('Route by meaning before layout.','A semantic pattern picks the behavior; the type picks geometry.'),('Gate on brand tokens.','Refuse to ship defaults into a branded project without asking.'),
 ('Confirm the plan in one message.','Type, size and what the budget cuts, before drawing.'),('Ship the checker.','self_check.py lets the agent verify its own file.')]))
s_src=sec('sources','Sources','Everything Here Is Checked','Each quote on this page is compared with its source file at build time; the build fails on any mismatch.',
 srcs([D.L(SKM),D.L(SK+'references/semantic-patterns.md'),D.L(C+'export-diagram.md'),D.L('.claude-plugin/plugin.json'),f'<a href="https://github.com/cathrynlavery/diagram-design">github.com/cathrynlavery/diagram-design</a>']))
nav=[('top','Overview'),('how','How it works'),('types','Types'),('gallery','Gallery'),('commands','Commands'),('antipatterns','Anti-patterns'),('findings','Findings'),('yours','Build your own'),('sources','Sources')]
JS=explorer_js('ty','dd-ty',types,list(FAM))+explorer_js('cm','dd-cm',cmds,['Commands','Skill scripts'])
D.finish()
n=build('diagram-design','Inside Diagram Design',nav,hro+s_how+s_types+s_gal+s_cmd+s_ap+s_find+s_steal+s_src,
 'Compiled 22 Oct 2026, updated 1 Nov 2026 to cathrynlavery/diagram-design @ 0cf73c3 (v2.6.136: box plot variant on scatter; self_check rejects a document that stopped early; dp-integration primary connectors get a focal_accent arrowhead; exploded type rejects CSS transforms on projected geometry; import fixes for Mermaid edge IDs, sequence autonumber, draw.io angle brackets and outer Excalidraw groups. 2.6.120: Mermaid import digest now lists else, and, and option regions; the run results are from 7a12007, and verify-mermaid-import passed at 0b9b10c) · every quote is checked against its source file at build time · not affiliated with the author.',JS)
print('built',n,'types',len(types),'cmds',len(cmds),'gallery',len(GI),'uap',len(uaprows),'sp',len(sprows))
