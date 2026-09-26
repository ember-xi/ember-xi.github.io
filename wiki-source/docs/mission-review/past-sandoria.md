# San d’Oria [S] story quests — 2026-09-25

Deliverable: past-sandoria.json. Thirteen original reference walkthroughs, S-00 Steamed Rams plus S-01 through S-12 (Gifts of the Griffon through Face of the Future). All requested schema fields, unique slugs and nonempty route steps validated. Every code URL was checked against the full pinned Git tree; all zones match current site's zone-data display names. Each article's requirements/walkthrough/notes/reward totals under 200 words before the independently sourced native implementation caveat.

No Site files edited. No server changes made. These articles are source-verified descriptions, not live test results. Parent must render era_note prominently, especially implementation_status=incomplete-reference.

## Sources read

All 13 scripts/quests/crystalWar/WOTG_SAN_*.lua files fetched at LandSandBoat f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4 and read in full. Native helpers at scripts/missions/wotg/helpers.lua were read. All external walkthrough source pages were retrieved via web-search cached results; direct BG requests returned 403, so no HTML-only acquisition is claimed. Quest-specific cache queries recovered deep route details. BG supplied Steamed/Gifts/Claws/Perils/Haze/Price/Bonds/Songbirds/Blood/Face. FFXIclopedia supplied Boy/Wrath/Chasing. Exact URLs are in each record.

## Main-story gates

- S-02 Claws: permits Back to the Beginning → Cait Sith.
- S-03 Boy: requires Back to the Beginning finished, Cait Sith active.
- S-04 Wrath: permits Cait Sith → The Queen of the Dance.
- S-05 Perils: requires Purple, The New Black finished.
- S-06 Haze: permits In the Name of the Father progression.
- S-07 Price: intended Crossroads of Time gate (A Nation on the Brink completed). Native quest acceptance omits that check, explicitly noted.
- S-08 Bonds: permits Crossroads progression.
- S-09 Songbirds: requires The Will of the World completed, Fate in Haze active.
- S-10 Blood: permits Fate in Haze progression.
- S-11 Chasing: intended Adieu, Lilisette gate, Darkness Descends completed. Native acceptance omits that check.
- S-12 Face: permits Adieu, Lilisette progression; automatically accepted after Chasing.

## Concrete pinned-base gaps

1. S-06 In a Haze of Glory: native completion handler explicitly assumes an unimplemented Ghoyu's Reverie instance. Full Git tree contains only scripts/zones/Ghoyus_Reverie/instances/doomvoid.lua; no mission instance.
2. S-08 Bonds That Never Die: only post-instance handlers are provided. Full Git tree has only scripts/zones/Everbloom_Hollow/instances/doomvoid.lua; Young Behemoth mission instance absent.
3. S-09 Songbirds: native quest explicitly flags Orcish Bloodletter as awaiting implementation/verification and set to a very high level. No normal level-75 completion claim.
4. S-10 Blood of Heroes: Forbidding Portal instance entry TODO and completion-event assumption; no matching Ghoyu instance in tree.
5. S-11 Chasing: explicit placeholder level-150 Menechme, helper Excenmille not spawned/level0. Also Blood's completion calls xi.quest.setVar without the 'Timer' key argument, while Chasing reads Timer; records preserve intended next-day guidance but flag source discrepancy.
6. S-12 Face: native entry notes/completion assumptions, matching Everbloom instance absent. Clandestine Marking is explicit native source of replacement infiltration kit; full ending transition handlers exist but battle is not complete.

These gaps cannot be repaired by changing a website guide. The full reference routes are retained, with explicit implementation caveats, to avoid implying that every documented mission is playable on the current server.

## Important route distinctions

- Claws: must enter Jugner[S] from East Ronfaure[S].
- Boy: correct herb color depends on collection time, not turn-in time: red 00–07:59, blue08–15:59, green16–23:59.
- Haze: native reward conversation at Rholont only 18:00–23:59.
- Price: collect the Underbrush victory scene before zoning; native kill flag is local.
- Songbirds: fishing targets are key items; Flint trade at Charred Firewood two terrain levels above I-7 tower.
- Chasing: Xarcabard[S] arrival from Beaucedine[S], later Batallia[S] arrival from Beaucedine[S] both required. Exact footprint order supplied.
- Face: routes deliberately use present-day Batallia/Jugner/Ghelsba/Yughott; finale requires the Batallia maw previously unlocked from past.
- Modern ilevel119 reassurance, Home Point shortcut prerequisites such as Beyond Infinity, Abyssea Atma rewards and automatic trust-unlock promises were omitted.
