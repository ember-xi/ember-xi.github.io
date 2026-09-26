'use strict';
const articles=window.ZENITH_ARTICLES||[];
const search=document.querySelector('#wiki-search');
const results=document.querySelector('#search-results');
const normalize=s=>s.normalize('NFKC').toLocaleLowerCase().replace(/[’‘]/g,"'");
const searchable=articles.map(a=>({...a,n:normalize(a.name),haystack:normalize(a.name+' '+a.category+' '+a.keys)}));
function searchNow(){
 const q=normalize(search.value.trim());results.replaceChildren();
 if(!q){results.hidden=true;return;}
 const tokens=q.split(/\s+/);
 const found=searchable.filter(a=>tokens.every(t=>a.haystack.includes(t))).sort((a,b)=>{
  const score=x=>(x.n===q?100:x.n.startsWith(q)?50:x.n.includes(q)?25:0)+(x.category==='Quests'?1:0);
  return score(b)-score(a)||a.name.localeCompare(b.name);
 }).slice(0,12);
 results.hidden=false;
 if(!found.length){const p=document.createElement('p');p.textContent='No matching articles. Try a shorter item, quest or NPC name.';results.append(p);return;}
 for(const a of found){const link=document.createElement('a');link.href=a.url;link.textContent=a.name;const note=document.createElement('small');note.textContent=a.category+' · '+a.note.slice(0,95);link.append(note);results.append(link);}
}
search.addEventListener('input',searchNow);
search.addEventListener('keydown',e=>{if(e.key==='Escape')results.hidden=true;if(e.key==='ArrowDown'){e.preventDefault();results.querySelector('a')?.focus();}if(e.key==='Enter'){const a=results.querySelector('a');if(a){e.preventDefault();location.href=a.href;}}});
results.addEventListener('keydown',e=>{const rows=[...results.querySelectorAll('a')];const i=rows.indexOf(document.activeElement);if(e.key==='Escape'){results.hidden=true;search.focus();}if(e.key==='ArrowDown'){e.preventDefault();rows[(i+1)%rows.length]?.focus();}if(e.key==='ArrowUp'){e.preventDefault();if(i<=0)search.focus();else rows[i-1]?.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.search'))results.hidden=true;});
const navButton=document.querySelector('.mobile-nav');navButton.addEventListener('click',()=>{const open=document.querySelector('.sidebar').classList.toggle('open');navButton.setAttribute('aria-expanded',String(open));});
for(const input of document.querySelectorAll('[data-step]')){
 const key='zenith-wiki-healers-promise-step-'+input.dataset.step;
 try{input.checked=localStorage.getItem(key)==='true';}catch{}
 input.closest('li').classList.toggle('done',input.checked);
 input.addEventListener('change',()=>{try{localStorage.setItem(key,String(input.checked));}catch{}input.closest('li').classList.toggle('done',input.checked);});
}
document.querySelector('#reset-steps')?.addEventListener('click',()=>{for(const i of document.querySelectorAll('[data-step]')){i.checked=false;i.dispatchEvent(new Event('change'));}});
const mapDialog=document.querySelector('#map-dialog');document.querySelector('#open-map')?.addEventListener('click',()=>mapDialog.showModal());document.querySelector('#close-map')?.addEventListener('click',()=>mapDialog.close());mapDialog?.addEventListener('click',e=>{if(e.target===mapDialog)mapDialog.close();});
const level=document.querySelector('#camp-level');
function filterCamps(){const raw=level.value.trim();const n=Number(raw);let count=0;for(const row of document.querySelectorAll('#camp-table tbody tr')){const show=!raw||(n>=Number(row.dataset.low)&&n<=Number(row.dataset.high));row.hidden=!show;if(show)count++;}document.querySelector('#camp-count').textContent=count+' camps';document.querySelector('#camp-empty').hidden=count!==0;}
level?.addEventListener('input',filterCamps);document.querySelector('#camp-reset')?.addEventListener('click',()=>{level.value='';filterCamps();});
const market=document.querySelector('#market-search');
function filterMarket(){const tokens=normalize(market.value.trim()).split(/\s+/).filter(Boolean);let count=0;for(const row of document.querySelectorAll('#market-table tbody tr')){row.hidden=!tokens.every(t=>normalize(row.dataset.search).includes(t));if(!row.hidden)count++;}document.querySelector('#market-count').textContent=count+' items';document.querySelector('#market-empty').hidden=count!==0;}
market?.addEventListener('input',filterMarket);document.querySelector('#market-reset')?.addEventListener('click',()=>{market.value='';filterMarket();market.focus();});
function oldBookmark(){if(document.body.dataset.page!=='index'||!location.hash)return;const key=decodeURIComponent(location.hash.slice(1));const target=window.ZENITH_LEGACY?.[key];if(target&&target!=='index.html')location.replace(target);}
oldBookmark();window.addEventListener('hashchange',oldBookmark);

for(const input of document.querySelectorAll('[data-list-filter]')){
 const list=document.getElementById(input.dataset.listFilter);
 const count=document.querySelector('[data-list-count="'+input.dataset.listFilter+'"]');
 const filter=()=>{const tokens=normalize(input.value.trim()).split(/\s+/).filter(Boolean);let n=0;for(const row of list.children){row.hidden=!tokens.every(t=>normalize(row.dataset.filter).includes(t));if(!row.hidden)n++;}count.textContent=n+' pages';};
 input.addEventListener('input',filter);filter();
}
document.querySelector('[data-print]')?.addEventListener('click',e=>{e.preventDefault();window.print();});

const enlargeButtons=document.querySelectorAll('[data-enlarge-map]');
if(enlargeButtons.length){
 const dialog=document.createElement('dialog');dialog.className='scout-map-dialog';dialog.setAttribute('aria-labelledby','scout-map-title');
 const header=document.createElement('header');const title=document.createElement('strong');title.id='scout-map-title';title.textContent='Scout location map';
 const close=document.createElement('button');close.type='button';close.textContent='Close';header.append(title,close);
 const content=document.createElement('div');dialog.append(header,content);document.body.append(dialog);let opener;
 close.addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
 dialog.addEventListener('close',()=>opener?.focus());
 for(const button of enlargeButtons)button.addEventListener('click',()=>{opener=button;title.textContent=button.dataset.mapTitle||'Location map';const figure=button.closest('figure');content.replaceChildren(figure.querySelector('.map-marked').cloneNode(true),figure.querySelector('figcaption').cloneNode(true));dialog.showModal();});
}
