# Item references and shared wiki layout

The 23 September 2026 request applies the Eden Magicite page structure to the complete Zenith wiki: a two-column facts table before the walkthrough and a Contents box alongside it. Use Zenith's verified content. Quest indexes retain NPC, Quest, Reward column order.

Item names link to acquisition references. Show documented monster names, native game-map squares, recipes with quantities and skill caps, NPC sources, and the exact Auction House category. Preserve all existing item URLs and the unchanged 689-item package price catalogue.

Native acquisition data is pinned to LandSandBoat f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4, matching the package baseline. Custom rewards take precedence and link back to their quest. Import only actual nonzero drop entries; do not infer guaranteed drops or rates. World coordinates never appear as player directions. Omit unverified grid cells rather than estimate them.

Fixed supply prices, automatic buyer limits, restocking targets, live stock, and completed sales are distinct. Single and full-stack values are separate. The website has no live connection to the local Windows database. Native history reads up to ten completed sales by item and stack flag; no fabricated transactions are added. Documentation changes do not imply a server installation.

The data importer is tools/import-item-sources.py. The page generator is content/english/item_guides.py. Rebuild with tools/build-wiki.py and validate with tools/check-wiki.py.
