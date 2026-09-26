"""Validate the published English route graph and imported package facts."""
from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
from collections import Counter
from functools import lru_cache
import json,re
R=Path(__file__).resolve().parents[1];D=R/'dist';C=R/'content'
m=json.loads((C/'page-manifest.json').read_text());old=json.loads((C/'legacy-pages.json').read_text());errors=[];links=0
retired={'an-edge-earned','hands-that-guard','stand-your-ground','hold-the-line','a-pair-of-quiet-blades','eyes-on-the-road','a-clean-recovery','a-shadows-safeguard','a-shadow-reforged','breakwater-crab'}
redirects=retired|{'road-companion','coastal-dispatch','sandbound-repairs','the-broken-watch','adventures'}
redirects|={'aht-urhgan-mission-16-ghosts-of-the-past','aht-urhgan-mission-45-ragnarok','crest-of-davoi-key-item','full-moon-fountain-mission','jeuno-mission'}
files={p.resolve():html.parse(str(p)) for p in D.rglob('*.html')}
idsets={p:set(doc.xpath('//@id')) for p,doc in files.items()}
@lru_cache(maxsize=None)
def local_ref(parent,value):
 u=urlsplit(value)
 if u.scheme or u.netloc:return None
 target=(parent/unquote(u.path)).resolve() if u.path else None
 return target,unquote(u.fragment),target.is_file() if target else True
for p,doc in files.items():
 if doc.xpath('string(/html/@lang)')!='en':errors.append((p.name,'language'))
 if re.search(r'[\u0600-\u06ff]',p.read_text()):errors.append((p.name,'untranslated text'))
 ids=doc.xpath('//@id')
 if any(n>1 for n in Counter(ids).values()):errors.append((p.name,'duplicate IDs'))
 if p.parent==D.resolve() and p.stem not in redirects:
  if len(doc.xpath('//h1'))!=1:errors.append((p.name,'title count'))
  if not doc.xpath('//link[starts-with(@href,"assets/wiki.css")]'):errors.append((p.name,'old stylesheet'))
  if not doc.xpath('//nav[@aria-label="Wiki navigation"]'):errors.append((p.name,'missing navigation'))
 for attr in ['href','src']:
  for value in doc.xpath('//@'+attr):
   if value.lower().startswith('wiki:'):errors.append((p.name,'unresolved wiki reference',value));continue
   ref=local_ref(p.parent,value)
   if ref is None:continue
   target,fragment,exists=ref;target=target or p
   if not exists:errors.append((p.name,'missing',value));continue
   if fragment and target in files and fragment not in idsets[target]:errors.append((p.name,'fragment',value))
   links+=1
for p in (D/'assets').glob('*.js'):
 if re.search(r'[\u0600-\u06ff]',p.read_text()):errors.append((str(p),'untranslated script'))
for error in errors:print('ERROR',error)
assert set(old)-redirects<=set(m),'Old URLs removed'
assert len(m)+len(redirects)==len(list(D.glob('*.html')))
assert files[(D/'road-companion.html').resolve()].xpath('//meta[@http-equiv="refresh"]/@content')==['0;url=mounts.html']
assert all((D/(k+'.html')).is_file() for k in m)
alllinks=set(files[(D/'all-pages.html').resolve()].xpath('//a/@href'))
assert all(k+'.html' in alllinks or k=='all-pages' for k in m)
js=(D/'assets/search-index.js').read_text();index=json.loads(js.split('window.ZENITH_ARTICLES=',1)[1].split(';\nwindow.ZENITH_LEGACY=')[0])
assert {a['url'] for a in index}=={k+'.html' for k in m}
legacy=json.loads(js.split('window.ZENITH_LEGACY=',1)[1].strip().rstrip(';'))
assert all((D/url).is_file() for url in legacy.values())
source=html.parse(str(C/'market-catalog-source.html'))
actual=files[(D/'market-catalog.html').resolve()]
a=[[x.text_content() for x in row.findall('td')] for row in source.xpath('//tbody/tr')]
b=[[x.text_content() for x in row.findall('td')] for row in actual.xpath('//*[@id="market-table"]//tbody/tr')]
assert a==b and len(b)==689,'Catalogue values changed'
assert len(set(actual.xpath('//*[@id="market-table"]//tbody/tr/td[1]/a/@href')))==689
assert len(files[(D/'exp-camps.html').resolve()].xpath('//*[@id="camp-table"]//tbody/tr'))==18
assert len([k for k in m if k.startswith('camp-') and k!='camp-travel-rules'])==18
for key,phrases in {
 'healers-promise':['3 Honey + 3 Distilled Water','H-9','30','Apururu (UC)','Accept the supply request'],
 'mounts':['Chocobo License','Mairee','Couvoullie','G-7'],
 'zenith-outpost':['F-5','Home Point #1','Conquest Points','No Supply Run'],
 'an-adventurer-leads':['15 enemies','45 or higher','50','five Trusts'],
 'companions-of-the-road':['10 enemies','25 or higher','30','four Trusts'],
 'equipment-quests':['Phara','Brygid','Razor Axe','Existing equipment','Original'],
 'first-limit-break':['Exoray Mold','Bomb Coal','Ancient Papyrus','third eligible kill','Trade','55'],
 'limit-break':['In Defiant Challenge','Testimony requirement','no automatic increases','Shattering Stars'],
 'auction-house':['689','5,000','20,000','100,000','installation'],
 'thief':['level 20','10%','Treasure Hunter'],
 'sparks-essentials':['always available','Qultada','King','Cid','Gilgamesh','F. Coffin','500 Sparks','weekly spending limit'],
 'fame-access':['182','173','preceding quests','real Fame','original non-Fame timers'],
 'update-log':['all 175 source files match','Three Roads','helper absent'],
}.items():
 text=files[(D/(key+'.html')).resolve()].xpath('//article')[0].text_content()
 for phrase in phrases:assert phrase.lower() in text.lower(),(key,phrase)
if errors:raise SystemExit(1)
print(f'PASS: {len(files)} HTML routes, {len(m)} indexed English articles, {links} local links/assets. All {len(old)} previous articles preserved.')
print('PASS: identical 689-item catalogue, 18 camp pages, no Arabic in public HTML/scripts, no missing targets or duplicate IDs. Key quest rules retained.')
