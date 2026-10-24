from common import *
SLUG='mattpocock-wayfinder'; M,P,T=docs(SLUG)
W=SP('wayfinder'); RD='README.md'; S='skills/engineering/setup-matt-pocock-skills/'
GH=S+'issue-tracker-github.md'; GL=S+'issue-tracker-gitlab.md'; LO=S+'issue-tracker-local.md'
Q=M.Q
hro=hero('Matt Pocock skill explainer · mattpocock/skills','mattpocock/wayfinder',11,
 'Plan work too big for one session as <mark>a map of decision tickets on your issue tracker</mark>, resolved one per session.',
 f'{Q("Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.",W)} It plans; it does not build.',
 [(PIN,'commit, 19 Oct 2026'),('717K','installs on skills.sh'),('128','lines in SKILL.md'),('4','ticket types'),('0','scripts')],
 [('Who it is for','Efforts where you cannot yet see the route: migrations, new products, anything with “fog”.'),('What you get','One map issue labelled <code>wayfinder:map</code>, child tickets with native blocking, and a decision log that grows a line per session.')])
s_why=sec('why','Why It Exists','Charge At The Destination And You Get Lost','',
 callouts([Q('A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to the **destination** isn\'t visible yet.',W),
  Q('Wayfinding is about finding that way, not charging at the destination.',W),
  Q('The pull to just do the work is usually the signal you\'ve reached the edge of the map and it\'s time to hand off.',W)])+
 f'<p>Latent Space interviewed Matt about it; he <a href="{X_WAY}">shared the breakdown</a> on 20 Aug 2026 (327 likes). Their post describes it as designed for the “fog of war”.</p>')
s_model=sec('model','Mental Model','The Map Is An Index; Each Decision Lives In One Ticket','',
 notes([('Map',Q('The map is an **index**, not a store.',W)),('Ticket size',Q('Its body is the question, sized to one 100K token agent session',W)),
  ('Frontier',Q('the **frontier** is the open, unblocked, unclaimed children, the edge of the known.',W)),
  ('Fog vs ticket',Q('The test is whether you can state the question precisely now, _not_ whether you can answer it now.',W)),
  ('Claim',Q('That assignee _is_ the claim: an open, unassigned ticket is unclaimed.',W)),('Names',Q('A wall of `#42, #43, #44` is illegible; names read at a glance.',W))])+
 code('''## Destination
## Notes
## Decisions so far
- [<closed ticket title>](link): <one-line gist of the answer>
## Not yet specified
## Out of scope''','The map body sections (abridged from wayfinder/SKILL.md).'))
IT=[
 dict(id='chart',name='Chart the map',group='Two modes',small='6 steps',pills=['mode','one session'],tag=Q('User invokes with a loose idea.',W),invoke='/wayfinder migrate billing off Stripe Checkout',
  how=['Grill and domain-model to name the destination.','Grill breadth-first to map the frontier.','Create the map, then the specifiable tickets; wire blocking in a second pass.','Fire research subagents in parallel, then stop.'],
  quotes=M.qs(['**If this surfaces no fog** (the way to the destination is already clear, the whole journey small enough for one session), you don\'t need a map.','Stop: charting is one session\'s work; it hand-resolves nothing.','a placeholder `#<n>` auto-links to an unrelated issue.'],W),files=[W],lesson='Create first, wire second: ids must exist before edges can.',src=MB+W),
 dict(id='work',name='Work through the map',group='Two modes',small='5 steps',pills=['mode','one ticket'],tag=Q('User invokes with a map (URL or number).',W),invoke='/wayfinder <map URL>',
  how=['Load the low-res map only.','Take the named ticket or the first frontier ticket; claim it first.','Resolve by its label type.','Post a resolution comment, close, append to Decisions so far.','Graduate fog into new tickets; rule out-of-scope work out.'],
  quotes=M.qs(['**never resolve more than one ticket per session**, with the exception of research tickets.','Read the label, not just the body: the body never states the type.','The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.'],W),files=[W],lesson='One ticket per session keeps every context window small.',src=MB+W),
 dict(id='research',name='Research',group='Ticket types',small='AFK',pills=['AFK','subagent'],tag=Q('Resolved by a subagent that calls the Skill tool with "research".',W),invoke='wayfinder:research',
  how=['Fired in parallel at charting time.','Findings go on a throwaway branch with a pointer from the ticket.'],quotes=M.qs(['capturing its findings on a throwaway `research/<name>` branch','Push the branch but open no PR: it is never merged.'],W),files=[W],lesson='Facts are cheap to gather in parallel; decisions are not.',src=MB+W),
 dict(id='proto',name='Prototype',group='Ticket types',small='HITL',pills=['HITL'],tag=Q('Use when "how should it look" or "how should it behave" is the key question.',W),invoke='wayfinder:prototype',
  how=['Calls the prototype skill to make something rough to react to.','Links the prototype as an asset.'],quotes=M.qs(['Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to'],W),files=[W],lesson='React to an artifact, not a description.',src=MB+W),
 dict(id='grill',name='Grilling',group='Ticket types',small='HITL, default',pills=['HITL','default'],tag=Q('**Grilling** (HITL): Conversation. The default case.',W),invoke='wayfinder:grilling',
  how=['Loads grilling + domain-modeling, the same pair as grill-with-docs.'],quotes=M.qs(['a grilling agent that answers its own questions has broken this'],W),files=[W],lesson='HITL means the human answers; the agent never stands in.',src=MB+W),
 dict(id='task',name='Task',group='Ticket types',small='HITL or AFK',pills=['does, not decides'],tag=Q('This is the one type that _does_ rather than decides, and it earns its place by unblocking a decision, not by delivering the destination.',W),invoke='wayfinder:task',
  how=['Agent does it alone where it can; otherwise hands over a checklist.','The answer records resulting facts later tickets need.'],quotes=M.qs(['Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen.'],W),files=[W],lesson='Doing is allowed only when it unblocks a decision.',src=MB+W),
 dict(id='gh',name='GitHub',group='Tracker backends',small='sub-issues',pills=['native blocking'],tag=Q('GitHub\'s **native issue dependencies**, the canonical, UI-visible representation.',GH),invoke='docs/agents/issue-tracker.md',
  how=['Children are sub-issues.','Blocking via the issue dependencies API.'],quotes=M.qs(['`gh issue create --parent <parent> ...`'],GH),files=[GH],lesson='Native blocking draws the frontier in the tracker UI.',src=MB+GH),
 dict(id='gl',name='GitLab',group='Tracker backends',small='Part of #map',pills=['Premium for blocking'],tag=Q('Native blocking links are a Premium/Ultimate feature',GL),invoke='docs/agents/issue-tracker.md',
  how=['Children carry a “Part of” line.','Free tier falls back to a Blocked by line.'],quotes=M.qs(['an issue carrying `Part of #<map>` at the top of its description'],GL),files=[GL],lesson='Check your GitLab tier before relying on the visual frontier.',src=MB+GL),
 dict(id='lo',name='Local markdown',group='Tracker backends',small='.scratch/',pills=['default'],tag=Q('The **map** is a file with one **child** file per ticket.',LO),invoke='.scratch/<effort>/map.md',
  how=['Tickets are numbered files with Type and Status lines.','Blocked by lines list ticket numbers.'],quotes=M.qs(['**Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.'],LO),files=[LO],lesson='Works with no tracker at all, but concurrent sessions can race on file edits.',src=MB+LO)]
s_ex=f'<section id="parts">{head("The Parts","Two Modes, Four Ticket Types, Three Backends","Click a part. Quotes are checked against the file named under each.")}{explorer("wx","parts")}</section>'
s_words=sec('words','In Their Own Words','Lauren Tan Suggests Mixing It With pstack','From the stream with Matt, auto transcript, verbatim (it hears “wayfinder” as “Wfinder” and “poteto” as “potato”).',
 tq(T,'Combine Wfinder with potato mode and make your own custom mode, right?','1:04:16')+
 tq(T,'someone might find a lot of success combining, you know, like your grill me with docs, uh, or wayfinder skill with some of the execution skills in Pstack as an example.','1:01:54'))
s_find=sec('findings','Gotchas','Read These Before You Chart',f'From reading every file at {PIN}. No scripts ship.',
 verdict([('Gap','Two answers for “no tracker”',f'The same paragraph says {Q("If not, tell the user to run `/setup-matt-pocock-skills`.",W)} and then {Q("If no tracker has been provided, default to the local-markdown tracker.",W)} Pick one when you adapt it.'),
  ('Cost','GitLab free tier','No native blocking, so the frontier is not visible in the GitLab UI; the skill falls back to a text line.'),
  ('Gap','Names its siblings by Skill tool','Research, prototype, grilling and domain-modeling must be installed too, or ticket types silently degrade.'),
  ('Copy','No triage labels on decision tickets',Q('`wayfinder:` labels are the only labels a map and its tickets carry, never a triage label like `ready-for-agent`',W)),
  ('Cost','Plans, not deliverables','When the map is done you still need a spec and tickets. That is what to-spec and to-tickets are for.')]))
s_pair=sec('pstack','Pairs With pstack','Wayfinder Plans Across Sessions; pstack Executes Inside One','',
 pairs(P,[('poteto-mode','poteto\'s agent style for concise, detailed responses','Lauren’s own suggestion: fold wayfinder into a custom mode.'),
  ('figure-it-out','Design an auditable playbook when no narrower one fits','The single-session cousin: use it when the fog fits in one context.'),
  ('show-me-your-work','Keep a reviewable decision trail for long-running','A per-session trail; wayfinder’s Decisions so far is the cross-session one.'),
  ('swarm','Fan out N parallel workers, drain them, and return one report.','Run several unblocked frontier tickets at once.'),
  ('principle-guard-the-context-window','Apply when context is filling up','The same instinct as one 100K-token ticket per session.')]))
s_next=sec('next','Where To Go Next','Then Turn The Map Into A Spec','',srcs([M.L(W),M.L(GH),M.L(GL),M.L(LO),f'<a href="{X_WAY}">Matt on the Latent Space breakdown</a>',
 '<a href="/mattpocock-grill-with-docs/">mattpocock/grill-with-docs</a>: the pair every grilling ticket loads','<a href="/mattpocock-to-spec-to-tickets/">mattpocock/to-spec → to-tickets</a>: what comes after the map']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('model','Mental model'),('parts','The parts'),('words','In their own words'),('findings','Gotchas'),('pstack','Pairs with pstack'),('next','Where to go next')]
JS=explorer_js('wx','mp-way',IT,['Two modes','Ticket types','Tracker backends'])
for d in (M,P,T): d.finish()
print('built',build(SLUG,'mattpocock/wayfinder',nav,hro+s_why+s_model+s_ex+s_words+s_find+s_pair+s_next,foot('wayfinder'),JS))
