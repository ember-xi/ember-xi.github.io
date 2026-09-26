# Bastok [S] national quest chain — research handoff

Output: `bastok-past-quests.json` — 13 articles, B-00–B-12, 79 ordered steps. Each has requirements, start location, route, notes, reward, main-story unlock, canonical `[S]` zones, BG/FFXIclopedia references, pinned native source and an implementation status. Original guide summaries; no copied dialogue. Images/maps are left to the parent integration.

## Native audit

Pinned LandSandBoat revision: `f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4`.

All 13 quest bodies were read; finding a script alone was not treated as proof of playability.

- B-00: route/rewards implemented. Campaign allegiance checks still have TODOs; first-enlistment route documented. The script allows an Adelbrecht dialogue without the Blue Recommendation Letter; guide gives the normal first-enlistment letter route and does not assert a tested allegiance switch.
- B-01–05: progression present. B-03 has an actual instance, ten enemies and seven-kill success logic. Known TODO: player locking during the entry cutscene, risking aggro. B-03 initial day wait is also TODO. B-04/B-05 native timers are enforced.
- B-06 Fire in the Hole: `Fire in the Hole instance is not implemented currently` in quest source.
- B-08 Honor Under Fire: missing Everbloom Hollow instance explicitly marked in quest source.
- B-10 What Price Loyalty: missing Everbloom Hollow instance explicitly marked in quest source.
- B-12 Bonds of Mythril: missing Throne Room battlefield explicitly marked in quest source. Keep Imp counter, Gargouille Warden trigger and Passkey steps do exist.
- B-07/B-09/B-11: their own scene/progression handlers exist, but access depends on earlier missing battles. `availability_note` explains this instead of describing them as presently completable.

B-06/08/10/12 each has `native_status: partial_battle_unimplemented` and a prominent explanatory `availability_note`. Full intended reference battle/follow-up routes still included, without claiming implementation, successful live tests, or live Trust eligibility. No native game files changed.

## Interleaving with WotG

Agreed with missions_wotg agent:

- B-02 permits finishing Back to the Beginning (2).
- B-04 permits Cait Sith (3) → The Queen of the Dance (4).
- B-06 requires and permits continuing In the Name of the Father (8).
- B-08 requires and permits continuing Crossroads of Time (15).
- B-10 requires and permits continuing Fate in Haze (26).
- B-12 requires and permits continuing Adieu, Lilisette (38).

B-05 native start does not additionally check mission 8; B-06 does. B-07/B-08 require current mission ≥15; B-09/B-10 ≥26; B-11/B-12 ≥38.

## Wait / reward corrections against retail guides

- B-01 sets `needToZone(true)`; B-02 has no extra timer.
- B-03 initial game-day wait is TODO; no real-world midnight instructed.
- B-03 completion writes B-04's next Vana'diel day + must-zone conditions.
- Blatherix after B-04 gives the Elixir and starts B-05's next Vana'diel day + must-zone conditions. This is required; it is not merely an optional reward pickup. B-04's direct reward is its title.
- B-05, B-06, B-07 opening scenes require entering Bastok Markets [S] from North Gustaberg [S].
- B-07, B-09, B-11 native starts do not enforce the extra day waits listed in retail walkthroughs.
- B-11 allows one Imp trade attempt per Vana'diel day; Elixir is not consumed. The answer changes by day. All three answer patterns are documented.
- B-11 native header incorrectly locates the Imps/objects in Baileys: active handlers and reference maps place them in **Castle Zvahl Keep [S]**. Data follows the handlers.

## Useful retrieved sources

BG/Fandom pages were retrieved via search cache; their direct sites often return 403/402 from tools. Horizon API returned missing pages for all 13 quests, so no unsupported Horizon attribution is added. Main web refs parent can open/search to cite if desired:

- `turn290search3`: The Truth Lies Hid — full Imp puzzle and route.
- `turn290search1`: Bonds of Mythril — four Imps, Gargouille, final two-stage fight.
- `turn292search2`: Honor Under Fire — complete reference entry and fight.
- `turn292search4`: What Price Loyalty — full route and portal I-7.
- `turn292search6`: Burden of Suspicion — middle G-9 pit → map2 east → map3 I-7 Sarcophagus; Blatherix Elixir.
- `turn296search3`: Beneath the Mask — complete route, Red Axe I-8 and Hoarfang F-10.
- `turn298search1`: Fire in the Hole — escort waves, post-battle scenes.

QA: all 13 sequential identifiers, source filenames, required fields and start-zone inclusion validated. No live server gameplay test was performed.
