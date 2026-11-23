import base64,io,html
from PIL import Image
def uri(path,maxw=640,q=72,bg=None):
    im=Image.open(path)
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA')
        if bg: b=Image.new('RGBA',im.size,bg);b.alpha_composite(im);im=b.convert('RGB')
    else: im=im.convert('RGB')
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    buf=io.BytesIO();im.save(buf,format='WEBP',quality=q,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
GCSS='''<style>.gimg.one .gi-l{display:block!important}.gimg.one .gi-d{display:none!important}
.gal.sm{grid-template-columns:repeat(auto-fill,minmax(170px,1fr))}.gal.sm .gimg img{height:150px}.gal.sm .gbody{padding:10px 12px 12px;gap:4px}.gal.sm .gbody h3{font-size:.95rem}.gal.sm .gbody p{font-size:.78rem;line-height:1.4}
.gal.wide{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}.gal.wide .gimg img{height:230px}
.gimg.dark{background:#1e1e1e!important}.gbody .meta{font-family:var(--f-display);font-size:.74rem;color:var(--ink-3)}
pre.ascii{font-size:.72rem;line-height:1.2;max-height:340px;overflow:auto;margin:0;padding:12px;background:var(--code-bg);border-radius:8px}
dialog.lb img{max-height:80vh}</style>'''
def card(o):
    e=html.escape
    il=o['il'];idk=o.get('id')
    cls='gimg'+('' if idk else ' one')+(' dark' if o.get('darkbg') else '')
    imgs=f'<img class="gi-l" src="{il}" alt="{e(o["n"])}">'+(f'<img class="gi-d" src="{idk}" alt="{e(o["n"])} (dark)">' if idk else '')
    pill=f'<span class="pill">{e(o["tag"])}</span>' if o.get('tag') else ''
    meta=f'<div class="meta">{o["meta"]}</div>' if o.get('meta') else ''
    d=f'<p>{o["d"]}</p>' if o.get('d') else ''
    return f'<article class="gcard" data-k="{e(o.get("k",""))}"><button type="button" class="{cls}" data-cap="{e(o.get("cap",o["n"]))}" aria-label="Enlarge {e(o["n"])}">{imgs}</button><div class="gbody"><h3>{e(o["n"])}{pill}</h3>{d}{meta}</div></article>'
def gallery(gid,items,cls=''):
    return f'<div class="gal {cls}" id="{gid}">'+''.join(card(o) for o in items)+'</div>'
def chips(gid,keys):
    return f'<div class="chips" data-gfilter="{gid}"><button type="button" class="chip" data-k="all" aria-pressed="true">All</button>'+''.join(f'<button type="button" class="chip" data-k="{k}" aria-pressed="false">{html.escape(lbl)}</button>' for k,lbl in keys)+'</div>'
LB='<dialog class="lb" id="lb" aria-labelledby="lbcap"><div class="lbin" id="lbin"><img id="lbimg" alt=""><div class="lbbar"><span id="lbcap"></span><span><button type="button" id="lbswap">Light / dark</button> <button type="button" id="lbx">Close</button></span></div></div></dialog>'
GJS=r'''
(function(){const lb=document.getElementById('lb');if(!lb)return;const im=document.getElementById('lbimg'),cap=document.getElementById('lbcap'),sw=document.getElementById('lbswap'),lbin=document.getElementById('lbin');let cur=null,dk=false;
function isDark(){const t=document.documentElement.getAttribute('data-theme');return t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches)}
function show(){const l=cur.querySelector('.gi-l'),d=cur.querySelector('.gi-d');const useD=dk&&d;im.src=(useD?d:l).src;im.alt=(useD?d:l).alt;lbin.classList.toggle('dk',!!(useD||cur.classList.contains('dark')));cap.textContent=cur.dataset.cap+(d?(useD?' · dark':' · light'):'');sw.style.display=d?'':'none'}
document.querySelectorAll('.gimg').forEach(b=>b.onclick=()=>{cur=b;dk=isDark();show();lb.showModal();document.getElementById('lbx').focus()});
lb.addEventListener('close',()=>{if(cur&&cur.isConnected)cur.focus()});
sw.onclick=()=>{dk=!dk;show()};document.getElementById('lbx').onclick=()=>lb.close();lb.addEventListener('click',e=>{if(e.target===lb)lb.close()});
document.querySelectorAll('[data-gfilter]').forEach(box=>{const g=document.getElementById(box.dataset.gfilter);const cs=[...box.querySelectorAll('.chip')];cs.forEach(c=>c.onclick=()=>{cs.forEach(x=>x.setAttribute('aria-pressed',x===c));const k=c.dataset.k;[...g.children].forEach(a=>{a.style.display=(k==='all'||a.dataset.k.split(' ').includes(k))?'':'none'})})});})();
'''
