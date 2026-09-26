"""Package a reproducible article snapshot, excluding source administration."""
from pathlib import Path
import argparse,gzip,json,shutil

R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--audit',required=True);p.add_argument('--images',required=True);p.add_argument('--supplements');p.add_argument('--allow-partial',action='store_true');args=p.parse_args()
source=Path(args.source);audit=Path(args.audit);out=R/'content/era-reference';out.mkdir(exist_ok=True)
metadata=json.loads((audit/'eden-namespace-0-info.json').read_text())+json.loads((audit/'eden-namespace-14.json').read_text())
filters=json.loads((audit/'eden-filter-audit.json').read_text());excluded={r['title'] for r in filters['excluded_titles']}|set(filters['excluded_categories'])
extra={'Known Relic Holders':'Personal source-server player roster','Eden\'s Warehouse':'Source-server storage service','New player guide to Eden':'Source-server installation and onboarding','New player guide to Eden by Falzum':'Source-server installation and onboarding','Eden Harvest Festival Guide':'Source-server seasonal event','Eden Starlight Celebration Guide':'Source-server seasonal event'}
excluded.update(extra)
extra['Zipacna/Video']='Duplicate optional encounter video; main Zipacna guide is retained'
excluded.update(extra)
supplement_files={}
supplement_titles={}
if args.supplements:
    for f in Path(args.supplements).glob('*.json'):
        data=json.loads(f.read_text())
        if not isinstance(data.get('articles'),list) or not data['articles']:continue
        supplement_files[f.name]=f
        for article in data['articles']:supplement_titles[article['title']]=article
existing={'Zeruhn Mines':'zone-zeruhn-mines','Zhayolm Remnants':'zone-zhayolm-remnants','Zulkheim':'region-zulkheim'}
records=[];missing=[];scope=[];replacements=[]
for r in metadata:
    if 'redirect' in r or r['title'] in excluded:continue
    f=source/(str(r['pageid'])+'.json.gz')
    if not f.exists():
        title=r['title']
        if title in supplement_titles:
            replacements.append({'title':title,'pageid':r['pageid'],'kind':'original concise guide','sources':supplement_titles[title].get('source_urls',[])})
        elif title in existing:
            replacements.append({'title':title,'pageid':r['pageid'],'kind':'existing Zenith guide','route':existing[title]})
        else:missing.append(title)
        continue
    d=json.loads(gzip.decompress(f.read_bytes()));records.append(d)
    scope.append({k:d.get(k) for k in ('title','pageid','namespace','revision','source','retrieved','categories','source_sha256')})
if missing and not args.allow_partial:raise SystemExit('Incomplete snapshot: '+str(len(missing))+' articles missing; first '+repr(missing[:5]))
for f in out.glob('articles-*.jsonl.gz'):f.unlink()
records.sort(key=lambda d:d['title'])
for offset in range(0,len(records),500):
    body='\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in records[offset:offset+500])+'\n'
    (out/('articles-'+str(offset//500).zfill(3)+'.jsonl.gz')).write_bytes(gzip.compress(body.encode(),mtime=0))
(out/'inventory.json').write_text(json.dumps({'snapshot':'2026-09-26','license':'https://creativecommons.org/licenses/by-sa/4.0/','articles':scope,'replacements':replacements,'missing':missing,'excluded':filters['excluded_titles']+[{'title':t,'reason':reason} for t,reason in extra.items()]},ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(audit/'eden-redirects.json',out/'redirects.json')
if (audit/'horizon-source-broken-file-map.json').exists():shutil.copyfile(audit/'horizon-source-broken-file-map.json',out/'broken-image-matches.json')
images=Path(args.images);manifest=json.loads((images/'images.json').read_text()) if (images/'images.json').exists() else {}
(out/'images.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
target=R/'dist/assets/era';target.mkdir(exist_ok=True)
for r in manifest.values():
    if r.get('path'):shutil.copyfile(images/Path(r['path']).name,R/'dist'/r['path'])
if args.supplements:
    (out/'supplements').mkdir(exist_ok=True)
    for f in (out/'supplements').glob('*.json'):f.unlink()
    for name,f in supplement_files.items():shutil.copyfile(f,out/'supplements'/name)
print(json.dumps({'packaged':len(records),'authored_or_existing_replacements':len(replacements),'missing':len(missing),'excluded':len(excluded),'images':sum('path'in r for r in manifest.values())}))
