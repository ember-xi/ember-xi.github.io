"""Local route maps and credited story portraits for mission walkthroughs."""
from pathlib import Path
from html import escape as esc
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def plain(value):
    return str(value).replace('’', "'").replace('‘', "'").replace('–', '-').casefold().replace('[s]', '(s)')


class MissionVisuals:
    def __init__(self, ed):
        self.ed = ed
        self.zones = json.loads((ROOT / 'zone-data.json').read_text())['zones']
        self.by_name = {plain(z['name']): z for z in self.zones}
        self.by_key = {plain(p['title']): k for k, p in ed.P.items() if p['category'] == 'Zones'}
        self.assets = json.loads((ROOT / 'image-assets.json').read_text())['assets']

    def find_zones(self, text, explicit=()):
        selected = []
        seen = set()
        for name in explicit:
            zone = self.by_name.get(plain(name))
            if zone and zone['name'] not in seen:
                selected.append(zone)
                seen.add(zone['name'])
        haystack = plain(text)
        candidates = []
        for zone in self.zones:
            for match in re.finditer(r'(?<!\w)' + re.escape(plain(zone['name'])) + r'(?!\w|\s*\(s\))', haystack):
                candidates.append((match.start(), match.end(), zone))
        occupied = []
        matches = []
        for start, end, zone in sorted(candidates, key=lambda x: (-(x[1] - x[0]), x[0])):
            if any(start < b and end > a for a, b in occupied):
                continue
            occupied.append((start, end))
            matches.append((start, zone))
        for _, zone in sorted(matches, key=lambda x: x[0]):
            if zone['name'] not in seen:
                selected.append(zone)
                seen.add(zone['name'])
        return selected

    def maps(self, zones):
        groups = []
        for zone in zones:
            maps = [m for m in zone.get('maps', []) if m.get('localPath')]
            if not maps:
                continue
            figures = []
            for number, item in enumerate(maps, 1):
                url = esc(item['localPath'], quote=True)
                label = zone['name'] + (' — ' + item['mapLabel'] if item.get('mapLabel') else (' — map ' + str(number) if len(maps) > 1 else ''))
                credit = esc(item.get('mapSourceLabel') or 'Map source')
                license_html = ' · <a href="' + esc(item['licenseUrl'], quote=True) + '">' + esc(item.get('license', 'License')) + '</a>' if item.get('licenseUrl') else ''
                figures.append('<figure><a href="' + url + '"><img src="' + url + '" width="' + str(item['width']) + '" height="' + str(item['height']) + '" loading="lazy" decoding="async" alt="' + esc(label, quote=True) + '"></a><figcaption>' + esc(label) + ' · <a href="' + url + '">Enlarge</a> · <a href="' + esc(item['sourceUrl'], quote=True) + '">' + credit + '</a>' + license_html + '</figcaption></figure>')
            groups.append('<details class="mission-map-group"' + (' open' if len(groups) < 2 and len(maps) <= 3 else '') + '><summary>' + esc(zone['name']) + '</summary><div class="mission-maps">' + ''.join(figures) + '</div></details>')
        if not groups:
            return ''
        return self.ed.section('Area maps', self.ed.para('Open a zone below, then select a map to enlarge it. Match the named floors and grid coordinates in the steps; these are reference area maps, not a live position tracker.') + ''.join(groups))

    def route_maps(self, page_key):
        source = ROOT / 'mission-route-assets.json'
        if not source.exists():
            return ''
        figures = []
        for item in json.loads(source.read_text()).get(page_key, []):
            url = esc(item['localPath'], quote=True)
            figures.append('<figure><a href="' + url + '"><img src="' + url + '" width="' + str(item['width']) + '" height="' + str(item['height']) + '" loading="lazy" alt="' + esc(item['title'], quote=True) + '"></a><figcaption>' + esc(item['title']) + ' · <a href="' + url + '">Enlarge</a> · <a href="' + esc(item['source_page'], quote=True) + '">Source</a><br>' + esc(item['credit']) + '</figcaption></figure>')
        return self.ed.section('Route illustration', '<div class="mission-maps">' + ''.join(figures) + '</div>') if figures else ''

    def portraits(self, text, preferred=()):
        haystack = plain(text)
        preference = {plain(name): i for i, name in enumerate(preferred)}
        matches = []
        for asset in self.assets:
            if asset['kind'] != 'npc' or (asset['title'] in ('Moogle', 'Vola') and plain(asset['title']) not in preference):
                continue
            name = plain(asset['title'])
            match = re.search(r'(?<!\w)' + re.escape(name) + r'(?!\w)', haystack)
            if match:
                matches.append((preference.get(name, 1000), match.start(), asset))
        figures = []
        seen_images = set()
        for _, _, asset in sorted(matches, key=lambda x: x[:2]):
            if asset['sha256'] in seen_images or len(figures) >= 4:
                continue
            seen_images.add(asset['sha256'])
            path = esc(asset['localPath'], quote=True)
            caption = asset.get('caption', asset['title'])
            figures.append('<figure><a href="' + path + '"><img src="' + path + '" width="' + str(asset['width']) + '" height="' + str(asset['height']) + '" loading="lazy" decoding="async" alt="' + esc(caption, quote=True) + '"></a><figcaption>' + esc(caption) + ' · <a href="image-credits.html#' + esc(asset['assetId'], quote=True) + '">Image source</a></figcaption></figure>')
        return self.ed.section('People in this mission', '<div class="mission-portraits">' + ''.join(figures) + '</div>') if figures else ''

    def links(self, zones):
        return self.ed.listing([self.ed.link(self.by_key[plain(z['name'])], esc(z['name'])) for z in zones if plain(z['name']) in self.by_key])
