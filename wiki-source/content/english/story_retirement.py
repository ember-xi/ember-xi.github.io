"""Retire the three custom story chains; preserve original quests and rewards."""
from lxml import html
RETIRED=('coastal-dispatch','sandbound-repairs','the-broken-watch','adventures')
TITLES=('Coastal Dispatch','Sandbound Repairs','The Broken Watch')
def install(ed):
 P=ed.P;section,para,table,link,add=ed.section,ed.para,ed.table,ed.link,ed.add
 for key,p in P.items():
  if key in RETIRED or key=='update-log':continue
  root=html.fragment_fromstring(p['body'],create_parent='div')
  for a in list(root.xpath('.//a')):
   if a.get('href','').split('.')[0] in RETIRED:
    row=next((r for r in a.iterancestors() if r.tag in ('tr','li')),None)
    if row is not None and row.getparent() is not None:row.getparent().remove(row)
    else:a.set('href','equipment-quests.html');a.text='Original equipment quests'
  for e in list(root.xpath('.//tr|.//li|.//p')):
   if any(t in e.text_content() for t in TITLES) and e.getparent() is not None:e.getparent().remove(e)
  p['body']=''.join(html.tostring(c,encoding='unicode') for c in root)
  for f in ('intro','body'):
   p[f]=p[f].replace('Accepted equipment, ring, Trust, side-quest and Limit Break records keep their counters. The responsible NPC now handles the next step and reward.','Ring, Trust and Limit Break progression continues at its NPC. Custom equipment and story quests are retired; their saved records and earned rewards remain.')
 for key in RETIRED:P.pop(key,None)
 for key,title,place in [('medicine-axe','Medicine Axe','Valkurm Dunes (H-7)'),('lucretia','Lucretia','Northern San d’Oria (E-6)'),('jiwon','Jiwon','Qufim Island (F-6)')]:
  add(key,title,'NPCs','Original NPC interactions remain available.',section('Location',para(place))+section('Current role',para('The added Zenith story quest is retired. This NPC uses its original dialogue and trade handling. No story materials or report are required.')),parent='npcs')
 body=section('Quest fights',table(['Quest','Opponent','Game-map location'],[(link('a-rhythm-worth-following','A Rhythm Worth Following'),'Wayward Weapon','Qufim Island (F-6)'),(link('a-doctors-promise','A Doctor’s Promise'),'Cratebreaker','Batallia Downs (H-6)')]))+section('Starting a fight',para('Accept the Trust quest from its NPC first. Prepare your Trusts and examine its ???. Return to the quest giver after winning.'))+section('Original NM hunts',para('Valkurm Emperor, Dune Widow and Aquarius now use their original spawn rules and drops. Their custom story pop markers are removed. First Limit Break still uses its regular monster item hunts.'))
 add('quest-encounters','Quest Encounters','Guides','Accepted Trust quests retain their required fights.',body,parent='quests')
 add('nm-challenges','Retired NM Challenges','Reference','The standalone challenge menu remains retired.',section('Current status',para('No standalone challenge acceptance or custom story pop markers. Original NMs use their native spawn rules and drops. '+link('quest-encounters','Trust quest encounters')+' remain available. Previously earned legacy challenge gifts may still be collected at Zenith Armsmith.')),parent='retired-activities')
 P['roadmap']['intro']='World Quests v3.5.0 removes the three custom story quests.'
 P['roadmap']['body']=P['roadmap']['body'].replace('Original spawn rules restored for 21 former challenge NMs.','Original spawn rules restored for all former challenge NMs, including the three former story opponents.')
 P['update-log']['body']=section('Custom story quests retired — v3.5.0',para('Coastal Dispatch, Sandbound Repairs and The Broken Watch are retired. Their NPCs resume original interactions, with no story-material trades or new story rewards. Earned items and gil are kept. Valkurm Emperor, Dune Widow and Aquarius resume native spawning and drops. Trust, city-ring and Limit Break quests are unchanged.'))+P['update-log']['body']
