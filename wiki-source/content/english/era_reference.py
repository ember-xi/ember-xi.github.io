"""Licensed level-75 reference, with stable local links and Zenith overlays."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlsplit, unquote, parse_qs, quote
from collections import defaultdict
import gzip, json, re, unicodedata
from lxml import html, etree

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'era-reference'
JOBS=['Warrior','Monk','White Mage','Black Mage','Red Mage','Thief','Paladin','Dark Knight','Beastmaster','Bard','Ranger','Samurai','Ninja','Dragoon','Summoner','Blue Mage','Corsair','Puppetmaster','Dancer','Scholar']
HOSTS={'edenxi.miraheze.org','horizonffxi.wiki','ffxiclopedia.fandom.com','classicffxi.fandom.com','www.bg-wiki.com','bg-wiki.com'}

def norm(s):
    s=unquote(s).replace('_',' ').replace('’',"'").replace('‘',"'")
    s=re.sub(r'\bplus\s*(\d)',r'+\1',s,flags=re.I)
    # Punctuation distinguishes real entities: ??? Gloves / Gloves, and the
    # separate Curses, Foiled...Again!? and Curses, Foiled Again! quests.
    s=re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).lower()).strip()
    return re.sub(r'\s*\+\s*','+',s)

def slug(s):
    s=re.sub(r'\bplus\s*(\d)',r'plus \1',s,flags=re.I).replace('+',' plus ')
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')

def load_records():
    for p in sorted(DATA.glob('articles-*.jsonl.gz')):
        with gzip.open(p,'rt') as f:
            for line in f:yield json.loads(line)

def source_title(url):
    if url.startswith('wiki:'):return unquote(url[5:]),''
    u=urlsplit(url)
    if u.netloc and u.hostname not in HOSTS:return None,u.fragment
    if u.path.startswith('/wiki/'):return unquote(u.path[6:]).replace('_',' '),u.fragment
    if u.path.startswith('/ffxi/'):return unquote(u.path[6:]).replace('_',' '),u.fragment
    if u.path.endswith('/index.php'):
        q=parse_qs(u.query)
        if q.get('action',['view'])[0] not in ('view','render'):return None,u.fragment
        if 'title' in q:return q['title'][0].replace('_',' '),u.fragment
    return None,u.fragment

def classify(r):
    c=' '.join(r.get('categories',[])).lower();t=r['title']
    if t in JOBS:return 'Jobs'
    if t.startswith('Category:'):return 'Categories'
    if 'key items' in c:return 'Key Items'
    if any(x in c for x in ('armor','weapons','items','food','crafting materials','ancient currency')):return 'Items'
    if 'npcs' in c:return 'NPCs'
    if any(x in c for x in ('bestiary','notorious monsters','monsters')):return 'Monsters'
    if 'quests' in c:return 'Quests'
    if 'missions' in c:return 'Missions'
    if any(x in c for x in ('areas','zones')):return 'Zones'
    if any(x in c for x in ('spells','magic','songs','ninjutsu','summoning')):return 'Spells'
    if any(x in c for x in ('job abilities','job traits','weapon skills','blood pact')):return 'Abilities'
    return 'Reference'

def inner(node):return esc(node.text or '')+''.join(html.tostring(c,encoding='unicode',with_tail=True) for c in node)

def install(ed):
    if not (DATA/'inventory.json').exists():return
    P,add,section,para,link=ed.P,ed.add,ed.section,ed.para,ed.link
    records=list(load_records()); supplements=[]
    for f in sorted((DATA/'supplements').glob('*.json')):
        supplements+=json.loads(f.read_text()).get('articles',[])
    for r in supplements:
        r['category']={'Equipment':'Items','Weapons':'Items','Armor':'Items','Materials':'Items','Job Abilities':'Abilities','Job Traits':'Abilities','Weapon Skills':'Abilities','Notorious Monsters':'Monsters','Magic':'Spells'}.get(r['category'],r['category'])
    oldkeys=set(P)
    mapping={}
    for k,p in P.items():
        n=norm(p['title'])
        if n not in mapping:mapping[n]=k
    # Navigation pages and every established URL remain canonical.
    fixed={'Category:Jobs':'jobs','Category:Items':'items','Category:Quests':'quests','Category:Missions':'missions','Category:NPCs':'npcs','Category:Areas':'zones', 'Category:Zones':'zones','Main Page':'index'}
    mapping.update({norm(t):k for t,k in fixed.items()})
    # Source titles have identities, not just spellings. These source articles
    # describe equipment, an AF quest, or a place rather than same-name missions.
    identities={
        'Ragnarok':'relic-ragnarok',
        'Ghosts of the Past':'quest-ghosts-of-the-past',
        'Jeuno':'region-jeuno',
        'Full Moon Fountain':'zone-full-moon-fountain',
        'Crest of Davoi':'crest-of-davoi-quest',
        'Aht Urhgan Mission 45: Ragnarok':'mission-toau-45',
        'Aht Urhgan Mission 16: Ghosts of the Past':'mission-toau-16',
        'Jeuno (Mission)':'mission-bastok-3-3',
        'Full Moon Fountain (Mission)':'mission-windurst-6-1',
        'Crest of Davoi (Key Item)':'key-item-crest-of-davoi',
    }
    mapping.update({norm(t):k for t,k in identities.items()})
    for t in JOBS:mapping[norm(t)]=slug(t)
    for short,title in zip(['WAR','MNK','WHM','BLM','RDM','THF','PLD','DRK','BST','BRD','RNG','SAM','NIN','DRG','SMN','BLU','COR','PUP','DNC','SCH'],JOBS):mapping[norm(short)]=slug(title)
    articlekeys={};used=set(P)|set(mapping.values())
    for r in records+supplements:
        title=r['title'];n=norm(title)
        key=mapping.get(n)
        if key is None:
            key=slug(title) or ('reference-'+str(r.get('pageid','page')))
            if key in used:key='era-'+key+'-'+str(r.get('pageid',len(used)))
            mapping[n]=key;used.add(key)
        articlekeys[title]=key
        if key not in P:add(key,title.removeprefix('Category:'),r.get('category') or classify(r),'',parent='all-pages')
    # Source categories can be referenced even when Eden has no category page.
    # Their membership is factual article metadata and can form a local directory.
    generated_categories={}
    for r in records:
        for title in r.get('categories',[]):
            title=re.sub(r' \(page does not exist\)$','',title)
            if re.search(r'Category:(?:Pages |Information Needed|Stubs|Templates|Help|Images|Blog)',title,re.I):continue
            n=norm(title)
            if n not in mapping:
                key=slug(title)
                if key in used:key='era-'+key
                mapping[n]=key;used.add(key);generated_categories[title]=key
                add(key,title.removeprefix('Category:'),'Categories','',parent='era-reference')
    for title,key in list(articlekeys.items()):
        if P[key]['category']=='Zones':mapping[norm(title+'/Maps')]=key
    for key,p in P.items():
        if p['category']=='Zones':mapping[norm(p['title']+'/Maps')]=key
    redirects=json.loads((DATA/'redirects.json').read_text())
    edges=redirects.get('redirects',redirects.get('edges',[]))
    if isinstance(edges,dict):edges=[dict(from_=a,to=b) for a,b in edges.items()]
    for _ in range(4):
        for edge in edges:
            src=edge.get('from',edge.get('from_'));dst=edge.get('to')
            if src and dst and norm(dst) in mapping:mapping[norm(src)]=mapping[norm(dst)]
    assets=json.loads((DATA/'images.json').read_text()) if (DATA/'images.json').exists() else {}
    image_matches=json.loads((DATA/'broken-image-matches.json').read_text()) if (DATA/'broken-image-matches.json').exists() else {}
    audit={'source_articles':len(records),'supplements':len(supplements),'local_titles':len(mapping),'unresolved':{},'unresolved_supplement_links':{},'excluded_source_rules':[]}
    source_anchors={}
    for r in records:
        tree=html.fromstring(r['html'])
        source_anchors[norm(r['title'])]={i for i in tree.xpath('//@id')}
    def rewrite(url, current=None, imported=False):
        if url.startswith('#'):
            fragment=unquote(url[1:])
            if imported and fragment not in source_anchors.get(norm(current or ''),set()):return '#'
            return '#era-'+quote(fragment,safe=':_-.') if imported and fragment else url
        title,fragment=source_title(url)
        if title is None:
            if url.startswith('//'):return 'https:'+url
            if url.startswith('/'):return 'https://edenxi.miraheze.org'+url
            return url
        key=mapping.get(norm(title))
        if key:
            # Source fragments point into retained source IDs, never guessed headings.
            frag=''
            decoded=unquote(fragment)
            if decoded and key not in fixed.values() and decoded in source_anchors.get(norm(title),set()):frag='#era-'+quote(decoded,safe=':_-.')
            return key+'.html'+frag
        if not title.startswith(('File:','Image:','Special:','Template:','User:','Talk:','Help:','MediaWiki:')):
            audit['unresolved'][title]=audit['unresolved'].get(title,0)+1
        if urlsplit(url).netloc:return ('https:'+url) if url.startswith('//') else url
        return 'https://edenxi.miraheze.org/wiki/'+quote(title.replace(' ','_'),safe='/:')+('#'+fragment if fragment else '')
    def clean(r):
        root=html.fragment_fromstring(r['html'],create_parent='div')
        for el in list(root.xpath('.//*[text()[contains(.,"{{{content}}}") or contains(.,"[[]]")]]')):
            if el.text_content().strip()=='[[]]':
                table=next((a for a in el.iterancestors() if a.tag=='table'),None)
                if table is not None and table.getparent() is not None:table.getparent().remove(table)
            elif el.text_content().strip()=='{{{content}}}':
                box=next((a for a in el.iterancestors() if 'NavFrame' in a.get('class','')),el)
                if box.getparent() is not None:box.getparent().remove(box)
        if r['title']=='Ebony Pole':
            for b in root.xpath('.//b'):
                if b.text and b.text.strip()=='MNK / WHM / BLM / SMN / SCH / GEO':b.text='MNK / WHM / BLM / SMN / SCH'
        # A few old source equipment tables inherited modern job eligibility.
        # Remove only explicit links to the two post-75 jobs, never ordinary words.
        for a in list(root.xpath('.//a[@href]')):
            target,_=source_title(a.get('href'))
            if target and norm(target) in {'geo','run','geomancer','rune fencer'}:
                if r['title']=='Pet':
                    p=a.getparent()
                    if p is not None and p.tag=='p':
                        markup=inner(p)
                        markup=re.sub(r'Additionally,.*?have no commands\.', '',markup,flags=re.S)
                        new=html.fragment_fromstring(markup,create_parent='p');p.getparent().replace(p,new)
                    continue
                previous=a.getprevious()
                if previous is not None:previous.tail=re.sub(r'/\s*$','',previous.tail or '')
                else:a.getparent().text=re.sub(r'/\s*$','',a.getparent().text or '')
                a.drop_tree()
        for a in root.xpath('.//a[contains(@href,"Special:Upload")]'):
            file=parse_qs(urlsplit(a.get('href')).query).get('wpDestFile',[''])[0]
            match=image_matches.get(file);asset=assets.get(match['image_url']) if match else None
            if asset and asset.get('path'):
                for child in list(a):a.remove(child)
                a.text=None;a.set('href',asset['path']);a.attrib.pop('class',None)
                width=min(300,int(match['width']));height=round(int(match['height'])*width/int(match['width']))
                a.append(html.Element('img',src=asset['path'],alt=r['title'].removeprefix('Category:'),width=str(width),height=str(height)))
                credit=html.Element('small',{'class':'source-credit'});reference=html.Element('a',href=match['source_file_url']);reference.text='Image source';credit.append(reference);a.addnext(credit)
        for bad in root.xpath('.//script|.//style|.//iframe|.//object|.//embed|.//form|.//input|.//button|.//link|.//meta|.//noscript|.//svg|.//math|.//audio|.//video|.//canvas|.//applet|.//base|.//textarea|.//select|.//comment()'):
            if bad.getparent() is not None:bad.getparent().remove(bad)
        for bad in root.xpath('.//*[@id="toc"]|.//*[contains(concat(" ",normalize-space(@class)," ")," mw-editsection ")]|.//*[contains(concat(" ",normalize-space(@class)," ")," noprint ")]'):
            if bad.getparent() is not None:bad.getparent().remove(bad)
        # Old hand-written source contents tables add clutter and often broken anchors.
        for table in list(root.xpath('.//table')):
            if not table.xpath('.//table') and 'Table of Contents:' in table.text_content() and len(table.text_content())<1000:
                if table.getparent() is not None:table.getparent().remove(table)
        for wrapper in list(root.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," mw-heading ")]')):wrapper.drop_tag()
        for image_link in root.xpath('.//a[contains(@href,"File:Check.png")]'):
            cell=image_link.getparent().getparent()
            candidates=cell.xpath('./div/a[@href]')
            if candidates and not candidates[0].text_content().strip():
                image_link.set('href',candidates[0].get('href'))
                label=candidates[0].get('title')
                if label:image_link.set('aria-label',label)
                cell.remove(candidates[0].getparent())
        seen=set()
        for el in root.iter():
            if not isinstance(el.tag,str):continue
            for attribute in list(el.attrib):
                if attribute.lower().startswith('on') or ':' in attribute or attribute.lower() in ('srcdoc','srcset','formaction'):del el.attrib[attribute]
            for attr in ('href','src'):
                val=el.get(attr,'').strip()
                if val.lower().startswith(('javascript:','vbscript:','data:')):el.attrib.pop(attr,None)
            if el.tag=='h1':el.tag='h2'
            if el.get('id'):
                ident='era-'+el.get('id')
                if ident in seen:el.attrib.pop('id',None)
                else:el.set('id',ident);seen.add(ident)
            if el.tag=='a' and el.get('href'):el.set('href',rewrite(el.get('href'),r['title'],True))
            if el.tag=='img':
                src=el.get('src','');src='https:'+src if src.startswith('//') else src
                if src.startswith('/'):src='https://edenxi.miraheze.org'+src
                if src in assets and assets[src].get('path'):el.set('src',assets[src]['path'])
                elif src:el.set('src',src)
                el.set('loading','lazy');el.set('decoding','async')
                if not el.get('alt'):el.set('alt',r['title'].removeprefix('Category:'))
            if el.tag=='table':
                el.attrib.pop('width',None)
            if el.get('style'):
                # Keep game stat colors, but remove fixed page widths and hidden content.
                style=el.get('style')
                style=';'.join(decl for decl in style.split(';') if '{{' not in decl)
                style=re.sub(r'(?:^|;)\s*(?:width|min-width|height|position|display)\s*:[^;]*','',style,flags=re.I)
                if re.search(r'url\s*\(|expression\s*\(|@import',style,re.I):style=''
                el.set('style',style)
        # Omit optional lore while retaining bookmarks used by source links.
        for heading in list(root.xpath('.//h2|.//h3|.//h4')):
            if heading.text_content().strip().lower() in {'historical background','history','etymology','lore','known relic holders','a word of warning'}:
                parent=heading.getparent()
                if parent is None:continue
                box=html.Element('span',{'class':'era-background-anchor'});index=parent.index(heading);following=[]
                if heading.get('id'):box.set('id',heading.get('id'))
                for sibling in list(parent)[index+1:]:
                    if sibling.tag in ('h2','h3','h4') or 'mw-heading' in sibling.get('class',''):break
                    following.append(sibling)
                parent.insert(index,box);parent.remove(heading)
                for sibling in following:parent.remove(sibling)
        # Item templates often show empty synthesis/desynthesis headings. Keep
        # their bookmarks but omit the empty sections from the practical guide.
        for heading in list(root.xpath('.//h2|.//h3|.//h4')):
            if heading.text_content().strip() not in {'Synthesis Recipes','Used in Recipes','Desynthesis Recipe','Obtained From Desynthesis'}:continue
            parent=heading.getparent();siblings=[]
            if parent is None:continue
            for sibling in list(parent)[parent.index(heading)+1:]:
                if sibling.tag in ('h2','h3','h4'):break
                siblings.append(sibling)
            value=' '.join(' '.join(s.text_content().split()) for s in siblings).strip().lower().strip('.')
            if value in ('','none','n/a','not applicable'):
                marker=html.Element('span')
                if heading.get('id'):marker.set('id',heading.get('id'))
                parent.replace(heading,marker)
                for sibling in siblings:parent.remove(sibling)
        # Main instructions stay fully expanded. Server-specific headings are labeled.
        for el in root.iter():
            if el.text and el.text.strip()=='Eden Custom Change:':
                el.text='Eden-specific rule (not a Zenith adjustment):'
                audit['excluded_source_rules'].append(r['title'])
        # Tables scroll within the article, never stretch the page.
        for table in list(root.xpath('.//table')):
            if table.getparent() is not None and not any(p.tag=='table' for p in table.iterancestors()):
                parent=table.getparent();wrap=html.Element('div',{'class':'table-wrap era-table'});parent.replace(table,wrap);wrap.append(table)
        return '<div class="era-reference">'+inner(root)+'</div>'
    def credit(r):
        source=r['source'];history=source+'?action=history'
        return '<p class="source-credit">Adapted from <a href="'+esc(source,quote=True)+'">Eden Wiki: '+esc(r['title'])+'</a> · <a href="'+esc(history,quote=True)+'">Contributors and history</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Revision '+str(r.get('revision') or 'unavailable')+'. Layout, links and optional background text adapted for Zenith.</p>'
    members=defaultdict(list);rendered_keys=set()
    for r in records:
        key=articlekeys[r['title']];p=P[key];base=clean(r)+credit(r)
        for c in r.get('categories',[]):
            c=re.sub(r' \(page does not exist\)$','',c)
            members[norm(c)].append(key)
        if key in rendered_keys:continue
        rendered_keys.add(key)
        if key in oldkeys:
            if p['category']=='Jobs' and r['title'] in JOBS:
                tree=html.fragment_fromstring(p['body'],create_parent='div')
                for heading in list(tree.xpath('./h2')):
                    if heading.text_content()=='Equipment journey':
                        nxt=heading.getnext();tree.remove(heading)
                        while nxt is not None and nxt.tag!='h2':after=nxt.getnext();tree.remove(nxt);nxt=after
                p['body']=section('Zenith adjustments',inner(tree))+section('Job reference',base)
                p['intro']='Abilities, skills, equipment and how to obtain them.'
            elif p['category']=='Items':
                p['body']=base+'<details class="era-existing"><summary>Zenith market and additional sources</summary>'+p['body']+'</details>'
            elif key not in ('index','jobs','items','quests','missions','npcs','zones'):
                p['body']+='<details class="era-existing"><summary>Additional level-75 reference</summary>'+base+'</details>'
        else:
            p['body']=para('<span class="reference-edition">Level 75 reference · '+link('server-rules','Zenith rules')+'</span>')+base;p['intro']='';p['era_import']=True
            p['parent']={'Jobs':'jobs','Items':'items','Quests':'quests','Missions':'missions','Zones':'zones','NPCs':'npcs','Monsters':'monsters','Spells':'spells','Abilities':'abilities','Key Items':'key-items','Categories':'era-reference'}.get(p['category'],'era-reference')
    for r in supplements:
        key=articlekeys[r['title']];body=r['body_html']
        root=html.fragment_fromstring(body,create_parent='div')
        intro=html.fragment_fromstring(r.get('intro',''),create_parent='div')
        for fragment in (root,intro):
            for a in fragment.xpath('.//a[@href]'):
                value=a.get('href');target,_=source_title(value)
                if value.startswith('wiki:') and norm(target) not in mapping:audit['unresolved_supplement_links'].setdefault(r['title'],[]).append(target)
                a.set('href',rewrite(value))
        sources=para(' · '.join('<a data-source-reference="true" href="'+esc(u,quote=True)+'">Reference '+str(i+1)+'</a>' for i,u in enumerate(r.get('source_urls',[]))))
        add(key,r['title'],r['category'],inner(intro),inner(root)+section('Sources',sources),parent='jobs' if r['category']=='Jobs' else 'era-reference')
        P[key]['era_import']=True
    # Every category is a full local directory, assembled from article metadata.
    for r in records:
        if not r['title'].startswith('Category:'):continue
        key=articlekeys[r['title']];keys=sorted(set(members[norm(r['title'])]),key=lambda k:P[k]['title'].lower())
        if keys:P[key]['body']+=section('Articles',ed.listing([link(k) for k in keys if k!=key]))
    for title,key in generated_categories.items():
        keys=sorted(set(members[norm(title)]),key=lambda k:P[k]['title'].lower())
        P[key]['body']=section('Articles',ed.listing([link(k) for k in keys if k!=key]));P[key]['era_import']=True
    def directory(category,key,title):
        keys=sorted([k for k,p in P.items() if p['category']==category and k!=key],key=lambda k:P[k]['title'].lower())
        body=section('Browse','<div class="filter-bar"><label>Find a page <input type="search" data-list-filter="'+key+'-list" placeholder="Name"></label><span data-list-count="'+key+'-list" role="status"></span></div><ul class="page-directory" id="'+key+'-list">'+''.join('<li data-filter="'+esc(P[k]['title'].lower(),quote=True)+'">'+link(k)+'</li>' for k in keys)+'</ul>')
        if key in P:P[key]['body']+=body
        else:add(key,title,category,'',body,parent='era-reference')
    for c,k,t in [('Items','items','Items'),('NPCs','npcs','NPCs'),('Quests','quests','Quests'),('Monsters','monsters','Monsters'),('Spells','spells','Spells'),('Abilities','abilities','Abilities and Weapon Skills'),('Key Items','key-items','Key Items')]:directory(c,k,t)
    hub_titles=['Category:Artifact Armor','Category:Relic Armor','Relic Weapons','Category:Weapons','Category:Weapon Skills','Category:Armor','Category:Abjurations','Category:Assault','Category:Salvage','Category:Einherjar','Category:Limbus','Dynamis','Merit Points','Category:Crafts','Category:Alchemy','Category:Bonecraft','Category:Clothcraft','Category:Cooking','Category:Fishing','Category:Goldsmithing','Category:Leathercraft','Category:Smithing','Category:Woodworking']
    hubkeys=list(dict.fromkeys(mapping[norm(t)] for t in hub_titles if norm(t) in mapping))
    add('era-reference','Level 75 Reference','Reference','Equipment, quests, enemies, crafting and endgame guides.',section('Explore',ed.listing([link(k) for k in hubkeys]))+section('Reference directories',ed.listing([link(k) for k in ('jobs','items','key-items','monsters','npcs','quests','missions','zones','spells','abilities')]))+para('Zenith-specific requirements and rewards are shown on the relevant guide. Original source-server changes are identified separately.'),parent='index')
    P['jobs']['body']=section('Job guides',ed.listing([link(mapping[norm(t)],t) for t in JOBS if mapping[norm(t)] in P]))+section('Equipment and progression',ed.listing([link(k) for k in hubkeys[:7]]))+P['jobs']['body']
    P['crafting']['body']=section('Crafts',ed.listing([link(mapping[norm(t)]) for t in hub_titles if norm(t) in mapping and any(x in t for x in ('Craft','Alchemy','Bonecraft','Clothcraft','Cooking','Fishing','Goldsmithing','Leathercraft','Smithing','Woodworking'))]))+P['crafting']['body']
    # Rewrite existing source-wiki links once after all current guides are present.
    for key,p in P.items():
        if p.get('era_import'):continue
        root=html.fragment_fromstring(p['body'],create_parent='div')
        for a in root.xpath('.//a[@href]'):
            value=a.get('href')
            if not value.startswith('wiki:') and urlsplit(value).hostname not in HOSTS:continue
            if any('source-credit' in node.get('class','') for node in [a,*a.iterancestors()]):continue
            if a.get('data-source-reference'):continue
            prior=a.xpath('preceding::h2[1]')
            if prior and any(word in prior[0].text_content().lower() for word in ('sources','references','image credits')):continue
            if re.match(r'^(?:BG Wiki|Horizon(?:XI)? Wiki|Eden Wiki|Reference \d|Image source)',a.text_content(),re.I):continue
            if value.startswith('wiki:') or urlsplit(value).hostname in HOSTS:a.set('href',rewrite(value))
        p['body']=inner(root)
    # Existing official job artwork now always opens the local job page.
    root=html.fragment_fromstring(P['jobs']['body'],create_parent='div')
    for figure in root.xpath('.//figure'):
        title=''.join(figure.xpath('.//a/span/text()')).strip()
        if norm(title) in mapping:
            for a in figure.xpath('./a'):a.set('href',mapping[norm(title)]+'.html')
    P['jobs']['body']=inner(root)
    for asset in json.loads((ROOT/'image-assets.json').read_text())['assets']:
        if asset['kind']!='job':continue
        key=mapping.get(norm(asset['title']))
        if key and key in P:
            P[key]['portraitHtml']='<figure class="reference-portrait"><img class="article-portrait" src="'+esc(asset['localPath'],quote=True)+'" alt="'+esc(asset['caption'],quote=True)+'" width="'+str(asset['width'])+'" height="'+str(asset['height'])+'" loading="lazy"><figcaption><a href="image-credits.html#'+asset['assetId']+'">Image source</a></figcaption></figure>'
    P['index']['body']=section('Explore the wiki',ed.listing([link('era-reference','Equipment, spells, enemies and endgame'),link('jobs','Job guides and Artifact / Relic equipment'),link('crafting','Crafting recipes')]))+P['index']['body']
    P['sources']['body']+=section('Level-75 reference articles',para('Eden Wiki contributors make their text available under <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0</a>. Each imported article links to its source and contributor history. These adapted articles are distributed under the same license. Game artwork and screenshots remain © SQUARE ENIX; see each image source. Administrative pages and source-server announcements are excluded.'))
    P['image-credits']['body']+=section('Additional game images',ed.table(['Image','Original file'],[(esc(a.get('sourceTitle',urlsplit(u).path.rsplit('/',1)[-1])), '<a href="'+esc(a.get('filePage') or a['articles'][0],quote=True)+'">Source and contributors</a>') for u,a in assets.items() if a.get('path')]))
    P['update-log']['body']=section('26 September 2026 — Connected level-75 reference',para('Added local job, equipment, acquisition, spell, monster, crafting and endgame reference pages with links between related articles. Existing Zenith mission walkthroughs and package notes remain. Removed later-expansion recipes from the native item reference and corrected retired equipment-quest prose.'))+P['update-log']['body']
    # Links into sections removed with source navigation/lore open the article
    # itself. Check actual retained IDs rather than trusting upstream markup.
    retained={key:set(html.fragment_fromstring(p['body'],create_parent='div').xpath('.//@id')) for key,p in P.items()}
    def retained_link(match,key):
        value=match.group(1);u=urlsplit(value)
        if u.scheme or u.netloc:return match.group(0)
        target=u.path.removesuffix('.html') if u.path else key
        if target in retained and unquote(u.fragment) not in retained[target]:return 'href="'+(u.path or '#')+'"'
        return match.group(0)
    for key,p in P.items():p['body']=re.sub(r'href="([^"\n]*#era-[^"\n]*)"',lambda m:retained_link(m,key),p['body'])
    (ROOT/'era-reference'/'build-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'era-reference'/'build-routes.json').write_text(json.dumps(articlekeys,ensure_ascii=False,indent=2)+'\n')
    ed.era_mapping=mapping
