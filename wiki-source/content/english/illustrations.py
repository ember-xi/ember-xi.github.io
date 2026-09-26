"""Verified game images in traditional wiki articles and reference tables."""
from pathlib import Path
from html import escape as esc
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def norm(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode().lower())


def install(ed):
    assets = json.loads((ROOT / 'image-assets.json').read_text())['assets']
    lookup = {(a['kind'], norm(a['title'])): a for a in assets}

    def image_tag(asset, cls='entity-thumb'):
        return '<img class="'+cls+'" src="'+esc(asset['localPath'], quote=True)+'" alt="'+esc(asset['caption'], quote=True)+'" width="'+str(asset['width'])+'" height="'+str(asset['height'])+'" loading="lazy" decoding="async">'

    def credit(asset):
        return 'image-credits.html#'+asset['assetId']

    def entity_image(kind, title, label):
        asset = lookup.get((kind, norm(title)))
        if not asset:
            return label
        return '<span class="illustrated-name"><a class="entity-image-link" href="'+esc(asset['localPath'], quote=True)+'" aria-label="View '+esc(asset['caption'], quote=True)+'">'+image_tag(asset)+'</a><span>'+label+'<small><a href="'+credit(asset)+'">Image source</a></small></span></span>'

    ed.entity_image = entity_image
    ed.has_entity_image = lambda kind, title: (kind, norm(title)) in lookup
    for key, page in ed.P.items():
        if page['category'] not in ('NPCs', 'Jobs'):
            continue
        kind = 'npc' if page['category'] == 'NPCs' else 'job'
        asset = next((a for a in assets if a['kind'] == kind and a.get('pageKey') == key), None) or lookup.get((kind, norm(page['title'])))
        if asset:
            page['portraitHtml'] = '<figure class="reference-portrait"><a href="'+esc(asset['localPath'], quote=True)+'">'+image_tag(asset, 'article-portrait')+'</a><figcaption>'+esc(asset['caption'])+' · <a href="'+credit(asset)+'">Image source</a></figcaption></figure>'

    # The directory remains an ordinary linked wiki category. Jobs without a
    # local article link to their reference page rather than a fabricated guide.
    job_art = [a for a in assets if a['kind'] == 'job']
    local_jobs = {norm(p['title']): k for k, p in ed.P.items() if p['category'] == 'Jobs'}
    gallery = []
    for asset in job_art:
        key = local_jobs.get(norm(asset['title']))
        url = key+'.html' if key else asset['sourcePage']
        gallery.append('<figure><a href="'+esc(url, quote=True)+'">'+image_tag(asset, 'job-directory-image')+'<span>'+esc(asset['title'])+'</span></a><figcaption><a href="'+credit(asset)+'">Image source</a></figcaption></figure>')
    ed.P['jobs']['body'] = ed.section('Jobs', '<div class="job-illustrations">'+''.join(gallery)+'</div>')+ed.P['jobs']['body']

    rows = []
    for asset in sorted(assets, key=lambda a: (a['kind'], a['title'])):
        source = asset.get('filePage') or asset['sourcePage']
        name = '<span id="'+asset['assetId']+'">'+esc(asset['title'])+'</span>'
        rows.append((name, esc(asset['kind'].title()), '<a href="'+esc(source, quote=True)+'">'+esc(asset.get('source', 'Source'))+'</a>', esc(asset.get('sourceUploader') or '—')))
    ed.add('image-credits', 'Image Credits', 'Reference', 'Original FINAL FANTASY XI game images and job artwork © SQUARE ENIX.',
           ed.para('NPC portraits and named monster images show the identified subject. Images in the Family column illustrate the monster family; individual variants can look different.')+
           ed.section('Sources', ed.table(['Subject', 'Type', 'Source file / page', 'Source uploader'], rows))+
           ed.para('Game artwork and screenshots remain © SQUARE ENIX. Wiki image contributors are credited above where identified by the source.'), parent='sources')
    ed.P['sources']['body'] += ed.section('NPC, Monster and Job Images', ed.para(ed.link('image-credits', 'Image credits and original source files')+'. Job illustrations and screenshots come from the official FINAL FANTASY XI website. NPC and monster images are credited to their source wiki files.'))
    ed.P['update-log']['body'] = ed.section('25 September 2026 — Game images', ed.para('Added official images for the twenty jobs through Wings of the Goddess, NPC portraits, and monster images in area tables. Family images are placed in the Family column.'))+ed.P['update-log']['body']
