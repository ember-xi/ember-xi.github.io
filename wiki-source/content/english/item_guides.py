"""Item acquisition and market references in the shared wiki page template."""
from pathlib import Path
from html import escape
from collections import Counter
import json,re,unicodedata

def slug(t):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()).strip('-')
def install(ed,itemmap,quest_registry):
    P,add,link,para,section,table=ed.P,ed.add,ed.link,ed.para,ed.section,ed.table
    root=Path(__file__).parents[1]/'item-data'
    data=json.loads((root/'sources.json').read_text())
    assert not any(s.get('tag') in {'ABYSSEA','SOA','ROV','TVR'} for item in data['items'].values() for s in item['recipes']), 'Later-era recipe in level-75 reference'
    items={int(k):v for k,v in data['items'].items()}
    market={v['itemid']:v for v in json.loads((root/'market.json').read_text())['items']}
    ref='https://github.com/LandSandBoat/server/blob/'+data['upstream']+'/'
    keys={int(i):k for i,k in itemmap.items()}
    keys[26167]='sneak-ring'
    for i,r in items.items():
        if 'gausebit' in r['native_name']:keys[i]='gausebit-wildgrass'
    for i,r in items.items():keys.setdefault(i,'item-'+str(i)+'-'+slug(r['name']))
    def ilink(i):
        name=items[i]['name'] if i in items else data.get('names',{}).get(str(i),'Item '+str(i))
        return link(keys[i],escape(name)) if i in keys else escape(name)
    def money(n):return f'{n:,} gil'
    def fold(rows,headers,label,count=10):
        result=table(headers,rows[:count])
        if len(rows)>count:result+='<details class="source-more"><summary>'+label+' ('+str(len(rows)-count)+')</summary>'+table(headers,rows[count:])+'</details>'
        return result
    def qmatches(name,reward):
        n=name.lower().replace('’',"'");r=reward.lower().replace('’',"'")
        return bool(re.search(r'(?<![a-z])'+re.escape(n)+r's?(?![a-z0-9+])',r))
    for i,r in items.items():
        key=keys[i];m=market.get(i);name=P[key]['title'] if key in P else r['name']
        # Existing item URLs and quest-specific explanations remain addressable.
        previous=P[key]['body'] if key in ('honey','distilled-water','gysahl-greens','gausebit-wildgrass','sneak-ring') and key in P else ''
        facts=[('Item ID',str(i)),('Stack size',str(r['stack'])),('Auction House',escape(r['category']))]
        if r.get('level'):facts.insert(1,('Equipment level',str(r['level'])))
        if m:facts.extend([('Buy single',money(m['sell_single'])),('Buy stack',money(m['sell_single']*r['stack']) if r['stack']>1 else 'Not stackable')])
        quest_rewards=[q for q in quest_registry if qmatches(name,q[4]) or i==26167 and q[0]=='silent-steps']
        body=''
        if quest_rewards:
            body+=section('Quest rewards',table(['Quest','Reward'],[(link(q[0],q[1]),q[4]) for q in quest_rewards]))
            if any('augment' in q[4] for q in quest_rewards):body+=para('The quest reward includes the listed augments. Ordinary Auction House copies have their normal properties.')
        if r['drops']:
            rows=[]
            for d in r['drops']:
                area=escape(d['zone'])
                if d['grids']:area+=' · '+', '.join('('+escape(g)+')' for g in d['grids'][:8])+(' · other roaming cells' if len(d['grids'])>8 else '')
                else:area+=' · map square not yet verified'
                rows.append((escape(d['monster']),area,'–'.join(map(str,d['level'])) if d['level'][0]!=d['level'][1] else str(d['level'][0]),d['method']))
            body+=section('Dropped by',fold(rows,['Monster','Zone / game map','Level','Method'],'More monster sources'))
            body+=para('Map squares show example spawn areas. Monsters can roam; drops are not guaranteed. Named monsters and event enemies can have additional spawn conditions.')
        if r['recipes']:
            rows=[]
            for s in r['recipes']:
                craft='<br>'.join(escape(c)+' '+str(lv) for c,lv in s['craft'])
                if s['key_item']:craft+='<br>Key item: '+escape(data.get('key_items',{}).get(str(s['key_item']),'Required crafting key item'))
                results=[]
                for j,(item,qty) in enumerate(s['results']):
                    if item and qty:results.append(('NQ' if j==0 else 'HQ'+str(j))+': '+str(qty)+' × '+ilink(item))
                rows.append(('Desynthesis' if s['desynth'] else 'Synthesis',craft,ilink(s['crystal']),'<br>'.join(str(qty)+' × '+ilink(item) for item,qty in s['ingredients']),'<br>'.join(results)))
            body+=section('Synthesis recipes',fold(rows,['Method','Craft / skill cap','Crystal','Ingredients','Result'],'More recipes',6))
            body+=para('Craft numbers are skill caps, not character levels. HQ results depend on synthesis quality. Required key items and subcrafts still apply.')
        if r['vendors']:
            rows=[(escape(v['npc']),escape(v['zone'])+' ('+escape(v['grid'])+')',money(v['base_price'])) for v in r['vendors']]
            body+=section('Sold by NPCs',fold(rows,['NPC','Zone / game map','Base price'],'More vendors',8))
            body+=para('The shop’s final price can change with Fame. Availability can depend on the NPC’s normal shop conditions.')
        if m:
            body+=section('Auction House',para('<strong>Category:</strong> '+escape(r['category']))+table(['Listing','Buy from Zenith stock','Automatic buyer limit'],[
                ('Single',money(m['sell_single']),money(m['buy_single'])),
                ('Stack of '+str(r['stack']),money(m['sell_single']*r['stack']) if r['stack']>1 else 'Not stackable',money(m['buy_single']*r['stack']) if r['stack']>1 else 'Not stackable')]))
            body+=para('These are the market package’s reference prices. Check the Auction House’s current stock before bidding. A higher bid spends the higher amount.')
            body+=para('When active, the market aims to keep '+str(m['single_stock'])+' single listings'+(' and '+str(m['stack_stock'])+' stacks' if m['stack_stock'] else '')+'. This is a restocking target, not a live stock count.')
        elif r['category_id'] in range(1,66):
            body+=section('Auction House',para('<strong>Category:</strong> '+escape(r['category']))+para('This item has no fixed price in Zenith’s 689-item stock catalogue. Check player listings and Price History for its actual selling price.'))
        else:body+=section('Auction House',para('This item cannot be listed at the Auction House. Use the acquisition sources above.'))
        if r['category_id'] in range(1,66):
            body+=section('Price History and stock',para('At an Auction House counter, find the item in the category above, choose Single or Stack, then open <strong>Price History</strong>. The two histories are separate. History lists up to ten completed sales, with the amount paid, date, seller and buyer.'))
            body+=para('The available quantity is shown in the Auction House listing. An empty history means there are no recorded completed sales for that item and listing type; it does not mean the item costs zero. This website does not have a live connection to your local Auction House.')+para(link('auction-house','Buying, selling and market limits'))
        if not r['drops'] and not r['recipes'] and not r['vendors'] and not quest_rewards and not m:
            body=section('How to obtain',para('An acquisition route for this item has not yet been verified for Zenith. Its Auction House category is shown below where trading is allowed.'))+body
        if previous:
            # Preserve existing custom usage instructions and map figures without duplicate price tables.
            from lxml import html
            tree=html.fragment_fromstring(previous,create_parent='div');keep=[];active=False
            for node in tree:
                if node.tag=='h2':active=node.text_content() in ['Quest use','Use the ring','Effects','Item description','Different from license food','NPC map locations','Item image','How to get it']
                if active:keep.append(html.tostring(node,encoding='unicode',with_tail=False))
            body+=''.join(keep)
        source_links=[]
        if r['recipes']:source_links.append('<a href="'+ref+'sql/synth_recipes.sql">Synthesis data</a>')
        if r['drops']:
            zone=r['drops'][0]['zone_id'];z=r['drops'][0]['zone'].replace('’','').replace(' ','_').lower()
            source_links.append('<a href="'+ref+'data/zones/">Monster and zone data</a>')
        source_links.append('<a href="'+ref+'sql/item_basic.sql">Item and Auction House category data</a>')
        body+=section('Sources',para(' · '.join(source_links))+para('Native sources match the server baseline used for Zenith’s packages. Custom rewards follow their linked quest guides.'))
        add(key,name,'Items','How to obtain '+escape(name)+', including its documented sources and Auction House information.',body,facts,parent='items')

    allkeys=list(dict.fromkeys([*keys.values(),'zenith-thiefs-knife','zenith-nation-aketons']))
    P['items']['body']=section('Find an item','<div class="filter-bar"><label>Filter item names <input type="search" data-list-filter="item-directory" placeholder="Item or material name"></label><span data-list-count="item-directory" role="status"></span></div><ul class="page-directory" id="item-directory">'+''.join('<li data-filter="'+escape(P[k]['title'].lower(),quote=True)+'">'+link(k)+'</li>' for k in sorted(allkeys,key=lambda k:P[k]['title']))+'</ul>')
    P['items']['intro']='Item sources, crafting recipes, NPC shops and Auction House categories. Open an item for its prices and directions.'
    # Category is visible with every catalogue item without altering price columns.
    P['market-catalog']['body']=P['market-catalog']['body'].replace('These fixed package prices are not a live inventory feed.','Open an item name to see its exact Auction House category, drop sources and crafting recipes. These fixed package prices are not a live inventory feed.')
    P['auction-house']['body']=section('Price History and current stock',ed.steps('Open an Auction House counter and choose the item’s category. Every item guide shows the category path.','Select Single or Stack. Check the number currently available, then choose Price History.','Read the last completed sales: amount paid, date, seller and buyer. Single and stack histories are separate; a stack price is for the full stack.','For supplied items with no completed sales yet, use the fixed buy price in the Zenith catalogue. List your own item using actual history as a reference; the automated buyer limit is a separate ceiling.'))+para('Completed purchases from Zenith stock and purchases made by its automatic buyer use the native sale history. Website catalogue prices are references; current stock and transactions are read inside the game.')+P['auction-house']['body']
    P['update-log']['body']=section('23 September: wiki tables and item acquisition',para('Shared page layout now places the information table above the walkthrough, with Contents alongside it. Quest lists use NPC, Quest and Reward. Item references include documented monster drops, synthesis recipes, NPC vendors and Auction House categories. Fixed market prices remain unchanged; native Price History and live in-game stock are explained.'))+P['update-log']['body']
    P['sources']['body']=section('Item acquisition and market references',para('Imported from the pinned LandSandBoat baseline '+data['upstream']+': item_basic.sql, synth_recipes.sql, native zone monster and NPC YAML, literal NPC shop stock, plus Auction Market v1.0’s unchanged 689-item catalogue. Zero/challenge placeholder positions are excluded. Only reviewed map transforms produce grid labels; unavailable cells are stated as unverified.'))+P['sources']['body']
    # Link rewards and materials wherever their exact names appear, including summary fields.
    aliases={}
    for i,r in items.items():
        for name in [r['name'],P[keys[i]]['title']]:
            if len(name)>=5:aliases[name]=keys[i]
    return keys,aliases
