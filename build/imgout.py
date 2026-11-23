"""Move inline base64 images out of a generated page into files next to it.

The gallery builders (gal.py's uri(), and the committed assets/*/gallery.json)
produce <img src="data:image/...;base64,...">. Inlined images can't be lazy-loaded
or cached and they block HTML parsing, so after each doc is built, build.py calls
externalize(slug): every data-URI src becomes site/<slug>/img/<content-hash>.<ext>
and the page references it relatively. Files no longer referenced are removed.

Usage on its own: python3 build/imgout.py <slug> [<slug> ...]
"""
import base64, hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SITE

EXT = {'webp': 'webp', 'png': 'png', 'jpeg': 'jpg', 'jpg': 'jpg', 'gif': 'gif', 'svg+xml': 'svg', 'avif': 'avif'}
DATA_SRC = re.compile(r'src="data:image/([a-z0-9+]+);base64,([A-Za-z0-9+/=]+)"')


def externalize(slug):
    page = os.path.join(SITE, slug, 'index.html')
    imgdir = os.path.join(SITE, slug, 'img')
    html = open(page, encoding='utf-8').read()
    written = set()

    def repl(m):
        kind, b64 = m.group(1), m.group(2)
        data = base64.b64decode(b64)
        name = hashlib.sha256(data).hexdigest()[:16] + '.' + EXT.get(kind, kind)
        if name not in written:
            os.makedirs(imgdir, exist_ok=True)
            path = os.path.join(imgdir, name)
            if not os.path.exists(path) or open(path, 'rb').read() != data:
                with open(path, 'wb') as f:
                    f.write(data)
            written.add(name)
        return f'src="img/{name}"'

    new = DATA_SRC.sub(repl, html)
    if new != html:
        with open(page, 'w', encoding='utf-8') as f:
            f.write(new)
    # Drop images from earlier builds that the page no longer uses.
    if os.path.isdir(imgdir):
        for f in os.listdir(imgdir):
            if f not in written and f'img/{f}"' not in new:
                os.remove(os.path.join(imgdir, f))
    return len(written)


if __name__ == '__main__':
    for s in sys.argv[1:]:
        print(f'{s}: {externalize(s)} images')
