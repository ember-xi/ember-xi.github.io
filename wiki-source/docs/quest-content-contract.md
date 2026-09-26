# Quest documentation contract

Every new or changed Zenith quest must be added to `content/english/quest_guides.py` in the same update as its website documentation. Match the delivered server code; do not infer rewards from quest titles.

Each quest needs:

- An exact Reward: item name, quantity, gil, augments or permanent unlock. Explicitly identify choice rewards.
- Its starting NPC and zone with the game-map grid, such as Northern San d’Oria (E-8).
- Requirements and numbered acceptance, objective, trade, combat and turn-in steps.
- Named monsters, exact required counts, example roaming map areas or the quest marker’s map square. Identify dungeon sections.
- A named reward NPC and return location. Link the same record from the quest directory, NPC page and related progression pages.

The shared registry produces the quest directory and summaries, so changing a reward cannot silently leave the index showing only a quest name. Native quest rewards remain distinct from custom changes. Do not invent an exact gil amount where server settings control it. Do not publish XYZ coordinates in player instructions.

Quest directory tables must use exactly this column order: **NPC | Quest | Reward**. Put the zone and game-map grid below the linked NPC name, and the required level below the linked quest name. The Reward cell must show the actual reward, never a quest title. Keep walkthrough details on the linked quest page.

Before publishing: build with `python tools/build-wiki.py`, check `python tools/check-wiki.py`, and review the changed quest pages against the actual payloads. The site is documentation; publishing it does not install or verify the running game server.
