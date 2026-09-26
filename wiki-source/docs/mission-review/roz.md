# RoZ mission contribution — 2026-09-25

Deliverable: `roz-missions.json`. 22 validated records: numbered RoZ 1–18, with Q1 Storms of Fate, Q2 Shadows of the Departed, Q3 Apocalypse Nigh and Q4 Divine Might. Q1–Q4 have `kind: quest` and explicit slugs; 18 is the joint CoP/RoZ final-log entry. These are editorial walkthroughs; no live Zenith completion or solo-battle claim was made. Parent owns images/maps and site integration.

All Horizon numbered mission pages 1–17, their revision IDs/timestamps, and supporting key-item/route pages were fetched through MediaWiki and saved in raw/. All 17 native RoZ scripts, four relevant quest definitions, and 11 relevant battlefield definitions were fetched at LandSandBoat commit f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4. JSON source/code arrays preserve exact URLs. Complete source payloads in raw/ are research inputs, not intended for publishing. Authoring used original concise summaries, not wholesale wiki text. Long ZM4 has independent Paintbrush, Lantern, key and native sources; ZM5 is condensed to 199 words over its requirements/walkthrough/notes/reward. ZM16's outer corridor is verified against the independently retrieved FFXIclopedia mission page and native battlefield. Ending source-specific requirements come from pinned quest logic.

## Critical checks

- Start: Rank 6 in the current nation at Norg. National Shadow Lord mission is 5-2; an inaccurate native comment saying 5-1 was not repeated. Postponed native RoZ introduction resumes from Tales' Beginning H-9, rather than assuming re-entry always starts it.
- Sky: Maryoh grants Cerulean Crystal during ZM12. Hall's Cermet Gate allows crystal holders through. ZM12's final native trigger is Shimmering Circle event 3; it advances to ZM13. Ordinary circle lift requires mission at least ZM13. Ru'Aun Gardens arrival event 51 completes ZM13. Ark Angels/Eald'narche are not first-Sky prerequisites. Optional teleport access was not conflated with this route.
- ZM12 Ancient Vessel: recheck qm7 after killing before zoning; its kill flag is local. Native prompt range 1.5 yalms.
- ZM14: Blank Target mission scene required before shard credit. Divine Might needs its additional quest flag for earring; optional, not mandatory.
- ZM15: native progression is Oaken Door event 172 then shrine zone-in; ordinary Gilgamesh event 173 does not set that state.
- ZM16 entrance is Celestial Gate, not Qe'Lov Gate. Route includes the outer corridor between Dark Elemental rooms, omitted by some shorter guides.
- Awakening: both epilogue bits must be set; it remains active until Apocalypse Nigh reward events 232/234. The Last Verse is a terminal entry, not an additional boss mission.
- Storms requires CoP Dawn Status 8. Shadows requires finished Storms, Awakening Status 3 and its wait. Apocalypse requires finished Shadows, its wait and zone change; after Sealion's Den, native progress is Hu'Xzoi Gate of the Gods `_iya`, not arbitrary zoning into Ru'Hmet.
- Base waits are next Vana'diel day. Optional era modules restore JST midnight. Parent confirmed reviewed modules/init.txt contains only custom/zenith, so the records describe base logic with a snapshot caveat. Horizon's inconsistent weekly-tally note was not imported.
- Base Apocalypse Aldo checks current-nation Rank >=5, whereas Horizon says 6. Base victory timer begins at battlefield completion, before Aldo. Documented without changing the server.
- Base Divine Might pentasphere creation accepts full-moon 18:00–05:59, with no weather check. The classic clear 00:00–03:00 route remains compatible and its narrower rules are labelled.
- Main RoZ BFs, Storms and Apocalypse explicitly allow Trusts in pinned definitions. Their 30-minute limits and six-person limits (18 for Storms) are documented as source checks only. Actual global options and combat balance were not tested.
- No Horizon wardrobe-slot or HAAP rewards were carried into Zenith claims. No blanket level 60/65 entry requirement was invented from wiki strategy recommendations.

## Known editorial limitations

- ZM5 Fire headstone is inconsistently labelled L-6 vs L-7 by Horizon's fragment and mission pages; records say near the L-6/L-7 tunnels, with precise route through Ifrit's Cauldron. Native monument coordinates are x491,y20,z301.
- Quicksand weight doors list traditional player weight requirements, and do not claim Trusts activate them. A site-installed shortcut or single-player gate override would need its own evidence.
- NPC portraits and maps are not bundled by this agent; the `zones` and `start` fields are prepared for the parent's already-licensed/source-attributed local assets.

Regeneration: run author.py, then finalize.py. `finalize.py` corrects the final names, adds native/era qualifications and validates schema, IDs and nonempty guides.
