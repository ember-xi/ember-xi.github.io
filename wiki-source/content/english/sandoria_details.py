"""Original mission instructions checked against the pinned native Lua state machines.

Inventory items use the shared native acquisition importer. Key-item records below
describe the actual event which awards them; they are never advertised as AH stock.
"""
from html import escape
from pathlib import Path
import json, re, runpy

REV = 'f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4'
BASE = 'https://github.com/LandSandBoat/server/blob/' + REV + '/'
GUARDS = 'Grilau — Northern San d’Oria (C-8); Endracion — Southern San d’Oria (F-9); Ambrotien — Southern San d’Oria (K-10)'

# Items which occupy inventory slots, as opposed to the Key Items menu.
PHYSICAL = {'Orcish Axe':16656,'Orcish Mail Scales':1112,'Bat Fang':891,
 'Bronze Sword':16535,'Pickaxe':605,'Mine Gravel':597,'Mythril Sand':599,
 'Parana Shield':12298,'Crystal Bass':4528,'Delkfutt Key':549,
 'Coeurl Meat':4377,'Quadav Charm':495,'Quadav Augury Shell':494,
 'Tenshodo Invite':548,'Prelate Key':1137,'San d’Orian Flag':181}

# name: (mission, award/source, purpose)
KEY_ITEMS = {
 'Orcish Hut Key':('1-3','Win Save the Children at the Hut Door, Ghelsba Outpost (F-10).','Examine the Hut Door again after winning to rescue the children. The key is consumed by the rescue scene.'),
 'Rescue Training Certificate':('2-1','After returning the Bronze Sword to Ruillont, speak to Vicorpasse at La Theine Plateau (F-6).','Return to a San d’Oria mission guard to finish The Rescue Drill.'),
 'Lost Document':('2-2','Speak to Zantaviat, then examine the ! beside the pond at Davoi (J-8).','Speak to Zantaviat again to exchange this document for the Temple Knights’ Davoi Report.'),
 'Temple Knights’ Davoi Report':('2-2','Zantaviat near Davoi’s entrance exchanges the Lost Document for this report.','Carry it back to a mission guard, then complete the cathedral scene.'),
 'Letter to the Consuls':('2-3','Halver in Chateau d’Oraguille (I-9), after accepting Journey Abroad.','Introduce yourself at the San d’Oria consulate in either Bastok or Windurst. The first city determines your route.'),
 'Shield Offering':('2-3','Kupipi in Heavens Tower, entered from Windurst Walls (H-7), on the Windurst-first route.','Speak to Uu Zhoumo in Giddeus, map 2 (F-7), to deliver the offering. This is separate from the two Parana Shields for Mourices.'),
 'Dark Key':('2-3','Kupipi grants it on the Windurst-second route after Mourices sends you to Heavens Tower.','Used for the Balga’s Dais leg of Journey Abroad; the post-battle scene removes it.'),
 'Kindred Crest':('2-3','Win The Rank 2 Final Mission in your second destination city.','Report to that city’s San d’Oria consul to receive the Kindred Report.'),
 'Kindred Report':('2-3','Mourices or Savae E Paleade exchanges the Kindred Crest after your dragon battle.','Speak to Halver in Chateau d’Oraguille (I-9) to finish Journey Abroad.'),
 'Adventurer’s Certificate':('2-3','Complete Journey Abroad by reporting to Halver.','Permanent proof of the completed mission; it is a key-item reward, not an inventory trade.'),
 'Royal Knights’ Davoi Report':('3-1','Quemaricond, patrolling around Davoi (H-7), during the first Infiltrate Davoi run.','Return to the Prince Royal’s room in Chateau d’Oraguille.'),
 'East Block Code':('3-1','On a repeat run, speak to Zantaviat and inspect the ! at Davoi (K-7).','Collect the other two block codes and return to Zantaviat.'),
 'South Block Code':('3-1','On a repeat run, speak to Zantaviat and inspect the ! at Davoi (L-8).','Collect the other two block codes and return to Zantaviat.'),
 'North Block Code':('3-1','On a repeat run, speak to Zantaviat and inspect the ! at Davoi (J-7).','Collect the other two block codes and return to Zantaviat.'),
 'Letter to the Ambassador':('3-3','Speak to Halver and examine the Great Hall door after accepting Appointment to Jeuno.','Begin the embassy and Delkfutt’s Tower rescue route.'),
 'Delkfutt Key (key item)':('3-3','Use the physical Delkfutt Key at the San d’Oria Cermet Door in the basement, Lower Delkfutt’s Tower (M-8).','The reviewed mission script grants this permanent key during the ambassador rescue. A future visit can use the key item at the door.'),
 'Archducal Audience Permit':('4-1','Accept Magicite at the San d’Oria embassy’s rear door in Ru’Lude Gardens.','Examine the Audience Chamber at Ru’Lude Gardens (H-6).'),
 'Letter to Aldo':('4-1','Receive the opening Magicite scene at the Audience Chamber, Ru’Lude Gardens (H-6).','Speak to Aldo inside the Tenshodo headquarters, Lower Jeuno (J-8).'),
 'Silver Bell':('4-1','Aldo grants it when you deliver the Letter to Aldo.','Enables the Crest of Davoi and Mysteries of Beadeaux prerequisite quests. Keep it; a previous nation’s copy also qualifies.'),
 'Tenshodo Application Form':('4-1','After asking Ghebi Damomohe about membership, speak to Jabbar or Silver Owl in Warehouse #2, Port Bastok (F-6).','Return to Ghebi Damomohe in Lower Jeuno (I-7). This is the application route to Tenshodo Membership.'),
 'Tenshodo Member’s Card':('4-1','Complete Tenshodo Membership with Ghebi Damomohe in Lower Jeuno (I-7).','Permanent access to the Tenshodo headquarters behind Neptune’s Spire. You do not trade away this card to Aldo.'),
 'Crest of Davoi':('4-1','Accept Baudin’s request in Upper Jeuno (G-8) after obtaining the Silver Bell. Trade him one Coeurl Meat.','Opens the Wall of Dark Arts at Davoi (G-7), leading to the Optistone.'),
 'Yagudo Torch':('4-1','After Aldo, speak to Paya-Sabya in Upper Jeuno (I-8), then Muckvix in Lower Jeuno (H-10).','Light the torch by the sealed door on the Castle Oztroja Magicite route.'),
 'Coruscant Rosary':('4-1','Accept Mysteries of Beadeaux I from Sattal-Mansal, then trade him one Quadav Charm.','One of the Beadeaux access key items needed for the sealed Magicite route.'),
 'Black Matinee Necklace':('4-1','Accept the Beadeaux requests from Sattal-Mansal, then trade him one Quadav Augury Shell.','The second Beadeaux access key item. Both exchanges take place in Lower Jeuno (J-8).'),
 'Magicite: Optistone':('4-1','Pass Davoi’s Wall of Dark Arts at (G-7), enter Monastic Cavern and examine Magicite.','Collect all three Magicites before returning to the Audience Chamber in Ru’Lude Gardens.'),
 'Magicite: Orastone':('4-1','Follow the Castle Oztroja torch-door route into the Altar Room, then examine Magicite.','Collect all three Magicites before returning to the Audience Chamber in Ru’Lude Gardens.'),
 'Magicite: Aurastone':('4-1','Obtain both Beadeaux access key items, enter Qulun Dome via Beadeaux’s underground route, then examine Magicite.','Collect all three Magicites before returning to the Audience Chamber in Ru’Lude Gardens.'),
 'Airship Pass':('4-1','Return all three Magicites to the Audience Chamber in Ru’Lude Gardens.','Access to the airships between Jeuno and the three starting nations. It is different from the Kazham Airship Pass. If already owned, the reviewed mission awards 20,000 gil instead of another pass.'),
 'Message to Jeuno':('4-1','Finish Magicite by reporting to Nelcabrit at the San d’Oria embassy in Ru’Lude Gardens.','Story letter carried into the next San d’Oria mission, The Ruins of Fei’Yin.'),
 'New Fei’Yin Seal':('5-1','Halver grants it after you have accepted The Ruins of Fei’Yin and completed his briefing.','Required for the mission route to the Burning Circle in Qu’Bia Arena.'),
 'Burnt Seal':('5-1','Win The Rank 5 Mission against Archlich Taber’quoan and finish the battlefield exit scene.','Return to Halver to finish The Ruins of Fei’Yin.'),
 'Shadow Fragment':('5-2','Defeat the Shadow Lord and finish the Throne Room victory scene.','Return to Halver for Rank 6; the fragment is removed when the mission completes.'),
 'Dreamrose':('6-1','Examine the Dreamrose flowers at Western Altepa Desert (G-7), defeat Sabotender Enamorado, then examine the flowers again.','Return to Halver. The NM kill alone does not put the Dreamrose in your key items.'),
 'Piece of Paper':('6-1','Complete the Chateau garden scene after delivering the Dreamrose.','Story item for Ranperre’s Final Rest; exchanged when you obtain the Ancient San d’Orian Book.'),
 'Ancient San d’Orian Book':('6-2','After the three Corrupted skeletons, enter the Heavy Stone Door at King Ranperre’s Tomb (H-8) and inspect the Tombstone inside.','Return to a mission guard, change zones, and speak to the guard again before visiting Trion.'),
 'Ancient San d’Orian Tablet':('7-1','Defeat Marauder Dvogzog on the raised West Ronfaure ledge (E-8), then examine the ??? again.','Take it back to the Papal Chamber at Northern San d’Oria’s cathedral.'),
 'Crystal Dowser':('7-2','Received during The Secret Weapon victory scene; Rahal grants the quest copy again during Lightbringer.','For Lightbringer, you must speak to Rahal after the Great Hall scene even if you remember receiving this item earlier.'),
 'Drops of Amnio':('8-1','Examine the Fountain of Kings at Quicksand Caves, map 2 (G-14), after defeating Honor and Valor.','Return to Halver, then wait one real minute and re-enter Northern San d’Oria for the required closing scene.'),
 'Piece of a Broken Key 1':('8-2','Examine one of the three key-fragment ??? points behind the side doors in Temple of Uggalepih, map 4 (G/H-10), after Rahal’s briefing.','Collect all three distinct fragments on each character; they unlock the Nio-A and Nio-Hum mission-door event.'),
 'Piece of a Broken Key 2':('8-2','Examine another key-fragment ??? behind the side doors in Temple of Uggalepih, map 4 (G/H-10).','You need all three distinct fragments. Repeatedly checking one ??? does not provide the other pieces.'),
 'Piece of a Broken Key 3':('8-2','Examine the remaining key-fragment ??? behind the side doors in Temple of Uggalepih, map 4 (G/H-10).','After the Nio fight, examine the second door from the west again; the scene consumes all three fragments.'),
 'Figure of Titan':('9-1','After the Great Hall briefing, examine the ??? at Valley of Sorrows (I-8).','First figure. Obtain this before trying to collect the Figure of Garuda.'),
 'Figure of Garuda':('9-1','With the Figure of Titan, examine the ??? at Xarcabard (H-7).','Second figure. Carry both to the isolated Batallia Downs island for the final NM encounter.'),
 'Figure of Leviathan':('9-1','Defeat Suparna and Suparna Fledgling by the monument on the isolated Batallia Downs island, then examine the ??? again.','Third figure. Return to the Great Hall with all three to finish Breaking Barriers.'),
}

DETAILS = {}
def mission(num,carry,stages,notes=()):
    DETAILS[num]={'carry':carry,'stages':stages,'notes':notes}

mission('1-1',['Orcish Axe'],[
 ('Accept the assignment', ['Speak to Grilau (C-8) in Northern San d’Oria, or one of the two Southern San d’Oria mission guards. Choose Smash the Orcish Scouts. Check that it appears under Missions → San d’Oria.']),
 ('Get the axe', ['Leave through a city gate into West Ronfaure or East Ronfaure. Hunt Orcish Fodder until one Orcish Axe drops. Open its item page below for documented spawn squares.','Keep the axe in your ordinary inventory. It is a mission trade, not an automatically counted kill.']),
 ('Turn it in', ['Return to a San d’Oria mission guard and trade exactly one Orcish Axe. You receive Rank Points; this mission itself does not promote you to Rank 2.'])],['Repeatable. On a repeat, accept the mission again before trading another axe.'])
mission('1-2',['Orcish Mail Scales','Bat Fang'],[
 ('Reach the tomb', ['Accept Bat Hunt from a mission guard. Travel south through East Ronfaure to the King Ranperre’s Tomb entrance at (H-11).','On the first tomb map, reach the Tombstone around (H/I-10) and examine it for the mission scene.']),
 ('First completion', ['Hunt Ding Bats in the tomb at night, 18:00–06:00 Vana’diel time, until Orcish Mail Scales drop. Keep one set in inventory.','Return to a mission guard and trade one Orcish Mail Scales.']),
 ('Repeating the mission', ['Accept Bat Hunt again and revisit the Tombstone. For a repeat completion, the required trade is one Bat Fang instead of Orcish Mail Scales.'])],['Avoid the tomb’s ghost enemies at low level. The Tombstone event is a separate requirement from obtaining the drop.'])
mission('1-3',['Orcish Hut Key'],[
 ('Get the briefing', ['Accept Save the Children. Speak to Arnau at the cathedral altar in Northern San d’Oria (M-6).']),
 ('Enter the rescue battle', ['Enter Ghelsba Outpost from West Ronfaure (E-4), then find the Hut Door at Ghelsba Outpost (F-10).','Examine the Hut Door and choose Save the Children. Defeat the three Orc enemies and finish the victory scene. You receive the Orcish Hut Key.']),
 ('Rescue and report', ['Examine the Hut Door again after leaving the battlefield. This uses the key and plays the rescue scene; simply winning is not enough.','Return to a San d’Oria mission guard for Rank 2 and 1,000 gil. You can revisit Arnau for the follow-up dialogue.'])])
mission('2-1',['Bronze Sword','Rescue Training Certificate'],[
 ('Find the missing trainee', ['Accept The Rescue Drill. Go to Galaihaurat in La Theine Plateau (E-6), then descend the ravine toward the Ordelle’s Caves entrance at (F-6).','Speak to Vicorpasse and the training party around the ravine. Enter Ordelle’s Caves and speak to Ruillont beside the pool at (G-3).']),
 ('Recover his sword', ['Return outside and speak to Deaufrain, Equesobillot and Galaihaurat. The mission chooses which of these three has the Bronze Sword for your run.','After the correct conversation, receive the Bronze Sword. Return inside and trade it to Ruillont. Buying a sword alone does not replace the required mission conversations.']),
 ('Finish the drill', ['Speak to Vicorpasse outside for the Rescue Training Certificate. Return to a San d’Oria mission guard to complete the mission.'])])
mission('2-2',['Lost Document','Temple Knights’ Davoi Report'],[
 ('Meet the scout', ['Accept The Davoi Report. From Jugner Forest (G-12), enter Davoi and speak to Zantaviat near the entrance.']),
 ('Find the missing page', ['Reach the pond at Davoi (J-8). Examine the ! on its southern side to obtain the Lost Document.','Return to Zantaviat. He replaces the document with the Temple Knights’ Davoi Report.']),
 ('Deliver the report', ['Speak to a San d’Oria mission guard with the report, then examine the Papal Chamber upstairs in the cathedral in Northern San d’Oria to finish the first-time story.'])],['This is optional for rank advancement if your Rank Points already unlock Journey Abroad.'])
mission('2-3',['Letter to the Consuls','Pickaxe','Mine Gravel','Mythril Sand','Shield Offering','Parana Shield','Dark Key','Kindred Crest','Kindred Report','Adventurer’s Certificate'],[
 ('Choose your first destination', ['Accept Journey Abroad, then speak to Halver in Chateau d’Oraguille (I-9) for the Letter to the Consuls.','You must visit both Bastok and Windurst. Follow ONE of the two routes below, according to the first consulate you visited. You only fight the dragon in the second nation.']),
 ('Route A — Bastok first', ['Go to Savae E Paleade in Metalworks (I-9), then Pius at (J-8), then Grohm at (H-9). Finish their conversations; Grohm supplies three Pickaxes.','Enter Palborough Mines from North Gustaberg. Trade a Pickaxe to a Mythril Seam, such as the first-floor seam at (I-8), until you obtain Mine Gravel. Pickaxes can break. Alternatively obtain the gravel from an actual AH listing.','At the third-floor refiner (I-6), trade one Mine Gravel to the input and operate the lever. Descend to the lower output lever and operate it to collect Mythril Sand.','Return to Savae E Paleade and trade one Mythril Sand. Then go to Mourices at Windurst Woods (F-10).','Speak to Kupipi inside Heavens Tower, entered from Windurst Walls (H-7), and receive the Dark Key. Travel through Giddeus to Balga’s Dais.','At the Burning Circle choose The Rank 2 Final Mission. Defeat Searcher and Black Dragon. Controlling the dragon while dealing with the eye first reduces simultaneous attacks.','After receiving the Kindred Crest, report to Mourices for the Kindred Report. Continue to the shared finish below.']),
 ('Route B — Windurst first', ['Speak to Mourices in Windurst Woods (F-10), then Kupipi in Heavens Tower for the Shield Offering.','Enter Giddeus from West Sarutabaruta. Give the offering to Uu Zhoumo by speaking to him on map 2 (F-7).','Defeat Zhuu Buxu the Silent on map 2 around (H-7) for a Parana Shield. You need two shields, so obtain a second drop after the NM respawns. These are separate inventory items from the Shield Offering.','Return to Mourices and trade both Parana Shields together. Travel to Savae E Paleade in Metalworks (I-9), then speak to Pius (J-8) and Grohm (H-9).','Go through Palborough Mines to Waughroon Shrine. Enter The Rank 2 Final Mission at the Burning Circle and defeat Seeker and Dark Dragon. The mining/refiner trade belongs to Route A, not this route.','Receive the Kindred Crest, then report to Savae E Paleade for the Kindred Report.']),
 ('Finish either route', ['Speak to Halver in Chateau d’Oraguille (I-9) with the Kindred Report. Receive Rank 3, 3,000 gil and the Adventurer’s Certificate.'])],['The classic dragon battle is level 25 capped. Use the entry conditions displayed by Zenith; another server’s Trust permissions and bonus inventory rewards are not included in this mission reward.'])
mission('3-1',['Royal Knights’ Davoi Report','East Block Code','South Block Code','North Block Code'],[
 ('First completion — Trion’s orders', ['Accept Infiltrate Davoi and examine Door: Prince Royal’s in Chateau d’Oraguille (G/H-7). This is Trion’s room.','Enter Davoi through Jugner Forest (G-12). Find the patrolling Quemaricond around Davoi (H-7) and speak to him for the Royal Knights’ Davoi Report.','Return to Door: Prince Royal’s and examine it to deliver the report and complete the mission.']),
 ('Repeat completion — block codes', ['Accept the repeat mission and speak to Zantaviat near Davoi’s entrance. Collect East Block Code at the ! in (K-7), South Block Code at (L-8), and North Block Code at (J-7).','Return to Zantaviat after collecting all three. Then report to a San d’Oria mission guard.'])])
mission('3-2',['Crystal Bass'],[
 ('Prepare the fish', ['Accept The Crystal Spring. You need one Crystal Bass; ordinary bass of another type will not work.','Obtain it from an actual Auction House listing under Fish, or fish at Jugner Forest’s Crystwater Spring (J-9). The item page explains the fishing source and equipment.']),
 ('Deliver and finish', ['Trade one Crystal Bass to a San d’Oria mission guard.','On your first completion, enter Chateau d’Oraguille for the scene and speak to Chalvatot in the garden (F-7). Repeat runs do not require these story scenes.'])],['Optional if your Rank Points already unlock Appointment to Jeuno.'])
mission('3-3',['Letter to the Ambassador','Delkfutt Key','Delkfutt Key (key item)'],[
 ('Get the letter', ['Accept Appointment to Jeuno, speak to Halver (I-9), and examine the Great Hall door in Chateau d’Oraguille. Receive the Letter to the Ambassador.','Go to the San d’Oria embassy in Ru’Lude Gardens and speak to Nelcabrit at (G-9).']),
 ('Reach the imprisoned ambassador', ['Enter Lower Delkfutt’s Tower from Qufim Island (F-6). If this is your first ascent, follow the tower’s stairs and teleporters through the middle and upper tower to floor 10.','Defeat Porphyrion on floor 10 and collect a physical Delkfutt Key. Make sure every player who needs one receives a key.','Use the key at the tower’s elevator route and descend to the basement. At the San d’Oria Cermet Door in Lower Delkfutt’s Tower basement (M-8), trade the physical key for the rescue scene. If you already hold the permanent Delkfutt Key (key item), examine the door instead.']),
 ('Report in Jeuno', ['Return to the San d’Oria embassy and examine the ambassador’s office door at Ru’Lude Gardens (H-10). Receive Rank 4 and 5,000 gil.'])],['The embassy doors in Delkfutt’s basement differ by nation. For this mission use the San d’Oria door at (M-8).'])
mission('4-1',['Tenshodo Invite','Tenshodo Member’s Card','Archducal Audience Permit','Letter to Aldo','Silver Bell','Coeurl Meat','Crest of Davoi','Yagudo Torch','Quadav Charm','Quadav Augury Shell','Coruscant Rosary','Black Matinee Necklace','Magicite: Optistone','Magicite: Orastone','Magicite: Aurastone','Airship Pass','Message to Jeuno'],[
 ('1. Accept Magicite in Jeuno', ['Speak to Nelcabrit at the San d’Oria embassy in Ru’Lude Gardens (G-9). If it is unavailable, raise Rank Points through your Conquest guard.','Examine the embassy’s rear door to accept Magicite and receive the Archducal Audience Permit. Examine the Audience Chamber upstairs at (H-6) for the Letter to Aldo.']),
 ('2. Enter the Tenshodo headquarters', ['If you lack the Tenshodo Member’s Card, complete Tenshodo Membership first. Its linked page gives both the application route and the Tenshodo Invite trade route.','Inside Neptune’s Spire in Lower Jeuno, pass the headquarters door at (J-7) and speak to Aldo at (J-8). He exchanges the letter for the Silver Bell and advances the mission.']),
 ('3. Arrange every stronghold’s access', ['With the Silver Bell, speak to Baudin in Upper Jeuno (G-8), accept his request, and trade one Coeurl Meat for the Crest of Davoi.','Speak to Paya-Sabya in Upper Jeuno (I-8), then Muckvix in his Lower Jeuno shop (H-10) for the Yagudo Torch. A preliminary Muckvix conversation gives background; Paya-Sabya’s scene is the required flag in the reviewed mission.','Speak to Sattal-Mansal inside the Tenshodo headquarters at Lower Jeuno (J-8). His conversation accepts Mysteries of Beadeaux I and II together.']),
 ('4. Obtain the Beadeaux access items', ['Travel to Beadeaux through Pashhow Marshlands. Defeat De’Vyu Headhunter on the upper level around (I-9) for one Quadav Charm, and Go’Bhu Gascon on the upper level around (F-6) for one Quadav Augury Shell.','Return to Sattal-Mansal. Trade the Quadav Charm by itself for the Coruscant Rosary, then the Quadav Augury Shell by itself for the Black Matinee Necklace. Do not combine both in a single trade.']),
 ('5. Collect the three Magicites', ['Davoi: enter from Jugner Forest (G-12). Reach the Wall of Dark Arts at Davoi (G-7); examine it using your Crest of Davoi, then enter Monastic Cavern. Examine Magicite in the chamber for Magicite: Optistone.','Castle Oztroja: enter from Meriphataud Mountains (L-8). Operate the correct lever at the first Brass Door (I-8); the other lever opens the floor trap. Climb onto map 3, continue through (G-7) to the upper outside walkway, then go north without dropping down. Follow the passage to the torch door at map 2 (H-9).','Use the Yagudo Torch at that door, continue south and through the next Brass Door to the Altar Room. Finish the entry scene and examine Magicite for Magicite: Orastone.','Beadeaux: with the Coruscant Rosary and Black Matinee Necklace, take the tunnel around (H-7), follow the underground passage to Qulun Dome, and pass its sealed door. Examine Magicite for Magicite: Aurastone. Watch the affliction devices on the approach; silence prevents casting your travel spells.']),
 ('6. Receive the pass and promotion', ['With all three Magicites, examine the Audience Chamber at Ru’Lude Gardens (H-6). The scene consumes the three stones and grants the Airship Pass. If you already own that pass, the native replacement is 20,000 gil.','Return to Nelcabrit at the embassy. This final report grants Rank 5, another 10,000 gil and Message to Jeuno. Leaving after the Audience Chamber scene does not complete the embassy report.'])],['Existing access key items from another nation can be reused. You still need the new nation’s embassy, Audience Chamber and Aldo scenes.','Bring travel protection and a way home. All three Magicites are key items; they do not appear in inventory and cannot be bought.'])
mission('5-1',['Message to Jeuno','New Fei’Yin Seal','Burnt Seal'],[
 ('Obtain the replacement seal', ['Return to Chateau d’Oraguille and speak to Halver about the message from Jeuno. Accept The Ruins of Fei’Yin from a mission guard, then return to Halver for the New Fei’Yin Seal.']),
 ('Travel to Qu’Bia Arena', ['Travel through Ranguemont Pass and Beaucedine Glacier to Fei’Yin’s entrance at (J-4).','In Fei’Yin, make for the Qu’Bia Arena passage at (K-8). Enter the arena and examine the Burning Circle; select The Rank 5 Mission.']),
 ('Break the undead force', ['Defeat Archlich Taber’quoan. Its skeleton helpers create pressure, so assign healing and add control while concentrating damage on the main target.','Finish the victory/exit scene and check for the Burnt Seal in Key Items. Return to Halver in Chateau d’Oraguille to complete the mission.'])],['This is the classic level-50 battlefield. Prepare for the conditions shown at entry, including any restriction on companions.'])
mission('5-2',['Shadow Fragment'],[
 ('Meet Trion', ['Accept The Shadow Lord. Speak to Halver, then examine Door: Prince Royal’s in Chateau d’Oraguille for Trion’s briefing.']),
 ('Reach the Throne Room', ['Cross Xarcabard to Castle Zvahl Baileys. Follow the inner keep route through Castle Zvahl Keep and its teleporters to the Throne Room.','Finish the entry scene, then examine the battlefield entrance for the Shadow Lord battle.']),
 ('Defeat the Shadow Lord', ['Bring physical and magical damage options. During the first phase, his physical/magical immunity changes require you to switch how you deal damage.','Save healing resources for the second phase’s repeated area attacks. Win both phases and finish the scene to receive the Shadow Fragment.']),
 ('Return to the kingdom', ['Report to Halver for Rank 6 and 20,000 gil. Examine the Great Hall door for the closing scene before starting Leaute’s Last Wishes.'])])
mission('6-1',['Dreamrose','Piece of Paper'],[
 ('Receive the king’s request', ['Finish the Great Hall scene after 5-2. Accept Leaute’s Last Wishes from a mission guard, speak to Halver, and examine the Great Hall door.']),
 ('Find the flower', ['Travel to Western Altepa Desert (G-7). Prepare your party before examining Dreamrose flowers: this summons Sabotender Enamorado.','Defeat the cactuar. Its 1000 Needles shares damage between eligible nearby targets; avoid facing it alone with insufficient HP.','Examine Dreamrose flowers again after victory to receive the Dreamrose key item.']),
 ('Deliver and follow the story', ['Return to Halver. Then approach the Chateau garden around (F-8) for the closing scene and Piece of Paper. Keep the paper for the next mission.'])])
mission('6-2',['Piece of Paper','Ancient San d’Orian Book'],[
 ('Investigate the tomb', ['Accept Ranperre’s Final Rest and examine Door: Prince Royal’s for Trion’s instructions.','At King Ranperre’s Tomb, first map (H-8), prepare for battle and examine the Heavy Stone Door. Defeat Corrupted Yorgos, Corrupted Ulbrig and Corrupted Soffeil.']),
 ('Recover the book', ['Examine the Heavy Stone Door after the enemies are defeated. Enter and inspect the Tombstone inside to obtain the Ancient San d’Orian Book.','Return to a San d’Oria mission guard. The guard takes the book for deciphering. Change to another zone and return, then speak to the guard again. The reviewed script requires zoning here, not an overnight wait.']),
 ('Complete Trion’s investigation', ['Examine Door: Prince Royal’s again. Return to the Heavy Stone Door in King Ranperre’s Tomb for the next scene.','Report to a San d’Oria mission guard for Rank 7 and 40,000 gil.'])])
mission('7-1',['Ancient San d’Orian Tablet'],[
 ('Take the cathedral assignment', ['Accept Prestige of the Papsque. Examine the Papal Chamber upstairs in the cathedral in Northern San d’Oria.']),
 ('Reach the isolated ledge', ['Enter Bostaunieux Oubliette through Chateau d’Oraguille. Speak to Couchatorage by the sewer lid on map 1 (E-7) to descend.','Follow the lower route to the exit at map 2 (E-10). This brings you onto the raised West Ronfaure ledge at (E-8); walking there directly from the city does not reach the ledge.']),
 ('Defeat the guardian', ['Examine the ??? on the ledge to summon Marauder Dvogzog. Be ready to survive Hundred Fists.','After defeating it, examine the ??? again for the Ancient San d’Orian Tablet. Do this before jumping off the ledge.','Return to the Papal Chamber and finish the mission scene.'])])
mission('7-2',['Crystal Dowser'],[
 ('Activate the assignment', ['Ask a mission guard about The Secret Weapon. Visit the garden in Chateau d’Oraguille (F-7) for the scene, then return to the guard to accept the assignment.']),
 ('Reach Horlais Peak', ['From West Ronfaure, enter Ghelsba Outpost. Follow the Fort Ghelsba / Yughott Grotto route to Horlais Peak.','At the Burning Circle choose The Secret Weapon. Prepare for a group fight against three Orcs, two warmachines and the Dragoon’s wyvern.']),
 ('Win and report', ['Use crowd control where possible and focus targets rather than spreading damage across the whole group. Finish the victory scene and receive the Crystal Dowser.','Return to a San d’Oria mission guard for Rank 8 and 60,000 gil.'])])
mission('8-1',['Drops of Amnio'],[
 ('Attend the briefing', ['Accept Coming of Age. Enter Chateau d’Oraguille for the scene, then speak to Halver.']),
 ('Find the Fountain of Kings', ['Enter Quicksand Caves from Eastern Altepa Desert (H-10). On map 2, drop at (E-11) and continue to the Fountain of Kings at (G-14).','Prepare before examining the fountain: Honor and Valor appear together. Defeat both, then examine the Fountain of Kings again for Drops of Amnio.']),
 ('Finish the ceremony', ['Return to Halver in Chateau d’Oraguille with Drops of Amnio.','Wait at least one real minute after that scene, then enter Northern San d’Oria from another zone for the required final scene. This scene unlocks further mission-guard interaction.'])],['Zenith’s reviewed source uses a 60-second wait. You do not need to wait for Japanese midnight.'])
mission('8-2',['Crystal Dowser','Prelate Key','Piece of a Broken Key 1','Piece of a Broken Key 2','Piece of a Broken Key 3'],[
 ('Speak to the king and Rahal', ['Finish Coming of Age’s Northern San d’Oria closing scene first. Accept Lightbringer, examine the Great Hall door, then speak to Rahal in Chateau d’Oraguille (H-9).','Receive the Crystal Dowser from Rahal. Having received one during 7-2 does not replace this conversation.']),
 ('Open the temple route', ['Obtain a Prelate Key before the sealed stairway. Tonberry Stabbers in Temple of Uggalepih, Tonberry Choppers in Yhoator Jungle and Tonberry Slashers in Den of Rancor can drop it. The linked item page lists documented map squares.','Enter Temple of Uggalepih from Yhoator Jungle. From the main entry, take the right-hand route back outside and continue into the other temple entrance. Follow the map-2 path to the Temple Guardian passage at (I-10).','Defeat Temple Guardian to open its door. Continue up the stairs and trade the Prelate Key at the locked Granite Door to reach the map-4 corridor.']),
 ('Collect three different fragments', ['Reach the four rooms on the southern side of the hall around map 4 (G/H-10). Count their doors from west to east.','Examine the ??? behind doors one, three and four. These award Piece of a Broken Key 1, Piece of a Broken Key 2 and Piece of a Broken Key 3. Each character must collect all three; your party leader’s fragments do not count for you.']),
 ('Fight and recover Lightbringer', ['Examine the second door from the west after obtaining all fragments. It summons Nio-A and Nio-Hum. Defeat both dolls, then examine the same door again for the mission scene.','Return to the Great Hall door in Chateau d’Oraguille to receive Rank 9 and 80,000 gil.'])],['Do not confuse the Prelate Key with the three Broken Key fragments. The former opens the route; the latter are personal mission progress.'])
mission('9-1',['Figure of Titan','Figure of Garuda','Figure of Leviathan'],[
 ('Collect the first two figures in order', ['Accept Breaking Barriers and examine the Great Hall door in Chateau d’Oraguille.','Examine the ??? at Valley of Sorrows (I-8) for the Figure of Titan. Then examine the ??? at Xarcabard (H-7) for the Figure of Garuda. Do these in that order.']),
 ('Reach the Batallia island', ['Enter Eldieme Necropolis from Batallia Downs (I-10). Use the gate mechanism to reach the southern room, then descend through the opening at (G-9).','Follow the lower passage to the exit onto the isolated island in Batallia Downs. Bring help for the gate route if you cannot operate it alone.']),
 ('Get the final figure', ['By the island’s stone monument, examine the ??? to summon Suparna and Suparna Fledgling. Defeat the pair.','Examine the ??? again for the Figure of Leviathan. Return to the Great Hall with all three figures and finish the scene.'])])
mission('9-2',['San d’Orian Flag'],[
 ('Attend the succession ceremony', ['Accept The Heir to the Light from a mission guard. Enter Northern San d’Oria for the ceremony scene, then enter Chateau d’Oraguille for the next briefing.']),
 ('Enter the final battle', ['Travel to Fei’Yin and enter Qu’Bia Arena via (K-8). Examine the Burning Circle and select The Heir to the Light.','Defeat the opening Orc force. In the second phase, Prince Trion joins the fight against Warlord Rojgnoj and the remaining Orcs. Keep Trion alive: his defeat fails the battle.']),
 ('Close the royal story', ['After victory, enter Northern San d’Oria and examine the Great Hall door in Chateau d’Oraguille.','Visit the Heavy Stone Door in King Ranperre’s Tomb (H-8) for the closing tomb scene. Return to Halver for Rank 10, 100,000 gil and the San d’Orian Flag.','Enter Southern San d’Oria for the epilogue. If your inventory was full when the flag was awarded, free a slot and speak to Halver again.'])])

ACQUISITION = {
 'Orcish Axe':'Defeat Orcish Fodder in East or West Ronfaure. Keep one axe and trade it to a San d’Oria mission guard after accepting 1-1. The table below lists the native drop areas.',
 'Orcish Mail Scales':'Dropped by Ding Bats in King Ranperre’s Tomb. Hunt the night spawns, 18:00–06:00 Vana’diel time. Examine the mission Tombstone before returning to trade the scales for your first Bat Hunt completion.',
 'Bat Fang':'Obtain a Bat Fang from the bat drops or sources below. It is the trade for a REPEAT of Bat Hunt; your first run uses Orcish Mail Scales. Accept the repeat and revisit the Tombstone before turning it in.',
 'Bronze Sword':'For The Rescue Drill, speak to Ruillont first, then visit Deaufrain, Equesobillot and Galaihaurat outside the cave. Your mission randomly assigns one of them to give you the sword. Trade it to Ruillont; buying it does not replace the conversations.',
 'Pickaxe':'Grohm in Metalworks (H-9) gives three Pickaxes during the Bastok-first Journey Abroad briefing. Trade one at a Mythril Seam in Palborough Mines for a chance at Mine Gravel. Pickaxes may break; bring spare tools if available.',
 'Mine Gravel':'Trade a Pickaxe to a Mythril Seam in Palborough Mines, such as the one at first-floor (I-8). Then trade one Mine Gravel to the third-floor refiner input at (I-6), operate its lever, and collect Mythril Sand at the lower output lever. Mine Gravel itself can be traded through the Auction House; its native category is shown below.',
 'Mythril Sand':'Make it using Palborough Mines’ ore refiner, not a synthesis crystal: put Mine Gravel into the third-floor input at (I-6), operate the lever, then use the output lever on the floor below. On San d’Oria’s Bastok-first route, trade one sand to Savae E Paleade in Metalworks (I-9).',
 'Parana Shield':'Defeat Zhuu Buxu the Silent in Giddeus, map 2 around (H-7). On San d’Oria’s Windurst-first route, obtain two shields and trade both to Mourices in Windurst Woods (F-10), after delivering the separate Shield Offering to Uu Zhoumo.',
 'Crystal Bass':'Fish at Crystwater Spring in Jugner Forest (J-9), or buy from an actual AH listing under Food → Fish. Equip a fishing rod in Ranged and bait in Ammo, stand beside the spring and use Fishing. Minnow and Sinking Minnow have strong native bait affinity; Little Worm and Insect Ball are also supported. The native fishing skill cap is 35, not a required character level. Trade one Crystal Bass to a mission guard for 3-2.',
 'Delkfutt Key':'Defeat Porphyrion on floor 10 of Upper Delkfutt’s Tower and collect a key. Use the elevator route to descend, then trade the key to the San d’Oria Cermet Door at Lower Delkfutt’s Tower basement (M-8). This rescue scene also grants the permanent Delkfutt Key (key item) in the reviewed mission.',
 'Coeurl Meat':'Obtain one slice from the Coeurl-family drop sources below or from an actual Auction House listing under Food → Ingredients. For Magicite, obtain Aldo’s Silver Bell first, accept Crest of Davoi from Baudin at Upper Jeuno (G-8), then trade him the meat.',
 'Quadav Charm':'Dropped by De’Vyu Headhunter on Beadeaux’s upper level around (I-9). Accept Sattal-Mansal’s Beadeaux requests after Aldo’s Silver Bell, then trade the charm by itself at Lower Jeuno (J-8) for the Coruscant Rosary.',
 'Quadav Augury Shell':'Dropped by Go’Bhu Gascon on Beadeaux’s upper level around (F-6). Trade one shell by itself to Sattal-Mansal at Lower Jeuno (J-8), after accepting his requests, for the Black Matinee Necklace.',
 'Tenshodo Invite':'A player who has completed Tenshodo Membership receives this transferable invitation. Obtain one from another player or an actual AH listing, then trade it to Ghebi Damomohe in Lower Jeuno (I-7). Alternatively complete the application-form route yourself; it rewards both an invitation and the permanent member’s card.',
 'Prelate Key':'Dropped by Tonberry Stabbers in Temple of Uggalepih, Tonberry Choppers in Yhoator Jungle and Tonberry Slashers in Den of Rancor. Trade it to the locked Granite Door on the stairway route after Temple Guardian when doing Lightbringer. It is consumed by the door; obtain another if you need to open it again.',
 'San d’Orian Flag':'Speak to Halver after completing all of The Heir to the Light’s final scenes, including the Heavy Stone Door in King Ranperre’s Tomb. If your inventory was full, free a slot and speak to Halver again. This is the nation-story furnishing reward, not a monster drop.'
}

SUPPORT = [
 ('tenshodo-membership','Tenshodo Membership','Ghebi Damomohe — Lower Jeuno (I-7)','Tenshodo Member’s Card + Tenshodo Invite',[
  'Visit Ghebi Damomohe behind the counter in Neptune’s Spire, Lower Jeuno (I-7). Choose one of the following two routes.',
  'Invitation route: obtain one Tenshodo Invite from a player or an Auction House listing and trade it to her. In Zenith’s reviewed native script, this trade does not require Jeuno Fame 3.',
  'Application route: with Jeuno Fame 3, choose the blank third dialogue option about membership. Travel to Warehouse #2 in Port Bastok (F-6) and speak to Jabbar or Silver Owl for the Tenshodo Application Form.',
  'Return to Ghebi Damomohe and speak to her with the form. She exchanges it for the Tenshodo Member’s Card and one Tenshodo Invite. Leave one inventory slot for the invitation.',
  'With the member’s card, use the door at the end of Neptune’s Spire’s hallway to enter the Tenshodo headquarters. Aldo and Sattal-Mansal are inside.'], 'Tenshodo_Membership.lua'),
 ('crest-of-davoi-quest','Crest of Davoi','Baudin — Upper Jeuno (G-8)','Crest of Davoi',[
  'Advance Magicite through the embassy, Audience Chamber and Aldo until you have the Silver Bell.',
  'Speak to Baudin in Upper Jeuno (G-8) and agree to obtain the requested meat.',
  'Get one Coeurl Meat from a documented monster source or an actual Auction House listing. Trade it to Baudin to receive the Crest of Davoi.',
  'In Davoi (G-7), examine the Wall of Dark Arts. Your crest opens the route into Monastic Cavern and its Magicite.'], 'Crest_of_Davoi.lua'),
 ('yagudo-torch-route','Yagudo Torch','Paya-Sabya — Upper Jeuno (I-8); Muckvix — Lower Jeuno (H-10)','Yagudo Torch',[
  'Start Magicite and speak to Aldo for the Silver Bell.',
  'Speak to Paya-Sabya in Upper Jeuno (I-8) for the garden scene.',
  'Speak to Muckvix in his Lower Jeuno shop (H-10). With the garden scene complete, he grants the Yagudo Torch. This is a Magicite substep, not a separate accepted quest in your quest log.',
  'Follow the Castle Oztroja route on the Magicite page. Light the torch by the sealed door and enter the Altar Room; finish its scene and examine Magicite.'], None),
 ('mysteries-of-beadeaux-i','Mysteries of Beadeaux I','Sattal-Mansal — Lower Jeuno (J-8), Tenshodo headquarters','Coruscant Rosary',[
  'Obtain the Silver Bell from Aldo during Magicite. Speak to Sattal-Mansal in the same headquarters; his conversation accepts both Beadeaux requests.',
  'Defeat De’Vyu Headhunter on the upper level of Beadeaux around (I-9) and collect one Quadav Charm.',
  'Return to Sattal-Mansal and trade only the Quadav Charm for the Coruscant Rosary. Complete the second request as well before travelling to the sealed Magicite door.'], 'Mysteries_of_Beadeaux_I.lua'),
 ('mysteries-of-beadeaux-ii','Mysteries of Beadeaux II','Sattal-Mansal — Lower Jeuno (J-8), Tenshodo headquarters','Black Matinee Necklace',[
  'Accept the two Beadeaux requests from Sattal-Mansal after obtaining Aldo’s Silver Bell.',
  'Defeat Go’Bhu Gascon on Beadeaux’s upper level around (F-6) and collect one Quadav Augury Shell.',
  'Return to Sattal-Mansal and trade only the shell for the Black Matinee Necklace. Your second required key item is the Coruscant Rosary from Mysteries of Beadeaux I.'], 'Mysteries_of_Beadeaux_II.lua')
]

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def mission_key(num):
    return 'smash-the-orcish-scouts' if num=='1-1' else 'mission-sandoria-'+num

def install(ed,itemmap):
    from lxml import html
    P,add,link,para,section,table,steps=ed.P,ed.add,ed.link,ed.para,ed.section,ed.table,ed.steps
    records=[r for r in runpy.run_path(str(Path(__file__).with_name('mission_data.py')))['RECORDS'] if r['nation']=='sandoria']
    bynum={r['number']:r for r in records}
    keys={name:'key-item-'+slug(name) for name in KEY_ITEMS}
    keys.update({name:itemmap[str(i)] for name,i in PHYSICAL.items()})
    def ilink(name):return link(keys[name],escape(name))
    def source(path,label='Native source'):return '<a href="'+BASE+path+'">'+label+'</a>'
    for name,(num,obtain,use) in KEY_ITEMS.items():
        body=section('How to obtain',para(escape(obtain)))+section('What to do with it',para(escape(use)))
        body+=section('Mission walkthrough',para(link(mission_key(num),bynum[num]['title'])))
        body+=section('Trading and storage',para('This is a key item. Find it under Key Items, not your ordinary inventory. It cannot be bought at the Auction House, crafted, traded to another player or placed in a bazaar.'))
        body+=section('Reference',para('<a href="'+bynum[num]['code']+'">Native mission definition</a>'))
        add(keys[name],name,'Key Items','Acquisition and use in the San d’Oria story.',body,[('Type','Key item'),('Obtained from',escape(obtain)),('Used in',link(mission_key(num),bynum[num]['title'])),('Auction House','Not available')],parent='sandoria-mission-items')

    for name in PHYSICAL:
        k=keys[name];page=P[k]
        usage=[num for num,d in DETAILS.items() if name in d['carry']]
        # Replace generic absence-of-source text when a scripted/fishing route is now documented.
        root=html.fragment_fromstring(page['body'],create_parent='div')
        for node in list(root):
            if node.tag=='h2' and node.text_content()=='How to obtain':
                following=node.getnext()
                if following is not None and 'not yet been verified' in following.text_content():root.remove(following);root.remove(node)
        old=''.join(html.tostring(x,encoding='unicode',with_tail=True) for x in root)
        page['body']=section('Mission acquisition and use',para(escape(ACQUISITION[name]))+para('Used in: '+', '.join(link(mission_key(num),num+' — '+bynum[num]['title']) for num in usage)))+old
        if name=='Crystal Bass':page['body']+=section('Fishing reference',para(source('sql/fishing_fish.sql','Native fish data')+' · '+source('sql/fishing_bait_affinity.sql','Native bait affinities')))
        if name in ('Mine Gravel','Mythril Sand'):page['body']+=section('Refiner reference',para(source('scripts/zones/Palborough_Mines/npcs/_3za.lua','Refiner input')+' · '+source('scripts/zones/Palborough_Mines/npcs/_3z9.lua','Refiner output')))

    for key,title,npc,reward,route,filename in SUPPORT:
        code=source('scripts/quests/jeuno/'+filename) if filename else '<a href="'+bynum['4-1']['code']+'">Native Magicite step</a>'
        body=section('Walkthrough',steps(*map(escape,route)))+section('Reward',para(escape(reward)))+section('Continue Magicite',para(link('mission-sandoria-4-1','Return to the complete Magicite route')))+section('Source',para(code))
        add(key,title,'Quests','Access quest for the national Magicite mission.',body,[('Start NPC',escape(npc)),('Reward',escape(reward)),('Related mission',link('mission-sandoria-4-1','Magicite'))],parent='missions-sandoria')

    for index,rec in enumerate(records):
        num=rec['number'];d=DETAILS[num];k=mission_key(num);old=P[k]
        nav='<nav class="mission-nav" aria-label="Mission navigation">'+(link(mission_key(records[index-1]['number']),'Previous: '+records[index-1]['number']) if index else '<span>First mission</span>')+link('missions-sandoria','San d’Oria missions')+(link(mission_key(records[index+1]['number']),'Next: '+records[index+1]['number']) if index+1<len(records) else '<span>National story complete</span>')+'</nav>'
        body=nav+section('Before you begin',para(escape(rec['requirements']))+para('Accept the mission before following its route. If the guard does not offer it, finish your current mission and any closing scenes, then raise Rank Points with crystals at a Conquest guard if required.'))
        rows=[]
        for name in d['carry']:
            rows.append((ilink(name),'Inventory item' if name in PHYSICAL else 'Key item',escape(ACQUISITION[name] if name in PHYSICAL else KEY_ITEMS[name][1])))
        body+=section('Items and key items',table(['Item — open for its source','Type','Where it comes from'],rows))
        if num=='4-1':body+=section('Prerequisite quests',table(['NPC','Quest / step','Reward'],[(escape(npc),link(key,title),escape(reward)) for key,title,npc,reward,route,filename in SUPPORT]))
        body+=section('Walkthrough',''.join('<h3>'+escape(title)+'</h3>'+steps(*map(escape,route)) for title,route in d['stages']))
        if d['notes']:body+=section('Important notes',ed.listing(list(map(escape,d['notes']))))
        # Keep the existing reviewed images and source credits intact.
        oldtree=html.fragment_fromstring(old['body'],create_parent='div')
        for h in oldtree.xpath('./h2'):
            if h.text_content()=='Route maps':
                nxt=h.getnext()
                if nxt is not None:body+=section('Route maps',html.tostring(nxt,encoding='unicode'))
        reward=rec['reward']
        if num=='2-3':reward+='; Adventurer’s Certificate'
        if num=='4-1':reward='Rank 5; 10,000 gil; Airship Pass (or 20,000 additional gil if already owned); Message to Jeuno'
        if num=='9-2':reward='Rank 10; 100,000 gil; San d’Orian Flag'
        body+=section('Completion and reward',para(escape(reward)))
        body+=section('References',para('<a href="'+rec['code']+'">Native mission script used by the Zenith baseline</a> · <a href="'+rec['source']+'">HorizonXI route and map reference</a>')+para('Written for Zenith from the reviewed mission steps. Battlefield conditions follow the server’s entry message; Horizon-exclusive wardrobe rewards are not part of these rewards.'))+nav
        start='Nelcabrit — Ru’Lude Gardens (G-9); accept at the embassy rear door' if num=='4-1' else GUARDS
        facts=[('Start NPC',escape(start)),('Requirements',escape(rec['requirements'])),('Mission','San d’Oria '+num),('Items / key items',', '.join(ilink(n) for n in d['carry'])),('Reward',escape(reward)),('Previous Mission',link(mission_key(records[index-1]['number']),records[index-1]['title']) if index else 'First mission'),('Next Mission',link(mission_key(records[index+1]['number']),records[index+1]['title']) if index+1<len(records) else 'National story complete')]
        add(k,rec['title'],'Missions','San d’Oria '+num+' — requirements, item sources, route and rewards.',body,facts,parent='missions-sandoria')

    directory=table(['Item / key item','Type','Used in'],[(ilink(name),'Inventory item' if name in PHYSICAL else 'Key item',', '.join(link(mission_key(num),num) for num in ([KEY_ITEMS[name][0]] if name in KEY_ITEMS else [n for n,d in DETAILS.items() if name in d['carry']]))) for name in sorted(keys)])
    add('sandoria-mission-items','San d’Oria Mission Items','Items','Every inventory material and story key item documented in the San d’Oria Rank 1–10 guides.',directory,parent='missions-sandoria')
    P['items']['body']=section('National mission materials',para(link('sandoria-mission-items','San d’Oria: all mission items and key items')))+P['items']['body']
    P['quests']['body']+=section('Magicite access quests',table(['NPC','Quest / step','Reward'],[(escape(npc),link(key,title),escape(reward)) for key,title,npc,reward,route,filename in SUPPORT]))
    P['missions-sandoria']['body']=section('Mission items and prerequisites',para(link('sandoria-mission-items','All San d’Oria mission materials and key items')+' · '+link('tenshodo-membership','Tenshodo Membership')+' · '+link('mission-sandoria-4-1','Magicite and its access quests')))+P['missions-sandoria']['body']
    for k in ['missions','missions-sandoria','missions-bastok','missions-windurst']:
        P[k]['body']=P[k]['body'].replace('The Quest Menu does not turn in these missions.','Report to the named mission NPC to complete each stage.').replace('the custom '+link('adventurer-log','Quest Menu'),'the custom '+link('adventurer-log','world quests'))
    P['update-log']['body']=section('23 September: San d’Oria mission walkthroughs',para('Expanded all 20 San d’Oria missions through Rank 10. Journey Abroad includes both city orders. Magicite includes its access quests and exchanges. Inventory materials and story key items have individual acquisition pages and working mission links. Corrected the Coming of Age wait to one minute and the Ranperre’s Final Rest deciphering step to a zone change, following the reviewed server scripts.'))+P['update-log']['body']
    return keys
