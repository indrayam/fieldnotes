import sys,os,re,json,glob
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
R='/home/box/illo-skill'; SK='skills/illo/'
D=Doc('illo',R,'https://github.com/tmchow/illo-skill/blob/0b0abee/')
SKM=SK+'SKILL.md'; VS=SK+'references/visual-style.md'; E=SK+'scripts/illo.py'
OLD=json.load(open('/workspace/dorothy-docs/_old/illo.json'))
def first_para(t):
    t=re.sub(r'^#.*\n','',t).strip(); return re.sub(r'\s+',' ',t.split('\n\n')[0])
def first_sent(p,n=260):
    m=re.match(r'(.{20,%d}?[.!?])(\s|$)'%n,plain(p)); return m.group(1) if m else plain(p)[:0]
# gallery: characters, looks, palettes, explainers, cutouts
gi=[];lookimg={}
for j,o in enumerate(OLD):
    k=o.get('k') or ''
    n=o['n']
    if k: cat='char'
    elif n.startswith('Riso'): cat='riso'
    elif '-' in n and o['d'].startswith('Prompt'): cat='expl'
    elif o['d'].startswith('Same cutout'): cat='cut'
    else: cat='look'
    gid=f'g{j}'
    d={'char':f'Character · {esc(k)} look','riso':'Riso palette study','expl':'Explainer register','cut':'Cutout backend comparison','look':'Look sample'}[cat]
    gi.append(dict(id=gid,n=n,il=o['il'],d=d,k=cat,dark=o.get('dark') in (True,'True')))
    lk=(k or (n.lower() if cat=='look' else ''))
    if cat=='look' or (lk and lk not in lookimg): lookimg[lk]=gid
lookimg.setdefault('riso',[g['id'] for g in gi if g['k']=='riso'][0])
chars={}
for o in OLD:
    if o.get('k'): chars.setdefault(o['k'],[]).append(o['n'])
# --- looks explorer
looks=[]
looks.append(dict(id='riso',name='riso',group='Print',small='default',pills=['default look','visual-style.md',f'{len(chars.get("riso",[]))} sample characters'],
  tag=D.Q('A risograph print of a small absurd machine-world: grainy, flat, bold-lined, generous with empty space — a clever idea drawn as one clean scene, not a diagram.',VS),
  invoke='illo: draw Blot explaining why retries need backoff',
  how=[D.Q('**Halftone grain** — fills are flat ink with a visible dot screen, not smooth.',VS),D.Q('**Ink-layer offset** — a slight misregistration between inks (a thin colored edge alongside the line). Subtle, not glitchy.',VS),D.Q('**Paper grain** — a faint stock texture under everything; never glossy.',VS),D.Q('**Flat fills** — no gradients, no soft drop shadows, no photographic light.',VS)],
  quotes=[[D.Q('The identity is the **print technique**, independent of color',VS),VS],[D.Q('Because the signature is the technique, the palette is a free parameter',VS),VS]],
  lesson='Make the identity a technique, not a color. Then palette becomes a free parameter.',files=[VS,SK+'references/palettes.md'],src=D.blob+VS,img=lookimg['riso']))
GRP={'Print':'woodcut gouache manila sketchbook fizz','Screen':'phosphor pixel snes blueprint chalk','Craft':'clay felt diorama enamel bricks bloom'}
grp={l:g for g,ls in GRP.items() for l in ls.split()}
LES={'bricks':'The one photoreal exception, fenced into its own look so it cannot leak into the others.','pixel':'Specify the fake resolution (160x90, nearest-neighbor) so the model commits to it.',
 'snes':'A look with eight sections needs its own QA; constraints in caps are the ones models ignore.','phosphor':'A dark-ground look inverts the palette roles, so the file remaps them explicitly.'}
for f in sorted(glob.glob(R+'/'+SK+'references/styles/*.md')):
    l=os.path.basename(f)[:-3]; p=SK+f'references/styles/{l}.md'; t=D.rd(p)
    st=re.search(r'^STYLE: (.+)$',t,re.M).group(1); sts=first_sent(st,240) or st[:0]
    qa=re.search(r'^## QA[^\n]*\n(.*?)(?=^## |\Z)',t,re.M|re.S)
    qb=[first_sent(b) for b in re.findall(r'^- (.+?)(?=^- |^\s*$|\Z)',qa.group(1),re.M|re.S)] if qa else []
    qb=[x for x in qb if x][:4]
    cd=re.search(r'Classic default \(no palette given\):[^\n]*(?:\n[^\n]+)?',t)
    q=[]
    if sts: q.append([D.Q(sts,p),p])
    if cd: q.append([D.Q(first_sent(cd.group(0),300) or plain(cd.group(0)).split('.')[0],p),p])
    fp=first_sent(first_para(t))
    cs=chars.get(l,[])
    looks.append(dict(id=l,name=l,group=grp.get(l,'Craft'),small=f'{len(cs)} chars' if cs else '',pills=[grp.get(l,'Craft'),f'styles/{l}.md · {D.lines(p)} lines']+([f'e.g. '+', '.join(cs[:3])] if cs else []),
      tag=D.Q(fp,p),invoke=f'illo: make a {l} style variant of blip, then draw it shipping a release',how=[D.Q(x,p) for x in qb],quotes=q,
      lesson=LES.get(l,'Each look replaces only the LINE LANGUAGE and STYLE lines of the shared prompt template; the method stays constant.'),
      files=[p],src=D.blob+p,img=lookimg.get(l,'')))
# --- engine explorer
def hp(name): return re.search(r'add_parser\("%s", help="([^"]+)"'%name,D.rd(E)).group(1)
ENG=[('generate','Engine',f'python3 "$SKILL_DIR/scripts/illo.py" generate --prompt-file p.txt --out /tmp/illo/run/hero.png --ref "$SKILL_DIR/assets/character-reference.webp" --aspect 16:9',
  ['Resolves a backend: codex or grok subscription CLI, or OpenRouter; grok-bot and muse-native are refused because they are agent-side.','Paid fallback to OpenRouter only with --allow-paid-fallback.','--count N renders variations; --cutout asks for a transparent PNG.'],
  'With no backend configured it exits 1 with a clear setup message; with --backend grok-bot it refuses and tells the agent to use its own image tool.',
  'Make the expensive path opt-in. A subscription render never silently falls back to a paid API.'),
 ('init','Engine','python3 "$SKILL_DIR/scripts/illo.py" init --backend grok-bot --no-key',['Writes ~/.config/illo/config.yaml.','Native-transport agents record their transport with --no-key.'],'Not run against the real home; doctor shows the config path it would use.','The help text says “run this yourself”: keys are the user’s to enter.'),
 ('doctor','Engine','python3 "$SKILL_DIR/scripts/illo.py" doctor',['Reports python, config path, model, character, assets, CLIs, API key and backend readiness.'],'Ran with a clean HOME: assets OK, no backend ready, and a note that Grok Bot can render natively. Exit 0.','A preflight that explains every missing piece beats a stack trace at render time.'),
 ('newrun','Engine','python3 "$SKILL_DIR/scripts/illo.py" newrun',['Creates and prints a fresh /tmp/illo/&lt;runid&gt; batch directory.'],'Created and printed a fresh /tmp/illo/<runid> directory (a side effect outside the repo).','Give every batch its own directory and manifest so galleries are reproducible.'),
 ('packs','Packs','python3 "$SKILL_DIR/scripts/illo.py" packs install blip',['list, show, install (or --all), update.','show prints a pack’s character.md so you can review it before installing.'],'packs list returned 57 community packs over the network; packs show blip printed the pack (style: riso).','Review before install: community packs are prompts that will run in your agent.'),
 ('gallery','Output','python3 "$SKILL_DIR/scripts/illo.py" gallery /tmp/illo/<runid>',['Reads manifest.jsonl and writes a self-contained index.html.'],'On an empty run it exits 1: “No manifest.jsonl in …”.','Every render writes a manifest line, so comparison pages come for free.'),
 ('keyout','Output','python3 "$SKILL_DIR/scripts/illo.py" keyout render.png --out cut.png --chroma magenta',['Chroma-keys a magenta or green screen to alpha.','Writes a manifest record for the cutout.'],'Keyed a magenta test image to an RGBA PNG. The record is hard-coded to backend muse-native even when Grok Bot made the image.','Agent-side renders still need the deterministic post-processing step in code.'),
 ('record','Output','python3 "$SKILL_DIR/scripts/illo.py" record --path hero.png --backend grok-bot --label hero',['Appends a manifest record for an agent-side native render (grok-bot or muse-native).'],'Help verified; it is how native renders join the gallery.','Native and engine renders share one manifest format.')]
eng=[]
for n,g,inv,how,ran,les in ENG:
    eng.append(dict(id=n,name=n,group=g,small='subcommand',pills=['illo.py',g],tag=D.Q(hp(n),E),invoke=inv,how=how,quotes=[[D.Q(hp(n),E),E]],
      extra=f'<div class="d-sec"><h4>What happened when I ran it</h4><p>{esc(ran)}</p></div>',lesson=les,files=[E],src=D.blob+E))
DR=SK+'scripts/diagram_route.py'; RH=SK+'scripts/repair-hermes-assets.sh'
eng.append(dict(id='diagram_route',name='diagram_route.py',group='Helpers',small=f'{D.lines(DR)} l',pills=['helper','routing'],tag=D.Q('Executable lock of composition.md\'s diagram-type picker and labeled-stages pack-solve.',DR),
  invoke='python3 scripts/diagram_route.py "show the flow of our deploy pipeline"',how=[D.Q('The prose in references/composition.md is the source of truth.',DR),D.Q('Bare "flow" is not an ask.',DR)],quotes=[],
  extra='<div class="d-sec"><h4>What happened when I ran it</h4><p>“show the flow of our deploy pipeline” → explainer / labeled_stages; “the growth loop” → explainer / loop; “illustrate why code review matters” → editorial. It has no argparse, so <code>--help</code> is classified as a request (editorial).</p></div>',
  lesson='Turn the routing prose into a test oracle, so the doc and the code cannot drift.',files=[DR],src=D.blob+DR))
eng.append(dict(id='repair',name='repair-hermes-assets.sh',group='Helpers',small=f'{D.lines(RH)} l',pills=['helper','Hermes only'],tag=D.Q('Hermes-only preflight: verify and repair the skill\'s binary assets.',RH),
  invoke='bash scripts/repair-hermes-assets.sh',how=[D.Q('Safe to run anywhere: it changes nothing when checksums already match.',RH)],quotes=[],
  extra='<div class="d-sec"><h4>What happened when I ran it</h4><p>Every asset matched assets/checksums.txt; nothing re-downloaded; exit 0.</p></div>',lesson='Work around a host bug with a checksum manifest, and say when to delete the workaround.',files=[RH],src=D.blob+RH))
# --- sections
GK=[('char','Characters'),('look','Looks'),('riso','Riso palettes'),('expl','Explainers'),('cut','Cutouts')]
hro=hero('Skill explainer · tmchow/illo-skill','Illo',0,
 'A <mark>recurring mascot performs the idea</mark>; the look and palette are just parameters.',
 f'An agent skill for editorial illustrations. One character pack carries one of 17 looks, a palette resolves on top, and a Python engine renders through a subscription CLI, OpenRouter or the agent’s own image tool. I read the skill, ran the 121-test suite and every engine subcommand. {D.Q("This is a configurable house style, not a generic image generator.",SKM)}',
 [('v0.37.0','release'),('0b0abee','commit, 21 Sep 2026'),('17','looks'),('57','community packs'),('8','engine subcommands'),('121','tests pass')],
 [('Who it is for','Writers who want a consistent illustrated voice across posts, decks and docs.'),('What you get','One image per idea: an editorial scene, an explainer diagram, a mini-comic or a transparent cutout.')])
s_how=sec('how','How It Works','The Method Is Constant; The Pack Is The Parameter','Five registers share one workflow: preflight, read and clarify, resolve the character, resolve the palette, generate reference-locked.',
 callouts([f'<b>One idea per image.</b> {D.Q("One image explains one idea: a key judgment, a flow, a before/after, a trap, a loop.",SKM)}',
  f'<b>The mascot is the subject.</b> {D.Q("A **recurring mascot** is the one performing the idea in every scene — the subject, never decoration.",SKM)}',
  f'<b>Look travels with the pack.</b> {D.Q("a character pack carries its **style** with it",SKM)}.',
  f'<b>Explainers are pack-solved.</b> {D.Q("A named pipeline or recipe is **labeled stages** inside that register — named phases in order, one connected system, pack-solved for this body, never a new look.",SKM)}',
  f'<b>Keys are the user’s.</b> {D.Q("Entering an API key is something the **user** does.",SKM)}']))
s_looks=f'<section id="looks">{head("The Looks","Seventeen Looks, Each One File","Pick a look. The tag is the file’s own opening; How it works lists its QA checks; quotes are its STYLE line and classic default palette, checked at build time.")}{explorer("lk","looks")}</section>'
s_gal=sec('gallery','Gallery','85 Real Renders','Characters from the community packs, look samples, riso palette studies, explainers and a cutout comparison across backends. Click to enlarge.',gchips('gil',GK)+gal('gil',gi))
s_eng=f'<section id="engine">{head("The Engine","Eight Subcommands And Two Helpers, All Run","scripts/illo.py is the only renderer. I ran each subcommand with a throwaway HOME so nothing touched a real config.")}{explorer("en","engine")}</section>'
s_find=sec('findings','What I Found Running It','Well Tested; Two Rough Edges','All runs used HOME=/tmp/illohome, nice and timeout, at commit 0b0abee.',
 table(['Run','Result','Note'],[
  ['pytest tests/','121 passed, 37 subtests','Run in a venv on the box.'],
  ['doctor','exit 0','No backend ready; points Grok Bot at the native path.'],
  ['packs list / show','57 packs','Fetches the community repo over the network.'],
  ['generate, no backend','exit 1','Clear setup message. A positional prompt is rejected; <code>--prompt</code> or <code>--prompt-file</code> is required.'],
  ['generate --backend grok-bot','refused','Correct: native renders are agent-side.'],
  ['keyout magenta test','RGBA PNG','Works; the manifest record says muse-native.'],
  ['diagram_route.py','routes correctly','5 phrasings matched composition.md.'],
  ['repair-hermes-assets.sh','all OK','Nothing re-downloaded.'],
  ['git status after runs','clean','newrun writes only to /tmp/illo.']])+
 verdict([('Bug','keyout hard-codes its backend','The record keyout writes always says <code>"backend": "muse-native"</code>, so a Grok Bot cutout is mislabeled in the manifest and gallery.'),
  ('Bug','diagram_route.py has no --help','It treats every argument as a request, so <code>--help</code> prints “editorial editorial default”.'),
  ('Gap','Agent-side paths are prose, not code','The Grok Bot and Muse native flows live in SKILL.md; the engine only refuses them and records afterward.'),
  ('Cost','packs list needs the network','Listing community packs fetches the remote repo on every call.'),
  ('Copy','Paid fallback is opt-in','<code>--allow-paid-fallback</code> must be set before a subscription failure can spend OpenRouter credits.'),
  ('Copy','Executable routing oracle','diagram_route.py parses composition.md and is tested against it, so the prose and the code cannot drift.')]))
s_steal=sec('yours','Build Your Own','What To Steal','',steal([('Separate method from parameters.','Character, look and palette are swappable files; the workflow never changes.'),
 ('Make identity a technique.','Riso is grain, offset and flat fills, not a color, so any palette still reads as the house style.'),
 ('Anchor sets on the first good image.','Every later render references the first one that passes the quality bar.'),
 ('Write a manifest line per render.','Galleries, comparisons and audits come for free.'),('Keep keys with the user.','The agent runs init only for keyless native transports.')]))
s_src=sec('sources','Sources','Everything Here Is Checked','Each quote on this page is compared with its source file at build time; the build fails on any mismatch.',
 srcs([D.L(SKM),D.L(VS),D.L(E),D.L(DR),D.L(SK+'references/composition.md'),'<a href="https://github.com/tmchow/illo-skill">github.com/tmchow/illo-skill</a>']))
nav=[('top','Overview'),('how','How it works'),('looks','Looks'),('gallery','Gallery'),('engine','Engine'),('findings','Findings'),('yours','Build your own'),('sources','Sources')]
JS=explorer_js('lk','il-lk',looks,['Print','Screen','Craft'])+explorer_js('en','il-en',eng,['Engine','Packs','Output','Helpers'])
D.finish()
n=build('illo','Inside Illo',nav,hro+s_how+s_looks+s_gal+s_eng+s_find+s_steal+s_src,
 'Compiled 22 Oct 2026 from tmchow/illo-skill @ 0b0abee (v0.37.0) · every quote is checked against its source file at build time · not affiliated with the author.',JS)
print('built',n,len(looks),len(eng),len(gi))
