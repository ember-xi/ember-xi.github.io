"""Import reviewed external assets and strip temporary paths from provenance."""
from pathlib import Path
import json,shutil,sys
R=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]).resolve()
for name in ['sandoria','bastok','windurst']:
    dest=R/'dist/assets/nations';dest.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source/(name+'.jpg'),dest/(name+'.jpg'))
data=json.loads((source/'maps/map-manifest.json').read_text())
for a in data['assets']:
    dest=R/'dist/assets/maps';dest.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source/'maps'/a['filename'],dest/a['filename'])
def clean(value):
    if isinstance(value,list):return [clean(x) for x in value]
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k not in ['local_path','asset_directory','source_html_snapshot','path']}
    return value
(R/'content/mission-maps.json').write_text(json.dumps(clean(data),indent=2)+'\n')
(R/'content/nation-images.json').write_text(json.dumps(clean(json.loads((source/'nation-manifest.json').read_text())),indent=2)+'\n')
print('Imported nation images and',len(data['assets']),'route maps.')
scouts=json.loads((source/'scouts/scout-map-manifest.json').read_text())
for a in scouts['assets']:
    shutil.copyfile(source/'scouts'/a['filename'],R/'dist/assets/maps'/a['filename'])
(R/'content/scout-maps.json').write_text(json.dumps(clean(scouts),indent=2)+'\n')
