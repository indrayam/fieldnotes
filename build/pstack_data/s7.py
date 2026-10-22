S = [
dict(id="poteto-help", cat="entry",
 tag="The front desk. Answers questions about pstack, points at the right skill, playbook or principle, and hands back a prompt to send rather than starting the work.",
 invoke="/poteto-help which skill should i use to check what a small diff could break?",
 how=["Infers the need from the message. If it is still unclear, asks one multiple-choice question: set up, start a task, pick a skill, fix a run, or make pstack your own.",
      "Checks state that changes the answer: a missing <code>pstack-models.mdc</code>, no <code>verify-*</code> skill, no formal verification skill. It offers <code>/setup-pstack</code> at most once per chat.",
      "Routes through a 33-row table of situations to skills, plus close calls (<code>/how</code> vs <code>/why</code> vs <code>/teach</code>, <code>/arena</code> vs <code>/swarm</code>) and a list of what is not in pstack.",
      "Covers the trigger phrases for playbooks and a symptom-to-fix table for runs that went wrong.",
      "Replies with the answer first, at most one example prompt, and a public GitHub link to the file the answer came from."],
 rules=["For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.",
        "Read the file you route to before you quote it, and trust it when it disagrees with this map.",
        "A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep."],
 lesson="It is a routing map that tells the agent to defer to the files it routes to, so the map can go stale without spreading wrong answers. The 0.15.30 update added the <code>/statechart</code> row."),
]
