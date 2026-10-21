import sys,json,os,html; sys.path.insert(0,'/workspace/dorothy-docs/_build')
from shell import *; from gal import *
R='/home/box/illo-skill/'; SK=R+'skills/illo/'
U='<span class="unc">uncertain</span>'
def C(f,l): return f'<code>{f} L{l}</code>'
P=json.load(open('/tmp/packs.json'))
STY={'bloom':'Flat cel character in a soft, lit painterly scene','blueprint':'White draftsman linework on a blueprint ground','bricks':'Photo of a world built from toy bricks (the photoreal one)','chalk':'White chalk on a slate board','clay':'Stop-motion plasticine on a paper-craft set','diorama':"Children's-book isometric tabletop diorama",'enamel':'Hard-enamel pin, flat glossy cells, raised metal line','felt':'Layered wool-felt cutouts','fizz':'90s soda-pop psychedelic screenprint','gouache':'Mid-century gouache poster','manila':'Rubber-stamped ink on a manila folder','phosphor':'Glowing CRT vector trace on black glass','pixel':'Chunky 4-colour pixel art','riso':'Risograph: grainy halftone, ink-layer offset (house default)','sketchbook':'Pencil-and-ink editorial cartoon sketch','snes':'16-bit console sprite with dither','woodcut':'Relief print, black + one off-register accent'}
nav=[('top','Overview'),('flow','Pipeline'),('routes','Request routing'),('backends','Backends'),('packs','Character packs'),('styles','The 17 looks'),('examples','Repo examples'),('engine','illo.py commands'),('run','What I ran'),('risks','Side effects and caveats'),('sources','Sources')]
hero=f'''<header class="hero" id="top">
<div class="eyebrow">A skill reference · illo 0.37.0 · tmchow/illo-skill @ 0b0abee (2026-09-21) · read 20 Oct 2026</div>
<h1>Illo</h1>
<p class="thesis">A <mark>prompt-building skill</mark> around an image model: a recurring mascot performs the idea, in one locked look per character.</p>
<p class="lede">illo is mostly prose (SKILL.md 780 lines plus 3,343 lines of references) that tells the agent how to turn an idea into one editorial illustration, a labelled explainer, or a transparent cutout. The actual pixels come from an external image model: Codex CLI, Grok CLI, OpenRouter (paid), or the agent's own built-in image tool. <code>scripts/illo.py</code> (2,309 lines, stdlib Python) handles config, backend choice, rendering calls, chroma-key cutouts, a manifest, an HTML gallery, and community character packs.</p>
<div class="facts" role="list">
<div class="fact" role="listitem"><b>57</b><span>community packs, <b>verified</b>: <code>illo.py packs list</code> printed 57 entries from the live <code>index.json</code>; 57 folders installed in <code>~/.config/illo/characters/</code>. Plus the shipped default Blot = 58 characters</span></div>
<div class="fact" role="listitem"><b>17</b><span>looks: 16 style files in <code>references/styles/</code> + riso (<code>visual-style.md</code>); SKILL.md frontmatter L8–9 "seventeen bundled looks"</span></div>
<div class="fact" role="listitem"><b>5</b><span>backend values: <code>BACKENDS</code> {C('illo.py',97)} codex, grok, openrouter, grok-bot, muse-native</span></div>
<div class="fact" role="listitem"><b>2,309</b><span>lines in <code>scripts/illo.py</code>; 9 subcommands ({C('illo.py','2197–2300')})</span></div>
<div class="fact" role="listitem"><b>121</b><span>unittest cases in <code>tests/</code> (8 files), all pass, 0.5 s</span></div>
<div class="fact" role="listitem"><b>236</b><span>commits; 214 by Trevin Chow, 21 release bot, 1 other (<code>git log</code>)</span></div>
</div>
<div class="where">
<div class="note"><h4>Where it lives</h4><p>Clone at <code>/home/box/illo-skill</code>, remote <code>https://github.com/tmchow/illo-skill</code>. Skill at <code>skills/illo/</code>: SKILL.md, <code>scripts/</code> (illo.py, diagram_route.py 780, repair-hermes-assets.sh), <code>references/</code> (13 + 16 styles), <code>assets/</code> (Blot sheet <code>character-reference.webp</code>, a pixel variant, checksums). MIT, author Trevin Chow, homepage illo-skill.com (frontmatter L18–26).</p></div>
<div class="note"><h4>What it is not</h4><p>Not a renderer. There is no local drawing code: every image is a model call. Quality and consistency come from the prompt recipe (locked character spec, contact map, palette hexes) plus the character sheet passed as a reference image. Results vary per call; the docs plan for rerolls and QA (step 6, L683).</p></div>
<div class="note"><h4>This box</h4><p><code>~/.config/illo/config.yaml</code> exists (mode 600) with <code>backend: grok-bot</code> and no API key. <code>doctor</code>: codex and grok CLIs absent, assets OK, all 57 packs readable.</p></div>
</div></header>'''
fig=f'''<section id="flow"><div class="sec-head"><div class="eyebrow">Pipeline</div><h2>From an idea to one image</h2><p>The SKILL.md workflow (L217–765), steps 0–7.</p></div>
<div class="figure"><svg viewBox="0 0 1000 300" role="img" aria-labelledby="iT iD"><title id="iT">illo workflow</title><desc id="iD">Preflight, read input, resolve character, plan, resolve palette, generate with reference, QA, deliver.</desc>
<defs><marker id="m1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<rect class="bx" x="10" y="40" width="150" height="90" rx="8"/><text class="t" x="22" y="66">0 Preflight</text><text class="tm" x="22" y="86">illo.py doctor</text><text class="tm" x="22" y="104">backend, assets</text><text class="tm" x="22" y="122">L219</text>
<rect class="bx" x="180" y="40" width="150" height="90" rx="8"/><text class="t" x="192" y="66">1 Read input</text><text class="tm" x="192" y="86">≤3 questions if thin</text><text class="tm" x="192" y="104">article → routing</text><text class="tm" x="192" y="122">L391</text>
<rect class="bx-skin" x="350" y="40" width="150" height="90" rx="8"/><text class="t" x="362" y="66">2 Character</text><text class="tm" x="362" y="86">Blot or a pack</text><text class="tm" x="362" y="104">pack fixes the look</text><text class="tm" x="362" y="122">L440</text>
<rect class="bx" x="520" y="40" width="150" height="90" rx="8"/><text class="t" x="532" y="66">3 Plan · 4 Palette</text><text class="tm" x="532" y="86">shot list</text><text class="tm" x="532" y="104">ink-punch default</text><text class="tm" x="532" y="122">L478 · L498</text>
<rect class="bx-hot" x="690" y="40" width="150" height="90" rx="8"/><text class="t" x="702" y="66">5 Generate</text><text class="tm" x="702" y="86">prompt-recipe +</text><text class="tm" x="702" y="104">sheet as --ref</text><text class="tm" x="702" y="122">L517</text>
<rect class="bx" x="860" y="40" width="130" height="90" rx="8"/><text class="t" x="872" y="66">6 QA · 7 Deliver</text><text class="tm" x="872" y="86">quality-bar.md</text><text class="tm" x="872" y="104">reroll / gallery</text><text class="tm" x="872" y="122">L683 · L696</text>
<path class="ar" d="M160 85 H178" marker-end="url(#m1)"/><path class="ar" d="M330 85 H348" marker-end="url(#m1)"/><path class="ar" d="M500 85 H518" marker-end="url(#m1)"/><path class="ar" d="M670 85 H688" marker-end="url(#m1)"/><path class="ar" d="M840 85 H858" marker-end="url(#m1)"/>
<rect class="zone" x="560" y="170" width="430" height="110" rx="10"/><text class="lab" x="576" y="194">Step 5 render paths</text>
<text class="tm" x="576" y="218">illo.py generate → codex exec / grok -p / OpenRouter HTTP</text>
<text class="tm" x="576" y="240">or agent-side: the agent's own image tool (grok-bot, muse-native)</text>
<text class="tm" x="576" y="262">then illo.py record → manifest; gallery → index.html</text>
<path class="ar-d" d="M765 130 V168" marker-end="url(#m1)"/>
<rect class="zone" x="10" y="170" width="520" height="110" rx="10"/><text class="lab" x="26" y="194">What the prompt carries (prompt-recipe.md)</text>
<text class="tm" x="26" y="218">one idea · composition/staging · locked CHARACTER spec</text>
<text class="tm" x="26" y="240">INTERACTION GEOMETRY contact map · LINE · STYLE</text>
<text class="tm" x="26" y="262">PALETTE hexes · TEXT HIERARCHY (1–3 items, or none)</text>
</svg></div></section>'''
routes=f'''<section id="routes"><div class="sec-head"><div class="eyebrow">SKILL.md L67–85</div><h2>Request routing</h2><p>The "Use cases" table maps a request to a register. Summarised:</p></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Request</th><th>Path</th></tr></thead><tbody>
<tr><td>Illustrate an article / URL</td><td>Source routing in <code>composition.md</code>: hero, hero + set, set, or mini-comic; one image per anchor</td></tr>
<tr><td>One concept</td><td>Up to ~3 quick questions if thin, then one image</td></tr>
<tr><td>"surprise me" [--autopick]</td><td><code>surprise.md</code> (547 lines): roll provenance, three candidate sayings, pick, render one</td></tr>
<tr><td>Sequence / before→after</td><td>One mini-comic</td></tr>
<tr><td>"show the flow", labelled stages</td><td>Explainer register: hand-built labelled stages / fan-out / timeline / loop / stack in the pack's look. <code>scripts/diagram_route.py</code> (780 lines) routes the type</td></tr>
<tr><td>X post / X Article banner</td><td>16:9 ink-punch; banner is 1536 × 640</td></tr>
<tr><td>Own mascot / new look</td><td><code>character-builder.md</code>; a new look = sibling "style variant pack" <code>&lt;name&gt;-&lt;style&gt;</code></td></tr>
<tr><td>Community characters</td><td><code>pack-sharing.md</code>, <code>packs list/show/install/update</code></td></tr>
<tr><td>Transparent cutout / idle GIF</td><td><code>cutout.md</code>, <code>--cutout --aspect 1:1</code>; programmatic motion on the PNG</td></tr>
</tbody></table></div>
<p class="figcap">Trigger rule (frontmatter L13–14): only when the skill is invoked directly or "illo" is named; never on generic "draw an image" requests.</p></section>'''
backends=f'''<section id="backends"><div class="sec-head"><div class="eyebrow">SKILL.md L87–156 · illo.py L381–405 · backends.md (381 lines)</div><h2>Backends</h2><p>Resolution ({C('illo.py','381–405')}): <code>--backend</code> &gt; config <code>backend:</code> &gt; capability default (Codex CLI, then Grok CLI, then OpenRouter key, else onboarding).</p></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Backend</th><th>How it renders</th><th>Cost</th><th>Cutouts</th></tr></thead><tbody>
<tr><td><code>codex</code></td><td>Shells out to the user's Codex CLI (<code>codex_exec_generate</code> L1230); gpt-image-2</td><td>Codex quota</td><td>Native alpha</td></tr>
<tr><td><code>grok</code></td><td><code>grok -p</code> headless (L1340); no model selector</td><td>Grok quota</td><td>No: JPEG, falls back</td></tr>
<tr><td><code>openrouter</code></td><td>HTTP to <code>openrouter.ai/api/v1/chat/completions</code> or <code>/images</code> (L34–35); default model <code>x-ai/grok-imagine-image-quality</code> (L72)</td><td><b>Paid</b> per image</td><td>Chroma key; default model gpt-5.4-image-2 (L74)</td></tr>
<tr><td><code>grok-bot</code></td><td>Agent-side: the agent calls its own image tool with the sheet as reference, then <code>illo.py record</code></td><td>Free</td><td>Not native (SKILL L284 contrasts with Muse) {U}</td></tr>
<tr><td><code>muse-native</code></td><td>Agent-side, Meta's Muse/Blip assistant</td><td>Free</td><td>Yes (L284)</td></tr>
</tbody></table></div>
<div class="callouts"><div class="callout"><span class="n">1</span><p><b>Key handling.</b> OpenRouter key lives only in <code>~/.config/illo/config.yaml</code> (mode 600), written by the user-run <code>init</code>. The engine never reads it from env or argv (L141–147, "Setup is the user's job" L157).</p></div>
<div class="callout"><span class="n">2</span><p><b>No silent spend.</b> A failed Codex/Grok render does not fall back to OpenRouter unless <code>--allow-paid-fallback</code> is passed (L147–148).</p></div>
<div class="callout"><span class="n">3</span><p><b>Small wording conflict.</b> SKILL L140–141 says Grok Bot is "not an <code>illo.py --backend</code> value", yet <code>BACKENDS</code> (L97) includes <code>grok-bot</code> and L248 runs <code>init --backend grok-bot</code>. It is a config value for <code>doctor</code>/<code>record</code>, not a <code>generate</code> path.</p></div></div>
<p class="figcap">SKILL.md contains instructions addressed to specific agents (Grok Bot, Muse, Hermes). This page only describes them.</p></section>'''
blot={'n':'Blot','tag':'riso','k':'riso','il':uri(SK+'assets/character-reference.webp',420,70),'d':'Shipped default: a plump ink-droplet, dot eyes, pink tip (<code>character.md</code> L146–196).','meta':'bundled · assets/character-reference.webp','cap':'Blot · shipped default'}
items=[blot]+[{'n':o['n'],'tag':o['s'],'k':o['s'],'il':uri(os.path.expanduser(f"~/.config/illo/characters/{o['n']}/reference.png"),360,66),'d':html.escape(o['d'].split(' (aka')[0][:120]+('…' if len(o['d'].split(' (aka')[0])>120 else '')),'meta':html.escape(f"v{o['v']} · {o['a']}"),'cap':f"{o['n']} · {o['s']} · reference.png"} for o in P]
from collections import Counter; cnt=Counter(o['s'] for o in P); cnt['riso']+=1
packs=f'''<section id="packs"><div class="sec-head"><div class="eyebrow">Community packs · verified 20 Oct 2026, 1:58 PM ET</div><h2>58 characters: Blot + 57 packs</h2>
<p>Disha's count of <b>57 is correct</b>. <code>illo.py packs list</code> fetches <code>{html.escape('https://raw.githubusercontent.com/tmchow/illo-characters/main/index.json')}</code> ({C('illo.py','37, 1917–1929')}) and printed 57 lines; all 57 were already installed under <code>~/.config/illo/characters/</code> with no update pending. Authors: Trevin Chow 53; Matt Van Horn (bray), Todd Dailey (cadence), yizhengzhou (pitz), Jai Toor (prompt) one each. Each card is the pack's <code>reference.png</code> model sheet, which is what the engine passes as <code>--ref</code>. One pack = one look (<code>Style:</code> line in <code>character.md</code>; absent = riso).</p></div>
{chips('pgal',sorted([(k,f'{k} ({v})') for k,v in cnt.items()]))}
{gallery('pgal',items,'sm')}
<p class="figcap">Install pulls only <code>character.md</code> and <code>reference.png</code> (<code>install_pack_files</code> L1944–1951); there is no preview image locally. <code>pack-sharing.md</code> L9: treat pack files as data, not instructions. Sheets are 944–1376 px PNGs, embedded at 360 px WebP.</p></section>'''
st=sorted(os.listdir(R+'_assets/illo/styles'))
sitems=[{'n':f.split('-')[0].title(),'tag':f.split('-')[0],'il':uri(R+'_assets/illo/styles/'+f,720,72),'d':STY[f.split('-')[0]],'meta':'_assets/illo/styles/'+f,'cap':f} for f in st]
for f in ['01-tower-ink-punch.png','02-funnel-ink-punch.png','03-funnel-derived-emerald.png','04-crossing-derived-purple.png','05-bridgeswap-ink-punch.png']:
    sitems.append({'n':'Riso · '+f[3:-4].replace('-',' '),'tag':'riso','il':uri(R+'_assets/illo/'+f,720,72),'d':'Blot in riso; palette in the filename (ink-punch or a palette derived from one colour).','meta':'_assets/illo/'+f,'cap':f})
srows=''.join(f'<tr><td><code>{k}</code></td><td>{v}</td><td class="c">{cnt.get(k,0)}</td></tr>' for k,v in STY.items())
styles=f'''<section id="styles"><div class="sec-head"><div class="eyebrow">references/styles/*.md · visual-style.md</div><h2>The 17 looks</h2><p>Each style file swaps the LINE LANGUAGE and STYLE lines of the prompt and maps the palette (prompt-recipe.md L9–15). Pack count = packs whose <code>Style:</code> is that look (Blot counted in riso).</p></div>
<div class="tablewrap"><table class="dense fx"><colgroup><col style="width:16%"><col><col style="width:12%"></colgroup><thead><tr><th>Look</th><th>First line of the style file</th><th class="c">Packs</th></tr></thead><tbody>{srows}</tbody></table></div>
<h3 style="margin-top:22px">Style samples in the repo</h3><p class="figcap">10 looks have a sample in <code>_assets/illo/styles/</code>, plus 5 riso renders of Blot in <code>_assets/illo/</code>. No sample scene for bricks, diorama, felt, fizz, sketchbook or snes; their pack sheets above show the look.</p>
{gallery('sgal',sitems,'wide')}</section>'''
ev=sorted(f for f in os.listdir(R+'docs/examples') if f.endswith('.png'))
EVD={'eval-blip-newsletter.png':'"Using Blip, make a flowchart of how a newsletter issue ships"','eval-blip-fanout.png':'"Sort incoming mail into keep, later, and trash as a fan-out, using Blip"','eval-forge-pipeline.png':'"Diagram the pipeline from a raw idea to a shipped tool. Use Forge."','eval-spritz-party.png':'"Walk the stages of throwing a last-minute dinner party, using Spritz"','eval-fathom-loop.png':'"Map the loop of investigating a weird production bug, using Fathom"','eval-sulk-bloom.png':'"Labeled stages of a mood becoming a small bloom, using Sulk"'}
eitems=[{'n':f[5:-4],'tag':'explainer','il':uri(R+'docs/examples/'+f,760,72),'d':'Prompt: '+html.escape(EVD[f]),'meta':'docs/examples/'+f,'cap':f} for f in ev]
cd=R+'_assets/illo/cutout-alpha-comparison/'
citems=[{'n':f.rsplit('.',1)[0],'tag':'cutout','il':uri(cd+f,420,72,bg=(200,200,200,255)),'d':'Same cutout prompt per backend; transparency shown on grey.','meta':'_assets/illo/cutout-alpha-comparison/'+f,'cap':f} for f in sorted(os.listdir(cd)) if f.endswith(('.png','.jpg'))]
examples=f'''<section id="examples"><div class="sec-head"><div class="eyebrow">docs/examples · _assets/illo/cutout-alpha-comparison</div><h2>Repo examples: explainers and cutouts</h2><p>Six explainer-register evals (prompts from <code>docs/examples/README.md</code>) and the cutout backend comparison. All are committed model outputs, not renders I made.</p></div>
{gallery('egal',eitems,'wide')}<h3 style="margin-top:22px">Cutout alpha comparison</h3>{gallery('cgal',citems)}</section>'''
engine=f'''<section id="engine"><div class="sec-head"><div class="eyebrow">scripts/illo.py main() L2197</div><h2>illo.py commands</h2></div>
<div class="tablewrap"><table class="dense"><thead><tr><th>Command</th><th>Does</th><th>Line</th></tr></thead><tbody>
<tr><td><code>generate</code></td><td>Render one image via codex / grok / openrouter; <code>--ref</code>, <code>--aspect</code>, <code>--cutout</code>, <code>--count</code>, <code>--model</code>, <code>--allow-paid-fallback</code></td><td>2201 · 1413</td></tr>
<tr><td><code>init</code></td><td>Write config (user runs it; key prompt)</td><td>2232 · 1615</td></tr>
<tr><td><code>doctor</code></td><td>Preflight: python, config, backend readiness, packs, asset checksums</td><td>2245 · 1760</td></tr>
<tr><td><code>newrun</code></td><td>Make <code>/tmp/illo/&lt;runid&gt;</code></td><td>2248 · 1883</td></tr>
<tr><td><code>packs list|show|install [--all]|update</code></td><td>Community packs from <code>index.json</code>; install fetches both files before writing</td><td>2251–2272 · 1954–2080</td></tr>
<tr><td><code>gallery [--embed]</code></td><td>Self-contained <code>index.html</code> from a run's manifest</td><td>2274 · 2081</td></tr>
<tr><td><code>keyout</code></td><td>Chroma-key an agent-side render to transparent PNG (pure-Python PNG decode, L473–710)</td><td>2283 · 2149</td></tr>
<tr><td><code>record</code></td><td>Append a manifest entry for an agent-side render</td><td>2294 · 2171</td></tr>
</tbody></table></div></section>'''
run=f'''<section id="run"><div class="sec-head"><div class="eyebrow">Run on the box, 20 Oct 2026, ~1:58 PM ET</div><h2>What I ran</h2></div>
{code("""cd /home/box/illo-skill/skills/illo
timeout 60 nice python3 scripts/illo.py packs list | wc -l     # 57 (network read of index.json)
ls ~/.config/illo/characters | wc -l                          # 57
timeout 60 nice python3 scripts/illo.py doctor
#  backend: grok-bot — transport: agent-side native Grok Bot image tool
#  codex cli: not installed · grok cli: not installed · api key: not set · assets: OK
cd /home/box/illo-skill && timeout 300 nice python3 -m unittest discover -s tests
#  Ran 121 tests in 0.515s  OK""")}
<p>To check the render path, I made one image the way the grok-bot transport describes: the prompt-recipe template filled for Blot, ink-punch palette, with <code>assets/character-reference.webp</code> as the reference. Blot stayed on-model (droplet, dot eyes, pink tip only) and the single label "ONE GATE" rendered cleanly. The image tool saves its output outside the box, so it isn't embedded here (attached to the report instead). I did not use <code>illo.py generate</code>: there is no Codex/Grok CLI here, and OpenRouter costs money.</p></section>'''
risks=f'''<section id="risks"><div class="sec-head"><div class="eyebrow">Side effects and caveats</div><h2>Things to know before running it</h2></div>
<div class="callouts">
<div class="callout"><span class="n">1</span><p><b>Network.</b> <code>packs list/show/install/update</code> fetch from raw.githubusercontent.com (60 s timeout, L1902–1914). OpenRouter calls are paid; <code>fetch_cost</code> (L1051) polls the generation cost.</p></div>
<div class="callout"><span class="n">2</span><p><b>Writes.</b> Config and packs under <code>~/.config/illo/</code>; runs in <code>/tmp/illo/&lt;runid&gt;</code>. Codex/Grok paths pick up the "freshest generated image" from those CLIs' output dirs (L1174, L1315), which could race with another session {U}.</p></div>
<div class="callout"><span class="n">3</span><p><b>Non-determinism.</b> Same prompt, different image. The skill's answer is variations (<code>--count</code>), a QA bar (<code>quality-bar.md</code>, 288 lines) and rerolls, not reproducibility.</p></div>
<div class="callout"><span class="n">4</span><p><b>Pack trust.</b> A pack's <code>character.md</code> is pasted into prompts. Community packs come via GitHub PRs to tmchow/illo-characters; <code>packs show</code> lets you read one before install.</p></div>
<div class="callout"><span class="n">5</span><p><b>Hermes.</b> <code>scripts/repair-hermes-assets.sh</code> and SKILL L174 repair binary assets that the Hermes agent runtime corrupts (checksums in <code>assets/checksums.txt</code>).</p></div>
</div></section>'''
srcs=f'''<section id="sources"><div class="sec-head"><div class="eyebrow">Sources</div><h2>Sources</h2></div><div class="srcs"><ul>
<li><code>skills/illo/SKILL.md</code> (780) · <code>scripts/illo.py</code> (2309) · <code>scripts/diagram_route.py</code> (780)</li>
<li><code>references/</code>: backends 381, character 221, character-builder 270, composition 623, cutout 311, models 104, pack-sharing 127, palettes 104, prompt-recipe 206, quality-bar 288, surprise 547, visual-style 77, article-set-character-reroute 84; <code>styles/*.md</code> (16)</li>
<li><code>tests/</code> 8 files · <code>_assets/illo/</code> · <code>docs/examples/</code></li>
<li><code>git log</code>: 236 commits, first de5f8ba 2026-05-19, head 0b0abee 2026-09-21 "release 0.37.0"</li>
<li>Live: <code>illo.py packs list</code> (index.json), <code>~/.config/illo/characters/*/character.md</code> for each pack's <code>Style:</code></li></ul></div></section>'''
foot='Built 20 Oct 2026 from <code>/home/box/illo-skill</code> @ 0b0abee and the installed packs. Images are the repo\'s and the packs\' own files, re-encoded as WebP.'
h=page('Inside Illo','Inside Illo',nav,GCSS+hero+fig+routes+backends+packs+styles+examples+engine+run+risks+srcs+LB,footer=foot,extra_js=GJS)
open('/workspace/dorothy-docs/illo/index.html','w').write(h);print(len(h))
