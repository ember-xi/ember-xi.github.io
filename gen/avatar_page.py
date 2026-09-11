# Builds an avatar page from a data dict using avatars.html as the shell.
import sys, json
def build(d):
    src=open('/home/claude/site/avatars.html',encoding='utf-8').read()
    head=src[:src.index('<div id="content">')].replace('<title>Avatars — EmberXI Wiki</title>','<title>%s — EmberXI Wiki</title>'%d['name'])
    rows=''.join('<tr><td class="ib-label">%s</td><td>%s</td></tr>'%(k,v) for k,v in d['infobox'])
    walk=''.join('<li>%s</li>'%x for x in d['walk'])
    route=''.join('<li>%s</li>'%x for x in d['route'])
    fight=''.join('<li>%s</li>'%x for x in d['fight'])
    rewards=''.join('<tr><td>%s</td><td>%s</td></tr>'%(a,b) for a,b in d['rewards'])
    changes=''.join('<li>%s</li>'%x for x in d['changes'])
    mini=''.join('<li>%s</li>'%x for x in d['mini'])
    body=f"""<div id="content"><h1 class="firstHeading">{d['name']}</h1><div class="article">
<div class="lead"><table class="infobox"><tr><th colspan="2" class="ib-title">{d['name']} — {d['quest']}</th></tr>{rows}</table><p>{d['intro']}</p></div>
<h2>Under 65: Trial-Size {d['quest']}</h2><ol>{mini}</ol>
<div class="mech"><b>Trial-Size rules:</b> solo, level 20 cap, Carbuncle only, 15 minutes. Buffs cast outside are kept. Best day: {d['bestday']}. Never on {d['badday']}.</div>
<h2>65 and up: {d['quest']} (Prime)</h2><ol>{walk}</ol>
<h2>Walking to the {d['cloister']}</h2><ul>{route}</ul>
<h2>The Fight</h2><ul>{fight}</ul>
<div class="mech"><b>EmberXI solo tips:</b> {d['tips']}</div>
<h2>Rewards</h2><p>One per win. The Whisper is used up when you take a reward; win again (once a day) for the next.</p><table class="wikitable"><tr><th>Reward</th><th>Notes</th></tr>{rewards}</table>
<h2>Prime Pact (level 75)</h2><p>Win this Prime fight as SMN 75 with {d['name']} already learned and the message === The Prime Pact === appears: you learn {d['pact']}.</p>
<h2>EmberXI changes</h2><ul>{changes}</ul>
</div><div id="foot">Last edited: 12 September 2026 · EmberXI Wiki</div></div></div></body></html>"""
    open('/home/claude/site/%s.html'%d['slug'],'w',encoding='utf-8').write(head+body)
if __name__=='__main__':
    build(json.load(open(sys.argv[1])))
