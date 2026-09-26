# Mission coverage audit — 25 September 2026

Baseline before expansion authoring: 60 concise national walkthroughs exist,
20 for each nation. The Missions category has those 60 pages, three national
hubs and one directory. No expansion mission walkthroughs or expansion hubs
exist. The directory explicitly says expansions are outside the current release.
Only nine national pages have configured route-map galleries. Requirements and
numbered steps are present; many later routes are concise and rely on reference
links for finer navigation. They must not be described as fully illustrated.

`inventory.json` and `inventory.csv` enumerate the baseline. `audit.py` rebuilds
them without changing the site. It classifies structural presence, not factual
completeness or live gameplay success. Native filenames retain their own spelling.

| Story campaign | Baseline authored | Missing inventory entries |
|---|---:|---:|
| San d’Oria | 20 | 0 |
| Bastok | 20 | 0 |
| Windurst | 20 | 0 |
| Rise of the Zilart | 0 | 18 |
| Chains of Promathia | 0 | 34 main/epilogue + 5 required branch guides |
| Treasures of Aht Urhgan | 0 | 48 |
| Wings of the Goddess | 0 | 54 |
| A Crystalline Prophecy | 0 | 12 including finale marker |
| A Moogle Kupo d’Etat | 0 | 15 including finale marker |
| A Shantotto Ascension | 0 | 15 including finale marker |

RoZ and CoP share The Last Verse and require the three intervening epilogue
quests: Storms of Fate, Shadows of the Departed, Apocalypse Nigh. Those three
quests are separate missing entries. CoP 3-3's two routes and 5-3's three paths
need fully actionable branch directions, even if embedded within parent pages.
WotG requires national quest chains; an expansion mission list alone is not
sufficient. The inventory flags selected early prerequisite quests, but does
not pretend to enumerate the entire WotG national chains. Assault and Campaign
Ops are separate operational systems and need separate inventory work if “all
missions” includes those systems.

## Enabled content and source limits

Captured `settings/main.lua` (not default settings) enables ROTZ, COP, TOAU,
WOTG, ACP, AMK and ASA; RESTRICT_CONTENT=1 and MAX_LEVEL=75. Abyssea, SoA,
RoV, TVR and Voidwatch are disabled. A content flag is not a playability test.
Do not equate the entire current WotG campaign with a strict historical
level-75 release cutoff without a separate release-date review.

Native revision: `f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4`.
The GitHub tree is complete (not truncated). RoZ handlers are under **rotz/**,
not zilart/. CoP has 33 main numbered handlers plus helpers; The Last Verse
is a shared epilogue state. AMK finale is a mission enum state without its
own numbered file. Absence of such a file does not establish absent content.

## Priority and exact unlocks

1. Create RoZ and CoP hubs with explicit entry prerequisites and named unlock
   milestones. Add all actual walkthroughs, chapter branches and needed access
   quests; do not use a list of outbound links as the completed deliverable.
2. Sky: Rank 6 allows the Norg opening (RoZ1). RoZ12 yields the Cerulean Crystal
   from Maryoh Comyujah after Ancient Vessel/papyrus. Take it to the Hall of
   the Gods and see the gate/circle cutscene to advance to RoZ13. Use the
   Shimmering Circle and enter Ru’Aun Gardens. Its arrival cutscene completes
   RoZ13 and starts Ark Angels. No need to complete Ark Angels to use Sky.
3. Sea: beat Tenzen in CoP7-5, watch the Sealion’s Den post-battle scene and
   Al’Taieu arrival scene. Native7-5 completes on that arrival and begins8-1.
   Access to Al’Taieu does **not** require completing8-1. Re-entry through
   Sueleen becomes available after7-5 completion. Do not attach a Limbus entry
   claim without listing its separate requirements.
4. CoP starts through Lower Delkfutt’s Tower, Upper Jeuno, then Monberaux;
   Rank6 is a RoZ condition, not a CoP opening requirement.
5. Follow with ToAU, WotG plus compulsory national quests, and all three
   add-ons. Improve existing national galleries/route precision while preserving
   their stable URLs. The user explicitly asked for requirements, steps, NPC
   images and maps, not counters or a redesigned dashboard.

## Sources retrieved 2026-09-25

- https://horizonffxi.wiki/Zilart_Mission_1
- https://horizonffxi.wiki/Zilart_Mission_12
- https://horizonffxi.wiki/Zilart_Mission_13
- https://horizonffxi.wiki/Promathia_Mission_1-1
- https://horizonffxi.wiki/The_Warrior%27s_Path
- https://horizonffxi.wiki/Promathia_Mission_8-1
- https://horizonffxi.wiki/Category:Rise_of_the_Zilart_Missions
- https://horizonffxi.wiki/Category:Chains_of_Promathia_Missions
- https://api.github.com/repos/LandSandBoat/server/git/trees/f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4?recursive=1

Native supporting files are saved under `native/scripts/` here: RoZ01,12,13,
CoP1-1,7-5,8-1, Hall of the Gods Cermet Gate and Shimmering Circle. The
native CoP7-5 event chain and RoZ13 completion are verified from those bytes.
No server files were edited and no live game test was performed.
