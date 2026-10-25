from common import *
SLUG='nextlevelbuilder-ui-ux-pro-max'; D=repo(SLUG,'UIUXPROMAX_SRC'); Q=D.Q
RD='README.md'; SK='.claude/skills/ui-ux-pro-max/SKILL.md'
hro=hero('Design Skills · nextlevelbuilder/ui-ux-pro-max','nextlevelbuilder/ui-ux-pro-max',17,
 'A <mark>searchable design reference</mark>, not a page builder.',
 Q('Searchable local UI/UX guidance: 79 searchable styles (50 active), 192 product palettes and exact reasoning profiles, 74 font pairings, 119 UX guidelines, 105 curated icons, 17 GSAP presets, 25 chart types, and 22 technology stacks.',SK),
 [(D.pin,'commit pinned'),('79','styles (50 active)'),('192','palettes'),('74','font pairings'),('119','UX guidelines')],
 [('Use it for','One answer to a narrow question: a palette for a fintech app, a chart type, an a11y rule, a GSAP preset.'),('Not for','Building or restyling a page. Use Impeccable or Hallmark for that.')])
s_when=sec('when','Search Or Hand Off','Ask It A Question; Let A Builder Build','',
 table(['You need','Do this','Why'],[
  ['A rule for one bug (focus ring, touch target, chip wrap)','<code>search.py "focus not obscured" --domain ux</code>','Small, cited answer; no taste involved'],
  ['A chart type or palette idea','<code>--domain chart</code> / <code>--domain color</code>','Lookup data, cheap to check'],
  ['Stack-specific detail','<code>--stack html-tailwind</code>','Separate from the design decision'],
  ['A new landing or marketing page','Hand off to <a href="/nutlope-hallmark/">Hallmark</a>','Its Floor bans logo walls and eyebrows that this data suggests'],
  ['An app, dashboard or existing screen','Hand off to <a href="/pbakaus-impeccable/">Impeccable</a>','PRODUCT.md / DESIGN.md plus a detector'],
  ['A whole design system','Builder\'s own system (<code>/impeccable document</code>)','<code>--design-system</code> output is generic, see below']])+
 notes([('Its own rule',Q('Build each query around **one dominant intent**, using **2–5 meaningful terms** and one useful constraint such as product, platform, or interaction.',SK)),('Its own skip list',Q('Skip it for pure backend logic, API/database design, non-visual performance work, infrastructure/DevOps, or non-visual scripts',SK)+'.')]))
s_cmd=sec('commands','Commands','Install Once, Then Call search.py','',
 code('''npm install -g ui-ux-pro-max-cli && uipro init --ai cursor     # or claude, codex ...
# Claude Code plugin instead:
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

S=~/.claude/skills/ui-ux-pro-max/scripts/search.py              # path differs per harness
python3 $S "error summary validation" --domain ux
python3 $S "fintech dashboard" --domain color -n 3
python3 $S "badge chip overflow nowrap" --stack html-tailwind
python3 $S "internal analytics" --design-system -p Acme          # prints; add --persist to write''')+
 notes([('persist is cautious',Q('If `design-system/<project-slug>/MASTER.md` already exists, `--persist` **skips writing and leaves it untouched** unless you also pass `--force`',SK)+'.'),('Python only','No dependencies. Try <code>python3</code> if <code>python</code> is missing.')]))
s_find=sec('findings','Findings','The Data Repeats The Tells The Builders Ban','Queries run on the box against the installed copy, 24 Oct 2026.',
 verdict([('Gap','Inter first','The top typography hit for "developer tool docs dark" was Inter for everything. Impeccable flags that as <code>overused-font</code>.'),
  ('Gap','Marketing pattern for a dashboard','<code>--design-system</code> for "internal analytics dashboard" returned an "Enterprise Gateway" pattern with a Client Logos section. Hallmark\'s Floor forbids logo walls.'),
  ('Copy','Good as a checklist','The UX and accessibility domains give useful, outcome-phrased rules. Use them as a second opinion under a builder.')]))
s_rule=one_builder('UI/UX Pro Max is <b>not a builder</b>, so it can sit next to any one of them as a lookup. The rule is about builders: Impeccable, Hallmark or Taste Skill, one per project.')
s_next=sec('next','Sources','Repo And Site','',srcs([D.L(SK,'SKILL.md'),D.L(RD,'README.md'),'<a href="https://uupm.cc">uupm.cc</a>']+NEXT_COMMON))
nav=[('top','Overview'),('when','Search or hand off'),('commands','Commands'),('findings','Findings'),('one-builder','Pick one builder'),('next','Sources')]
D.finish()
print('built',build(SLUG,'nextlevelbuilder/ui-ux-pro-max',nav,hro+s_when+s_cmd+s_find+s_rule+s_next,foot(D),''))
