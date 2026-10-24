from common import *
SLUG='mattpocock-handoff'; M,P,T=docs(SLUG)
H=SP('handoff'); CH='skills/in-progress/claude-handoff/SKILL.md'; RD='README.md'
Q=M.Q
hro=hero('Matt Pocock skill explainer · mattpocock/skills','mattpocock/handoff',11,
 'Five sentences that <mark>compact a conversation into a note a fresh agent can pick up</mark>.',
 f'{Q("Compact the current conversation into a handoff document for another agent to pick up.",H)} It writes to your temp folder, points at artifacts instead of copying them, and names the skills the next agent should load.',
 [(PIN,'commit, 19 Oct 2026'),('1.0M','installs on skills.sh'),('16','lines in SKILL.md'),('420K','claude-handoff installs'),('0','scripts')],
 [('Who it is for','Long sessions whose context is full or drifting, where starting fresh beats compacting in place.'),('What you get','One markdown file in <code>$TMPDIR</code> (or <code>/tmp</code>) to paste or point the next session at.')])
s_why=sec('why','Why It Exists','A Fresh Context Beats A Full One','',
 callouts([Q('Write a handoff document summarising the current conversation so a fresh agent can continue the work.',H),
  Q('If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.',H)]))
s_model=sec('model','Mental Model','The Five Rules, One Per Sentence','The whole body of SKILL.md, split up.',
 notes([('Where',Q('Save to the temporary directory of the user\'s OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.',H)),
  ('Next skills',Q('Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.',H)),
  ('Pointers',Q('Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.',H)),
  ('Secrets',Q('Redact any sensitive information, such as API keys, passwords, or personally identifiable information.',H)),
  ('Focus',Q('What will the next session be used for?',H)+' (the argument hint)')]))
IT=[
 dict(id='ho',name='handoff',group='Shipped',small='16 lines',pills=['user-invoked','productivity'],tag=Q('Compact the current conversation into a handoff document for another agent to pick up.',H),invoke='/handoff next session: write the migration tests',
  how=['Summarize the conversation for a fresh agent.','Save to the OS temp dir, not the repo.','Add suggested skills; link artifacts; redact secrets.'],quotes=M.qs(['- not the current workspace.'],H),files=[H,SP('handoff','agents/openai.yaml')],lesson='Keep handoff notes out of the repo so they never get committed.',src=MB+H),
 dict(id='ch',name='claude-handoff',group='In progress',small='in-progress/',pills=['Claude Code only','launches an agent'],tag=Q('Hand the current conversation off to a fresh background agent that picks up the work immediately.',CH),invoke='/claude-handoff',
  how=['Same summary rules as handoff.','Then launches a background Claude Code agent with the summary as its prompt.'],
  quotes=M.qs(['`claude --bg --name "<descriptive name>" -- "$(cat <summary file>)"`','Passing the file keeps the shell from running backticks or expanding `$` in the summary.','since the summary becomes the agent\'s prompt.'],CH),files=[CH],lesson='Pass prompts through a file, never inline, so the shell cannot expand them.',src=MB+CH)]
s_ex=f'<section id="parts">{head("The Parts","One Shipped Skill, One In Progress","Click a part. Quotes are checked against the file named under each.")}{explorer("hx","parts")}</section>'
s_find=sec('findings','Gotchas','It Is Prose, So Check The Output',f'From reading both files at {PIN}. No scripts ship.',
 verdict([('Cost','Temp files vanish','<code>/tmp</code> is cleared on reboot on many systems and is local to one machine. Move the file if the next session is tomorrow or elsewhere.'),
  ('Gap','Redaction is on trust','Nothing checks the output for keys. Read it before pasting it anywhere shared.'),
  ('Gap','claude-handoff is not shipped','It lives under <code>skills/in-progress/</code> and is Claude Code specific, yet skills.sh already lists 420K installs for it.'),
  ('Copy','Suggested skills section','The next agent loads the right skills on turn one instead of rediscovering them.')]))
s_pair=sec('pstack','Pairs With pstack','handoff Writes The Note; pstack Reads The History','',
 pairs(P,[('recall','Reconstruct your recent working context from your own chat history','The other direction: rebuild context from history when nobody wrote a handoff.'),
  ('ketchup','Catch the user up on what changed in this chat since their last message','A handoff for the human rather than for an agent.'),
  ('principle-guard-the-context-window','Route bulk to subagents; keep summaries in the main thread, not raw payloads.','The same reason to hand off: keep context small.')])+'<p>Lauren on why she wrote recall, after losing context between chats:</p>'+
 tq(T,'was just a way for me to collapse collapse and compress that workflow into a skill.','1:03:10'))
s_next=sec('next','Where To Go Next','Read Both Files; They Are Short','',srcs([M.L(H),M.L(CH),'<a href="/mattpocock-wayfinder/">mattpocock/wayfinder</a>: the other way Matt splits work across sessions']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('model','Mental model'),('parts','The parts'),('findings','Gotchas'),('pstack','Pairs with pstack'),('next','Where to go next')]
JS=explorer_js('hx','mp-ho',IT,['Shipped','In progress'])
for d in (M,P,T): d.finish()
print('built',build(SLUG,'mattpocock/handoff',nav,hro+s_why+s_model+s_ex+s_find+s_pair+s_next,foot('handoff'),JS))
