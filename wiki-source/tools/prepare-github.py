#!/usr/bin/env python3
"""Prepare a static GitHub Pages checkout locally. Never commits or contacts remotes."""
import argparse, datetime, hashlib, html, json, re, shutil
from collections import Counter
from pathlib import Path

EXCLUDE={'__pycache__','.git','.DS_Store','node_modules'}
SECRET=re.compile(rb'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9]{30,})')
BANNER='<aside id="legacy-migration-banner" style="padding:12px 16px;background:#fff3cd;color:#332701;border-bottom:1px solid #b89b44;font:14px/1.5 sans-serif">Archived EmberXI page. These historical settings may differ from the current server. <a href="index.html" style="color:#174a72">Open the current wiki</a>.</aside>'

def copy_tree(src,dst):
    if src.resolve()==dst.resolve():return
    shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns(*EXCLUDE,'*.pyc','*.pyo'))

def rewrite_zilart(text):
    # Exact quoted relative URLs only; do not mutate race-zilart or external links.
    return re.sub(r'(["\'])((?:\./)?zilart\.html)(?=[#?"\'])',lambda m:m[1]+m[2].replace('zilart.html','race-zilart.html'),text)

def redirect(target):
    quoted=json.dumps(target)
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page moved — Zenith XI Wiki</title><link rel="canonical" href="'+html.escape(target,quote=True)+'"><script>location.replace('+quoted+'+location.search+location.hash);</script><noscript><meta http-equiv="refresh" content="0;url='+html.escape(target,quote=True)+'"></noscript></head><body><p>This page moved to <a href="'+html.escape(target,quote=True)+'">the current wiki article</a>.</p></body></html>\n'

def public_audit(report):
    report=json.loads(json.dumps(report))
    for r in report['routes']:
        r.pop('archived_source',None)
        if r['old_route']=='zones.html':
            r.update(action='retain_current_route',new_route='zones.html',confidence=1.0,reason='Intentional compatibility exception: legacy zones.html duplicated nms.html. Keep the current Areas index at zones.html; legacy nms.html redirects to the NM directory.')
            r.pop('migration',None)
    report['semantic_route_collisions']=[c for c in report.get('semantic_route_collisions',[]) if c.get('new_route')=='missions-roz.html']
    report['counts']=dict(Counter(r['action'] for r in report['routes']))
    report['source_commit']='SOURCE_COMMIT_PENDING'
    report['publication']={'mode':'GitHub Pages static root','legacy_zones_exception':True,'credentials_included':False}
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--site',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--audit',type=Path,required=True);ap.add_argument('--dist',type=Path)
    ap.add_argument('--source-commit',default=None)
    ap.add_argument('--apply',action='store_true',help='Write local checkout; otherwise validate and print the plan.')
    args=ap.parse_args();site=args.site.resolve();repo=args.repo.resolve();dist=(args.dist or site/'dist').resolve()
    assert (repo/'.git').exists(),'Destination must be the separate Git checkout.'
    assert dist.is_dir() and (dist/'index.html').is_file(),'Built dist missing.'
    assert site!=repo and dist!=repo,'Source and destination must differ.'
    audit=json.loads(args.audit.read_text()); legacy={}
    for r in audit['routes']:
        if r['action']=='preserve_legacy_original':
            src=Path(r.get('archived_source',''))
            if not src.is_file():src=repo/r['old_route']
            assert src.is_file(),f'Missing legacy original: {r["old_route"]}'
            legacy[r['old_route']]=src.read_text()
        if r['action']=='redirect':assert (dist/r['new_route']).is_file(),r['new_route']
    assert (dist/'zilart.html').is_file() and (dist/'missions-roz.html').is_file()
    # Source selection is explicit: no .git, environment, credentials or auth settings.
    roots=[dist]+[site/x for x in ['content','tools','docs']]
    total=0
    for root in roots:
        assert root.is_dir(),root.name
        for p in root.rglob('*'):
            if any(x in EXCLUDE for x in p.relative_to(root).parts):continue
            if p.is_symlink():raise RuntimeError('Symlink excluded: '+str(p.relative_to(root)))
            if p.is_file():
                total+=1
                if p.suffix.lower() in {'.html','.json','.js','.cjs','.mjs','.py','.md','.txt','.yaml','.yml','.toml'} and SECRET.search(p.read_bytes()):
                    raise RuntimeError('Credential-like token detected; source not copied: '+str(p.relative_to(root)))
    plan={'source_files':total,'redirects':sum(r['action']=='redirect' for r in audit['routes']),'preserved_legacy_pages':len(legacy),'apply':args.apply}
    if not args.apply:print(json.dumps(plan));return
    copy_tree(dist,repo)
    shutil.copy2(dist/'zilart.html',repo/'race-zilart.html')
    rewritten=0
    for original in dist.rglob('*'):
        if not original.is_file():continue
        rel=original.relative_to(dist)
        if original.suffix=='.html' or ('search-index' in original.name and original.suffix in {'.js','.json'}):
            dest=repo/rel;before=dest.read_text();after=rewrite_zilart(before)
            if before!=after:dest.write_text(after);rewritten+=1
    rp=repo/'race-zilart.html';rp.write_text(rewrite_zilart(rp.read_text()))
    for r in audit['routes']:
        if r['action']=='redirect':(repo/r['old_route']).write_text(redirect(r['new_route']))
    (repo/'zilart.html').write_text(redirect('missions-roz.html'))
    for route,body in legacy.items():
        body=re.sub(r'<aside\b[^>]*id=["\']legacy-migration-banner["\'][^>]*>.*?</aside>','',body,flags=re.S|re.I)
        body=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+BANNER,body,count=1,flags=re.I)
        assert 'legacy-migration-banner' in body,route
        (repo/route).write_text(body)
    # Existing repository assets and old files are intentionally left in place.
    source=repo/'wiki-source';source.mkdir(exist_ok=True)
    for name in ['content','tools','docs']:copy_tree(site/name,source/name)
    if Path(__file__).resolve()!=(source/'tools'/'prepare-github.py').resolve():shutil.copy2(Path(__file__).resolve(),source/'tools'/'prepare-github.py')
    report=public_audit(audit)
    report['source_commit']=args.source_commit or audit.get('source_commit','SOURCE_COMMIT_PENDING')
    report.update({'prepared_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_dist_html_count':len(list(dist.rglob('*.html'))),'current_manifest_page_count':len(json.loads((site/'content/page-manifest.json').read_text()))})
    docs=repo/'docs';docs.mkdir(exist_ok=True)
    (docs/'legacy-url-migration.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (repo/'.nojekyll').write_text('')
    (repo/'README.md').write_text('''# Zenith XI Wiki\n\nStatic level-75 wiki with documented Zenith additions. The repository root contains the published HTML and assets. GitHub Pages should publish the `main` branch, `/ (root)` directory; `.nojekyll` disables Jekyll processing. No server, npm package, secret, or credential is required to serve these files.\n\n## Content and source snapshot\n\nThe `wiki-source/content`, `wiki-source/tools`, and `wiki-source/docs` directories preserve the source snapshot and build tools. Source commit: `SOURCE_COMMIT_PENDING`. Rebuild instructions are in [wiki-source/README.md](wiki-source/README.md). Source attribution and licenses are retained in article footers and the wiki source pages; game images remain attributed to their original owners.\n\n## Legacy URLs\n\n[docs/legacy-url-migration.json](docs/legacy-url-migration.json) records each audited legacy URL and its successor. Job, mission and punctuation aliases preserve query strings and fragments. The old `zilart.html` walkthrough opens the current Rise of the Zilart missions; the current people/disambiguation article is retained at `race-zilart.html`. `zones.html` intentionally remains the Areas index: the old version duplicated the NM index, which is still reachable through `nms.html`.\n\nNine unresolved EmberXI pages retain their original content with an archive banner. Their old custom settings are historical, not current Zenith configuration. They are not added to current wiki navigation. Existing repository images, styles and older files remain available for legacy references.\n\nPublishing, committing and remote configuration are separate from the local preparation script. Never place GitHub tokens or other credentials in this repository.\n''')
    (source/'README.md').write_text('''# Rebuilding the wiki source snapshot\n\nRequirements: Python 3.9 or newer, `lxml`, Pillow with WebP support, and Node.js for JavaScript checks. The builder automatically runs compaction and finalization. Git is needed by finalization, which can stage unused-image deletions with git rm --ignore-unmatch; it never uses force. The runtime site itself is static.\n\nFrom the repository root, seed the local build with the published assets and create the preview directory:\n\n```sh\nmkdir -p wiki-source/dist/assets wiki-source/dist/preview\ncp -R assets/. wiki-source/dist/assets/\ncd wiki-source\npython tools/build-wiki.py\n```\n\nKeep the metadata in `docs/era-import/compact-assets.json` and `docs/era-import/shared-styles.json`; it preserves asset pruning mappings and shared style IDs. No app server, root package.json, or npm install is needed. The full source snapshot is under `content`, `tools`, and `docs`; Python cache files are excluded.\n\nAfter rebuilding, return to the repository root and prepare publication files locally:\n\n```sh\ncd ..\npython wiki-source/tools/prepare-github.py --site wiki-source --repo . --audit docs/legacy-url-migration.json --apply\n```\n\nWithout `--apply`, the preparation command validates its inputs and prints the plan. It never commits, pushes, accesses credentials, or changes remote configuration. Review the resulting diff before publishing. The source commit is recorded separately in the root README and migration manifest.\n''')
    readme=repo/'README.md';readme.write_text(readme.read_text().replace('SOURCE_COMMIT_PENDING',report['source_commit']))
    # Sanitize historical local-machine provenance while retaining the source data.
    for relative,field in [('docs/quest-coverage-2026-09-25/summary.json','sitePath'),('docs/quest-coverage-2026-09-25/coverage.json','sitePath'),('content/native-zone-facts-metadata.json','sourceRoot')]:
        file=source/relative
        if file.exists():
            data=json.loads(file.read_text())
            if field in data:data[field]='local source snapshot'
            file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    historical=source/'docs/mission-review/past-windurst.md'
    if historical.exists():historical.write_text(historical.read_text().replace('/root/missions_wotg','mission content review'))
    # Verify exactly the transferred page and redirect changes; old missing assets stay untouched.
    for r in report['routes']:
        if r['new_route']:assert (repo/r['new_route']).is_file(),r['new_route']
    assert (repo/'zones.html').read_bytes()==(dist/'zones.html').read_bytes(),'Areas index changed unexpectedly.'
    assert 'location.search+location.hash' in (repo/'job-war.html').read_text()
    assert not any(p.is_dir() for p in source.rglob('__pycache__'))
    assert '/workspace/' not in (docs/'legacy-url-migration.json').read_text()
    plan.update({'rewritten_current_files':rewritten,'prepared':True});print(json.dumps(plan))

if __name__=='__main__':main()
