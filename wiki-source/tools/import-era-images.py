"""Download images referenced by the licensed article snapshot, with provenance."""
import argparse, asyncio, gzip, hashlib, json
from pathlib import Path
from urllib.parse import urlsplit
import aiohttp

async def main(args):
    source=Path(args.articles);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    manifest=out/'images.json';known=json.loads(manifest.read_text()) if manifest.exists() else {}
    urls={}
    for p in source.glob('*.json.gz'):
        d=json.loads(gzip.decompress(p.read_bytes()))
        for u in d['images']:urls.setdefault(u,[]).append(d['source'])
    extras={r['url']:r for r in json.loads(Path(args.extra).read_text())} if args.extra else {}
    for u,r in extras.items():urls.setdefault(u,[]).append(r['descriptionurl'])
    # Public CDN images only; no arbitrary origins from source HTML.
    hosts={'static.wikitide.net','static.miraheze.org','static.wikia.nocookie.net','vignette.wikia.nocookie.net','images.wikia.com','images1.wikia.nocookie.net','images2.wikia.nocookie.net','images3.wikia.nocookie.net','images4.wikia.nocookie.net','horizonffxi.wiki'}
    pending=[u for u in urls if (u not in known or 'error' in known[u] or not (out/Path(known[u].get('path','missing')).name).is_file()) and urlsplit(u).hostname in hosts]
    queue=asyncio.Queue()
    for u in pending:queue.put_nowait(u)
    async with aiohttp.ClientSession(trust_env=True,headers={'User-Agent':'Mozilla/5.0 (compatible; ZenithWiki reference importer)'},timeout=aiohttp.ClientTimeout(total=40),connector=aiohttp.TCPConnector(limit=6)) as s:
        async def worker():
            while not queue.empty():
                try:u=queue.get_nowait()
                except asyncio.QueueEmpty:return
                result={'url':u,'articles':urls[u],'copyright':'FINAL FANTASY XI game images and artwork © SQUARE ENIX; original file attribution retained.'}
                if u in extras:result.update(filePage=extras[u]['descriptionurl'],width=extras[u]['width'],height=extras[u]['height'],sourceTitle=extras[u]['name'])
                try:
                    async with s.get(u) as r:
                        if r.status!=200:raise ValueError('HTTP '+str(r.status))
                        mime=r.headers.get('Content-Type','').split(';')[0];b=await r.read()
                    ext={'image/jpeg':'.jpg','image/png':'.png','image/gif':'.gif','image/webp':'.webp'}.get(mime)
                    if not ext:raise ValueError('Unsupported image type '+mime)
                    if len(b)>8*1024*1024:raise ValueError('Image exceeds 8 MiB')
                    if ext=='.svg' and any(x in b.lower() for x in (b'<script',b'javascript:',b'<foreignobject')):raise ValueError('Active SVG rejected')
                    name=hashlib.sha256(u.encode()).hexdigest()[:24]+ext;(out/name).write_bytes(b)
                    result.update(path='assets/era/'+name,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
                except Exception as e:result['error']=str(e)
                known[u]=result
                if len(known)%100==0:manifest.write_text(json.dumps(known,ensure_ascii=False,indent=2));print('Images processed',len(known),flush=True)
                queue.task_done()
        await asyncio.gather(*(worker() for _ in range(6)))
    manifest.write_text(json.dumps(known,ensure_ascii=False,indent=2))
    print(json.dumps({'referenced':len(urls),'saved':sum('path'in r for r in known.values()),'failed':sum('error'in r for r in known.values()),'outside_cdn':len([u for u in urls if urlsplit(u).hostname not in hosts])}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--articles',required=True);p.add_argument('--output',required=True);p.add_argument('--extra');asyncio.run(main(p.parse_args()))
