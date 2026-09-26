# Past-era zone map acquisition — 2026-09-25

Deliverable: `past-maps.json` has **20 exact zone names and 50 preferred images**. `alternateSources` preserves all 30 FF11 Database images (17 zones), including six maps superseded by English Remapster variants. Every selected original raster has localPath, width, height, source page, direct source URL, SHA-256, byte size, language, and attribution.

## Sources and exact variants

- English maps: AkadenTK/remapster_maps, pinned commit `831bf3f2a27cc8581cb098af554f07bf70707420`, original 1024-pixel wiki PNGs. Verified repository file names explicitly use `_s` for past areas. Visually checked Southern San d'Oria[S], Bastok Markets[S], Batallia Downs[S], Rolanberry Fields[S], East Ronfaure[S], and Eldieme[S] map 2; all display the past-era name. License CC-BY-SA-4.0, copied unchanged as REMAPSTER-LICENSE.txt. Existing source logo/attribution retained. Walk of Echoes uses original zone's 18 files; the separately named `walk_of_echoes_p2_*` files were excluded.
- FF11 Database: exact `s_` past-era HTML pages, decoded Shift_JIS and verified English headings with `(S)` or `[S]`. Images extracted only from `<IMG ... USEMAP="#MapN">`, excluding item icons. Original GIFs are 512x512. These maps contain Japanese annotations, English NPC names/links, and coordinate grids. Grauberg[S] visually checked for past Pashhow/North Gustaberg links and proper terrain. Page originals saved beside assets for source audit. Copyright credit from source is retained in metadata.
- Every file decoded with Pillow, image dimensions checked, and SHA-256 validated after consolidation. No generated images, added pins, present-day substitutions, or altered source imagery.

## Integration

- Read `zones` for the preferred set, not the older intermediate `acquired-maps.json` (that intermediate records initial strict-heading parser failures, subsequently fully repaired in `ff11db-maps.json` with zero errors).
- The other ten inventory zones were assigned to the CoP agent at `work/missions-media/past-maps-alt`: Windurst Waters(S), Fort Karugo-Narugo(S), Beaucedine(S), Xarcabard(S), Castle Zvahl Baileys/Keep(S), Everbloom Hollow, Ruhotz Silvermines, Ghoyu's Reverie, and Throne Room(S). Merge its manifest separately.
- Remapster and FF11 Database maps are reference material. Modern source annotations, Home Points, or Walk of Echoes layouts must not be presented as proof that the corresponding service/event is enabled on Zenith or available under its level-75 rules.
- No Site checkout files were changed.
