# Mission and Scout documentation review — 19 September 2026

This release adds three national hubs and 60 original, concise mission guides.
San d’Oria 1-1 retains its existing `smash-the-orcish-scouts.html` route.
Individual pages cite HorizonXI walkthroughs and the LandSandBoat definition at
revision `f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4`. Those sources do not establish
Zenith battlefield settings or live completion. Alternate nation-visit orders in
2-3 are explicitly distinguished from each guide’s selected route.

Nation photography is official PlayOnline imagery. Thirty selected mission maps
and the two Scout maps retain source-image credits. Source URLs and provenance
are recorded in `nation-images.json`, `mission-maps.json`, and `scout-maps.json`.

The Scout review read the delivered Qufim Wall, NPC Roles, and Travel and Quest
Clarity archives without executing any installer or changing server files.
Qufim Wall preserves three different Valkurm positions across supported source
variants. The outpost and older entrance layouts must not be conflated.
Clarity does not edit `job_journey_data.lua`. World positions are source-confirmed;
map overlays identify corroborated landmarks, not pixel-exact NPC tracking.
The older entrance area is approximate. Live NPC visibility remains unverified.

Validation:

- `python3 tools/build-wiki.py`
- `python3 tools/check-wiki.py`
- `python3 tools/check-missions-scouts.py`
- `node --check dist/assets/wiki.js`
- `node --check dist/assets/search-index.js`
- `git diff --check`

The static Site has no compatible managed preview server. No browser-render or
live game test is claimed. HTML routes, anchors, image decoding, map geometry,
mission navigation, English text, and preserved market/camp data are checked.

## Follow-up: exact uploaded audit match

The user reported that the Scout still could not be found and requested an exact
file check. The uploaded audit collected 2026-09-19T04:16:43Z identifies
job_journey_data.lua with SHA-256
`2cdcc8b2e1164a7ed95094c256d830705ccecc2a4687a568a951f062c3275e75`.
Its bytes match the Qufim Wall outpost variant. The audited job_journeys.lua
matches NPC Roles payload
`2dbc9de5f126c40b4bd27deb4b67c3e8ed976e2a6b2b703e621ea9dc43c1a070`.
The previous audit omitted both Valkurm and Qufim Zone.lua files. The cause of
absence is not established. Current source collection is required to inspect
the actual initialization chain. The old entrance suggestion is withdrawn for
this audited installation; the blue legacy-area overlay was removed.

## Follow-up: six source files collected at 13:13:43 UTC

The uploaded Scout Check 1.0.1 ZIP contains report.json and exactly six allowed
Lua files. Their byte sizes and SHA-256 hashes were independently verified.
Both zone files contain the Atlas wrapper followed by the Job Journeys wrapper.
Valkurm's zone source hash is
`6bccf5110454dcfab8260e4549074cc8e06b20c463236fdd06ce813f0f2a5351`;
Qufim's is `fa4b93ae8951fe8e7d61c9b73793de8c0432a4ed4af955bd0c4acbfb21ddef54`.
The Scout data hash remains the outpost variant above. The current quest module
hash is `2a45b10c8bb5bc2063f07587dccf2c88cadcfa1487050ffdcf0940dbc9a4aaea`.
Atlas and catalog hashes are respectively
`002a2bcc8fe182e2adb6f3b47cfd25d0ccfa058c86e360d130cdefe43bdd93ac` and
`575331ac6ef810733e674de8d966f7817888ee855d167474580d59e8ead09aba`.

An isolated LuaJIT 2.1 execution of those exact zone and supporting modules,
with native engine APIs and uncollected dependencies mocked, requests Atlas
followed by Scout in each zone, at the recorded coordinates. Repeated calls
honor the local-variable duplicate guard. Injected errors at Mog Tablet or
Atlas stop Valkurm initialization before Scout creation. Those injected
failures demonstrate control flow, not the actual live cause.

The previously reviewed Valkurm navmesh (SHA-256
`4803d9fccaf97291b9079cd70a9bd62b0e8d48fd8214e16d250f21c65fd04256`)
has a walkable detail surface at the Scout X/Z with Y -8.0271. This does not
establish client visibility or justify an arbitrary relocation. No server
patch was made. Runtime startup output and the live NPC state remain needed.
The Site now reflects the received source evidence instead of requesting the
same six files again.

## Runtime confirmation and requested replacement

The user's automatic report at 13:57:57 UTC confirms successful initialization
and one normal Scout per zone. Valkurm remains present after player entry at
13:58:35, ID 17201153, position 135,-7.827,109. The user explicitly requested
replacing that Scout with one next to the outpost books.

Scout By Books v1.0 changes only the zone-103 position data to 135,-7.793,93,
rotation 64. Native Field Manual and Survival Guide are 4.036 and 5.385 yalms
away. The pinned terrain surface supports the new point and 72 surrounding
samples. The NPC height uses the neighboring native book's mesh offset.
Fresh-start Lua tests create exactly one Scout at the new point, keep the
original quest callback and duplicate guard, and leave Qufim unchanged.
Full server restart discards the old dynamic instance and creates one from
the updated point. No database or quest-progress reset is involved.

The website distinguishes the delivered replacement from the old runtime
baseline. New-point installation and client visibility are not claimed as
already verified. The H-7 landmark overlay remains geographically applicable.
