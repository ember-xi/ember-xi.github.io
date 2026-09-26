"""Story gates for Tu'Lia and Al'Taieu, checked against the pinned native code."""
from pathlib import Path
import importlib.util


def install(ed):
    spec = importlib.util.spec_from_file_location('mission_visuals', Path(__file__).with_name('mission_visuals.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    images = module.MissionVisuals(ed)
    link, section, para, steps, table = ed.link, ed.section, ed.para, ed.steps, ed.table
    sky = section('Before you begin', ed.listing(['Finish your current nation’s Mission 5-2 and reach Rank 6.', 'Start Rise of the Zilart in Norg. Prepare access to Kazham, the jungles and the temple routes as each mission requires.', 'Complete RoZ in story order. Owning a teleport option or a map does not replace mission progress.']))
    sky += section('Route to Sky', table(['Stage', 'What to complete', 'Guide'], [
        ('National story', 'Finish the Shadow Lord mission and reach Rank 6.', link('missions', 'Choose your nation')),
        ('RoZ 1–4', 'Start at Norg, meet Gilgamesh and Jakoh, then finish the Temple of Uggalepih mission.', link('mission-roz-1', 'Start RoZ')),
        ('RoZ 5–8', 'Gather the crystal fragments, finish the quicksand battles and defeat Kam’lanaut.', link('mission-roz-5', 'Crystal-fragment route')),
        ('RoZ 9–12', 'Follow the Ro’Maeve and Hall of the Gods scenes, then obtain the Cerulean Crystal from Maryoh Comyujah.', link('mission-roz-12', 'The Mithra and the Crystal')),
        ('RoZ 13', 'Use the Shimmering Circle and enter Ru’Aun Gardens; watch the arrival scene.', link('mission-roz-13', 'The Gate of the Gods')),
    ]))
    sky += section('The final entry steps', steps('Obtain the Cerulean Crystal key item from Maryoh Comyujah during The Mithra and the Crystal. Reach the Hall of the Gods through Ro’Maeve.', 'Examine the Cermet Gate and proceed to the Shimmering Circle. Finish the Circle’s scene to complete The Mithra and the Crystal and advance to The Gate of the Gods.', 'Use the Shimmering Circle again as directed, proceed through the opened route and enter Ru’Aun Gardens. Finish its arrival scene.', 'Confirm that you are in Ru’Aun Gardens and Ark Angels is now the active RoZ mission. You have reached Sky; defeating the Ark Angels is a later story objective.'))
    sky += section('Returning with Zenith Atlas', para('Atlas’s Sky camp route checks the required RoZ progress and a previous Ru’Aun Gardens visit. Make the first story entry normally; Atlas does not award the Cerulean Crystal or finish a mission. See ' + link('camp-travel-rules', 'Camp Travel Rules') + '.'))
    sky += images.maps(images.find_zones('', ['Norg', 'Ro\'Maeve', 'Hall of the Gods', 'Ru\'Aun Gardens']))
    sky += section('References', ed.listing(['<a href="https://horizonffxi.wiki/Zilart_Mission_12">HorizonXI Wiki: RoZ 12</a>', '<a href="https://horizonffxi.wiki/Zilart_Mission_13">HorizonXI Wiki: RoZ 13</a>', '<a href="https://github.com/LandSandBoat/server/blob/f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4/scripts/missions/rotz/13_The_Gate_of_the_Gods.lua">Native Ru’Aun Gardens arrival completion</a>']))
    ed.add('sky-access', 'Sky Access', 'Guides', 'Reach Tu’Lia / Ru’Aun Gardens through Rise of the Zilart.', sky, [('Story requirement', 'National Rank 6, then RoZ 1–13'), ('Key item', 'Cerulean Crystal'), ('First arrival', 'Hall of the Gods → Ru’Aun Gardens')], parent='missions-roz', status='Story gate verified in the reviewed source; your character’s completion is not read by this website.')

    sea = section('Before you begin', ed.listing(['Begin Chains of Promathia by entering Lower Delkfutt’s Tower, then follow the Upper Jeuno and Monberaux scenes.', 'RoZ completion and national Rank 6 are not prerequisites for beginning CoP.', 'Finish every CoP chapter and required branch through The Warrior’s Path. Check the item, travel and battlefield conditions on each mission page.']))
    sea += section('Route to Sea', table(['Stage', 'Goal', 'Guide'], [
        ('Chapter 1', 'Complete the opening and all three Promyvions.', link('mission-cop-1-1', 'The Rites of Life')),
        ('Chapters 2–4', 'Travel through Tavnazia, both Roads Fork routes, Diabolos and the Ouryu story battle.', link('missions-cop', 'CoP mission order')),
        ('Chapter 5', 'Finish Promyvion-Vahzl and all three Three Paths branches.', link('mission-cop-5-3', 'Three Paths')),
        ('Chapter 6', 'Complete the story leading to the airship battle and defeat its consecutive enemies.', link('mission-cop-6-4', 'One to be Feared')),
        ('Chapter 7', 'Finish the preparation scenes, win against Tenzen and view the post-battle and arrival scenes.', link('mission-cop-7-5', 'The Warrior’s Path')),
    ]))
    sea += section('The final entry steps', steps('Finish the prerequisites for The Warrior’s Path and enter its battlefield from Sealion’s Den. Defeat Tenzen.', 'After the victory, finish the post-battle scene in Sealion’s Den. Do not treat the win alone as the entire mission completion.', 'Continue to Al’Taieu and watch its arrival scene. The reviewed mission completes The Warrior’s Path here and begins Garden of Antiquity (8-1).', 'You now have access to Al’Taieu. Completing 8-1 is needed for the next stage inside the palace, not for your first entry to Sea.'))
    sea += section('Returning and continuing', para('After completing 7-5, Sueleen in Sealion’s Den provides the return route to Al’Taieu. ' + link('mission-cop-8-1', 'Garden of Antiquity') + ' explains the next palace gates. Limbus has additional entry requirements and is not automatically entered or cleared by unlocking Sea.'))
    sea += images.portraits('Tenzen Prishe Ulmia', ['Tenzen'])
    sea += images.maps(images.find_zones('', ['Sealion\'s Den', 'Al\'Taieu', 'Tavnazian Safehold']))
    sea += section('References', ed.listing(['<a href="https://horizonffxi.wiki/The_Warrior%27s_Path">HorizonXI Wiki: The Warrior’s Path</a>', '<a href="https://horizonffxi.wiki/Promathia_Mission_8-1">HorizonXI Wiki: Garden of Antiquity</a>', '<a href="https://github.com/LandSandBoat/server/blob/f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4/scripts/missions/cop/7_5_The_Warriors_Path.lua">Native 7-5 battle, Sealion’s Den and Al’Taieu event sequence</a>']))
    ed.add('sea-access', 'Sea Access', 'Guides', 'Reach Al’Taieu through Chains of Promathia.', sea, [('Story requirement', 'CoP through The Warrior’s Path (7-5) and its arrival scene'), ('Final battle before access', 'Tenzen'), ('Next mission after entry', 'Garden of Antiquity (8-1)')], parent='missions-cop', status='Story gate verified in the reviewed source; your character’s completion is not read by this website.')
