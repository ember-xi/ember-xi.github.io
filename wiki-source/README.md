# Rebuilding the wiki source snapshot

Requirements: Python 3.9 or newer, `lxml`, Pillow with WebP support, and Node.js for JavaScript checks. The builder automatically runs compaction and finalization. Git is needed by finalization, which can stage unused-image deletions with git rm --ignore-unmatch; it never uses force. The runtime site itself is static.

From the repository root, seed the local build with the published assets and create the preview directory:

```sh
mkdir -p wiki-source/dist/assets wiki-source/dist/preview
cp -R assets/. wiki-source/dist/assets/
cd wiki-source
python tools/build-wiki.py
```

Keep the metadata in `docs/era-import/compact-assets.json` and `docs/era-import/shared-styles.json`; it preserves asset pruning mappings and shared style IDs. No app server, root package.json, or npm install is needed. The full source snapshot is under `content`, `tools`, and `docs`; Python cache files are excluded.

After rebuilding, return to the repository root and prepare publication files locally:

```sh
cd ..
python wiki-source/tools/prepare-github.py --site wiki-source --repo . --audit docs/legacy-url-migration.json --apply
```

Without `--apply`, the preparation command validates its inputs and prints the plan. It never commits, pushes, accesses credentials, or changes remote configuration. Review the resulting diff before publishing. The source commit is recorded separately in the root README and migration manifest.
