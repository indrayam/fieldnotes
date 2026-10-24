from common import *
SLUG='mattpocock-setup-matt-pocock-skills'; M,P,T=docs(SLUG)
D='skills/engineering/setup-matt-pocock-skills/'; S=D+'SKILL.md'; RD='README.md'
GH=D+'issue-tracker-github.md'; GL=D+'issue-tracker-gitlab.md'; LO=D+'issue-tracker-local.md'; TL=D+'triage-labels.md'; DO=D+'domain.md'
Q=M.Q
hro=hero('Matt Pocock skill explainer · mattpocock/skills','mattpocock/setup-matt-pocock-skills',11,
 'A one-time interview that <mark>writes docs/agents/*.md so the engineering skills know your tracker, labels and glossary</mark>.',
 f'{Q("Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.",S)} {Q("This is a prompt-driven skill, not a deterministic script.",S)}',
 [(PIN,'commit, 19 Oct 2026'),('1.1M','installs on skills.sh'),('118','lines in SKILL.md'),('3','sections: A, B, C'),('0','scripts')],
 [('Who it is for','Anyone about to use wayfinder, to-spec, to-tickets, implement-spec, triage, code-review or ask-matt in a repo.'),('What you get','An <code>## Agent skills</code> block in CLAUDE.md or AGENTS.md, plus docs/agents/issue-tracker.md, domain.md and maybe triage-labels.md.')])
s_why=sec('why','Why It Exists','The Skills Ask “Which Tracker?” So Answer Once','',
 callouts([Q('Scaffold the per-repo configuration that the engineering skills assume:',S),
  Q('When the installer asks which skills to take, include `setup-matt-pocock-skills`.',RD),
  Q('Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.',S)]))
s_model=sec('model','Mental Model','Explore, Recommend, Confirm, Write','',
 notes([('Explore',Q('Read whatever exists; don\'t assume:',S)),('Ask',Q('One section, one answer, then the next.',S)),
  ('Skip',Q('skip the section entirely when exploration already settled it',S)),('Write',Q('Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that\'s already there.',S))])+
 code('''## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.''','The block it adds to CLAUDE.md or AGENTS.md.'))
IT=[
 dict(id='a',name='Section A: Issue tracker',group='The three sections',small='always',pills=['GitHub default'],tag=Q('Default posture: these skills were designed for GitHub.',S),invoke='docs/agents/issue-tracker.md',
  how=['GitHub remote → GitHub; GitLab remote → GitLab.','Otherwise offer GitHub, GitLab, local markdown, or other.','Other trackers are recorded as freeform prose.'],
  quotes=M.qs(['**Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose'],S),files=[S,GH,GL,LO],lesson='Recommend from evidence (the git remote) so the user answers in one word.',src=MB+S),
 dict(id='b',name='Section B: Triage labels',group='The three sections',small='only with triage',pills=['conditional'],tag=Q('Skip this section entirely if the `triage` skill isn\'t installed',S),invoke='docs/agents/triage-labels.md',
  how=['Asks one question: keep the five defaults?','On GitHub or GitLab, creates any missing labels.'],
  quotes=M.qs(['`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`','When Section B ran on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`).'],S),files=[S,TL],lesson='Map onto existing labels instead of creating duplicates.',src=MB+S),
 dict(id='c',name='Section C: Domain docs',group='The three sections',small='single by default',pills=['GLOSSARY.md','docs/adr/'],tag=Q('Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root).',S),invoke='docs/agents/domain.md',
  how=['Written without asking for most repos.','Multi-context only when monorepo signals exist.'],quotes=M.qs(['their absence means single-context, which is almost every repo.'],S),files=[S,DO],lesson='Do not ask a question the repo already answered.',src=MB+S),
 dict(id='pick',name='Which file gets the block',group='Write rules',small='CLAUDE.md first',pills=['no duplicates'],tag=Q('If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate.',S),invoke='CLAUDE.md, else AGENTS.md',
  how=['Edit CLAUDE.md if it exists, else AGENTS.md.','If neither exists, ask; never pick for the user.'],quotes=M.qs(['If neither exists, ask the user which one to create; don\'t pick for them.'],S),files=[S],lesson='Safe to re-run: it updates in place.',src=MB+S)]
s_ex=f'<section id="parts">{head("The Parts","Three Questions, Then Files","Click a part. Quotes are checked against the file named under each.")}{explorer("sx","parts")}</section>'
s_who=sec('readers','Who Reads It','Seven Skills Point Back Here','Each of these says to run setup when no tracker is configured (from grepping the repo at '+PIN+').',
 table(['Skill','Reads'],[['<code>wayfinder</code>','tracker “Wayfinding operations”'],['<code>to-spec</code>, <code>to-tickets</code>','tracker + triage labels'],['<code>implement-spec</code>','tracker'],['<code>triage</code>','tracker + triage labels'],['<code>code-review</code>, <code>ask-matt</code>','setup docs']]))
s_find=sec('findings','Gotchas','Prompt-Driven Means You Review The Draft',f'From reading every file at {PIN}. No scripts ship, and it was not run against a live repo.',
 verdict([('Gap','ready-for-agent without triage','to-spec and to-tickets always apply <code>ready-for-agent</code>, but this skill only writes or creates labels when triage is installed.'),
  ('Gap','Sub-issues only on GitHub','The GitLab and local tracker docs have no sub-issue operation, though to-tickets asks for one.'),
  ('Cost','GitLab blocking needs Premium',Q('Native blocking links are a Premium/Ultimate feature',GL)),
  ('Gap','skills.sh needs Node 22.20+','Running <code>npx skills@latest add --help</code> on the box (Node 20.19) crashed: skills 1.7.4 requires node ≥22.20.0. The README does not say so.'),
  ('Copy','Never picks AGENTS.md vs CLAUDE.md for you','It edits whichever exists and asks when neither does.')]))
s_pair=sec('pstack','Pairs With pstack','pstack Has Its Own Setup, For Models Not Trackers','',
 pairs(P,[('setup-pstack','Configure which models pstack uses per role and at what reasoning budget.','Different job: pstack configures models; Matt configures the repo. Run both.'),
  ('create-verification-skill','Generate a project-local verification skill that drives your app the way a user does','Another one-time per-repo setup worth doing alongside.')]))
s_next=sec('next','Where To Go Next','Then Run The Skills It Configures','',srcs([M.L(S),M.L(GH),M.L(GL),M.L(LO),M.L(TL),M.L(DO),'<a href="/mattpocock-wayfinder/">mattpocock/wayfinder</a>','<a href="/mattpocock-to-spec-to-tickets/">mattpocock/to-spec → to-tickets</a>']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('model','Mental model'),('parts','The parts'),('readers','Who reads it'),('findings','Gotchas'),('pstack','Pairs with pstack'),('next','Where to go next')]
JS=explorer_js('sx','mp-setup',IT,['The three sections','Write rules'])
for d in (M,P,T): d.finish()
print('built',build(SLUG,'mattpocock/setup-matt-pocock-skills',nav,hro+s_why+s_model+s_ex+s_who+s_find+s_pair+s_next,foot('setup'),JS))
