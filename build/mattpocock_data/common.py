# Shared pieces for the five mattpocock/<skill> explainers (same template as the other skill docs).
# Three quote sources, each checked at build time: the skills repo, the pstack plugin, and verbatim
# excerpts of the Matt Pocock x poteto stream committed under build/assets/mattpocock/.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skdoc import *
from config import src, ASSETS
PIN='5beb35b'
MB=f'https://github.com/mattpocock/skills/blob/{PIN}/'
def docs(slug):
    M=Doc(slug,src('MATTPOCOCK_SKILLS_SRC'),MB)
    ps=src('PSTACK_SRC'); h=subprocess.run('git rev-parse --short=7 HEAD',shell=True,capture_output=True,text=True,cwd=ps).stdout.strip() or 'main'
    P=Doc(slug,ps,f'https://github.com/cursor/plugins/blob/{h}/'); P.h=h
    T=Doc(slug,os.path.join(ASSETS,'mattpocock'),'https://www.youtube.com/watch?v=MN9dGgmLyso#')
    return M,P,T
TR='poteto-stream-excerpts.md'
VIDEO='https://www.youtube.com/watch?v=MN9dGgmLyso'
X_GRILL='https://x.com/mattpocockuk/status/2085413313672810740'
X_WAY='https://x.com/mattpocockuk/status/2090546341357183232'
SKSH='https://skills.sh/mattpocock/skills'
def sk(name): return {'grill-with-docs':'engineering','wayfinder':'engineering','to-spec':'engineering','to-tickets':'engineering','implement-spec':'engineering',
  'setup-matt-pocock-skills':'engineering','domain-modeling':'engineering','research':'engineering','prototype':'engineering','tdd':'engineering','code-review':'engineering','triage':'engineering',
  'grill-me':'productivity','grilling':'productivity','handoff':'productivity'}[name]
def SP(name,f='SKILL.md'): return f'skills/{sk(name)}/{name}/{f}'
def PP(name): return f'pstack/skills/{name}/SKILL.md'
def tq(T,q,when):
    """A transcript quote card."""
    return f'<p class="quote">“{T.Q(q,TR)}”<span class="qsrc">Lauren Tan (poteto), <a href="{VIDEO}">stream with Matt Pocock</a>, {when}</span></p>'
def pairs(P,rows):
    """rows: (pstack skill, exact fragment of its description, how it pairs)"""
    return table(['pstack skill','What pstack says it does','How it pairs'],
      [[f'<a href="{P.blob}{PP(n)}"><code>{n}</code></a>',f'“{P.Q(q,PP(n))}”',how] for n,q,how in rows],cls='dense fx')
def adoption(rows):
    return table(['Signal','Number','Source'],rows)
def foot(name):
    return f'Compiled 23 Oct 2026 from mattpocock/skills @ {PIN} (committed 19 Oct 2026) · install counts from skills.sh as of 23 Oct 2026 · every quote is checked against its source file at build time · not affiliated with Matt Pocock or Lauren Tan.'
NEXT_COMMON=[f'<a href="https://github.com/mattpocock/skills">github.com/mattpocock/skills</a>: the repo and its README',
  f'<a href="{SKSH}">skills.sh/mattpocock/skills</a>: install counts per skill',
  '<a href="https://docs.indrayam.com/pstack/">Inside pstack</a>: the pstack explainer on this site',
  f'<a href="{VIDEO}">Matt Pocock with poteto, live</a>: the stream quoted here']
# Long handle-style titles ("mattpocock/setup-matt-pocock-skills") have no spaces; let them wrap on narrow screens.
_hero=hero
def hero(*a): return '<style>.hero h1,.hero .lede,.hero .thesis{overflow-wrap:anywhere}.hero{min-width:0}</style>'+_hero(*a)
