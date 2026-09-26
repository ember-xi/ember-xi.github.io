"""Import acquisition references from the pinned server snapshot, without executing SQL."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, csv, hashlib, json, math, re
import yaml

def load_yaml(s):return yaml.load(s,Loader=yaml.CSafeLoader)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/item-data'
parser=argparse.ArgumentParser()
parser.add_argument('source',type=Path)
args=parser.parse_args()
SRC=args.source
REF='f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4'
def sqlrows(name):
    text=(SRC/'sql'/f'{name}.sql').read_text();variables={}
    def number(s):
        s=re.sub(r'@(\w+)',lambda m:str(variables[m[1]]),s)
        if not re.fullmatch(r'[0-9a-fA-FxX()|&+\-~ \t]+',s):raise ValueError(s)
        return eval(s,{'__builtins__':{}},{})
    for line in text.splitlines():
        m=re.match(r'SET @(\w+)\s*=\s*([^;]+);',line)
        if m:
            try:variables[m[1]]=number(m[2])
            except (ValueError,KeyError):pass
        m=re.match(r'INSERT INTO `?'+name+r'`? VALUES \((.*)\);',line)
        if m:
            cells=next(csv.reader([m[1]],quotechar="'",escapechar='\\',skipinitialspace=True))
            row=[]
            for cell in cells:
                if cell=='NULL':row.append(None)
                elif cell.startswith('@') or re.fullmatch(r'-?\d+',cell):row.append(number(cell))
                elif re.fullmatch(r'-?\d+\.\d+',cell):row.append(float(cell))
                else:row.append(cell)
            yield row

basic={r[0]:r for r in sqlrows('item_basic')}
names={r[2]:i for i,r in basic.items()}
equipment={r[0]:r[2] for r in sqlrows('item_equipment')}
enum={k:int(v) for k,v in re.findall(r'^\s*(\w+)\s*=\s*(\d+),',(SRC/'scripts/enum/item.lua').read_text(),re.M)}
zones={r[0]:str(r[3]) for r in sqlrows('zone_settings')}
zoneids={v.lower():k for k,v in zones.items()}
orig=json.loads((OUT/'map-origins.json').read_text())
trans=json.loads((OUT/'map-transforms.json').read_text())
market=json.loads((OUT/'market.json').read_text())
catalog={r['itemid']:r for r in market['items']}
categories={int(i):path.replace('->',' → ').replace('&',' & ') for i,path in re.findall(r'SET @\w+\s*=\s*(\d+);\s*-- ([^\n]+)',(SRC/'sql/item_basic.sql').read_text()) if int(i)<=65}
categories.update({0:'Not sold at the Auction House',1:'Weapons → Hand-to-Hand',4:'Weapons → Great Swords',6:'Weapons → Great Axes',10:'Weapons → Great Katana',13:'Weapons → Ranged',14:'Weapons → Instruments',34:'Furnishings',59:'Food → Ingredients'})
def label(name):
    name=name.replace('_',' ')
    return name.replace('San dOria','San d’Oria').replace('RuLude','Ru’Lude').replace('dOraguille','d’Oraguille').replace('Crawlers Nest','Crawlers’ Nest')
def grid(zone,point):
    if not point or len(point)<3 or point[:3] in ([0,0,0],[1,1,1],[1,0,0]):return None
    x,y,z=point[:3];which=''
    if str(zone) in orig and zone not in (195,197):
        ox,oz,size=orig[str(zone)];col=math.floor((x-ox)/size);row=math.floor((oz-z)/size)+1
    elif str(zone) in trans:
        matches=[m for m in trans[str(zone)] if any(b['x1']<=x<=b['x2'] and b['y1']<=z<=b['y2'] and b['z1']<=y<=b['z2'] for b in m['boxes'])]
        if len(matches)!=1:return None
        m=matches[0];col=math.floor((x*m['mult']+m['xoff']-16)/32);row=math.floor((-z*m['mult']+m['yoff']-16)/32)+1
        if len(trans[str(zone)])>1:which=' · map '+str(m['id']+1)
    else:return None
    return chr(65+col)+'-'+str(row)+which if 0<=col<15 and 1<=row<=15 else None

# Custom quest materials and rewards which are outside the market catalogue.
extra={13495,13496,13497,26167,enum['CLUMP_OF_GAUSEBIT_WILDGRASS']}
# National-story materials and access items, including optional repeat routes.
extra.update({181,494,495,548,549,597,599,605,891,1112,1137,4377,4528,12298,16535,16656})
# Resolve names found in current quest rewards by native short names and existing labels.
quest_names=['Greataxe','Chain Mittens',"Warrior\'s Belt +1",'Poison Dagger','Beetle Mittens','Balance Ring','Breastplate','Brigandine','Beetle Earring +1','Silver Hairpin','Puissance Ring','Alacrity Ring','Wisdom Ring','Solace Ring','Ruby Ring','Emerald Ring','Diamond Ring','Sapphire Ring','Beeswax','Cotton Cloth','Insect Wing','Iron Ore','Iron Ingot','Silk Thread','Gausebit Wildgrass','Exoray Mold','Bomb Coal','Ancient Papyrus','Dragon Chronicles','Meat Jerky','Apple Pie','Potion','Ether','Mandragora Lantern','Rabbit Hide','Flint Stone','Bat Wing','Honey','Distilled Water','Gysahl Greens']
def normal(s):return re.sub(r'[^a-z0-9+]','',s.lower().replace('’',"'"))
for wanted in quest_names:
    matches=[i for i,r in basic.items() if normal(r[2])==normal(wanted) or normal(r[3])==normal(wanted)]
    if matches:extra.add(min(matches))
selected=set(catalog)|extra
recipes=defaultdict(list)
crafts=['Woodworking','Smithing','Goldsmithing','Clothcraft','Leathercraft','Bonecraft','Alchemy','Cooking']
rawrecipes=list(sqlrows('synth_recipes'))
for r in rawrecipes:
    if len(r)>30 and r[30] in {'ABYSSEA','SOA','ROV','TVR'}:continue
    for i in set(r[21:25]):
        if not i:continue
        recipes[i].append({'id':r[0],'desynth':bool(r[1]),'key_item':r[2],'craft':[[crafts[k],n] for k,n in enumerate(r[3:11]) if n], 'crystal':r[11],'ingredients':[[i,n] for i,n in Counter(x for x in r[13:21] if x).items()], 'results':[[r[j],r[j+4]] for j in range(21,25)],'tag':r[30] if len(r)>30 else None})
# Include one level of ingredients as usable reference pages; do not invent recipes for them.
for i in list(selected):
    for r in recipes[i]:selected.update(x for x,n in r['ingredients']);selected.add(r['crystal'])
selected.discard(0);selected.intersection_update(basic)
items={i:{'id':i,'name':catalog[i]['label'] if i in catalog else label(basic[i][2]).title(), 'native_name':basic[i][2], 'level':equipment.get(i), 'flags':basic[i][7], 'stack':basic[i][6], 'category':categories.get(basic[i][8],'Not sold at the Auction House') if not basic[i][7]&64 else 'Not sold at the Auction House', 'category_id':basic[i][8] if not basic[i][7]&64 else 0, 'recipes':recipes[i], 'drops':[], 'vendors':[]} for i in sorted(selected)}
for wanted in quest_names:
    for i in items:
        if normal(basic[i][2])==normal(wanted) or normal(basic[i][3])==normal(wanted):items[i]['name']=wanted
for i,name in {13495:'San d’Orian Ring',13496:'Windurstian Ring',13497:'Bastokan Ring',534:'Gausebit Wildgrass',181:'San d’Orian Flag',494:'Quadav Augury Shell',495:'Quadav Charm',548:'Tenshodo Invite',549:'Delkfutt Key',597:'Mine Gravel',599:'Mythril Sand',605:'Pickaxe',1112:'Orcish Mail Scales',1137:'Prelate Key',4377:'Coeurl Meat',4528:'Crystal Bass',12298:'Parana Shield',16656:'Orcish Axe'}.items():
    items[i]['name']=name
for r in items.values():r['recipes'].sort(key=lambda s:(s['desynth'],bool(s['key_item']),max((lv for _,lv in s['craft']),default=0),s['id']))

drop_records=defaultdict(dict)
def add_drop(i,zone,name,level,cells,kind='Drop'):
    if i not in items:return
    key=(zone,name,kind)
    entry=drop_records[i].setdefault(key,{'monster':name,'zone':label(zones[zone]),'zone_id':zone,'level':level[:],'grids':set(),'method':kind})
    entry['level']=[min(entry['level'][0],level[0]),max(entry['level'][1],level[1])]
    entry['grids'].update(cells)

classic=set(range(100,255))|{1,2,3,4,5,6,7,8,9,10,11,12,13,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39}
for folder in sorted((SRC/'data/zones').iterdir()):
    zone=zoneids.get(folder.name)
    if zone not in classic or not (folder/'mobs.yaml').exists():continue
    d=load_yaml((folder/'mobs.yaml').read_text()) or {}
    regions=load_yaml((folder/'regions.yaml').read_text()).get('regions',{}) if (folder/'regions.yaml').exists() else {}
    templates=d.get('templates',{})
    for spawn in d.get('spawns',{}).values():
        t=templates.get(spawn.get('template'),{});lv=spawn.get('level',[0,0])
        if not isinstance(lv,list):lv=[lv,lv]
        if not lv[0] or lv[0]>75:continue
        name=label(t.get('display_name',spawn.get('script',spawn.get('template','Monster'))))
        region_names=spawn.get('region',[])
        if isinstance(region_names,str):region_names=[region_names]
        points=[spawn['at']] if spawn.get('at') else [p for rn in region_names for p in regions.get(rn,{}).get('poly',[])]
        cells={g for p in points if (g:=grid(zone,p))}
        loot=spawn.get('loot',t.get('loot',{}))
        for drop in loot.get('drops',[]):
            if drop.get('chance') in (0,'never'):continue
            entries=[drop] if 'item' in drop else drop.get('one_of',[])
            if isinstance(entries,dict):entries=[{'item':x} for x in entries]
            for e in entries:
                if isinstance(e,dict):add_drop(names.get(e.get('item')),zone,name,lv,cells)
        steal=loot.get('steal')
        if isinstance(steal,str):add_drop(names.get(steal),zone,name,lv,cells,'Steal')

# The remaining non-migrated zones use SQL groups and spawn tables.
dropids=defaultdict(list)
for r in sqlrows('mob_droplist'):
    if r[4] in items and r[5]:dropids[r[0]].append(r[4])
groups={(r[2],r[0]):r for r in sqlrows('mob_groups')}
for r in sqlrows('mob_spawn_points'):
    zone=(r[0]>>12)&0xFFF;g=groups.get((zone,r[4]))
    if zone not in classic or not g or not 0<r[5]<=75:continue
    cell=grid(zone,r[7:10]);cells={cell} if cell else set()
    for i in dropids[g[6]]:add_drop(i,zone,r[3] or label(r[2]),r[5:7],cells)
for i,rows in drop_records.items():
    for r in rows.values():r['grids']=sorted(r['grids'],key=lambda s:(s[0],int(re.search(r'\d+',s)[0])))
    items[i]['drops']=sorted(rows.values(),key=lambda r:(not bool(r['grids']),r['level'][0],r['zone'],r['monster']))

# Only literal, named general-shop stock. Conditional availability is retained as a note.
npc_positions={}
for folder in (SRC/'data/zones').iterdir():
    zone=zoneids.get(folder.name)
    if zone not in classic or not (folder/'npcs.yaml').exists():continue
    for npc in (load_yaml((folder/'npcs.yaml').read_text()) or {}).get('npcs',{}).values():
        if npc.get('script') and npc.get('at'):
            npc_positions[(zone,npc['script'])]=grid(zone,npc['at'])
for f in (SRC/'scripts/zones').glob('*/npcs/*.lua'):
    zone=zoneids.get(f.parent.parent.name.lower())
    if zone not in classic:continue
    s=f.read_text()
    if 'xi.shop.general(player, stock' not in s:continue
    stock=re.search(r'local stock\s*=\s*\{([\s\S]*?)\n\s*\}',s)
    if not stock:continue
    for token,price in re.findall(r'\{\s*(xi\.item\.\w+|\d+)\s*,\s*(\d+)\s*\}',stock[1]):
        i=enum.get(token.split('.')[-1]) if token.startswith('xi.item.') else int(token)
        if i in items:
            cell=npc_positions.get((zone,f.stem))
            if cell:items[i]['vendors'].append({'npc':label(f.stem),'zone':label(zones[zone]),'grid':cell,'base_price':int(price),'source':str(f.relative_to(SRC))})

key_file=SRC/'scripts/enum/key_item.lua'
key_names={int(v):label(k.lower()).title() for k,v in re.findall(r'^\s*(\w+)\s*=\s*(\d+),',key_file.read_text(),re.M)} if key_file.exists() else {}
data={'key_items':key_names,'upstream':REF,'date':'2026-09-23','scope':'Market items, quest rewards/materials and direct synthesis ingredients. Native acquisition references; custom quest rewards are documented separately.','categories':categories,'names':{i:label(str(r[2])).title() for i,r in basic.items()},'items':items}
(OUT/'sources.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
review={'upstream':REF,'items':len(items),'items_with_drops':sum(bool(x['drops']) for x in items.values()),'items_with_recipes':sum(bool(x['recipes']) for x in items.values()),'items_with_vendors':sum(bool(x['vendors']) for x in items.values()),'sha256':{str(f.relative_to(SRC)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (SRC/'sql').glob('*.sql') if f.stem in ['item_basic','synth_recipes','mob_droplist','mob_spawn_points','mob_groups','zone_settings']}}
(OUT/'review.json').write_text(json.dumps(review,indent=2))
print(json.dumps(review))
