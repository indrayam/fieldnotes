"""Paths for the build. Everything inside the repo is relative to this file.
External source repos come from env vars; defaults are the paths on Dorothy's box."""
import os, sys
BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
SITE = os.path.join(ROOT, 'site')
ASSETS = os.path.join(BUILD, 'assets')
SOURCES = {  # env var: (default, what to clone)
    'PSTACK_SRC': ('/workspace/src/plugins-latest', 'github.com/cursor/plugins (needs pstack/ inside, full git history)'),
    'DIAGRAM_DESIGN_SRC': ('/home/box/diagram-design', 'github.com/cathrynlavery/diagram-design @ 7a12007'),
    'ILLO_SRC': ('/home/box/illo-skill', 'github.com/tmchow/illo-skill @ 0b0abee'),
    'DRAWIO_SRC': ('/home/box/drawio-skill', 'github.com/jgraph/drawio-mcp @ 05c1747'),
    'PRETTY_MERMAID_SRC': ('/home/box/pretty-mermaid-skills', 'github.com/imxv/Pretty-mermaid-skills @ e234ab7'),
    'EXCALIDRAW_SRC': ('/home/box/mcp_excalidraw', 'github.com/yctimlin/mcp_excalidraw @ 774a70c'),
    'MATTPOCOCK_SKILLS_SRC': ('/workspace/dorothy-docs/_scratch/mattpocock-skills', 'github.com/mattpocock/skills @ 5beb35b'),
    'INDRAYAM_V1_SRC': ('/workspace/dorothy-docs/_src/indrayam-site/v1', 'the v1 folder of the indrayam.com site repo (needs style.css)'),
}
def src(var):
    default, what = SOURCES[var]
    p = os.environ.get(var, default)
    if not os.path.isdir(p):
        sys.exit(f'Missing source for {var}: {p} does not exist.\nClone {what} and set {var}=/path/to/it.')
    return p
def asset(slug, name): return os.path.join(ASSETS, slug, name)
def out(slug):
    p = os.path.join(SITE, slug, 'index.html'); os.makedirs(os.path.dirname(p), exist_ok=True); return p
