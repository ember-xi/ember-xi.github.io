"""Complete quest guides from World Quests 3.2.0 and retained native sources.

The reward registry drives the quest index, NPC pages and quest summaries together.
Map labels describe game-map cells; roaming areas are examples, not fixed markers.
"""
import re

# Unlisted native access tasks have their own full articles. These records keep
# the quest directory, NPC and reward pages tied to the same acquisition facts.
DUNGEON_ACCESS_GUIDES = {
 'weighted-stones': {
  'key': 'garlaige-citadel-gate-access',
  'title': 'Garlaige Citadel Gate Access',
  'npc_key': 'garlaige-weighted-stones',
  'npc_name': '??? (Weighted Stones)',
  'location': 'Garlaige Citadel, Map 1 (G-8)',
  'level': 'No level requirement',
  'reward_key': 'pouch-of-weighted-stones',
  'reward': 'Pouch of Weighted Stones',
  'reward_type': 'Permanent key item',
  'cost': 'Free',
  'turn_in': 'Receive the key item at the same ???; no return trip.',
 },
}

STATUS = 'Guide matched to World Quests v3.2.0. Installation on the running server is not confirmed by the wiki.'
NPCS = {
 'zenith-armsmith': ('Zenith Armsmith', 'Northern San d’Oria (E-8)', 'Beside Home Point #1.'),
 'achantere-ring': ('Achantere, T.K.', 'Northern San d’Oria (C-8)', 'At the western gate.'),
 'rabid-wolf-ring': ('Rabid Wolf, I.M.', 'Bastok Markets (E-11)', 'At the western gate.'),
 'rakoh-buuma-ring': ('Rakoh Buuma', 'Windurst Woods (K-10)', 'At the southern gate area.'),
 'gondebaud': ('Gondebaud', 'Southern San d’Oria (L-6)', 'Trust representative.'),
 'nanaa-mihgo': ('Nanaa Mihgo', 'Windurst Woods (J-3)', 'At the Cat Burglar’s Lair; advanced THF equipment quest.'),
 'monberaux': ('Monberaux', 'Upper Jeuno (G-10)', 'Inside the infirmary.'),
 'maat': ('Maat', 'Ru’Lude Gardens (H-5)', 'Talk here for both Limit Break quests.'),
 'medicine-axe': ('Medicine Axe', 'Valkurm Dunes (H-7)', 'At the outpost.'),
 'lucretia': ('Lucretia', 'Northern San d’Oria (E-6)', 'At the Blacksmiths’ Guild.'),
 'jiwon': ('Jiwon', 'Qufim Island (F-6)', 'At the outpost shelter.'),
 'apururu': ('Apururu', 'Windurst Woods (H-9)', 'Inside the Manustery, behind the counter.'),
 'mapitoto': ('Mapitoto', 'Upper Jeuno (G-7)', 'At the chocobo stables.'),
 'brutus': ('Brutus', 'Upper Jeuno (G-7)', 'At the chocobo stables; trade grass to the Chocobo beside him.'),
 'norejaie': ('Norejaie', 'Southern San d’Oria (K-6)', 'Eco-Warrior: San d’Oria.'),
 'raifa': ('Raifa', 'Port Bastok (D-6)', 'Eco-Warrior: Bastok.'),
 'lumomo': ('Lumomo', 'Windurst Waters, north (F-10)', 'Eco-Warrior: Windurst.'),
 'matildie': ('Matildie', 'Northern San d’Oria (J-8)', 'Adventurer Coupon turn-in.'),
 'alaune': ('Alaune', 'Southern San d’Oria (G-10)', 'Tutorial training.'),
 'gulldago': ('Gulldago', 'Bastok Markets (D-11)', 'Tutorial training.'),
 'selele': ('Selele', 'Windurst Woods (K-10)', 'Tutorial training.'),
 'clarion-star': ('Clarion Star', 'Port Bastok (K-7)', 'Trust registration and Cipher exchange.'),
 'wetata': ('Wetata', 'Windurst Woods (G-10)', 'Trust registration and Cipher exchange.'),
 'excenmille': ('Excenmille', 'Northern San d’Oria (D-9)', 'San d’Oria’s first companion.'),
 'naji': ('Naji', 'Metalworks (J-8)', 'Bastok’s first companion.'),
 'rolandienne': ('Rolandienne', 'Southern San d’Oria (G-10)', 'Records of Eminence and Sparks.'),
 'isakoth': ('Isakoth', 'Bastok Markets (E-11)', 'Records of Eminence and Sparks.'),
 'fhelm-jobeizat': ('Fhelm Jobeizat', 'Windurst Woods (J-10)', 'Records of Eminence and Sparks.'),
 'wije-tiren': ('Wije Tiren', 'Windurst Woods (I-8)', 'Distilled Water vendor.'),
 'mejuone': ('Mejuone', 'Upper Jeuno (G-7)', 'Gysahl Greens vendor at the stables.'),
 'secodiand': ('Secodiand', 'Northern San d’Oria (E-6)', 'Fear of the Dark.'),
}
# key, title, level, owner, reward, summary, group
QUESTS = [
 ('an-edge-earned','An Edge Earned','WAR 15+','zenith-armsmith','1 Greataxe — Accuracy +2, Attack +2 augments','Defeat 6 Hill Lizards with a Great Axe in Main.','WAR equipment'),
 ('hands-that-guard','Hands That Guard','WAR 25+','zenith-armsmith','1 Chain Mittens — Accuracy +2, Attack +2 augments','Record both Scout reports and defeat 6 Clippers.','WAR equipment'),
 ('stand-your-ground','Stand Your Ground','WAR 35+','zenith-armsmith','1 Warrior’s Belt +1 — STR +2, Accuracy +2 augments','Win your own Breakwater Crab fight.','WAR equipment'),
 ('hold-the-line','Hold the Line','WAR 40+','zenith-armsmith','1 Breastplate — Accuracy +2, Attack +2 augments','Win your own Ironhide Beetle fight.','WAR equipment'),
 ('a-pair-of-quiet-blades','A Pair of Quiet Blades','THF 20+','zenith-armsmith','2 Poison Daggers — each has Accuracy +2, Attack +1 augments','Defeat 6 Sand Hares with a Dagger in Main.','THF equipment'),
 ('eyes-on-the-road','Eyes on the Road','THF 25+','zenith-armsmith','1 Beetle Mittens — DEX +1, Accuracy +2 augments','Record both Scout reports and defeat 6 Land Worms.','THF equipment'),
 ('a-clean-recovery','A Clean Recovery','THF 35+','zenith-armsmith','1 Balance Ring — AGI +1, Accuracy +2 augments; native DEX +2 remains','Win your own Breakwater Crab fight.','THF equipment'),
 ('a-shadows-safeguard','A Shadow’s Safeguard','THF 45+','zenith-armsmith','1 Brigandine — Accuracy +2, AGI +1 augments','Win your own Cache Guardian fight.','THF equipment'),
 ('a-shadow-reforged','A Shadow Reforged','THF 70+','nanaa-mihgo','1 Thief’s Knife — Accuracy +3, DEX +2 augments; native Treasure Hunter +1 remains','Trade 2 Silk Threads + 1 Mythril Ingot; win your Sozu Rogberry quest fight.','THF equipment'),
 ('three-nations-one-journey','Three Nations, One Journey','Rank 10 in all three nations','achantere-ring','Choose 1: Kingdom Aketon, Republic Aketon OR Federation Aketon — HP +30, MP +30, Accuracy +5 augments','Complete all three national mission lines; existing Rank 10 records count.','National mission reward'),
 ('promise-san-doria','A Promise to San d’Oria','10+','achantere-ring','1 San d’Orian Ring — DEF +2, STR +2, MND +2, Accuracy +2 total','Defeat 3 Orcish Fodder in West Ronfaure.','Rings'),
 ('promise-bastok','A Promise to Bastok','10+','rabid-wolf-ring','1 Bastokan Ring — HP +15, DEX +2, VIT +2 total','Defeat 3 Young Quadav in North Gustaberg.','Rings'),
 ('promise-windurst','A Promise to Windurst','10+','rakoh-buuma-ring','1 Windurstian Ring — MP +15, AGI +2, INT +2 total','Defeat 3 Yagudo Initiates in East Sarutabaruta.','Rings'),
 ('silent-steps','Silent Steps','1+','achantere-ring','1 Sneak Ring — Sneak + Invisible for 8 minutes; reuse every 10 minutes','Trade 2 Beeswax + 1 Cotton Cloth together to any city ring guard.','Rings'),
 ('companions-of-the-road','Companions of the Road','30+','gondebaud','Permanent allowance of 4 Trusts','Visit Qufim and Eastern Altepa; earn 10 eligible kills with a living Trust.','Trusts'),
 ('an-adventurer-leads','An Adventurer Leads','50+','gondebaud','Permanent allowance of 5 Trusts','Visit Crawlers’ Nest and Western Altepa; earn 15 eligible kills with a living Trust.','Trusts'),
 ('healers-promise','A Healer’s Promise','30+','apururu','Permanent Trust spell: Apururu (UC)','Trade 3 Honey + 3 Distilled Water together after accepting.','Trusts'),
 ('a-rhythm-worth-following','A Rhythm Worth Following','40+','gondebaud','Permanent Trust spell: Uka Totlihn','Win your own Wayward Weapon fight in Qufim.','Trusts'),
 ('a-doctors-promise','A Doctor’s Promise','60+','monberaux','Permanent Trust spell: Monberaux','Win your own Cratebreaker fight in Batallia Downs.','Trusts'),
 ('coastal-dispatch','Coastal Dispatch','20+; final fight ~30','medicine-axe','4,000 gil + choose 1: Beetle Earring +1 OR Silver Hairpin','Deliver supplies, scout the route and defeat Valkurm Emperor.','Equipment side quests'),
 ('sandbound-repairs','Sandbound Repairs','35+; final fight ~47','lucretia','6,000 gil + choose 1: Puissance Ring, Alacrity Ring, Wisdom Ring OR Solace Ring','Commission repairs with 2 Iron Ingots, investigate the shipment, report to Lucretia, then defeat Dune Widow.','Equipment side quests'),
 ('the-broken-watch','The Broken Watch','60+; final fight ~72','jiwon','10,000 gil + choose 1: Ruby Ring, Emerald Ring, Diamond Ring OR Sapphire Ring','Restore the outpost, deliver 3 Silk Threads, inspect the lower Boyahda Tree, then defeat Aquarius.','Equipment side quests'),
 ('first-limit-break','First Limit Break','50; limit still 50','maat','Level limit 55; Horizon Breaker title','Collect 1 Exoray Mold, 1 Bomb Coal and 1 Ancient Papyrus; trade all three together.','Limit Break'),
 ('limit-break','Final Limit Break','70','maat','Level limit 75 across all jobs','Win your job’s final solo trial; no Testimony required.','Limit Break'),
 ('eco-warrior','Eco-Warrior','Battle cap 25','norejaie','10,000 gil base + 1 Dragon Chronicles + 1 saved EXP bonus','Choose one nation; complete its dungeon encounter and return with the key item.','Weekly quest'),
 ('adventurer-coupon','Adventurer Coupon','New character','matildie','3,000 gil; 12 Meat Jerky OR 12 Apple Pies by job; 5 Potions; 5 Ethers; 1 Mandragora Lantern','Trade 1 Adventurer Cpn.; prepare 12 free inventory slots.','Travel and starting quests'),
 ('chocobos-wounds','Chocobo’s Wounds','20+','brutus','Chocobo License key item; Chocobo Trainer title','Complete six feeding attempts; four consume 1 Gausebit Wildgrass each.','Travel and starting quests'),
 ('road-companion','A Companion for the Road','20+','mapitoto','Trainer’s Whistle + Chocobo Companion key items; personal chocobo','Trade 1 Gysahl Greens, examine Upper Jeuno Home Points 1 → 3 → 2, then return.','Travel and starting quests'),
 ('fear-of-the-dark','Fear of the Dark','Original quest','secodiand','200 gil base + San d’Oria fame','Trade 2 Bat Wings together. Repeatable.','Travel and starting quests'),
]

def install(ed):
    P,add,link,para,section,table,steps,listing=ed.P,ed.add,ed.link,ed.para,ed.section,ed.table,ed.steps,ed.listing
    registry={q[0]:q for q in QUESTS}
    def location(owner):
        n,z,landmark=NPCS[owner]
        return link(owner,n)+' · '+z+'. '+landmark
    def summary(q):
        k,title,level,owner,reward,goal,group=q
        contacts=['achantere-ring','rabid-wolf-ring','rakoh-buuma-ring'] if k in ('silent-steps','three-nations-one-journey') else ['norejaie','raifa','lumomo'] if k=='eco-warrior' else [owner]
        return [('Start NPC','<br>'.join(location(n) for n in contacts)),('Required level',level),('Objective',goal),('Reward',reward)]
    def questtable(qs):
        rows=[]
        for q in qs:
            contacts=['achantere-ring','rabid-wolf-ring','rakoh-buuma-ring'] if q[0] in ('silent-steps','three-nations-one-journey') else ['norejaie','raifa','lumomo'] if q[0]=='eco-warrior' else [q[3]]
            npc='<br><br>'.join(link(n,NPCS[n][0])+'<br>'+NPCS[n][1] for n in contacts)
            rows.append((npc,link(q[0],q[1])+'<br>'+q[2],q[4]))
        return table(['NPC','Quest','Reward'],rows)

    # Update all retained references before generating shared summaries.
    changes={
      'Gondebaud → Claim reward':'Claim reward',
      'Use Zenith Adventures for the current connected stories':'Visit the individual quest givers for current equipment side quests',
      'Equipment quests, Trust slots and Crystal Paths; near Home Point #1':'WAR and THF equipment quests; Home Point #1 (E-8)',
      'Moogle quest acceptance, progress records and rewards are handled by Zenith Armsmith.':'Each quest has its own NPC; see the quest directory for names, map squares and rewards.',
      'The Qufim Scout provides its report and the encounter when your active chapter requires it.':'The Qufim Scout records reports. Quest battles begin at ??? in Qufim Island (F-6).',
      'Zenith uses a saved Armsmith activation':'Zenith uses saved activation at Norejaie, Raifa or Lumomo',
      'NM marker and reward guide':'Quest battle locations',
      'href="nm-challenges.html"':'href="quest-encounters.html"',
      'Three Roads is a prepared series that is not installed yet.':'Each quest now has its own NPC; check the quest directory for the reward you want.',
      'for the custom Moogle quest menu':'for WAR / THF equipment quests at Home Point #1 (E-8)',
      'Select the current equipment chapter and open the chapter.':'Open your next equipment chapter.',
    }
    for key,p in P.items():
        if key in ('sources','update-log'):continue
        for field in ('body','intro'):
            for a,b in changes.items():p[field]=p[field].replace(a,b)
        if p.get('status','') and any(x in p['status'] for x in ['World Quests v3.0.2','Progression v2.1.0']):p['status']=STATUS

    # Equipment chapters: explicit field targets and marker placement on every page.
    fields={
      'an-edge-earned':('Hill Lizards','Valkurm Dunes (D-6)/(D-7)','a Great Axe'),
      'a-pair-of-quiet-blades':('Sand Hares','Valkurm Dunes (I-7)/(J-7)','a Dagger'),
      'hands-that-guard':('Clippers','Qufim Island (G-7)/(H-7)',None),
      'eyes-on-the-road':('Land Worms','Qufim Island (H-7)/(H-8)',None),
    }
    previous={'hands-that-guard':'an-edge-earned','stand-your-ground':'hands-that-guard','hold-the-line':'stand-your-ground','eyes-on-the-road':'a-pair-of-quiet-blades','a-clean-recovery':'eyes-on-the-road','a-shadows-safeguard':'a-clean-recovery'}
    bosses={'stand-your-ground':('Breakwater Crab','37'),'a-clean-recovery':('Breakwater Crab','37'),'hold-the-line':('Ironhide Beetle','at least 42; scales with your level'),'a-shadows-safeguard':('Cache Guardian','at least 47; scales with your level')}
    for q in QUESTS[:8]:
        k,t,lv,owner,reward,goal,g=q
        route=[]
        if k in previous:route.append('Finish '+link(previous[k],registry[previous[k]][1])+' and collect its entire reward first.')
        route.append('Speak to '+location(owner)+' Use '+lv+' as your main job. The next chapter appears automatically; choose Accept quest.')
        if k in fields:
            enemy,area,weapon=fields[k]
            if not weapon:route+=['Talk to Zenith Scout at the Valkurm Dunes outpost (H-7), beside the books, to record the first report.','Talk to Zenith Scout at the Qufim Island outpost (F-6) to record the second report.']
            route.append('Defeat 6 '+enemy+' in '+area+'.'+(' Keep '+weapon+' equipped in Main.' if weapon else ' There is no weapon requirement; reports and kills can be done in either order.'))
            route.append('These are roaming monster areas. Other qualifying '+enemy+' in the same zone count too. Stay alive, within 50 yalms and on '+lv+'. Kills before acceptance do not count.')
        else:
            boss,bosslv=bosses[k]
            route+=['Go to the Qufim Island outpost (F-6). Summon your Trusts, then examine ??? and select '+boss+'.','Win your own fight within 10 minutes. Boss level: '+bosslv+'. Stay alive, on the job you started with, and within 50 yalms for credit.']
        route.append('Return to Zenith Armsmith in Northern San d’Oria (E-8), Home Point #1. Choose Claim reward. Free '+('two inventory slots' if k=='a-pair-of-quiet-blades' else 'one inventory slot')+' before collecting.')
        add(k,t,'Quests',goal,section('Walkthrough',steps(*route))+section('Reward',para(reward+'. Once per character. Augments are added to the item’s native properties.'))+section('If your bag is full',para('The undelivered reward remains saved. Make space and choose Claim reward again; do not restart the task.'))+para(link('zenith-scout','Scout maps')+' · '+link('quest-encounters','Quest ??? locations')),parent='warrior-quests' if g.startswith('WAR') else 'thief-quests',status=STATUS)

    # Individual ring quests, plus the new reusable travel ring.
    ringtargets=[('Orcish Fodder','West Ronfaure (G-7)/(H-7)'),('Young Quadav','North Gustaberg (G-8)/(H-8)'),('Yagudo Initiates','East Sarutabaruta (H-9)/(H-10)')]
    for q,(enemy,area) in zip([registry[k] for k in ('promise-san-doria','promise-bastok','promise-windurst')],ringtargets):
        k,t,lv,owner,reward,goal,g=q
        add(k,t,'Quests',goal,section('Walkthrough',steps('At main level 10+, speak to '+location(owner)+' Choose this city’s ring quest, then Accept quest. Any home nation may accept it.','Defeat 3 '+enemy+' in '+area+' after accepting. Stay alive and within 50 yalms, on a level-10+ main job.','Return to '+location(owner)+' Choose Claim reward with one free inventory slot.'))+section('Reward',para(reward+'. Once per character.'))+para('The three city quests are independent. An existing copy of the Rare ring prevents a duplicate reward. The city visit is recorded when you accept here.'),parent='city-rings',status=STATUS)
    q=registry['silent-steps']
    add('silent-steps','Silent Steps','Quests','Earn a reusable Sneak Ring for quiet travel.',
        section('Walkthrough',steps('Speak to any one of the three city ring guards listed above. Choose Silent Steps, then Accept quest.','Obtain 2 Beeswax and 1 Cotton Cloth. Bought, crafted or farmed materials all work. '+link('market-catalog','Check the Auction House catalogue')+' for listings; stock is not guaranteed.','Keep one free main-inventory slot. Trade exactly 2 Beeswax + 1 Cotton Cloth together to any of those guards, with no gil or extra items.','Receive 1 Sneak Ring immediately. This is one shared quest, with one ring per character; changing city does not grant another.'))+
        section('Reward',para(q[4]+'. Level 1, all jobs, either ring slot; reusable.'))+
        section('Use the ring',steps('Equip Sneak Ring in either ring slot and wait 5 seconds.','Open Items and use the equipped ring. Activation takes 1 second. Equipping it alone does not activate it.','Sneak and Invisible last up to 8 minutes. The next use is available 10 minutes after activation. Normal cancellation and detection rules still apply.'))+
        section('Already have a Sneak Ring?',para('Your existing ring receives the same server effects; no repeat quest is required. If you already own one, the guard keeps your materials and does not issue a duplicate.'))+
        section('Item description',para('The native item name is Sneak Ring. Its static description may still list only Sneak and the old 15-minute reuse; Zenith applies both effects and the 10-minute reuse on the server. This guide describes v3.1.1.')),parent='city-rings',status=STATUS)
    add('sneak-ring','Sneak Ring','Items','Zenith’s reusable Sneak + Invisible ring.',section('How to get it',para(link('silent-steps','Complete Silent Steps')+': trade 2 Beeswax + 1 Cotton Cloth after accepting at a city ring guard.'))+section('Effects',table(['Property','Value'],[('Duration','8 minutes: Sneak + Invisible'),('Reuse','10 minutes from activation'),('Equip / activation delay','5 seconds / 1 second'),('Jobs / level','All jobs / level 1'),('Use','Equip, then use through Items; not automatic on equip.')])),parent='items',status=STATUS)

    for key,title,owner,level,boss,area,time in [
        ('a-rhythm-worth-following','A Rhythm Worth Following','gondebaud',40,'Wayward Weapon','Qufim Island outpost (F-6)',10),
        ('a-doctors-promise','A Doctor’s Promise','monberaux',60,'Cratebreaker','Batallia Downs (H-6), sapling field',15)]:
        reward=registry[key][4]
        add(key,title,'Quests','Earn '+reward.replace('Permanent Trust spell: ','')+' as a permanent companion.',
            section('Requirements',para('Main level '+str(level)+'+ and a Trust permit from any starting city.'))+
            section('Walkthrough',steps('Speak to '+location(owner)+(' Finish his original introduction if it is offered first.' if owner=='monberaux' else '')+' Accept '+title+'.','Go to '+area+'. Summon your Trusts before examining ???. Choose '+('Begin challenge' if owner=='monberaux' else boss)+'.','Defeat '+boss+' within '+str(time)+' minutes. It scales with your level, minimum '+str(level+2)+'. Stay alive, within 50 yalms and on the same main job used to start the fight.','Return to '+location(owner)+' Collect your Trust reward.'))+
            section('Reward',para(reward+'. Learned directly, once per character. After acquisition, the companion can be used on your other jobs under normal Trust rules.'))+
            section('Retry',para('Losing does not erase acceptance. Return to the same ??? once the previous encounter clears and try again.')),parent='unlock-trusts',status=STATUS)

    # Retained original training and travel quests also need actionable locations.
    cities=table(['City','Zenith Guide / Atlas location'],[
        ('Southern San d’Oria','(G-10), near Alaune and Home Point #1'),
        ('Bastok Markets','(D-11), beside Gulldago'),
        ('Windurst Woods','(K-10), beside Selele')])
    P['zenith-guide']['body']=section('Locations',cities)+section('Travel',steps('Speak to Zenith Guide at a location above.','Choose Present crystals or Past crystals, then an unlocked destination.','Choose Travel. '+link('gate-crystals','Crystal requirements and travel fees')+' apply.'))+para(link('quests','Quest NPCs and rewards')+' are handled by the specialists listed in the directory.')
    P['zenith-guide']['facts']=[('Purpose','Crystal travel')]
    P['zenith-atlas']['body']=section('Starting-city books',cities)+section('Field books',para('Valkurm Dunes: outpost (H-7). Qufim Island: outpost (F-6). For other camps, '+link('exp-camps','open the camp guide')+' to see its book’s game-map square and route.'))+section('Use the Atlas',steps('Choose Recommended for my level or Browse levels 10–75.','Read the camp’s targets and required level before travelling.','Examine the original Field Manual or Grounds Tome at the destination to activate training. Atlas does not select the page for you.'))
    P['zenith-atlas']['facts']=[('Purpose','EXP camp routes and travel')]
    P['gate-crystals']['body']+=section('Where to find Zenith Guide',cities)
    P['tutorial-quests']['body']=section('Start and return',table(['Nation','Tutorial NPC','Game-map location'],[('San d’Oria',link('alaune','Alaune'),'Southern San d’Oria (G-10)'),('Bastok',link('gulldago','Gulldago'),'Bastok Markets (D-11)'),('Windurst',link('selele','Selele'),'Windurst Woods (K-10)')]))+para('Follow one city’s training in order. Speak to that same NPC after each requested task to receive the reward listed below.')+P['tutorial-quests']['body']
    P['tutorial-quests']['body']=P['tutorial-quests']['body'].replace('<td>Northern San d’Oria</td>','<td>Northern San d’Oria (E-8)</td>').replace('<td>West Ronfaure</td>','<td>West Ronfaure (G-9)</td>').replace('<td>Bastok Mines</td>','<td>Bastok Mines (I-9)</td>').replace('<td>North Gustaberg</td>','<td>North Gustaberg (D-10)</td>').replace('<td>Port Windurst</td>','<td>Port Windurst (B-5)</td>').replace('<td>West Sarutabaruta</td>','<td>West Sarutabaruta (H-6)</td>')
    P['road-companion']['body']=P['road-companion']['body'].replace('Upper Jeuno Home Point #1 near','Upper Jeuno Home Point #1 (F-5) near').replace('Upper Jeuno Home Point #3 near','Upper Jeuno Home Point #3 (G-9) near').replace('Upper Jeuno Home Point #2 toward','Upper Jeuno Home Point #2 (I-11) toward')
    P['road-companion']['body']+=section('Gysahl Greens vendor',para(location('mejuone')))
    P['healers-promise']['body']=P['healers-promise']['body'].replace('Wije Tiren in Windurst Woods sells','Wije Tiren in Windurst Woods (I-8) sells')
    P['chocobos-wounds']['body']=P['chocobos-wounds']['body'].replace('Upper Jeuno chocobo stables','Upper Jeuno chocobo stables (G-7)')
    P['adventurer-coupon']['body']=P['adventurer-coupon']['body'].replace('Matildie in Northern San d’Oria or another adventurer assistant supported by the coupon package','Matildie in Northern San d’Oria (J-8)')
    P['limit-break']['body']=P['limit-break']['body'].replace('at Maat.','at Maat in Ru’Lude Gardens (H-5).')
    P['eco-warrior']['body']+=section('Dungeon helpers and fight markers',table(['Nation','Helper: apply ointment','Quest ???: fight and collect key item'],[
        ('San d’Oria','Rojaireaut — Ordelle’s Caves (G-3), entrance map','Ordelle’s Caves (G-9), lower section; defeat 1 Necroplasm, then examine again for Indigested Stalagmite.'),
        ('Bastok','Degga — Gusgen Mines (H-9), entrance map','Gusgen Mines (H-6), same map; defeat 2 Puddings, then examine again for Indigested Ore.'),
        ('Windurst','Ahko Mhalijikhari — Maze of Shakhrami (C-9), entrance-side map','Maze of Shakhrami (I-10), southern-passage map; defeat 3 Wyrmflies, then examine again for Indigested Meat.')]))
    P['eco-warrior']['body']=P['eco-warrior']['body'].replace('Activate at Your Eco-Warrior quest giver','Activate at your Eco-Warrior quest giver')

    add('a-shadow-reforged','A Shadow Reforged','Quests','Nanaa’s advanced THF equipment quest, adapted for Zenith.',
        section('Start',para('Speak to Nanaa Mihgo in Windurst Woods (J-3), at the Cat Burglar’s Lair. Use THF as your main job at level 70+. First complete '+link('a-shadows-safeguard','A Shadow’s Safeguard')+' and claim its Brigandine. Choose Accept quest.'))+
        section('Walkthrough',steps(
            'Trade 2 Silk Threads and 1 Mythril Ingot together to Nanaa. Existing materials count; crafting them yourself is optional.',
            'Travel to Temple of Uggalepih, Map 3 (G-8). The native ??? is in the small room behind the secret door. Nearby enemies can aggro; prepare your Trusts first.',
            'Examine ??? and choose Begin quest fight. This accepted quest does not require a Flickering Lantern. Defeat Sozu Rogberry, level 65–66, within 15 minutes.',
            'Be alive, on THF, in the same zone and within 50 yalms when your own quest-spawned Sozu dies. Another player’s pop does not complete your quest. A loss keeps the materials step complete; retry once the previous fight and corpse clear.',
            'Return to Nanaa (J-3). Choose Claim reward if you have no Thief’s Knife. If you already own one, including its normal drop from Sozu, unequip it and trade that knife alone to Nanaa for the upgrade.'))+
        section('Materials',table(['Material','Quantity','Acquisition'],[
            (link('item-816-spool-of-silk-thread','Silk Thread'),'2','Crawler drops or synthesis; Auction House → Materials → Clothcraft. Open the item for monsters, map squares and recipes.'),
            (link('item-653-mythril-ingot','Mythril Ingot'),'1','Synthesis or Auction House → Materials → Goldsmithing. Open the item for recipes and reference prices.')]))+
        section('Reward',para('One '+link('zenith-thiefs-knife','Thief’s Knife')+' with Accuracy +3 and DEX +2 augments. The native Treasure Hunter +1 remains; the quest does not add another Treasure Hunter bonus. Equipment level 70, THF only.'))+
        section('Saved rewards',para('One reward per character. A full inventory keeps the claim waiting. An existing knife is never deleted automatically; the exact knife you trade is upgraded without being consumed. A knife with different existing augments is refused so those augments are not overwritten. Original Nanaa interactions remain under Other business, and normal Flickering Lantern trades still work at the Temple marker.')),
        parent='quests',status=STATUS)
    add('three-nations-one-journey','Three Nations, One Journey','Quests','An optional reward for finishing all three national mission lines.',
        section('Start NPC',table(['NPC','Game-map location'],[(link(k,NPCS[k][0]),NPCS[k][1])for k in ('achantere-ring','rabid-wolf-ring','rakoh-buuma-ring')]))+
        section('Walkthrough',steps(
            'Reach Rank 10 in at least one nation. Three Nations, One Journey then appears at the city ring guards. Accept it at any of the three.',
            'Complete the San d’Oria, Bastok and Windurst national mission lines to Rank 10. Your existing ranks count, including ranks earned before this package. The quest does not reset ranks or require repeating completed missions.',
            'When all three ranks are 10, return to any of the three guards and choose one Aketon: Kingdom, Republic or Federation. No weekly Conquest reset wait and no three-Aketon material turn-in.',
            'If you already own your chosen Aketon, unequip it and trade that exact coat alone to the guard. It is upgraded in place. Your choice is saved once selected; one shared reward across all three guards.'))+
        section('Reward',para('Choose one '+link('zenith-nation-aketons','native nation Aketon')+' with HP +30, MP +30 and Accuracy +5 augments. All jobs, level 1. Native properties remain; this is not a Ducal Aketon and does not grant a new universal movement-speed effect. No extra gil reward.'))+
        section('Mission routes',para(link('missions','National mission walkthroughs'))),parent='quests',status=STATUS)
    add('zenith-thiefs-knife','Thief’s Knife: Zenith Reward','Items','An earned upgrade to the native level-70 THF knife.',
        section('Stats',table(['Property','Reward'],[('Equipment','THF Lv.70'),('Native bonus','Treasure Hunter +1'),('Additional augments','Accuracy +3; DEX +2')]))+
        section('How to obtain',para(link('a-shadow-reforged','A Shadow Reforged')+' starts at Nanaa Mihgo, Windurst Woods (J-3). The ordinary knife also drops from Sozu Rogberry, Temple of Uggalepih, Map 3 (G-8). The quest lets you upgrade that copy by trading it alone to Nanaa after your qualifying victory.'))+
        section('Auction House',para('Ordinary knife: Weapons → Daggers; check stock and Price History for the actual price. It is not in Zenith’s fixed stock-price catalogue. The quest augments are not included on ordinary market copies.')),
        parent='items',status=STATUS)
    add('zenith-nation-aketons','Nation Aketons: Zenith Reward','Items','Choose one enhanced nation coat after Rank 10 in all three nations.',
        section('Reward options',table(['Choose one','Equipment','Additional augments'],[(n,'All jobs · Lv.1','HP +30; MP +30; Accuracy +5')for n in ('Kingdom Aketon','Republic Aketon','Federation Aketon')]))+
        section('How to obtain',para(link('three-nations-one-journey','Three Nations, One Journey')+' at Achantere (Northern San d’Oria C-8), Rabid Wolf (Bastok Markets E-11) or Rakoh Buuma (Windurst Woods K-10). Existing native properties remain.'))+
        section('Auction House',para('These coats are not Auction House listings in the reviewed Zenith item data. Earn the enhanced copy from the quest. If you already own a normal copy, trade it alone after meeting the quest requirements.')),
        parent='items',status=STATUS)

    # One shared summary for every actual quest prevents reward/index drift.
    for q in QUESTS:
        p=P[q[0]]
        p['facts']=summary(q)
        p['status']=STATUS if q[0] not in ('adventurer-coupon','chocobos-wounds','road-companion','fear-of-the-dark') else p.get('status')
        if not re.search(r'<h2>Rewards?</h2>',p['body']):p['body']+=section('Reward',para(q[4]+'.'))
    for key in ['companions-of-the-road','an-adventurer-leads']:
        P[key]['body']=P[key]['body'].replace('choose Gondebaud → Claim reward','choose Claim reward')
        P[key]['body']+=section('Finding the areas',para('Use '+link('exp-camps','Zenith Atlas camp routes')+' to find the zone entrances and books. A visit means entering the zone; there is no hidden quest marker. Kills may be in any area if they meet this quest’s enemy-level and EXP conditions.'))
    revised={
        'coastal-dispatch': [
            'Accept at Medicine Axe, Valkurm Dunes outpost (H-7), level 20+. Speak to him again to receive the route assignment.',
            'Scout the Selbina entrance in Valkurm Dunes (G-9). Approach the entrance outside town while out of combat.',
            'Trade 4 Insect Wings together to Medicine Axe (H-7). Damselflies drop them; existing wings and Auction House purchases count.',
            'Examine ??? in Whitebone Sands, Valkurm Dunes (E-9), and choose Investigate.',
            'Prepare Trusts, examine the same ???, and defeat Valkurm Emperor (level 29–30).',
            'Report to Medicine Axe (H-7) and choose your reward.'],
        'sandbound-repairs': [
            'Accept at Lucretia, Northern San d’Oria Blacksmiths’ Guild (E-6), level 35+. Speak again about the shipment.',
            'Trade 2 Iron Ingots together to Lucretia. Craft them or buy them; there is no crafting-skill requirement.',
            'Examine Dune Widow’s ??? in Eastern Altepa Desert (G-8). Choose Investigate.',
            'Return to Lucretia (E-6) and report the damaged shipment. She prepares the repair.',
            'Return to the same ??? in Eastern Altepa (G-8). Summon Trusts and defeat Dune Widow (level 45–47).',
            'Report to Lucretia and choose your ring.'],
        'the-broken-watch': [
            'Accept at Jiwon, Qufim Island outpost (F-6), level 60+. Approach his shelter while out of combat to inspect the outpost.',
            'Speak to Jiwon about the damaged watch supplies.',
            'Trade 3 Silk Threads together to Jiwon. Gather, craft or buy them; existing threads count.',
            'Examine Aquarius’s ??? in The Boyahda Tree, lower map (H-9). Choose Investigate.',
            'Prepare Trusts and use the same ??? to defeat Aquarius (level 69–71).',
            'Return to Jiwon (F-6), report and choose your level-72 ring.'],
    }
    for key,tasks in revised.items():
        q=registry[key];owner=q[3]
        P[key]['body']=section('Start and finish',para(location(owner)))+section('Walkthrough',steps(*tasks))+section('Reward',para(q[4]+'. Once per character.'))
        P[key]['body']+=section('Materials and saved progress',para('Material sources: '+link('item-846-insect-wing','Insect Wing')+' · '+link('item-651-iron-ingot','Iron Ingot')+' · '+link('item-816-spool-of-silk-thread','Silk Thread')+'. Open the relevant item for monster locations, crafting recipes and Auction House details.'))
        P[key]['body']+=para('New starts use these revised objectives. If your old six-monster stage already had kills recorded, finish its remaining count; that stage is preserved. Completed stages, material deliveries and claimed rewards stay saved. A full inventory keeps the reward waiting.')

    groups=list(dict.fromkeys(q[-1] for q in QUESTS))
    intro='Choose your reward below, then open the quest for exact objectives, materials, map squares and turn-in steps.'
    index=''.join(section(g,questtable([q for q in QUESTS if q[-1]==g])) for g in groups)
    index+=section('Tutorials and original missions',listing([link('tutorial-quests','Tutorial training: food, vouchers, Warp Ring and Free Chocopasses'),link('roe-trusts','RoE: five Trust Ciphers, EXP and Sparks'),link('trust-starting-cities','First city Trusts and permits'),link('missions','National missions: rank and mission rewards')]))
    index+=section('Reading rewards',para('“Choose 1” means one item from the listed choices, plus the listed gil. Equipment augments are additional stats unless the row explicitly says total. All map locations use the game’s letter-number squares.'))
    index+=section('Travel and EXP',para(link('zenith-guide','Zenith Guide')+' handles crystal travel; '+link('zenith-atlas','Zenith Atlas')+' handles camps. '+link('zenith-scout','Zenith Scout')+' records equipment reports.'))
    add('quests','Quests','Quests',intro,index,status=STATUS)
    for key,title in [('adventurer-log','Find Your Quest NPC'),('character-progress','Character Progress'),('adventure-goals','Finding Your Next Goal')]:
        add(key,title,'Guides',intro,index,parent='quests',status=STATUS)
    for key,title,groupset in [('equipment-quests','Equipment Quests',{'WAR equipment','THF equipment'}),('warrior-quests','Warrior Equipment Quests',{'WAR equipment'}),('thief-quests','Thief Equipment Quests',{'THF equipment'}),('city-rings','Rings',{'Rings'}),('adventures','Equipment Side Quests',{'Equipment side quests'}),('trust-journeys','Trust Journeys',{'Trusts'}),('unlock-trusts','Unlock Trusts',{'Trusts'})]:
        qs=[q for q in QUESTS if q[-1] in groupset and q[0]!='a-shadow-reforged']
        if key=='trust-journeys':qs=[registry[x] for x in ['companions-of-the-road','an-adventurer-leads']]
        if key=='unlock-trusts':qs=[registry[x] for x in ['healers-promise','a-rhythm-worth-following','a-doctors-promise']]
        body=section('Quests and rewards',questtable(qs))
        if 'equipment' in key or key in ('warrior-quests','thief-quests'):
            body+=section('Start and claim',steps('Visit Zenith Armsmith in Northern San d’Oria (E-8), Home Point #1, on the required main job.','Your next chapter appears automatically. Choose Accept quest before doing its objectives.','Return to the Armsmith and choose Claim reward. Collect the complete reward before starting the next chapter.'))+para('Eight equipment chapters exist: four WAR and four THF. Progress is independent between jobs. Open a chapter above for its target areas and exact rewards. Installation on the live server is not confirmed by this wiki.')
        if key in ('equipment-quests','thief-quests'):body+=section('Advanced THF quest',questtable([registry['a-shadow-reforged']]))
        add(key,title,'Quests' if key not in ('trust-journeys','unlock-trusts') else 'Trusts',intro,body,parent='quests',status=STATUS)
    for owner,(name,place,landmark) in NPCS.items():
        qs=[q for q in QUESTS if q[3]==owner or q[0] in ('silent-steps','three-nations-one-journey') and owner in ('rabid-wolf-ring','rakoh-buuma-ring') or q[0]=='eco-warrior' and owner in ('raifa','lumomo')]
        old=P.get(owner,{}).get('body','')
        body=section('Location',para(place+'. '+landmark))
        if qs:body+=section('Quests and rewards',questtable(qs))+section('How to use this NPC',para('Open a quest above for its requirements, steps and exact turn-in. This NPC handles the quests listed here. Original services remain available through Other business where applicable.'))
        elif old:body+=old
        else:
            dest='tutorial-quests' if owner in ('alaune','gulldago','selele') else 'trust-starting-cities' if owner in ('clarion-star','wetata','excenmille','naji') else 'sparks-essentials' if owner in ('rolandienne','isakoth','fhelm-jobeizat') else 'healers-promise' if owner=='wije-tiren' else 'road-companion'
            body+=section('What to do',para(link(dest,'Service and walkthrough')))
        if owner=='zenith-armsmith':body+=section('Previously earned rewards',para('Saved, unclaimed rewards from retired activities appear only when owed. New ring, Trust, side and Limit Break quests belong to the other NPCs in '+link('quests','the quest directory')+'.'))
        if owner in ('gondebaud','clarion-star','wetata'):body+=section('Trust permits and Ciphers',para(link('trust-starting-cities','Starting-city Trust quests')+' · '+link('roe-trusts','RoE Cipher walkthrough')))
        add(owner,name,'NPCs',landmark,body,facts=[('Location',place)],parent='npcs')
    P['npcs']['body']=section('NPC locations and services',table(['NPC','Game-map location','Service'],[(link(k,n),place,landmark)for k,(n,place,landmark) in NPCS.items()]))+section('Travel and field help',listing([link('zenith-guide','Zenith Guide: travel locations'),link('zenith-atlas','Zenith Atlas: camps and city books'),link('zenith-scout','Zenith Scout: report locations')]))
    # Add a location reference wherever a named service is mentioned, including
    # missions, city pages, materials, starting guides, Sparks and Trust articles.
    for key,p in list(P.items()):
        if key in NPCS or key in ('sources','update-log','quests','adventurer-log','character-progress','adventure-goals','npcs'):continue
        if key in registry:continue  # already has an explicit start / return summary
        plain=re.sub('<[^>]+>',' ',p['body']+' '+p['intro'])
        hits=[(link(k,n),place)for k,(n,place,_) in NPCS.items() if n in plain]
        if hits:p['body']+=section('NPC map locations',table(['NPC','Game-map location'],hits))
    P['quest-encounters']['body']=section('Advanced THF encounter',para('Sozu Rogberry · '+link('a-shadow-reforged','A Shadow Reforged')+' · Temple of Uggalepih, Map 3 (G-8). Use the native ??? after the material delivery.'))+P['quest-encounters']['body']
    P['items']['body']=section('Reusable travel ring',para(link('sneak-ring','Sneak Ring')+' — '+link('silent-steps','Silent Steps walkthrough')))+P['items']['body']
    P['index']['body']=section('Quest rewards and locations',para(link('quests','Browse every quest by its exact reward')+' · '+link('silent-steps','Silent Steps: reusable Sneak + Invisible ring')))+P['index']['body']
    P['update-log']['body']=section('23 September: complete quest rewards and directions',para('Quest, NPC and progression pages now share an explicit reward registry. Quest summaries identify the start and return NPC, game-map square, requirements and exact reward. Includes Silent Steps from World Quests v3.2.0: 8-minute Sneak + Invisible, 10-minute reuse. Retired central-menu directions are removed from current guides. This website update does not install the server package.'))+P['update-log']['body']
    P['update-log']['body']=section('23 September: World Quests v3.2.0',para('Three equipment side quests now use varied field objectives. Added A Shadow Reforged at Nanaa Mihgo and Three Nations, One Journey at the city ring guards. Current walkthroughs, exact rewards and game-map directions match the downloadable package; installing the package is still required.'))+P['update-log']['body']
    P['sources']['body']=section('Design references',para('<a href="https://horizonffxi.wiki/Fill_In">Horizon: Fill In</a> and <a href="https://horizonffxi.wiki/Omni_Aketon">Horizon: Omni Aketon</a> informed the two new quests. Zenith uses its own prerequisites, rewards and steps; these pages document Zenith behavior. Native item IDs, augments and Sozu’s marker were checked against the reviewed server sources.'))+P['sources']['body']
    P['sources']['body']=section('Quest walkthrough review: World Quests v3.2.0',para('Rewards and conditions were checked against job_journeys.lua, earned_journeys.lua, trust_journey.lua, story_journeys.lua, limit_break.lua, clinic.lua, stealth_ring.lua and world_npcs.lua in the delivered package. NPC map locations use native NPC data, custom placement files and the reviewed grid transforms. Roaming monster areas use spawn-region data and are examples, not guaranteed fixed spawn points.'))+P['sources']['body']
