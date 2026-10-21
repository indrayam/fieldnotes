#!/usr/bin/env bash
# Rebuild docs.indrayam.com site from an explicit allowlist of PUBLIC slugs and redeploy.
# Never add ai-native-assessment / ai-harness-setup (internal Cisco material).
set -euo pipefail
ROOT=/workspace/dorothy-docs
SITE=$ROOT/_site
PUBLIC_SLUGS=(pstack diagram-design illo drawio pretty-mermaid excalidraw)
rm -rf "$SITE"; mkdir -p "$SITE"
for s in "${PUBLIC_SLUGS[@]}"; do mkdir -p "$SITE/$s"; cp "$ROOT/$s/index.html" "$SITE/$s/index.html"; done
python3 "$ROOT/_build/site_index.py" "$SITE"
# Shared favicon: /favicon.ico + inject into each doc page copy (source docs untouched)
cp "$SITE/images/favicon.ico" "$SITE/favicon.ico"
for s in "${PUBLIC_SLUGS[@]}"; do
  rg -qi 'rel="shortcut icon"|rel="icon"' "$SITE/$s/index.html" || sed -i '0,/<\/head>/s##<link rel="Shortcut Icon" href="/images/favicon.ico">\n</head>#' "$SITE/$s/index.html"
done
# Leak check
if rg -l -i 'detect\.py|hello-skills|ai-native-assessment|ai-harness-setup|cisco' "$SITE"; then echo "LEAK DETECTED - aborting"; exit 1; fi
# Deployment manifest (used by the Vercel connector: create_deployment, project indrayam-docs, team indrayam)
python3 - "$SITE" <<'P'
import json,os,sys
site=sys.argv[1]; files=[]
for d,_,fs in os.walk(site):
  for f in fs:
    p=os.path.join(d,f); r=os.path.relpath(p,site)
    if r=='manifest.json': continue
    files.append({"file":r,"encoding":"utf-8","data":"$file:"+p})
json.dump({"name":"indrayam-docs","project":"indrayam-docs","target":"production","projectSettings":{"framework":None,"buildCommand":None,"outputDirectory":None},"files":files},open('/workspace/dorothy-docs/_build/deploy-manifest.json','w'),indent=1)
P
echo "Site built at $SITE"
if command -v vercel >/dev/null && vercel whoami >/dev/null 2>&1; then
  cd "$SITE" && vercel deploy --prod --yes --scope indrayam --name indrayam-docs
else
  echo "vercel CLI not authenticated: deploy via Vercel connector create_deployment (team indrayam) using _build/deploy-manifest.json"
fi
