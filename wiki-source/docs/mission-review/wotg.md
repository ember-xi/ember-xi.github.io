# WotG walkthrough audit

## Deliverables

- `missions.json`: every main Wings of the Goddess mission, numbered 1–54, including short cutscene chapters.
- `memory-quests.json`: all nine Her Memories journal quests. Homecoming Queen contains three child quests; one of the three Footfalls branches supplies fragment IV. All three branches are documented, without requiring all three.
- `build_data.py` and `build_memory.py`: reproducible authoring sources.
- `native-audit.json`: pinned file inventory, SHA-256, callback counts, TODO excerpts, and interpreted status.
- `native/`: primary script evidence. These are research copies, not patches to the server.

Past national story walkthroughs are separate delegated deliverables: 13 San d'Oria [S], 13 Bastok [S], and 13 Windurst [S] records including each recruitment quest. They must be merged and linked alongside this data. Images and maps are supplied by the parent integration.

## Scope and availability

Pinned LandSandBoat revision: `f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4`.

All 54 main mission files exist and contain native progression logic or delegate to helpers. That fact is not proof that every battle can be entered and completed. `implemented-handler` means relevant handler logic was found; it does not mean a live Zenith character completed the mission. There was no live server or game-client test in this research task. An enabled expansion flag also does not establish completeness or level-75 balance.

Nine main missions contain explicit pending battle or instance integration:

| Mission | Missing or incomplete integration |
|---|---|
| 14 A Nation on the Brink | Everbloom Hollow instance; mission script assumes a future return event |
| 23 Dungeons and Dancers | Everbloom Hollow maze instance and failure/return integration |
| 24 Distorter of Time | Ruhotz Silvermines battle and failure/return integration |
| 31 Prelude to a Storm | Ghoyu's Reverie instance and victory-return integration |
| 32 Storm's Crescendo | Ghoyu's Reverie relay instance and victory-return integration |
| 33 Into the Beast's Maw | Distress-flare instance entry and victory-return integration |
| 37 Darkness Descends | Throne Room [S] battlefield victory hookup |
| 46 When Wills Collide | Walk of Echoes battlefield ID and victory hookup |
| 51 Maiden of the Dusk | Walk of Echoes final battle entry and victory hookup |

All nine records have `native_status: partial` and an explicit `availability_note`. A later chapter with cutscene handlers can still be unreachable through normal play because of an earlier blocker. Do not identify mission 14 as necessarily the first overall blocker: national prerequisite quests have their own incomplete battles, audited by the national-chain agents.

Mission 41 delegates fragment completion to `helpers.lua` and the Her Memories quests. It is not simply an empty stub. However, **Her Memories: Verdure Footfalls** has no quest handler in the complete pinned GitHub tree (22,628 entries, not truncated), and no corresponding legacy fallback was found in the fetched Windurst Waters [S] / West Sarutabaruta [S] NPC, Zone and DefaultActions scripts. This branch is marked `missing-handler`; mission 41 also has a prominent partial-availability note. The Bastok and San d'Oria memory branches have handlers.

The main mission-7 battle is genuinely distinct from these gaps: `scripts/battlefields/La_Vaule_[S]/purple_the_new_black.lua` and `scripts/zones/La_Vaule_[S]/mobs/Galarhigg.lua` accompany its mission handler. Native paths use `[S]`; the data uses that convention consistently in display and zone-link fields. Wiki URLs retain their canonical `(S)` spelling where needed.

## National prerequisites

`scripts/missions/wotg/helpers.lua` checks a qualifying chain from any one past nation. Past allegiance is independent of the player's present-day nation. National quests are in the Crystal War quest log, not the WotG mission list.

| Main mission gate | San d'Oria alternative | Bastok alternative | Windurst alternative |
|---|---|---|---|
| Finish 2, begin 3 | Claws of the Griffon | Fires of Discontent | The Tigress Strikes |
| Finish 3, begin 4 | Wrath of the Griffon | Burden of Suspicion | A Manifest Problem |
| 8 | In a Haze of Glory | Fire in the Hole | A Feast for Gnats |
| 15 | Bonds That Never Die | Honor Under Fire | The Forbidden Path |
| 26 | Blood of Heroes | What Price Loyalty | Howl from the Heavens |
| 38 | Face of the Future | Bonds of Mythril | At Journey's End |

The actual helper call locations resolve potentially confusing helper names. Day waits marked TODO in those helpers are not imposed by this guide. Actual native day/zone waits, for example Amaura's tonic and the Grauberg scenes, are retained.

## Historical level-cap boundary

- Main missions 1–38 were available by March 2010, although the national finale needed by mission 38 was released in the June 2010 update as the cap started rising.
- Main missions 39–44 and the Her Memories quests were released in September 2010.
- Main missions 45–54 were released in December 2010.
- The later chapters remain documented for story continuity and carry an era note. Their inclusion is not a claim that their retail balance, entry configuration, or Zenith implementation is suitable for level 75.

Useful dated sources:

- https://www.playonline.com/pcd2/topics/ff11us/detail/5449/detail.html — May 20, 2010 announcement of the upcoming national finales.
- https://www.playonline.com/pcd2/topics/ff11us/detail/5702/detail.html — August 19, 2010 announcement of the next WotG missions.
- https://www.bg-wiki.com/ffxi/September_2010_Version_Update_Changes — enumerates By the Fading Light through Glimmer of Life and the nine memory quests.
- https://www.playonline.com/pcd2/topics/ff11eu/detail/5910/detail.html — November 11, 2010 finale announcement.
- https://www.bg-wiki.com/ffxi/December_2010_Version_Update_Changes — final main-story update.

## Research and editorial choices

Walkthrough text is newly written and concise. The primary evidence is pinned native mission/quest logic; BG Wiki, FFXIclopedia and the Japanese FF11 terminology wiki supply route and battle details. Per-mission sources and pinned code links are preserved. Eden/Horizon do not provide complete later-WotG coverage, so their absence was not filled with invented server-specific behavior. A similarly named public `wiki.zenithxi.com` mirror is unrelated to the user's installation and was not used as evidence of Zenith availability.

Material code/reference differences are made explicit: Dancers in Distress chooses its requested item randomly in this core; Grave Resolve requires an examination before the Lilac trade; Forget Me Not completes after its automatic Grauberg visit and return to a Jeuno maw. The guide does not promise Trust support, a battle level cap, solo viability, current retail travel shortcuts, or a server-ready instance where none was verified.

The Dungeons and Dancers maze route and Storm's Crescendo circuit have concrete instructions. The latter names all 24 operative objective, smoke cues, circuit direction and linked map numbers; exact geometric relay maps should accompany the parent image/map integration. No large wiki passage or dialogue was copied. The guide is not a substitute for testing the unfinished content once implemented.
