# Quest coverage audit — snapshot 25 September 2026

This is a read-only audit of `zenith-site/content/page-manifest.json`, `content/zone-data.json`, current generated article bodies and the quest documentation contract. No Site or server files were changed. Root is handling the missing Pouch of weighted stones article separately; this snapshot precedes that work.

## Finding

The current site is not a complete quest wiki through level 75. The 1,140 quest references already stored in original/Rise of the Zilart/Chains of Promathia/Treasures of Aht Urhgan zone pages represent **544 distinct quest names**:

| Coverage | Unique referenced quest names |
|---|---:|
| Dedicated article with an observed Walkthrough section | 9 |
| Covered under another guide title | 4 |
| Named only in the Limit Break progression summary | 4 |
| No local walkthrough found | 527 |

Thus **531 referenced quests lack a dedicated or alias walkthrough**, including the four Limit Break summaries. The four alias-covered names are In Defiant Challenge (First Limit Break) and the three nation-specific Eco-Warrior quests (one combined Eco-Warrior guide). Alias coverage is not a validation of every rule or step.

The exact-title walkthroughs are Brygid the Stylist; Brygid the Stylist Returns; The Doorman; Fear of the Dark; Mysteries of Beadeaux I; Mysteries of Beadeaux II; Tenshodo Membership; Chocobo's Wounds; and Crest of Davoi. Crest also has a key-item page; that duplicate is not a second quest.

The manifest contains 1,789 articles, but 1,216 are Items and only 30 have category Quests, including directory pages and custom quests. Article count is not evidence of comprehensive quest coverage.

## Inventory limitations

| Zone expansion grouping | Zones | Quest references | Unique names within grouping |
|---|---:|---:|---:|
| Original | 83 | 736 | 388 |
| Rise of the Zilart | 46 | 180 | 108 |
| Chains of Promathia | 43 | 91 | 50 |
| Treasures of Aht Urhgan | 33 | 133 | 72 |
| Wings of the Goddess | 31 | 0 | 0 |

Counts overlap between groupings. Location expansion does not prove that each referenced quest belongs to the level-75 era. **WotG has no extracted quest inventory at all**, so the 544-name list is a lower bound, not a complete scope. Unlisted mini-quests and key-item access actions can be absent even from zone quest tables. The Pouch example exposes precisely this gap.

The current 64 Mission-category records are the three nations' mission pages and mission directories; expansion-story coverage must be inventoried separately. Do not describe the site as complete through RoZ/CoP/ToAU/WotG based on the existing national mission pages.

## Priority access gaps

| Access feature | Current local coverage | Primary community reference | Practical coverage needed |
|---|---|---|---|
| Pouch of weighted stones / Banishing Gates | No article in this snapshot; root implementing | https://horizonffxi.wiki/Banishing_Gate | Acquisition location, all three gates, prerequisites, permanent KI behavior and related Garlaige routes. |
| Magicked Astrolabe / Eldieme gates | Existing detailed `the-eldieme-necropolis-door-quest` article | Existing article links reviewed NPC/gate implementation and community references | Retain this as an example of an unlisted mini-quest with a real walkthrough. |
| Portal Charm / Three Mage Gate | No dedicated article; acquisition is one note in `mission-windurst-3-2` | https://horizonffxi.wiki/Portal_Charm and https://horizonffxi.wiki/Three_Mage_Gate | Kupipi acquisition, mission dependency, required item, permanent access and alternate gate methods. |
| Paintbrush of Souls | No local article | https://horizonffxi.wiki/Paintbrush_of_Souls | Key acquisition, library/books/casket sequence, correct map floors, using the blank frame and waiting before advancing its dialogue. |
| Moongate Pass | No local article | https://horizonffxi.wiki/Moongate_Pass_Quest | Unlisted quest; moon/time/weather or helper access, searching behind gates, obtaining permanent pass. |
| Rhinostery Certificate / Toraimarai Turmoil | No local article | https://horizonffxi.wiki/Toraimarai_Turmoil and https://horizonffxi.wiki/Rhinostery | Full prerequisite chain, Windurst fame, certificate granted on acceptance, Priming Gate access, optional shell turn-in completion. |
| Crimson Orb / Wall of Banishing | No local article; `limit-break` only summarizes crest collection | https://horizonffxi.wiki/Obtaining_a_Crimson_Orb | Unlisted access sequence, Sedal-Godjal, four ponds, curse and return; link from Whence Blows the Wind. Source pages disagree on some pond grid labels, so verify map/script before publishing coordinates. |
| Tonberry Key / Everyone's Grudge | No local article | https://horizonffxi.wiki/Everyone%27s_Grudge_%28Quest%29 and https://horizonffxi.wiki/Tonberry_Key | Unlocking the priest's room, prerequisite/turn-in, permanent key and repeatable hate reset. Source fee descriptions differ; verify script instead of copying a price range. |
| Loadstone / Open Sesame | No local article | https://ffxiclopedia.fandom.com/wiki/Open_Sesame and https://www.bg-wiki.com/ffxi/Loadstone | Solo weighted-door access in Quicksand Caves. Verify Zenith inclusion: this is later retail convenience content, so level-75 usefulness alone does not establish era eligibility. |
| Altepa Gate | No local guide | https://www.bg-wiki.com/ffxi/Altepa_Gate | Separate four-column gate puzzle; Loadstone helps with weighted doors but does not replace the Altepa Gate sequence. |
| Boarding Permit / The Road to Aht Urhgan | No local article | https://horizonffxi.wiki/The_Road_to_Aht_Urhgan | Mandatory ToAU travel access. Current Horizon page has its own 2026 launch-event requirements; those are not Zenith rules. Match the reviewed native quest/source before writing this guide. |

The Rhinostery prerequisite chain listed by Horizon is Food for Thought → Overnight Delivery → Water Way to Go → Blue Ribbon Blues → Toraimarai Turmoil. Those prerequisite walkthroughs are also missing locally; documenting only the final certificate would leave another route incomplete.

## Other concrete gaps already referenced locally

- An Explorer's Footsteps appears in 18 zone quest tables without a walkthrough.
- Strange Apparatus appears in eight zone tables without a guide.
- The Holy Crest and other job unlocks, numerous Borghertz artifact hand quests, map quests, weapon-skill quests and summon trials are in the existing reference inventory without local guides.
- Atop the Highest Mountains, Whence Blows the Wind, Riding on the Clouds and Shattering Stars have one-row progression summaries, not full walkthroughs. In Defiant Challenge has the separate First Limit Break guide and was counted accordingly.

## Files and method

- `coverage.json`: all 544 normalized names, observed coverage status, local article/alias matches and original zone-row provenance, including source revision where stored.
- `coverage.csv`: compact reviewable backlog with local matches and source URLs.
- `summary.json`: counts, scope, snapshot manifest hash and limitations.

Normalization ignores punctuation/case and normalizes Unicode. Exact local titles were checked against generated article headings. Known alternative titles were inspected manually. Body-name mentions were not counted as walkthroughs; misleading text collisions such as The Rescue, The Three Magi and The Usual were rejected.

Completion should be measured against a canonical era/level-scoped quest and unlisted-access inventory, then checked for prerequisites, rewards, complete numbered steps, exact NPC/map locations, and links from quest/NPC/zone/item pages. Merely generating pages or importing zone-table names will not close these gaps.
