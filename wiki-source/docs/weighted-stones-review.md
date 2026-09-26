# Weighted Stones review — 25 September 2026

## Evidence and scope

The user reported that the floor-level acquisition target was absent in Garlaige Citadel at the wiki location. This is a game availability problem as well as a missing guide.

The reviewed server export has NPC 17596841, script qm17, position [-354.945, -0.162, 262.339], model 53, status normal, and content abyssea. Its captured main settings have RESTRICT_CONTENT=1 and ENABLE_ABYSSEA=0. These are captured settings, not a live connection to the running server.

At pinned LandSandBoat revision f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4, qm17.lua opens event 23 when the key item is absent and awards POUCH_OF_WEIGHTED_STONES (1846) on option 1. There are no level, fame, mission, job or fee checks. The NPC loader moves content-disabled targets to 0,0,0 and makes them disappear. Restoring visibility alone would therefore be incorrect.

The targeted correction removes only this target's Abyssea tag after checking the live file on the user's computer. It does not globally enable Abyssea or award the item without the event. Offline validation does not prove the Windows installation or client interaction has succeeded.

## Door behavior

Reviewed _5k0.lua, _5k9.lua and _5ki.lua: a closed gate and ownership of the key item cause a 1500 ms delay, then a 15-second opening. Each works from either side and retains the key item. The original pressure-switch method remains.

## Website changes

- Four connected articles: acquisition, permanent key item, target and Banishing Gates.
- Registry entry in quest_guides.py supplies shared identity, location and reward.
- Links from Quests, Items, NPCs, Travel, Garlaige Citadel and First Limit Break.
- Entrance route uses present-day Map 1 (G-8); map caption distinguishes the unrelated Divine paint marker.
- The 2012 origin is documented as an optional later travel convenience, not misrepresented as original level-75-era content.
- Source availability, package readiness and an in-game test are not conflated.

## Sources

- https://www.bg-wiki.com/ffxi/Pouch_of_weighted_stones
- https://ffxiclopedia.fandom.com/wiki/Pouch_of_weighted_stones
- https://horizonffxi.wiki/Banishing_Gate
- https://forum.square-enix.com/ffxi/threads/24155-June-14-2012-%28JST%29-Version-Update
- https://github.com/LandSandBoat/server/blob/f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4/scripts/zones/Garlaige_Citadel/npcs/qm17.lua
- https://github.com/LandSandBoat/server/blob/f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4/src/map/utils/zoneutils.cpp

## Remaining coverage

The adjacent quest-coverage-2026-09-25 report audits the pre-change site. It is a lower bound: the imported WotG areas lack quest rows, and simple title coverage is not a full content audit. Do not describe the site as a complete level-75 wiki. Missing walkthroughs must be researched against the Zenith base and authored as actual articles; a list of external quest names does not count as local walkthrough coverage.
