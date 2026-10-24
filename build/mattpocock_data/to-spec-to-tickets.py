from common import *
SLUG='mattpocock-to-spec-to-tickets'; M,P,T=docs(SLUG)
S=SP('to-spec'); TK=SP('to-tickets'); IM=SP('implement-spec'); RD='README.md'; TL='skills/engineering/setup-matt-pocock-skills/triage-labels.md'
Q=M.Q
hro=hero('Matt Pocock skill explainer · mattpocock/skills','mattpocock/to-spec → to-tickets',11,
 'Two skills that turn a finished conversation into <mark>a published spec, then a graph of tracer-bullet tickets</mark>.',
 f'to-spec: {Q("Do NOT interview the user; just synthesize what you already know.",S)} to-tickets: {Q("Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.",TK)} implement-spec then builds the graph.',
 [(PIN,'commit, 19 Oct 2026'),('714K','to-spec installs (unlabeled row)'),('710K','to-tickets installs'),('282K','implement-spec installs'),('0','scripts')],
 [('Who it is for','You have already grilled the idea (or charted it with wayfinder) and want it on the tracker as work an agent can grab.'),('What you get','One spec issue, N ticket issues (or .scratch files) with blocking edges, all labelled ready-for-agent.')])
s_why=sec('why','Why It Exists','Talk First, Then Write It Down Once','Both skills refuse to start from nothing: they synthesize what the conversation already holds.',
 callouts([Q('This skill takes the current conversation context and codebase understanding and produces a spec.',S),
  Q('Work from whatever is already in the conversation context.',TK),Q('"Make the change easy, then make the easy change."',TK),
  Q('Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.',S)]))
s_model=sec('model','Mental Model','A Spec Is The What; Tickets Are A Task Graph','',
 notes([('Seams',Q('The fewer seams across the codebase, the better - the ideal number is one.',S)),
  ('Tracer bullets',Q('Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer',TK)),
  ('Size',Q('Each slice is sized to fit in a single fresh context window',TK)),
  ('Graph',Q('The tickets are not a list of steps. They are a **task graph** with blocking relationships between them.',IM))])+
 code('''## Problem Statement
## Solution
## User Stories        (a LONG, numbered list)
## Implementation Decisions
## Testing Decisions
## Out of Scope
## Further Notes''','The to-spec template headings.'))
IT=[
 dict(id='spec',name='to-spec',group='The pipeline',small='3 steps',pills=['user-invoked','no interview'],tag=Q('Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you\'ve already discussed.',S),invoke='/to-spec',
  how=['Explore the repo; use glossary words; respect ADRs.','Sketch the test seams, highest first; confirm them with the user.','Write the template and publish; apply ready-for-agent.'],
  quotes=M.qs(['Check with the user that these seams match their expectations.','Apply the `ready-for-agent` triage label - no need for additional triage.','This list of user stories should be extremely extensive and cover all aspects of the feature.'],S),files=[S],lesson='Agree the test seams before writing the spec; everything else is synthesis.',src=MB+S),
 dict(id='tix',name='to-tickets',group='The pipeline',small='5 steps',pills=['user-invoked','quiz'],tag=Q('Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges',TK),invoke='/to-tickets <spec issue URL>',
  how=['Gather context; fetch the spec if passed by reference.','Optionally explore and look for prefactors.','Draft vertical slices with blocking edges.','Quiz the user on granularity and edges; iterate.','Publish in dependency order, blockers first.'],
  quotes=M.qs(['Iterate until the user approves the breakdown.','Do NOT close or modify any parent issue.','Use the per-ticket file template below: one ticket per file, never a single combined file.'],TK),files=[TK],lesson='Publish blockers first so later tickets can reference real ids.',src=MB+TK),
 dict(id='ec',name='Expand–contract',group='The pipeline',small='exception',pills=['wide refactors'],tag=Q('**Wide refactors are the exception to vertical slicing.**',TK),invoke='(inside to-tickets)',
  how=['Expand: add the new form beside the old.','Migrate call sites in batches, each blocked by the expand.','Contract: delete the old form, blocked by every batch.'],
  quotes=M.qs(['Don\'t force it into a tracer bullet; sequence it as **expand–contract**.','green is promised only there.'],TK),files=[TK],lesson='When a slice cannot land green, change the shape of the graph, not the rule.',src=MB+TK),
 dict(id='impl',name='implement-spec',group='The handoff',small='9 steps',pills=['user-invoked','subagents'],tag=Q('Implement the result of /to-spec and /to-tickets in code.',IM),invoke='/implement-spec <spec URL>',
  how=['Read spec and tickets; optional exploration subagent saves notes outside the repo.','Create one integration branch.','Implementer subagents, one worktree each, call tdd per ticket.','A merger subagent merges each finished branch; new frontier tickets start.','code-review on the integration branch at the end; one fixer subagent.'],
  quotes=M.qs(['Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits.','calls the Skill tool with `tdd` to build the ticket;','Once all tickets are complete, call the Skill tool with `code-review` on the integration branch.'],IM),files=[IM],lesson='Pass pointers, not pasted context, between subagents.',src=MB+IM)]
s_ex=f'<section id="parts">{head("The Parts","Spec, Tickets, Then Code","Click a part. Quotes are checked against the file named under each.")}{explorer("tx","parts")}</section>'
s_tl=sec('flow','The Flow','One Conversation Becomes A Merged Branch','',
 timeline([('grill','Talk it through','grill-with-docs or a finished wayfinder map'),('/to-spec','Publish the spec','template + ready-for-agent'),('/to-tickets','Publish the graph','quiz, then blockers first'),('/implement-spec','Build in parallel','worktrees + tdd + merger + code-review')]))
s_find=sec('findings','Gotchas','Where The Text Disagrees With Itself',f'From reading every file at {PIN}. No scripts ship, and nothing was run against a live tracker.',
 verdict([('Gap','README says to-spec quizzes you',f'The README’s workflow list says {Q("quizzes you about which modules you\'re touching before creating a spec",RD)}, but its own skill list says {Q("No interview, just synthesizes what you\'ve already discussed.",RD)} The skill sits between: no interview, one seam check.'),
  ('Gap','ready-for-agent may not exist',f'Both skills apply <code>ready-for-agent</code>, but setup only writes the label vocabulary in Section B, and only when the triage skill is installed. Without it the label may be missing on your tracker.'),
  ('Gap','“tracker doc’s operation” for sub-issues','to-tickets says to make each ticket a sub-issue via the tracker doc, but only the GitHub tracker doc defines a sub-issue operation; the GitLab and local docs do not.'),
  ('Cost','Context-window sizing is a judgment call','“A single fresh context window” is not measured; size slices by feel or borrow wayfinder’s 100K-token yardstick.'),
  ('Copy','No file paths in specs','Specs and tickets stay valid while code moves. Prototype snippets are the only allowed exception.')]))
s_pair=sec('pstack','Pairs With pstack','pstack Covers What Happens Inside Each Ticket','',
 pairs(P,[('architect','Sketch types, signatures, and module structure before code','Run before to-spec to settle Implementation Decisions as real types.'),
  ('blast-radius','Find what a change could break somewhere else before it ships','Sizes expand–contract batches; to-tickets even uses the phrase “blast radius”.'),
  ('tdd','Use only when the user explicitly asks for TDD','implement-spec’s implementers call Matt’s tdd; pstack’s is narrower and opt-in.'),
  ('interrogate','Multiple LLM reviewers challenge changes from independent angles','A heavier swap for the final code-review step.'),
  ('create-verification-skill','Generate a project-local verification skill that drives your app the way a user does','Gives “demoable or verifiable on its own” a real check.')])+
 tq(T,'the single most important skill that should be in your toolkit is verification','16:14'))
s_next=sec('next','Where To Go Next','Set Up The Tracker First','',srcs([M.L(S),M.L(TK),M.L(IM),M.L(TL),'<a href="/mattpocock-setup-matt-pocock-skills/">mattpocock/setup-matt-pocock-skills</a>: all three need it','<a href="/mattpocock-wayfinder/">mattpocock/wayfinder</a>: produces the decisions a spec synthesizes']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('model','Mental model'),('parts','The parts'),('flow','The flow'),('findings','Gotchas'),('pstack','Pairs with pstack'),('next','Where to go next')]
JS=explorer_js('tx','mp-tst',IT,['The pipeline','The handoff'])
for d in (M,P,T): d.finish()
print('built',build(SLUG,'mattpocock/to-spec → to-tickets',nav,hro+s_why+s_model+s_ex+s_tl+s_find+s_pair+s_next,foot('to-spec'),JS))
