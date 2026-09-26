"""Document the delivered job patch without claiming installation."""


def install(ed):
    P, section, para, table = ed.P, ed.section, ed.para, ed.table
    status = 'Job Balance v1.0.1 is prepared and tested offline. Installation and in-game behavior are not yet confirmed.'
    P['thief']['body'] = P['thief']['body'].replace('Higher Dual Wield tiers are unchanged.', 'Job Balance v1.0.1 adds Dual Wield II at level 40; it requires the new package.')
    P['thief']['body'] = P['thief']['body'].replace('No custom Treasure Hunter, Thief ability or weapon-skill changes are included in the documented packages.', 'Treasure Hunter remains unchanged. The new Ambush recast benefit is described below.')
    P['thief']['body'] += section('Job Balance v1.0.1', para(status)+table(['Feature', 'Behavior'], [
        ('Dual Wield II', 'THF40, 15% delay reduction. It replaces the first tier; the two values do not add together.'),
        ('Ambush merits', 'At main THF75, each purchased rank removes one second from Sneak Attack and Trick Attack recasts, up to five seconds. Native accuracy and Group 1 recast merits remain. This timing is a Zenith choice.'),
        ('Support jobs / level sync', 'Normal native trait rules apply. The Ambush addition is disabled below effective main level 75 and for THF support jobs.'),
    ]))
    P['warrior']['body'] += section('Job Balance v1.0.1', para(status)+para('Raging Rush and Steel Cyclone use the improved formulas already included in the native base. The default setting already enables them, so the package normally adds no further damage increase. If that global setting is disabled, these two formulas apply to main-job WAR only. Skill and quest unlocks remain required.'))
    jobs = [
        ('summoner', 'Summoner', 'SMN', [
            ('Whispering Wind', 'Keeps native healing and removes Blindness, Poison, Paralysis, Disease/Virus, Petrification, Sleep, Silence and Slow. Works on eligible full-HP targets. Does not remove Plague, Doom or Curse.'),
            ('Crimson Howl', 'Three-minute duration, retaining the native 9% attack potency.'),
            ('Magical Blood Pacts', '+15 magic accuracy for player main-SMN avatar damage and magical ailment resist rolls. Native wards without an accuracy roll remain unchanged. No damage multiplier is added.'),
        ]),
        ('dragoon', 'Dragoon', 'DRG', [('Steady Wing', 'Available at DRG30. Requires a wyvern; native shield behavior, three-minute duration and five-minute recast remain.')]),
        ('paladin', 'Paladin', 'PLD', [
            ('Auto Refresh', 'Available at PLD25, retaining 1 MP per tick and normal native support-job rules.'),
            ('Enlight', 'Learn and cast from PLD40. Mamaroon in Nashmau sells Scroll of Enlight for 100,800 gil. The client tooltip can still show retail level 85.'),
            ('Chivalry', 'Available at PLD45 without a merit unlock. Converts TP to MP and consumes the TP. Native ten-minute recast and earned merit potency remain.'),
        ]),
    ]
    for key, name, short, rows in jobs:
        ed.add(key, name, 'Jobs', 'Documented Zenith adjustments for '+name+'.', section('Job Balance v1.0.1', table(['Ability / feature', 'Zenith behavior'], rows))+section('Progression', para('Normal job unlocks, learned-spell ownership and effective-level requirements remain. This package does not grant free levels, spells, items or merit points.')), facts=[('Job', short), ('Package', 'Job Balance v1.0.1')], parent='jobs', status=status)
    P['jobs']['body'] = P['jobs']['body'].replace('Further job adjustments will be documented after review; no additional custom ability values are currently confirmed.', 'Job Balance v1.0.1 is documented on the Warrior, Thief, Summoner, Dragoon and Paladin pages; installation is not yet confirmed.')
    P['jobs']['body'] += section('Job Balance v1.0.1', para(status)+ed.listing([ed.link(k) for k in ('warrior', 'thief', 'summoner', 'dragoon', 'paladin')]))
