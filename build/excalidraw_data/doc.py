import sys,os,re,json
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
from gal import uri
from config import src, asset
R=src('EXCALIDRAW_SRC')
D=Doc('excalidraw',R,'https://github.com/yctimlin/mcp_excalidraw/blob/66b768b/')
S='skills/excalidraw-skill/SKILL.md'; CS='skills/excalidraw-skill/references/cheatsheet.md'
def Q(s,f=S): return D.Q(s,f)
cs=D.rd(CS)
OLD=json.load(open(asset('excalidraw','gallery.json')))
gi=[dict(id=f'g{j}',n=o['n'],il=o['il'],d=re.sub(r'\s*\(L[\d–-]+\)','',o['d']),k='demo' if 'demo' in o['n'] else 'style',dark=o.get('dark',False)) for j,o in enumerate(OLD)]
for j,(p,n,d) in enumerate([(asset('excalidraw','s1.png'),'This run: SKILL.md example','Headless screenshot from the canvas server, 8 elements.'),(asset('excalidraw','s1d.png'),'This run: --dark','Same scene with --dark.'),(asset('excalidraw','r.png'),'This run: offline render','render on the exported .excalidraw, no server.')]):
    gi.append(dict(id=f'r{j}',n=n,il=uri(p),d=d,k='run',dark=False))
# MCP tools
tools=[]
for sec_ in re.split(r'^### ',cs.split('## MCP Tools')[1].split('## Canvas REST')[0],flags=re.M)[1:]:
    g=sec_.split('\n')[0].strip()
    for m in re.finditer(r'^\| `(\w+)` \| ([^|]+) \| (.+) \|$',sec_,re.M):
        n,desc,par=m.group(1),m.group(2).strip(),m.group(3).strip()
        tools.append(dict(id=n,name=n,group=g,small='',pills=[g],tag=Q(desc,CS),invoke=f'{n}({esc(par)})' if par!='(none)' else f'{n}()',how=[],quotes=[],extra='',
          lesson='Every tool has a CLI twin, so an agent without MCP loses nothing.',files=[CS],src=D.blob+CS,img=''))
GT=list(dict.fromkeys(t['group'] for t in tools))
# CLI
RAN={'start':'Spawned the server on a private port (3917): pid printed, exit 0.','stop':'Stopped only its own pid after a /health check; status then exited 3.','status':'JSON with element count and renderers {node: true, browser: 0}.',
 'add':'Created the 8-element SKILL.md example; arrows bound automatically.','update':'Moved svc-a; its bound arrows re-routed.','get':'Unknown id: “Element with ID nope not found”, exit 1.',
 'query':'--type arrow returned the 4 arrows with points.','describe':'Plain-text list of ids, positions, labels and a bounding box.','screenshot':'PNG, dark PNG and SVG, all with renderer “node”, no browser.',
 'render':'Rendered the exported file offline: 570×380, 12 elements.','export':'JSON and Obsidian .excalidraw.md both wrote 12 elements. A path in a missing directory fails with ENOENT.',
 'import':'Re-imported the .excalidraw.md with --replace: 12 elements.','mermaid':'Exit 4 with no browser tab, as documented.','snapshot':'save / list / restore all worked; restore brought back 8 elements.',
 'arrange':'align --to top on two ids: successCount 2.','clear':'Without --yes: exit 2 and a usage line. With --yes: cleared.','share':'Not run: it uploads the scene to excalidraw.com.','install-skill':'Not run: it replaces a skills directory.'}
cli=[]
for sec_ in re.split(r'^### ',cs.split('## CLI Reference')[1].split('## MCP Tools')[0],flags=re.M)[1:]:
    g=sec_.split('\n')[0].strip()
    for m in re.finditer(r'^\| `([^`]+)`[^|]*\| (.+) \|$',sec_,re.M):
        cmd,desc=m.group(1),m.group(2).strip()
        k=cmd.split()[0].split('\\')[0]
        if k=='help' or any(c['name']==k for c in cli): continue
        cli.append(dict(id='c'+k.replace('-',''),name=k,group=g,small='',pills=[g],tag=Q(desc,CS),invoke=f'npx -y mcp-excalidraw-server {cmd.replace(chr(92),"")}',how=[],quotes=[],
         extra=f'<div class="d-sec"><h4>What happened when I ran it</h4><p>{esc(RAN[k])}</p></div>' if k in RAN else '',lesson='JSON on stdout and fixed exit codes make the CLI scriptable.',files=[CS,'src/cli'],src=D.blob+CS,img=''))
GC=list(dict.fromkeys(c['group'] for c in cli))
hro=hero('Skill explainer · yctimlin/mcp_excalidraw','Excalidraw',0,
 'An agent draws on a <mark>live canvas, then screenshots its own work</mark> and fixes what it sees.',
 f'A skill, a CLI and an MCP server over one Excalidraw canvas. I read the skill and cheatsheet, ran the test suite, and drove every local CLI command against a private server. {Q("Pairing `describe` with `screenshot` is what makes this skill powerful.")}',
 [('66b768b','commit, 30 Oct 2026'),('v2.1.2','package'),(str(len(tools)),'MCP tools'),(str(len(cli)),'CLI commands'),('3','interfaces'),('5 suites','tests pass')],
 [('Who it is for','Agents drawing architecture or flow diagrams users will edit by hand.'),('What you get','An editable .excalidraw (or Obsidian .md) file, plus PNG or SVG.')])
s_how=sec('how','How It Works','Plan The Grid, Draw, Screenshot, Fix','From SKILL.md.',callouts([
 f'<b>Pick an interface.</b> {Q("Three interfaces drive the same live canvas. Pick the first one that applies:")}',
 f'<b>Plan.</b> {Q("Plan your coordinate grid — map out tiers and x-positions before writing JSON.")}',
 f'<b>Check every batch.</b> {Q("After each `add` / `apply` / `batch_create_elements`, take a screenshot and check:")}',
 f'<b>Say it out loud.</b> {Q("If you find any issue: **stop, fix it, re-screenshot, then continue.**")}',
 f'<b>No browser for checks.</b> {Q("Screenshots and image exports render headless inside the canvas server, so you never need a browser tab to check your own work.")}']))
s_cli=f'<section id="cli">{head("The CLI",f"{len(cli)} Commands, Fixed Exit Codes","Descriptions are quoted from the cheatsheet. I ran each on a private port, except the two that publish or replace files.")}{explorer("cl","commands")}</section>'
s_gal=sec('gallery','Gallery',f'{len(gi)} Renders','Renders from the earlier review, plus three from this run. Click to enlarge.',gchips('gex',[('style','Styling'),('run','This run'),('demo','Repo demo')])+gal('gex',gi))
s_mcp=f'<section id="tools">{head("The MCP Tools",f"{len(tools)} Tools, One Per CLI Verb","Grouped as in the cheatsheet; parameters are shown as listed there.")}{explorer("mt","tools")}</section>'
s_find=sec('findings','What I Found Running It','Solid And Well Tested; A Few Sharp Edges','Run on a copy in /tmp with nice and timeout; the server ran on port 3917 and I stopped it by its own pid.',
 table(['Run','Result','Note'],[['npm test (6 suites)','pass','stdio wire 5/5, local bind, 25 render checks, state, durable state, share URL.'],['CLI session','16 commands','All behaved as documented.'],
  ['mermaid with no tab','exit 4','As documented.'],['export to a missing directory','exit 1','ENOENT; no mkdir.']])+
 verdict([('Copy','Headless verification','Screenshots render in the server with Excalidraw’s own renderer; the agent never needs a browser to see its work.'),
  ('Copy','Exit codes as an API','0 ok, 1 error, 2 usage, 3 canvas unreachable, 4 browser needed. Destructive clear needs --yes (exit 2 otherwise).'),
  ('Copy','Safe stop','stop checks /health identity and only signals its own server.'),
  ('Gap','Export does not create directories','A path inside a missing folder fails with ENOENT.'),
  ('Gap','Mermaid needs a browser tab','Conversion runs in the frontend, so headless agents cannot use it.'),
  ('Cost','Element counts drift','add and snapshot report 8 elements; export reports 12, because bound label text becomes separate elements. SKILL.md’s duplicate-text section covers the related auto-sync issue.'),
  ('Cost','share uploads','share sends an encrypted scene to excalidraw.com unless self-hosted URLs are set. I did not run it.')]))
s_steal=sec('yours','Build Your Own','What To Steal','',steal([('One canvas, three interfaces.','MCP, CLI and REST map 1:1.'),('Text plus pixels.','describe for ids, screenshot for quality.'),
 ('A written checklist.','Seven checks after every batch.'),('Name the anti-patterns.','Zone labels, cross-zone arrows and label spam, each with a fix.')]))
s_src=sec('sources','Sources','Everything Here Is Checked','Each quote is compared with its source file at build time; the build fails on any mismatch.',
 srcs([D.L(S),D.L(CS),'<a href="https://github.com/yctimlin/mcp_excalidraw">github.com/yctimlin/mcp_excalidraw</a>']))
nav=[('top','Overview'),('how','How it works'),('cli','CLI'),('gallery','Gallery'),('tools','MCP tools'),('findings','Findings'),('yours','Build your own'),('sources','Sources')]
JS=explorer_js('cl','ex-cl',cli,GC)+explorer_js('mt','ex-mt',tools,GT)
D.finish()
n=build('excalidraw','Inside Excalidraw',nav,hro+s_how+s_cli+s_gal+s_mcp+s_find+s_steal+s_src,'Compiled 22 Oct 2026 from yctimlin/mcp_excalidraw @ 774a70c, updated 1 Nov 2026 to 66b768b (still v2.1.2: MCP file tools resolve symlinks and restrict file types; dark theme persists after copy link, copy as SVG and wrap in frame; ?element= links resolve after the scene loads; idle autosync loop fixed) · every quote is checked against its source file at build time · not affiliated with the author.',JS)
print('built',n,len(cli),len(tools),len(gi))
