"""Build the complete English wiki from reviewed editorial and package data."""
from pathlib import Path
from html import escape
from lxml import html
import importlib.util,json,re,unicodedata
R=Path(__file__).resolve().parents[1];C=R/'content';D=R/'dist'
spec=importlib.util.spec_from_file_location('articles',C/'english/articles.py');ed=importlib.util.module_from_spec(spec);spec.loader.exec_module(ed)
P=ed.P;add=ed.add;link=ed.link;para=ed.para;section=ed.section;table=ed.table;listing=ed.listing;steps=ed.steps
mspec=importlib.util.spec_from_file_location('missions',C/'english/missions.py');missions=importlib.util.module_from_spec(mspec);mspec.loader.exec_module(missions);missions.install(ed)
legacy=json.loads((C/'legacy-routes.json').read_text())
old=json.loads((C/'legacy-pages.json').read_text())
def slug(t):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()).strip('-')
def listlinks(keys):return listing([link(k) for k in keys])
def serial(e):return html.tostring(e,encoding='unicode',with_tail=False)
def contents(e):return escape(e.text or '')+''.join(html.tostring(c,encoding='unicode',with_tail=True) for c in e)
def text(t):return html.fragment_fromstring(t,create_parent='div').text_content()
# Exact source camp facts, each with its own walkthrough.
camps=json.loads((C/'camp-catalog.json').read_text())['camps'];campkeys=[];zones={};rows=[]
for c in camps:
 name=c['name'].replace('Crawlers Nest','Crawlers’ Nest').replace('RuAun Gardens','Ru’Aun Gardens')
 key=f'camp-{slug(name)}-{c["low"]}-{c["high"]}';zonekey='zone-'+slug(name);campkeys.append(key)
 targets=table(['Target','Training book'],[(escape(t.strip()),escape(c['training'])+' · Page '+str(c['page'])) for t in c['targets'].split(',')])
 body=section('Getting there',steps('Open Zenith Atlas. Select Recommended for my level or Browse levels 10-75.',f'Select {name}, levels {c["low"]}–{c["high"]}. You must meet the lower level of the range.',escape(c['route']),f'Examine the original {c["training"]} and select Page {c["page"]}. Atlas does not activate training for you.'))+section('Targets',targets)+section('Before you fight',para(f'{c["trusts"]} Trusts are suggested. This is a difficulty recommendation, not an automatic capacity unlock. '+link('trust-journeys','Earn additional slots through Trust Journeys.'))+para('Check enemies before fighting. Some targets stop awarding EXP before the end of the suggested range, and route targets can differ from the complete training-page list.')+para('Travel gives one minute of Sneak, Invisible and Deodorize; some detection types can bypass these. '+link('camp-travel-rules','Read the camp travel rules.')))
 if c.get('sky'):body+=para('<strong>Sky access:</strong> The Gate of the Gods progress and a previous Ru’Aun Gardens visit are required. Atlas does not unlock the story.')
 book_grid=json.loads((C/'map-grid-locations.json').read_text())['camp_books'][str(c['zone'])]
 body+=section('Map location',para(c['training']+' at '+book_grid+'. '+('The Atlas arrival is beside the outpost books.' if c['zone'] in (103,126) else 'Start here, then follow the route above to the hunting area.')))
 if c['zone']==103:body+=section('Arrival correction',para('Travel and Quest Clarity v1.0 corrects both Valkurm camp routes. At login, it can move an alive, out-of-combat character still within three yalms of the former bad arrival to the corrected point, once per character. It is not a general unstuck command.'))
 add(key,f'{name}: Levels {c["low"]}–{c["high"]}','EXP Camps',f'A Zenith Atlas camp in {link(zonekey,name)}.',body,[('Recommended level',f'{c["low"]}–{c["high"]}'),('Suggested Trusts',str(c['trusts'])),('Training',f'{c["training"]} · Page {c["page"]}'),('Zone',link(zonekey,name))],parent='exp-camps',status=ed.CLARITY if c['zone']==103 else None)
 rows.append(f'<tr data-low="{c["low"]}" data-high="{c["high"]}"><td>{c["low"]}–{c["high"]}</td><td>{link(key,name)}</td><td>{escape(c["targets"])}</td><td>{c["training"]} · {c["page"]}</td><td>{c["trusts"]}</td></tr>')
 zones.setdefault(zonekey,{'name':name,'keys':[],'zone':c['zone'],'route':c['route']})['keys'].append(key)
for k,z in zones.items():
 body=section('EXP camps',listlinks(z['keys']))+section('Arrival and hazards',para(z['route']))
 if k in ['zone-valkurm-dunes','zone-qufim-island']:body+=section('Zenith NPCs',para(link('zenith-scout','Zenith Scout')+' handles active equipment-quest field steps. '+link('zenith-atlas','Zenith Atlas')+' handles camp travel. They are placed near the outpost staging point in the prepared placement packages.'))
 add(k,z['name'],'Zones','Camp routes and documented Zenith services in '+z['name']+'.',body,[('Zone ID',str(z['zone']))],parent='zones')
add('exp-camps','EXP Camps','Guides','Choose a level range to open its own travel route, targets and training-page guide.',section('Find a camp','''<div class="filter-bar"><label for="camp-level">Your level <input id="camp-level" type="number" min="1" max="75" placeholder="1–75"></label><button id="camp-reset" type="button">Show all</button><span id="camp-count" role="status">18 camps</span></div><div class="table-wrap"><table id="camp-table"><thead><tr><th>Level</th><th>Camp</th><th>Targets</th><th>Training</th><th>Trusts</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div><p id="camp-empty" hidden>No camp in this catalogue matches that level. From levels 1–9, begin outside your starting city.</p>''')+section('Using the Atlas',para('The catalogue contains 18 recommendations through level 75. Level ranges are guidance; move on if enemies become Too Weak. '+link('camp-travel-rules','Travel rules')+' explain arrival protection and story conditions.')))
# City entries keep every location grounded in the reviewed guide.
citydata=[
('southern-san-doria','Southern San d’Oria',[('Alaune','Tutorial training'),('Zenith Guide','Gate Crystal travel only'),('Zenith Atlas','EXP camp travel'),('Rolandienne','RoE and Sparks'),('Gondebaud','Trust registration and Cipher exchanges; L-6')]),
('northern-san-doria','Northern San d’Oria',[('Zenith Armsmith','Equipment quests, Trust slots and Crystal Paths; near Home Point #1'),('Matildie','Adventurer Coupon'),('Excenmille','San d’Oria Trust quest; D-9'),('Jeanvirgaud','Outpost teleportation'),('Secodiand','Fear of the Dark')]),
('bastok-markets','Bastok Markets',[('Gulldago','Tutorial training'),('Zenith Guide','Gate Crystal travel only'),('Zenith Atlas','EXP camp travel'),('Isakoth','RoE and Sparks')]),
('windurst-woods','Windurst Woods',[('Selele','Tutorial training'),('Zenith Guide','Gate Crystal travel only'),('Zenith Atlas','EXP camp travel'),('Fhelm Jobeizat','RoE and Sparks'),('Wetata','Trust registration and Cipher exchanges'),('Apururu','A Healer’s Promise; Manustery, H-9'),('Wije Tiren','Distilled Water vendor')]),
('upper-jeuno','Upper Jeuno',[('Brutus','Chocobo’s Wounds at the chocobo stables'),('Mapitoto','A Companion for the Road at the chocobo stables'),('Mejuone','Gysahl Greens vendor at the stables')])]
for k,title,services in citydata:
 body=section('NPCs and services',table(['NPC','Service'],services))
 if k=='windurst-woods':body+=section('Apururu’s location',para('Inside the Manustery at H-9. See '+link('healers-promise','A Healer’s Promise')+' for the marked map and complete walkthrough.'))
 if k=='upper-jeuno':body+=section('Chocobo route',para('The custom '+link('road-companion','personal chocobo quest')+' examines Home Points in order #1 → #3 → #2, after feeding.'))
 add('zone-'+k,title,'Zones','Documented quest contacts and Zenith services in '+title+'.',body,parent='zones',status=ed.CLARITY if k!='upper-jeuno' else None)
# Catalogue values are copied verbatim. Each catalogue item is independently addressable.
market=html.parse(str(C/'market-catalog-source.html'));marketrows=[];itemkeys=[];itemmap={};special={'4370':'honey','4509':'distilled-water','4545':'gysahl-greens'}
for row in market.xpath('//tbody/tr'):
 cells=[x.text_content().strip() for x in row.findall('td')]
 name,i,level,buy,stack,buystack,sell,sellstack=cells
 key=special.get(i,'item-'+i+'-'+slug(name));itemkeys.append(key);itemmap[i]=key
 stats=section('Auction House prices',table(['Listing','Buy from supplied stock','Automated buyer cap'],[('Single',buy+' gil',sell+' gil'),('Stack of '+stack,buystack+' gil' if buystack!='—' else 'Not stackable',sellstack+' gil' if sellstack!='—' else 'Not stackable')]))
 note=para('Prices describe Auction Market v1.0, not live inventory. The service must be installed and running. Bidding above the supply price spends the higher amount. Automated purchases remain subject to '+link('auction-house','market limits')+'.')
 if key in P:P[key]['body']+=stats+note
 else:
  facts=[('Item ID',i),('Stack size',stack)]
  if level!='—':facts.append(('Equipment level',level))
  add(key,name,'Items',f'{escape(name)} is included in the Zenith Auction Market starter catalogue.',stats+section('How to buy',steps('Open an Auction House counter and find this item.','Select a single or stack listing as applicable. Bid the listed supply price when stock is available.'))+section('Selling to the market',para('List the item at or below its buyer cap. The service can buy it after at least one minute, on the next five-minute cycle, if the daily limits allow. Proceeds arrive through the Mog House Delivery Box from AH-Jeuno.')+note),facts,parent='items')
 search=' '.join(cells[:3]);marketrows.append('<tr data-search="'+escape(search.lower(),quote=True)+'"><td>'+link(key,escape(name))+'</td>'+''.join('<td>'+escape(c)+'</td>' for c in cells[1:])+'</tr>')
add('market-catalog','Auction House Price Catalogue','Economy','Browse all 689 items in Auction Market v1.0. Open an item name for its own reference page.',section('Catalogue','''<div class="filter-bar"><label for="market-search">Find an item <input id="market-search" type="search" placeholder="Name, item ID or level" autocomplete="off"></label><button id="market-reset" type="button">Clear</button><span id="market-count" role="status">689 items</span></div><div class="table-wrap"><table id="market-table"><thead><tr><th>Item</th><th>ID</th><th>Level</th><th>Buy single</th><th>Stack size</th><th>Buy stack</th><th>Buyer cap / single</th><th>Buyer cap / stack</th></tr></thead><tbody>'''+''.join(marketrows)+'''</tbody></table></div><p id="market-empty" hidden>No matching items. Try a shorter name or an item ID.</p>''')+para('All prices are in gil. A dash means the field does not apply. These fixed package prices are not a live inventory feed. '+link('auction-house','Read buying, selling and daily-limit rules.')),parent='auction-house',status=ed.READY)
# Index lists are ordinary wiki links, not nested article content.
def directory(keys,ident=None):
 return '<ul class="page-directory"'+(f' id="{ident}"' if ident else '')+'>'+''.join(f'<li data-filter="{escape(P[k]["title"].lower(),quote=True)}">{link(k)}</li>' for k in sorted(keys,key=lambda k:P[k]['title'].lower()))+'</ul>'
add('items','Items','Items','Item references, quest materials and catalogue prices for Zenith XI.',section('Quest materials',listlinks(['honey','distilled-water','gysahl-greens','gausebit-wildgrass']))+section('Browse items','<div class="filter-bar"><label>Filter item names <input type="search" data-list-filter="item-directory" placeholder="Start typing an item name"></label><span data-list-count="item-directory" role="status"></span></div>'+directory(itemkeys,'item-directory'))+para('The catalogue covers the starter market selection, not every item in FINAL FANTASY XI. Augmented quest rewards are described on their quest pages.'))
add('zones','Zones','Zones','Open a zone for its documented Zenith services, camps and quest links.',section('Cities',directory(['zone-'+c[0] for c in citydata]))+section('Adventure areas',directory(list(zones))))
add('npcs','NPCs','NPCs','Quest givers and guides with documented Zenith services.',section('NPC directory',directory([k for k,p in P.items() if p['category']=='NPCs'])))
questgroups=[('Equipment journeys',[e[2] for e in ed.EQUIPMENT]),('Three Roads',[r[0] for r in ed.ROAD]),('Trust progression',['healers-promise','trust-san-doria','companions-of-the-road','an-adventurer-leads']),('Travel and training',['adventurer-coupon','tutorial-quests','crystal-paths','chocobos-wounds','road-companion']),('Original quests',['fear-of-the-dark'])]
add('quests','Quests','Quests','Every quest below has a separate walkthrough with requirements, the starting NPC, objectives and rewards.',''.join(section(t,directory(keys)) for t,keys in questgroups))
# Primary sources: preserve the reviewed version, not moving upstream claims.
sourceurls=json.loads((C/'source-links.json').read_text())
labels=['Equipment data','Tutorial Quest','Records of Eminence','Trust implementation','Ashita configurations','XIPivot 4.3.001','Player messages and NPC direction']
add('sources','Sources','Reference','Zenith’s custom rules are documented from its delivered source packages. Upstream references explain the base game and tools.',section('Zenith packages',listing(['Starter Weapons; Complete v0.9.2; Warrior v1.0; THF20.','RoE + Sparks v1.0; Sparks Essentials v1.0; Cleanup Phase 2 permanent Cipher selection.','Trust Combat v1.0; Trust Recovery v1.1; Adventurer Progression v1.0.','Apururu Quest v1.0; Three Roads v1.0; Job Journeys v1.0.','Travel v1.1; Gate Crystals v1.0; Road Companion v1.0.','Adventurer Log v1.0; NPC Placement v1.0; Quest Readability v1.0; Menu Pages v1.0; Qufim Wall v1.0; NPC Roles v1.0.', 'Sandoria NPC Row v1.0: layout confirmed by the player. Travel and Quest Clarity v1.0: six-file update prepared and tested offline; installation not yet confirmed.','Fame Access v1.0 source edits; Cleanup Phase 1 and Phase 2 v1.0; installed-source audit dated 19 September 2026.','Auction Market v1.0 and its 689-item price catalogue.']))+section('Upstream references',listing([f'<a href="{escape(url)}">{label}</a>' for label,url in zip(labels,sourceurls)]))+section('Maps and artwork',para('Windurst Woods map: <a href="https://www.ffxi-atlas.com/maps/windurst_woods/">Vana’diel Atlas</a>. Honey and Apururu game images © SQUARE ENIX. Locations use the letter and number shown on the game map, with dungeon sections where needed.'))+section('Documentation status',para('Source availability is not proof that a package is installed on the running server. Consult '+link('update-log','Update Log')+' for the evidence recorded so far. Custom Zenith rules take precedence over generic retail instructions where documented.')))
# Simple traditional wiki front page.
portal=[('Begin your adventure',['getting-started','server-rules','tutorial-quests','adventurer-coupon','fame-access']),('Quests & missions',['quests','missions','equipment-quests','adventurer-log']),('Jobs & companions',['jobs','warrior','thief','trusts','trust-journeys']),('Explore Vana’diel',['exp-camps','zones','travel','gate-crystals','mounts']),('Items & economy',['items','auction-house','market-catalog','crafting']),('Systems & support',['records-of-eminence','sparks-essentials','launcher','npcs'])]
body='<div class="wiki-portals">'+''.join('<section class="portal"><h2>'+t+'</h2>'+listlinks(keys)+'</section>' for t,keys in portal)+'</div>'
body+=section('Featured walkthroughs',table(['NPC','Quest','Reward'],[(link('apururu','Apururu')+'<br>Windurst Woods (H-9)',link('healers-promise','A Healer’s Promise'),'Permanent Apururu (UC)'),(link('zenith-armsmith','Zenith Armsmith')+'<br>Northern San d’Oria (E-8)',link('a-pair-of-quiet-blades','A Pair of Quiet Blades'),'2 Poison Daggers — each with Accuracy +2, Attack +1'),(link('mapitoto','Mapitoto')+'<br>Upper Jeuno (G-7)',link('road-companion','A Companion for the Road'),'Personal chocobo · quest source verified')]))
body+=section('About Zenith XI',para('A personal level-75 FINAL FANTASY XI adventure with Trust companions, custom side quests and exploration-based progression. The wiki keeps original systems and Zenith changes clearly documented.'))+para(link('update-log','Recent updates')+' · '+link('roadmap','Development roadmap')+' · '+link('sources','Sources'))
add('index','Main Page','Home','Welcome to the Zenith XI Wiki — your guide to quests, equipment, companions and the road to level 75.',body)
sspec=importlib.util.spec_from_file_location('scouts',C/'english/scouts.py');scouts=importlib.util.module_from_spec(sspec);sspec.loader.exec_module(scouts);scouts.install(ed)
aspec=importlib.util.spec_from_file_location('adventures',C/'english/adventures.py');adventures=importlib.util.module_from_spec(aspec);aspec.loader.exec_module(adventures);adventures.install(ed)
espec=importlib.util.spec_from_file_location('eco_warrior',C/'english/eco_warrior.py');eco_warrior=importlib.util.module_from_spec(espec);espec.loader.exec_module(eco_warrior);eco_warrior.install(ed)
pspec=importlib.util.spec_from_file_location('progression',C/'english/progression.py');progression=importlib.util.module_from_spec(pspec);pspec.loader.exec_module(progression);progression.install(ed)
wspec=importlib.util.spec_from_file_location('world_quests',C/'english/world_quests.py');world_quests=importlib.util.module_from_spec(wspec);wspec.loader.exec_module(world_quests);world_quests.install(ed)
qspec=importlib.util.spec_from_file_location('quest_guides',C/'english/quest_guides.py');quest_guides=importlib.util.module_from_spec(qspec);qspec.loader.exec_module(quest_guides);quest_guides.install(ed)
ispec=importlib.util.spec_from_file_location('item_guides',C/'english/item_guides.py');item_guides=importlib.util.module_from_spec(ispec);ispec.loader.exec_module(item_guides)
itemmap,item_aliases=item_guides.install(ed,itemmap,quest_guides.QUESTS)
itemmap={str(i):key for i,key in itemmap.items()}
dspec=importlib.util.spec_from_file_location('sandoria_details',C/'english/sandoria_details.py');sandoria_details=importlib.util.module_from_spec(dspec);dspec.loader.exec_module(sandoria_details)
item_aliases.update(sandoria_details.install(ed,itemmap))
jspec=importlib.util.spec_from_file_location('jeuno_travel',C/'english/jeuno_travel.py');jeuno_travel=importlib.util.module_from_spec(jspec);jspec.loader.exec_module(jeuno_travel);jeuno_travel.install(ed)
cspec=importlib.util.spec_from_file_location('classic_equipment',C/'english/classic_equipment.py');classic_equipment=importlib.util.module_from_spec(cspec);cspec.loader.exec_module(classic_equipment);classic_equipment.install(ed)
sspec=importlib.util.spec_from_file_location('story_retirement',C/'english/story_retirement.py');story_retirement=importlib.util.module_from_spec(sspec);sspec.loader.exec_module(story_retirement);story_retirement.install(ed)
mspec=importlib.util.spec_from_file_location('native_maat',C/'english/native_maat.py');native_maat=importlib.util.module_from_spec(mspec);mspec.loader.exec_module(native_maat);native_maat.install(ed)
aspec=importlib.util.spec_from_file_location('astrolabe',C/'english/astrolabe.py');astrolabe=importlib.util.module_from_spec(aspec);aspec.loader.exec_module(astrolabe);astrolabe.install(ed)
kspec=importlib.util.spec_from_file_location('weighted_stones',C/'english/weighted_stones.py');weighted_stones=importlib.util.module_from_spec(kspec);kspec.loader.exec_module(weighted_stones);weighted_stones.install(ed,quest_guides.DUNGEON_ACCESS_GUIDES['weighted-stones'])
bspec=importlib.util.spec_from_file_location('job_balance',C/'english/job_balance.py');job_balance=importlib.util.module_from_spec(bspec);bspec.loader.exec_module(job_balance);job_balance.install(ed)
imspec=importlib.util.spec_from_file_location('illustrations',C/'english/illustrations.py');illustrations=importlib.util.module_from_spec(imspec);imspec.loader.exec_module(illustrations);illustrations.install(ed)
zspec=importlib.util.spec_from_file_location('world_zones',C/'english/zones.py');world_zones=importlib.util.module_from_spec(zspec);zspec.loader.exec_module(world_zones);world_zones.install(ed)
emspec=importlib.util.spec_from_file_location('expansion_missions',C/'english/expansion_missions.py');expansion_missions=importlib.util.module_from_spec(emspec);emspec.loader.exec_module(expansion_missions);expansion_missions.install(ed)
maspec=importlib.util.spec_from_file_location('mission_access',C/'english/mission_access.py');mission_access=importlib.util.module_from_spec(maspec);maspec.loader.exec_module(mission_access);mission_access.install(ed)
erspec=importlib.util.spec_from_file_location('era_reference',C/'english/era_reference.py');era_reference=importlib.util.module_from_spec(erspec);erspec.loader.exec_module(era_reference);era_reference.install(ed)
add('all-pages','All Pages','Reference','Browse the complete English article index.')
P['all-pages']['body']='<div class="filter-bar"><label>Filter pages <input type="search" data-list-filter="all-page-list" placeholder="Quest, item, NPC or zone"></label><span data-list-count="all-page-list" role="status"></span></div>'+directory([k for k in P if k!='all-pages'],'all-page-list')
# Preserve every existing page URL and section bookmark.
assert set(old)-{'road-companion'}-set(classic_equipment.RETIRED)-set(story_retirement.RETIRED)<=set(P),set(old)-set(P)
legacy.update({'missions':'missions.html','quests':'quests.html','overview':'index.html','main':'index.html','fear-of-the-dark':'fear-of-the-dark.html'})
(C/'page-manifest.json').write_text(json.dumps({k:{a:v[a] for a in ['title','category','parent']} for k,v in P.items()},ensure_ascii=False,indent=2))
# Cross-link exact entity names once per article, without altering existing links.
entities=dict(item_aliases)
for k,p in P.items():
 if p['category'] in ['NPCs','Zones'] or k in ['honey','gysahl-greens','gausebit-wildgrass','distilled-water','warrior','thief']:
  entities[p['title']]=k
for i,title in [('16496','Poison Dagger'),('12680','Chain Mittens'),('12711','Beetle Mittens'),('13240','Warrior’s Belt +1'),('13524','Balance Ring')]:
 if i in itemmap:entities[title]=itemmap[i]
pattern=re.compile(r'(?<![\w’])('+ '|'.join(re.escape(x) for x in sorted(entities,key=len,reverse=True))+r')(?![\w’])')
def crosslink(root,k):
 seen=set();blocked={'a','h1','h2','h3','h4','script','style','code','button','label'}
 for node in list(root.iter()):
  for attr in ['text','tail']:
   parent=node if attr=='text' else node.getparent()
   val=getattr(node,attr)
   if parent is None or not val or any(a.tag in blocked or 'era-reference' in a.get('class','') for a in [parent,*parent.iterancestors()]):continue
   matches=[]
   for m in pattern.finditer(val):
    if k.startswith(('mission-bastok-','mission-windurst-')) and entities[m.group()].startswith('key-item-'):continue
    if entities[m.group()]!=k and m.group() not in seen:
     matches.append(m);seen.add(m.group())
   if not matches:continue
   setattr(node,attr,val[:matches[0].start()]);offset=0 if attr=='text' else parent.index(node)+1
   for n,m in enumerate(matches):
    a=html.Element('a',href=entities[m.group()]+'.html');a.text=m.group();end=matches[n+1].start() if n+1<len(matches) else len(val);a.tail=val[m.end():end];parent.insert(offset,a);offset+=1
 return root
def linked_fragment(value,k):return contents(crosslink(html.fragment_fromstring(value,create_parent='div'),k))
def prepare(k,p):
 root=html.fragment_fromstring(p['body'],create_parent='div')
 if not p.get('era_import'):root=crosslink(root,k)
 # Heading IDs and article contents.
 used=set();toc=[]
 for h in root.xpath('.//h2'):
  if any('portal' in a.get('class','') for a in h.iterancestors()):continue
  ident=h.get('id') or slug(h.text_content());base=ident;n=2
  while ident in used:ident=base+'-'+str(n);n+=1
  used.add(ident);h.set('id',ident);toc.append((ident,h.text_content()))
 for nav in root.xpath('.//nav[@data-zone-contents]'):
  heading=html.Element('h3');heading.text='Table of Contents';nav.append(heading)
  links=html.Element('ul')
  for ident,title in toc:
   li=html.Element('li');a=html.Element('a',href='#'+ident);a.text=title;li.append(a);links.append(li)
  nav.append(links)
 return contents(root),toc
nav=[('Navigation',[('index','Main Page'),('getting-started','Getting Started'),('all-pages','All Pages'),('update-log','Recent Updates')]),('Game Guide',[('quests','Quests'),('missions','Missions'),('jobs','Jobs'),('trusts','Trusts'),('exp-camps','EXP Camps'),('travel','Travel'),('mounts','Chocobo Rentals')]),('Reference',[('era-reference','Level 75 Reference'),('items','Items'),('zones','Zones'),('npcs','NPCs'),('monsters','Monsters'),('spells','Spells'),('abilities','Abilities & Weapon Skills'),('records-of-eminence','RoE & Sparks'),('auction-house','Auction House'),('crafting','Crafting'),('launcher','Launcher')]),('About',[('server-rules','Server Rules'),('roadmap','Roadmap'),('sources','Sources')])]
crystal='<svg viewBox="0 0 40 64" aria-hidden="true"><path d="M20 1 36 24 31 48 20 63 8 48 4 24Z" fill="#235fa1"/><path d="M20 1 17 31 4 24Z" fill="#96d5fa"/><path d="M20 1 36 24 17 31Z" fill="#4ca6e5"/><path d="m17 31 14 17 5-24Z" fill="#c2e8fc"/><path d="M17 31 8 48 4 24Z" fill="#377fc0"/><path d="m17 31 3 32 11-15Z" fill="#4fa8e4"/></svg>'
icon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath fill='%232461a2' d='M16 1 27 12 23 25 16 31 8 25 5 12Z'/%3E%3C/svg%3E"
index=[]
for k,p in P.items():
 body,toc=prepare(k,p);parent=p['parent'];parentlink=link(parent) if parent in P else link('index','Main Page')
 aside=''.join('<section><h2>'+label+'</h2>'+''.join('<a href="'+url+'.html"'+(' aria-current="page"' if url==k else '')+'>'+title+'</a>' for url,title in links)+'</section>' for label,links in nav)
 box=''
 if p['facts'] or p.get('portraitHtml'):
  photo=p.get('portraitHtml') or ('<img class="npc-portrait" src="assets/apururu-web.webp" alt="Apururu" width="200" height="224">' if k in ['healers-promise','apururu'] else '')
  name_label='Mission Name' if p['category']=='Missions' else 'Quest Name' if p['category']=='Quests' else 'Name'
  facts=[(name_label,escape(p['title']))]+p['facts']
  box='<section class="page-summary" aria-label="Quick reference">'+photo+'<table class="summary-table"><tbody>'+''.join('<tr><th scope="row">'+t+'</th><td>'+linked_fragment(v,k)+'</td></tr>' for t,v in facts)+'</tbody></table></section>'
 toc_html='<nav class="toc" aria-label="Article contents"><strong>Contents</strong><ol>'+''.join('<li><a href="#'+escape(ident,quote=True)+'">'+escape(title)+'</a></li>' for ident,title in toc)+'</ol></nav>' if len(toc)>=3 and k not in ['index','all-pages','items'] else ''
 if p.get('layout') in ('zone','area-category'):toc_html=''
 overview='<div class="article-overview">'+box+toc_html+'</div>' if box or toc_html else ''
 status='<div class="status-note"><strong>Status:</strong> '+p['status']+' <a href="update-log.html">Details</a></div>' if p['status'] else ''
 lead_html='<p class="lead">'+p['intro']+'</p>' if p['intro'] and p.get('layout')!='zone' else ''
 desc=escape(text(p['intro']),quote=True)
 document=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(p['title'])} - Zenith XI Wiki</title><meta name="description" content="{desc}"><link rel="icon" href="{icon}"><link rel="stylesheet" href="assets/wiki.css?v=13"><script defer src="assets/search-index.js?v=15"></script><script defer src="assets/wiki.js?v=13"></script></head><body data-page="{k}"><a class="skip" href="#content">Skip to content</a><header class="topbar"><a class="small-brand" href="index.html">ZENITH XI <span>WIKI</span></a><button class="mobile-nav" aria-expanded="false" aria-controls="wiki-nav" type="button">Menu</button><div class="search"><label class="sr-only" for="wiki-search">Search Zenith XI Wiki</label><input id="wiki-search" type="search" placeholder="Search Zenith XI Wiki" autocomplete="off" aria-controls="search-results"><div id="search-results" class="search-results" hidden></div></div><a class="top-link" href="all-pages.html">All pages</a></header><div class="layout"><aside class="sidebar" id="wiki-nav"><a class="brand" href="index.html">{crystal}<strong>ZENITH XI</strong><span>THE ADVENTURER’S WIKI</span></a><nav aria-label="Wiki navigation">{aside}</nav></aside><main id="content"><div class="page-tabs"><span class="selected">{escape(p['category'])}</span><a href="all-pages.html">Article index</a><button class="print-link" type="button" data-print>Print</button></div><article class="article"><div class="breadcrumb">{parentlink} <span>›</span> {escape(p['title'])}</div><h1>{escape(p['title'])}</h1><div class="wiki-byline">From Zenith XI Wiki</div>{lead_html}{overview}{status}<div class="article-body">{body}</div><div class="category-footer"><strong>Category:</strong> {escape(p['category'])}<span> · </span>{parentlink}</div></article><footer class="footer"><p>Zenith XI Wiki · English edition · Updated 26 September 2026</p><p><a href="sources.html">Sources</a> · <a href="update-log.html">Implementation status</a> · <a href="roadmap.html">Roadmap</a><br>FINAL FANTASY XI and original game artwork © SQUARE ENIX.</p></footer></main></div><noscript><p class="no-js">Search and filters need JavaScript. All articles remain available through the <a href="all-pages.html">page index</a>.</p></noscript></body></html>'''
 document=re.sub(r'(assets/(?:wiki\.css|wiki\.js|search-index\.js)\?v=)\d+',r'\g<1>42',document)
 (D/(k+'.html')).write_text(document)
 index.append({'name':p['title'],'url':k+'.html','category':p['category'],'note':text(p['intro'])[:160],'keys':text(p['body'])[:600]})
(D/'road-companion.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=mounts.html"><title>Chocobo Rentals</title></head><body><a href="mounts.html">Chocobo Rentals</a></body></html>')
legacy['road-companion']='mounts.html'
for k in ['index','honey','healers-promise']:
 (D/'preview'/f'{k}.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../{k}.html"><title>{P[k]["title"]}</title><script>location.replace("../{k}.html"+location.hash)</script></head><body><a href="../{k}.html">Open {P[k]["title"]}</a></body></html>')
(D/'assets/search-index.js').write_text('window.ZENITH_ARTICLES='+json.dumps(index,ensure_ascii=False,separators=(',',':'))+';\nwindow.ZENITH_LEGACY='+json.dumps(legacy)+';\n')
print(f'Built {len(P)} English pages; {len(camps)} camps; {len(marketrows)} catalogue items. All {len(old)} previous page URLs preserved.')

for retired in classic_equipment.RETIRED+story_retirement.RETIRED:
 (D/(retired+'.html')).write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=equipment-quests.html"><title>Original equipment quests</title></head><body><a href="equipment-quests.html">Original equipment quests</a></body></html>')

# Keep previously published qualified titles after consolidating their content.
for alias,target in {
 'aht-urhgan-mission-16-ghosts-of-the-past':'mission-toau-16',
 'aht-urhgan-mission-45-ragnarok':'mission-toau-45',
 'crest-of-davoi-key-item':'key-item-crest-of-davoi',
 'full-moon-fountain-mission':'mission-windurst-6-1',
 'jeuno-mission':'mission-bastok-3-3',
}.items():
 (D/(alias+'.html')).write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+target+'.html"><title>'+escape(P[target]['title'])+'</title></head><body><a href="'+target+'.html">'+escape(P[target]['title'])+'</a></body></html>')

# Compact production output while preserving full source articles and image dimensions.
import subprocess,sys
subprocess.run([sys.executable,str(R/"tools/compact-site.py")],check=True)
subprocess.run([sys.executable,str(R/"tools/finalize-site.py")],check=True)
