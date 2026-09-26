"""Player-facing guide checked against Zenith Progression v2.1.0 payloads."""
import json
from pathlib import Path


def install(ed):
    P, add, link, para, section, table, steps, listing = ed.P, ed.add, ed.link, ed.para, ed.section, ed.table, ed.steps, ed.listing
    status = 'Progression v2.1.0 guide. Package checked offline; installation and in-game verification are still pending.'
    hub = 'Zenith Armsmith near Home Point #1 in Northern San d’Oria'
    menu_rows = [
        ('My Quests', 'Your active objectives and waiting rewards. Ready rewards appear first.'),
        ('Zenith Adventures', 'Story quests, Eco-Warrior and World advice.'),
        ('NM Challenges', '24 named monsters: choose one, track its ??? and start the fight there.'),
        ('Character Progress', 'Job Quests, Trust Capacity, Unlock Trusts, City Rings and Limit Break.'),
        ('Leave', 'Close the conversation.')]
    add('adventurer-log', 'Quest Menu', 'Quests', 'Four clear sections at the Armsmith. Start an activity in its section; follow it and collect rewards in My Quests.',
        section('Main menu', para('Speak to '+hub+'.')+table(['Choose','What is inside'], menu_rows))+
        section('Character Progress', table(['Choose','Guide'], [
            ('Job Quests',link('equipment-quests','Four WAR chapters and four THF chapters')),
            ('Trust Capacity',link('trust-journeys','Unlock the fourth and fifth Trust slots')),
            ('Unlock Trusts',link('unlock-trusts','Uka Totlihn and Monberaux')),
            ('City Rings',link('city-rings','Three city quests and their augmented rings')),
            ('Limit Break',link('limit-break','Your route from level 50 to 75'))]))+
        section('Using My Quests', steps('Accept a quest in its category. Opening its details alone does not accept it.',
            'Open My Quests to see the exact next objective, named enemies and your count. Progress survives logout and job changes; individual quests still check their job and level requirements.',
            'When a reward is ready, open that entry in My Quests and choose its claim action or one gift. Free inventory space if needed; completed work stays saved.'))+
        para('First Limit Break uses an actual Trade of its three items to the Armsmith. Original quests and story missions keep their original NPCs; Eco-Warrior rewards come from the nation’s original quest giver.')+
        section('Finding your way back',para('Use Back to return to the previous menu. Paged lists preserve your page when you return from quest details. '+link('retired-activities','Older completed rewards')+' remain available in My Quests.')),
        parent='quests',status=status)
    add('zenith-armsmith','Zenith Armsmith','NPCs','Your quest hub near Home Point #1 in Northern San d’Oria.',
        section('Choose a section',table(['Menu','Purpose'],menu_rows))+
        section('Start here',listing([link('adventurer-log','Full menu guide'),link('adventures','Story adventures'),link('nm-challenges','NM Challenges'),link('character-progress','Character Progress')]))+
        section('Rewards',para('Use My Quests for ready Zenith rewards. For First Limit Break, trade the three requested items together. The Scout handles field reports and trial encounters; Zenith Guide handles Gate Crystal travel.')),parent='npcs',status=status)
    add('character-progress','Character Progress','Quests','Permanent character upgrades, grouped in one Armsmith menu.',
        section('Pick your next upgrade',table(['Menu','What to do','Result'],[
            ('Job Quests',link('equipment-quests','WAR: 15, 25, 35, 40 · THF: 20, 25, 35, 45'),'Augmented equipment'),
            ('Trust Capacity',link('trust-journeys','Level 30 and level 50 journeys'),'Fourth and fifth Trust slots'),
            ('Unlock Trusts',link('unlock-trusts','Uka at 40 · Monberaux at 60'),'Permanent Trust spells'),
            ('City Rings',link('city-rings','Visit each city and defeat its named enemies at level 10+'),'One augmented ring per city'),
            ('Limit Break',link('limit-break','First quest at 50; final trial at 70'),'Raise the level limit to 75')]))+
        para('Start at Zenith Armsmith → Character Progress. Accepted tasks and ready rewards appear in My Quests. Your current equipment, learned Trusts and completed quests are preserved.'),parent='quests',status=status)

    add('limit-break','Limit Break','Quests','Earn your first increase at level 50, progress automatically through the next three increases, then win your final job trial at 70.',
        section('The road to level 75',table(['At level','What to do','New limit'],[
            ('50',link('first-limit-break','Collect Exoray Mold, Bomb Coal and Ancient Papyrus; trade them to the Armsmith.'),'55'),
            ('55','The next limit opens automatically after the previous limit is unlocked.','60'),
            ('60','Automatic increase.','65'),('65','Automatic increase.','70'),
            ('70','Accept the final trial at the Armsmith, win, then collect the unlock in My Quests.','75')]))+
        section('Final trial at 70',steps('Open Character Progress → Limit Break → Limit Break at the Armsmith. Choose Accept final trial.',
            'Choose Travel to trial. No Testimony is needed; retries are free.',
            'Win your job’s original battle. It is solo, without Trusts or a support job. The original abilities and job-specific win conditions remain.',
            'Return to the Armsmith and choose My Quests → Limit Break → Unlock level 75.'))+
        section('Which opponent?',table(['Main job','Opponent'],[('WAR, MNK, WHM, BLM, RDM, THF, PLD, DRK, BST, BRD, RNG, SAM, NIN, DRG, SMN','Maat'),('BLU','Raubahn'),('COR','Qultada'),('PUP','Shamarhaan')]))+
        para('DNC, SCH, GEO and RUN do not have a supported final trial in this package. Unlocking 75 on a supported job opens the limit for your whole character.')+
        section('Existing progress',para('Already unlocked a higher limit? It stays unlocked. This update does not lower your cap or make you repeat an earned increase.')),
        parent='character-progress',status=status)
    add('first-limit-break','First Limit Break','Quests','At main level 50, collect three named items and trade them together to Zenith Armsmith to unlock level 55.',
        section('Accept the quest',para('With your level limit still at 50, speak to '+hub+'. Choose Character Progress → Limit Break → First Limit Break → Accept quest. Check your item counts in My Quests.'))+
        section('Collect one of each',table(['Item','Defeat','Zone','Enemy level'],[
            ('1 Exoray Mold','Exoray','Crawlers Nest','51–53'),('1 Bomb Coal','Explosure','Garlaige Citadel','52–53'),('1 Ancient Papyrus','Lich','The Eldieme Necropolis','51–55')]))+
        para('These are regular monsters. You do not need a ??? or an NM challenge. Trusts are allowed, and items you already own count.')+
        section('No long drop grind',para('The original drops still work. If an item has not dropped, the quest gives you that missing item directly after your third eligible kill of its monster type, once. Stay alive, in the same zone, within 50 yalms, and make sure your party receives the kill credit. Counts survive logout and job changes.'))+
        para('If your inventory is full, your earned item is saved. Free a slot and open the quest details at the Armsmith. Discarding an item received through this guarantee does not grant another guaranteed copy; the original drops remain available.')+
        section('Hunting locations',para('The quest’s Hunting locations option gives these example roaming areas. Use the letter and number on the indicated game map. Every original monster of the listed type in the specified zone counts.')+
            table(['Monster','Example area'],[('Exoray','Mushroom room: (G-9)/(G-10), mushroom room map.'),('Explosure','Bomb room: (I-8), bomb-room map.'),('Lich','Northwest tombs: (C-4), northwest tombs map. The past [S] zone does not count.')]))+
        section('Trade and unlock 55',steps('Put 1 Exoray Mold, 1 Bomb Coal and 1 Ancient Papyrus in your main Inventory.',
            'Use Trade on Zenith Armsmith and offer all three together: exactly one of each, with no gil or extra items.',
            'The three items are consumed. Your level limit becomes 55 across all jobs; In Defiant Challenge is completed and you receive the Horizon Breaker title.'))+
        para('You do not need to visit Maat for this first quest. '+link('limit-break','See the following increases and the final trial.')),
        facts=[('Start','Main level 50 · limit 50'),('Turn-in','Trade all 3 items together'),('Reward','Level limit 55'),('Trusts','Allowed')],parent='limit-break',status=status)

    stories=[
        ('coastal-dispatch','Coastal Dispatch',20,30,'4,000 gil + ONE: Beetle Earring +1 OR Silver Hairpin',[
            'Speak to Medicine Axe at the Valkurm Dunes outpost, H-7.',
            'Defeat 6 Damselflies in Valkurm Dunes.',
            'Trade exactly 4 Insect Wings to Medicine Axe. Existing wings count.',
            'Approach the Selbina entrance in Valkurm Dunes, G-9. Stay outside Selbina until the visit records.',
            'Defeat Valkurm Emperor, level 29–30. Prepare Trusts, then use its ??? in Whitebone Sands: (E-9) → Begin challenge.',
            'Report to Medicine Axe. Return to the Armsmith and claim your reward in My Quests.']),
        ('sandbound-repairs','Sandbound Repairs',35,47,'6,000 gil + ONE: Puissance Ring, Alacrity Ring, Wisdom Ring OR Solace Ring',[
            'Speak to Lucretia at the Blacksmiths’ Guild in Northern San d’Oria: (E-6).',
            'Commission the repair: trade exactly 2 Iron Ingots to Lucretia. Bought or crafted ingots both work.',
            'Examine Dune Widow’s ??? in Eastern Altepa Desert: (G-8). Choose Investigate for quest.',
            'Defeat 6 Giant Spiders in Eastern Altepa Desert.',
            'Return to the same ???, choose Begin challenge and defeat Dune Widow, level 45–47.',
            'Report to Lucretia. Claim your reward from the Armsmith in My Quests.']),
        ('the-broken-watch','The Broken Watch',60,72,'10,000 gil + ONE: Ruby Ring, Emerald Ring, Diamond Ring OR Sapphire Ring (equip level 72)',[
            'Approach Jiwon’s shelter at the Qufim Island outpost, F-6, to record your visit.',
            'Speak to Jiwon about the damaged watch supplies.',
            'Trade exactly 3 Silk Threads to Jiwon. Gathered, bought or crafted threads count.',
            'Defeat 6 Robber Crabs, level 62–66, in the lower Boyahda Tree.',
            'Use Aquarius’s ??? in The Boyahda Tree: (H-9), lower map. Defeat Aquarius, level 69–71.',
            'Report to Jiwon at Qufim F-6. Claim your reward from the Armsmith in My Quests.'])]
    for key,title,level,recommended,reward,objectives in stories:
        add(key,title,'Quests','A six-step adventure: follow the current objective, help its NPCs and earn a final reward.',
            section('Start',para('At '+hub+', choose Zenith Adventures → Story quests → '+title+' → Accept quest. Start at main level '+str(level)+'; the final fight is recommended around level '+str(recommended)+'.'))+
            section('Six steps',steps(*objectives))+section('Reward',para(reward+'. Once per character.'))+
            section('Progress',para('Do the steps in order. My Quests names the next NPC, item or monster. Earlier kills do not count for later steps. At a supporting NPC, select the story’s option; Other business keeps the NPC’s original service. Trade only the requested materials.'))+
            para('Progress survives logout, death and job changes. There is no crafting-skill requirement for deliveries. Trusts are allowed for the final NM. '+link('nm-challenges','NM marker and reward guide')+'.'),
            facts=[('Start level',str(level)),('Final fight recommended',str(recommended)),('Steps','6'),('Reward','Gil + one choice')],parent='adventures',status=status)
    add('adventures','Zenith Adventures','Guides','Follow a connected story, join Eco-Warrior, or find your next useful goal.',
        section('Story quests',para('At Zenith Armsmith choose Zenith Adventures → Story quests. Each chain has six steps; My Quests shows only what you need to do next.')+
            table(['Adventure','Start / final fight recommendation','Final reward'],[(link(k,t),f'{l} / {r}',g)for k,t,l,r,g,o in stories]))+
        section('Other choices',listing([link('eco-warrior','Eco-Warrior')+' — the three-nation weekly circuit.',link('adventure-goals','World advice')+' — equipment and original quest suggestions.',link('nm-challenges','NM Challenges')+' — a separate main-menu section with 24 fights.']))+
        section('A clearer quest list',para('Standalone hunt contracts and exploration routes have been replaced by connected adventures. '+link('retired-activities','Already earned rewards stay available')+'. Inventory remains at 80 slots.')),parent='quests',status=status)

    nms=json.loads((Path(__file__).resolve().parents[1]/'progression-nms.json').read_text())
    rows=[]
    for r in nms:
        gift=f"{r['gift']['gil']:,} gil + ONE: "+' OR '.join(f"{c['quantity']} {c['name']}" for c in r['gift']['choices'])
        rows.append((r['name'],r['area'],f"{r['monsterLow']}–{r['monsterHigh']}",f"X {r['pos'][0]:g}, Z {r['pos'][2]:g}",r['reward'],gift))
    add('nm-challenges','NM Challenges','Quests','24 original named monsters, summoned from ??? markers, with a separate gift for your first victory.',
        section('Start a fight',steps('At Zenith Armsmith, choose NM Challenges → the monster’s name → Track this NM.',
            'Travel to the listed zone. Tracking gives the marker’s direction and approximate distance when you enter; the Scout can show guidance too.',
            'Find the ??? at the listed map square. Summon your Trusts, prepare, then choose Begin challenge.',
            'Defeat the monster within 15 minutes. After a loss, retry at the marker once the previous monster disappears.',
            'For your first victory, return to Zenith Armsmith → My Quests, select that NM and choose one gift.'))+
        para('No pop item or lottery wait is required. Native enemy levels, abilities and loot are preserved. Repeat fights can still drop native loot; the separate first-win gift is awarded only once per character.')+
        section('All 24 encounters',para('Locations use the letter and number on the game map. Listed levels are the monster’s levels, not a guarantee that the encounter is easy at that level.')+table(['NM','Zone','Enemy level','??? location','Featured native loot','First-win gift'],rows,ident='nm-challenge-table'))+
        section('Story encounters',para('Valkurm Emperor, Dune Widow and Aquarius also appear in story chains. Reach the relevant story step before fighting. Investigate for quest and Begin challenge are separate options on Dune Widow’s marker.')),
        facts=[('Encounters','24'),('Enemy levels','17–75'),('Time limit','15 minutes'),('Retry cost','Free')],parent='quests',status=status)

    add('city-rings','City Rings','Quests','Earn each city’s augmented ring through its own short quest, whatever your home nation.',
        section('How to earn a ring',steps('At main level 10+, choose Zenith Armsmith → Character Progress → City Rings and accept the city’s quest.',
            'Visit the listed city and defeat 3 of its named enemies in the listed outdoor zone after accepting.',
            'Return to the Armsmith and collect the ring from My Quests.'))+
        section('Three quests',table(['Quest','City to visit','Defeat 3','Reward: total stats'],[
            ('A Promise to San d’Oria','Northern San d’Oria','Orcish Fodder · West Ronfaure','San d’Orian Ring: DEF +2, STR +2, MND +2, Accuracy +2'),
            ('A Promise to Bastok','Bastok Markets','Young Quadav · North Gustaberg','Bastokan Ring: HP +15, DEX +2, VIT +2'),
            ('A Promise to Windurst','Windurst Woods','Yagudo Initiate · East Sarutabaruta','Windurstian Ring: MP +15, AGI +2, INT +2')]))+
        para('Each quest rewards once per character. These totals include the ring’s native stats and its augments. If you already own another version of the Rare ring, the claim waits; this package does not delete it automatically. Your reward remains saved.'),parent='character-progress',status=status)
    for key,title,job,level,boss,reward in [
        ('hold-the-line','Hold the Line','WAR',40,'Ironhide Beetle','Breastplate with Accuracy +2 and Attack +2 augments'),
        ('a-shadows-safeguard','A Shadow’s Safeguard','THF',45,'Cache Guardian','Brigandine with Accuracy +2 and AGI +1 augments')]:
        add(key,title,'Quests',f'The fourth {job} equipment chapter.',
            section('Walkthrough',steps(f'Finish and collect your level-35 {job} chapter. Reach {job} {level}+.',
                'At Zenith Armsmith choose Character Progress → Job Quests, select this chapter and Accept quest.',
                f'Visit the Qufim Scout beside the outpost. Prepare Trusts and begin your {boss} encounter.',
                'Win within 10 minutes. Stay alive, on the same job and within 50 yalms. The boss scales with your level; its minimum is '+str(level+2)+'.',
                'Collect your reward at Zenith Armsmith → My Quests.'))+section('Reward',para(reward+'. Once per character.')),
            parent='warrior-quests' if job=='WAR' else 'thief-quests',status=status)
    add('unlock-trusts','Unlock Trusts','Trusts','Earn Uka Totlihn and Monberaux through a challenge. Both require a starting-city Trust permit.',
        section('Uka Totlihn — level 40',steps('At main level 40+, open Zenith Armsmith → Character Progress → Unlock Trusts → Uka → Accept quest.',
            'Visit the Qufim Scout beside the outpost and begin the Wayward Weapon encounter. Prepare your current Trusts first.',
            'Win within 10 minutes. The boss scales with your level, with a minimum of 42. Stay alive, on the same job and within 50 yalms.',
            'Collect Trust: Uka Totlihn in My Quests.'))+
        section('Monberaux — level 60',steps('At main level 60+, choose Unlock Trusts → Monberaux → Accept quest. Monberaux in Upper Jeuno, G-10, remains an alternative quest contact.',
            'Find the ??? in the Batallia Downs sapling field around H-6.',
            'Prepare Trusts, choose Begin challenge and defeat Cratebreaker within 15 minutes. Its minimum level is 62 and it scales with yours. Stay alive, on the same job and within 50 yalms.',
            'Return to Zenith Armsmith → My Quests → Monberaux → Claim Trust.'))+
        para('Each spell is a permanent reward. Losing a fight does not erase acceptance; retry after the monster disappears. These quests unlock companions, while '+link('trust-journeys','Trust Capacity')+' increases how many you can summon. '+link('healers-promise','Apururu’s quest')+' keeps its own NPC and walkthrough.'),parent='character-progress',status=status)

    retired_body=section('What changed',para('Progression replaces the 16 standalone hunt contracts, two exploration routes, hunt milestones and Crystal Paths with '+link('adventures','three connected story adventures')+' and '+link('nm-challenges','24 NM Challenges')+'. The old activities are no longer offered as new quests.'))+section('Already earned a reward?',para('At the first login after upgrading, completed but unclaimed old rewards are retained. Collect them from Zenith Armsmith → My Quests. Partially finished retired activities do not continue in the new menus; their old counters are not erased.'))+section('Travel stays available',para(link('gate-crystals','Gate Crystal travel')+' continues through Zenith Guide. Collected crystals, existing equipment, city rings, learned Trusts and the 80-slot Inventory are preserved.'))
    add('retired-activities','Older Quest Rewards','Reference','Where to find rewards from activities replaced by Progression.',retired_body,parent='quests',status=status)
    for key,title in [('hunt-contracts','Hunt Contracts'),('exploration-routes','Exploration Routes'),('crystal-paths','Crystal Paths')]:
        add(key,title,'Reference','This activity is retired in Progression. Previously earned rewards remain in My Quests.',retired_body,parent='retired-activities')
    for key in ['three-roads']+[r[0] for r in ed.ROAD]:
        add(key,P[key]['title'],'Reference','An earlier prepared quest design, superseded in the current progression guide.',
            section('Current adventures',para('Use '+link('adventures','Zenith Adventures')+' for the current connected stories and '+link('city-rings','City Rings')+' for the three permanent city rewards. The old Courier, Smith and Scribe instructions are not part of Progression v2.1.0.')),parent='retired-activities')

    # Refresh preserved walkthroughs without changing their objectives or rewards.
    quest_keys=['warrior-quests','thief-quests','trust-journeys','companions-of-the-road','an-adventurer-leads','breakwater-crab']+[q[2] for q in ed.EQUIPMENT]
    for key in quest_keys:
        p=P[key]
        p['body']=p['body'].replace('Equipment quests → Claim reward','My Quests → select the chapter → Claim reward').replace('Trust slots → Claim reward','My Quests → select the capacity quest → Claim reward')
        p['body']=p['body'].replace('Select Equipment quests. Quest details explains the task; Accept quest starts it.','Select Character Progress → Job Quests and open the chapter. Read its details, then choose Accept quest.').replace('Open Trust slots. Quest details shows the requirements; choose Accept quest to begin.','Open Character Progress → Trust Capacity, read the requirements and choose Accept quest.')
        if key=='breakwater-crab':p['intro']='The level-35 encounter for the WAR and THF equipment journeys.'
        p['status']=status
    for key,new in [('warrior-quests','hold-the-line'),('thief-quests','a-shadows-safeguard')]:
        P[key]['intro']=P[key]['intro'].replace('Three chapters','Four chapters')
        level, boss, reward = (40, 'Ironhide Beetle', 'Breastplate: Accuracy +2 and Attack +2 augments') if key == 'warrior-quests' else (45, 'Cache Guardian', 'Brigandine: Accuracy +2 and AGI +1 augments')
        P[key]['body']=P[key]['body'].replace('</tbody>', '<tr><td>'+str(level)+'</td><td>'+link(new)+'</td><td>Win your own '+boss+' encounter at the Qufim Scout.</td><td>'+reward+'</td></tr></tbody>', 1)
    add('equipment-quests','Equipment Quests','Quests','Eight equipment chapters: four for WAR and four for THF, with independent saved progress.',
        section('Start and claim',steps('Visit '+hub+' on the required main job and level.',
            'Open Character Progress → Job Quests. Read the chapter’s objective and reward, then choose Accept quest.',
            'Complete its named objectives after accepting. Earlier kills do not count.',
            'Return to My Quests, select the chapter and choose Claim reward. Collect it fully before beginning the next chapter.'))+
        section('Choose your track',listing([link('warrior-quests','WAR: levels 15, 25, 35 and 40'),link('thief-quests','THF: levels 20, 25, 35 and 45')]))+
        section('Field help',para(link('zenith-scout','Zenith Scout')+' records the two level-25 reports and starts the Qufim trial encounters. Your quest details name the actual enemies and remaining count.'))+
        section('Rewards',para('Each chapter rewards once. Make room before claiming; two slots are needed for the paired THF daggers. If your bag fills, the remaining reward stays saved. This guide describes the package; installation is not yet confirmed.')),parent='character-progress',status=status)

    add('adventure-goals','World Advice','Guides','Find an equipment option or an original quest that suits your job and level.',
        section('Use the advice menu',para('At Zenith Armsmith choose Zenith Adventures → World advice. Read the source and requirements, then pin a goal if useful. Equipment comes from its normal source; original quest acceptance and rewards stay with the named NPC.'))+
        section('Equipment',para('Compare suggested gear with what you wear, then check '+link('market-catalog','the Auction House catalogue')+'. A suggestion does not grant an item or guarantee current stock.'))+
        section('Looking for a monster challenge?',para('Open the separate '+link('nm-challenges','NM Challenges')+' section. Choose a monster, track its marker and use ??? → Begin challenge.')),parent='adventures',status=status)
    add('quests','Quests','Quests','Choose a story, hunt an NM, or earn a permanent character upgrade.',
        section('Your quest hub',para(link('adventurer-log','Quest Menu')+' explains where everything lives. Check My Quests for active steps and waiting rewards.'))+
        section('Zenith Adventures',listing([link(k,t)for k,t,*rest in stories]+[link('eco-warrior','Eco-Warrior'),link('adventure-goals','World advice')]))+
        section('NM Challenges',para(link('nm-challenges','All 24 encounters, marker positions and rewards')))+
        section('Character Progress',listing([link('equipment-quests','WAR and THF Job Quests'),link('trust-journeys','Trust Capacity'),link('unlock-trusts','Unlock Trusts'),link('city-rings','City Rings'),link('limit-break','Limit Break')]))+
        section('Other quest givers',listing([link('healers-promise','Apururu: A Healer’s Promise'),link('trust-starting-cities','Starting-city Trust quests'),link('road-companion','A Companion for the Road'),link('chocobos-wounds','Chocobo’s Wounds'),link('tutorial-quests','Tutorial quests'),link('fear-of-the-dark','Fear of the Dark')]))+
        para(link('retired-activities','Previously earned rewards')),status=status)

    # Remove stale activity invitations and menu paths from navigation and hubs.
    import re
    for key,p in P.items():
        if key in ('update-log','sources'):continue  # These contain explicitly dated release history.
        p['body']=re.sub(r'<h2>Optional Adventures</h2>.*?(?=<h2>|$)','',p['body'],flags=re.S)
        p['body']=p['body'].replace('Equipment quests, Trust slots and Crystal Paths; near Home Point #1','My Quests, Zenith Adventures, NM Challenges and Character Progress; near Home Point #1')
        p['body']=p['body'].replace('Accept, review and claim equipment quests, Trust-slot journeys and Crystal Paths. Choose Quest details, Accept quest or Claim reward separately. Equipment chapters require the correct main job and level.','Your hub for My Quests, Zenith Adventures, NM Challenges and Character Progress.')
    P['index']['body']=re.sub(r'^<h2>New optional adventures</h2>.*?</p>','',P['index']['body'],flags=re.S)
    P['index']['body']=section('Progression v2.1.0',para(link('first-limit-break','First Limit Break: the three items')+' · '+link('adventurer-log','New quest menu')+' · '+link('adventures','Story adventures')+' · '+link('nm-challenges','24 NM Challenges')))+P['index']['body']
    P['server-rules']['body']=P['server-rules']['body'].replace('Maximum level 75. The configured initial limit is 50; complete the limit-break quests to progress.','Maximum level 75. '+link('limit-break','Complete First Limit Break at 50; automatic increases at 55, 60 and 65; final job trial at 70.'))
    P['getting-started']['body']=P['getting-started']['body'].replace('Three Roads is a prepared series that is not installed yet.','City Rings start at level 10; story adventures start at level 20.')
    P['getting-started']['body']+=section('Your first limit break',para('At level 50, '+link('first-limit-break','collect three items from named monsters')+' and trade them to the Armsmith. The following increases open automatically until the final trial at 70.'))
    P['trusts']['body']+=section('More earned companions',para(link('unlock-trusts','Uka Totlihn at 40 and Monberaux at 60')+' are under Character Progress → Unlock Trusts.'))
    P['gate-crystals']['body']=re.sub(r'<h2>Collection quest</h2>.*?(?=<h2>|$)',section('Quest rewards and travel',para('Crystal Paths is retired. '+link('retired-activities','Older earned rewards')+' remain in My Quests; Gate Crystal travel continues.')),P['gate-crystals']['body'],flags=re.S)
    P['eco-warrior']['body']=P['eco-warrior']['body'].replace('Zenith Armsmith → Eco-Warrior → Activate EXP bonus','Zenith Armsmith → My Quests → Eco EXP bonus → Activate EXP bonus').replace('Zenith Armsmith → Eco-Warrior','Zenith Armsmith → Zenith Adventures → Eco-Warrior')
    P['eco-warrior']['body']=P['eco-warrior']['body'].replace('Requires Eco-Warrior v1.0, Cleanup Phase 2 and the current Adventures v1.1 Armsmith menu.','Uses the Eco-Warrior rules with the Progression v2.1.0 menu. Saved EXP bonuses appear in My Quests.')
    P['eco-warrior']['status']=status
    add('daily-activities','Daily Activities','Guides','Optional objectives alongside your main adventures.',section('Choose an activity',listing([link('daily-roe','Daily RoE objectives'),link('eco-warrior','Eco-Warrior: one reward per Conquest week'),link('adventures','Story adventures: saved steps with no daily deadline'),link('nm-challenges','NM Challenges: repeat fights and once-only first-win gifts')]))+para('A separate custom daily currency and attendance reward system has not been added.'))
    add('roadmap','Roadmap','Reference','Current package work and the decisions still open.',
        section('Packaged in Progression v2.1.0',listing(['Unified in-game quest menus and My Quests rewards.','Three connected stories, 24 NM Challenges and retained completed old rewards.','Job quests, city rings, Trust capacity and Trust unlocks in Character Progress.','First Limit Break item hunt at 50, automatic increases to 70, then the original solo final trial.']))+
        section('Next verification',para('Install the delivered package and check menus, marker placement, quest credit and rewards in game. Windows installation and live play for v2.1.0 are not confirmed.'))+
        section('Still under discussion or deferred',listing(['One Trust in the final limit-break trial: discussion only; current trial remains solo.','Custom quest-completion fanfare: not included.','Further illustrated maps: deferred.','Guide addon and UI font work: canceled at the player’s request.'])))
    P['update-log']['body']=section('21 September: Progression v2.1.0 guide',para('The wiki now matches the delivered package: First Limit Break at 50 uses three monster items, with a once-only guarantee after three eligible kills per type; the following increases open automatically until 70. Added the unified quest menu, three story chains, all 24 NM marker locations and gifts, city rings, fourth WAR/THF chapters, and Uka/Monberaux guidance. Old hunt, exploration and Crystal Paths pages now explain retirement and retained rewards. This website update does not confirm installation on the game server.'))+section('Earlier release history',para('The entries below record older package states. Use the current guides above for the Progression menus.'))+P['update-log']['body']
    P['sources']['body']=section('Current progression guide',para('Checked against the delivered ZenithXI-Progression-v2.1.0 package: limit_break.lua, quest_menus.lua, story_journeys.lua, nm_challenges.lua and its 24-entry data catalogue, plus the preserved job, earned-journey, clinic and Eco-Warrior providers. Coordinates are copied from the reviewed source; no new map-grid positions are inferred.'))+P['sources']['body']
