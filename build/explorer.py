# Shared explorer template ported from the "Inside pstack" reference: CSS, JS and markup helpers.
import json
CSS = r"""
.rail{top:calc(env(safe-area-inset-top,0px) + 24px)}
.toc{display:none}
@media (max-width:980px){.toc{display:block;position:sticky;top:0;z-index:30;margin:0 -4px;padding:calc(env(safe-area-inset-top,0px) + 8px) 4px 8px;background:var(--paper);border-bottom:1px solid var(--line);font-family:var(--f-display)}
.toc summary{cursor:pointer;font-size:.9rem;font-weight:600;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:10px}.toc summary::-webkit-details-marker{display:none}
.toc summary::after{content:"Jump to ▾";font-weight:400;color:var(--ink-3);font-size:.82rem}.toc[open] summary::after{content:"Close ▴"}
.toc ol{list-style:none;margin:8px 0 2px;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:2px 10px}.toc a{display:block;padding:5px 6px;font-size:.88rem;color:var(--ink-2);text-decoration:none;border-radius:6px}.toc a:hover{background:var(--panel)}
.toc .theme-btn{margin-top:6px}}
section[id],header[id]{scroll-margin-top:calc(env(safe-area-inset-top,0px) + 64px)}
.explorer{display:grid;grid-template-columns:minmax(250px,320px) minmax(0,1fr);gap:18px;height:min(80vh,780px);min-height:520px}
.ex-list{display:grid;grid-template-rows:auto auto minmax(0,1fr);gap:10px;min-width:0;min-height:0}
.search{width:100%;font:inherit;font-family:var(--f-display);font-size:.92rem;padding:9px 12px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-family:var(--f-display);font-size:.78rem;border:1px solid var(--line);background:var(--panel);color:var(--ink-2);padding:4px 10px;border-radius:999px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--skin);border-color:var(--skin);color:#fff}
.items{overflow-y:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel);min-height:0;overscroll-behavior:contain}
.grp{font-family:var(--f-display);font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);padding:12px 14px 4px;font-weight:600}
.item{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:baseline;width:100%;text-align:left;background:none;border:0;border-left:3px solid transparent;padding:8px 14px 8px 11px;cursor:pointer;color:var(--ink);font-family:var(--f-mono);font-size:.82rem;transition:background .35s var(--ease),border-color .35s var(--ease)}
.item span{overflow-wrap:anywhere}.item:hover{background:var(--code-bg)}
.item[aria-selected="true"]{background:var(--gold-soft);border-left-color:var(--gold)}
.item small{font-family:var(--f-display);color:var(--ink-3);font-size:.72rem;font-variant-numeric:tabular-nums}
.empty{padding:16px;color:var(--ink-3);font-family:var(--f-display);font-size:.88rem}
.ex-detail{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);min-width:0;min-height:0;overflow:hidden}
.ex-pane{position:absolute;inset:0;overflow-y:auto;padding:26px 30px 34px;transition:opacity .22s var(--ease);overscroll-behavior:contain}
.ex-pane.fading{opacity:0}
.d-top{display:grid;gap:8px;margin-bottom:18px}
.d-name{font-family:var(--f-mono);font-size:1.35rem;font-weight:600;color:var(--ink);overflow-wrap:anywhere}
.d-tag{font-size:1.04rem;color:var(--ink-2);max-width:62ch}
.d-meta{display:flex;flex-wrap:wrap;gap:6px}
.pill.skin{background:var(--skin-soft);color:var(--skin)}
.d-sec{margin-top:20px;display:grid;gap:8px}
.d-sec h4{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.d-sec ol,.d-sec ul{margin:0;padding-left:1.25em;display:grid;gap:7px;max-width:70ch}
.d-sec li{font-size:.97rem}
.invoke{font-family:var(--f-mono);font-size:.82rem;background:var(--code-bg);border-radius:8px;padding:10px 12px;white-space:pre-wrap;overflow-wrap:anywhere}
.quote{border-left:3px solid var(--skin);padding:2px 0 2px 14px;font-style:italic;font-size:.97rem;max-width:68ch;color:var(--ink)}
.files{display:flex;flex-wrap:wrap;gap:6px}.files code{font-size:.76rem}
.lesson{background:var(--gold-soft);border-radius:10px;padding:12px 14px;font-size:.96rem;max-width:70ch}
.lesson b{font-family:var(--f-display)}
.sheet-close,.backdrop{display:none}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:10px}
.pcard{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:6px;align-content:start;min-width:0;overflow-wrap:anywhere}
.pcard h4{font-size:.98rem}.pcard p{font-size:.92rem;color:var(--ink-2)}
.pcard .when{font-size:.84rem;color:var(--ink-3)}
.pcard .test{font-size:.88rem;color:var(--ink);font-style:italic;border-top:1px dashed var(--line);padding-top:6px}
.gname{display:flex;align-items:baseline;gap:10px;margin-top:22px}.gname span{font-family:var(--f-display);font-size:.8rem;color:var(--ink-3)}
.stub{font-family:var(--f-display);font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;background:var(--gold-soft);color:#7a5208;padding:1px 7px;border-radius:999px;margin-left:6px;vertical-align:middle}
dialog.ex-sheet{display:none}
@media (max-width:860px){
.explorer{grid-template-columns:minmax(0,1fr);height:62vh;min-height:420px}
.explorer>.ex-detail{display:none}
dialog.ex-sheet[open]{display:block;position:fixed;inset:auto 0 0 0;margin:0;width:100%;max-width:none;height:86vh;max-height:none;padding:0;border:0;background:transparent;color:inherit;overflow:visible;animation:ex-sheet-in .6s var(--ease)}
dialog.ex-sheet::backdrop{background:rgba(20,18,28,.45)}
dialog.ex-sheet .ex-detail{height:100%;border-radius:16px 16px 0 0;padding-bottom:env(safe-area-inset-bottom,0px)}
.ex-pane{padding:52px 20px 34px}
.sheet-close{display:block;position:absolute;top:10px;right:12px;z-index:2;font-family:var(--f-display);font-size:.85rem;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:5px 14px;cursor:pointer}}
@keyframes ex-sheet-in{from{transform:translateY(105%)}to{transform:translateY(0)}}
"""
JS = r"""
const xesc=(s)=>String(s).replace(/[&<>"]/g,(c)=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const xstore={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const xmobile=()=>window.matchMedia("(max-width: 860px)").matches;
document.querySelectorAll("[data-close]").forEach((b)=>b.addEventListener("click",()=>{const d=b.closest("dialog");if(d)d.close()}));
document.querySelectorAll(".toc a").forEach((a)=>a.addEventListener("click",()=>a.closest("details").open=false));
function makeExplorer({prefix,groups,getText,renderItem,renderDetail,key}){
  const $=(s)=>document.getElementById(prefix+s);
  const itemsEl=$("Items"),chipsEl=$("Chips"),searchEl=$("Search"),detailEl=$("Detail"),paneEl=$("Pane"),sheetEl=$("Sheet"),homeEl=$("Explorer");
  // Mobile: the detail pane moves into a modal <dialog> (focus moves in, Esc and backdrop close it) and back on close.
  let opener=null;const sheetLabel=sheetEl?sheetEl.getAttribute("aria-label"):"";
  function openSheet(btn){if(!sheetEl)return;opener=btn;const nm=btn&&btn.querySelector("span");sheetEl.setAttribute("aria-label",nm?nm.textContent.trim():sheetLabel);sheetEl.appendChild(detailEl);sheetEl.showModal();const c=detailEl.querySelector(".sheet-close");if(c)c.focus()}
  if(sheetEl){sheetEl.addEventListener("close",()=>{homeEl.appendChild(detailEl);const back=(opener&&opener.isConnected)?opener:itemsEl.querySelector(`.item[data-id="${CSS.escape(selected)}"]`);if(back)back.focus();opener=null});
    sheetEl.addEventListener("click",(e)=>{if(e.target===sheetEl)sheetEl.close()});
    window.matchMedia("(max-width: 860px)").addEventListener("change",(e)=>{if(!e.matches&&sheetEl.open)sheetEl.close()})}
  let filter="all",query="";const all=groups.flatMap(([,l])=>l);
  let selected=xstore.get(key);if(!all.some((x)=>x.id===selected))selected=all[0].id;
  chipsEl.innerHTML=[["all","All"],...groups.map(([g])=>[g,g])].map(([v,l])=>`<button class="chip" type="button" data-v="${xesc(v)}" aria-pressed="${v===filter}">${xesc(l)}</button>`).join("");
  chipsEl.addEventListener("click",(e)=>{const b=e.target.closest(".chip");if(!b)return;filter=b.dataset.v;chipsEl.querySelectorAll(".chip").forEach((c)=>c.setAttribute("aria-pressed",c.dataset.v===filter));drawList()});
  searchEl.addEventListener("input",()=>{query=searchEl.value.trim().toLowerCase();drawList()});
  function drawList(){let h="",n=0;for(const [g,l] of groups){if(filter!=="all"&&filter!==g)continue;const rows=l.filter((x)=>!query||getText(x).toLowerCase().includes(query));if(!rows.length)continue;h+=`<div class="grp">${xesc(g)}</div>`;h+=rows.map((x)=>{n++;return renderItem(x,x.id===selected)}).join("")}
    itemsEl.innerHTML=n?h:`<div class="empty">Nothing matches "${xesc(query)}".</div>`;itemsEl.dataset.count=n}
  itemsEl.addEventListener("click",(e)=>{const b=e.target.closest(".item");if(b)select(b.dataset.id,true,b)});
  itemsEl.addEventListener("keydown",(e)=>{if(e.key!=="ArrowDown"&&e.key!=="ArrowUp")return;const its=[...itemsEl.querySelectorAll(".item")];const i=its.findIndex((x)=>x.dataset.id===selected);const nx=its[Math.max(0,Math.min(its.length-1,i+(e.key==="ArrowDown"?1:-1)))];if(nx){e.preventDefault();select(nx.dataset.id,false);nx.focus()}});
  function select(id,fromClick,btn){const changed=id!==selected;selected=id;xstore.set(key,id);
    itemsEl.querySelectorAll(".item").forEach((b)=>b.setAttribute("aria-selected",b.dataset.id===id));
    if(changed){paneEl.classList.add("fading");setTimeout(()=>{paneEl.innerHTML=renderDetail(id);paneEl.scrollTop=0;paneEl.classList.remove("fading")},220)}
    if(fromClick&&xmobile())openSheet(btn)}
  drawList();paneEl.innerHTML=renderDetail(selected);
}
"""
def explorer(prefix, label):
    """Markup for one master-detail explorer; data and renderers are supplied in JS."""
    return f'''<div class="explorer" id="{prefix}Explorer">
<div class="ex-list"><input class="search" id="{prefix}Search" type="search" placeholder="Filter {label}…" aria-label="Filter {label}">
<div class="chips" id="{prefix}Chips"></div>
<div class="items" id="{prefix}Items" role="listbox" aria-label="{label.title()}"></div></div>
<div class="ex-detail" id="{prefix}Detail" aria-live="polite"><button class="sheet-close" type="button" data-close>Close</button><div class="ex-pane" id="{prefix}Pane"></div></div></div>
<dialog class="ex-sheet" id="{prefix}Sheet" aria-label="{label.title()} details"></dialog>'''
def data_js(name, obj):
    return f'const {name}={json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")};\n'
