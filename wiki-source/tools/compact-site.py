"""Compact static output without removing articles, images, or image dimensions."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
from html import unescape
from urllib.parse import unquote
import hashlib,json,re
R=Path(__file__).resolve().parents[1];D=R/'dist'
report_path=R/'docs/era-import/compact-assets.json'
prior=json.loads(report_path.read_text()) if report_path.exists() else {}
def convert(p):
 if p.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}:return
 original=p.read_bytes();digest=hashlib.sha256(original).hexdigest();rel=p.relative_to(D).as_posix()
 if prior.get('hashes',{}).get(rel)==digest:return
 with Image.open(p) as image:
  if getattr(image,'n_frames',1)>1:return
  im=image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
  b=BytesIO();im.save(b,'WEBP',quality=90,method=4);data=b.getvalue()
  if len(data)>=len(original)*.88:return
  target=p if p.suffix.lower()=='.webp' else p.with_name(p.stem+'-web.webp')
  target.write_bytes(data)
  with Image.open(target) as test:assert test.size==image.size;test.verify()
 return rel,target.relative_to(D).as_posix(),len(original),len(data),hashlib.sha256(data).hexdigest()
with ThreadPoolExecutor(max_workers=6) as pool:changes=[c for c in pool.map(convert,list((D/'assets').rglob('*'))) if c]
mapping=dict(prior.get('mapping',{}))
mapping.update({a:b for a,b,*_ in changes if a!=b})
# Update source metadata as well as the rendered pages for reproducible builds.
if mapping:
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
 files=list(D.rglob('*.html'))+list(D.rglob('*.css'))+list(D.rglob('*.js'))
 files+=list((R/'content').rglob('*.json'))+list((R/'content').rglob('*.py'))+list((R/'content').rglob('*.html'))
 files+=[R/'tools/build-wiki.py']
 for p in files:
  source=p.read_text();updated=pattern.sub(lambda m:mapping[m.group()],source)
  if updated!=source:p.write_text(updated)
# The sidebar markup is identical on every article; serve one shared copy.
sidebar_file=D/'assets/sidebar.js';sample=(D/'index.html').read_text()
side=re.search(r'<aside class="sidebar"[^>]*>.*?</aside>',sample,re.S)
if side and 'shared-sidebar' not in side.group():
 markup=re.sub(r' aria-current="page"','',side.group())
 inner=markup[markup.index('>')+1:markup.rfind('</aside>')]
 code='(()=>{const e=document.getElementById("shared-sidebar");if(!e)return;let s='+json.dumps(inner)+';const k=document.body.dataset.page;s=s.replace(`href="${k}.html"`,`href="${k}.html" aria-current="page"`);e.innerHTML=s;})();\n'
 sidebar_file.write_text(code)
 fallback='<aside class="sidebar" id="shared-sidebar"><nav aria-label="Wiki navigation"><a href="index.html">Main Page</a><a href="jobs.html">Jobs</a><a href="all-pages.html">All Pages</a></nav></aside>'
 for p in D.rglob('*.html'):
  text=p.read_text();updated=re.sub(r'<aside class="sidebar"[^>]*>.*?</aside>',lambda m:fallback,text,flags=re.S)
  if updated!=text:
   updated=updated.replace('<script defer src="assets/search-index.js','<script defer src="assets/sidebar.js?v=42"></script><script defer src="assets/search-index.js')
   p.write_text(updated)
# Share the identical header and footer with the same progressively enhanced shell.
for tag,cls,ident in [('header','topbar','shared-topbar'),('footer','footer','shared-footer')]:
 found=re.search(r'<'+tag+r' class="'+cls+r'"[^>]*>.*?</'+tag+'>',sample,re.S)
 if found and ident not in found.group():
  markup=found.group();inner=markup[markup.index('>')+1:markup.rfind('</'+tag+'>')]
  with sidebar_file.open('a') as stream:stream.write('(()=>{const e=document.getElementById('+json.dumps(ident)+');if(e)e.innerHTML='+json.dumps(inner)+';})();\n')
  replacement='<'+tag+' class="'+cls+'" id="'+ident+'"></'+tag+'>'
  for p in D.rglob('*.html'):
   text=p.read_text();updated=re.sub(r'<'+tag+r' class="'+cls+r'"[^>]*>.*?</'+tag+'>',lambda m:replacement,text,flags=re.S)
   if updated!=text:p.write_text(updated)
# Replace the repeated inline favicon with the exact same SVG as one asset.
icon=re.search(r'<link rel="icon" href="(data:image/svg\+xml,[^"]+)"',sample)
if icon:
 (D/'assets/favicon.svg').write_text(unquote(unescape(icon.group(1)).split(',',1)[1]))
 for p in D.rglob('*.html'):
  text=p.read_text();updated=re.sub(r'(<link rel="icon" href=")data:image/svg\+xml,[^"]+',r'\1assets/favicon.svg',text)
  if updated!=text:p.write_text(updated)
for old,new in mapping.items():
 p=D/old
 if p.exists():p.unlink()
# Remove original encodings only after every rendered reference was rewritten.
used=set()
for p in D.rglob('*.html'):used.update(re.findall(r'assets/[^"<>\s?#]+',p.read_text()))
for old in mapping:assert old not in used,old
hashes=dict(prior.get('hashes',{}));hashes.update({new:digest for old,new,before,after,digest in changes})
report={'hashes':hashes,'mapping':mapping,'converted':len(changes),'before_bytes':sum(c[2] for c in changes),'after_bytes':sum(c[3] for c in changes)}
report_path.write_text(json.dumps(report,indent=2)+'\n')
total=sum(p.stat().st_size for p in D.rglob('*') if p.is_file())
print(json.dumps({'images_reencoded':len(changes),'image_bytes_saved':report['before_bytes']-report['after_bytes'],'expanded_bytes':total,'limit_bytes':256*1024*1024}))
# finalize-site.py applies the final pruning and expanded-size gate.
