# Builds site/pstack/index.html from the pstack source tree plus the per-item data in pstack_data/.
import sys,os,re,glob,json,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from shell import page, esc, code
from explorer import explorer, data_js
from config import src, out, BUILD
SRC=src('PSTACK_SRC'); PS=SRC+'/pstack'; DD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'pstack_data')
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True,cwd=SRC).stdout.strip()
H=sh('git rev-parse HEAD'); h7=H[:7]; VER=json.load(open(PS+'/plugin.json'))['version']
HDATE=sh('git log -1 --format=%cs')
GH=f'https://github.com/cursor/plugins/blob/{h7}/pstack/'; GT=f'https://github.com/cursor/plugins/tree/{h7}/pstack/'
def L(p,t=None): return f'<a href="{GH}{p}">{t or esc(p)}</a>'
def rd(p): return open(os.path.join(PS,p)).read()
def norm(s): return re.sub(r'\s+',' ',s).strip()
def wc(p): return int(subprocess.run(['wc','-w',os.path.join(PS,p)],capture_output=True,text=True).stdout.split()[0])
BAD=[]
def check(q,path):
    if norm(q) not in norm(rd(path)): BAD.append((path,q))
    return q
def md(s):  # escape, then render `code` spans the way the source writes them
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',esc(s))
def load(f):
    ns={}; exec(open(os.path.join(DD,f)).read(),ns); return ns
# ---------- skills ----------
S=[];A=[]
for f in sorted(glob.glob(DD+'/s*.py'),key=lambda x:int(re.findall(r'\d+',os.path.basename(x))[0])):
    ns=load(os.path.basename(f)); S+=ns['S']; A=ns.get('A',A)
CATS={'entry':'Entry and setup','understand':'Understand','build':'Design and build','verify':'Review and verify','write':'Writing','learn':'Learning loop','agent':'Subagents'}
skill_dirs=sorted(d for d in os.listdir(PS+'/skills') if not d.startswith('principle-'))
assert sorted(s['id'] for s in S)==skill_dirs, set(skill_dirs)^{s['id'] for s in S}
DMI={}
for d in os.listdir(PS+'/skills'):
    fm=rd(f'skills/{d}/SKILL.md').split('---')[1]; DMI[d]='disable-model-invocation: true' in fm
for s in S:
    p=f'skills/{s["id"]}/SKILL.md'; s['words']=wc(p)
    s['files']=sorted(os.path.relpath(os.path.join(r,f),PS+'/skills/'+s['id']) for r,_,fs in os.walk(PS+'/skills/'+s['id']) for f in fs)
    s['rules']=[md(check(q,p)) for q in s['rules']]; s['dmi']=DMI[s['id']]; s['src']=GT+'skills/'+s['id']
    assert s['cat'] in CATS and 4<=len(s['how'])<=6 and 2<=len(s['rules'])<=4, s['id']
for a in A:
    a.update(cat='agent',isAgent=True,words=wc(a['file']),files=[a['file']],src=GH+a['file'],invoke='')
    a['rules']=[md(check(q,a['file'])) for q in a['rules']]
ALL=S+A
# ---------- playbooks ----------
pb=load('playbooks.py'); PB={}
for key,label,ids in pb['G']:
    for i in ids:
        p=f'skills/poteto-mode/playbooks/{i}.md'; t=rd(p); b=pb['B'][i]
        st=re.search(r'\*\*(You own[^*]*)\*\*',t); rp=re.search(r'^\*\*Reply:\*\*\s*(.+)$',t,re.M)
        PB[i]=dict(id=i,group=label,words=wc(p),steps=b['steps'],quotes=[md(check(q,p)) for q in b['quotes']],
                   stance=md(st.group(1)) if st else '',reply=md(rp.group(1)) if rp else '')
pb_files=sorted(f[:-3] for f in os.listdir(PS+'/skills/poteto-mode/playbooks') if f.endswith('.md'))
assert sorted(PB)==pb_files
PBG=[[label,ids] for _,label,ids in pb['G']]
# ---------- principles ----------
pr=load('principles.py'); TEST,STUBS=pr['P'],pr['STUBS']
idx=rd('skills/poteto-mode/SKILL.md').split('## Principles',1)[1]
idx=re.split(r'\n## ',idx)[0]; PR=[]; grp=None
for line in idx.splitlines():
    g=re.match(r'^\*\*(\w+)\*\*\s*$',line)
    if g: grp=g.group(1); continue
    m=re.match(r'^- \*\*(.+?)\.\*\*(?: \(\*\*principle-([a-z-]+)\*\*\)\.)?\s*(.+)$',line) or re.match(r'^- \*\*(.+?)\*\* \(\*\*principle-([a-z-]+)\*\*\)\.\s*(.+)$',line)
    if not m: continue
    name,leaf,rest=m.group(1).rstrip('.'),m.group(2),m.group(3)
    leaf=leaf or re.sub(r'[^a-z0-9-]','',name.lower().replace(' ','-'))
    when,_,rule=rest.partition('. ')
    PR.append(dict(group=grp,leaf=leaf,name=name,when=when+'.',rule=rule,test=md(check(TEST[leaf],f'skills/principle-{leaf}/SKILL.md')),words=wc(f'skills/principle-{leaf}/SKILL.md'),stub=STUBS.get(leaf)))
pdirs=sorted(d[10:] for d in os.listdir(PS+'/skills') if d.startswith('principle-'))
assert sorted(p['leaf'] for p in PR)==pdirs==sorted(TEST), set(pdirs)^{p['leaf'] for p in PR}
# ---------- verified facts ----------
NSK=len(os.listdir(PS+'/skills')); NDMI=sum(DMI.values()); NOT_DMI=[k for k,v in DMI.items() if not v]
NCOMMITS=int(sh('git log --oneline -- pstack | wc -l')); FIRST=sh("git log --reverse --format=%cs -- pstack | head -1")
NAUTH=int(sh("git log --format=%an -- pstack | grep -c '^lauren$'"))
SLOC=int(sh("find pstack/skills -path '*scripts*' -type f \\( -name '*.ts' -o -name '*.mjs' -o -name '*.sh' \\) -not -name '*.test.ts' -not -path '*node_modules*' | xargs cat | wc -l"))
TLOC=int(sh("find pstack/skills -type f -name '*.test.ts' -not -path '*node_modules*' | xargs cat | wc -l"))
RUNS=json.load(open(DD+'/runs.json'))
MODELS=re.findall(r'^([a-z][a-z ,/-]+): ((?:claude|grok)[^\n]*)$',rd('skills/setup-pstack/SKILL.md'),re.M)
assert len(MODELS)==17, len(MODELS)
NRULE=len(re.findall(r'^\| \d+ \|',rd('skills/unslop/SKILL.md'),re.M))
small=min((p for p in PR if not p['stub']),key=lambda p:p['words'])
# ---------- quote checks for prose sections ----------
README='README.md'; G2='docs/guide/02-poteto-mode.md'; G7='docs/guide/07-overnight.md'
Q=lambda q,p: md(check(q,p))
# ---------- sections ----------
def head(i,eyebrow,h2,p=''): return f'<div class="sec-head"><div class="eyebrow">{eyebrow}</div><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}</div>'
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A research report · pstack v{VER} · cursor/plugins @ {L("",h7)} ({HDATE}) · compiled 22 Oct 2026</div>
<h1><span class="p">p</span>stack</h1>
<p class="thesis">“<mark>{Q("if you want to go fast, go deep first.",README)}</mark>”</p>
<p class="lede">pstack is the pack of agent skills Lauren Tan (poteto) ships in <code>cursor/plugins</code> under the MIT license. One router skill, <code>/poteto-mode</code>, picks a playbook for the task and pulls in the other skills as each step needs them. The README states the aim: “{Q("pstack helps you write less, but higher quality code.",README)}” This report reads every SKILL.md, playbook and agent file at commit {h7}, runs the pack’s own scripts and checks, and explains how each piece is built and which parts are worth reusing.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>{len(S)}</b><span>command skills</span></div>
<div class="fact" role="listitem"><b>{len(PR)}</b><span>one-rule principles</span></div>
<div class="fact" role="listitem"><b>{len(PB)}</b><span>playbooks in the router</span></div>
<div class="fact" role="listitem"><b>{len(A)}</b><span>subagent definitions</span></div>
<div class="fact" role="listitem"><b>{SLOC/1000:.1f}k</b><span>lines of script code, plus {TLOC/1000:.1f}k of tests</span></div>
<div class="fact" role="listitem"><b>{NCOMMITS}</b><span>commits since {FIRST}</span></div></div>
<div class="where">
<div class="note"><h4>Where it lives</h4><p>The public copy is <code>cursor/plugins/pstack</code>. It installs in Cursor with <code>/add-plugin pstack</code>, and in Claude Code from a generated <code>harness/pstack/</code> tree (<code>/plugin install pstack@cursor-plugins</code>). Of the {NCOMMITS} commits touching <code>pstack/</code>, {NAUTH} are authored as “lauren”.</p></div>
<div class="note"><h4>What a skill is here</h4><p>A folder with a <code>SKILL.md</code> (YAML frontmatter plus Markdown), sometimes with <code>references/</code> and <code>scripts/</code>. {NDMI} of the {NSK} skills set <code>disable-model-invocation: true</code>; the exception is <code>/{NOT_DMI[0]}</code>. Nothing loads because a word in a prompt matched.</p></div>
<div class="note"><h4>No planning skill, on purpose</h4><p>The README: “{Q("personally, i don't believe in planning. the best spec is code.",README)}” Planning lives in Cursor’s plan mode and in the multi-phase-plan playbook, not in a default step.</p></div></div></header>'''
svg='''<div class="figure"><svg viewBox="0 0 1000 300" role="img" aria-labelledby="mT"><title id="mT">pstack: prompt to router to playbook to workflow skills, subagents and principles, then proof and a PR</title>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="115" width="150" height="70" rx="8"/><text class="t" x="24" y="143">Your prompt</text><text class="tm" x="24" y="165">goal + done check</text>
<rect class="bx-hot" x="200" y="115" width="170" height="70" rx="8"/><text class="t" x="214" y="143">/poteto-mode</text><text class="tm" x="214" y="165">router + principle index</text>
<rect class="bx-skin" x="410" y="115" width="160" height="70" rx="8"/><text class="t" x="424" y="143">1 of 23 playbooks</text><text class="tm" x="424" y="165">steps → todo list</text>
<rect class="bx" x="610" y="20" width="200" height="70" rx="8"/><text class="t" x="624" y="48">workflow skills</text><text class="tm" x="624" y="70">how · architect · arena · swarm</text>
<rect class="bx" x="610" y="115" width="200" height="70" rx="8"/><text class="t" x="624" y="143">subagents per role</text><text class="tm" x="624" y="165">pstack-models.mdc</text>
<rect class="bx" x="610" y="210" width="200" height="70" rx="8"/><text class="t" x="624" y="238">principle leaves</text><text class="tm" x="624" y="260">read in full when applied</text>
<rect class="bx-hot" x="850" y="115" width="140" height="70" rx="8"/><text class="t" x="864" y="143">Proof → PR</text><text class="tm" x="864" y="165">opening-a-pr</text>
<path class="ar" d="M160 150 H198" marker-end="url(#m1)"/><path class="ar" d="M370 150 H408" marker-end="url(#m1)"/>
<path class="ar" d="M570 140 L608 60" marker-end="url(#m1)"/><path class="ar" d="M570 150 H608" marker-end="url(#m1)"/><path class="ar" d="M570 160 L608 240" marker-end="url(#m1)"/>
<path class="ar" d="M810 55 L848 135" marker-end="url(#m1)"/><path class="ar" d="M810 150 H848" marker-end="url(#m1)"/><path class="ar-d" d="M810 245 L848 165" marker-end="url(#m1)"/></svg></div>'''
smap=f'''<section id="map">{head("map",L("skills/poteto-mode/SKILL.md","poteto-mode/SKILL.md"),"One router, many playbooks, a small set of multi-agent workflows","A prompt names a goal and a check that can pass or fail. The router picks a playbook and copies its steps into the todo list. Those steps call workflow skills, which fan out to subagents on the model assigned to each role. Principles constrain the choices, and nothing counts as done until it is proven on the real artifact.")}{svg}
<p class="figcap">Subagents spawned inside playbook steps run as <code>poteto-agent</code>, which loads poteto-mode first. Panels (arena, architect, interrogate) run one subagent per model listed for the role.</p></section>'''
pf=f'skills/principle-{small["leaf"]}/SKILL.md'
anat=f'''<section id="anatomy">{head("anatomy","Anatomy of a skill","How the files are shaped","A few strict conventions carry most of the design. They are the part to copy into another pack.")}
<div class="twocol"><div class="codecard"><span class="c"># the entire {esc(pf)} ({small["words"]} words, the shortest non-stub principle)</span>
{esc(rd(pf).strip())}</div>
<div class="callouts">
<div class="callout"><span class="n">1</span><p><b>The name is the folder.</b> The frontmatter <code>name</code> matches the directory, and other files cite a principle as <code>principle-&lt;name&gt;</code> instead of pasting it.</p></div>
<div class="callout"><span class="n">2</span><p><b>The description carries the trigger.</b> Principles open with “Apply when…”, so the router’s index can quote the trigger and the rule in one line.</p></div>
<div class="callout"><span class="n">3</span><p><b>Explicit invocation only.</b> {NDMI} of {NSK} SKILL.md files set <code>disable-model-invocation: true</code>. A skill runs when typed or when a playbook step reads it by path.</p></div>
<div class="callout"><span class="n">4</span><p><b>Orchestrators delegate to references.</b> Multi-agent skills keep subagent prompts in <code>references/</code>, one file per receiving role. The Files list in each explorer entry below is computed from the tree.</p></div></div></div></section>'''
sk=f'''<section id="skills">{head("skills",f"skills/* · {len(S)} commands + {len(A)} agents","Every command is a folder with one SKILL.md","Pick a skill to see how to call it, how it works, a few lines quoted from its file, its files and the design lesson. Word counts are <code>wc -w</code> of the SKILL.md at this commit.")}
{explorer("skill","skills")}</section>'''
spb=f'''<section id="playbooks">{head("playbooks","skills/poteto-mode/playbooks/ · 23","Each playbook is a stance, numbered steps and a reply contract","The router copies a playbook’s steps into the todo list verbatim. Steps here are paraphrased; stances, quotes and Reply lines are copied from the files.")}
{explorer("pb","playbooks")}
<div class="note" style="margin-top:16px"><h4>Who may merge</h4><p>Re-checked at {h7}. Babysit never merges: “{Q("Babysitting never authorizes merging.","skills/poteto-mode/playbooks/babysit.md")}” Shipping lands on request, bottom-up, one PR at a time. Autopilot-full owners merge only what the swarm verified: “{Q("The owner merges only what you verified, tested on the trunk it lands on.","skills/poteto-mode/playbooks/autopilot-full.md")}” Autopilot-stack owners never “{Q("retarget, merge, close a PR, or arm auto-merge","skills/poteto-mode/playbooks/autopilot-stack.md")}”.</p></div></section>'''
GN={'Core':'how to think','Architecture':'how to shape code','Verification':'how to know it works','Delegation':'how to use agents','Meta':'how to improve the system'}
pc=''
for g in GN:
    lst=[p for p in PR if p['group']==g]
    pc+=f'<div class="gname"><h3>{g}</h3><span>{len(lst)} · {GN[g]}</span></div><div class="pgrid">'
    for p in lst:
        stub=f'<span class="stub" title="Leaf trimmed to a fragment by {esc(p["stub"])}">stub</span>' if p['stub'] else ''
        pc+=f'<article class="pcard"><h4>{L("skills/principle-"+p["leaf"]+"/SKILL.md",esc(p["name"]))}{stub}</h4><p class="when">{md(p["when"])}</p><p>{md(p["rule"])}</p><p class="test">{p["test"]}</p></article>'
    pc+='</div>'
spr=f'''<section id="principles">{head("principles",f"skills/principle-* · {len(PR)}",f"{len(PR)} rules, one per file","Each card gives the trigger and rule from the router’s index, then a line from the leaf file that works as the test. Cards marked stub point at leaves that were cut down to a fragment (see the findings).")}{pc}</section>'''
mrows=''.join(f'<tr><td>{esc(r)}</td><td><code>{esc(m)}</code></td></tr>' for r,m in MODELS)
smod=f'''<section id="models">{head("models",L("skills/setup-pstack/SKILL.md","setup-pstack/SKILL.md"),"Assign each role the model that suits it","<code>/setup-pstack</code> writes one line per role into <code>~/.cursor/rules/pstack-models.mdc</code> (an always-apply rule for every project). Fast Grok models do the reading and mechanical edits; Opus judges, writes and takes the hardest work; panels list both families.")}
<div class="tablewrap"><table class="dense"><thead><tr><th>Role line</th><th>Default</th></tr></thead><tbody>{mrows}</tbody></table></div>
{code("/add-plugin pstack                      # Cursor\n/plugin marketplace add cursor/plugins  # Claude Code\n/plugin install pstack@cursor-plugins","Install, then run /setup-pstack once.")}
<div class="note"><h4>Stale defaults</h4><p>A rule file written before a default changed still pins the old model. A rerun keeps roles set to something other than the default, so delete stale lines (or the file) and run <code>/setup-pstack</code> again.</p></div></section>'''
sc=f'''<section id="scripts">{head("scripts","skills/*/scripts · run on the box 22 Oct 2026","The rules that run as code",f"About {SLOC/1000:.1f}k lines of Bun, TypeScript, Node and shell, with {TLOC/1000:.1f}k lines of tests. Each script turns a rule the agent could forget into a check that exits non-zero.")}
<div class="tablewrap"><table class="dense"><thead><tr><th>Script</th><th>Used by</th><th>What it enforces (verified)</th></tr></thead><tbody>
<tr><td>{L("skills/poteto-mode/scripts/check-plan.mjs","<code>check-plan.mjs</code>")}</td><td>multi-phase-plan</td><td>Lints a plan file against the required skeleton. Exits 1 when it finds problems and 2 on bad usage.</td></tr>
<tr><td><code>scripts/watch-pr/</code></td><td>babysit, shipping</td><td>Polls a PR and returns a typed verdict. Exit codes in <code>policy.ts</code>: 0 ready or complete, 2 merge conflicts, 3 review threads, 4 failing checks, 6 merge gate, 7 query failure, 5 timeout.</td></tr>
<tr><td><code>scripts/orch/</code></td><td>orchestrate</td><td>File-backed state for the coordinator, “{Q("one command in and one line out","skills/poteto-mode/playbooks/orchestrate.md")}”. “{Q("The CLI never spawns, waits, or wakes anything.","skills/poteto-mode/playbooks/orchestrate.md")}”</td></tr>
<tr><td>{L("skills/poteto-mode/scripts/worktree-audit.sh","<code>worktree-audit.sh</code>")}</td><td>worktree-cleanup</td><td>Read-only table (SIZE AGE MERGED DIRTY REMOTE PR LAST_CHAT BUCKET) sorting worktrees into hold-wip, hold-open-pr, verify-recent-chat, safe and review. Without <code>-b</code> it warns and uses origin/main. “{Q("The bucket is advice, not permission.","skills/poteto-mode/playbooks/worktree-cleanup.md")}”</td></tr>
<tr><td>{L("skills/show-me-your-work/scripts/log.sh","<code>log.sh</code>")}</td><td>show-me-your-work</td><td>Appends a timestamped TSV row. In a test run it stripped tabs inside cells and prefixed <code>=cmd</code> with <code>'</code>, blocking spreadsheet formula injection.</td></tr>
<tr><td>{L("skills/poteto-mode/scripts/bootstrap.ts","<code>bootstrap.ts</code>")}</td><td>watch-pr, orch</td><td>Installs the scripts’ dependency keyed on <code>package.json</code> and <code>bun.lock</code>.</td></tr></tbody></table></div>
<div class="note"><h4>Test results</h4><p>{RUNS["bun"]}</p></div></section>'''
drv=f'''<section id="driving">{head("driving",L("docs/guide/02-poteto-mode.md","docs/guide")+" · poteto-help/references/prompting.md","Short prompts with a check that can pass or fail","The guide says a prompt carries up to five things, each one sentence long.")}
<ol class="steal"><li><p><b>The goal.</b> What is wrong, or what is wanted.</p></li><li><p><b>The done check.</b> “{Q("It must be able to pass or fail.",G2)}” “{Q('"Make it better" and "work on it for an hour" aren\'t checks.',G2)}”</p></li><li><p><b>The proof.</b> Real command output, a video, the stored value, or a before-and-after number.</p></li><li><p><b>What is already known.</b> A symptom, repro step, log line or link.</p></li><li><p><b>Real constraints.</b> “repro first”, “don't change any code yet”, “zero behavior change”.</p></li></ol>
{code("/poteto-mode the csv export drops its last row since yesterday's deploy. failing job id is 4812. repro first, then fix. done means the 60k-row fixture exports every row. show me the row counts before and after.","All five in one prompt, from docs/guide/02-poteto-mode.md.")}
<p>Two things stay out: a list of skills, because “{Q("a hand-written sequence usually reorders or drops steps the playbook would have kept",G2)}”, and a theory of the cause, because “{Q("A stated guess narrows the search to wherever you pointed.",G2)}”</p>
{code("/poteto-mode im going to bed. migrate every caller to the new parser in a fresh worktree off <base>.\ndone means zero old callers, all parser fixtures pass, old api deleted.\nkeep a decision log. don't ask me before committing.\n/loop until done. if you're truly stuck after a few hours, stop and write up why.","The overnight contract, from docs/guide/07-overnight.md.")}
<blockquote class="pull"><p>“{Q("A loop you don't trust just produces unchecked work faster, and the mess compounds with every iteration.",G7)}”</p><cite>docs/guide/07-overnight.md, “Earn the trust before the loop”</cite></blockquote></section>'''
FIND=RUNS['findings']
fnd=f'''<section id="findings">{head("findings",f"Checked on the box at {h7}","Where the docs and the code disagree","Gaps found while reading every file, plus the results of the repo’s own consistency checks.")}<div class="callouts">'''+''.join(f'<div class="callout"><span class="n">{i+1}</span><p>{x}</p></div>' for i,x in enumerate(FIND))+'</div></section>'
ver=f'''<section id="verdict">{head("verdict","An assessment","Strong ideas that travel, an orchestration that costs","A reading of the files and history, not a benchmark.")}
<div class="where">
<div class="note"><h4><span class="verdict v-good">Copy</span> Evidence at every step</h4><p>Replies label claims, playbooks end in proof on the real artifact, and scripts such as watch-pr and check-plan exit non-zero instead of trusting prose.</p></div>
<div class="note"><h4><span class="verdict v-good">Copy</span> The author is never the critic</h4><p>Comment Sicko, cross-family arena judges and the swarm that “never wrote the code” separate building from reviewing.</p></div>
<div class="note"><h4><span class="verdict v-good">Copy</span> Skills get shorter</h4><p>The history is full of cut passes (#419, #538, #571). The shortest non-stub principle is {small["words"]} words.</p></div>
<div class="note"><h4><span class="verdict v-cost">Cost</span> Tokens and ceremony</h4><p>Panels, swarms and cross-model reviews multiply model calls, and the playbooks are heavy for small changes even with <code>skip: &lt;reason&gt;</code>.</p></div>
<div class="note"><h4><span class="verdict v-cost">Cost</span> Prose only guides</h4><p>Outside the scripts, every rule depends on the model following text. The cut passes also leave fragments behind (see the stubs).</p></div>
<div class="note"><h4><span class="verdict v-port">Port</span> One person’s stack</h4><p>Defaults assume Opus 5.5 plus Grok 4.7, GitHub or Origin, and Bugbot. <code>/automate-me</code> exists to draft a personal mode instead.</p></div></div></section>'''
yours=f'''<section id="yours">{head("yours","Build your own","What to copy first","Ordered by payback for effort, judged from which skills the rest of the pack depends on.")}
<ol class="steal">
<li><p><b>A scripted way to prove behavior per app.</b> <code>/create-verification-skill</code> is what “verified” means everywhere else in the pack.</p></li>
<li><p><b>Reply rules that demand evidence.</b> Failing-then-passing output pasted verbatim, and claims labeled.</p></li>
<li><p><b>Author and critic in separate agents.</b> Start with a comment-stripping critic and a judge who never sees model names.</p></li>
<li><p><b>One router, small playbooks.</b> A stance line, numbered steps copied into todos, and a <code>Reply:</code> contract.</p></li>
<li><p><b>Turn repeated corrections into structure.</b> <code>/correct</code>’s ladder: architecture, then types or lint, then a test, then docs.</p></li>
<li><p><b>Explicit-only skills with the rule in the description.</b> <code>disable-model-invocation: true</code> plus “Apply when…”.</p></li>
<li><p><b>Prune and re-test.</b> Delete instructions the current model follows unprompted, then check the stubs that pruning leaves.</p></li></ol></section>'''
TL=[("23 May 2026","24bd6eb","“Add pstack plugin” lands in cursor/plugins."),("26 May – 13 Jun","#86–#133","Versions 0.2 to 0.9.1; per-role models via <code>/setup-pstack</code> (#121); the hillclimb playbook."),("Jul","#147–#178","model-the-domain principle; create- and maintain-verification-skill (#150); a parity sweep with the private skill tree (#156); the swarm skill."),("1–2 Aug","0.13, 0.14","Autopilot playbooks, <code>/no-comments</code> with Comment Sicko, <code>/technical-writing</code>, bro, babysit, shipping, orchestrate and worktree-cleanup."),("7 Sep","#333","0.15.0. Defaults move to Opus 5.5 and Grok 4.7 on 22 Sep (#414); #419 cuts “19 more instructions Opus 5.5 does not need”."),("3–14 Oct","#494–#617","<code>/correct</code>, <code>/poteto-help</code>, <code>/ketchup</code>; Sol dropped (#511); distill pass (#538); #571 cuts sections from seven skills."),("18–19 Oct","#710–#729","0.15.26 to 0.15.29: formal verification skills, Claude Code harness, <code>/sharpen</code> restored to its original prompt."),("21 Oct","eb4db2b · #741",f"0.15.30 adds <code>/statechart</code>, which draws TLA+ models as charts.")]
hist=f'''<section id="history">{head("history",f"git log -- pstack · {NCOMMITS} commits","How it got here")}
<ol class="timeline">'''+''.join(f'<li><b>{d}</b> <span class="mono">{c}</span><p>{t}</p></li>' for d,c,t in TL)+'</ol></section>'
srcs=f'''<section id="sources">{head("sources","Sources","Where to read further")}<ol class="srcs">
<li>{L("README.md","README")} and {L("docs/guide/README.md","the ten-chapter guide")}</li>
<li>{L("skills/poteto-mode/SKILL.md","poteto-mode SKILL.md")} and {L("skills/poteto-mode/playbooks/investigation.md","the playbooks folder")}</li>
<li>{L("skills/poteto-help/references/prompting.md","poteto-help prompting reference")}</li>
<li>{L("skills/automate-me/SKILL.md","/automate-me")}, for drafting a personal mode</li>
<li>Upstream tree: <a href="{GT}">github.com/cursor/plugins/tree/{h7}/pstack</a></li></ol></section>'''
nav=[('top','Overview'),('map','How it fits'),('anatomy','Anatomy'),('skills','Skills'),('playbooks','Playbooks'),('principles','Principles'),('models','Models'),('scripts','Scripts'),('driving','Prompting'),('findings','Findings'),('verdict','Assessment'),('yours','Build your own'),('history','History'),('sources','Sources')]
JSX=data_js('SKILLS',ALL)+data_js('CATS',CATS)+data_js('PLAYBOOKS',PB)+data_js('PBG',PBG)+r'''
const skById=Object.fromEntries(SKILLS.map((s)=>[s.id,s]));
makeExplorer({prefix:"skill",key:"pstack-skill",groups:Object.entries(CATS).map(([k,l])=>[l,SKILLS.filter((s)=>s.cat===k)]),
 getText:(s)=>[s.id,s.tag,...s.how,...s.rules].join(" ").replace(/<[^>]+>/g,""),
 renderItem:(s,on)=>`<button class="item" type="button" role="option" data-id="${s.id}" aria-selected="${on}"><span>${s.isAgent?"":"/"}${xesc(s.id)}</span><small>${s.isAgent?"agent":s.words+" w"}</small></button>`,
 renderDetail:(id)=>{const s=skById[id];const m=[`<span class="pill">${xesc(CATS[s.cat])}</span>`,`<span class="pill skin">${s.words} words in ${s.isAgent?xesc(s.files[0]):"SKILL.md"}</span>`];
  if(!s.isAgent)m.push(`<span class="pill">${s.dmi?"disable-model-invocation":"model-invocable"}</span>`);
  let h=`<div class="d-top"><div class="d-name">${s.isAgent?"":"/"}${xesc(s.id)}</div><div class="d-meta">${m.join("")}</div><p class="d-tag">${s.tag}</p></div>`;
  if(s.invoke)h+=`<div class="d-sec"><h4>Try it</h4><div class="invoke">${xesc(s.invoke)}</div></div>`;
  h+=`<div class="d-sec"><h4>How it works</h4><ol>${s.how.map((x)=>`<li>${x}</li>`).join("")}</ol></div>`;
  h+=`<div class="d-sec"><h4>In its own words</h4>${s.rules.map((r)=>`<p class="quote">“${r}”</p>`).join("")}</div>`;
  h+=`<div class="d-sec"><h4>Files</h4><div class="files">${s.files.map((f)=>`<code>${xesc(f)}</code>`).join("")}</div></div>`;
  h+=`<div class="d-sec"><h4>Design lesson</h4><p class="lesson">${s.lesson}</p></div>`;
  return h+`<div class="d-sec"><p style="font-size:.85rem"><a href="${s.src}">Read the source on GitHub</a></p></div>`}});
const pbGroups=PBG.map(([g,ids])=>[g,ids.map((i)=>PLAYBOOKS[i])]);
makeExplorer({prefix:"pb",key:"pstack-pb",groups:pbGroups,
 getText:(p)=>[p.id,p.stance,...p.steps,...p.quotes,p.reply].join(" ").replace(/<[^>]+>/g,""),
 renderItem:(p,on)=>`<button class="item" type="button" role="option" data-id="${p.id}" aria-selected="${on}"><span>${xesc(p.id)}</span><small>${p.words} w</small></button>`,
 renderDetail:(id)=>{const p=PLAYBOOKS[id];
  let h=`<div class="d-top"><div class="d-name">playbooks/${xesc(p.id)}.md</div><div class="d-meta"><span class="pill">${xesc(p.group)}</span><span class="pill skin">${p.words} words</span></div><p class="d-tag">${p.stance?`<b>${p.stance}</b>`:`<i>This file has no “You own…” stance line.</i>`}</p></div>`;
  h+=`<div class="d-sec"><h4>Steps (paraphrased)</h4><ol>${p.steps.map((x)=>`<li>${x}</li>`).join("")}</ol></div>`;
  h+=`<div class="d-sec"><h4>In its own words</h4>${p.quotes.map((q)=>`<p class="quote">“${q}”</p>`).join("")}</div>`;
  h+=`<div class="d-sec"><h4>Reply</h4><p class="lesson">${p.reply||"<i>No <code>**Reply:**</code> line in this file.</i>"}</p></div>`;
  return h+`<div class="d-sec"><p style="font-size:.85rem"><a href="https://github.com/cursor/plugins/blob/'''+h7+r'''/pstack/skills/poteto-mode/playbooks/${p.id}.md">Read the source on GitHub</a></p></div>`}});
'''
if BAD:
    for p,q in BAD: print('QUOTE NOT FOUND',p,repr(q[:90]))
    sys.exit(1)
foot=f'Compiled 22 Oct 2026 from cursor/plugins @ {h7} (pstack v{VER}, committed {HDATE}) · every quote is checked against its source file at build time · not affiliated with Cursor or Lauren Tan.'
html=page('Inside pstack','pstack',nav,hero+smap+anat+sk+spb+spr+smod+sc+drv+fnd+ver+yours+hist+srcs,footer=foot,extra_js=JSX)
open(out('pstack'),'w').write(html)
json.dump(dict(version=VER,commit=h7,skills=len(S),agents=len(A),playbooks=len(PB),principles=len(PR),dmi=f'{NDMI}/{NSK}',sloc=SLOC,tloc=TLOC,commits=NCOMMITS,bytes=len(html)),open(os.path.join(BUILD,'pstack_counts.json'),'w'))
print(open(os.path.join(BUILD,'pstack_counts.json')).read())
