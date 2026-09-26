# Zenith XI Wiki

Static level-75 wiki with documented Zenith additions. The repository root contains the published HTML and assets. GitHub Pages should publish the `main` branch, `/ (root)` directory; `.nojekyll` disables Jekyll processing. No server, npm package, secret, or credential is required to serve these files.

## Content and source snapshot

The `wiki-source/content`, `wiki-source/tools`, and `wiki-source/docs` directories preserve the source snapshot and build tools. Source commit: `4514bcf1c46af2266ebb616ac7b239587d86ab05`. Rebuild instructions are in [wiki-source/README.md](wiki-source/README.md). Source attribution and licenses are retained in article footers and the wiki source pages; game images remain attributed to their original owners.

## Legacy URLs

[docs/legacy-url-migration.json](docs/legacy-url-migration.json) records each audited legacy URL and its successor. Job, mission and punctuation aliases preserve query strings and fragments. The old `zilart.html` walkthrough opens the current Rise of the Zilart missions; the current people/disambiguation article is retained at `race-zilart.html`. `zones.html` intentionally remains the Areas index: the old version duplicated the NM index, which is still reachable through `nms.html`.

Nine unresolved EmberXI pages retain their original content with an archive banner. Their old custom settings are historical, not current Zenith configuration. They are not added to current wiki navigation. Existing repository images, styles and older files remain available for legacy references.

Publishing, committing and remote configuration are separate from the local preparation script. Never place GitHub tokens or other credentials in this repository.
