# Past-zone maps: alternate-source delivery

Ready to integrate: `past-maps-alt.json`, 68 original 512×512 GIF assets for 9 zones, with source page/image URLs, dimensions, SHA256 and local paths. No failed downloads remain.

| Zone | Images |
| --- | ---: |
| Xarcabard (S) | 1 |
| Beaucedine Glacier (S) | 1 |
| Castle Zvahl Baileys (S) | 4 |
| Castle Zvahl Keep (S) | 4 |
| Windurst Waters (S) | 2 |
| Fort Karugo-Narugo (S) | 2 |
| Ghoyu's Reverie | 18 |
| Everbloom Hollow | 18 |
| Ruhotz Silvermines | 18 |

Original source is FF11 Database, https://ff11db.sakura.ne.jp/database/map/. The specific past variants or named instances were checked against the original page headings. All original Japanese annotations and map credits remain unchanged. These are published map references, not Zenith custom markers. The requested FFXI Atlas homepage was temporarily only “BRB”; BG/Fandom direct image discovery was unavailable.

All 68 files passed PIL decode/size checks and checksum verification. All 14 outdoor/city/castle maps were visually inspected. A further 10 instance images were inspected: maps 1/9/18 for Ruhotz and Everbloom, maps 1/9/17 plus 9-1 for Ghoyu. Per-file `visuallyVerified` reflects those actual checks; all files have source and binary verification. Do not relabel the unviewed layouts as visually inspected.

Ghoyu's Reverie has 17 numbered layouts plus a second annotation of map 9. The HTML accidentally reuses `USEMAP="#Map9"` for that image, but its heading and anchor explicitly say `MAP9-1`. The manifest corrects the ID to `Map9-1`. Map order is numeric in the final manifest. Instance map galleries represent multiple layouts; they should not imply all maps are used by every mission.

## Throne Room (S)

There is no in-game map for this zone. FFXIclopedia states “Maps: None” and map acquisition N/A; an official forum report independently states no map and no coordinates. The manifest records this under `noMapZones`, with sources. If route imagery is needed, use Castle Zvahl Keep (S), map 4 (`s_zvahl8.gif`) showing its west exit at G-7, explicitly labelled as the approach. Do not assign a present-day Throne Room image as a past-zone map.

Source evidence:
- https://ffxiclopedia.fandom.com/wiki/Throne_Room_%28S%29
- https://forum.square-enix.com/ffxi/archive/index.php/t-19132.html

Integration must preserve the asset captions/source links and clearly label Japanese annotations. Do not rerun `acquire.py` after integration without also running `finalize.py`; the latter fixes order, map 9-1 identity, provenance checks and no-map metadata.
