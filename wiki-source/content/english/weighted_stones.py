"""Garlaige's native solo gate access, checked against qm17 and all three doors."""


def install(ed, record):
    P, add, section, para, table, link, steps = (
        ed.P, ed.add, ed.section, ed.para, ed.table, ed.link, ed.steps)
    quest = record['key']
    npc = record['npc_key']
    item = record['reward_key']
    zone = 'zone-garlaige-citadel'
    gates = 'banishing-gates'
    revision = 'f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4'
    source_root = 'https://github.com/LandSandBoat/server/blob/' + revision
    references = section('References', ed.listing([
        '<a href="https://www.bg-wiki.com/ffxi/Pouch_of_weighted_stones">BG Wiki: Pouch of weighted stones</a>',
        '<a href="https://ffxiclopedia.fandom.com/wiki/Pouch_of_weighted_stones">FFXIclopedia: entrance route</a>',
        '<a href="https://horizonffxi.wiki/Banishing_Gate">HorizonXI Wiki: Banishing Gate locations</a>',
        '<a href="' + source_root + '/scripts/zones/Garlaige_Citadel/npcs/qm17.lua">Native acquisition event</a>',
        '<a href="' + source_root + '/scripts/zones/Garlaige_Citadel/npcs/_5k0.lua">Native gate interaction</a>',
    ]))
    availability = para('<strong>Zenith availability:</strong> This target is hidden in the reviewed Zenith setup. Weighted Stones v1.0 corrects its availability; installation and an in-game check are pending. No level or prior quest unlocks it.')
    overview = table(['NPC', 'Quest', 'Reward'], [(
        link(npc, record['npc_name']) + '<br>' + record['location'],
        link(quest, record['title']) + '<br>' + record['level'],
        link(item, record['reward']) + '<br>' + record['reward_type'] + ' · ' + record['cost'],
    )])
    directions = steps(
        'Enter present-day ' + link(zone, 'Garlaige Citadel') + ' from Sauromugue Champaign and descend the entrance stairs. Use Map 1, not Garlaige Citadel [S].',
        'Continue straight at the first four-way junction. Before the hole in the floor, enter the first room on your right, at (G-8).',
        'Look for ??? on a small rock on the left, near the doorway leading into the next room. This is a floor-level target, not a ceiling target.',
        'Examine ??? and accept taking the stones. The event awards ' + link(item, record['reward']) + ' immediately. No item trade, fee or battle is required.',
        'Confirm it in Permanent Key Items. ' + record['turn_in'],
        'Select a closed ' + link(gates, 'Banishing Gate') + ' to open it. After a brief delay, the door opens for 15 seconds; pass through promptly. Keep the key item for future visits.',
    )
    map_html = '<figure class="area-map"><div class="map-marked"><img loading="lazy" src="assets/zones/garlaigecitadel1-3eb45e24.webp" alt="Garlaige Citadel Map 1; find the weighted-stones target in grid G-8" width="512" height="512"></div><figcaption>Map 1: weighted stones are in (G-8). The blue Divine paint marker printed on this map identifies a different ???.</figcaption><button type="button" data-enlarge-map data-map-title="Garlaige Citadel — Map 1">Enlarge</button></figure>'
    map_html += para('<small>Map: <a href="https://horizonffxi.wiki/File:GarlaigeCitadel1.png">HorizonXI Wiki</a>. Original game map © SQUARE ENIX.</small>')
    add(quest, record['title'], 'Quests',
        'Obtain a permanent key item to open all three Banishing Gates by yourself. This is an unlisted acquisition task, without a quest-log entry.',
        section('Quest overview', overview) +
        section('Requirements', para('Any job and level. No fame, mission or quest prerequisite is checked by the acquisition event. You must not already own the key item. Nearby enemies still pose a threat.') + availability) +
        section('Walkthrough', directions) +
        section('Map', map_html) +
        section('If you cannot find it', ed.listing([
            'Check the zone name: Garlaige Citadel, present-day, Map 1 (G-8).',
            'Use the small rock near the inner doorway. Other ??? targets in the same dungeon serve different quests.',
            'If the target is absent in this room, check the Zenith availability note above. If the target says nothing is out of the ordinary, check whether you already have the key item.',
        ])) +
        section('Related quests', para('Useful when passing the gates for ' + link('first-limit-break', 'In Defiant Challenge') + ', artifact equipment and other dungeon objectives. Gate access does not complete those objectives.')) + references,
        facts=[('Starting NPC', link(npc, '???')), ('Location', record['location']),
               ('Reward', link(item, record['reward'])), ('Cost', record['cost']),
               ('Repeatable', 'No; the key item is retained')], parent='quests')
    add(item, record['reward'], 'Key Items',
        'A permanent key item that allows its holder to open the Banishing Gates in Garlaige Citadel alone.',
        section('Obtained from', table(['Source', 'Location', 'Cost'], [
            (link(npc, '???'), record['location'], record['cost'])])) +
        section('How to obtain', para('Examine the floor-level ??? on a small rock and accept the stones. No quest acceptance elsewhere is needed. ' + link(quest, 'Full walkthrough and map') + '.') + availability) +
        section('Use', para('Select any closed ' + link(gates, 'Banishing Gate') + '. The native interaction waits about 1.5 seconds, then opens the door for 15 seconds. It works from either side and does not consume the key item. No ordinary inventory slot is required.')) +
        section('History', para('Solo gate access with this key item was added in the <a href="https://forum.square-enix.com/ffxi/threads/24155-June-14-2012-%28JST%29-Version-Update">June 2012 retail update</a>. Zenith treats it as an optional travel convenience for its level-75 adventure.')) + references,
        facts=[('Type', record['reward_type']), ('Zone', link(zone, 'Garlaige Citadel')), ('Cost', record['cost'])], parent='items')
    add(npc, record['npc_name'], 'NPCs',
        'A floor-level target that awards the Pouch of Weighted Stones.',
        section('Location', para(record['location'] + ': a small rock near the doorway to the adjoining room. From the entrance, continue straight at the first junction and enter the first room on the right.')) +
        section('Quest and reward', overview) + section('Availability', availability) + references,
        facts=[('Displayed name', '???'), ('Location', record['location'])], parent='npcs')
    add(gates, 'Banishing Gates', 'Guides',
        'Three doors divide the passages of Garlaige Citadel.',
        section('Locations', table(['Gate', 'Game-map location'], [
            ('First Banishing Gate', 'Map 1 (I-9)'),
            ('Second Banishing Gate', 'Map 2 (H-9)'),
            ('Third Banishing Gate', 'Map 2 (H-6)'),
        ])) +
        section('Open a gate alone', para('Obtain ' + link(item, record['reward']) + ' at Map 1 (G-8), then select the closed gate. The key item is retained. ' + link(quest, 'Directions to the stones') + '.') + para('The reviewed door scripts open each gate for 15 seconds after a short delay. Continue through before it closes.')) +
        section('Pressure switches', para('The original method uses four players, one on each of the associated floor switches. When all four are pressed, the gate opens briefly.')) +
        section('Map', para(link(zone, 'Garlaige Citadel maps and connected areas'))) + references,
        parent=zone)
    note = section('Solo access: Banishing Gates', para(
        'Obtain ' + link(item, record['reward']) + ' from ??? at Map 1 (G-8) to open the three gates yourself. ' +
        link(quest, 'Full directions, requirements and map') + ' · ' + link(gates, 'Gate locations') + '.') + availability)
    P[zone]['body'] += note
    P['first-limit-break']['body'] += note
    # Add to the existing access table rather than inventing another quest menu.
    body = P['quests']['body']
    heading = '<h2>Dungeon access quests</h2>'
    start = body.index(heading)
    end = body.index('</tbody>', start)
    row = overview.split('<tbody>', 1)[1].split('</tbody>', 1)[0]
    P['quests']['body'] = body[:end] + row + body[end:]
    for key in ('items', 'travel', 'npcs'):
        P[key]['body'] += section('Garlaige Citadel access', para(link(quest, record['title']) + ' · ' + link(item, record['reward']) + ' · ' + link(npc, record['npc_name'])))
    P['update-log']['body'] = section('25 September 2026 — Weighted Stones', para(
        'Added the acquisition walkthrough, permanent key item, target and Banishing Gate reference, with links from Garlaige Citadel and First Limit Break. Weighted Stones v1.0 corrects the hidden acquisition marker; an in-game check is pending.')) + P['update-log']['body']
