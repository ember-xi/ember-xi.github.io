# ToAU walkthrough delivery

Files ready for integration:
- `toau-missions.json`: all 48 numbered missions, 147 ordered steps, each with requirements, starting target/location, notes, rewards, next mission/unlocks, zones, reference links, pinned code links and native_status.
- `toau-access.json`: Tenshodo Membership and The Road to Aht Urhgan prerequisites.
- `toau-campaign.json`: campaign introduction, starting requirements and milestone table.

Scope: complete story chain. No whole-mission stubs in this native ToAU chain; mission 48 is intentionally persistent. Static source review is not live installation/clear verification.

Source review:
- Read all 48 mission scripts at LSB f45ab5c0aa3607b4b8fb694da58434e4dd29a2e4 and the full Road/Tenshodo scripts.
- Fetched all 48 Horizon articles via MediaWiki revision API, with per-page oldid links in JSON. The Road page is now Horizon-specific launch access and is deliberately NOT imported as Zenith behavior.
- Read separate native instance/battlefield files for 15/22/29/31/35/42/44, plus relevant final boss and allied-NPC AI; native instance_list confirms 30-minute instances except 44 (45 minutes).
- All prose is independently written. No copied dialogue transcript, modern wardrobe/Atma reward, Rhapsodies shortcut, or Horizon launch-token scheme.

Important corrections from raw wiki references:
- 6 has no midnight wait in pinned code; 8 requires zoning only.
- 11, 18, 24, 25, 33, 38, 40 require next Vana'diel day and zoning, not Japanese real-world midnight.
- Lost Kingdom consumes Spectral Scent at the successful final scene, not at the opening scene; no repeat acid trade after defeat.
- 33 has no title in the native reward table.
- 46 requires approved attire and empty Main/Sub. Nadeey discarded-ring recovery is TODO, so no exchange/recovery promise.
- 48 stays in the log by design.

Native limitations recorded on specific pages:
- 22: Karababa spell-list/setup TODO; native spell/death/warp handlers exist, but do not rely on full retail support behavior.
- 29: missing Lancelord dialogue and possibly additional boss mechanics.
- 35: missing Gessho dialogue and possibly additional mechanics/improper clone spawning.
- 42: Amnaf low-HP Azure Lore/Chain Affinity sequence unfinished.
- 44: Raubahn final immunity approximated by player main-job counts; damage-history logic and Reraise presentation incomplete, Azure Lore fight block commented out. Guide recommends a second damage type and identifies this difference.

Trust scope: Only missions 22, 29, 35 are explicitly labeled native Trust-allowed in guide, because their battlefield files set allowTrusts=true. The instance missions are not advertised as verified solo/Trust clears.

Validation: 48 consecutive numbers/titles; all required fields; all records have nonempty steps, zones, reference and native links. Supplementary quest data contains two entries. Parent should add maps/images and link all native route targets to actual site slugs.
