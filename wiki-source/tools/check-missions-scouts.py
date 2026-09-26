"""Regression checks for national mission navigation and source-based Scout maps."""
from pathlib import Path
from lxml import html
from PIL import Image
from collections import Counter
import runpy,re,json
R=Path(__file__).resolve().parents[1];D=R/'dist'
records=runpy.run_path(str(R/'content/english/mission_data.py'))['RECORDS']
assert len(records)==60
assert Counter(m['nation'] for m in records)=={'sandoria':20,'bastok':20,'windurst':20}
def key(m):return 'smash-the-orcish-scouts' if m['nation']=='sandoria' and m['number']=='1-1' else 'mission-'+m['nation']+'-'+m['number']
for nation in ['sandoria','bastok','windurst']:
    group=[m for m in records if m['nation']==nation]
    hub=html.parse(str(D/f'missions-{nation}.html'))
    assert all(hub.xpath('//*[@id=$id]',id='rank-'+str(i)) for i in range(1,10))
    for i,m in enumerate(group):
        doc=html.parse(str(D/(key(m)+'.html')))
        assert key(m)+'.html' in hub.xpath('//a/@href')
        walkthrough=doc.xpath('//*[@id="walkthrough"]')[0]
        route_steps=[]
        for node in walkthrough.itersiblings():
            if node.tag=='h2':break
            route_steps.extend(node.xpath('./li'))
        assert len(route_steps)>=2,(m['nation'],m['number'])
        nav=doc.xpath('//nav[@class="mission-nav"][1]//a/@href')
        assert f'missions-{nation}.html' in nav
        if i:assert key(group[i-1])+'.html' in nav
        if i<19:assert key(group[i+1])+'.html' in nav
        assert m['source'] in doc.xpath('//a/@href') and m['code'] in doc.xpath('//a/@href')
for name in ['zenith-scout','hands-that-guard','eyes-on-the-road']:
    doc=html.parse(str(D/(name+'.html')))
    text=doc.xpath('//article')[0].text_content()
    for phrase in ['H-7','F-6','report']:
        assert phrase.lower() in text.lower(),(name,phrase)
    assert 'X -264' not in text and '135, -7.793, 93' not in text, 'Use game-map grids in player directions'
    if name!='zenith-scout':
        assert 'zenith-scout.html' in doc.xpath('//a/@href')
        continue
    assert len(doc.xpath('//button[@data-enlarge-map]'))==2
    markers=doc.xpath('//*[contains(@class,"scout-marker")]/@style')
    assert len(markers)==2
    assert markers[0]=='left:46.875%;top:40.625%;width:6.25%;height:6.25%'
    assert markers[1]=='left:34.375%;top:34.375%;width:6.25%;height:6.25%'
    for src in doc.xpath('//figure//img/@src'):
        with Image.open(D/src) as im: assert im.size==(512,512)
for p in list((D/'assets/maps').glob('*'))+list((D/'assets/nations').glob('*')):
    with Image.open(p) as im:im.verify()
for file in ['mission-maps.json','nation-images.json','scout-maps.json']:
    assert '/workspace/' not in (R/'content'/file).read_text(),file
details=runpy.run_path(str(R/'content/english/sandoria_details.py'))
assert len(details['DETAILS'])==20
for num,detail in details['DETAILS'].items():
    doc=html.parse(str(D/(details['mission_key'](num)+'.html')))
    rows=doc.xpath('//*[@id="items-and-key-items"]/following-sibling::div[1]//tbody/tr')
    assert len(rows)==len(detail['carry']),(num,len(rows))
    assert all(row.xpath('./td[1]/a/@href') for row in rows),num
for name in details['KEY_ITEMS']:
    doc=html.parse(str(D/('key-item-'+details['slug'](name)+'.html')))
    assert 'cannot be bought at the Auction House' in doc.xpath('//article')[0].text_content(),name
journey=(D/'mission-sandoria-2-3.html').read_text()
assert 'Route A' in journey and 'Route B' in journey and 'Waughroon Shrine' in journey and 'Balga’s Dais' in journey
assert 'one real minute' in (D/'mission-sandoria-8-1.html').read_text()
assert 'requires zoning here, not an overnight wait' in (D/'mission-sandoria-6-2.html').read_text()
print('PASS: 60 mission pages; all 20 expanded San d’Oria routes, material links and key-item pages; both Journey Abroad branches; native wait corrections; navigation, Scout maps and images.')
