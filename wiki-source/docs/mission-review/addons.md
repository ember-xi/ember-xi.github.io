# Add-on mission content handoff — 25 September 2026

Import `missions-addons.json`, or the three separate `acp.json`, `amk.json`, `asa.json` lists. `author.py` rebuilds all four. `python work/missions-addons/validate.py` checks the schema, sequences, required route fields and internal consistency.

There are **42 entries**: ACP 12, AMK 15, ASA 15. Three are explicit completion/reward markers, so this is 39 sequential playable story stages plus 3 log markers, not 42 battles. The records contain original English requirements, route steps, coordinates, rewards, source links and pinned native evidence. Parent owns images/maps and Site integration; these files contain no imported images and do not change the Site.

The reviewed native revision is `f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4`. Framework placeholders do **not** establish that a mission is unplayable: legacy zone handling exists for ACP 5 (Fei'Yin), ACP 8 (Hall of the Gods) and ACP 9 (Lower Delkfutt's Tower). Other legacy coverage and every live Zenith completion remain unverified. Per-record availability notes preserve this distinction.

Concrete native issues for a future server audit, not changed by this content work:

- AMK 6: code maps Cups to impact and Batons to piercing; the wiki maps Cups to piercing and Batons to blunt. Guide recommends all four orbs, avoiding a disputed single-orb damage assumption.
- AMK 10: the numbered file repeats Sea Serpent Grotto interactions instead of demonstrating the Chamber of Oracles battlefield. Legacy battlefield handling remains to be checked.
- AMK 14: the numbered file contains an Upper Jeuno door event rather than the complete final fight. Legacy handling remains to be checked.
- ASA 5: initial Andrause shop event 237 gives `SOULTRAPPER, 12` where the comment says plates. Subsequent event 238 gives the correct blank plates. The guide flags the initial purchase inconsistency without claiming the entire mission cannot work.
- ASA 6–15 framework files are placeholders; legacy and battlefield coverage are unconfirmed.

Route details deliberately preserved because they prevent common wasted trips:

- ACP 4 requires checking the Qufim ??? again after winning. A failed attempt needs the Goblin NM seedspalls again.
- ACP 6 requires choosing **Mark of Seed**, rather than the alternative Azure key.
- ACP 10 includes all twelve tower afterglows and the final Omnis Stone interaction.
- AMK 4's roast is a harvesting **key item**, not purchased food.
- AMK 8 requires the Sahagin Key and **Waterfall Basin**, not the nearby ???.
- AMK 9 identifies random marker sites and the separate weight-door travel requirement. Later-retail Loadstone access is conditional, not presumed on Zenith.
- AMK 13 includes all four puzzles, weekday order for the pip digit, and the eight-minute level-1 gauntlet.
- ASA 3 lists component and final synthesis recipes; final kit must be self-crafted.
- ASA 4 requires checking the Protocrystal again after each win.
- ASA 6 requires rechecking the Outcropping after the battle.
- ASA 8 lists all six damage-type NMs and the nighttime Zi'Tah window.
- ASA 9 includes the eight sap search areas; ASA 12 lists all sixteen tablets by map/grid.

Only AMK 13 exceeds 200 words in combined route/requirements/notes/reward (219), using two wiki pages plus the full native helper/mission implementation. Other records are below 200 combined words. Sources were reviewed through available search retrieval and pinned native files; direct wiki page opens may return 403, so no claim of a successful complete link crawl is made.

Potential renderer detail: `Mog House` is the correct conceptual start for AMK 1–2, but is not a normal overworld zone. Those entries also list the three home-city districts. Do not force a broken overworld map for the Mog House itself.

This is an authored reference collection. It does not claim that every campaign is live-playable or that every route has already received image/map treatment.
