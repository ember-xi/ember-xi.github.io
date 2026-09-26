# Game images — 25 September 2026

Preserved the traditional wiki layout. Added portraits to existing NPC articles,
official artwork/screenshots for all twenty jobs through Wings of the Goddess,
and small illustrations within existing zone tables. Exact monster images go in
the Name column; representative images go in the Family column. No image is
assigned to a custom Zenith NPC by guessing its race or model.

`content/image-assets.json` records sources, captions, copyright context, hashes
and local paths. Images are local static files, have explicit dimensions, use
aspect-ratio-preserving rendering and lazy loading, and link to source credits.
The import helper verifies the reviewed bytes and avoids network work at build.

Coverage: 20 jobs, 29 native NPC portraits, 44 named monsters and 124 family
labels. There are 208 distinct image files. Exact portraits or labeled family
examples illustrate 3,582 of 3,588 existing monster-table rows; this is not a
claim of that many individual monster portraits.

Unresolved native NPC portraits: Matildie and Rabid Wolf, I.M. Custom Zenith
Guide/Scout/Atlas/Outpost and the invisible weighted-stones marker need suitable
in-game captures. Unillustrated monster rows: Hydra, Tinnin, Chigoe, Berried
Chigoe, Armed Gears and Ob. They retain ordinary text and source links.

The three new job articles document only the delivered Job Balance v1.0 changes
for SMN, DRG and PLD; WAR/THF documentation preserves earlier Zenith adjustments.
They explicitly mark installation as unconfirmed. No fabricated job mechanics
were added to accompany the other artwork.

Validation: all acquired images decoded successfully and matched their recorded
hashes. Official job art, supplemental NPC images and family replacements were
visually reviewed. Existing full wiki and zone checks pass. These checks concern
the website, not installation of the downloadable server package.
