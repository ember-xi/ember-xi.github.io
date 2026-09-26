# Bilingual wiki preview

Scope: three article-style pages under `/preview/`; the existing full guide remains at `/index.html`. Its header links to the preview. English article/NPC/item/zone names, Arabic walkthroughs. Search includes Arabic aliases and links back to the complete existing guide. Checklist state is browser-local and described as such. No account, server connection or game state is implied.

## Content evidence
- A Healer's Promise: original `ZenithXI-Apururu-Quest-v1.0/apururu_quest.lua` and Quest Tidy variant. Player screenshot confirms this custom menu appears on the installed server. Requirements: current main job 30+, any Trust permit; exactly 3 Honey + 3 Distilled Water; one permanent spell 955; no Unity membership. Failed spell grant keeps the paid reward pending. Native NPC source and progress remain intact.
- Apururu: zone 241, entity 17764372, position [-12.093,-2.750,15.935,66] in the pinned Windurst Woods YAML. Standard NPC location is Manustery H-9. The map highlights the entire H-9 grid square, NOT a fabricated exact character pin. H-9 bounds reproduced from the map's 512-pixel grid: [258,290,32,32].
- Honey (4370): item_basic.sql stack 12, ingredient category. Recipe 70507 in synth_recipes.sql: Cooking cap 12, Wind Crystal 4098, 4 Beehive Chips 912; yields 4/6/9/12 Honey. East Sarutabaruta Giant_Bee template lists pot_of_honey as uncommon drop and steal item. No drop rate or static point is claimed.
- Wije Tiren: Windurst Woods NPC script includes Distilled Water at base price 12; preview avoids a fixed price because shop pricing may vary.
- Pinned server revision: f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4. This review is not a live-database inventory check. Auction availability is explicitly conditional.

## Asset provenance
Downloaded factual FFXI imagery, not AI-generated locations:
- https://horizonffxi.wiki/w/images/7/70/Windurst-woods.png — map attributed in article to Vana'diel Atlas / source page; underlying game copyright Square Enix. CSS adds the grid highlight without altering image pixels.
- https://horizonffxi.wiki/w/images/a/ad/Apururu.jpg — NPC image, credited through NPC source article.
- https://horizonffxi.wiki/w/images/4/49/Honey.jpg — game item description image with source link.
No third-party walkthrough text is copied. Arabic instructions come from the reviewed custom quest implementation.

## Validation
`tools/check-wiki-preview.py`: all three HTML entrypoints, local assets, links/fragments to existing guide, unique IDs, alt text, one H1 and source-map annotation passed. `node --check dist/preview/wiki.js` passed. Responsive CSS includes 1200/980/680 breakpoints and reduced-motion support.
This buildless static Site has no compatible supervised development server in the managed preview runtime. No browser screenshot or live visual QA is claimed. Existing pages, catalog and audience are preserved.
