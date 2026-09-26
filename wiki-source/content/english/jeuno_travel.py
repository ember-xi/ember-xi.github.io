"""Jeuno travel and stable rentals, matched to World Quests v3.3.0."""
from lxml import html

def install(ed):
    P=ed.P
    add,section,para,table,link=ed.add,ed.section,ed.para,ed.table,ed.link
    status='World Quests v3.3.0. Install the update and restart the server to use the Jeuno services.'
    # Remove the retired quest from directories, reward tables and related quests.
    for p in P.values():
        if 'road-companion.html' in p['body']:
            root=html.fragment_fromstring(p['body'],create_parent='div')
            for anchor in list(root.xpath('.//a[@href="road-companion.html"]')):
                row=next((a for a in anchor.iterancestors() if a.tag in ('tr','li')),None)
                if row is not None and row.getparent() is not None:row.getparent().remove(row)
                elif anchor.getparent() is not None:
                    anchor.set('href','mounts.html');anchor.text='Chocobo Rentals'
            p['body']=''.join(html.tostring(c,encoding='unicode') for c in root)
        for field in ('intro','body'):
            p[field]=p[field].replace('Apururu and Mapitoto keep their own quests.','Apururu keeps her own quest.')
            p[field]=p[field].replace('Apururu and Mapitoto keep their own NPCs.','Apururu keeps her own NPC.')
            p[field]=p[field].replace('Apururu keeps A Healer’s Promise, and Mapitoto keeps A Companion for the Road.','Apururu keeps A Healer’s Promise.')
            p[field]=p[field].replace('Trusts and personal chocobo','Trusts and chocobo rentals').replace('Check recovery after combat and the Mapitoto quest in game.','Check recovery after combat and stable rentals in game.')
    add('mounts','Chocobo Rentals','Travel','Earn a Chocobo License, then rent a chocobo from a stable.',
        section('Before your first ride',para('Complete '+link('chocobos-wounds','Chocobo’s Wounds')+' with Brutus in Upper Jeuno (G-7). Its reward is the Chocobo License. Keep this license for stable rentals.'))+
        section('Rent in Upper Jeuno',table(['NPC','In-game map','Service'],[(link('brutus','Brutus'),'Upper Jeuno (G-7)','Chocobo License quest'),('Mairee or Couvoullie','Upper Jeuno (G-7), chocobo stables','Chocobo rental'),('Mejuone','Upper Jeuno (G-7), chocobo stables','Stable shop; Gysahl Greens')]))+
        section('How to ride',para('Speak to Mairee or Couvoullie at the stables and choose the rental. The NPC shows the current fee and checks the normal rental requirements. Pay the fee to start your ride. Return to a stable when you need another rental.'))+
        section('Jeuno connections',para(link('zenith-outpost','Zenith Outpost')+' and '+link('zenith-guide','Zenith Guide')+' are beside Home Point #1 in Upper Jeuno (F-5). Choose an outpost or an owned Gate Crystal destination.'))+
        section('References',para('<a href="https://horizonffxi.wiki/Upper_Jeuno">Upper Jeuno NPC locations</a>. Rental behavior was checked against the native Mairee and Couvoullie scripts. Zenith travel changes are defined by World Quests v3.3.0.')),
        parent='travel',status=status)
    p=P['chocobos-wounds']
    root=html.fragment_fromstring(p['body'],create_parent='div')
    for heading in list(root.xpath('.//h2[text()="Next step"]')):
        sibling=heading.getnext()
        while sibling is not None and sibling.tag!='h2':
            following=sibling.getnext();sibling.getparent().remove(sibling);sibling=following
        heading.getparent().remove(heading)
    p['body']=''.join(html.tostring(c,encoding='unicode') for c in root)+section('After receiving your license',para('Speak to Mairee or Couvoullie at the Upper Jeuno chocobo stables (G-7) to '+link('mounts','rent a chocobo')+'.'))
    p['parent']='mounts'
    add('zenith-outpost','Zenith Outpost','NPCs','Outpost travel from Jeuno using the same rules and fees as the starting cities.',
        section('Location',para('Upper Jeuno (F-5), beside Home Point #1 near the Batallia Downs gate. Look for the goblin named Zenith Outpost. Zenith Guide stands beside him.'))+
        section('Travel',para('Speak to Zenith Outpost, choose a destination, then pay gil or Conquest Points. The menu shows the price before you pay. Use Next and Previous for more destinations; Back returns from the payment screen.'))+
        section('Requirements',para('No Supply Run or extra Jeuno rank requirement. Your current main-job level and the existing story-access rules determine which destinations appear. Fees use the same national-control calculation as city outpost travel. '+link('outposts','Read the destination requirements')+'.'))+
        section('Return',para('The normal outpost return service takes you to your home nation. This update adds a departure point in Jeuno; it does not change the return destination.')),
        facts=[('Zone','Upper Jeuno'),('In-game map','F-5'),('Landmark','Home Point #1'),('Payment','Gil or Conquest Points')],parent='outposts',status=status)
    P['outposts']['body']=section('Jeuno service',para(link('zenith-outpost','Zenith Outpost')+' — Upper Jeuno (F-5), beside Home Point #1. Same destination rules, gil fees and Conquest Point option as the city services. No additional Rank 3 requirement.'))+P['outposts']['body']
    P['outposts']['status']=status
    P['zenith-guide']['body']+=section('Jeuno location',para('Upper Jeuno (F-5), beside Home Point #1 and Zenith Outpost. The same Gate Crystal menu, crystal ownership, first-trip allowance, subsequent fee and teleport animation apply here.'))
    P['zenith-guide']['status']=status
    P['gate-crystals']['body']+=section('From Jeuno',para('Use Zenith Guide beside Upper Jeuno Home Point #1 (F-5). This shares your existing crystal unlocks and first-trip allowance with the guides in the starting cities.'))
    add('zone-upper-jeuno','Upper Jeuno','Zones','Chocobo stables, quest contacts and Zenith travel services.',
        section('NPCs and services',table(['NPC','In-game map','Service'],[
            (link('zenith-outpost','Zenith Outpost'),'F-5 · Home Point #1','Outpost travel; gil or CP'),
            (link('zenith-guide','Zenith Guide'),'F-5 · Home Point #1','Gate Crystal travel'),
            (link('brutus','Brutus'),'G-7 · Chocobo stables','Chocobo’s Wounds; Chocobo License'),
            ('Mairee or Couvoullie','G-7 · Chocobo stables','Chocobo rental'),
            ('Mejuone','G-7 · Chocobo stables','Stable shop'),
            (link('monberaux','Monberaux'),'G-10 · Infirmary','The Doctor’s Oath'),
        ]))+section('Getting around',para('Home Point #1 is near the Batallia Downs gate. For a chocobo, visit the stables at (G-7). '+link('mounts','Chocobo rental guide')+'.')),
        parent='zones',status=status)
    if 'mapitoto' in P:
        add('mapitoto','Mapitoto','NPCs','A resident of the Upper Jeuno chocobo stables (G-7).',section('Chocobo travel',para('For the Chocobo License, speak to '+link('brutus','Brutus')+'. Rent your chocobo from Mairee or Couvoullie at the stables. '+link('mounts','Read the rental guide')+'.')),parent='npcs',status=status)
    # The old URL remains a redirect, outside search and the quest directory.
    P.pop('road-companion',None)
    P['travel']['body']+=section('Jeuno and chocobos',para(link('zenith-outpost','Outpost travel from Upper Jeuno (F-5)')+' · '+link('zenith-guide','Gate Crystal travel')+' · '+link('mounts','Chocobo rentals')+'.'))
    P['npcs']['body']+=section('Jeuno travel',para(link('zenith-outpost','Zenith Outpost')+' and '+link('zenith-guide','Zenith Guide')+' — Upper Jeuno (F-5), Home Point #1.'))
    P['update-log']['body']=section('23 September 2026 — Jeuno travel',para('World Quests v3.3.0 adds Zenith Outpost and Zenith Guide beside Upper Jeuno Home Point #1 (F-5). Outpost rules match the starting cities. Personal chocobo summoning and its custom quest are retired; the Chocobo License and stable rentals remain. Tenzoki’s Chocobo Companion is removed from Mounts at login after installation.'))+P['update-log']['body']

    P['tutorial-quests']['body']+=section('Echad Ring retired',para('From World Quests v3.3.1, the final tutorial step awards 12 Free Chocopasses only. Echad Ring is no longer a tutorial reward in any starting city. Existing tutorial progress remains.'))
    P['update-log']['body']=section('23 September 2026 — Echad Ring retired',para('World Quests v3.3.1 removes Echad Ring from the final tutorial reward in all three starting cities. The installer removes only Tenzoki’s Echad Ring copies, with an inventory backup; other items and tutorial progress remain. No other balance changes are included. Install the package while the game server is stopped.'))+P['update-log']['body']
