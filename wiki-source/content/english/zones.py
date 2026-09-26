"""Traditional area-category and zone articles, following the reference wikis."""
from pathlib import Path
from html import escape as esc
from urllib.parse import quote
from collections import defaultdict
import json, re, unicodedata

ROOT = Path(__file__).resolve().parents[1]

def norm(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower())

def slug(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', value.replace("'", '')).strip('-')

def external(url, label):
    return '<a href="' + esc(url, quote=True) + '">' + esc(str(label)) + '</a>'

def install(ed):
    zones = json.loads((ROOT / 'zone-data.json').read_text())['zones']
    native = json.loads((ROOT / 'native-zone-facts.json').read_text())
    native = {norm(k):v for k,v in native.items()}
    P, add, section, para, table = ed.P, ed.add, ed.section, ed.para, ed.table
    previous = {norm(p['title']):(k,p.copy()) for k,p in P.items() if k.startswith('zone-')}
    keys = {norm(z['name']):previous.get(norm(z['name']),('zone-'+slug(z['name']),))[0] for z in zones}
    local = {norm(p['title']):k for k,p in P.items()}; local.update(keys)
    region = lambda z:z.get('region') or z.get('group') or 'Other Areas'
    regions = {region(z):'region-'+slug(region(z)) for z in zones}
    groups = defaultdict(list)
    for z in zones:groups[region(z)].append(z)

    def link_name(name, base='https://horizonffxi.wiki/'):
        if not name or name in ('---','--','None','N/A'):return esc(name or '—')
        if norm(name) in local:return ed.link(local[norm(name)],esc(name))
        return external(base+quote(name.replace(' ','_'),safe="()'-"),name)

    def value(v):
        return ', '.join(str(x) for x in v) if isinstance(v,list) and v else str(v) if v else '—'

    def items(values,base):
        return '<br>'.join(link_name(str(x),base) for x in values) if isinstance(values,list) and values else esc(values) if isinstance(values,str) and values else '—'

    def figure(m,name,number):
        src=m.get('localPath') or m['url'];label=m.get('mapLabel') or 'Map '+str(number)
        dims=f' width="{m["width"]}" height="{m["height"]}"' if m.get('width') and m.get('height') else ''
        return '<figure class="area-map" id="map-'+str(number)+'"><div class="map-marked"><img loading="lazy" decoding="async" src="'+esc(src,quote=True)+'" alt="'+esc(name+' — '+label,quote=True)+'"'+dims+'></div><figcaption>'+esc(label)+'</figcaption><button type="button" data-enlarge-map data-map-title="'+esc(name+' — '+label,quote=True)+'">Enlarge</button></figure>'

    for z in zones:
        name=z['name'];key=keys[norm(name)];old=previous.get(norm(name),(None,{}))[1]
        source=z['sourceUrl'];source_name=z.get('sourceLabel') or 'HorizonXI Wiki'
        base='https://www.bg-wiki.com/ffxi/' if 'bg-wiki' in source else 'https://ffxiclopedia.fandom.com/wiki/' if 'ffxiclopedia' in source else 'https://horizonffxi.wiki/'
        area_type=z.get('type') or 'Area';expansion=z.get('expansion') or ''
        type_phrase={'Outdoor':'an outdoor area','Field':'an outdoor area','Dungeon':'a dungeon','City':'a city area','Battlefield':'a battlefield','Dynamis':'a Dynamis area','City, Battlefield':'a city and battlefield'}.get(area_type,'an area')
        description='<strong>'+esc(name)+'</strong> is '+type_phrase+' in '+ed.link(regions[region(z)],esc(region(z)))+'.'
        maps=[m for m in z.get('maps',[]) if m.get('localPath') or m.get('url')]
        connections=z.get('connections',[])
        native_zone=native.get(norm(name),{});native_used=False
        if not connections and native_zone.get('connections'):
            connections=native_zone['connections'];native_used=True
        exits=[]
        for c in connections:
            destination=c.get('zone') or c.get('name') or ''
            coordinates=' ('+esc(value(c['coordinates']))+')' if c.get('coordinates') else ''
            notes=' — '+esc(value(c['notes'])) if c.get('notes') else ''
            exits.append(link_name(destination,base)+coordinates+notes)
        connection_html=ed.listing(exits) if exits else para('See '+external(source,'area access information')+'.')
        facts=[('Area Name',esc(name)),('Type',esc(area_type)),('Region',ed.link(regions[region(z)],esc(region(z))))]
        if expansion:facts.append(('Expansion',esc(expansion)))
        if maps:facts.append(('Maps',' · '.join('<a href="#map-'+str(i+1)+'">'+esc(m.get('mapLabel') or 'Map '+str(i+1))+'</a>' for i,m in enumerate(maps))))
        elif z.get('noInGameMap'):facts.append(('Maps','No in-game map'))
        for label,field in [('Map Acquisition','mapAcquisition'),('Requirements','requirements'),('Restrictions','restrictions')]:
            if z.get(field):facts.append((label,esc(value(z[field]))))
        facts.extend((label,val) for label,val in old.get('facts',[]) if label=='Zone ID')
        info='<table class="zone-information"><caption>Zone Information</caption><tbody>'+''.join('<tr><th scope="row">'+label+'</th><td>'+val+'</td></tr>' for label,val in facts)+'</tbody></table>'
        map_html=figure(maps[0],name,1) if maps else para('No in-game map.' if z.get('noInGameMap') else external(source,'Map reference'))
        body='<div class="zone-infobox"><div class="zone-description"><h3>Description</h3>'+para(description)+'</div><div class="zone-navigation"><nav data-zone-contents aria-label="Article contents"></nav><h3>Connections</h3>'+connection_html+'</div><div class="zone-primary-map"><h3>Map</h3>'+map_html+'</div><aside class="zone-info">'+info+'</aside></div>'
        if z.get('mapEditorialNote'):body+=para('<span class="map-note">'+esc(z['mapEditorialNote'])+'</span>')
        quests=z.get('quests',[])
        if quests:
            rows=[(link_name(q['name'],base),esc(value(q.get('type'))),link_name(q.get('starter',''),base),link_name(q.get('zone',''),base)+(' ('+esc(value(q['coordinates']))+')' if q.get('coordinates') else '')) for q in quests if q.get('name')]
            body+=section('Involved in Quests / Missions',table(['Quest / Mission','Type','Starter','Location'],rows))
        npcs=z.get('npcs',[])
        if npcs:
            body+=section('NPCs',table(['Name','Location','Type'],[(ed.entity_image('npc',n['name'],link_name(n['name'],base)),esc(value(n.get('coordinates'))),esc(value(n.get('type') or n.get('role')))) for n in npcs if n.get('name')]))
        elif native_zone.get('npcs'):
            names=sorted({n['name'] for n in native_zone['npcs'] if n.get('name')})
            if names:
                native_used=True
                body+=section('NPCs','<ul class="page-directory">'+''.join('<li>'+(ed.link(local[norm(n)],esc(n)) if norm(n) in local else esc(n))+'</li>' for n in names)+'</ul>')
        for label,kinds in [('Notorious Monsters',{'nm','notorious'}),('Regular Monsters',{'regular'}),('Event Monsters',{'special','event'})]:
            monsters=[m for m in z.get('monsters',[]) if str(m.get('kind','regular')).lower() in kinds]
            if not monsters:continue
            rows=[]
            for m in monsters:
                notes=[str(m[f]) for f in ('spawnType','behavior') if m.get(f)]
                if m.get('horizonChange'):notes.append('Horizon-specific variant')
                monster_name=ed.entity_image('monster',m['name'],link_name(m['name'],base))
                family_name=esc(value(m.get('family')))
                if not ed.has_entity_image('monster',m['name']):family_name=ed.entity_image('family',m.get('family',''),family_name)
                rows.append((monster_name,esc(value(m.get('level'))),items(m.get('drops',[]),base),items(m.get('steal',[]),base),family_name,esc(value(m.get('spawns'))),esc('; '.join(notes)) or '—'))
            body+=section(label,table(['Name','Level','Drops','Steal','Family','Spawns','Notes'],rows))
        if len(maps)>1:
            body+=section('Maps','<div class="mission-maps area-maps">'+''.join(figure(m,name,i+1) for i,m in enumerate(maps) if i>0)+'</div>')
        if old.get('body'):
            body+=old['body']
            if old.get('status'):body+=para('<small>'+old['status']+'</small>')
        related=[]
        for pk,p in list(P.items()):
            if pk.startswith(('zone-','region-')) or pk in ('zones','all-pages','index'):continue
            if key+'.html' in p['body'] and p['category'] in ('Missions','Quests','EXP Camps','Guides','NPCs'):related.append(pk)
        if related:body+=section('See Also',ed.listing([ed.link(k) for k in sorted(set(related),key=lambda k:P[k]['title'])]))
        sources=[external(source,source_name+' — '+name)]
        if z.get('sourceRevision') and 'horizonffxi.wiki' in source:sources.append(external('https://horizonffxi.wiki/w/index.php?oldid='+str(z['sourceRevision']),'Revision used'))
        if native_used:sources.append(ed.link('sources','Zenith base-world records'))
        for note_source in z.get('mapNoteSources',[]):sources.append(external(note_source['url'],note_source['label']))
        body+=section('References',ed.listing(sources)+para('External references describe their own server or retail rules. Documented Zenith changes take precedence.'))
        if maps:
            credits=[]
            for i,m in enumerate(maps):
                credit=external(m.get('sourceUrl') or m['url'],'Map '+str(i+1)+' — '+(m.get('mapSourceLabel') or 'Source'))
                if m.get('licenseUrl'):credit+=' ('+external(m['licenseUrl'],m.get('license','License'))+')'
                credits.append(credit)
            body+='<p class="map-note">Map credits: '+ ' · '.join(credits)+'. Original game maps © SQUARE ENIX; redrawn maps retain the credited authorship and license.</p>'
        if native_used:body+=para('<small>Supplemental NPC names and exits are from the base-world snapshot; expansion conditions can affect availability.</small>')
        add(key,old.get('title') or name,'Zones',description,body,parent='zones')
        P[key]['layout']='zone'

    for name,members in sorted(groups.items()):
        body=''
        for title,types in [('Cities',{'City','City, Battlefield'}),('Outdoor Areas',{'Outdoor','Field'}),('Dungeons',{'Dungeon'}),('Battlefields',{'Battlefield','Dynamis'}),('Other Areas',set())]:
            chosen=[z for z in members if z.get('type') in types or not types and z.get('type') not in {'City','City, Battlefield','Outdoor','Field','Dungeon','Battlefield','Dynamis'}]
            if chosen:body+=section(title,ed.listing([ed.link(keys[norm(z['name'])],esc(z['name'])) for z in sorted(chosen,key=lambda z:z['name'])]))
        add(regions[name],name,'Regions','',body,parent='zones')

    continents=['The Middle Lands','The Aradjiah Continent','The Shadowreign Era','The Ulbuka Continent','Other Areas']
    category_groups={c:{} for c in continents}
    for z in zones:category_groups[z['continent']].setdefault(z['group'],[]).append(z)
    by_name={z['name']:z for z in zones}
    extra={'The Middle Lands':{'Minor Cities':['Selbina','Mhaura','Tavnazian Safehold'],'Outland Cities':['Kazham','Norg','Rabao']},'The Aradjiah Continent':{'The Empire of Aht Urhgan':['Aht Urhgan Whitegate','Al Zahbi','Nashmau']},'The Ulbuka Continent':{'The Sacred City of Adoulin':['Eastern Adoulin','Western Adoulin','Celennia Memorial Library']}}
    for c,group in extra.items():
        for name,names in group.items():category_groups[c][name]=[by_name[n] for n in names if n in by_name]
    city_order=['The Republic of Bastok',"The Kingdom of San d'Oria",'The Federation of Windurst','The Grand Duchy of Jeuno','Minor Cities','Outland Cities','The Empire of Aht Urhgan','The Sacred City of Adoulin']
    body=''
    world_path=ROOT/'world-map-assets.json'
    if world_path.exists():
        world=json.loads(world_path.read_text())
        body+=section('World Map','<div class="world-maps">'+''.join('<figure><a href="'+esc(m['localPath'],quote=True)+'"><img src="'+esc(m['localPath'],quote=True)+'" alt="'+esc(m['label'],quote=True)+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'"></a><figcaption>'+esc(m['label'])+' · '+external(m['sourceUrl'],'Source')+'</figcaption></figure>' for m in world)+'</div>')
    body+='<nav class="area-jump" aria-label="Continents">'+' · '.join('<a href="#'+slug(c)+'">'+esc(c)+'</a>' for c in continents)+'</nav>'
    for continent in continents:
        entries=[]
        ordered=sorted(category_groups[continent],key=lambda n:(0,city_order.index(n)) if n in city_order else (1,n))
        for name in ordered:
            members=category_groups[continent][name]
            region_name=name if name in regions else region(members[0]) if name in city_order[:4] else None
            heading=ed.link(regions[region_name],esc(name)) if region_name else esc(name)
            links=ed.listing([ed.link(keys[norm(z['name'])],esc(z['name'])) for z in sorted(members,key=lambda z:z['name'])])
            entries.append('<section class="area-group'+(' area-cities' if name in city_order else '')+'"><h3>'+heading+'</h3>'+links+'</section>')
        body+=section(continent,'<div class="area-groups">'+''.join(entries)+'</div>')
    intro='Vana’diel is divided into regions, with cities, outdoor areas, dungeons and battlefields.'
    add('zones','Areas','Zones',intro,body,parent='index')
    P['zones']['layout']='area-category'
    P['sources']['body']+=section('Area References',para('Area facts and maps are attributed on each article. The area-category and zone-article organization follows '+external('https://horizonffxi.wiki/Category:Areas','HorizonXI Wiki')+' and '+external('https://edenxi.miraheze.org/wiki/Category:Areas','Eden Wiki')+'. External game rules are references; documented Zenith changes take precedence.'))
    P['sources']['body']+=section('Base-world area snapshot',para('Supplemental NPCs and exits come from the native development reference used for Zenith, recorded on 24 September 2026. Only explicitly normal named NPCs were selected. Anonymous triggers, doors and effects were excluded; expansion restrictions still apply.'))
    P['update-log']['body']=section('25 September 2026 — Area pages',para('Reorganized the area category into continent and region link groups. Zone articles now use a map and Zone Information panel, followed by quest, NPC and monster tables.'))+P['update-log']['body']
