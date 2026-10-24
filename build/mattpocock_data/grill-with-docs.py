from common import *
SLUG='mattpocock-grill-with-docs'; M,P,T=docs(SLUG)
G=SP('grill-with-docs'); GM=SP('grill-me'); GR=SP('grilling'); DM=SP('domain-modeling'); ADR=SP('domain-modeling','ADR-FORMAT.md'); GF=SP('domain-modeling','GLOSSARY-FORMAT.md'); RD='README.md'
Q=M.Q
hro=hero('Matt Pocock skill explainer · mattpocock/skills','mattpocock/grill-with-docs',11,
 'A two-line wrapper that turns a design interview into <mark>a glossary and ADRs written as you go</mark>.',
 f'The whole SKILL.md is one instruction: {Q("Call the Skill tool twice, for \"grilling\" and \"domain-modeling\".",G)} All the behavior lives in those two skills, so this page explains them. Matt calls the grill skills {Q("my most popular skills",RD)}.',
 [(PIN,'commit, 19 Oct 2026'),('1.2M','installs on skills.sh'),('7','lines in SKILL.md'),('2','skills it calls'),('0','scripts')],
 [('Who it is for','Anyone about to change code who wants the agent to understand the plan, and the project’s words, first.'),('What you get','A settled plan, plus GLOSSARY.md entries and docs/adr/ files created only when there is something to record.')])
s_why=sec('why','Why It Exists','Misalignment Is The Most Common Failure',f'From the repo README.',
 callouts([Q('The most common failure mode in software development is misalignment.',RD),Q('The fix for this is a **grilling session** - getting the agent to ask you detailed questions about what you\'re building.',RD),
  Q('Agents are usually dropped into a project and asked to figure out the jargon as they go. So they use 20 words where 1 will do.',RD),
  f'{Q("It\'s hard to explain how powerful this is. It might be the single coolest technique in this repo.",RD)} That is Matt on the shared-language half.']))
s_model=sec('model','Mental Model','A Design Tree, Worked One Frontier At A Time','grilling supplies the interview; domain-modeling supplies the side effects.',
 notes([('The design tree',Q('Map this as a **design tree**: every decision branches into the decisions that hang off it.',GR)),
  ('The frontier',Q('The **frontier** is every decision whose prerequisites are already settled',GR)),
  ('Facts vs decisions',Q('Finding _facts_ is your job, never the user\'s.',GR)+' '+Q('The _decisions_ are the user\'s: put each to them and wait.',GR)),
  ('Docs as a side effect',Q('When a term is resolved, update `GLOSSARY.md` right there.',DM))]))
IT=[
 dict(id='gwd',name='grill-with-docs',group='The wrappers',small='7 lines',pills=['user-invoked','engineering'],tag=Q('A relentless interview to sharpen a plan or design, which also creates docs (ADR\'s and glossary) as we go.',G),
  invoke='/grill-with-docs I want to add partial refunds to checkout',how=['Loads grilling and domain-modeling in the same session.','The interview runs as grilling describes; glossary and ADR writes follow domain-modeling.'],
  quotes=M.qs(['Call the Skill tool twice, for "grilling" and "domain-modeling".'],G),files=[G,SP('grill-with-docs','agents/openai.yaml')],lesson='A user-invoked skill can be a pure composition of reusable ones.',src=MB+G),
 dict(id='gm',name='grill-me',group='The wrappers',small='7 lines',pills=['user-invoked','productivity'],tag=Q('A relentless interview to sharpen a plan or design.',GM),invoke='/grill-me',
  how=['Loads grilling only: same interview, no glossary or ADRs.','The README points it at non-code uses.'],quotes=M.qs(['Call the Skill tool with "grilling".'],GM)+M.qs(['for non-code uses'],RD),files=[GM],lesson='Pick grill-me when there is no repo whose language should be recorded.',src=MB+GM),
 dict(id='gr',name='grilling',group='The engines',small='30 lines',pills=['model-invoked','productivity'],tag=Q('Grill the user relentlessly about a plan, decision, or idea.',GR),invoke='grill me on this migration plan',
  how=['Ask the whole frontier in one round, numbered, each with a recommended answer.','Wait for answers, recompute the frontier, ask the next round.','Send sub-agents for facts; ask only the questions that do not wait on them.','Stop when the frontier is empty and the user confirms.'],
  quotes=M.qs(['Word each question so "yes" accepts your recommended answer.','A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.','Do not act on it until the user confirms you have reached a shared understanding.'],GR),
  files=[GR],lesson='Recommend an answer for every question, so a fast user can reply “yes” down the list.',src=MB+GR),
 dict(id='dm',name='domain-modeling',group='The engines',small='79 lines',pills=['model-invoked','engineering'],tag=Q('Build and sharpen a project\'s domain model.',DM),invoke='(loaded by grill-with-docs)',
  how=['Challenge terms that conflict with GLOSSARY.md.','Propose one canonical term for fuzzy words.','Invent edge-case scenarios; check the code agrees with what you say.','Write glossary entries inline; offer an ADR only when the three tests pass.'],
  quotes=M.qs(['Create files lazily: only when you have something to write.','`GLOSSARY.md` should be totally devoid of implementation details.','If any of the three is missing, skip the ADR.'],DM),files=[DM,ADR,GF],lesson='Gate the expensive artifact (an ADR) behind explicit tests so it stays rare and worth reading.',src=MB+DM),
 dict(id='adr',name='ADR-FORMAT.md',group='Formats',small='helper',pills=['format'],tag=Q('An ADR can be a single paragraph.',ADR),invoke='docs/adr/0001-slug.md',
  how=['Numbered sequentially; scan for the highest number and add one.','Optional Status, Considered Options and Consequences, only when useful.'],
  quotes=M.qs(['The value is in recording *that* a decision was made and *why*, not in filling out sections.','**Hard to reverse**: the cost of changing your mind later is meaningful','**Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"','**The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons'],ADR),
  files=[ADR],lesson='Short ADRs get written; long templates get skipped.',src=MB+ADR),
 dict(id='gf',name='GLOSSARY-FORMAT.md',group='Formats',small='helper',pills=['format'],tag=Q('**Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.',GF),invoke='GLOSSARY.md (or GLOSSARY-MAP.md for many contexts)',
  how=['One root GLOSSARY.md for most repos.','A GLOSSARY-MAP.md lists contexts when a repo has several.'],quotes=M.qs(['**Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.'],GF),files=[GF],lesson='The _Avoid_ list is what stops synonym drift.',src=MB+GF)]
s_ex=f'<section id="parts">{head("The Parts","Two Words In SKILL.md, Four Files Of Behavior","Click a part. Quotes are checked against the file named under each.")}{explorer("gx","parts")}</section>'
s_how=sec('how','How It Works','Each Round Asks Everything It Can, Then Waits','The round format, copied from grilling/SKILL.md.',
 code('''❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>''','Format of one round.')+
 callouts([Q('Ask the whole frontier in one round: number each question and give your recommended answer.',GR),Q('When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it',GR),
  Q('When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately.',DM),Q('When the user states how something works, check whether the code agrees.',DM),
  Q('The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed.',GR)]))
s_cmp=sec('family','The Grill Family','Use One Of Three, Not All Three','',
 table(['Skill','What loads','Writes files?','Use when'],[['<code>grill-me</code>','grilling','No','Non-code plans and ideas'],['<code>grill-with-docs</code>','grilling + domain-modeling','GLOSSARY.md, docs/adr/','Code changes in a repo'],['<code>grilling</code>','itself','No','The agent reaches for it on its own (model-invoked)']])+
 adoption([['grill-me installs','1.4M',f'<a href="{SKSH}">skills.sh</a>, 23 Oct 2026'],['grill-with-docs installs','1.2M',f'<a href="{SKSH}">skills.sh</a>'],['grilling installs','979K',f'<a href="{SKSH}">skills.sh</a>'],['Matt: Meta’s Muse Code ships /grill and /grill-with-docs','959 likes, 6 Aug 2026',f'<a href="{X_GRILL}">x.com/mattpocockuk</a>']]))
s_words=sec('words','In Their Own Words','Lauren Tan On Why Grilling Works','From the stream with Matt, auto transcript, verbatim.',
 tq(T,'And that\'s why sort of grilling, I think, works effectively. Grilling is a Yeah. Yeah. It it draws those words out of you, right?','8:59')+
 tq(T,'someone might find a lot of success combining, you know, like your grill me with docs, uh, or wayfinder skill with some of the execution skills in Pstack as an example.','1:01:54'))
s_find=sec('findings','Gotchas','It Is Only As Good As The Skill Loader','From reading every file at '+PIN+'. No scripts ship, so there was nothing to run.',
 verdict([('Gap','Depends on a “Skill tool”','The whole body is “call the Skill tool twice”. In an agent without a skill-loading tool, the wrapper does nothing unless grilling and domain-modeling are installed and the agent opens them itself.'),
  ('Gap','Name clash with pstack','pstack has <code>principle-model-the-domain</code>, which is about stateful code shape, not glossaries. Different jobs, similar names; keep both.'),
  ('Gap','README still mentions CONTEXT.md','The README example links a glossary “still named <code>CONTEXT.md</code>” from before the rename. The skills now use GLOSSARY.md.'),
  ('Cost','Rounds are long','Asking the whole frontier at once means big first rounds. Answer “yes” to accept a recommendation.'),
  ('Copy','Lazy files','No empty GLOSSARY.md or docs/adr/ until a term or decision is actually settled.')]))
s_pair=sec('pstack','Pairs With pstack','Grill First, Then Hand The Settled Plan To pstack','pstack has no skill that interviews you about the plan. These are the hand-offs that fit.',
 pairs(P,[('architect','Sketch types, signatures, and module structure before code','Feed it the settled answers and new glossary terms; type names follow the glossary.'),
  ('in-your-own-words','Restate in your own words what you think the user\'s goals are','Run it after grilling as a cheap check that the agent really understood.'),
  ('interrogate','Multiple LLM reviewers challenge changes from independent angles','grill-with-docs reviews your thinking; interrogate reviews the resulting code.'),
  ('tdd','Use only when the user explicitly asks for TDD','Glossary terms become test names.'),
  ('create-verification-skill','Generate a project-local verification skill that drives your app the way a user does','What Lauren calls the most important skill; grilling cannot replace it.')])+
 tq(T,'verification I would say is probably the most important skill in PAC','18:43'))
s_next=sec('next','Where To Go Next','Read The Two Engines',''
 ,srcs([M.L(G),M.L(GR),M.L(DM),M.L(ADR),M.L(GF),M.L(GM),f'<a href="{X_GRILL}">Matt on Muse Code copying grill</a>']+NEXT_COMMON+['<a href="/mattpocock-wayfinder/">mattpocock/wayfinder</a> uses grill-with-docs’ pair for every grilling ticket']))
nav=[('top','Overview'),('why','Why it exists'),('model','Mental model'),('parts','The parts'),('how','How it works'),('family','The grill family'),('words','In their own words'),('findings','Gotchas'),('pstack','Pairs with pstack'),('next','Where to go next')]
JS=explorer_js('gx','mp-gwd',IT,['The wrappers','The engines','Formats'])
for d in (M,P,T): d.finish()
n=build(SLUG,'mattpocock/grill-with-docs',nav,hro+s_why+s_model+s_ex+s_how+s_cmp+s_words+s_find+s_pair+s_next,foot('grill-with-docs'),JS)
print('built',n)
