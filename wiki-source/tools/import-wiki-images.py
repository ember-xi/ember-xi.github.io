"""Import a reviewed image manifest; no network lookups during site builds."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('manifest', type=Path)
args = parser.parse_args()
data = json.loads(args.manifest.read_text())
assets = []
seen = set()
for record in data['assets']:
    source = Path(record['localPath'])
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != record['sha256']:
        raise ValueError('Image differs from reviewed bytes: '+record['title'])
    title_key = re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', record['title']).encode('ascii', 'ignore').decode().lower())
    identity = (record['kind'], title_key)
    if identity in seen:
        raise ValueError('Duplicate image identity: '+str(identity))
    seen.add(identity)
    suffix = source.suffix.lower()
    if suffix not in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
        raise ValueError('Unsupported image type: '+suffix)
    relative = 'assets/entities/'+digest[:20]+suffix
    target = ROOT / 'dist' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(source, target)
    elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise ValueError('Image filename collision')
    item = dict(record)
    item['localPath'] = relative
    item['assetId'] = record['kind']+'-'+title_key+'-'+digest[:8]
    assets.append(item)

output = {'retrievedAt': data['retrievedAt'], 'assets': assets, 'unresolved': data.get('unresolved', []), 'notes': data.get('notes', [])}
(ROOT/'content/image-assets.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
print('Imported', len(assets), 'verified image mappings.')
