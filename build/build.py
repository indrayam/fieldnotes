"""Build docs.indrayam.com.  Usage: python3 build/build.py [slug|index|all]   (default: all)
Each doc is written to site/<slug>/index.html; 'index' rebuilds site/index.html."""
import os, sys, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BUILD, SITE
DOCS = {'pstack': 'pst.py', 'diagram-design': 'diagram-design_data/doc.py', 'illo': 'illo_data/doc.py',
        'drawio': 'drawio_data/doc.py', 'pretty-mermaid': 'pretty-mermaid_data/doc.py', 'excalidraw': 'excalidraw_data/doc.py',
        **{f'mattpocock-{k}': f'mattpocock_data/{k}.py' for k in ('grill-with-docs', 'wayfinder', 'to-spec-to-tickets', 'handoff', 'setup-matt-pocock-skills')},
        'index': 'site_index.py'}
LEAK = re.compile(r'hello-skills|ai-native-assessment|ai-harness-setup|detect\.py', re.I)
def run(slug):
    print(f'== {slug}', flush=True)
    r = subprocess.run([sys.executable, os.path.join(BUILD, DOCS[slug])], cwd=BUILD)
    if r.returncode: sys.exit(f'{slug}: build failed (exit {r.returncode})')
def leak_check():
    for d, _, fs in os.walk(SITE):
        for f in fs:
            if f.endswith('.html') and LEAK.search(open(os.path.join(d, f), encoding='utf-8').read()):
                sys.exit(f'LEAK: internal material in {os.path.join(d, f)}')
if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if arg != 'all' and arg not in DOCS: sys.exit(f'unknown slug {arg}; choose from: all, ' + ', '.join(DOCS))
    for s in (DOCS if arg == 'all' else [arg]): run(s)
    leak_check(); print('ok')
