"""Zenith Eco-Warrior v1.0: prepared package rules, not live-server status."""
def install(ed):
    P,add,section,para,table,steps,link,listing=ed.P,ed.add,ed.section,ed.para,ed.table,ed.steps,ed.link,ed.listing
    add('eco-warrior','Eco-Warrior','Quests',
        'Fight for one nation each Conquest week. Earn gil, Dragon Chronicles and an EXP bonus you can save for later.',
        section('Start with any nation',table(['Nation','Accept and collect rewards','Battle area','Defeat'],[
            ('San d’Oria','Norejaie · Southern San d’Oria (K-6)','Ordelle’s Caves','1 Necroplasm'),
            ('Bastok','Raifa · Port Bastok (D-6)','Gusgen Mines','2 Puddings'),
            ('Windurst','Lumomo · Windurst Waters, north (F-10)','Maze of Shakhrami','3 Wyrmflies')]))+
        section('What to do',steps(
            'Accept Eco-Warrior from one of the three contacts above. Only one nation’s Eco-Warrior can be active at a time.',
            'Enter that nation’s battle area and speak to its helper: Rojaireaut in Ordelle’s Caves, Degga in Gusgen Mines, or Ahko Mhalijikhari in the Maze of Shakhrami. Apply the ointment for Zenith’s level-25 restriction.',
            'Examine the quest’s ??? to start the encounter. Defeat every required monster while under the quest restriction.',
            'Examine the same ??? again for the key item. Returning to the dungeon helper first is optional; the helper can remove the restriction.',
            'Return to the original contact for your reward. Keep inventory space for Dragon Chronicles. If it cannot be delivered, your quest and key item remain ready to turn in.'))+
        section('Rewards each completion',table(['Reward','How it works'],[
            ('10,000 gil','Base quest reward; the server’s existing quest-gil rate still applies.'),
            ('Dragon Chronicles','The original EXP scroll. Use it from your inventory.'),
            ('One saved EXP bonus','Activate at Zenith Armsmith → Eco-Warrior → Activate EXP bonus. Grants +75% EXP, up to 10,000 extra EXP, with a 24-hour effect duration. This is an earning bonus, not an immediate 10,000 EXP award.')]))+
        para('Saved bonuses stay on your character until activated. If Dedication or Commitment is already active, use it first: activation preserves the existing effect and retains the saved Eco bonus. Each successful activation spends one saved bonus.')+
        section('Weekly rotation',listing([
            'Complete one Eco-Warrior per Conquest week across all three nations. The next reward opens at the next server Conquest tally.',
            'Finish all three nations before repeating a nation. Choose their order freely; finishing the third nation opens a fresh circuit for a later week.',
            'Zenith Armsmith → Eco-Warrior shows your active quest, completed circuit nations, weekly lock and saved bonuses.',
            'A quest accepted before this update can still be finished. Older completed quests do not retroactively fill the new circuit or grant bonus credits. An existing weekly lock is retained.']))+
        section('Completion sound',para('The original Eco-Warrior completion scene already invokes the native quest fanfare. This package keeps that scene. A new fanfare for Zenith’s custom quests is not included: playback through this server’s Lua API has not been verified.'))+
        section('Version and references',para('Requires Eco-Warrior v1.0, Cleanup Phase 2 and the current Adventures v1.1 Armsmith menu. Offline quest, reward, menu and reversible-installation checks passed; Windows installation and in-game play have not yet been confirmed.')+
            listing([
                '<a href="https://horizonffxi.wiki/Eco-Warrior_%28San_d%27Oria%29">Horizon Eco-Warrior</a>: inspiration for the weekly three-nation circuit and reward increase.',
                '<a href="https://horizonffxi.wiki/Tale_Of_The_Wandering_Heroes">Horizon’s EXP-bonus reward</a>: reference for the 75%, 24-hour, 10,000-extra-EXP limits. Zenith uses a saved Armsmith activation instead of adding Horizon’s custom item.',
                'Zenith Eco-Warrior v1.0 source and tests; existing level cap 25 and native encounters preserved.'])),
        facts=[('Level cap','25'),('Frequency','Once per Conquest week'),('Rotation','All 3 nations before repeating'),('Reward contact','Original quest giver')],parent='quests',status=ed.READY)
    for k in ('quests','adventurer-log','zenith-armsmith','adventures'):
        P[k]['body']+=section('Eco-Warrior',para(link('eco-warrior','Eco-Warrior')+' adds a weekly three-nation circuit and saved EXP bonuses. The original quest giver handles acceptance and rewards; Armsmith shows progress and activates earned bonuses. Requires Eco-Warrior v1.0.'))
    P['update-log']['body']=section('19 September: Eco-Warrior package ready',para(link('eco-warrior','Eco-Warrior v1.0')+' keeps the level-25 encounters, raises base gil to 10,000, adds an all-three-nations rotation and awards a saved +75% EXP bonus. Offline checks passed. Installation and in-game verification remain unconfirmed. Custom-quest fanfare playback is still pending.'))+P['update-log']['body']
