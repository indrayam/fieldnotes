from common import *
SLUG='nextlevelbuilder-ui-ux-pro-max'; D=repo(SLUG,'UIUXPROMAX_SRC'); Q=D.Q
RD='README.md'; SK='.claude/skills/ui-ux-pro-max/SKILL.md'
hro=hero('Design Skills · nextlevelbuilder/ui-ux-pro-max','nextlevelbuilder/ui-ux-pro-max',17,
 'A <mark>searchable design reference</mark>, not a page builder.',
 Q('Searchable local UI/UX guidance: 80 searchable styles (51 active), 192 product palettes and exact reasoning profiles, 74 font pairings, 119 UX guidelines, 105 curated icons, 17 GSAP presets, 25 chart types, and 22 technology stacks.',SK),
 [(D.pin,'commit pinned'),('2.15.0','plugin version'),('80','styles (51 active)'),('192','palettes'),('119','UX guidelines')],
 [('Use it for','One answer to a narrow question: a palette for a fintech app, a chart type, an a11y rule, a GSAP preset.'),('Not for','Building or restyling a page. Use Impeccable or Hallmark for that.')])
s_when=sec('when','Search Or Hand Off','Ask It A Question; Let A Builder Build','',
 table(['You need','Do this','Why'],[
  ['A rule for one bug (focus ring, touch target, chip wrap)','<code>search.py "focus not obscured" --domain ux</code>','Small, cited answer; no taste involved'],
  ['A chart type or palette idea','<code>--domain chart</code> / <code>--domain color</code>','Lookup data, cheap to check'],
  ['Stack-specific detail','<code>--stack html-tailwind</code>','Separate from the design decision'],
  ['A style or product type that must work right-to-left','<code>--domain style --rtl=full</code>','Filters on the new <code>rtl_level</code> column; style and product only'],
  ['A new landing or marketing page','Hand off to <a href="/nutlope-hallmark/">Hallmark</a>','Its Floor bans logo walls and eyebrows that this data suggests'],
  ['An app, dashboard or existing screen','Hand off to <a href="/pbakaus-impeccable/">Impeccable</a>','PRODUCT.md / DESIGN.md plus a detector'],
  ['A whole design system','Builder\'s own system (<code>/impeccable document</code>)','<code>--design-system</code> output is generic, see below']])+
 notes([('Its own rule',Q('Build each query around **one dominant intent**, using **2–5 meaningful terms** and one useful constraint such as product, platform, or interaction.',SK)),('Its own skip list',Q('Skip it for pure backend logic, API/database design, non-visual performance work, infrastructure/DevOps, or non-visual scripts',SK)+'.')]))
s_new=sec('new','What Changed In 2.15.0','Three Additions: A Native Style, An RTL Filter, Nuxt UI 4.12','Upstream 9a3f14f → b7d5353 (plugin 2.15.0). Every command below was run against an isolated scratch clone at b7d5353, 7 Nov 2026. The installed fleet copy is still the older 79-style version until it is re-copied, so these flags are not there yet.',
 table(['Change','What it means for you','Seen on the box'],[
  ['<b>Apple Native Experience</b> style (row 90, <code>apple-native-experience</code>)','A platform style for apps that should feel like iOS / iPadOS / macOS: system type, semantic adaptive colours, 44px targets. It explicitly does not require Liquid Glass or blur.','<code>"apple native" --domain style -n 1</code> → Status active, Type Platform/System, <code>rtl_level: full</code>'],
  ['Style count 79 → 80 searchable, 50 → 51 active','That one new style is the whole count change. 9 more rows are deprecated and stay out of search.','<code>catalog-summary.json</code>: total 89, searchable 80, active 51'],
  ['<code>--rtl</code> / <code>--rtl=LEVEL</code>','New <code>rtl_level</code> column on every style and product: <b>full</b>, <b>partial</b>, <b>caveats</b>. Bare <code>--rtl</code> keeps all three levels and just shows the column; <code>--rtl=full</code> keeps only rows that mirror without rework.','Active styles: 36 full, 9 partial, 6 caveats. Products: 70 full, 91 partial, 31 caveats.'],
  ['Nuxt UI pinned to 4.12.0','Rows 77–83 added: UChart (categories, colours, donut data), UApp auto locale with @nuxtjs/i18n, UCheckboxGroup max, UFileUpload reject, and a 4.11.3 security-upgrade note.','<code>"chart donut" --stack nuxt-ui</code> → "Feed UChart donut one row per slice"']])+
 notes([('Its own RTL rule',Q('`caveats` means the style or product encodes reading direction — say so before recommending it, and propose a mirrorable alternative when the user needs a strict RTL build.',SK)),
  ('Where --rtl is refused','Only with <code>--domain style</code> or <code>product</code>. With <code>--domain ux</code>, <code>--stack</code> or <code>--design-system</code> the CLI exits with a usage error, e.g. <code>--rtl is not supported with --design-system; run a separate --domain style or --domain product query</code>.'),
  ('Apple Native, shown','No gallery here: the row ships text tokens, not renders. Its own variables: <code>--font-body: system-ui</code>, <code>--radius-control: 10px</code>, <code>--touch-target: 44px</code>, <code>--motion-duration: 150-300ms</code>.')]))
s_cmd=sec('commands','Commands','Install Once, Then Call search.py','',
 code('''npm install -g ui-ux-pro-max-cli && uipro init --ai cursor     # or claude, codex ...
# Claude Code plugin instead:
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

S=~/.claude/skills/ui-ux-pro-max/scripts/search.py              # path differs per harness
python3 $S "error summary validation" --domain ux
python3 $S "fintech dashboard" --domain color -n 3
python3 $S "badge chip overflow nowrap" --stack html-tailwind
python3 $S "internal analytics" --design-system -p Acme          # prints; add --persist to write
python3 $S "apple native" --domain style -n 1                   # new in 2.15.0
python3 $S "admin dashboard data" --domain style --rtl=full     # RTL filter, style/product only
python3 $S "chart donut" --stack nuxt-ui                        # Nuxt UI 4.12 rows''')+
 notes([('persist is cautious',Q('If `design-system/<project-slug>/MASTER.md` already exists, `--persist` **skips writing and leaves it untouched** unless you also pass `--force`',SK)+'.'),('Python only','No dependencies. Try <code>python3</code> if <code>python</code> is missing.')]))
s_find=sec('findings','Findings','The Data Repeats The Tells The Builders Ban','Inter and logo-wall checks: installed copy, 24 Oct 2026. RTL check: scratch clone at b7d5353, 7 Nov 2026.',
 verdict([('Gap','Inter first','The top typography hit for "developer tool docs dark" was Inter for everything. Impeccable flags that as <code>overused-font</code>.'),
  ('Gap','Marketing pattern for a dashboard','<code>--design-system</code> for "internal analytics dashboard" returned an "Enterprise Gateway" pattern with a Client Logos section. Hallmark\'s Floor forbids logo walls.'),
  ('Gap','The RTL example in SKILL.md comes back empty','At b7d5353 the documented example <code>"dashboard" --domain style --rtl=full</code> returned <b>0 results</b>, although plain <code>"dashboard" --domain style</code> returns Bento Box Grid, which is <code>rtl_level: full</code>. A more specific query (<code>"admin dashboard data"</code>) did return full rows. If <code>--rtl=full</code> is empty, retry with more terms before deciding nothing fits.'),
  ('Copy','Good as a checklist','The UX and accessibility domains give useful, outcome-phrased rules. Use them as a second opinion under a builder.')]))
s_rule=one_builder('UI/UX Pro Max is <b>not a builder</b>, so it can sit next to any one of them as a lookup. The rule is about builders: Impeccable, Hallmark or Taste Skill, one per project.')
s_next=sec('next','Sources','Repo And Site','',srcs([D.L(SK,'SKILL.md'),D.L(RD,'README.md'),'<a href="https://uupm.cc">uupm.cc</a>']+NEXT_COMMON))
nav=[('top','Overview'),('when','Search or hand off'),('new','What changed in 2.15.0'),('commands','Commands'),('findings','Findings'),('one-builder','Pick one builder'),('next','Sources')]
D.finish()
print('built',build(SLUG,'nextlevelbuilder/ui-ux-pro-max',nav,hro+s_when+s_new+s_cmd+s_find+s_rule+s_next,foot(D),''))
