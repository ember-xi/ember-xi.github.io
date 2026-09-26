"""Verify full source-catalog coverage, map integrity and rendered factual rows."""
from pathlib import Path
from lxml import html
from PIL import Image
from collections import Counter
import json, re, unicodedata

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'content/zone-data.json').read_text())['zones']
manifest = json.loads((root / 'content/page-manifest.json').read_text())
norm = lambda s: re.sub('[^a-z0-9]', '', unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower())
pages = {norm(p['title']): k for k, p in manifest.items() if k.startswith('zone-') and p['category']=='Zones'}
assert len(data) == len({norm(z['name']) for z in data}), 'Duplicate zone names'
assert {norm(z['name']) for z in data} == set(pages), 'World catalog and rendered zones differ'
index = html.parse(str(root / 'dist/zones.html'))
category_links = index.xpath('//section[contains(@class,"area-group")]//li/a/@href')
assert set(category_links) == {k+'.html' for k in pages.values()}, 'Area category links are incomplete'
assert not index.xpath('//*[@id="zone-count" or @id="zone-search" or @id="zone-expansion"]'), 'Unexpected dashboard controls'
assert not index.xpath('//*[contains(@class,"zone-stats")]'), 'Unexpected zone counters'
assert index.xpath('//div[@class="world-maps"]//img'), 'Missing reference world maps'
maps = 0; images = set(); monsters = 0; quests = 0
for z in data:
    p = root / 'dist' / (pages[norm(z['name'])]+'.html')
    doc = html.parse(str(p))
    content = doc.xpath('//article')[0].text_content()
    assert doc.xpath('//table[@class="zone-information"]'), 'Missing zone infobox: '+z['name']
    assert doc.xpath('//nav[@data-zone-contents]/ul/li/a'), 'Missing article contents: '+z['name']
    assert z.get('sourceUrl'), z['name']
    assert z.get('hasSourcePage') or z.get('hasInfobox'), 'Unresolved area reference: '+z['name']
    assert z.get('expansion'), 'Missing expansion: '+z['name']
    assert '{{' not in content and '[[' not in content, 'Raw template markup: '+z['name']
    for m in z.get('maps', []):
        src = m.get('localPath') or m.get('url')
        if not src:
            continue
        assert doc.xpath('//img[@src=$src]', src=src), (z['name'], src)
        maps += 1
        if m.get('localPath'):
            asset = root / 'dist' / src
            assert asset.is_file()
            if asset not in images:
                with Image.open(asset) as image:
                    image.verify()
                images.add(asset)
    for kind, records in [('monsters', z.get('monsters', [])), ('quests', z.get('quests', []))]:
        for item in records:
            assert item['name'] in content, (z['name'], kind, item['name'])
        if kind == 'monsters': monsters += len(records)
        else: quests += len(records)
print(f'PASS: {len(data)} zone pages match the complete source catalog; {maps} map placements ({len(images)} local images verified), {monsters} monster rows and {quests} quest/mission rows rendered.')
