import sys,json,re; sys.path.insert(0,'/workspace/dorothy-docs/_build')
from shell import *
D=json.load(open('/workspace/dorothy-docs/_build/pstack_desc.json'))
H='190d28736eff128ec94f502a22c7fe0c4b56cd37'; GH=f'https://github.com/cursor/plugins/blob/{H[:7]}/pstack/'
def L(p,t=None): return f'<a href="{GH}{p}">{t or p}</a>'
def sk(n): return L(f'skills/{n}/SKILL.md',f'<code>/{n}</code>')
def split(d):
    m=re.search(r'\s(Use (?:for|when|only when)|Apply (?:when|before|after|during|to))\b',' '+d)
    if d.startswith('Apply') or d.startswith('Use'):
        s=re.split(r"(?<=\.)\s",d,maxsplit=1); return (s[1] if len(s)>1 else '—', s[0])
    if m: i=m.start()-1; return d[:i].strip(), d[i:].strip()
    return d,'Type the slash command.'
G=[('Route and configure',['poteto-mode','poteto-help','setup-pstack','automate-me']),
('Understand and restate',['how','why','teach','recall','ketchup','in-your-own-words','bro','sharpen']),
('Design and fan out',['architect','arena','swarm','figure-it-out']),
('Review and verify',['interrogate','blast-radius','no-comments','correct','benchmark-checklist','tdd','create-verification-skill','maintain-verification-skill','create-formal-verification-skill','maintain-formal-verification-skill']),
('Write',['unslop','technical-writing','typescript-best-practices']),
('Long runs and learning',['show-me-your-work','reflect']),
('Grok Bot',['make-bot-ui'])]
P=[('Core',['laziness-protocol','foundational-thinking','redesign-from-first-principles','attack-the-premise','subtract-before-you-add','minimize-reader-load','outcome-oriented-execution','experience-first','exhaust-the-design-space','build-the-lever']),
('Architecture',['model-the-domain','boundary-discipline','type-system-discipline','make-operations-idempotent','migrate-callers-then-delete-legacy-apis','separate-before-serializing-shared-state']),
('Verification',['prove-it-works','fix-root-causes','sequence-verifiable-units','test-behavior-not-implementation','explain-the-number']),
('Delegation',['guard-the-context-window','never-block-on-the-human']),('Meta',['encode-lessons-in-structure'])]
assert sum(len(x) for _,x in G)==32 and sum(len(x) for _,x in P)==24
NEW={'create-formal-verification-skill','maintain-formal-verification-skill'}
def band(cls,g,n): return f'<div class="gband {cls}"><span>{g}</span><span class="gcount">{n}</span></div>'
rows=''
for g,ns in G:
    rows+=band('gb-cmd',g,len(ns))+'<div class="cards">'
    for n in ns:
        w,u=split(D[n]); rows+=f'<article class="card"><div class="ch">{sk(n)}<span class="kt kt-cmd">command</span>{"<span class=\"tag\">new</span>" if n in NEW else ""}</div><dl><dt>What</dt><dd>{esc(w)}</dd><dt>When</dt><dd>{esc(u)}</dd></dl></article>'
    rows+='</div>'
prow=''
for g,ns in P:
    prow+=band('gb-pr',g,len(ns))+'<div class="cards">'
    for n in ns:
        d=D['principle-'+n]; prow+=f'<article class="card c-pr"><div class="ch">{L(f"skills/principle-{n}/SKILL.md","<code>"+n+"</code>")}<span class="kt kt-pr">principle</span></div><dl><dt>When it applies</dt><dd>{esc(d)}</dd></dl></article>'
    prow+='</div>'
PB=[('investigation','read-only question'),('bug-fix','repro → root cause → fix'),('perf-issue','measured slowness vs baseline'),('hillclimb','one metric, hypothesis loop'),('runtime-forensics','live symptom'),('trace-forensics','captured profile'),('feature','new behavior from a data shape'),('refactoring','behavior-preserving'),('prototype','throwaway sketch decides a fork'),('visual-parity','pixel-exact UI'),('authoring-a-skill','writing a SKILL.md'),('eval','blinded skill/prompt eval'),('babysit','PR to merge-ready'),('shipping','land verified stack'),('autonomous-run','long task, no stops'),('orchestrate','multi-day coordinator'),('autopilot-full','independent PRs to merged'),('autopilot-stack','one linear stack'),('session-pickup','resume prior work'),('pause-safely','suspend cleanly'),('multi-phase-plan','phased / stacked'),('worktree-cleanup','prune worktrees'),('opening-a-pr','ends every playbook')]
pbt=band('gb-pb','All playbooks',len(PB))+'<div class="cards cards-sm">'+''.join(f'<article class="card c-pb"><div class="ch">{L(f"skills/poteto-mode/playbooks/{p}.md","<code>"+p+"</code>")}<span class="kt kt-pb">playbook</span></div><dl><dt>For</dt><dd>{d}</dd></dl></article>' for p,d in PB)+'</div>'
nav=[('top','Overview'),('tldr','TL;DR'),('why','Why it exists'),('model','Mental model'),('how','How it works'),('workflow','Workflow skills'),('principles','Principles'),('playbooks','Playbooks'),('install','Install and setup'),('examples','Examples'),('gotchas','Gotchas and findings'),('new','What\'s new'),('next','Where to go next')]
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A skill reference · pstack v0.15.29 · cursor/plugins @ {L("", H[:7])} (20 Oct 2026) · read 21 Oct 2026</div>
<h1>pstack</h1>
<p class="thesis">“if you want to go fast, go deep first.”</p>
<p class="lede">pstack is Lauren Tan’s (poteto) pack of agent skills for Cursor, MIT licensed, living in <code>cursor/plugins/pstack</code>. One router skill, <code>/poteto-mode</code>, picks a playbook for your task and pulls in the other skills and principles as its steps need them. The README’s goal: “pstack helps you write less, but higher quality code.” This page covers the tree as of the latest commit and checks its scripts by running them.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>56</b><span>SKILL.md files: 32 commands + 24 principles</span></div>
<div class="fact" role="listitem"><b>23</b><span>playbooks in <code>poteto-mode/playbooks/</code></span></div>
<div class="fact" role="listitem"><b>2</b><span>subagents: <code>poteto-agent</code>, <code>comment-sicko</code></span></div>
<div class="fact" role="listitem"><b>68</b><span>Bun tests over the router scripts, all passing on rerun</span></div>
<div class="fact" role="listitem"><b>146</b><span>commits touching <code>pstack/</code> since 23 May 2026</span></div>
<div class="fact" role="listitem"><b>18</b><span>commits since the reference’s v0.15.25 (14 Oct)</span></div>
</div></header>'''
tldr=f'''<section id="tldr"><div class="sec-head"><div class="eyebrow">TL;DR</div><h2>TL;DR</h2></div>
<ul><li>Install with <code>/add-plugin pstack</code>, run <code>/setup-pstack</code> once, then start real work with <code>/poteto-mode</code>.</li>
<li>Every one of the 56 skills sets <code>disable-model-invocation: true</code>. Nothing fires on its own: you type a slash command, or <code>/poteto-mode</code> reads a skill file by path when a step needs it.</li>
<li>Work is split by model: code delegates go to Grok (<code>grok-4.7-xhigh-fast</code>), judgment and prose go to Opus (<code>claude-opus-5-5-xhigh</code>). Panels (arena, architect, interrogate) run one subagent per listed model.</li>
<li>The rule that runs through all of it: prove it on the real artifact. Tests alone don’t count as verification.</li>
<li>New since v0.15.25: formal verification (<code>/create-formal-verification-skill</code>, <code>/maintain-formal-verification-skill</code>), a Claude Code install, a docs-vs-tree check, and a reworked <code>/sharpen</code> and <code>/ketchup</code>.</li></ul></section>'''
why=f'''<section id="why"><div class="sec-head"><div class="eyebrow">{L("README.md")}</div><h2>Why it exists</h2></div>
<p>The README begins with a complaint: “ai writes too much slop code… throughput without quality is not a goal i aspire to.” Her answer has two parts. First, go deep on one agent so you can trust its output. Second, once you trust it, run many agents in parallel (“fearless parallelism”). A model is chosen for each role because “every frontier model has its strengths and weaknesses.”</p>
<div class="note"><h4>No planning skill, on purpose</h4><p>“personally, i don’t believe in planning. the best spec is code.” Cursor’s plan mode covers planning, and <code>poteto-mode</code> has a multi-phase-plan playbook, but planning isn’t the default.</p></div></section>'''
svg='''<div class="figure"><svg viewBox="0 0 1000 300" role="img" aria-labelledby="mT"><title id="mT">pstack mental model: prompt to router to playbook to skills and principles to proof and PR</title>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="115" width="150" height="70" rx="8"/><text class="t" x="24" y="143">Your prompt</text><text class="tm" x="24" y="165">goal + done check</text>
<rect class="bx-hot" x="200" y="115" width="170" height="70" rx="8"/><text class="t" x="214" y="143">/poteto-mode</text><text class="tm" x="214" y="165">router + 24-principle index</text>
<rect class="bx-skin" x="410" y="115" width="160" height="70" rx="8"/><text class="t" x="424" y="143">1 of 23 playbooks</text><text class="tm" x="424" y="165">steps → todo list</text>
<rect class="bx" x="610" y="20" width="200" height="70" rx="8"/><text class="t" x="624" y="48">workflow skills</text><text class="tm" x="624" y="70">how · architect · arena · swarm</text>
<rect class="bx" x="610" y="115" width="200" height="70" rx="8"/><text class="t" x="624" y="143">subagents per role</text><text class="tm" x="624" y="165">pstack-models.mdc</text>
<rect class="bx" x="610" y="210" width="200" height="70" rx="8"/><text class="t" x="624" y="238">principle leaves</text><text class="tm" x="624" y="260">read in full when applied</text>
<rect class="bx-hot" x="850" y="115" width="140" height="70" rx="8"/><text class="t" x="864" y="143">Proof → PR</text><text class="tm" x="864" y="165">opening-a-pr</text>
<path class="ar" d="M160 150 H198" marker-end="url(#m1)"/><path class="ar" d="M370 150 H408" marker-end="url(#m1)"/>
<path class="ar" d="M570 140 L608 60" marker-end="url(#m1)"/><path class="ar" d="M570 150 H608" marker-end="url(#m1)"/><path class="ar" d="M570 160 L608 240" marker-end="url(#m1)"/>
<path class="ar" d="M810 55 L848 135" marker-end="url(#m1)"/><path class="ar" d="M810 150 H848" marker-end="url(#m1)"/><path class="ar-d" d="M810 245 L848 165" marker-end="url(#m1)"/>
</svg></div>'''
model=f'''<section id="model"><div class="sec-head"><div class="eyebrow">{L("skills/poteto-mode/SKILL.md")}</div><h2>Mental model</h2><p>Think of it as a router, playbooks, tools, and rules. The playbook picks the steps, the workflow skills do the heavy work through subagents, the principles constrain the choices, and nothing counts until it’s proven.</p></div>{svg}
<p class="figcap">Bundled skills resolve as <code>../&lt;name&gt;/SKILL.md</code> from the router, so the router hands its own absolute path to every <code>poteto-agent</code> prompt.</p></section>'''
how=f'''<section id="how"><div class="sec-head"><div class="eyebrow">poteto-mode “Non-negotiables”</div><h2>How it works</h2></div>
<ol><li><b>Match a playbook.</b> The router opens a todo list whose first items are the playbook’s steps, copied in word for word.</li>
<li><b>Fire triggers.</b> A nontrivial change triggers <code>how</code>. Code that crosses a function boundary triggers <code>architect</code>. A contested design triggers <code>interrogate</code>. Parallel work goes to <code>swarm</code> or <code>arena</code>. Any prose triggers <code>unslop</code>. A measured number triggers <code>benchmark-checklist</code>. Before review, <code>no-comments</code> runs. Long or unattended work triggers <code>show-me-your-work</code>.</li>
<li><b>Don’t ask what you can observe.</b> Before asking “which approach?”, the router checks whether running something would answer it. If so, it builds a sketch with the prototype playbook. Only real product or preference calls go to the human.</li>
<li><b>Cite principles.</b> The reply names each principle that changed a decision. It may cite only principles whose leaf SKILL.md it read in this session.</li>
<li><b>Prove and ship.</b> <code>check-plan.mjs</code> enforces the rule that “a PR is verified only when its unit, live, and perf boxes are all checked”. Every playbook ends with <code>opening-a-pr</code>.</li></ol>
<div class="tablewrap"><table class="dense"><thead><tr><th>Script</th><th>What it does (verified)</th></tr></thead><tbody>
<tr><td>{L("skills/poteto-mode/scripts/check-plan.mjs","<code>check-plan.mjs</code>")}</td><td>Lints a plan.md for the required sub-blocks (Depends on, Files, Build, Verify unit/live/perf, Review gate, Merge). Run with no arguments, it prints usage.</td></tr>
<tr><td><code>scripts/orch/</code>, <code>scripts/watch-pr/</code></td><td>Bun/TS for orchestrating subagents and polling PRs (the babysit cadence). Covered by 68 tests.</td></tr>
<tr><td>{L("skills/poteto-mode/scripts/worktree-audit.sh","<code>worktree-audit.sh</code>")}</td><td>A read-only audit table (SIZE, AGE, MERGED, DIRTY, REMOTE, PR, LAST_CHAT, BUCKET). It never deletes anything. Without <code>-b</code> it warns and uses origin/main.</td></tr>
<tr><td>{L("skills/show-me-your-work/scripts/log.sh","<code>log.sh</code>")}</td><td>Appends a row to the decision TSV. In my run it removed tabs inside cells and prefixed <code>=cmd</code> with <code>'</code> to block spreadsheet formula injection.</td></tr></tbody></table></div></section>'''
wf=f'''<section id="workflow"><div class="sec-head"><div class="eyebrow">skills/* · 32 commands</div><h2>Workflow skills</h2><p>The “what” and “when” text comes from each skill’s own frontmatter <code>description</code>. Click a name to open the file at this commit.</p></div>
{rows}</section>'''
pr=f'''<section id="principles"><div class="sec-head"><div class="eyebrow">skills/principle-* · 24</div><h2>Principles</h2><p>Each principle is a short rule, 9 to 34 lines long. The router groups them into the five headings below. Each one is invoked as <code>principle-&lt;name&gt;</code>.</p></div>
{prow}</section>'''
pb=f'''<section id="playbooks"><div class="sec-head"><div class="eyebrow">skills/poteto-mode/playbooks/ · 23</div><h2>Playbooks</h2></div>
{pbt}</section>'''
inst=f'''<section id="install"><div class="sec-head"><div class="eyebrow">README · {L("skills/setup-pstack/SKILL.md")}</div><h2>Install and setup</h2></div>
{code("""/add-plugin pstack                      # Cursor
/plugin marketplace add cursor/plugins  # Claude Code
/plugin install pstack@cursor-plugins   # → commands become /pstack:<name>""")}
<p><code>/setup-pstack</code> does the following:</p><ol><li>Detects which model slugs you can pass to a Task subagent.</li><li>Asks for a budget: <code>unlimited</code>=max, <code>large</code>=xhigh (the default), <code>medium</code>=high, <code>small</code>=medium.</li><li>Shows each role with its model and asks you to confirm.</li><li>Validates that every slug was detected.</li><li>Overwrites <code>~/.cursor/rules/pstack-models.mdc</code> with <code>alwaysApply: true</code>.</li><li>Offers <code>/create-verification-skill</code> once, then <code>/create-formal-verification-skill</code> once.</li></ol>
{code("""# budget: large (xhigh)
feature, refactoring: grok-4.7-xhigh-fast
judgment and prose: claude-opus-5-5-xhigh
arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
interrogate reviewers: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
swarm workers: grok-4.7-xhigh-fast""","An excerpt of the default rule shape (17 role lines in full). Grok tops out at xhigh, so <code>unlimited</code> keeps Grok at xhigh.")}
<div class="note"><h4>Stale defaults</h4><p>A rule file written before a default changed still pins the old default. Delete those role lines, or the whole file, and run <code>/setup-pstack</code> again. A rerun keeps any role you set to something other than the default.</p></div>
<div class="note"><h4>Not bundled</h4><p><code>deslop</code>, <code>control-cli</code> and <code>control-ui</code> ship in <code>cursor-team-kit</code>. <code>/create-skill</code> is built into Cursor. The router calls all of them, so install cursor-team-kit to get the full set.</p></div></section>'''
ex=f'''<section id="examples"><div class="sec-head"><div class="eyebrow">README, guide</div><h2>Examples</h2></div>
{code("/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro first, then fix and verify.","README: routes to the bug-fix playbook.")}
{code("/poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by morning.","README: autonomous run, with a show-me-your-work decision trail.")}
{code("/how do we cancel runs? do we have an n+1 when we look up every run to cancel?")}
{code("/interrogate review this pr.")}
<p>To keep poteto-mode active across turns, pick it from the <code>/</code> menu and press <b>option+enter</b>. That makes it a Custom Mode. The README says it pairs with Cursor’s <code>/loop</code> for runs that last hours.</p></section>'''
got=f'''<section id="gotchas"><div class="sec-head"><div class="eyebrow">Checked 21 Oct 2026 on the box</div><h2>Gotchas and findings</h2></div><div class="callouts">
<div class="callout"><span class="n">1</span><p><b>“Use when…” never triggers on its own.</b> All 56 SKILL.md files set <code>disable-model-invocation: true</code>, including <code>typescript-best-practices</code> (“Use when reading or editing any .ts”) and <code>tdd</code>. Those descriptions read like auto-triggers, but these skills only run from a slash command or when the router reads them. This is a gap between the docs and the behavior.</p></div>
<div class="callout"><span class="n">2</span><p><b>Three principles say only when, not what.</b> The descriptions of <code>model-the-domain</code>, <code>never-block-on-the-human</code> and <code>redesign-from-first-principles</code> give the trigger but not the rule. The router’s index fills that in.</p></div>
<div class="callout"><span class="n">3</span><p><b>One flaky cold test run.</b> The first <code>bun test</code> (Bun 1.4.2) reported 59 pass, 1 fail and 1 error across 60 tests. Five reruns all passed 68/68. I didn’t capture the failing test, so I can’t say which one it was.</p></div>
<div class="callout"><span class="n">4</span><p><b>Side effects.</b> <code>/setup-pstack</code> overwrites <code>~/.cursor/rules/pstack-models.mdc</code>, which applies to every project. The <code>log.sh</code> script creates the parent directory of the log file. The verification skills generate new project-local skills and open PRs. Babysit stops at merge-ready and never merges. Shipping merges when you ask it to land (bottom-up, <code>gh pr merge --squash</code>, may arm auto-merge and <code>--force-with-lease</code> the next PR). Autopilot-full owners merge granted queue items after swarm verification; autopilot-stack never merges.</p></div>
<div class="callout"><span class="n">5</span><p><b>Grok Bot–specific skill.</b> <code>/make-bot-ui</code> builds a webhook UI that wakes a Grok Bot, with optional Tailscale exposure. It’s the only skill tied to a product other than Cursor.</p></div>
<div class="callout"><span class="n">6</span><p><b>Docs are consistent.</b> The repo’s own <code>scripts/check-pstack-docs.mjs</code> reports “56 skills (32 commands, 24 principles), 23 playbooks, 2 agents … 0 problems”. <code>generate-pstack-harness-trees.mjs --check</code> reports “harness/pstack is up to date”. Every skill name matches its folder (fixed in #702).</p></div></div></section>'''
new=f'''<section id="new"><div class="sec-head"><div class="eyebrow">6ce45c5 (v0.15.25) → {H[:7]} (v0.15.29)</div><h2>What’s new vs the reference</h2><p>The saved “Inside pstack” report describes v0.15.25 (14 Oct) with 54 skills. Since then, 18 commits changed 35 files (+366/−142).</p></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Commit</th><th>Change</th></tr></thead><tbody>
<tr><td>#709, #721</td><td>New <code>/create-formal-verification-skill</code>: picks the riskiest code, uses TLA+ by default for ordering bugs, falls back to generated-input tests when no verifier exists, and must show each property failing on a broken variant.</td></tr>
<tr><td>#716</td><td>New <code>/maintain-formal-verification-skill</code>: brings the model back in line after the code changes.</td></tr>
<tr><td>#715</td><td><code>/setup-pstack</code> now offers formal verification too (step 8).</td></tr>
<tr><td>#637, #705</td><td>Claude Code install from a generated <code>harness/pstack/</code> tree. CI fails when the tree is stale. See {L("docs/harness/claude-code.md","claude-code.md")}.</td></tr>
<tr><td>#704</td><td>Docs refresh plus the <code>check-pstack-docs.mjs</code> docs-vs-tree check.</td></tr>
<tr><td>#628, #692, #708</td><td><code>/ketchup</code> now uses screenshots, videos and diagrams, and lists every item waiting on you, never cutting one to save words.</td></tr>
<tr><td>#712, #729</td><td><code>/sharpen</code> went back to its original prompt and now returns only the rewrite.</td></tr>
<tr><td>#633, #634</td><td>Four principles (attack-the-premise, fix-root-causes, make-operations-idempotent, test-behavior-not-implementation) were restated as reasoning rather than rules. Marginal sections were cut from four skills.</td></tr>
<tr><td>#700, #702</td><td>Brand types now use a type guard instead of <code>as</code>. Every skill is named after its folder.</td></tr></tbody></table></div>
<div class="note"><h4>Installed copy = upstream</h4><p>The plugin cache at <code>~/agent-data/plugins/cache/cursor-public/pstack/{H[:7]}…</code> is identical to the fresh clone. <code>diff -r</code> shows only a <code>.cache-complete</code> marker.</p></div></section>'''
nxt=f'''<section id="next"><div class="sec-head"><div class="eyebrow">Sources</div><h2>Where to go next</h2></div><div class="srcs"><ul>
<li>{L("docs/guide/README.md","The pstack guide")}: ten chapters, from setup to recipes and pitfalls.</li>
<li>{L("README.md","README")} · {L("skills/poteto-mode/SKILL.md","poteto-mode SKILL.md")} · {L("skills/poteto-help/SKILL.md","/poteto-help")} (ask it which skill fits)</li>
<li>{L("skills/automate-me/SKILL.md","/automate-me")}: draft your own <code>&lt;name&gt;-mode</code> from your transcripts.</li>
<li>{L("automations/benny/README.md","benny")}: a dormant Slack triage-and-fix automation pack that only runs on Cursor.</li>
<li>Upstream: <a href="https://github.com/cursor/plugins/tree/main/pstack">github.com/cursor/plugins/tree/main/pstack</a> · plugin install <code>/home/box/agent-data/plugins/pstack</code></li></ul></div></section>'''
foot=f'Built 21 Oct 2026 from cursor/plugins @ {H[:7]} (commit 20 Oct 2026, 7:05 PM EDT), pstack v0.15.29. All facts come from the repo files, git log and local script runs.'
extra='''<style>.tag{font:600 .62rem var(--f-mono,monospace);background:var(--gold-soft);color:#7a5208;padding:1px 6px;border-radius:9px;text-transform:uppercase}
:root{--b-cmd:#8a2a46;--b-cmd-ink:#f2f6fa;--b-pr:#fcefcc;--b-pr-ink:#5e3f05;--b-pr-rule:#d9971a;--b-pb:#c7e2f5;--b-pb-ink:#173f5f;--k-cmd:#8a2a46;--k-cmd-ink:#fff;--k-pr:#d9971a;--k-pr-ink:#1f1a2c;--k-pb:#c7e2f5;--k-pb-ink:#173f5f;--tag-ink:#7a5208}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--b-cmd:#5a1c30;--b-cmd-ink:#fbe9ef;--b-pr:#3a2f17;--b-pr-ink:#f6d48a;--b-pr-rule:#f1bd4f;--b-pb:#1f3447;--b-pb-ink:#bfe2fa;--k-cmd:#e88ca6;--k-cmd-ink:#1f1a2c;--k-pr:#f1bd4f;--k-pr-ink:#1f1a2c;--k-pb:#9fd0f2;--k-pb-ink:#14121c;--tag-ink:#f1bd4f}}
:root[data-theme="dark"]{--b-cmd:#5a1c30;--b-cmd-ink:#fbe9ef;--b-pr:#3a2f17;--b-pr-ink:#f6d48a;--b-pr-rule:#f1bd4f;--b-pb:#1f3447;--b-pb-ink:#bfe2fa;--k-cmd:#e88ca6;--k-cmd-ink:#1f1a2c;--k-pr:#f1bd4f;--k-pr-ink:#1f1a2c;--k-pb:#9fd0f2;--k-pb-ink:#14121c;--tag-ink:#f1bd4f}
.tag{color:var(--tag-ink)}
.gband{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:22px 0 10px;padding:9px 14px;border-radius:9px;font-family:var(--f-display);font-weight:700;font-size:.95rem;letter-spacing:.01em}
.gcount{font-size:.75rem;font-weight:700;padding:1px 9px;border-radius:999px;background:rgba(255,255,255,.18)}
.gb-cmd{background:var(--b-cmd);color:var(--b-cmd-ink)}
.gb-pr{background:var(--b-pr);color:var(--b-pr-ink);border-left:6px solid var(--b-pr-rule)}.gb-pr .gcount{background:var(--b-pr-rule);color:#1f1a2c}
.gb-pb{background:var(--b-pb);color:var(--b-pb-ink);border-left:6px solid var(--sky-ink)}.gb-pb .gcount{background:var(--sky-ink);color:var(--panel)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;min-width:0}.cards-sm{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--k-cmd);border-radius:10px;padding:12px 14px;box-shadow:var(--shadow);min-width:0;overflow-wrap:anywhere}
.card.c-pr{border-top-color:var(--k-pr)}.card.c-pb{border-top-color:var(--sky-ink)}
.card .ch{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:6px}.card .ch a{margin-right:auto;font-weight:600}.card .ch code{font-size:.86rem;white-space:normal}
.kt{font-family:var(--f-display);font-size:.64rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:999px;white-space:nowrap}
.kt-cmd{background:var(--k-cmd);color:var(--k-cmd-ink)}.kt-pr{background:var(--k-pr);color:var(--k-pr-ink)}.kt-pb{background:var(--k-pb);color:var(--k-pb-ink)}
.card dl{margin:0}.card dt{font-family:var(--f-display);font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin-top:6px}.card dd{margin:2px 0 0;font-size:.88rem;color:var(--ink-2);line-height:1.45}</style>'''
h=page('pstack','pstack',nav,extra+hero+tldr+why+model+how+wf+pr+pb+inst+ex+got+new+nxt,footer=foot)
open('/workspace/dorothy-docs/pstack/index.html','w').write(h);print(len(h))
