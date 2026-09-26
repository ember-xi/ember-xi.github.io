"""Check complete source scope, key progression routes and final supplements."""
from pathlib import Path
from lxml import html
import json

R=Path(__file__).resolve().parents[1];C=R/'content';D=R/'dist';E=C/'era-reference'
inventory=json.loads((E/'inventory.json').read_text())
routes=json.loads((E/'build-routes.json').read_text())
audit=json.loads((E/'build-audit.json').read_text())
manifest=json.loads((C/'page-manifest.json').read_text())
assert not inventory['missing'],inventory['missing']
expected={r['title'] for r in inventory['articles']}
expected.update(r['title'] for r in inventory['replacements'] if r['kind']!='existing Zenith guide')
assert expected<=set(routes),sorted(expected-set(routes))
for r in inventory['replacements']:
    if r['kind']=='existing Zenith guide':assert r['route'] in manifest,r
assert not audit['unresolved_supplement_links'],audit['unresolved_supplement_links']
assert routes['??? Gloves']!=routes['Gloves']
assert routes['Curses, Foiled...Again!?']!=routes['Curses, Foiled Again!']
for title,key,category,distinct in [
 ('Ragnarok','relic-ragnarok','Items','mission-toau-45'),
 ('Ghosts of the Past','quest-ghosts-of-the-past','Quests','mission-toau-16'),
 ('Jeuno','region-jeuno',None,'mission-bastok-3-3'),
 ('Full Moon Fountain','zone-full-moon-fountain','Zones','mission-windurst-6-1'),
 ('Crest of Davoi','crest-of-davoi-quest','Quests','key-item-crest-of-davoi'),
]:
 assert routes[title]==key,(title,routes[title])
 assert key in manifest and distinct in manifest,(key,distinct)
 if category:assert manifest[key]['category']==category,(key,manifest[key]['category'])
warrior=html.parse(str(D/'warrior.html'))
assert warrior.xpath('//article//a[@href="relic-ragnarok.html"]'), 'WAR relic weapon resolves to a mission'
monk=html.parse(str(D/'monk.html'))
assert monk.xpath('//article//a[@href="beat-cesti.html"]'), 'MNK artifact weapon is not linked'
beat=html.parse(str(D/'beat-cesti.html'))
assert beat.xpath('//article//a[@href="quest-ghosts-of-the-past.html"]'), 'MNK AF1 resolves to a mission'
jobs=['Warrior','Monk','White Mage','Black Mage','Red Mage','Thief','Paladin','Dark Knight','Beastmaster','Bard','Ranger','Samurai','Ninja','Dragoon','Summoner','Blue Mage','Corsair','Puppetmaster','Dancer','Scholar']
for title in jobs:
    key=routes[title];doc=html.parse(str(D/(key+'.html')))
    assert doc.xpath('//article//img[contains(@class,"article-portrait")]'),title
    text=doc.xpath('//article')[0].text_content().lower()
    assert 'artifact' in text and 'relic' in text,title
for title in ['An Imperial Heist','Duties, Tasks, and Deeds','Forging a New Myth','Coming Full Circle','A Little Knowledge','Lakeside Minuet','Bravura']:
    assert title in routes,title
    doc=html.parse(str(D/(routes[title]+'.html')))
    assert len(doc.xpath('//article')[0].text_content())>250,title
for title in ['Zoredonite','Zikko']:assert manifest[routes[title]]['category']=='Monsters'
assert manifest[routes['Zephyr Mantle']]['category']=='Spells'
for title in ['Pet','Ebony Pole','Armor Sets/Level 1-10']:
    doc=html.parse(str(D/(routes[title]+'.html')))
    assert not doc.xpath('//article//a[normalize-space()="RUN" or normalize-space()="GEO" or normalize-space()="Geomancer"]'),title
print(f'PASS: {len(expected)} source-scope articles plus existing replacements accounted for; 20 job portraits, AF/Relic references and Mythic chain verified.')
print('PASS: no unresolved supplemental guide links; distinct item/quest identities and era-only job eligibility retained.')
