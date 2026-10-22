# Shared builder for the explorer-style skill explainers (same template as pst.py / Inside pstack).
# A doc lives in build/<slug>_data/doc.py and uses the helpers below. Every quote goes through Doc.Q,
# which checks it against its source file and makes the build fail on any mismatch.
import sys,os,re,json,subprocess,html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from shell import page, esc, code
from explorer import explorer, data_js
from gal import uri, GCSS, LB, GJS
BUILD=os.path.dirname(os.path.abspath(__file__))
def plain(s):
    s=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',s)
    s=s.replace('**','').replace('`','').replace('\\','')
    s=re.sub(r'(?<![\w*])\*(?!\s)([^*\n]+?)\*(?!\w)',r'\1',s)
    s=re.sub(r'(?<![\w_])_([^_\n]+?)_(?![\w])',r'\1',s)
    return re.sub(r'\s+',' ',s).strip()
def md(s):
    s=esc(s)
    s=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<![\w*])\*(?!\s)([^*\n]+?)\*(?!\w)',r'<i>\1</i>',s)
    return s
class Doc:
    def __init__(s,slug,root,blob,tree=None):
        s.slug,s.root,s.blob,s.tree=slug,root,blob,tree or blob.replace('/blob/','/tree/')
        s.BAD=[];s._c={}
    def sh(s,c,cwd=None): return subprocess.run(c,shell=True,capture_output=True,text=True,cwd=cwd or s.root).stdout.strip()
    def rd(s,p):
        if p not in s._c: s._c[p]=open(os.path.join(s.root,p),encoding='utf-8',errors='replace').read()
        return s._c[p]
    def ok(s,q,p): return plain(q) in plain(s.rd(p))
    def Q(s,q,p):
        if not s.ok(q,p): s.BAD.append((p,q))
        return md(q)
    def qs(s,lst,p): return [[s.Q(q,p),p] for q in lst]
    def L(s,p,t=None): return f'<a href="{s.blob}{p}">{t or esc(p)}</a>'
    def lines(s,p): return s.rd(p).count('\n')
    def finish(s):
        if s.BAD:
            for p,q in s.BAD: print('QUOTE NOT FOUND',p,repr(q[:110]))
            sys.exit(1)
def head(eyebrow,h2,p=''): return f'<div class="sec-head"><div class="eyebrow">{eyebrow}</div><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}</div>'
def sec(i,eyebrow,h2,p,body): return f'<section id="{i}">{head(eyebrow,h2,p)}{body}</section>'
def wordmark(t,i): return f'{esc(t[:i])}<span class="p">{esc(t[i])}</span>{esc(t[i+1:])}'
def hero(eyebrow,title,li,thesis,lede,facts,notes):
    f=''.join(f'<div class="fact" role="listitem"><b>{a}</b><span>{b}</span></div>' for a,b in facts)
    n=''.join(f'<div class="note"><h4>{a}</h4><p>{b}</p></div>' for a,b in notes)
    return f'''<header class="hero" id="top"><div class="eyebrow">{eyebrow}</div><h1>{wordmark(title,li)}</h1>
<p class="thesis">{thesis}</p><p class="lede">{lede}</p><div class="facts" role="list">{f}</div><div class="where">{n}</div></header>'''
def callouts(lst): return '<div class="callouts">'+''.join(f'<div class="callout"><span class="n">{i+1}</span><p>{x}</p></div>' for i,x in enumerate(lst))+'</div>'
def notes(lst): return '<div class="where">'+''.join(f'<div class="note"><h4>{a}</h4><p>{b}</p></div>' for a,b in lst)+'</div>'
V={'Copy':'v-good','Cost':'v-cost','Port':'v-port','Bug':'v-bad','Gap':'v-warn'}
def verdict(lst): return notes([(f'<span class="verdict {V[k]}">{k}</span> {h}',b) for k,h,b in lst])
def steal(lst): return '<ol class="steal">'+''.join(f'<li><p><b>{a}</b> {b}</p></li>' for a,b in lst)+'</ol>'
def timeline(lst): return '<ol class="timeline">'+''.join(f'<li><b>{d}</b> <span class="mono">{c}</span><p>{t}</p></li>' for d,c,t in lst)+'</ol>'
def srcs(lst): return '<ol class="srcs">'+''.join(f'<li>{x}</li>' for x in lst)+'</ol>'
def table(hd,rows,cls='dense'):
    return '<div class="tablewrap"><table class="'+cls+'"><thead><tr>'+''.join(f'<th>{h}</th>' for h in hd)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def gal(gid,items,cls=''):
    """items: dict(id, n, il (data uri), d, k, dark)"""
    out=''
    for o in items:
        c='gimg one'+(' dark' if o.get('dark') else '')
        out+=f'<article class="gcard" data-k="{esc(o.get("k",""))}"><button type="button" class="{c}" data-cap="{esc(o["n"])}" aria-label="Enlarge {esc(o["n"])}"><img class="gi-l" id="{o["id"]}" src="{o["il"]}" alt="{esc(o["n"])}" loading="lazy"></button><div class="gbody"><h3>{esc(o["n"])}</h3>{"<p>"+o["d"]+"</p>" if o.get("d") else ""}</div></article>'
    return f'<div class="gal {cls}" id="{gid}">{out}</div>'
def gchips(gid,keys):
    return f'<div class="chips" style="margin:6px 0 12px" data-gfilter="{gid}"><button type="button" class="chip" data-k="all" aria-pressed="true">All</button>'+''.join(f'<button type="button" class="chip" data-k="{k}" aria-pressed="false">{esc(l)}</button>' for k,l in keys)+'</div>'
XCSS='''<style>.d-img{background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px;cursor:zoom-in}.d-img.dk{background:#1e1e1e}.d-img img{display:block;width:100%;max-height:300px;object-fit:contain}
.qsrc{display:block;font-style:normal;font-family:var(--f-display);font-size:.72rem;color:var(--ink-3);margin-top:3px}.hero h1 .p{color:var(--skin)}
.thesis mark{background:linear-gradient(transparent 55%,var(--gold-soft) 55%);color:inherit;padding:0 .1em}
.pill.sky{background:var(--sky);color:var(--sky-ink)}.pill.gold{background:var(--gold-soft);color:#7a5208}:root[data-theme="dark"] .pill.gold{color:var(--gold)}</style>'''
def explorer_js(prefix,key,items,groups,blobnote='Read the source on GitHub'):
    """items: list of dicts with id,name,group,pills,tag,invoke,how,quotes[[html,path]],files,lesson,src,img,dark,extra"""
    return data_js('IT_'+prefix,items)+data_js('GR_'+prefix,groups)+r'''
(()=>{const I=IT_P,by=Object.fromEntries(I.map((x)=>[x.id,x]));
makeExplorer({prefix:"P",key:"K",groups:GR_P.map((g)=>[g,I.filter((x)=>x.group===g)]),
 getText:(s)=>[s.name,s.tag,...(s.how||[]),...(s.quotes||[]).map((q)=>q[0])].join(" ").replace(/<[^>]+>/g,""),
 renderItem:(s,on)=>`<button class="item" type="button" role="option" data-id="${xesc(s.id)}" aria-selected="${on}"><span>${xesc(s.name)}</span><small>${xesc(s.small||"")}</small></button>`,
 renderDetail:(id)=>{const s=by[id];let h=`<div class="d-top"><div class="d-name">${xesc(s.name)}</div><div class="d-meta">${(s.pills||[]).map((p,i)=>`<span class="pill${i==1?" skin":i==2?" sky":""}">${p}</span>`).join("")}</div><p class="d-tag">${s.tag}</p></div>`;
  if(s.img){const el=document.getElementById(s.img);if(el)h+=`<div class="d-sec"><button type="button" class="d-img${s.dark?" dk":""}" data-g="${s.img}" aria-label="Enlarge"><img src="${el.src}" alt="${xesc(s.name)} render"></button></div>`}
  if(s.invoke)h+=`<div class="d-sec"><h4>Try it</h4><div class="invoke">${xesc(s.invoke)}</div></div>`;
  if(s.how&&s.how.length)h+=`<div class="d-sec"><h4>How it works</h4><ol>${s.how.map((x)=>`<li>${x}</li>`).join("")}</ol></div>`;
  if(s.quotes&&s.quotes.length)h+=`<div class="d-sec"><h4>In its own words</h4>${s.quotes.map((q)=>`<p class="quote">“${q[0]}”<span class="qsrc">${xesc(q[1])}</span></p>`).join("")}</div>`;
  if(s.extra)h+=s.extra;
  if(s.files&&s.files.length)h+=`<div class="d-sec"><h4>Files</h4><div class="files">${s.files.map((f)=>`<code>${xesc(f)}</code>`).join("")}</div></div>`;
  if(s.lesson)h+=`<div class="d-sec"><h4>Design lesson</h4><p class="lesson">${s.lesson}</p></div>`;
  return h+(s.src?`<div class="d-sec"><p style="font-size:.85rem"><a href="${s.src}">BLOBNOTE</a></p></div>`:"")}});
document.getElementById("PPane").addEventListener("click",(e)=>{const b=e.target.closest(".d-img");if(!b)return;const g=document.getElementById(b.dataset.g);if(g)g.closest(".gimg").click()});})();
'''.replace('IT_P','IT_'+prefix).replace('GR_P','GR_'+prefix).replace('"P"','"'+prefix+'"').replace('"K"','"'+key+'"').replace('PPane',prefix+'Pane').replace('BLOBNOTE',blobnote)
def build(slug,title,nav,body,footer,js):
    html=page(title,slug,nav,GCSS+XCSS+body+LB,footer=footer,extra_js=js+GJS)
    from config import out as _o; out=_o(slug)
    open(out,'w').write(html); return len(html)
