(() => {
 'use strict';
 const own=document.currentScript.src, base=new URL('../',own);
 const page=location.pathname.split('/').pop();
 const match=page.match(/^item-(\d+)-/);
 const full=page==='auction-history.html';
 const catalog=page==='market-catalog.html';
 const ah=page==='auction-house.html';
 if(!full&&!match&&!catalog&&!ah)return;
 if(document.getElementById('zenith-ah-prices'))return;
 const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('auction-history.css?v=1',own);document.head.append(css);
 const box=document.createElement('section');box.id='zenith-ah-prices';box.className='ah-prices';
 const host=document.querySelector('.article-body')||document.querySelector('article');if(!host)return;host.prepend(box);
 function node(tag,text,cls){const x=document.createElement(tag);if(text!==undefined)x.textContent=text;if(cls)x.className=cls;return x;}
 function link(text,url){const x=node('a',text);x.href=url;return x;}
 const money=n=>Number.isSafeInteger(n)&&n>=0?n.toLocaleString('en-US')+' gil':'—';
 const date=s=>new Date(s).toLocaleString('en-GB',{timeZone:'Asia/Kuwait',dateStyle:'medium',timeStyle:'short'})+' Kuwait';
 const title=node('h2','Zenith sale history');box.append(title);
 const status=node('p','Loading completed sales…','ah-note');box.append(status);
 const toolbar=node('div',undefined,'ah-toolbar');
 toolbar.append(link('Browse all item prices',new URL('auction-history.html',base)));
 const label=node('label','Load newer export','ah-load'), input=node('input');input.type='file';input.accept='.json,application/json';input.setAttribute('aria-label','Load a newer auction-history.json export');label.append(input);toolbar.append(label);
 const reset=node('button','Use website data');reset.type='button';toolbar.append(reset);box.append(toolbar);
 const body=node('div');box.append(body);let data,local=false;
 function validate(d){
  if(d?.version!==1||!Number.isFinite(Date.parse(d.captured_at))||typeof d.items!=='object'||!d.items||Array.isArray(d.items))throw Error('Invalid export');
  if(Object.keys(d.items).length>65535)throw Error('Too many items');
  for(const [id,x] of Object.entries(d.items)){
   if(!/^\d+$/.test(id)||x.id!==Number(id)||x.id<1||x.id>65535||typeof x.name!=='string'||x.name.length>200||!Number.isInteger(x.stack_size)||x.stack_size<1||x.stack_size>99)throw Error('Invalid item');
   for(const k of ['single','stack'])if(!Array.isArray(x[k])||x[k].length>5||x[k].some(s=>!Number.isSafeInteger(s.gil)||s.gil<=0||!Number.isFinite(Date.parse(s.at))))throw Error('Invalid sale');
   if(x.reference)for(const k of ['supply_single','supply_stack','buyer_cap_single','buyer_cap_stack'])if(x.reference[k]!==null&&(!Number.isSafeInteger(x.reference[k])||x.reference[k]<0))throw Error('Invalid reference');
  }
  return d;
 }
 function median(s){const a=s.map(x=>x.gil).sort((a,b)=>a-b);return a.length?Math.round((a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2):null;}
 function detail(item){
  const pane=node('div',undefined,'ah-detail');pane.append(node('h3',item.name+' · #'+item.id));
  const grid=node('div',undefined,'ah-grid');pane.append(grid);
  for(const kind of ['single','stack']){
   const card=node('section',undefined,'ah-card');card.append(node('h4',kind==='single'?'Single item':'Full stack · '+item.stack_size+' items'));grid.append(card);
   if(kind==='stack'&&item.stack_size===1){card.append(node('p','This item does not stack.'));continue;}
   const sales=[...item[kind]].sort((a,b)=>Date.parse(b.at)-Date.parse(a.at));
   card.append(node('div',sales.length?money(sales[0].gil):'No recorded sales','ah-price'));
   card.append(node('p',sales.length?'Last completed sale · '+date(sales[0].at):'A missing history is not a zero price.','ah-note'));
   if(sales.length){
    const table=node('table');table.setAttribute('aria-label',kind+' last five completed sales');
    const head=node('tr');head.append(node('th','Paid'),node('th','Date'));const th=node('thead');th.append(head);table.append(th);
    const tb=node('tbody');for(const s of sales){const tr=node('tr');tr.append(node('td',money(s.gil)),node('td',date(s.at)));tb.append(tr);}table.append(tb);card.append(table);
    card.append(node('p','Suggested listing: '+money(median(sales))+' · median of '+sales.length+' retained sale'+(sales.length===1?'':'s')+'. A guide, not a guaranteed sale.','ah-suggestion'));
   }
   if(item.reference){
    const cap=item.reference['buyer_cap_'+kind];const supply=item.reference['supply_'+kind];
    const refs=node('div',undefined,'ah-reference');refs.append(node('strong','Fixed market reference — not sale history'));
    refs.append(node('p','Buy from market: '+money(supply)));
    refs.append(node('p','Market buyer pays up to: '+money(cap)));
    refs.append(node('small',data.market_enabled?'Buyer limits, daily budgets and availability still apply. Listings above this cap will not be bought by the market bot.':'The market was paused at export time. Reference prices do not guarantee availability.'));
    card.append(refs);
   }
  }
  pane.append(node('p','In game: Auction House → item → Single / Stack → Price History. Stack prices above are for the entire stack.','ah-note'));
  return pane;
 }
 function render(){
  body.replaceChildren();const age=Date.now()-Date.parse(data.captured_at);
  status.textContent=(local?'Your loaded export — this browser tab only. ':'Website snapshot. ')+'Updated '+date(data.captured_at)+'. '+(age>86400000?'More than 24 hours old. ':'')+'Not a live feed.';
  if(match){const x=data.items[match[1]];if(x)body.append(detail(x));else body.append(node('p','No data for this item in this export.'));return;}
  if(!full){body.append(node('p','Single and stack sales are separate. Open the price browser to see the last five sales and fixed market references.'));return;}
  const field=node('input');field.type='search';field.placeholder='Search item name or ID';field.setAttribute('aria-label','Search item name or ID');field.className='ah-search';body.append(field);
  const count=node('p',undefined,'ah-note'), list=node('div',undefined,'ah-list'),selected=node('div');body.append(count,list,selected);
  const items=Object.values(data.items).sort((a,b)=>a.name.localeCompare(b.name));
  function choose(x){selected.replaceChildren(detail(x));history.replaceState(null,'','#'+x.id);selected.scrollIntoView({behavior:'smooth',block:'start'});}
  function filter(){
   const q=field.value.toLowerCase().trim();const found=items.filter(x=>(x.name+' '+x.id).toLowerCase().includes(q));
   count.textContent=found.length+' matching items'+(found.length>60?' · showing first 60; type to narrow the list.':'.');list.replaceChildren();
   const table=node('table'),head=node('tr');for(const t of ['Item','Last single','Last full stack'])head.append(node('th',t));const th=node('thead');th.append(head);table.append(th);const tb=node('tbody');
   for(const x of found.slice(0,60)){
    const tr=node('tr'),td=node('td'),b=node('button',x.name);b.type='button';b.className='ah-item-link';b.onclick=()=>choose(x);td.append(b,node('small',' #'+x.id));
    tr.append(td,node('td',x.single.length?money(x.single[0].gil):'No sales'),node('td',x.stack_size===1?'Not stackable':x.stack.length?money(x.stack[0].gil):'No sales'));tb.append(tr);
   }table.append(tb);list.append(table);
  }
  field.addEventListener('input',filter);filter();
  const id=location.hash.slice(1);if(data.items[id])selected.append(detail(data.items[id]));
 }
 async function load(){try{const r=await fetch(new URL('auction-history.json',own),{cache:'no-store'});if(!r.ok)throw Error();data=validate(await r.json());local=false;render();}catch{status.textContent='Sale history is unavailable. Try again or load a newer export. No prices have been substituted.';}}
 input.addEventListener('change',async()=>{try{const f=input.files[0];if(!f)return;if(f.size>15000000)throw Error();const next=validate(JSON.parse(await f.text()));data=next;local=true;render();}catch{status.textContent='Could not read this export. Existing prices were retained; choose a valid auction-history.json.';}finally{input.value='';}});
 reset.onclick=load;load();
})();
