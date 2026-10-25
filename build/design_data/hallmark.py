from common import *
from gal import uri
SLUG='nutlope-hallmark'; D=repo(SLUG,'HALLMARK_SRC'); Q=D.Q
RD='README.md'; SK='skills/hallmark/SKILL.md'; T=lambda n:f'skills/hallmark/references/themes/{n}.md'
hro=hero('Design Skills · nutlope/hallmark','nutlope/hallmark',8,
 'A landing-page skill that <mark>refuses to look AI-generated</mark>, and a linter that proves it.',
 Q('A design skill for Claude Code, Codex, Cursor and OpenCode that refuses to look AI-generated.',RD)+' Made by Together AI. Use it for new marketing and landing pages, not app screens.',
 [(D.pin,'commit, 22 Oct 2026'),('2.0.0','skill version'),('48','themes (README)'),('16','Floor rules'),('3','verbs: build, redesign, audit')],
 [('Who it is for','A new landing, launch or product page where the first screen has to sell.'),('What you get','One self-contained HTML/CSS page, stamped with its decisions, linted at eight widths and reviewed by a fresh-context subagent.')])
s_why=sec('why','Why It Exists','Models Fall Into The Same Ten Tells','',
 callouts([Q('Hallmark holds a hard floor and then gets out of the way.',RD),
  Q('the eyebrow above every heading, tracked-capital labels, one coloured word in a headline, a page of empty frames or nothing but photographs, a hero that misses its screen, an email sign-up at the end of every page, a form that says thanks without sending anything.',RD),
  Q('A fresh-context reviewer gets the last word.',RD)]))
s_install=sec('install','Install','One Command, Global By Default','',
 code('''npx skills add nutlope/hallmark -g                       # every harness, every project
npx skills add nutlope/hallmark -g --agent claude-code   # one harness (codex, cursor, opencode, github-copilot)
npm i -g puppeteer-core                                  # + Chrome: needed for sloplint --render and screenshots''')+
 table(['Harness','Lands in','Invoke'],[['Claude Code','<code>~/.claude/skills/hallmark</code>','<code>/hallmark &lt;prompt&gt;</code>'],['Codex CLI','<code>~/.agents/skills/hallmark</code>','<code>$hallmark &lt;prompt&gt;</code>'],['Cursor, OpenCode','finds the copies above','<code>/hallmark &lt;prompt&gt;</code>']])+
 notes([('Why -g',Q('`-g` installs for every project; leave it off to install into the current one.',RD)),('Node',Q('Needs Node 18 or later.',RD)+' Without puppeteer the static checks still run.'),('If it stays quiet','Name it: <i>use hallmark to build ...</i>. Its description stops it from touching existing designs unless named.')]))
s_verbs=sec('verbs','The Verbs','Build Is The Default; Redesign And Audit Need Its Name','',
 code('''/hallmark a landing page for a dotfiles CLI       # build (deals 3 themes)
/hallmark Terminal: a landing page for burrow     # build in a named theme
/hallmark custom: ...                             # no theme, Floor still holds
/hallmark redesign ./src/app                      # keeps content + wiring, new system + layout
/hallmark audit ./index.html                      # report only, no edits''')+
 notes([('Rule',Q('Never use it on an existing design unless the user names Hallmark, as in `/hallmark redesign <path>`.',SK)),
  ('Redesign safety',Q('`sloplint --before` records every link, field, handler and heading first, `sloplint --kept` fails the redesign if one went missing',RD)+'.'),
  ('Lighter redesigns','Say <i>keep the layout</i> for a restyle or <i>polish</i> for only the tells.'),
  ('What about "study"?','No <code>study</code> verb ships in v2. SKILL.md lists only '+Q('`redesign <target>` (a full redesign keeping content and wiring) and `audit <target>` (a report)',SK)+'. "study" only shows up as an eval brief (<code>eval/</code>, b6) that expects the skill to decline.')]))
s_flow=sec('flow','How A Build Runs','Ask Once, Deal A Theme, Build The Hero Alone','The eight steps from SKILL.md, short.',
 steal([('0 Pre-flight.','Reads fonts, palette, framework and any <code>DESIGN.md</code>, which overrides everything.'),('1 Ask once.','Material, audience, use, tone. Or say <i>go ahead</i>. '+Q('Facts are never inferred',SK)+'.'),('2 Shape.','Names the visitor\'s job, then <code>theme.mjs draw</code> deals the page anatomy.'),('3 Direction.','<code>theme.mjs deal</code> offers three themes; the agent picks one and says why.'),('4 to 5 Load and Picks.','Loads one theme file, then posts a Picks block: your one chance to redirect.'),('6 Build.','Hero first, linted with <code>--stage hero</code> and reviewed cold, then the rest.'),('7 Sweep.','<code>sloplint --render</code> until clean, gates walked, fresh reviewer, then the material ask.')]))
TH=[('editorial','Editorial','Longform posts, essays, a personal magazine voice.'),('newsprint','Newsprint','Daily Diff style: dated issues, columns, a newspaper feel.'),('terminal','Terminal','CLI tools, dotfiles, homelab, anything you install from a shell.'),('specimen','Specimen','Typography-led pages; a single essay or manifesto.'),('grid','Grid','Indexes, directories, systems; Swiss and modular.'),('ink','Ink','Plain black notice; the quietest option.')]
GI=[dict(id=f'th-{s}',n=n,il=uri(os.path.join(D.root,f'skills/hallmark/references/themes/{s}.jpg'),maxw=720),d=fit,k='fit') for s,n,fit in TH]
def first(s):
    t=D.rd(T(s)); body=t.split('---',2)[2]; line=[l for l in body.splitlines() if l.strip() and not l.startswith('#')][0]
    return line.split(',')[0]
IT=[dict(id=s,name=n,group='Fits Anand',small=D.rd(T(s)).split('display: ')[1].split('\n')[0],pills=['theme','genre: '+D.rd(T(s)).split('genre: ')[1].split('\n')[0]],
  tag=Q(first(s),T(s)),invoke=f'/hallmark {n}: a landing page for ...',how=[fit,'Named themes skip the deal; the stamp records "(by request)".'],
  quotes=[[Q('keywords: '+D.rd(T(s)).split('keywords: ')[1].split('\n')[0],T(s)),T(s)]],files=[T(s),T(s).replace('.md','.jpg')],img=f'th-{s}',
  lesson='A theme is a material, not a plan: it never sets layout.',src=D.blob+T(s)) for s,n,fit in TH]
s_themes=sec('themes','Theme Catalog','Six Of The 48 Suit A Terminal-First Engineer','Picked for Anand\'s sites (indrayam.com, Daily Diff, Cribsheets) and CLI-tool landings. Pictures are the repo\'s own theme renders.',
 f'{explorer("hx","themes")}'+gal('ghx',GI,'sm')+notes([('Theme is a material',Q('A theme is a material, not a plan: it never says what a page contains or in what order, so two prompts in one theme make two different pages.',RD)),('All of them','<a href="https://www.usehallmark.com">usehallmark.com</a> shows all 48. The repo folder holds 48 theme files plus a README.')]))
s_lint=sec('sloplint','Sloplint','The Floor Is Enforced By A Script, Not A Prompt','',
 code('''node ~/.claude/skills/hallmark/scripts/sloplint.mjs page.html            # static checks
node .../sloplint.mjs page.html --render                                   # + eight widths in Chrome
node .../sloplint.mjs src/ --url http://localhost:3000/ --scope page --json
node .../sloplint.mjs ./src/app --before    # snapshot links, fields, handlers before a redesign
node .../sloplint.mjs ./src/app --kept      # fail if any went missing
# exit 1 on any FAIL''')+
 '<p>Run on the box against a deliberately sloppy one-screen test page (output trimmed) (24 Oct 2026):</p>'+
 code('''FAIL 2a  purple-to-blue gradient on .h
FAIL 10a transition: all on body
FAIL 20  no Hallmark stamp on the first non-empty line of any CSS
FAIL 34  no overflow-x: clip on html and body
FAIL 38i <em>/<i> inside <h1>
FAIL 48  font-family literal "Inter" on body
FAIL 48  colour literal #7c3aed outside tokens (x2)
WARN 46a metric "Trusted by 10,000+": verify the user supplied this number
WARN F23 the document lacks lang on <html>, a <title>, a meta description
sloplint: 8 FAIL, 2 WARN across 1 file(s).   # exit 1''')+
 notes([('Tiers','<b>Floor</b> never ships. <b>Reflex</b> can be waived on the record. <b>Finish</b> never blocks.'),('It reads frameworks too','.html and .css, plus .jsx, .tsx, .vue, .svelte, .astro (Tailwind class strings, cn/clsx/cva).'),('Edit-time hook','<code>node skills/hallmark/scripts/install-hook.mjs</code> adds a Floor check on edits, Claude Code only.')]))
s_find=sec('findings','Findings And Gotchas','Named Colours Slip Past The Floor',f'From reading {D.pin} and running sloplint on the box.',
 verdict([('Bug','Named colours are not caught','<code>linear-gradient(purple,blue)</code> passed both 2a (purple-to-blue gradient) and 48 (colour literal). The same gradient written as hex (<code>#7c3aed,#2563eb</code>) failed both. Floor rule 11 says never a purple-to-blue gradient, so the linter misses named colours.'),
  ('Gap','"study" is not a v2 verb','The brief listed build / redesign / audit / study. Only redesign and audit ship as verbs; build is the default.'),
  ('Gap','Version labels disagree','<code>package.json</code> and SKILL.md say 2.0.0; the commit that brought in v2 is titled "Hallmark v2.2".'),
  ('Gap','Theme count','README says forty-eight; <code>references/themes/</code> has 48 theme <code>.md</code> files plus <code>README.md</code> (49 <code>.md</code> files).'),
  ('Cost','Strict copy rules','About 80 words per screen and no eyebrows or tracked caps. Great for landings, wrong for docs or dashboards. Use Impeccable there.'),
  ('Copy','before/kept for redesigns','Snapshotting every link and handler before a rewrite and failing if any disappear is worth stealing for any refactor.')]))
s_rule=one_builder('Hallmark is the builder for <b>landing and marketing pages</b>. Choose it, and leave Impeccable and Taste Skill unloaded on that project.')
s_next=sec('next','Sources','Read SKILL.md; It Is 154 Lines','',srcs([D.L(SK,'SKILL.md'),D.L(RD,'README.md'),D.L('skills/hallmark/references/gates.md','references/gates.md'),D.L('skills/hallmark/scripts/sloplint.mjs','scripts/sloplint.mjs'),'<a href="https://www.usehallmark.com">usehallmark.com</a>: every theme with a finished page']+NEXT_COMMON))
nav=[('top','Overview'),('why','Why it exists'),('install','Install'),('verbs','The verbs'),('flow','How a build runs'),('themes','Theme catalog'),('sloplint','Sloplint'),('findings','Findings'),('one-builder','Pick one builder'),('next','Sources')]
JS=explorer_js('hx','ds-hal',IT,['Fits Anand'])
D.finish()
print('built',build(SLUG,'nutlope/hallmark',nav,hro+s_why+s_install+s_verbs+s_flow+s_themes+s_lint+s_find+s_rule+s_next,foot(D),JS))
