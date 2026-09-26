"""Check the requested story inventory and rendered walkthrough completeness."""
from pathlib import Path
from lxml import html
from collections import Counter
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('expansions', ROOT / 'content/english/expansion_missions.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
records = module.load_records()
mains = [r for r in records if not r.get('branch_of') and r.get('kind', 'mission') == 'mission']
expected = {'roz': 18, 'cop': 34, 'toau': 48, 'wotg': 54, 'acp': 12, 'amk': 15, 'asa': 15}
assert Counter(r['campaign'] for r in mains) == Counter(expected), 'Missing main mission entries'
for campaign, count in expected.items():
    if campaign != 'cop':
        assert {int(r['number']) for r in mains if r['campaign'] == campaign} == set(range(1, count + 1)), campaign
assert {str(r['number']) for r in mains if r['campaign'] == 'cop'} == {
    '1-1', '1-2', '1-3', '2-1', '2-2', '2-3', '2-4', '2-5',
    '3-1', '3-2', '3-3', '3-4', '3-5', '4-1', '4-2', '4-3', '4-4',
    '5-1', '5-2', '5-3', '6-1', '6-2', '6-3', '6-4',
    '7-1', '7-2', '7-3', '7-4', '7-5', '8-1', '8-2', '8-3', '8-4', '8-5'
}
assert len([r for r in records if r.get('branch_of') in ('3-3', '5-3')]) == 5
for nation in ('sandoria', 'bastok', 'windurst'):
    assert len([r for r in records if r.get('sequence_group') == 'past-' + nation]) == 13, ('Past nation chain incomplete', nation)
assert len([r for r in records if r['title'].startswith('Her Memories: ')]) == 9
keys = [module.key(r) for r in records]
assert len(keys) == len(set(keys)), 'Duplicate mission URLs'
missing_images = []
for record in records:
    key = module.key(record)
    for field in ('title', 'requirements', 'start', 'steps', 'reward', 'sources'):
        assert record.get(field), (key, 'empty ' + field)
    assert all(isinstance(s, str) and s.strip() for s in record['steps']), key
    page = html.parse(str(ROOT / 'dist' / (key + '.html')))
    article = page.xpath('//article')[0]
    if not record.get('reuse_existing'):
        assert article.xpath('.//h2[normalize-space()="Before you begin"]'), key
        assert article.xpath('.//h2[normalize-space()="Walkthrough"]'), key
        assert article.xpath('.//ol/li'), key
    if record.get('availability_note'):
        assert article.xpath('.//aside[contains(@class,"mission-availability")]'), (key, 'missing availability note')
    if not article.xpath('.//img'):
        missing_images.append(key)
for nation in ('sandoria', 'bastok', 'windurst'):
    manifest = json.loads((ROOT / 'content/page-manifest.json').read_text())
    pages = [k for k, p in manifest.items() if p['parent'] == 'missions-' + nation and p['category'] == 'Missions']
    assert len(pages) == 20, (nation, len(pages))
    for key in pages:
        page = html.parse(str(ROOT / 'dist' / (key + '.html')))
        if not page.xpath('//article//img'):
            missing_images.append(key)
assert not missing_images, ('Walkthroughs without an image or area map', missing_images)
for key, target in [('sky-access', 'mission-roz-13.html'), ('sea-access', 'mission-cop-7-5.html')]:
    page = html.parse(str(ROOT / 'dist' / (key + '.html')))
    assert target in page.xpath('//article//a/@href'), key
print('PASS: all 196 expansion main mission entries, five CoP branch routes, and 60 national missions are present.')
print('PASS:', len(records) - len(mains), 'branch/access/epilogue/quest guides; every walkthrough has images or local maps and nonempty steps/requirements.')
