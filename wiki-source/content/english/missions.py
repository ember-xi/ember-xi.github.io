"""National mission pages. Editorial summaries, not a live-server test."""
from html import escape
from pathlib import Path
import json
import runpy

NATIONS=[('sandoria','San d’Oria','The Kingdom of San d’Oria'),('bastok','Bastok','The Republic of Bastok'),('windurst','Windurst','The Federation of Windurst')]

def install(ed):
    P,add,link,para,section,table,steps=ed.P,ed.add,ed.link,ed.para,ed.section,ed.table,ed.steps
    records=runpy.run_path(str(Path(__file__).with_name('mission_data.py')))['RECORDS']
    maps=json.loads((Path(__file__).parents[1]/'mission-maps.json').read_text())['missions']
    def key(m):return 'smash-the-orcish-scouts' if m['nation']=='sandoria' and m['number']=='1-1' else 'mission-'+m['nation']+'-'+m['number']
    def a(k,label):return link(k,escape(label))
    def cards():
        return '<div class="nation-grid">'+''.join(f'<a class="nation-card" href="missions-{n}.html"><img src="assets/nations/{n}.jpg" width="768" height="309" alt="{escape(title)} city view"><span>{name}</span><small>20 missions · Rank 1–10</small></a>' for n,name,title in NATIONS)+'</div>'
    common=para('These are original national story missions, not Zenith Moogle side quests. Accept them from your nation’s mission guards and follow the named story NPCs. The Quest Menu does not turn in these missions.')+para('Your current nation, completed story steps and Rank Points control availability. If the next mission is missing, speak to a mission guard and raise Rank Points with crystals at a Conquest guard when required. Optional repeatable missions are included in the numbered order; you do not necessarily need every one to advance.')
    for n,name,title in NATIONS:
        missions=[m for m in records if m['nation']==n]
        for i,m in enumerate(missions):
            nav='<nav class="mission-nav" aria-label="Mission navigation">'
            nav+=a(key(missions[i-1]),'Previous: '+missions[i-1]['number']) if i else '<span>First mission</span>'
            nav+=a('missions-'+n,name+' missions')
            nav+=a(key(missions[i+1]),'Next: '+missions[i+1]['number']) if i+1<len(missions) else '<span>National story complete</span>'
            nav+='</nav>'
            body=nav+section('Before you begin',para(m['requirements']))+section('Walkthrough',steps(*[escape(s) for s in m['steps']]))
            if m.get('notes'):body+=section('Important notes',ed.listing([escape(s) for s in m['notes']]))
            if m.get('locations'):
                body+=section('Locations and references',table(['Place / NPC','Location','Reference'],[(escape(label),escape(loc),f'<a href="{escape(url,quote=True)}">Location reference</a>') for label,loc,url in m['locations']]))
            mapkey=('san-doria' if n=='sandoria' else n)+'-'+m['number']+'.html'
            if maps.get(mapkey):
                body+=section('Route maps','<div class="mission-maps">'+''.join(f'<figure><a href="assets/maps/{escape(x["filename"],quote=True)}"><img src="assets/maps/{escape(x["filename"],quote=True)}" width="512" height="512" loading="lazy" alt="{escape(x["label"])} map"></a><figcaption>{escape(x["label"])} · <a href="assets/maps/{escape(x["filename"],quote=True)}">Enlarge map</a> · <a href="{escape(x["source_page"],quote=True)}">Source</a></figcaption></figure>' for x in maps[mapkey])+'</div>')
            body+=section('Completion and reward',para(escape(m['reward'])))
            body+=section('References',para(f'<a href="{escape(m["source"],quote=True)}">HorizonXI Wiki: {escape(name)} {m["number"]}</a> · <a href="{escape(m["code"],quote=True)}">LandSandBoat mission definition</a>')+para('The route summary covers the original story. Other servers’ extra rewards, level-cap settings and Trust rules are not promises of Zenith behavior. Confirm battlefield entry conditions in game.'))+nav
            add(key(m),m['title'],'Missions',f'{name} Mission {m["number"]}.',body,[('Start NPC',escape(m.get('start',name+' mission guard'))),('Requirements',escape(m['requirements'])),('Nation / mission',a('missions-'+n,name)+' · '+m['number']),('Reward',escape(m['reward'])),('Previous Mission',a(key(missions[i-1]),missions[i-1]['title']) if i else 'First mission'),('Next Mission',a(key(missions[i+1]),missions[i+1]['title']) if i+1<len(missions) else 'National story complete')],parent='missions-'+n,status='Reference walkthrough; completion on Zenith has not been confirmed.')
        rankjump='<nav class="rank-jump" aria-label="Jump to rank">'+''.join(f'<a href="#rank-{r}">Rank {r}</a>' for r in range(1,10))+'</nav>'
        body=f'<div class="nation-header"><img src="assets/nations/{n}.jpg" width="768" height="309" alt="{escape(title)} city view"><div><p>{escape(title)}</p><p>20 missions · Complete 9-2 to reach Rank 10.</p></div></div>'+rankjump+common
        for rank in range(1,10):
            group=[m for m in missions if m['number'].startswith(str(rank)+'-')]
            body+=section('Rank '+str(rank),table(['Mission','Title','Reward'],[(m['number'],a(key(m),m['title']),escape(m['reward'])) for m in group]))
        body+=section('Other nations',cards())
        add('missions-'+n,name+' Missions','Missions','Choose a mission below for its requirements, route, important NPCs and completion steps.',body,parent='missions')
    add('missions','Missions','Missions','Choose your nation to browse its story from Rank 1 through Rank 10.',cards()+section('National mission progression',common)+section('Using these guides',para('Each mission has its own page, with numbered steps and previous / next links. Early missions and Magicite include selected route maps; other pages link to their walkthrough reference. Unverified grid coordinates are not invented.')+para('This directory covers the three present-day national stories. Expansion mission walkthroughs are outside this release.'))+section('Zenith and original missions',para('The national story stays separate from '+link('quests','Quests')+' and the custom '+link('adventurer-log','Quest Menu')+'. See '+link('server-rules','Server Rules')+' for the level-75 profile and '+link('update-log','Update Log')+' for confirmed package installation.'))+section('Image credits',para('Nation images: FINAL FANTASY XI © SQUARE ENIX, via <a href="https://www.playonline.com/ff11us/intro/world/index.html">PlayOnline</a>. Map credits remain on the originals; individual source links appear beneath each map.')))
