# Shared pieces for the three Design Skills explainers (Impeccable, Hallmark, UI/UX Pro Max).
# Each quote goes through Doc.Q and is checked against the pinned source checkout at build time.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
from config import src
PINS={'IMPECCABLE_SRC':('pbakaus/impeccable','9368675'),'HALLMARK_SRC':('nutlope/hallmark','7ec8682'),'UIUXPROMAX_SRC':('nextlevelbuilder/ui-ux-pro-max-skill','9a3f14f')}
def repo(slug,var):
    r,pin=PINS[var]; D=Doc(slug,src(var),f'https://github.com/{r}/blob/{pin}/'); D.pin=pin; D.repo=r; return D
# The cross-cutting rule, on every sheet (Usha UX's brief for Anand's fleet).
def one_builder(here):
    return sec('one-builder','Fleet Rule','Pick One Builder Per Project',
      'This rule sits on all three Design Skills sheets.',
      notes([('The rule','Never load <b>Impeccable</b>, <b>Hallmark</b> and <b>Taste Skill</b> together on one project. Pick one builder.'),
        ('Why','Each ships its own floor, bans and stamp. Impeccable writes PRODUCT.md, DESIGN.md and <code>.impeccable/</code>. Hallmark writes <code>.hallmark/</code> and a CSS stamp. Two builders on one page argue: one deals a theme, the other rolls a visual world, and the agent splits the difference.'),
        ('Rule of thumb','App, dashboard, settings, existing product UI: <a href="/pbakaus-impeccable/">Impeccable</a>. New landing or marketing page: <a href="/nutlope-hallmark/">Hallmark</a>. Need a palette, font pair or UX rule: <a href="/nextlevelbuilder-ui-ux-pro-max/">UI/UX Pro Max</a>. It is a lookup, so it can sit next to either builder.'),
        ('You are here',here)]))
NEXT_COMMON=['<a href="/pbakaus-impeccable/">pbakaus/impeccable</a>: the app and dashboard builder',
  '<a href="/nutlope-hallmark/">nutlope/hallmark</a>: the landing page builder',
  '<a href="/nextlevelbuilder-ui-ux-pro-max/">nextlevelbuilder/ui-ux-pro-max</a>: the searchable lookup']
def foot(D,extra=''):
    return f'Compiled 24 Oct 2026 from {D.repo} @ {D.pin}{extra} · every quote is checked against its source file at build time · not affiliated with the authors.'
_hero=hero
def hero(*a): return '<style>.hero h1,.hero .lede,.hero .thesis{overflow-wrap:anywhere}.hero{min-width:0}</style>'+_hero(*a)
