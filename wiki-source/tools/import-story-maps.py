"""Import reviewed original map bytes and their exact area/source identities."""
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('manifests', nargs='+', type=Path)
args = parser.parse_args()
groups = defaultdict(list)
no_maps = []
for path in args.manifests:
    data = json.loads(path.read_text())
    if 'zones' in data:
        for zone in data['zones']:
            groups[zone['zone']].extend(zone['maps'])
    else:
        for asset in data['assets']:
            groups[asset['zone']].append(asset)
    no_maps.extend(data.get('noMapZones', []))
catalogue_path = ROOT / 'content/zone-data.json'
catalogue = json.loads(catalogue_path.read_text())
zones = {z['name']: z for z in catalogue['zones']}
provenance = []
for name, assets in groups.items():
    assert name in zones, ('Unknown zone', name)
    imported = []
    seen = set()
    for asset in assets:
        source = Path(asset['localPath'])
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert digest == asset['sha256'], ('Map bytes changed', source)
        if digest in seen:
            continue
        seen.add(digest)
        relative = 'assets/missions/maps/' + digest[:20] + source.suffix.lower()
        destination = ROOT / 'dist' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            assert hashlib.sha256(destination.read_bytes()).hexdigest() == digest
        else:
            shutil.copyfile(source, destination)
        item = dict(asset)
        item['localPath'] = relative
        item['url'] = asset['sourceUrl']
        item['originalUrl'] = asset['sourceUrl']
        item['sourceUrl'] = asset['sourcePage']
        item['mapPageUrl'] = asset['sourcePage']
        item['title'] = asset.get('title') or asset.get('name')
        item['mapLabel'] = (asset.get('mapId') or '').replace('Map', 'Map ')
        item['mapSourceLabel'] = asset.get('sourceLabel') or asset.get('source')
        if 'Japanese' in asset.get('language', '') or 'Japanese' in asset.get('caption', ''):
            item['mapSourceLabel'] += ' — Japanese annotations'
        imported.append(item)
        provenance.append({'zone': name, **item})
    zones[name]['maps'] = imported
    zones[name]['mapEditorialNote'] = 'Maps retain their source annotations. Follow the mission steps for Zenith requirements; modern reference markers do not grant access. Instance galleries show alternative layouts, not a single continuous route.'
for item in no_maps:
    assert item['zone'] in zones
    zones[item['zone']]['noInGameMap'] = True
    zones[item['zone']]['mapEditorialNote'] = item['note']
    zones[item['zone']]['mapNoteSources'] = item['sources']
catalogue_path.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'content/story-map-provenance.json').write_text(json.dumps({'retrievedAt': '2026-09-25', 'assets': provenance, 'noMapZones': no_maps}, ensure_ascii=False, indent=2) + '\n')
print('Imported', len(provenance), 'unchanged map images for', len(groups), 'zones;', len(no_maps), 'documented no-map zone.')
