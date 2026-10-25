from common import *
SLUG='pbakaus-impeccable'; D=repo(SLUG,'IMPECCABLE_SRC'); Q=D.Q
RD='README.md'; SK='.claude/skills/impeccable/SKILL.md'; R=lambda n:f'.claude/skills/impeccable/reference/{n}.md'
hro=hero('Design Skills · pbakaus/impeccable','pbakaus/impeccable',8,
 'One skill, 24 commands and a detector that <mark>catches AI design tells without an LLM</mark>.',
 Q('Design guidance for AI coding agents. 1 skill, 24 commands, live browser iteration, and 62 deterministic detector rules for AI-generated frontend design.',RD)+' Use it for app UI, dashboards, settings and existing product screens.',
 [(D.pin,'commit, 23 Oct 2026'),('4.7.1','skill version in repo'),('24','commands'),('62','detector rules (README count)'),('17','harnesses listed')],
 [('Who it is for','Anand and the fleet (Ellie FSE, Usha UX) when an agent builds or reviews app screens.'),('What you get','<code>PRODUCT.md</code> (product truth), <code>DESIGN.md</code> (visual system), one <code>/impeccable</code> command, and a hook that lints UI edits.')])
s_why=sec('why','Why It Exists','Every Model Learned The Same SaaS Template','',
 callouts([Q("Every model trained on the same SaaS templates. Skip the guidance and you get the same handful of tells on every project: Inter for everything, purple-to-blue gradients, cards nested in cards, gray text on colored backgrounds, the rounded-square icon tile above every heading.",RD),
  Q("Anthropic's [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) was the first widely-used design skill for Claude. Impeccable started from there.",RD)+'<sup>1</sup>']))
s_install=sec('install','Install','One Installer, Then Init Inside Your Agent','Run these from the project root. The <code>npx</code> step copies files; <code>init</code> is the part that thinks.',
 code('''# 1. copy the skill + hook into every harness it detects (asks project vs global)
npx impeccable install

# scripted: pick harnesses and scope up front
npx impeccable install --providers=claude,codex,cursor,grok --scope=project

# 2. inside Claude Code / Cursor / Grok Build (Codex: $impeccable)
/impeccable init

# later: refresh skill + hook
npx impeccable update''')+
 table(['Harness','Where it lands','One extra step'],[
  ['Claude Code','<code>.claude/skills/impeccable</code>; hook in <code>.claude/settings.local.json</code>','Or <code>/plugin marketplace add pbakaus/impeccable</code>'],
  ['Cursor','<code>.cursor/skills/impeccable</code>; hook in <code>.cursor/hooks.json</code>','Post-edit hook only; no Stop deep pass'],
  ['Codex CLI','<code>.agents/skills/</code>; hook in <code>.codex/hooks.json</code>',Q('Codex users should open `/hooks` after install or update and approve the project hook when prompted.',RD)],
  ['Grok Build','<code>.grok/skills/</code>; <code>.grok/hooks/impeccable.json</code>','<code>/hooks-trust</code> or launch with <code>--trust</code>'],
  ['Copilot (VS Code)','<code>.github/skills/</code> or the Marketplace extension','The extension installs no hooks']])+
 notes([('Why npx at all',Q('Node is only involved if you use the `npx impeccable` installer, which is a shim around the same binary',RD)+'. The skill itself runs a self-contained engine binary.'),
  ('Keep the noise out of git','Paste the README\'s <code># impeccable-ignore-start</code> block into <code>.gitignore</code>. Keep <code>.impeccable/config.json</code>, <code>design.json</code>, <code>surfaces/*.md</code> and <code>critique/*.md</code> tracked.'),
  ('Telemetry','Theme "rolls" call impeccable.style. Turn off recording with <code>npx impeccable telemetry off</code> or <code>DO_NOT_TRACK=1</code>.')]))
s_model=sec('model','Mental Model','PRODUCT.md Is Truth, DESIGN.md Is Look','Two files, written by two different commands, read by every other command.',
 notes([('PRODUCT.md, from init',Q('`init` captures durable product truth in PRODUCT.md. It does not invent a visual world and does not write DESIGN.md',R('init'))+'. Audience, purpose, constraints, voice.'),
  ('DESIGN.md, from document',Q('Generate a `DESIGN.md` file at the project root that captures the current visual design system, so AI agents generating new screens stay on-brand.',R('document'))+' YAML tokens up top, then prose. '+Q('Tokens are normative; prose provides context for how to apply them.',R('document'))),
  ('Modes pick the ambition',Q('The mode names what the visitor\'s success looks like on this surface.',SK)+' Persuade, Operate, Read, Experience. Dashboards are Operate: '+Q('Scanability, consistency, native expectations, and the real usage scene outrank expression.',SK)),
  ('Refine vs redesign',Q('Refinement preserves; redesign replaces.',SK)+' Polish keeps the incumbent look. A redesign replaces DESIGN.md.')]))
C=lambda c:f'`{c}'
def cmd(id,name,cat,tagq,ref,inv,how,qs,lesson):
    return dict(id=id,name=name,group=cat,small=cat,pills=[cat,'/impeccable'],tag=Q(tagq,SK),invoke=inv,how=how,quotes=D.qs(qs,R(ref)) if qs else [],files=[R(ref)],lesson=lesson,src=D.blob+R(ref))
IT=[
 cmd('init','init','Build','Capture durable product context in PRODUCT.md','init','/impeccable init',['Scans the repo first so you are not asked known facts.','Interviews only for gaps.','Writes PRODUCT.md; never DESIGN.md.'],['Treat repository evidence as a hypothesis, not user approval.'],'Separate what the product is from how it looks.'),
 cmd('document','document','Build','Generate DESIGN.md from existing project code','document','/impeccable document',['Reads tokens, CSS and components.','Writes DESIGN.md in the Google design.md format: YAML tokens, then up to eight sections.'],['Tokens are normative; prose provides context for how to apply them.'],'Make the existing look a file the next agent reads.'),
 cmd('critique','critique','Evaluate','UX design review with heuristic scoring','critique','/impeccable critique landing',['Two isolated assessments: design review, then detector/browser evidence.','Synthesises a critique and saves a snapshot under .impeccable/critique/.'],['If you degrade for any reason, the report\'s first line MUST be a banner: `⚠️ DEGRADED: single-context (<reason>)`.'],'Run the human-judgment pass before the linter output can anchor it.'),
 cmd('audit','audit','Evaluate','Technical quality checks (a11y, perf, responsive)','audit','/impeccable audit blog',['Scores five dimensions 0 to 4.','Reports only; other commands fix.'],["Don't fix issues; document them for other commands to address."],'Keep the reporter and the fixer separate.'),
 cmd('polish','polish','Refine','Final quality pass before shipping','polish','/impeccable polish settings',['Aligns with the design system.','Refuses to sneak in a redesign.'],['Polish is refinement, never concealed redesign.','A detector result is defect evidence, not proof of quality.'],'A clean lint is not a finished page; look at it.'),
 cmd('bolder','bolder','Refine','Amplify safe or bland designs','bolder','/impeccable bolder the hero',['Raises one named part, leaves the rest.','Rejects "more effects" as the answer.'],['The reflex answer, reaching for more effects, is the opposite of bold; reject it first.'],'Bold is conviction in one place, not decoration everywhere.'),
 cmd('quieter','quieter','Refine','Tone down aggressive or overstimulating designs','quieter','/impeccable quieter pricing',['Restrains palette and adds air.','Keeps the point of view.'],['Quiet design is harder than bold design. Subtlety needs precision.'],'Quieter is not generic.'),
 cmd('animate','animate','Enhance','Add purposeful animations and motion','animate','/impeccable animate onboarding',['Motion only to explain state, relationship or hierarchy.'],['Decoration without purpose is animation debt.'],'Every animation should answer "what changed?"'),
 cmd('distill','distill','Refine','Strip to essence, remove complexity','distill','/impeccable distill the settings page',['Finds redundant elements and repeated information.','Removes them.'],["Strip a design to its essence. Remove anything that doesn't earn its place"],'Subtract before you add.'),
 cmd('live','live','Iterate','Visual variant mode: pick elements in the browser, iterate on alternatives','live','/impeccable live',['Needs a dev server with HMR or a static HTML file.','Pick an element, get variants hot-swapped.'],['Live editing requires a local checkout; injection into deployed production sites (including HTTPS) is unsupported.'],'Iterate on the rendered page, never on production.')]
s_ex=f'<section id="commands">{head("The Commands","Ten Commands Do Most Of The Work","The other 14 (shape, harden, onboard, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, extract, generate, craft) follow the same pattern. Quotes are checked against the reference file under each.")}{explorer("ix","commands")}</section>'
s_det=sec('detector','Detectors And Hooks','The Linter Runs With No LLM And No API Key','',
 code('''npx impeccable detect src/              # scan a folder (findings on stderr)
npx impeccable detect --json .          # CI: JSON on stdout
npx impeccable detect --github src/     # GitHub Actions annotations
npx impeccable detect https://example.com   # rendered page, needs local Chrome
npx impeccable ignores add-value overused-font Inter --reason "Brand font"
# exit 0 clean · 2 findings · 1 could not scan''')+
 notes([('What it catches',Q('The detector catches 62 deterministic issues across AI slop (side-tab borders, purple gradients, bounce easing, dark glows) and general design quality (line length, cramped padding, small touch targets, skipped headings, and more).',RD)),
  ('The hook',Q('The hook runs the Impeccable design detector on direct UI file edits and surfaces findings back into the agent flow.',RD)),
  ('Two tiers',Q('The per-edit hook surfaces only the immediate tier: mechanical, unambiguous problems worth interrupting an edit for',R('hooks'))+'. Taste findings wait for a deeper pass on Stop (Claude Code, Codex, Grok Build; not Cursor).'),
  ('Read it right',Q('A clean detector run is evidence, not proof of visual or accessibility quality',RD)+'.')]))
s_find=sec('findings','Findings And Gotchas','The README Lags The Skill In Places',f'From reading the repo at {D.pin} and running the published CLI on the box (Node 20.19, 24 Oct 2026).',
 verdict([('Gap','craft is described two ways','README: "Full shape-then-build flow with visual iteration". SKILL.md: "'+Q('Deprecated alias for an ordinary new-work request',SK)+'". Trust SKILL.md.'),
  ('Gap','npm is a release behind','The repo says 4.7.1; <code>npm view impeccable version</code> returned 4.7.0. <code>npx impeccable</code> gets 4.7.0.'),
  ('Bug','Silent on old Node','<code>package.json</code> requires Node 22.18 or later. On Node 20.19, <code>npx impeccable detect --list-rules</code> printed nothing and exited 0, with no warning. Check <code>node -v</code> first.'),
  ('Gap','Cursor note may be stale','The README still says Cursor skills need the Nightly channel. That may be out of date; check before you follow it.'),
  ('Cost','Hooks run outside model approval',Q('In Claude Code, installed command hooks run independently of model-tool approval.',RD)+' The first edit can download the engine binary.'),
  ('Copy','Reporter vs fixer','audit documents and never fixes; critique runs its two assessments isolated so the linter cannot anchor the judgment.')]))
s_steal=sec('steal','What To Use','Init Once, Then Audit, Critique, Polish','',
 steal([('Start:','<code>npx impeccable install</code>, then <code>/impeccable init</code>, then <code>/impeccable document</code> if the app already has a look.'),
  ('Review:','<code>/impeccable critique &lt;screen&gt;</code> for design, <code>/impeccable audit &lt;screen&gt;</code> for a11y and performance.'),
  ('Adjust:','<code>bolder</code>, <code>quieter</code>, <code>distill</code>, <code>animate</code> on one named target at a time.'),
  ('Ship:','<code>/impeccable polish</code>, then <code>npx impeccable detect --json</code> in CI.'),
  ('Pin your favourite:','<code>/impeccable pin audit</code> gives you <code>/audit</code>.')]))
s_rule=one_builder('Impeccable is the builder for <b>apps and dashboards</b>. Choose it, and leave Hallmark and Taste Skill unloaded.')
s_next=sec('next','Sources','Read The Skill, Then The README','',srcs([D.L(SK,'SKILL.md'),D.L(RD,'README.md'),D.L(R('hooks'),'reference/hooks.md'),'<a href="https://impeccable.style">impeccable.style</a>: docs, hooks and detector pages','<sup>1</sup> Anthropic <a href="https://github.com/anthropics/skills/tree/main/skills/frontend-design">frontend-design</a>: the skill Impeccable grew from. No separate sheet; Impeccable replaces it for this fleet.']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('install','Install'),('model','Mental model'),('commands','Commands'),('detector','Detectors and hooks'),('findings','Findings'),('steal','What to use'),('one-builder','Pick one builder'),('next','Sources')]
JS=explorer_js('ix','ds-imp',IT,['Build','Evaluate','Refine','Enhance','Iterate'])
D.finish()
print('built',build(SLUG,'pbakaus/impeccable',nav,hro+s_why+s_install+s_model+s_ex+s_det+s_find+s_steal+s_rule+s_next,foot(D),JS))
