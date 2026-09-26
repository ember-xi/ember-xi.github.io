"""Keep source image dimensions and attribution while reducing publish size."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import hashlib,json,re

R=Path(__file__).resolve().parents[1];D=R/'dist';folder=D/'assets/era'
def convert(path):
    if path.suffix.lower() not in {'.png','.jpg','.jpeg'}:return None
    before=path.read_bytes()
    with Image.open(path) as image:
        if getattr(image,'n_frames',1)>1:return None
        im=image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
        buf=BytesIO();im.save(buf,'WEBP',lossless=True,method=3)
        data=buf.getvalue();mode='lossless'
        if len(data)>len(before)*0.55:
            buf=BytesIO();im.save(buf,'WEBP',quality=94,method=4)
            if len(buf.getvalue())<len(data):data=buf.getvalue();mode='quality-94'
        if len(data)>=len(before)*0.9:return None
        target=path.with_suffix('.webp');target.write_bytes(data)
        with Image.open(target) as check:assert check.size==image.size;check.verify()
    return (str(path.relative_to(D)),str(target.relative_to(D)),len(before),len(data),mode,hashlib.sha256(data).hexdigest())

with ThreadPoolExecutor(max_workers=6) as pool:results=[r for r in pool.map(convert,folder.iterdir()) if r]
mapping={r[0]:r[1] for r in results}
pattern=re.compile(r'assets/era/[a-f0-9]{24}\.(?:png|jpe?g)')
for p in D.rglob('*.html'):
    text=p.read_text();changed=pattern.sub(lambda m:mapping.get(m.group(),m.group()),text)
    if changed!=text:p.write_text(changed)
manifest=R/'content/era-reference/images.json';data=json.loads(manifest.read_text())
byold={r[0]:r for r in results}
for asset in data.values():
    if asset.get('path') in byold:
        old,new,before,after,mode,digest=byold[asset['path']]
        asset.update(path=new,optimizedEncoding=mode,optimizedSha256=digest,optimizedBytes=after)
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for old in mapping:(D/old).unlink()
report={'images':len(results),'before_bytes':sum(r[2] for r in results),'after_bytes':sum(r[3] for r in results),'paths':mapping}
(R/'docs/era-import/image-optimization.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='paths'}))
