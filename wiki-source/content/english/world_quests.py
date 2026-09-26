"""World Quests v3.0.0: matches reviewed NPC endpoints and quest ownership."""
import re

def install(ed):
    P,add,link,para,section,table,steps,listing=ed.P,ed.add,ed.link,ed.para,ed.section,ed.table,ed.steps,ed.listing
    status='World Quests v3.0.2. Package checked offline; Windows installation and in-game verification are pending.'
    scout_maps=''.join(re.findall(r'<h2>(?:Valkurm Dunes map|Qufim Island map)</h2>.*?</figure>',P['zenith-scout']['body'],flags=re.S))
    owners=[
        ('Zenith Armsmith','Northern San d’Oria','Home Point #1; (E-8)','WAR and THF equipment chapters','zenith-armsmith'),
        ('Achantere, T.K.','Northern San d’Oria','(C-8)','San d’Oria ring','achantere-ring'),
        ('Rabid Wolf, I.M.','Bastok Markets','(E-11)','Bastok ring','rabid-wolf-ring'),
        ('Rakoh Buuma','Windurst Woods','(K-10)','Windurst ring','rakoh-buuma-ring'),
        ('Gondebaud','Southern San d’Oria','(L-6)','Fourth/fifth Trust slots; Uka Totlihn','gondebaud'),
        ('Monberaux','Upper Jeuno','(G-10)','Trust: Monberaux','monberaux'),
        ('Maat','Ru’Lude Gardens','(H-5)','First Limit Break and the final trial','maat'),
        ('Medicine Axe','Valkurm Dunes','Outpost, H-7','Coastal Dispatch equipment reward','medicine-axe'),
        ('Lucretia','Northern San d’Oria','Blacksmiths’ Guild; (E-6)','Sandbound Repairs ring choice','lucretia'),
        ('Jiwon','Qufim Island','Outpost, F-6','The Broken Watch ring choice','jiwon'),
    ]
    directory=table(['NPC','Zone','Where','Purpose'],[(link(k,n),z,pos,purpose)for n,z,pos,purpose,k in owners])
    for key,p in P.items():
        if key in ('update-log','sources'):continue
        for field in ('body','intro'):
            s=p[field]
            s=s.replace('Zenith Armsmith → My Quests → Eco EXP bonus → Activate EXP bonus','Your Eco-Warrior quest giver → Activate EXP bonus')
            s=s.replace('Zenith Armsmith → Zenith Adventures → Eco-Warrior','The original Eco-Warrior quest giver')
            s=s.replace('Zenith Armsmith → Character Progress → Job Quests','Zenith Armsmith')
            s=s.replace('Character Progress → Job Quests','the current equipment chapter')
            s=s.replace('Character Progress → Trust Capacity','Gondebaud’s current capacity quest')
            s=s.replace('under Character Progress → Unlock Trusts','from their NPCs: Gondebaud for Uka; Monberaux for the doctor’s quest')
            s=s.replace('My Quests → select the chapter → Claim reward','Zenith Armsmith → Claim reward')
            s=s.replace('My Quests → select the capacity quest → Claim reward','Gondebaud → Claim reward')
            s=s.replace('My Quests, Zenith Adventures, NM Challenges and Character Progress; near Home Point #1','WAR and THF equipment quests; near Home Point #1')
            s=s.replace('Your hub for My Quests, Zenith Adventures, NM Challenges and Character Progress.','WAR and THF equipment quests. Other rewards have their own NPCs.')
            s=s.replace('Win your own Ironhide Beetle encounter at the Qufim Scout.','Win your own Ironhide Beetle fight at the Qufim outpost ???.')
            s=s.replace('Win your own Cache Guardian encounter at the Qufim Scout.','Win your own Cache Guardian fight at the Qufim outpost ???.')
            s=s.replace('Saved EXP bonuses appear in My Quests.','Activate saved EXP bonuses at Norejaie, Raifa or Lumomo.')
            p[field]=s
    for key in ('trust-journeys','companions-of-the-road','an-adventurer-leads'):
        p=P[key];p['body']=p['body'].replace('Zenith Armsmith','Gondebaud').replace('Northern San d’Oria','Southern San d’Oria').replace('near Home Point #1','at (L-6)').replace('Home Point #1','(L-6)').replace('My Quests','Gondebaud’s quest');p['status']=status
    for key in ('hold-the-line','a-shadows-safeguard','breakwater-crab'):
        p=P[key];p['body']=p['body'].replace('Qufim Scout','Qufim outpost ??? (F-6)').replace('My Quests','Zenith Armsmith').replace('Begin encounter','Begin quest fight');p['status']=status
    # The old ring stats/objectives stay; only the contacts and menu directions move.
    ringbody=P['city-rings']['body']
    ringbody=re.sub(r'<h2>.*?</h2>.*?(?=<h2>|$)', '', ringbody, count=1,flags=re.S)
    ringbody=ringbody.replace('Zenith Armsmith','the ring’s city representative').replace('My Quests','the city representative’s quest').replace('Character Progress → City Rings','the ring quest')
    add('city-rings','City Rings','Quests','Earn each city’s ring from its own representative at level 10+.',
        section('Start and return here',table(['Ring','NPC','Location'],[(['San d’Oria Ring','Bastok Ring','Windurst Ring'][i],link(owners[i+1][4],owners[i+1][0]),owners[i+1][1]+' · '+owners[i+1][2])for i in range(3)]))+
        section('Three short quests',steps('Speak to the representative of the city whose ring you want. Read the objective and choose Accept quest.',
            'San d’Oria: defeat 3 Orcish Fodder in West Ronfaure. Bastok: defeat 3 Young Quadav in North Gustaberg. Windurst: defeat 3 Yagudo Initiates in East Sarutabaruta.',
            'Return to that same representative and choose Claim reward. Existing completion and installed ring stats are preserved.'))+ringbody,parent='quests',status=status)
    intro=(section('Choose the reward you want',directory)+section('How conversations work',steps('Speak to the NPC responsible for that reward. The current objective and reward appear immediately.',
        'Choose Accept quest, complete the named task, and return to the same NPC to claim.',
        'The Armsmith shows the next equipment chapter for your current job. Gondebaud offers the next capacity quest and Uka. Original NPC services remain under Other business.'))+
        section('Travel and EXP',para(link('zenith-guide','Zenith Guide')+' handles travel. '+link('zenith-atlas','Zenith Atlas')+' handles EXP camps. '+link('zenith-scout','Zenith Scout')+' records field reports.')))
    for key,title in [('quests','Quests'),('adventurer-log','Find Your Quest NPC'),('character-progress','Character Progress')]:
        add(key,title,'Quests','Go straight to the NPC who offers the reward you want.',intro,parent=None if key=='quests' else 'quests',status=status)
    add('zenith-armsmith','Zenith Armsmith','NPCs','WAR and THF equipment quests near Northern San d’Oria Home Point #1.',
        section('Equipment',steps('Come on WAR or THF at the required level. The next unfinished chapter is shown automatically.','Read the objective and reward; choose Accept quest.','Return here to claim before starting the next chapter.'))+
        section('Your chapters',listing([link('warrior-quests','WAR: 15, 25, 35, 40'),link('thief-quests','THF: 20, 25, 35, 45')]))+
        section('Already earned older rewards',para('Only if you have a saved, unclaimed reward, an extra reward entry appears here. This does not restart retired activities.')),
        parent='npcs',status=status)
    add('equipment-quests','Equipment Quests','Quests','Eight equipment chapters: four for WAR and four for THF, with saved independent progress.',
        section('Start and claim',steps('Visit Zenith Armsmith near Northern San d’Oria Home Point #1 on the required job.','Your next chapter appears directly. Read it and choose Accept quest.','Complete the named objectives after acceptance; return to the Armsmith and choose Claim reward.'))+
        section('Chapters',listing([link('warrior-quests','WAR: 15, 25, 35 and 40'),link('thief-quests','THF: 20, 25, 35 and 45')]))+
        section('Field work',para('The Scouts record the two level-25 reports. Accepted level-35 and later trials start at the Qufim outpost ???, (F-6). Bring Trusts before examining it.'))+
        section('Rewards',para('All existing equipment, augments, counts and reward receipts are retained. A full inventory keeps the remaining reward waiting. Live installation is not yet confirmed.')),
        parent='quests',status=status)
    for key in ('first-limit-break','limit-break'):
        p=P[key]
        p['body']=p['body'].replace('At Zenith Armsmith','At Maat').replace('Zenith Armsmith','Maat').replace('the Armsmith','Maat').replace('the Armsmith’s','Maat’s')
        p['body']=p['body'].replace('Northern San d’Oria','Ru’Lude Gardens').replace('near Home Point #1','at (H-5)')
        p['body']=p['body'].replace('Character Progress → Limit Break → First Limit Break → Accept quest','Accept quest').replace('Character Progress → Limit Break → Limit Break','the current Limit Break quest')
        p['body']=p['body'].replace('My Quests → Limit Break → Unlock level 75','Unlock level 75').replace('My Quests','Maat’s quest details')
        p['body']=p['body'].replace('You do not need to visit Maat for this first quest.','Maat accepts both the first item turn-in and the final trial unlock.')
        p['intro']=p['intro'].replace('Zenith Armsmith','Maat');p['status']=status
    add('unlock-trusts','Unlock Trusts','Trusts','Earn new companions from the NPC responsible for each quest.',
        section('Uka Totlihn · level 40',steps('Speak to Gondebaud in Southern San d’Oria, (L-6). Accept A Rhythm Worth Following. A starting-city Trust permit is required.',
            'Prepare Trusts, then examine ??? at the Qufim outpost: (F-6). Choose Wayward Weapon.',
            'Win within 10 minutes, alive on the same job and within 50 yalms. The boss scales with your level, minimum 42.',
            'Return to Gondebaud to claim Trust: Uka Totlihn.'))+
        section('Monberaux · level 60',steps('Speak to Monberaux in Upper Jeuno, G-10. Finish his original introduction if necessary, then accept A Doctor’s Promise.',
            'Prepare Trusts and examine the ??? in Batallia Downs, (H-6). Defeat Cratebreaker within 15 minutes; minimum level 62, scaling with yours.',
            'Stay alive, on the same job and within 50 yalms. Return to Monberaux to receive his Trust.'))+
        para(link('trust-journeys','Capacity quests')+' also start and finish at Gondebaud. '+link('healers-promise','Apururu’s quest')+' remains with Apururu.'),parent='trusts',status=status)
    sides=[('coastal-dispatch','Coastal Dispatch','Medicine Axe','Valkurm Dunes outpost, H-7',20,30),('sandbound-repairs','Sandbound Repairs','Lucretia','Northern San d’Oria Blacksmiths’ Guild, (E-6)',35,47),('the-broken-watch','The Broken Watch','Jiwon','Qufim Island outpost, F-6',60,72)]
    for key,title,npc,place,lvl,final in sides:
        p=P[key];s=p['body']
        s=re.sub(r'<h2>Start</h2>.*?(?=<h2>|$)',section('Start and finish',para('Speak to '+npc+' at '+place+'. Accept at level '+str(lvl)+'+. The final fight is recommended around level '+str(final)+'. Return to this same NPC for the reward.')),s,flags=re.S)
        s=s.replace('Return to the Armsmith and claim your reward in My Quests.','Claim your reward from '+npc+'.').replace('Claim your reward from the Armsmith in My Quests.','Claim your reward from '+npc+'.')
        s=s.replace('Begin challenge','Begin quest fight').replace('Investigate for quest','Investigate').replace('My Quests names the next NPC, item or monster.','Your quest giver names the next NPC, item or monster.').replace('At a supporting NPC, select the story’s option;','Speak to your quest giver to report completed work;')
        s=s.replace('A six-step adventure','An equipment side quest');p['body']=s;p['intro']='An equipment side quest from '+npc+'.';p['parent']='quests';p['status']=status
    sidebody=(section('Equipment side quests',table(['Quest','NPC','Start / final fight recommendation'],[(link(k,t),n,str(l)+' / '+str(f))for k,t,n,place,l,f in sides]))+
        para('Each quest starts and finishes at its own NPC. Existing accepted steps and rewards are preserved. There is no separate Story Quests menu.'))
    add('adventures','Equipment Side Quests','Quests','Three existing equipment quests, each with its own giver.',sidebody,parent='quests',status=status)
    encounterbody=(section('Quest fights',table(['Opponent','Required quest','Marker'],[
        ('Breakwater Crab','Accepted WAR/THF level-35 chapter','Qufim outpost: (F-6)'),
        ('Wayward Weapon','A Rhythm Worth Following','Same Qufim ???'),('Ironhide Beetle','Hold the Line','Same Qufim ???'),('Cache Guardian','A Shadow’s Safeguard','Same Qufim ???'),
        ('Cratebreaker','A Doctor’s Promise','Batallia Downs: (H-6)'),
        ('Valkurm Emperor','Coastal Dispatch: defeat the NM step','Valkurm Dunes: (E-9)'),
        ('Dune Widow','Sandbound Repairs: investigate or defeat the NM step','Eastern Altepa Desert: (G-8)'),
        ('Aquarius','The Broken Watch: defeat the NM step','The Boyahda Tree: (H-9), lower map')]))+
        section('How it works',steps('Accept the quest from its own NPC and reach the required step.','Prepare your Trusts, then examine ???. It only offers a fight that your current quest needs.','A loss keeps acceptance saved. Retry once the arena is clear. Return to your quest giver for the reward.'))+
        para('Standalone NM Challenges and new first-win challenge gifts are retired. The other 21 monsters have their original spawn rules restored. Already earned, unclaimed challenge gifts remain at the Armsmith. First Limit Break uses regular monster item hunts, not these ??? markers.'))
    add('quest-encounters','Quest Encounters','Guides','An NM fight is a step toward a specific quest reward.',encounterbody,parent='quests',status=status)
    add('nm-challenges','Retired NM Challenges','Reference','Standalone challenges have been retired; accepted quests still have their required fights.',encounterbody,parent='retired-activities',status=status)
    add('adventure-goals','Finding Your Next Goal','Guides','Choose a useful reward, then visit its NPC.',directory+para('For normal equipment sources, use '+link('market-catalog','the Auction House catalogue')+'. Weapon-skill unlocks retain their original quests; no new custom weapon-skill reward is added in this package.'),parent='quests',status=status)
    retired=(section('Saved rewards',para('Old hunt, exploration and Crystal Paths activities stay retired. Already earned rewards remain as conditional entries at Zenith Armsmith. The same applies to first-win NM gifts earned before this update. No new challenge gifts are generated.'))+
        section('Preserved progression',para('Accepted equipment, ring, Trust, side-quest and Limit Break records keep their counters. The responsible NPC now handles the next step and reward. Existing equipment, learned Trusts and unlocked limits remain.')))
    for key in ('retired-activities','hunt-contracts','exploration-routes','crystal-paths'):
        add(key,P[key]['title'],'Reference','Previously earned rewards remain available.',retired,parent='quests',status=status)
    for name,zone,pos,purpose,key in owners:
        if key=='zenith-armsmith':continue
        target='city-rings' if 'ring' in key else 'trust-journeys' if key=='gondebaud' else 'unlock-trusts' if key=='monberaux' else 'limit-break' if key=='maat' else {'medicine-axe':'coastal-dispatch','lucretia':'sandbound-repairs','jiwon':'the-broken-watch'}[key]
        add(key,name,'NPCs',purpose+'.',section('Location',para(zone+' · '+pos+'.'))+section('Quest',para(link(target,'Objective, requirements and reward')))+para('Accept and collect the reward here. Other business retains the NPC’s original service where applicable.'),parent='npcs',status=status)
    add('zenith-scout','Zenith Scout','NPCs','Field reports for the level-25 WAR and THF equipment quests.',section('Report',para('Accept the equipment quest from Zenith Armsmith. Speak to each Scout on WAR or THF 25+; the required report records directly. Your enemy count is shown with its name.'))+section('Locations',table(['Zone','In-game map'],[('Valkurm Dunes outpost','H-7, beside the books; existing placement retained'),('Qufim Island outpost','(F-6)')]))+section('Trial fights',para('The Qufim quest ??? is at (F-6). '+link('quest-encounters','See the required quests and opponents')+'.')),parent='npcs',status=status)
    P['zenith-scout']['body']+=scout_maps
    for key in ('eco-warrior',):
        P[key]['body']+=section('Saved EXP bonus',para('After earning a bonus, speak to Norejaie, Raifa or Lumomo. Choose Activate EXP bonus when ready; Other business opens the original Eco-Warrior interaction. No bonus is consumed merely by opening the menu.'))
        P[key]['status']=status
    P['npcs']['body']=section('Zenith quest contacts',directory)+P['npcs']['body']
    P['getting-started']['body']=P['getting-started']['body'].replace('trade them to the Armsmith','trade them to Maat in Ru’Lude Gardens')
    P['gate-crystals']['body']=P['gate-crystals']['body'].replace('remain in My Quests','appear at Zenith Armsmith only when a saved reward is waiting')
    P['index']['body']=re.sub(r'<h2>Progression v2.1.0</h2>.*?(?=<h2>|$)','',P['index']['body'],flags=re.S)
    P['index']['body']=section('Find your quest giver',para(link('quests','NPC locations and rewards')+' · '+link('first-limit-break','First Limit Break at Maat')+' · '+link('quest-encounters','Quest ??? locations')))+P['index']['body']
    add('daily-activities','Daily Activities','Guides','Choose activities with a reward you want.',listing([link('daily-roe','Daily RoE objectives'),link('eco-warrior','Eco-Warrior weekly circuit'),link('quests','NPC quests')]))
    add('roadmap','Roadmap','Reference','World Quests v3.0.2 adds game-map locations.',section('Included',listing(['Guide for travel; Atlas for EXP camps.','Quest acceptance and rewards at specialist NPCs.','Equipment, rings, Trusts and Limit Break keep their saved records.','Quest-only ??? fights; standalone Story Quests and NM Challenges menus removed.','Original spawn rules restored for 21 former challenge NMs.']))+section('Verification',para(status))+section('Deferred',listing(['Guide addon and UI font: canceled.','More illustrated maps: deferred.','One Trust in the final trial: discussion only; current trial remains solo.','New custom weapon-skill rewards and completion fanfare: not added by this package.'])))
    P['update-log']['body']=section('22 September: World Quests v3.0.0',para('Specialist NPCs now own acceptance and rewards. Maat handles Limit Break; Gondebaud handles capacity and Uka; city representatives handle rings. Standalone challenges are retired and quest markers check the active objective. The package preserves progression and saved rewards. '+status))+P['update-log']['body']
    P['sources']['body']=section('Game-map locations',para('NPCs, quest markers and training books use map squares. The labels are derived from the installed positions and checked with <a href="https://github.com/SmithReact/VanaCompass/blob/0cc135b0148cbb1198cb456e88d1e7b324258a8f/data/grid_calibrations.lua">VanaCompass grid calibrations</a> and <a href="https://www.ffxidb.com/public/js/maps.js">FFXIDB map transforms</a>. Dungeon map geometry was reviewed for <a href="https://www.ffxidb.com/zones/153/aquarius">Boyahda</a>, <a href="https://www.ffxidb.com/zones/197/exoray">Crawlers’ Nest</a>, <a href="https://www.ffxidb.com/zones/200/explosure">Garlaige</a> and <a href="https://www.ffxidb.com/zones/195/lich">Eldieme</a>. Custom marker locations follow Zenith’s files.'))+P['sources']['body']
    P['update-log']['body']=section('22 September: map locations',para('NPC, enemy and quest-marker directions now use the game map’s letter-number squares. EXP camp book locations also use map squares, with dungeon sections identified. World Quests v3.0.2 applies the same format to game messages.'))+P['update-log']['body']
    P['sources']['body']=section('World Quests source review',para('NPC routing, objective checks and reward ownership are checked against world_npcs.lua, quest_trials.lua and the modified quest providers. Positions come from reviewed NPC data or script coordinates; map squares are checked against the game-map grid.'))+P['sources']['body']

    for key,p in P.items():
        if key in ('update-log','sources'):continue
        for field in ('body','intro'):
            p[field]=p[field].replace('Zenith Armsmith → Zenith Armsmith','Zenith Armsmith → Claim reward').replace('choose Zenith Armsmith → Claim reward','choose Claim reward').replace('select Zenith Armsmith → Claim reward','select Claim reward')
            p[field]=p[field].replace('The original Eco-Warrior quest giver shows your active quest, completed circuit nations, weekly lock and saved bonuses.','Your original quest giver handles acceptance and completion; saved bonuses appear there when available.')
            p[field]=p[field].replace('Uses the Eco-Warrior rules with the Progression v2.1.0 menu.','Uses the existing Eco-Warrior rules with NPC conversations.')
            p[field]=p[field].replace('If you already own another version of the Rare ring, the claim waits; this package does not delete it automatically. Your reward remains saved.','An existing copy of the Rare ring satisfies delivery; no second copy is created. This package does not replace the installed ring stats.')
        if key in ('trust-journeys','companions-of-the-road','an-adventurer-leads'):
            p['intro']=p['intro'].replace('Zenith Armsmith','Gondebaud')
            if p.get('facts'):p['facts']=[(a,b.replace('Zenith Armsmith','Gondebaud').replace('Northern San d’Oria · Home Point #1','Southern San d’Oria · (L-6)')) for a,b in p['facts']]
        if key in [q[2] for q in ed.EQUIPMENT]:p['status']=status
    p=P['breakwater-crab'];p['body']=p['body'].replace('Visit the Qufim Zenith Scout. Prepare yourself and your Trusts before choosing Begin quest fight.','Prepare your Trusts and examine ??? beside the Qufim outpost, (F-6). Choose Breakwater Crab.')
    p['facts']=[(a,'Quest ???' if a=='Starting NPC' else b)for a,b in p.get('facts',[])]
    for key,job,enemy in [('hands-that-guard','WAR','Clippers'),('eyes-on-the-road','THF','Land Worms')]:
        p=P[key]
        reward=re.search(r'<h2>Reward</h2>.*?(?=<h2>|$)',p['body'],flags=re.S)
        p['body']=section('Walkthrough',steps('Finish the previous equipment chapter. Speak to Zenith Armsmith on '+job+' 25+ and choose Accept quest.',
            'Speak to the Valkurm Scout beside the H-7 outpost books. The report records directly.',
            'Speak to the Qufim Scout at the outpost (F-6). The second report records directly.',
            'Defeat 6 '+enemy+' in Qufim Island after acceptance, alive and nearby on '+job+' 25+.',
            'Return to Zenith Armsmith and choose Claim reward.'))+(reward.group() if reward else '')+section('Maps',listing(['<a href="zenith-scout.html#valkurm-dunes-map">Valkurm Scout map</a>','<a href="zenith-scout.html#qufim-island-map">Qufim Scout map</a>']))
        p['status']=status
