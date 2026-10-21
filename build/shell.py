import re
CSS=open('/tmp/base.css').read()
CSS+="""
.v-bad{background:#f6dcdc;color:#7a1f1f}.v-warn{background:var(--gold-soft);color:#7a5208}
:root[data-theme="dark"] .v-bad{background:#3a1f22;color:#f0a8a8}:root[data-theme="dark"] .v-warn{color:var(--gold)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .v-bad{background:#3a1f22;color:#f0a8a8}:root:not([data-theme="light"]) .v-warn{color:var(--gold)}}
td.c,th.c{text-align:center}.tablewrap{max-width:100%;min-width:0}section{min-width:0}td code,th code{font-size:.8em}
table.dense{width:100%}table.dense td.nm{white-space:normal}table.dense td code{white-space:normal}table.fx{table-layout:fixed}table.dense td,table.dense th{overflow-wrap:anywhere;font-size:.86rem;vertical-align:top}
table.mx th{letter-spacing:0;font-size:.64rem;text-transform:none}table.mx td.y{background:var(--sky);color:var(--sky-ink);font-weight:600;text-align:center}
table.mx td.n{color:var(--ink-3);text-align:center}
tr.grp td{background:var(--code-bg);font-family:var(--f-display);font-weight:700;font-size:.82rem;letter-spacing:.04em}
.code pre{overflow-x:auto;max-width:100%}.code{max-width:100%}
.s0{color:var(--ink-3)}.s4{color:var(--sky-ink);font-weight:700}
"""
JS=r"""
function mk(t,c,txt){const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e}
document.querySelectorAll('.code').forEach(w=>{const b=mk('button','copy','Copy');b.type='button';b.onclick=async()=>{const t=w.querySelector('pre').innerText;try{await navigator.clipboard.writeText(t)}catch(e){const r=document.createElement('textarea');r.value=t;document.body.appendChild(r);r.select();document.execCommand('copy');r.remove()}b.textContent='Copied';b.classList.add('ok');setTimeout(()=>{b.textContent='Copy';b.classList.remove('ok')},1400)};w.appendChild(b)});
const tbn=document.getElementById('themeBtn'),root=document.documentElement,order=['system','light','dark'];
let th=root.getAttribute('data-theme')||'system';tbn.textContent='Theme: '+th;
tbn.onclick=()=>{th=order[(order.indexOf(th)+1)%3];if(th==='system')root.removeAttribute('data-theme');else root.setAttribute('data-theme',th);try{localStorage.setItem('dd-theme',th)}catch(e){}tbn.textContent='Theme: '+th};
document.querySelectorAll('[data-filter]').forEach(box=>{const tb=document.getElementById(box.dataset.filter);const chips=[...box.querySelectorAll('.chip')];chips.forEach(c=>c.onclick=()=>{chips.forEach(x=>x.setAttribute('aria-pressed',x===c));const k=c.dataset.k;[...tb.rows].forEach(r=>{r.style.display=(k==='all'||r.dataset.k===k)?'':'none'})})});
const links=[...document.querySelectorAll('#railList a')],secs=links.map(a=>document.querySelector(a.getAttribute('href')));
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){const i=secs.indexOf(e.target);links.forEach((l,j)=>l.classList.toggle('on',i===j))}})},{rootMargin:'-20% 0px -70% 0px'});
secs.forEach(s=>s&&io.observe(s));
"""
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def code(s,cap=None): return f'<div class="code"><pre>{esc(s)}</pre></div>'+(f'<p class="figcap">{cap}</p>' if cap else '')
DEFAULT_FOOT=""
def page(title,eyebrow,nav,body,footer=None,extra_js=''):
    lis=''.join(f'<li><a href="#{i}"{" class=\"on\"" if n==0 else ""}>{t}</a></li>' for n,(i,t) in enumerate(nav))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=JetBrains+Mono:wght@400;600&display=swap">
<script>(function(){{try{{var t=localStorage.getItem('dd-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<style>{CSS}</style></head><body><div class="shell">
<nav class="rail" aria-label="Sections"><div class="eyebrow">{eyebrow}</div><ol id="railList">{lis}</ol>
<button class="theme-btn" id="themeBtn" type="button">Theme: system</button></nav>
<main>{body}
<footer>{footer or DEFAULT_FOOT}</footer>
</main></div><script>{JS}{extra_js}</script></body></html>'''
