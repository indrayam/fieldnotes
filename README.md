# cribsheets.indrayam.com

Single-page explainers, each a self-contained HTML file. Edited from more than one machine and agent, so follow the sync rules in `AGENTS.md`.

## Layout
- `site/`: exactly what is deployed. One folder per doc (`site/<slug>/index.html`) plus the home page `site/index.html`.
- `build/`: generators. `build.py` is the entry point, `config.py` holds all paths, `skdoc.py`/`shell.py`/`explorer.py`/`gal.py`/`base.css` are the shared template, `<slug>_data/doc.py` (and `pst.py` + `pstack_data/` for pstack; `mattpocock_data/<skill>.py` + `mattpocock_data/common.py` for the Matt Pocock skills; `design_data/<skill>.py` + `design_data/common.py` for the Design Skills) hold each doc's content, `site_index.py` builds the home page, `assets/` holds committed images and gallery data.

## Deploys
Push to `main` and Vercel (project `indrayam-docs`, Root Directory `site`, no build step) deploys automatically. Nothing is built on Vercel; commit the generated `site/` files.

## Building
```
pip install -r build/requirements.txt     # Pillow
python3 build/build.py all                # or: pstack | diagram-design | illo | drawio | pretty-mermaid | excalidraw | mattpocock-<skill> | pbakaus-impeccable | nutlope-hallmark | nextlevelbuilder-ui-ux-pro-max | index
```
Each doc quotes its source repo and checks every quote at build time (build fails on a mismatch), so it needs that repo checked out at the commit named in the doc's footer. Point to them with env vars (defaults are the box paths):

| Var | Repo |
|---|---|
| `PSTACK_SRC` | github.com/cursor/plugins (contains `pstack/`, full history) |
| `DIAGRAM_DESIGN_SRC` | github.com/cathrynlavery/diagram-design @ 7a12007 |
| `ILLO_SRC` | github.com/tmchow/illo-skill @ 0b0abee |
| `DRAWIO_SRC` | github.com/jgraph/drawio-mcp @ 05c1747 |
| `PRETTY_MERMAID_SRC` | github.com/imxv/Pretty-mermaid-skills @ e234ab7 |
| `EXCALIDRAW_SRC` | github.com/yctimlin/mcp_excalidraw @ 774a70c |
| `MATTPOCOCK_SKILLS_SRC` | github.com/mattpocock/skills @ 5beb35b (the five `mattpocock-*` docs) |
| `IMPECCABLE_SRC` | github.com/pbakaus/impeccable @ 9368675 (`pbakaus-impeccable`) |
| `HALLMARK_SRC` | github.com/nutlope/hallmark @ 7ec8682 (`nutlope-hallmark`) |
| `UIUXPROMAX_SRC` | github.com/nextlevelbuilder/ui-ux-pro-max-skill @ 9a3f14f (`nextlevelbuilder-ui-ux-pro-max`) |
| `INDRAYAM_V1_SRC` | the `v1/` folder of the indrayam.com site (for `style.css`) |

A missing source stops the build with a message naming the var. You only need the sources for the docs you rebuild.

## Rules
- Hand edits in `site/` are fine for pages that are not generated.
- Generated docs (everything listed above): edit `build/`, then rebuild. A hand edit to their `site/` file is overwritten on the next rebuild.
- Check branch and working-tree state before editing; follow `AGENTS.md` for safe synchronization. Keep commits small; never force-push.
- No internal Cisco material (ai-native-assessment, ai-harness-setup, anything from work). `build.py` fails if it finds it.
- Content work stays in this repo; don't edit the sibling indrayam.com repos from here. Shared site chrome (header nav, footer, `style.css`, favicon) may change here as part of a cross-site update; see `AGENTS.md`.
