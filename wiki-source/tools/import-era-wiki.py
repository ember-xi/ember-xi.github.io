"""Download attributed Eden reference articles; resumable, bounded public GETs.

Only public article URLs are fetched. No accounts, edits or protected dumps.
The original revision, article URL and contributor-history URL are retained.
"""
import argparse, asyncio, gzip, hashlib, json, re, time
from pathlib import Path
from urllib.parse import quote, urljoin
import aiohttp
from lxml import html

BASE = 'https://edenxi.miraheze.org'

def extract(data, record):
    tree = html.fromstring(data)
    nodes = tree.xpath('//*[@id="mw-content-text"]/*[contains(concat(" ",normalize-space(@class)," ")," mw-parser-output ")]')
    if not nodes:
        nodes = tree.xpath('//*[@id="mw-content-text"]')
    if not nodes:
        raise ValueError('No article content in response')
    node = nodes[0]
    revision = re.search(r'"wgRevisionId"\s*:\s*(\d+)', data)
    categories = tree.xpath('//*[@id="mw-normal-catlinks"]//li/a/@title')
    title = tree.xpath('string(//*[@id="firstHeading"])').strip() or record['title']
    images = sorted(set(urljoin(BASE, s) for s in node.xpath('.//img/@src') if s and not s.startswith('data:')))
    body = html.tostring(node, encoding='unicode')
    return dict(title=title, pageid=record['pageid'], namespace=record.get('ns',0),
                revision=int(revision.group(1)) if revision else record.get('lastrevid'),
                source=BASE+'/wiki/'+quote(record['title'].replace(' ','_'),safe='/:'),
                retrieved='2026-09-26', categories=categories, images=images, html=body,
                source_sha256=hashlib.sha256(data.encode()).hexdigest())

async def main(args):
    records = json.loads(Path(args.inventory).read_text())
    if args.categories:
        records += json.loads(Path(args.categories).read_text())
    records = [r for r in records if 'redirect' not in r and r.get('contentmodel','wikitext')=='wikitext']
    # Job, equipment and acquisition navigation is downloaded first.
    priorities={'Warrior','Monk','White Mage','Black Mage','Red Mage','Thief','Paladin','Dark Knight','Beastmaster','Bard','Ranger','Samurai','Ninja','Dragoon','Summoner','Blue Mage','Corsair','Puppetmaster','Dancer','Scholar','Artifact Armor','Relic Armor','Relic Weapons','Limbus','Dynamis','Category:Jobs','Category:Artifact Armor','Category:Relic Weapons'}
    records.sort(key=lambda r:(r['title'] not in priorities, r['title']))
    if args.limit: records=records[:args.limit]
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    pending=[]
    for r in records:
        p=out/(str(r['pageid'])+'.json.gz')
        if not p.exists():pending.append(r)
    queue=asyncio.Queue()
    for r in pending:queue.put_nowait(r)
    state={'total':len(records),'cached':len(records)-len(pending),'downloaded':0,'failed':[]}
    halted=asyncio.Event()
    started=time.monotonic()
    async with aiohttp.ClientSession(trust_env=True,headers={'User-Agent':'Mozilla/5.0 (compatible; ZenithWiki reference importer; attributed CC-BY-SA mirror)'},connector=aiohttp.TCPConnector(limit=args.workers),timeout=aiohttp.ClientTimeout(total=60)) as session:
        async def worker():
            while not queue.empty() and not halted.is_set():
                try:r=queue.get_nowait()
                except asyncio.QueueEmpty:return
                url=BASE+'/wiki/'+quote(r['title'].replace(' ','_'),safe='/:')
                error=None
                for attempt in range(3):
                    try:
                        async with session.get(url) as response:
                            if response.status in (429,503):
                                state['paused_reason']='Source requested a cooldown (HTTP '+str(response.status)+')'
                                state['retry_after']=response.headers.get('Retry-After')
                                halted.set();return
                            if response.status!=200:raise RuntimeError('HTTP '+str(response.status))
                            data=await response.text()
                        parsed=extract(data,r)
                        p=out/(str(r['pageid'])+'.json.gz');tmp=p.with_suffix('.tmp')
                        tmp.write_bytes(gzip.compress(json.dumps(parsed,ensure_ascii=False,separators=(',',':')).encode(),mtime=0));tmp.replace(p)
                        state['downloaded']+=1;error=None;break
                    except Exception as e:
                        error=str(e)
                        if attempt<2:await asyncio.sleep(1+attempt*2)
                if error:state['failed'].append({'title':r['title'],'pageid':r['pageid'],'error':error})
                queue.task_done()
                n=state['downloaded']+len(state['failed'])
                if n%100==0:
                    state['seconds']=round(time.monotonic()-started,1)
                    (out/'progress.json').write_text(json.dumps(state,indent=2))
                    print(json.dumps({k:v for k,v in state.items() if k!='failed'}|{'errors':len(state['failed'])}),flush=True)
                await asyncio.sleep(args.delay)
        await asyncio.gather(*(worker() for _ in range(args.workers)))
    state['seconds']=round(time.monotonic()-started,1)
    (out/'progress.json').write_text(json.dumps(state,indent=2));print(json.dumps(state),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inventory',required=True);p.add_argument('--categories');p.add_argument('--output',required=True);p.add_argument('--workers',type=int,default=4);p.add_argument('--limit',type=int);p.add_argument('--delay',type=float,default=.2)
    asyncio.run(main(p.parse_args()))
