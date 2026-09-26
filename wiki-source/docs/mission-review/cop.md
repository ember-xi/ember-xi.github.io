# Chains of Promathia mission authoring

Final deliverable: `cop-missions.json` — 38 complete records: all 33 numbered missions from 1-1 through 8-4, two 3-3 branches, and all three 5-3 paths. Shared epilogue quests / The Last Verse are being supplied separately by the RoZ author.

All authored English prose is original. Local source snapshots: `source/` (Horizon pages, supporting item/route pages, all 34 pinned native CoP Lua files, battlefield and critical NPC handlers), and `late/` for chapters 6–8. Native commit: f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4. Sources/code URLs are embedded per record. Main records have native_status=implemented, which means the pinned upstream mission handler exists, not that this user's live install has been completed or exhaustively tested.

## Critical corrections / confirmed requirements

- CoP starts by entering Lower Delkfutt's Tower from Qufim, then Upper Jeuno/Monberaux; it has no national Rank 6 requirement.
- First Promyvion boss win completes 1-2; the other two complete 1-3. Entry alone is insufficient.
- Aqueducts route includes Minotaur, the ladder scene, lamp puzzle, Ornate Gate scene and Justinius report. Fighting Minotaur alone is insufficient.
- Road Forks requires both city paths. Windurst needs the entire mirror NPC chain, Lioumere, 30-minute Mimeo Jewel climb and the three feather conversations.
- Sacrarium requires two openings of the two-lock gate. Small-key trader is held in a cutscene; Large-key trade occurs during it. Temple Knight Key bypass exists in both native keyhole handlers and is obtainable after A Hard Day's Knight by trading both keys to Quelveuiat.
- Native 5-1 treats Chasalvige / Anoki as optional clues; Horizon currently claims they are required. The guide includes them but clearly describes the native distinction.
- Light of Vahzl is obtained on initial Vahzl arrival in 5-1, not after the 5-2 battlefield. Corrected against native code.
- All three Three Paths branches are fully spelled out and linked by branch_of=5-3. Tenzen includes both separate Pso'Xja towers, two Batallia ??? interactions, and post-Disaster-Idol door. Ulmia includes both BCs. Louverance includes Cid before the Gold Key trade and a final Cid report.
- Tarnotik's Snow Lily travel is native and enabled when current CoP mission >= Three Paths. Gold Key trade requires the post-battle Cid scene.
- Native battlefield caps use MAX_LEVEL. Most reviewed mission battles explicitly allow Trusts. Flames for the Dead does not set allowTrusts and therefore inherits false from scripts/globals/battlefield.lua. The record explicitly distinguishes that exception and optional era overrides.
- Horizon's 45-second Snoll fuse is not the pinned native implementation: native Snoll grows through timed stages and has timed / TP-triggered combustion at the final stage. The guide labels the 45-second number historical.
- See `late/REVIEW.md` for exact Sea arrival, Dawn farewell/ring and late mission handling. Sea opens after Tenzen 7-5 victory AND Sealion departure / Al'Taieu arrival scenes, before completing 8-1.

## Source allocation

Short records remain comfortably below 200 words. Longer combined branches rely on distinct sources for different facts: native for mission-state order and keys; Horizon mission article for field grids; separately retrieved Parradamo Tor for its climb route; separate Sacrarium page for maze/door practical details; separate item pages for chips and Gold Key; Tarnotik / Newton navigation for transport; separate battlefield and mob scripts for Trust/cap/timer behavior. No wiki paragraphs were copied. The same mission source is not used to justify invented Zenith customization.

## Known limits / illustrations

- Actual enabled optional era modules and local Zenith overrides are not resolved by this author; records do not promise live entry rules or solo success.
- Existing local zone maps should illustrate each record via its zones array. The full Hu'Xzoi / Ru'Hmet map sets are necessary for escort and tower routes.
- Parradamo Tor needs a useful climb illustration beyond the broad Attohwa zone map. A separately retrieved `parradamo-tor-route.jpg` plus `tor-imageinfo.json` are supplied for parent inspection/integration.
- Do not assign unrelated NPC/monster portraits as mission art. Relevant exact portraits can be added by the existing site image mapping.
- No Sites or server files were edited. All work is confined to work/missions-cop.
