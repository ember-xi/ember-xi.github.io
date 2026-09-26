"""Import an attributed factual zone snapshot and verified map assets."""
from pathlib import Path
import json, shutil, sys, re

root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1])
data_file = source / 'zones-facts-merged.json'
if not data_file.exists():
    data_file = source / 'zones-facts.json'
data = json.loads(data_file.read_text())
assets = json.loads((source / 'map-assets.json').read_text())
asset_by_name = {k.removeprefix('File:').replace('_', ' ').casefold(): v for k, v in assets.items()}
destination = root / 'dist/assets/zones'
destination.mkdir(parents=True, exist_ok=True)
copied = set(); unresolved = []
for z in data['zones']:
    for m in z.get('maps', []):
        a = m.copy() if m.get('url') else asset_by_name.get(m['title'].removeprefix('File:').replace('_', ' ').casefold())
        if not a:
            if not m.get('url'):
                unresolved.append((z['name'], m['title']))
            continue
        m.update({k:a[k] for k in ('url','sourceUrl','width','height') if a.get(k)})
        if a.get('localPath') and Path(a['localPath']).is_file():
            src = Path(a['localPath'])
            if not src.stat().st_size:
                original = Path(m.get('originalLocalPath') or '')
                if not original.is_file() or not original.stat().st_size:
                    raise ValueError('Empty map image: ' + str(src))
                src = original
                m['url'] = m.get('originalUrl') or m['url']
                m['width'] = m.get('originalWidth') or m['width']
                m['height'] = m.get('originalHeight') or m['height']
            if src.name not in copied:
                shutil.copyfile(src, destination / src.name)
                copied.add(src.name)
            m['localPath'] = 'assets/zones/' + src.name
        m.pop('originalLocalPath', None)
    for mob in z.get('monsters', []):
        if any(marker in mob.get('spawns', '') for marker in ('NM=', 'NM =', 'Pos:', 'Template:')):
            raise ValueError('Malformed spawn field: ' + z['name'] + ' / ' + mob['name'])
(root / 'content/zone-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Imported {len(data["zones"])} zones and {len(copied)} local map assets.')
if unresolved:
    print('Map references without image URLs:', json.dumps(unresolved))
