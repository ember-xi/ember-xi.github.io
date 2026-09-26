"""Original, concise route summaries checked against the linked references.

Horizon-only inventory rewards, modern retail shortcuts and unverified Zenith
battlefield settings are deliberately excluded. Source revision is pinned.
"""
from urllib.parse import quote
import re

RECORDS=[]
REV='f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4'
NAMES={'sandoria':"San d'Oria",'bastok':'Bastok','windurst':'Windurst'}
REWARDS={'1-3':'Rank 2; 1,000 gil','2-3':'Rank 3; 3,000 gil','3-3':'Rank 4; 5,000 gil','4-1':'Rank 5; 10,000 gil; Airship Pass','5-2':'Rank 6; 20,000 gil','6-2':'Rank 7; 40,000 gil','7-2':'Rank 8; 60,000 gil','8-2':'Rank 9; 80,000 gil','9-2':'Rank 10; 100,000 gil; national flag'}
def m(n,num,title,route,locations=(),notes=(),required=None,start=None,filename=None):
    source='https://horizonffxi.wiki/'+quote(NAMES[n].replace(' ','_')+'_Mission_'+num)
    stem=re.sub(r"[,’']",'',title).replace(' ','_')
    if title=="The Ruins of Fei'Yin":stem='The_Ruins_of_FeiYin'
    if title=="The Jester Who'd Be King":stem='The_Jester_Whod_be_King'
    filename=filename or num.replace('-','_')+('_0_' if num=='2-3' else '_')+stem+'.lua'
    RECORDS.append(dict(nation=n,number=num,title=title,steps=route.split('|'),locations=[(x,y,source+'#Walkthrough') for x,y in locations],notes=list(notes),requirements=required or f'Be allied with {NAMES[n]}, have Rank {num[0]}, and finish the preceding required story steps. Raise Rank Points if the mission is not offered.',start=start or NAMES[n]+' mission guard',reward=REWARDS.get(num,'Rank Points'),source=source,code=f'https://github.com/LandSandBoat/server/blob/{REV}/scripts/missions/{n}/{filename}'))

def magicite(n):
    m(n,'4-1','Magicite',
      'Begin at your embassy in Ru’Lude Gardens, then visit the Audience Chamber (H-6). Take the letter to Aldo in Lower Jeuno’s Tenshodo headquarters; arrange Tenshodo access first.|'
      'After meeting Aldo, trade Coeurl Meat to Baudin in Upper Jeuno for the Crest of Davoi. Speak with Muckvix, Paya-Sabya, then Muckvix again for the Yagudo Torch.|'
      'Speak with Sattal-Mansal. Obtain a Quadav Charm from De’Vyu Headhunter and a Quadav Augury Shell from Go’Bhu Gascon in Beadeaux; exchange both for his access key items.|'
      'Reach Davoi’s Wall of Dark Arts (G-7) and collect the Optistone beyond it.|'
      'Traverse Castle Oztroja, use the torch-access door, and collect the Orastone in the Altar Room.|'
      'Enter Qulun Dome through Beadeaux and collect the Aurastone.|'
      'Visit the Audience Chamber, then your embassy in Ru’Lude Gardens for the promotion.',
      notes=('Bring Sneak and Invisible supplies. Obtain the access key items before attempting the sealed areas. The source maps show the multi-floor routes.','An existing Airship Pass changes that part of the original reward; this is not a Khazam Airship Pass.'),start=NAMES[n]+' embassy in Ru’Lude Gardens')

m('sandoria','1-1','Smash the Orcish Scouts',
  'Accept the mission from a San d’Oria mission guard.|Hunt Orcish Fodder in East or West Ronfaure for one Orcish Axe.|Trade that axe to the mission guard.',
  [('Orcish Fodder','East / West Ronfaure')],required='San d’Oria allegiance and Rank 1. Accept the mission before turning in the axe.')
m('sandoria','1-2','Bat Hunt',
  'Accept Bat Hunt. Enter King Ranperre’s Tomb from East Ronfaure (H-11).|Examine the Tombstone around (H/I-10). Hunt Ding Bats at night for Orcish Mail Scales.|Take the scales back to a San d’Oria mission guard.',
  [('Tombstone','King Ranperre’s Tomb (H/I-10)'),('Entrance','East Ronfaure (H-11)')],
  ['Ding Bats appear from 18:00 to 06:00 Vana’diel time. Avoid the nearby ghost at low level.','Repeat completions use a Bat Fang and require another Tombstone visit; the first completion requires Orcish Mail Scales.'])
m('sandoria','1-3','Save the Children',
  'Accept the mission and speak with Arnau at the cathedral altar in Northern San d’Oria (M-6).|Enter Ghelsba Outpost from West Ronfaure (E-4). Reach the Hut Door (F-10).|Enter Save the Children and defeat the three Orcs.|Examine the Hut Door again after victory to use the Orcish Hut Key and see the rescue scene.|Report to a San d’Oria mission guard.',
  [('Arnau','Northern San d’Oria (M-6)'),('Hut Door','Ghelsba Outpost (F-10)')],['Do not leave immediately after the battle: the second Hut Door interaction is part of completion.'])
m('sandoria','2-1','The Rescue Drill',
  'Accept the drill and meet Galaihaurat at La Theine Plateau (E-6). Descend the ravine at (F-6) toward Ordelle’s Caves.|Inside the caves, find Ruillont by the pond at (G-3).|Return to La Theine and speak with Deaufrain, Equesobillot and Galaihaurat until the assigned knight gives you Ruillont’s Bronze Sword.|Trade the sword to Ruillont. Speak with Vicorpasse outside for the Rescue Training Certificate.|Report to your mission guard.',
  [('Ruillont','Ordelle’s Caves (G-3)'),('Vicorpasse','La Theine Plateau (F-6)')],['A sword bought in advance does not bypass the conversation that identifies Ruillont’s missing weapon.'])
m('sandoria','2-2','The Davoi Report',
  'Accept the mission and enter Davoi from Jugner Forest (G-12). Speak with Zantaviat near the entrance.|Examine the ! on the south bank of the pond at Davoi (J-8) for the Lost Document.|Return to Zantaviat for the report, then speak with your mission guard.|Visit the Papal Chamber upstairs in Northern San d’Oria’s cathedral to finish.',
  [('Lost Document','Davoi (J-8), south side of pond')],['Optional for rank progression when sufficient Rank Points unlock 2-3.'])
m('sandoria','2-3','Journey Abroad',
  'Accept the mission and speak with Halver. This route visits Bastok first; the opposite order uses different objectives.|Meet Savae E Paleade in Metalworks (I-9), then Pius (J-8) and Grohm (H-9).|Obtain Mine Gravel in Palborough Mines using a Pickaxe at a Mythril Seam. Feed it to the third-floor refiner (I-6), pull its lever, then collect Mythril Sand from the lever below. Trade the sand to Savae E Paleade.|Meet Mourices in Windurst Woods (F-10), then Kupipi in Heavens Tower for the Dark Key.|Reach Balga’s Dais through Giddeus. Win The Rank 2 Final Mission against Searcher and Black Dragon.|Return to Mourices for the report, then Halver for Rank 3.',
  [('Bastok consul','Metalworks (I-9)'),('Windurst consul','Windurst Woods (F-10)')],
  ['This is the Bastok-first walkthrough. If Windurst is already your first destination, use the alternate route in the reference rather than following the mining steps.'])
m('sandoria','3-1','Infiltrate Davoi',
  'Accept the mission and examine Prince Trion’s room in Chateau d’Oraguille (G/H-7).|Enter Davoi and speak with the patrolling Quemaricond around (H-7) to obtain the Royal Knights’ report.|Return to Trion’s room to finish.',
  [('Quemaricond','Davoi (H-7), patrol')],['A repeat run uses Zantaviat and the ! points at K-7, L-8 and J-7, then Zantaviat and a mission guard. The first run follows Trion’s instructions.'])
m('sandoria','3-2','The Crystal Spring',
  'Accept the mission and obtain one Crystal Bass. Buy it from the Auction House when available, or fish at Jugner Forest’s Crystwater Spring (J-9).|Trade the fish to a mission guard.|Enter Chateau d’Oraguille for the scene, then speak with Chalvatot at (F-7).',
  [('Crystwater Spring','Jugner Forest (J-9)'),('Chalvatot','Chateau d’Oraguille (F-7)')],['Optional if your Rank Points already allow 3-3. Repeat runs do not require the Chateau scenes.'])
m('sandoria','3-3','Appointment to Jeuno',
  'Accept the mission, speak with Halver, and examine the Great Hall door to receive the ambassador’s letter.|Meet Nelcabrit in the San d’Oria embassy in Ru’Lude Gardens.|Enter Delkfutt’s Tower. Obtain a Delkfutt Key from Porphyrion on floor 10 if you lack access; use the key and elevator route to reach the basement.|Examine the basement door at (M-8) for the ambassador scene; trade the physical key if necessary.|Return to the embassy and examine the ambassador’s office door at (H-10).',
  [('Ambassador door','Lower Delkfutt’s Tower basement (M-8)')],['The three nations use different basement doors. Choose the San d’Oria door.'])
magicite('sandoria')
m('sandoria','5-1',"The Ruins of Fei'Yin",
  'Visit Chateau d’Oraguille and speak with Halver. Accept the mission from a guard, then obtain the New Fei’Yin Seal from Halver.|Enter Fei’Yin from Beaucedine Glacier (J-4). Continue to Qu’Bia Arena at Fei’Yin (K-8).|Enter The Rank 5 Mission. Defeat Archlich Taber’quoan while managing its skeleton helpers.|After receiving the Burnt Seal, report to Halver.',
  [('Arena entrance','Fei’Yin (K-8)')],['The New Fei’Yin Seal is required. The classic battlefield is level 50 capped; check Zenith’s entry message and use suitable equipment.'])
m('sandoria','5-2','The Shadow Lord',
  'Accept the mission and speak with Halver, then visit Prince Trion’s room.|Travel through Xarcabard, Castle Zvahl Baileys and Castle Zvahl Keep to the Throne Room. The Keep’s teleporters lead toward the final passage.|Examine the door for the scene and enter the Shadow Lord battle.|In phase one, alternate physical and magical damage as his immunities change. Be ready for sustained area damage in phase two.|After victory, return to Halver. Examine the Great Hall door for the closing scene.',
  [('Battlefield','Throne Room, through Castle Zvahl Keep')],['Bring both physical and magical damage options. Do not assume another server’s Trust permissions apply to Zenith.'])
m('sandoria','6-1',"Leaute's Last Wishes",
  'Finish the Great Hall scene from 5-2. Accept this mission, speak with Halver and examine the Great Hall door for the king’s request.|Find Dreamrose flowers in Western Altepa Desert (G-7). Examine them to summon Sabotender Enamorado.|Defeat it and examine the flowers again to obtain the Dreamrose.|Return to Halver, then approach the Chateau garden (F-8) for the final scene and Piece of Paper.',
  [('Dreamrose flowers','Western Altepa Desert (G-7)')],['Plan for 1000 Needles damage; spreading it across eligible nearby party members and pets can help.'])
m('sandoria','6-2',"Ranperre's Final Rest",
  'Accept the mission and visit Prince Trion’s room.|At King Ranperre’s Tomb (H-8), examine the Heavy Stone Door and defeat the summoned skeleton enemies.|Examine the door again, enter and check the Tombstone for the Ancient San d’Orian Book.|Report to a mission guard. After the deciphering stage becomes available, speak with the guard again and visit Trion.|Return to the Heavy Stone Door for its scene, then report to a mission guard.',
  [('Heavy Stone Door','King Ranperre’s Tomb, first map (H-8)')],['If the guard is still deciphering the book, zone and speak again. Follow the in-game wait condition rather than assuming another server’s timer.'])
m('sandoria','7-1','Prestige of the Papsque',
  'Accept the mission and visit the Papal Chamber in Northern San d’Oria’s cathedral.|Enter Bostaunieux Oubliette. Speak with Couchatorage by the sewer lid at map 1 (E-7) to descend.|Follow the route to map 2 (E-10), emerging on the raised West Ronfaure ledge at (E-8).|Examine the ???, defeat Marauder Dvogzog, then examine it again for the Ancient San d’Orian Tablet.|Return to the Papal Chamber.',
  [('Exit ledge','West Ronfaure (E-8), reached through the Oubliette')],['Do not jump off the ledge before collecting the tablet. Prepare for Hundred Fists.'])
m('sandoria','7-2','The Secret Weapon',
  'Ask a mission guard about the assignment. Visit Chateau d’Oraguille’s garden (F-7), then return to the guard to accept it.|Reach Horlais Peak through the Ghelsba / Yughott route and enter The Secret Weapon.|Defeat the three Orcs, their two warmachines and the Dragoon’s wyvern. Crowd control helps keep the fight manageable.|After the victory scene and Crystal Dowser, report to a San d’Oria mission guard.',
  [('Battlefield','Horlais Peak')],['Prepare for several simultaneous targets and enemy special abilities.'])
m('sandoria','8-1','Coming of Age',
  'Accept the mission. Enter Chateau d’Oraguille for the scene and speak with Halver.|Enter Quicksand Caves from Eastern Altepa Desert (H-10). On map 2, drop at (E-11) and reach the Fountain of Kings at (G-14).|Examine the fountain to summon Honor and Valor. Defeat the enemies, then examine it again for Drops of Amnio.|Return to Halver. Once the story wait has elapsed, enter Northern San d’Oria for the closing scene.',
  [('Fountain of Kings','Quicksand Caves map 2 (G-14)')],['The reference uses a Japanese-midnight wait. Zenith’s actual story timer has not been play-tested.'])
m('sandoria','8-2','Lightbringer',
  'Accept the mission, examine the Great Hall door and speak with Rahal (H-9) for the Crystal Dowser.|Prepare a Prelate Key for the Temple of Uggalepih route. Defeat the Temple Guardian to open the guarded passage.|In the destination hall, inspect the ??? behind doors one, three and four, counted west to east. Each player needs all three Pieces of a Broken Key.|Check the second door to summon Nio-Hum and Nio-A. Defeat them and examine that door again.|Return to the Great Hall door for Rank 9.',
  [('Rahal','Chateau d’Oraguille (H-9)'),('Key fragments','Temple of Uggalepih, four-door hall')],['Doors and fragments are individual progress checks. Keep Tonberry hate and dungeon access in mind.'])
m('sandoria','9-1','Breaking Barriers',
  'Accept the mission and examine the Great Hall door.|Collect the figures in this order: Titan from the ??? in Valley of Sorrows (I-8), then Garuda from Xarcabard (H-7).|Enter Eldieme Necropolis from Batallia Downs (I-10), reach the southern room and descend at (G-9). Continue to the isolated Batallia island.|Examine the ??? near the stone monument to summon Suparna and Suparna Fledgling. Defeat both, then check again for the Figure of Leviathan.|Return to the Great Hall door.',
  [('Figure of Titan','Valley of Sorrows (I-8)'),('Figure of Garuda','Xarcabard (H-7)')],['The three figures must be obtained in order.'])
m('sandoria','9-2','The Heir to the Light',
  'Accept the mission. Enter Northern San d’Oria for the ceremony scene, then Chateau d’Oraguille.|Travel to Fei’Yin and Qu’Bia Arena. Enter The Heir to the Light.|Clear the first Orc group. In phase two, protect Prince Trion while defeating Warlord Rojgnoj and his two companions; Trion’s defeat fails the battle.|After victory, enter Northern San d’Oria and examine the Great Hall door.|Visit the Heavy Stone Door in King Ranperre’s Tomb (H-8), then speak with Halver for the rewards.|Enter Southern San d’Oria for the epilogue.',
  [('Final battlefield','Qu’Bia Arena'),('Final tomb scene','King Ranperre’s Tomb (H-8)')],['Have healing available for Prince Trion, not only the player party.'])

m('bastok','1-1','The Zeruhn Report',
  'Accept the mission from a Bastok mission guard.|Enter Zeruhn Mines through Bastok Mines (D-7). Speak with Makarim at (H-11) for the Zeruhn Report.|Return to the Metalworks and speak with Naji near the President’s Office (J-8).',
  [('Makarim','Zeruhn Mines (H-11)'),('Naji','Metalworks (J-8)')],required='Bastok allegiance and Rank 1.')
m('bastok','1-2','A Geological Survey',
  'Accept the mission and speak with Cid in Metalworks (H-8) for the Blue Acidity Tester.|Enter Dangruf Wadi from South Gustaberg (D-9). At (I-8), ride the geyser to the ledge.|Check that the key item is now a Red Acidity Tester.|Report to Cid.',
  [('Cid','Metalworks (H-8)'),('Geyser','Dangruf Wadi (I-8)')],['This is a key-item test, not an instruction to defeat the nearby monsters.'])
m('bastok','1-3','Fetichism',
  'Accept the mission.|Collect one each of Fetich Head, Fetich Torso, Fetich Arms and Fetich Legs from Quadav. Palborough Mines is the standard hunting destination.|Trade all four pieces together to a Bastok mission guard.',
  [('Hunting area','Palborough Mines, entered from North Gustaberg (K-3)')],['You need four distinct parts, not four copies of one part.'])
m('bastok','2-1','The Crystal Line',
  'Accept the mission and speak with Cid in Metalworks (H-8).|Trade a synthesis crystal to a functioning crag Telepoint, such as the northern Telepoint at the Crag of Dem, to obtain a Faded Crystal.|Trade the Faded Crystal to Cid for the C. L. Report.|Speak with Ayame in the Metalworks Cannonry (K-7) to finish.',
  [('Dem Telepoint','Konschtat Highlands (I-6)'),('Ayame','Metalworks (K-7)')],['The Telepoint and Dimensional Portal are different targets.'])
m('bastok','2-2','Wading Beasts',
  'Accept the mission and obtain one Lizard Egg, from a lizard drop or an available seller.|Trade the egg to Alois in Metalworks (J-8).',
  [('Alois','Metalworks (J-8)')],['Optional for rank progression. The egg need not come specifically from Dangruf Wadi.'])
m('bastok','2-3','The Emissary',
  'Accept the mission and speak with Naji for the presidential briefing and Letter to the Consuls. This route visits San d’Oria first.|At the Bastok consulate in Northern San d’Oria (K-10), speak with Baraka and Helaku, then Halver in the Chateau.|Defeat Warchief Vatgit in Ghelsba Outpost and report to Helaku.|Meet Melek at the Bastok consulate in Port Windurst (F-6), then Kupipi in Heavens Tower for the Dark Key.|Reach Balga’s Dais through Giddeus. Win The Rank 2 Final Mission against Searcher and Black Dragon.|Return to Melek for the report, then Naji in Bastok.',
  [('Helaku','Northern San d’Oria (K-10)'),('Melek','Port Windurst (F-6)')],['If you already chose Windurst first, use the alternate route in the reference. Its offering and final battlefield differ.'])
m('bastok','3-1','The Four Musketeers',
  'Accept the mission and speak with Iron Eater at the President’s Office in Metalworks (J-8).|Enter Beadeaux for the scene. Defeat 20 Copper Quadav there while the mission is active.|Leave through the Pashhow Marshlands zone line and see the completion scene with Ayame.',
  [('Objective','20 Copper Quadav in Beadeaux')],['If the completion scene does not play, check the kill requirement. Use the ordinary exit rather than relying on a teleport to trigger it.'])
m('bastok','3-2','To the Forsaken Mines',
  'Accept the mission, prepare Hare Meat and speak with Davyad in Bastok Mines (K-6).|Go to the ??? at Gusgen Mines (J-7). Trade the meat to summon Blind Moby.|Defeat it and obtain a Glocolite for each player needing the mission.|Trade your Glocolite to Rashid in Bastok Mines (H-10).',
  [('Blind Moby trigger','Gusgen Mines (J-7)'),('Rashid','Bastok Mines (H-10)')],['Optional for rank progression. Bring a meat for each additional spawn you need.'])
m('bastok','3-3','Jeuno',
  'Accept the mission and speak with Lucius in Metalworks (J-9) for the letter.|Meet Goggehn at the Bastok embassy in Ru’Lude Gardens (H-10).|Reach Delkfutt’s Tower basement. If needed, defeat Porphyrion on floor 10 for the Delkfutt Key and use the elevator route.|Examine the basement door at (L-9), trading the physical key if needed, for the ambassador scene.|Return to the Bastok embassy’s office door for completion.',
  [('Ambassador door','Lower Delkfutt’s Tower basement (L-9)')],['The first-floor cermet door at E-8 is the shortcut for characters with the appropriate key access.'])
magicite('bastok')
m('bastok','5-1','Darkness Rising',
  'Speak with Naji for the presidential briefing and New Fei’Yin Seal.|Travel through Beaucedine Glacier to Fei’Yin, then Qu’Bia Arena at (K-8).|Enter The Rank 5 Mission. Defeat Archlich Taber’quoan while controlling its skeleton allies.|Receive the Burnt Seal and return to Naji.',
  [('Arena entrance','Fei’Yin (K-8)')],['Obtain the seal before travelling. The classic fight is level 50 capped; confirm the actual Zenith entry restriction.'])
m('bastok','5-2','Xarcabard, Land of Truths',
  'Accept the mission and enter the President’s Office for Karst’s briefing.|Travel through Xarcabard and Castle Zvahl to the Throne Room.|Enter the Shadow Lord battle. Switch between physical and magical damage as phase-one immunities change.|Defeat the second phase while keeping the party healed through area attacks.|Return to President Karst for the promotion.',
  [('Battlefield','Throne Room, through Castle Zvahl Keep')],['Bring both physical and magical damage options.'])
m('bastok','6-1','Return of the Talekeeper',
  'Accept the mission. Meet Medicine Eagle in Bastok Mines (H-6), then Drake Fang near the boat in Zeruhn Mines (H-6).|Examine the ??? among glowing rocks in Western Altepa Desert (G-8) to summon Western Sphinx and Eastern Sphinx.|Defeat the enemies and examine the ??? again for the Altepa Moonpebble.|Report to Tall Mountain in Bastok Mines (J-7).',
  [('Sphinx trigger','Western Altepa Desert (G-8)'),('Tall Mountain','Bastok Mines (J-7)')],['Collect the Moonpebble before leaving the area.'])
m('bastok','6-2',"The Pirates' Cove",
  'Accept the mission and speak with Naji. Visit Gilgamesh in Norg until he briefs you about Frag Rocks.|Prepare Adaman Ore. Enter Ifrit’s Cauldron from Yhoator Jungle (I-5) and reach the lava ??? on map 1 (H-7).|Trade the ore to summon Magma and Salamander. Defeat Magma and obtain a Frag Rock; prepare for the other enemy as well.|Trade your Frag Rock to Gilgamesh, then return to Naji.',
  [('Magma trigger','Ifrit’s Cauldron map 1 (H-7)')],['The Norg introductory Zilart scene may be needed to access Gilgamesh’s room. Each player needs a Frag Rock.'])
m('bastok','7-1','The Final Image',
  'Accept the mission and speak with Cid.|Search Ro’Maeve for the mission ???. Possible squares include D-10, E-9, E-10, G-9, I-8, K-10, K-11, L-10 and L-7.|Examine it and defeat the two Mokkurkalfi golems.|Find and examine the ??? again for Reinforced Cermet, then return to Cid.',
  [('Mission trigger','Ro’Maeve; changing ??? position')],['Nearby enemies can detect magic. The ??? may move; obtain the key item before zoning.'])
m('bastok','7-2','On My Way',
  'Accept the mission and speak with Karst, then Hilda at the Steaming Sheep in Port Bastok (E-6).|Reach Waughroon Shrine through Palborough Mines and enter On My Way.|Defeat Sa’Nha Soulsaver, Go’Bha Slaughterer, Ku’Jhu Graniteskin and Da’Shu Knightslayer. Crowd control helps; separate the White Mage to keep Benediction from waking the group.|Return to Karst after obtaining the Letter from Werei.|Speak with Gumbah in Bastok Mines (J-7) for the closing scene.',
  [('Hilda','Port Bastok (E-6)'),('Battlefield','Waughroon Shrine')])
m('bastok','8-1','The Chains That Bind Us',
  'Accept the mission and speak with Iron Eater.|Enter Quicksand Caves from Western Altepa Desert (G-5). Pass the weighted door at (H-8) and inspect the Galka Statue at (G-11).|Defeat the three Antica, then examine the statue again.|Use the separate Western Altepa entrance at (D-12), reached through C-11 / D-11. Pass the eastern weighted doors toward map 6.|Examine the ??? before the mural at map 6 (H-8), then return to Iron Eater.',
  [('First objective','Quicksand Caves, Galka Statue (G-11)'),('Second objective','Quicksand Caves map 6 (H-8)')],['Arrange enough player weight to open the doors; do not assume Trusts operate the sensors.'])
m('bastok','8-2','Enter the Talekeeper',
  'Accept the mission and visit Drake Fang in Zeruhn Mines (H-6).|Enter Kuftal Tunnel from Western Altepa Desert. Examine the upper ??? at (H-8) for the falling-wood message.|Reach the lower room beneath it and inspect the second ??? to summon Dervo’s, Gizerl’s and Gordov’s Ghosts.|Defeat the mission enemies and inspect the lower ??? for the Old Piece of Wood.|Return to Drake Fang.',
  [('Wood triggers','Kuftal Tunnel (H-8), upper and lower levels')],['Every player needs the upper trigger. The route here does not depend on despawn tricks.'])
m('bastok','9-1','The Salt of the Earth',
  'Accept the mission. Speak with Alois in Metalworks (J-8), then Dancing Wolf in Rabao (G-7).|At Gustav Tunnel map 2 (G-6), examine the pond ??? to summon Gigaplasm.|Defeat the splitting family: Gigaplasm becomes Macroplasms, then Microplasms and Nanoplasms. Finish one branch while controlling the others.|After all are defeated, examine the ??? for Miraclesalt.|Return to Dancing Wolf, then Alois.',
  [('Gigaplasm trigger','Gustav Tunnel map 2 (G-6)')],['Bring crowd control and magic damage. Avoid leaving all split enemies active at once.'])
m('bastok','9-2','Where Two Paths Converge',
  'Accept the mission and speak with Iron Eater in Metalworks (J-8).|Reach Castle Zvahl’s Throne Room and enter Where Two Paths Converge.|Fight Zeid through the first phase. After the scene, Volker joins; keep him alive or the battle fails.|Manage Zeid’s Shadow of Rage summons and finish Zeid.|Return to Iron Eater for the final scene and Rank 10 rewards.',
  [('Final battlefield','Throne Room')],['Bring healing for Volker. Enemy area attacks can inflict Sleep.'])

m('windurst','1-1','The Horutoto Ruins Experiment',
  'Accept the mission from a Windurst guard, then meet Hakkuru-Rinkuru at the Orastery in Port Windurst (E-7).|Enter Lily Tower in East Sarutabaruta (J-7). In Inner Horutoto Ruins, pass the cracked wall at (H-9) and examine the Gate: Magical Gizmo at (I-10).|Search the six Ancient Magical Gizmos at G-8, G-9, H-8, H-9, I-8 and I-9 until you obtain the Cracked Mana Orb.|Return to Hakkuru-Rinkuru.',
  [('Hakkuru-Rinkuru','Port Windurst (E-7)'),('Lily Tower','East Sarutabaruta (J-7)')],required='Windurst allegiance and Rank 1. Accept the mission before visiting the Orastery.')
m('windurst','1-2','The Heart of the Matter',
  'Accept the mission and meet Apururu in the Windurst Woods Manustery (H-9) for six Dark Mana Orbs.|Speak with Pore-Ohre outside Marguerite Tower in East Sarutabaruta (J-11) for the Southeastern Star Charm, then enter.|Put the orbs into all six Ancient Magical Gizmos, including the two side rooms.|Pass the eastern cracked wall and examine the Gate: Magical Gizmo to charge them.|Revisit all six gizmos to retrieve the Glowing Mana Orbs.|Leave for East Sarutabaruta, then report to Apururu.',
  [('Apururu','Windurst Woods (H-9)'),('Pore-Ohre / tower','East Sarutabaruta (J-11)')],['If the gate will not open, check that you spoke with Pore-Ohre. Collect every charged orb before leaving.'])
m('windurst','1-3','The Price of Peace',
  'Accept the mission and speak with Leepe-Hoppe on the Rhinostery roof in Windurst Waters (J-9) for the food and drink offerings.|Enter Giddeus from West Sarutabaruta (F-8). Deliver the food to Laa Mozi at (H-7) and the drink to Ghoo Pakya at (G-7).|Return to the Rhinostery roof for the scene.|Report to a Windurst mission guard.',
  [('Leepe-Hoppe','Windurst Waters (J-9), roof'),('Offerings','Giddeus: Laa Mozi (H-7), Ghoo Pakya (G-7)')])
m('windurst','2-1','Lost for Words',
  'Accept the mission. Speak with Tosuka-Porika at the Optistery in northern Windurst Waters (G-8), then Nanaa Mihgo in Windurst Woods (J-3).|Enter the Maze of Shakhrami from Tahrongi Canyon (K-5). Take the upper-map (G-6) passage to the lower map and search Fossil Rocks for Lapis Coral.|Return to Nanaa Mihgo for the Hideout Key.|Enter Lily Tower in East Sarutabaruta (J-7). Follow Inner Horutoto’s cracked wall (G-9) into Beetles Burrow and examine the Mahogany Door at (G-8).|Visit the House of the Hero in Windurst Walls (G-3), then return to Tosuka-Porika.',
  [('Nanaa Mihgo','Windurst Woods (J-3)'),('Mahogany Door','Inner Horutoto Ruins, Beetles Burrow (G-8)')])
m('windurst','2-2','A Testing Time',
  'Accept this optional mission and speak with Moreno-Toeno at the Aurastery in northern Windurst Waters (L-6). Note the game time when receiving the Creature Counter.|For the first assignment, defeat at least 30 monsters in Tahrongi Canyon during the assigned 24 Vana’diel hours.|Return to Moreno-Toeno in the final game hour of that window and report.',
  [('Moreno-Toeno','Windurst Waters (L-6)'),('First assignment','Tahrongi Canyon')],['This is timed: an early visit does not complete the test, and a late report fails. Follow the deadline in the NPC dialogue. Repeat assignments use Buburimu Peninsula and a longer window.','Optional for rank progression when sufficient Rank Points unlock 2-3.'])
m('windurst','2-3','The Three Kingdoms',
  'Accept the mission and obtain the letter from Kupipi in Heavens Tower. This route visits Bastok first.|Meet Patt-Pott in Metalworks (I-7), Pius (J-8), then Grohm (H-9).|Mine Gravel in Palborough Mines. Feed it into the third-floor refiner (I-6), pull its lever, and collect Mythril Sand from the lever below. Trade the sand to Patt-Pott and speak again.|Meet Kasaroro in Northern San d’Oria (H-9), then Halver in the Chateau.|Reach Horlais Peak through Ghelsba, Fort Ghelsba and Yughott Grotto. Defeat Spotter and Dread Dragon in The Rank 2 Final Mission.|Report to Kasaroro, then return to Kupipi.',
  [('Bastok consul','Metalworks (I-7)'),('San d’Oria consul','Northern San d’Oria (H-9)')],['This is the Bastok-first route. If San d’Oria was your first destination, the alternate route requires Vatgit and later the Waughroon Shrine battle; follow the reference for that branch.'])
m('windurst','3-1','To Each His Own Right',
  'Accept the mission, speak with Kupipi for the Starway Stairway Bauble, then meet Rhy Epocan upstairs in Heavens Tower.|Speak with Hakkuru-Rinkuru at the Port Windurst Orastery (E-7).|Reach the lever door on Castle Oztroja’s first map (I-8). Personally operate the trap lever and fall for the mission scene.|Return to Rhy Epocan.',
  [('Trap door','Castle Oztroja, first map (I-8)')],['Another player triggering the fall does not substitute for your own mission interaction.'])
m('windurst','3-2','Written in the Stars',
  'Accept the mission and speak with Zubaba on Heavens Tower’s second floor for the Charm of Light.|Enter Inner Horutoto through Lily Tower, pass Beetles Burrow (D-10), and reach the Three Mage Gate in Rose Tower (H-9).|Use the gate with White Mage, Red Mage and Black Mage assistance, or your existing Portal Charm. An unlocked Toraimarai Canal route is another approach.|Examine the Gate of Light on Rose Tower map 2 (G-7).|Return to Zubaba.',
  [('Three Mage Gate','Inner Horutoto, Rose Tower (H-9)'),('Gate of Light','Rose Tower map 2 (G-7)')],['After the first completion, trading a Rolanberry to Kupipi obtains a Portal Charm.','Optional for rank progression. Repeat or later-rank variants request three Rusty Daggers instead; follow Zubaba’s current assignment.'])
m('windurst','3-3','A New Journey',
  'Accept the mission for the Star-crested Summons. Visit the Vestal Chamber atop Heavens Tower and receive the ambassador’s letter.|Meet Pakh Jatalfih at the Windurst embassy in Ru’Lude Gardens (I-9).|Climb Delkfutt’s Tower and obtain a Delkfutt Key from Porphyrion on floor 10 if needed. Use the elevator route to the basement.|Examine the Windurst ambassador’s basement door at (L-7); trade the physical key if necessary.|Return to Pakh Jatalfih and examine the embassy office door.',
  [('Embassy','Ru’Lude Gardens (I-9)'),('Ambassador door','Lower Delkfutt’s Tower basement (L-7)')],['Each nation has a different basement door.'])
magicite('windurst')
m('windurst','5-1','The Final Seal',
  'Visit the Vestal Chamber atop Heavens Tower to receive the New Fei’Yin Seal.|Enter Fei’Yin from Beaucedine Glacier (J-4) and continue to Qu’Bia Arena at Fei’Yin (K-8).|Enter The Rank 5 Mission. Defeat Archlich Taber’quoan while managing its skeleton helpers.|Return to the Vestal Chamber with the Burnt Seal.',
  [('Arena entrance','Fei’Yin (K-8)')],['Bring the New Fei’Yin Seal. The classic battlefield is level 50 capped; check Zenith’s entry message.'],start='Vestal Chamber, Heavens Tower')
m('windurst','5-2','The Shadow Awaits',
  'Accept the mission and visit the Vestal Chamber.|Travel through Xarcabard, Castle Zvahl Baileys and Castle Zvahl Keep to the Throne Room.|Enter the Shadow Lord battle. In phase one, switch physical and magical damage as his immunities change; phase two requires sustained healing through area damage.|After victory, enter Heavens Tower for the scene and visit the Vestal Chamber.',
  [('Battlefield','Throne Room, through Castle Zvahl Keep')],['Bring both physical and magical damage options.'])
m('windurst','6-1','Full Moon Fountain',
  'Accept the mission and meet Hakkuru-Rinkuru in Port Windurst (E-7) for the Southwestern Star Charm.|Enter Dahlia Tower in West Sarutabaruta (F-11). At Outer Horutoto Ruins (J-8), examine the Gate: Magical Gizmo to summon four Jack Cardians.|Defeat the Cardians, then examine the gate again.|Enter Full Moon Fountain through Toraimarai Canal for the completion scene.',
  [('Dahlia Tower','West Sarutabaruta (F-11)'),('Cardian trigger','Outer Horutoto Ruins (J-8)')],['Prepare for Black Mage, Red Mage, White Mage and Paladin enemies. Plan your Canal access before travelling.'])
m('windurst','6-2','Saintly Invitation',
  'Accept the mission and visit the Vestal Chamber for the Holy One’s Invitation.|Enter Saintly Invitation at Balga’s Dais. Defeat all four Yagudo for the Balga Champion Certificate.|Obtain a Judgment Key from Yagudo Flagellants and climb Castle Oztroja through its password route.|Trade the key to the second Brass Door at (H-5). Speak with Kaa Toru the Just beyond it for the oath and Ashura Necklace.|Return to the Vestal Chamber.',
  [('Battlefield','Balga’s Dais'),('Kaa Toru the Just','Castle Oztroja, beyond second Brass Door (H-5)')],['The key door closes quickly. Gather the party before opening it. Prepare for Summoner, Ninja, Samurai and White Mage enemies.'])
RECORDS[-1]['reward']='Rank 7; 40,000 gil; Ashura Necklace'
m('windurst','7-1','The Sixth Ministry',
  'Accept the mission. Speak with Tosuka-Porika at the Optistery in northern Windurst Waters (G-8) for the Optistery Ring.|In Toraimarai Canal map 2 (G-8), defeat the four Hinge Oils.|Go up the stairs at (H-8) and examine the Marble Door.|Inside the laboratory, examine the Tome of Magic by the desk.|Return to Tosuka-Porika for the Book of the Gods.',
  [('Hinge Oils','Toraimarai Canal map 2 (G-8)'),('Laboratory','Marble Door, map 2 (H-8)')])
m('windurst','7-2','Awakening of the Gods',
  'Accept the mission and speak with Leepe-Hoppe on the Rhinostery roof in southern Windurst Waters (J-9), then Kerutoto below.|Meet Romaa Mihgo in Kazham (H-11).|Defeat Bonze Marberry at Temple of Uggalepih map 3 (J-9) for a Cursed Key.|Trade the key to the Granite Door on map 3 (J-6).|Return to Leepe-Hoppe.',
  [('Bonze Marberry','Temple of Uggalepih map 3 (J-9)'),('Granite Door','Temple of Uggalepih map 3 (J-6)')],['Each player needs a Cursed Key. Tonberry hate can make Everyone’s Rancor dangerous.','Kerutoto may have another quest scene waiting; make sure you receive this mission’s dialogue.'])
m('windurst','8-1','Vain',
  'Accept the mission and speak with Moreno-Toeno in northern Windurst Waters (L-6) for the Star Seeker.|Examine Qu’Hau Spring in Ro’Maeve (H-6).|Meet Sedal-Godjal on Davoi’s upper ledge (J-8), reached through Monastic Cavern via the (H-11) entrance and (I-8) exit.|Defeat Dirtyhanded Gochakzuk in central Davoi (H-8) for a Curse Wand.|Trade the wand to Sedal-Godjal, then return to Moreno-Toeno.',
  [('Qu’Hau Spring','Ro’Maeve (H-6)'),('Sedal-Godjal','Davoi (J-8), raised ledge'),('Curse Wand','Davoi (H-8)')])
m('windurst','8-2',"The Jester Who'd Be King",
  'Accept the mission. Meet Apururu in Windurst Woods (H-9) for the Manustery Ring.|Collect three rings: Rukususu behind Fei’Yin map 2’s Cermet Door (F-6), Sedal-Godjal at Davoi (J-8), and Tosuka-Porika at Windurst Waters (G-8).|Return to Apururu, then speak with Kupipi.|Enter Amaryllis Tower in West Sarutabaruta (F-4). Pass Outer Horutoto’s cracked wall (I-6); examine the next map’s cracked wall (G-8) to summon Queen of Coins and Queen of Swords.|Defeat both, then recheck the wall for the Orastery Ring.|Speak with Apururu, Shantotto in Windurst Walls (K-7), then Apururu again.|Reach the Gate of Darkness in Inner Horutoto’s Rose Tower map 2 (I-7) through the Three Mage Gate or Canal route. Examine it, then return to Apururu.',
  [('Cardian trigger','Outer Horutoto Ruins, beyond Amaryllis Tower (G-8)'),('Gate of Darkness','Inner Horutoto Ruins, Rose Tower map 2 (I-7)')])
m('windurst','9-1','Doll of the Dead',
  'Accept the mission and speak with Apururu. Enter Heavens Tower, visit the Vestal Chamber, then return to Apururu.|Obtain Goobbue Humus from Old Goobbue in the Boyahda Tree or Goobbue Gardener in the Sanctuary of Zi’Tah.|Trade the humus to the lone Mandragora Warden in the Boyahda Tree’s western (F-4) area for the Letter from Zonpa-Zippa.|Return to Apururu.|Enter Full Moon Fountain from Toraimarai Canal (G-7) for the final scene.',
  [('Mandragora Warden','The Boyahda Tree (F-4), lone warden'),('Final scene','Full Moon Fountain')],['Use the solitary Mandragora Warden, not the nearby pair.'])
m('windurst','9-2','Moon Reading',
  'Accept the mission and visit the Vestal Chamber.|Collect the three verses in any order: Qu’Hau Spring in Ro’Maeve (H-6), the Chamber of Oracles reached through Quicksand Caves from Western Altepa (D-12), and the Temple of Uggalepih room at map 2 (E-8), using an Uggalepih Key.|Return to the Vestal Chamber.|Enter Moon Reading at Full Moon Fountain. Defeat all four Ace Cardians in the first stage.|In the second stage, defeat Tatzlwurm and Yali while keeping Ajido-Marujido alive.|Return to the Vestal Chamber and examine it again as needed for both closing scenes and Rank 10.',
  [('Final battlefield','Full Moon Fountain'),('Temple verse','Temple of Uggalepih map 2 (E-8)')],['Prepare weighted-door access for Quicksand Caves and healing for Ajido-Marujido.'])
