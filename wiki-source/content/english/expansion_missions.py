"""Sourced expansion story walkthroughs, linked to local maps and NPC images."""
from pathlib import Path
from html import escape as esc
import importlib.util
import json
import re
import runpy
import unicodedata
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGNS = {
    'roz': ('Rise of the Zilart', 'RoZ', 'National Rank 6 → Norg → Sky'),
    'cop': ('Chains of Promathia', 'CoP', 'Lower Delkfutt’s Tower → Tavnazia → Sea'),
    'toau': ('Treasures of Aht Urhgan', 'ToAU', 'Mhaura → Aht Urhgan Whitegate → mercenary story'),
    'wotg': ('Wings of the Goddess', 'WotG', 'Cavernous Maws → past national quests → main story'),
    'acp': ('A Crystalline Prophecy', 'ACP', 'Jeuno and the Seed Crystal story'),
    'amk': ('A Moogle Kupo d’Etat', 'AMK', 'Mog House → Moogle story'),
    'asa': ('A Shantotto Ascension', 'ASA', 'Windurst Walls → Shantotto story'),
}
REV = 'f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4'


def key(record):
    return record.get('slug') or 'mission-' + record['campaign'] + '-' + re.sub(r'[^a-z0-9]+', '-', str(record['number']).lower()).strip('-')


def strings(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    return value


def load_records():
    records = []
    for source in sorted((ROOT / 'expansion-missions').glob('*.json')):
        data = json.loads(source.read_text())
        records.extend(data if isinstance(data, list) else data['records'])
    return records


def install(ed):
    spec = importlib.util.spec_from_file_location('mission_visuals', Path(__file__).with_name('mission_visuals.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    visuals = module.MissionVisuals(ed)
    records = load_records()
    if not records:
        raise ValueError('Expansion mission data is required')
    if len({key(r) for r in records}) != len(records):
        raise ValueError('Duplicate expansion mission URL')
    by_campaign = {c: [r for r in records if r['campaign'] == c] for c in CAMPAIGNS}
    zone_walkthroughs = {}
    by_title = {}
    explicit_aliases = set()
    for record in records:
        by_title.setdefault(record['title'], []).append(record)
        for alias in record.get('aliases', []):
            explicit_aliases.add(alias)
            by_title.setdefault(alias, []).append(record)

    def rich(value, current=None):
        text = str(value)
        eligible = {title: matches for title, matches in by_title.items() if len(title) >= 9 or title in explicit_aliases}
        pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(t) for t in sorted(eligible, key=len, reverse=True)) + r')(?!\w)')
        parts = []
        cursor = 0
        for match in pattern.finditer(text):
            parts.append(esc(text[cursor:match.start()]))
            candidates = eligible[match.group()]
            target = next((r for r in candidates if current and r['campaign'] == current['campaign']), candidates[0])
            parts.append(esc(match.group()) if current and key(current) == key(target) else ed.link(key(target), esc(match.group())))
            cursor = match.end()
        parts.append(esc(text[cursor:]))
        return ''.join(parts)

    def nav(record, mains):
        hub = 'missions-' + record['campaign']
        if record.get('sequence_group'):
            mains = [r for r in records if r.get('sequence_group') == record['sequence_group']]
        if record in mains:
            position = mains.index(record)
            left = ed.link(key(mains[position - 1]), 'Previous: ' + esc(str(mains[position - 1]['number']))) if position else '<span>Opening mission</span>'
            right = ed.link(key(mains[position + 1]), 'Next: ' + esc(str(mains[position + 1]['number']))) if position + 1 < len(mains) else '<span>End of campaign list</span>'
        else:
            parent = next((r for r in mains if str(r['number']) == str(record.get('branch_of'))), None)
            left = ed.link(key(parent), 'Return to ' + esc(parent['title'])) if parent else '<span>Related story quest</span>'
            right = '<span>Follow the prerequisites on this page</span>'
        return '<nav class="mission-nav" aria-label="Mission navigation">' + left + ed.link(hub, CAMPAIGNS[record['campaign']][0]) + right + '</nav>'

    for campaign, group in by_campaign.items():
        mains = [r for r in group if not r.get('branch_of') and r.get('kind', 'mission') not in ('quest', 'branch', 'guide')]
        for record in group:
            current_key = key(record)
            start = record['start']
            if isinstance(start, str):
                start = {'npc': start, 'zone': ''}
            contact = ' · '.join(str(start.get(k, '')) for k in ('npc', 'zone', 'grid') if start.get(k))
            route = strings(record['steps'])
            alltext = json.dumps(record, ensure_ascii=False)
            zones = visuals.find_zones(alltext, strings(record.get('zones')))
            for zone in zones:
                zone_walkthroughs.setdefault(module.plain(zone['name']), []).append(record)
            if record.get('reuse_existing'):
                if current_key not in ed.P:
                    raise ValueError('Missing existing prerequisite guide: ' + current_key)
                ed.P[current_key]['body'] += visuals.portraits(alltext, [start.get('npc', '')]) + visuals.maps(zones)
                if record.get('related'):
                    ed.P[current_key]['body'] += ed.section('Further travel', ed.listing([ed.link(item['key'], esc(item['label'])) for item in record['related']]))
                continue
            navigation = nav(record, mains)
            body = navigation
            if record.get('availability_note'):
                body += '<aside class="mission-availability"><strong>Zenith availability</strong>' + ed.para(esc(record['availability_note'])) + '</aside>'
            body += ed.section('Before you begin', ed.listing([rich(s, record) for s in strings(record['requirements'])]))
            body += ed.section('Starting point', ed.para(esc(contact)))
            if record.get('era_note'):
                body += ed.para('<strong>Era note:</strong> ' + esc(record['era_note']))
            body += visuals.portraits(alltext, [start.get('npc', '')])
            body += ed.section('Walkthrough', ed.steps(*[rich(step, record) for step in route]))
            branches = [r for r in group if str(r.get('branch_of', '')) == str(record['number'])]
            if branches:
                body += ed.section('Required paths', ed.listing([ed.link(key(r), esc(str(r['number']) + ' — ' + r['title'])) for r in branches]))
            if record.get('notes'):
                body += ed.section('Battle and progress notes', ed.listing([rich(s, record) for s in strings(record['notes'])]))
            body += ed.section('Completion and reward', ed.para(rich(record['reward'], record)))
            if record.get('unlocks'):
                body += ed.section('What this opens', ed.listing([rich(s, record) for s in strings(record['unlocks'])]))
            if record.get('related'):
                body += ed.section('Related walkthroughs', ed.listing([ed.link(item['key'], esc(item['label'])) for item in record['related']]))
            body += visuals.route_maps(current_key) + visuals.maps(zones)
            if zones:
                body += ed.section('Zone guides', visuals.links(zones))
            source_rows = []
            for source in record['sources']:
                if isinstance(source, str):
                    source = {'url': source, 'label': 'Walkthrough source'}
                source_rows.append('<a href="' + esc(source['url'], quote=True) + '">' + esc(source.get('label', 'Walkthrough source')) + '</a>')
            for source in strings(record.get('code')):
                if isinstance(source, dict):
                    source_rows.append('<a href="' + esc(source['url'], quote=True) + '">' + esc(source.get('label', 'Reviewed mission implementation')) + '</a>')
                else:
                    source_rows.append('<a href="' + esc(source, quote=True) + '">Reviewed mission implementation</a>')
            body += ed.section('References', ed.listing(source_rows) + ed.para('Steps are an original summary of the linked walkthrough and reviewed source. Other servers’ bonus rewards are not included. ' + ed.link('mission-reading-guide', 'How to read requirements, waits and battlefield notes') + '.')) + navigation
            kind = record.get('kind', 'mission')
            category = 'Quests' if kind == 'quest' else 'Missions'
            ed.add(current_key, record['title'], category, CAMPAIGNS[campaign][0] + ' · ' + ('Related quest' if kind == 'quest' else 'Mission ' + str(record['number'])) + '.', body,
                   [('Story', ed.link('missions-' + campaign, CAMPAIGNS[campaign][0])), ('Mission', esc(str(record['number']))), ('Start', esc(contact)), ('Reward', esc(record['reward']))],
                   parent='missions-' + campaign, status='Reference walkthrough; completion on Zenith has not been confirmed.')

        first = mains[0]
        body = ed.section('Before you begin', ed.listing([rich(s, first) for s in strings(first['requirements'])]))
        if campaign == 'roz':
            body += ed.para('For the shortest story route to Tu’Lia, use ' + ed.link('sky-access', 'Sky Access') + '. Ark Angels is a later objective, not the entry requirement.')
        elif campaign == 'cop':
            body += ed.para('For the route to Al’Taieu, use ' + ed.link('sea-access', 'Sea Access') + '. Rank 6 and RoZ progress are not prerequisites for beginning CoP.')
        elif campaign == 'wotg':
            body += ed.para('WotG alternates between its main story and a past nation’s quest chain. A qualifying chain from one nation is sufficient at the main-story gates; do not complete all three unless you want their separate stories.')
            body += ed.para('The complete expansion is indexed here, including later chapters released after the original level-75 period. Known missing battle implementations are identified on their pages; the full campaign is not confirmed completable on Zenith.')
        elif campaign in ('acp', 'amk', 'asa'):
            body += ed.para('This is a reference walkthrough of the original add-on. Enabling an expansion does not fill missing quest or battlefield code; check the availability note before committing to a route.')
        body += ed.section('Mission order', ed.table(['Mission', 'Walkthrough', 'Completion / unlock'], [(esc(str(r['number'])), ed.link(key(r), esc(r['title'])), rich('; '.join(strings(r.get('unlocks'))) or r['reward'], r)) for r in mains]))
        auxiliary = [r for r in group if r not in mains]
        if auxiliary:
            if campaign == 'wotg':
                for nation, title in [('sandoria', 'San d’Oria [S] quest order'), ('bastok', 'Bastok [S] quest order'), ('windurst', 'Windurst [S] quest order')]:
                    chain = [r for r in auxiliary if r.get('sequence_group') == 'past-' + nation]
                    body += ed.section(title, ed.table(['Quest', 'Walkthrough', 'Requirements'], [(esc(str(r['number'])), ed.link(key(r), esc(r['title'])), rich(' '.join(strings(r['requirements'])), r)) for r in chain]))
                memory = [r for r in auxiliary if not r.get('sequence_group')]
                body += ed.section('Her Memories branches', ed.listing([ed.link(key(r), esc(r['title'])) for r in memory]))
            else:
                body += ed.section('Branches and related quests', ed.table(['Route', 'Walkthrough', 'Requirements'], [(esc(str(r['number'])), ed.link(key(r), esc(r['title'])), rich(' '.join(strings(r['requirements'])), r)) for r in auxiliary]))
        blocked = [r for r in group if r.get('availability_note')]
        if blocked:
            body += ed.section('Availability notes before you travel', ed.table(['Mission / quest', 'Reviewed limitation'], [(ed.link(key(r), esc(r['title'])), esc(r['availability_note'])) for r in blocked]))
        body += ed.section('Reading these guides', ed.para(ed.link('mission-reading-guide', 'Requirements, travel, battle rules and source differences') + '. Each mission has numbered steps and local maps where the area has a map. ' + ed.link('missions', 'All story campaigns') + '.'))
        ed.add('missions-' + campaign, CAMPAIGNS[campaign][0] + ' Missions', 'Missions', CAMPAIGNS[campaign][2] + '.', body, parent='missions')

    # Keep every national URL and its selected, annotated route maps. Add the
    # previously omitted area maps and story portraits to all national guides.
    nationals = runpy.run_path(str(Path(__file__).with_name('mission_data.py')))['RECORDS']
    for record in nationals:
        page_key = 'smash-the-orcish-scouts' if record['nation'] == 'sandoria' and record['number'] == '1-1' else 'mission-' + record['nation'] + '-' + record['number']
        page = ed.P[page_key]
        text = json.dumps(record, ensure_ascii=False)
        pictures = visuals.portraits(text)
        page['body'] = page['body'].replace('<h2>Walkthrough</h2>', pictures + '<h2>Walkthrough</h2>', 1)
        maps = visuals.maps(visuals.find_zones(text))
        page['body'] = page['body'].replace('<h2>References</h2>', maps + '<h2>References</h2>', 1)

    ed.add('mission-reading-guide', 'Using the Mission Walkthroughs', 'Guides', 'Check your current mission, prepare its entry requirements, then follow its route.',
           ed.section('Before starting', ed.steps('Open the in-game Missions menu and select the correct nation or expansion. Compare the exact active title with this wiki; a cutscene can advance the mission without a battle.', 'Read Before you begin. Complete every named prerequisite, obtain the required key items, and finish the preceding mission’s final reporting scene.', 'Read the starting NPC and zone. Prepare listed consumables, access items and enough inventory space before travelling.')) +
           ed.section('Requirements and difficulty', ed.para('A required level, rank or key item controls acceptance or entry. A suggested battle level describes difficulty. These are different conditions. Historical level caps from other servers do not prove Zenith’s current battlefield cap; mission notes identify reviewed differences.') + ed.para('A Trust permit and enough Trust slots do not guarantee entry into every battlefield. Read the specific mission note, and follow the entry message in game. An NPC missing from a disabled or unfinished area cannot be repaired by repeating the wiki route.')) +
           ed.section('Waits and stalled progress', ed.listing(['A Vana’diel-day wait is an in-game day boundary. A real-day or Japanese-midnight wait is different; follow the type specified in the mission note.', 'If a cutscene fails to trigger, finish the previous NPC’s closing dialogue, check the current mission title and zone out/in when the route asks for it.', 'Modern retail Home Points, Survival Guides and Rhapsodies shortcuts may not exist or may require prior registration. Use the ordinary route first unless you have already unlocked the shortcut.', 'An availability note identifies a known missing or unconfirmed implementation. It is not a request to reinstall the game or enable unrelated expansions.'])) +
           ed.section('Scope', ed.para('This directory covers the three present-day national stories, RoZ, CoP, ToAU, WotG and the three 2009 add-ons. The late WotG conclusion is retained with its era and implementation notes. Assault, Campaign Ops and repeatable battle systems are separate from these story mission chains. Adoulin, Rhapsodies, Voracious Resurgence and Abyssea are outside the level-75 story guide scope.')) +
           ed.section('Sources and images', ed.para('Walkthrough text is summarized for this wiki. Source links remain on each page; game imagery and map credits remain with the original contributors and SQUARE ENIX. ' + ed.link('image-credits', 'Image credits') + '.')), parent='missions')

    rows = [
        (ed.link('missions-sandoria', 'San d’Oria'), 'San d’Oria allegiance; mission guard and Rank Points', 'Rank 1 → Rank 10'),
        (ed.link('missions-bastok', 'Bastok'), 'Bastok allegiance; mission guard and Rank Points', 'Rank 1 → Rank 10'),
        (ed.link('missions-windurst', 'Windurst'), 'Windurst allegiance; mission guard and Rank Points', 'Rank 1 → Rank 10'),
    ]
    for campaign in CAMPAIGNS:
        first = next(r for r in by_campaign[campaign] if r.get('kind', 'mission') not in ('quest', 'guide', 'branch') and not r.get('branch_of'))
        rows.append((ed.link('missions-' + campaign, CAMPAIGNS[campaign][0]), rich(' '.join(strings(first['requirements']))), CAMPAIGNS[campaign][2]))
    body = ed.section('Story campaigns', ed.table(['Campaign', 'To begin', 'Story route'], rows))
    body += ed.section('Access goals', ed.table(['Goal', 'Required story progress', 'Walkthrough'], [('Sky / Tu’Lia', 'National Rank 6, then RoZ through The Gate of the Gods and arrival in Ru’Aun Gardens.', ed.link('sky-access', 'Open Sky')), ('Sea / Al’Taieu', 'CoP through The Warrior’s Path and the Al’Taieu arrival scene.', ed.link('sea-access', 'Open Sea'))]))
    body += ed.section('Follow your current mission', ed.para('Choose a campaign, then open the exact mission title shown in game. Each page lists its prerequisites, starting point, ordered steps, rewards, local area maps and available NPC portraits. ' + ed.link('mission-reading-guide', 'Read the mission guide notes') + '.'))
    ed.add('missions', 'Missions', 'Missions', 'National and expansion story walkthroughs, including the routes that unlock Sky and Sea.', body)
    ed.P['update-log']['body'] = ed.section('25 September 2026 — Story mission walkthroughs', ed.para('Added expansion mission pages, entry requirements, story branches, credited NPC images and route maps. The mission directory now links the Sky and Sea access routes. Known missing core battle steps are stated on the affected pages.')) + ed.P['update-log']['body']

    # Existing zone tables were assembled before these new articles. Link their
    # exact mission/quest names locally while retaining all source/image links.
    def normalized(value):
        return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower())
    story_links = {normalized(r['title']): key(r) for r in records}
    for page in ed.P.values():
        if page['category'] != 'Zones':
            continue
        root = html.fragment_fromstring(page['body'], create_parent='div')
        for anchor in root.xpath('.//td//a[@href]'):
            href = anchor.get('href', '')
            target = story_links.get(normalized(anchor.text_content()))
            if target and href.startswith(('https://horizonffxi.wiki/', 'https://www.bg-wiki.com/', 'https://ffxiclopedia.fandom.com/')):
                anchor.set('href', target + '.html')
        page['body'] = ''.join(html.tostring(child, encoding='unicode') for child in root)
        related = zone_walkthroughs.get(module.plain(page['title']), [])
        if related:
            table = ed.section('Story walkthroughs in this area', ed.table(['Story', 'Mission / quest'], [(CAMPAIGNS[r['campaign']][1] + ' ' + esc(str(r['number'])), ed.link(key(r), esc(r['title']))) for r in related]))
            page['body'] = page['body'].replace('<h2>References</h2>', table + '<h2>References</h2>', 1)
