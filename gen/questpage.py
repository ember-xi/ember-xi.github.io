import json,sys
def build(d):
    src=open('/home/claude/site/job-smn.html',encoding='utf-8').read()
    head=src[:src.index('<div id="content">')].replace('<title>Summoner — EmberXI Wiki</title>','<title>%s — EmberXI Wiki</title>'%d['name'])
    rows=''.join('<tr><th>%s</th><td>%s</td></tr>'%(k,v) for k,v in d['box'])
    rew=''.join('<li>%s</li>'%r for r in d['rewards'])
    def li(items):
        out=''
        for it in items:
            if isinstance(it,str): out+='<li>%s</li>'%it
            elif len(it)==1:
                out+='<li>%s</li>'%it[0]
            else:
                head_,subs=it[0],it[1]
                out+='<li>%s<ul>%s</ul></li>'%(head_,''.join('<li>%s</li>'%x for x in subs))
        return out
    nav='<table class="wikitable questnav" dir="ltr"><tr><th>&larr; Previous quest</th><th>Next quest &rarr;</th></tr><tr><td>%s</td><td>%s</td></tr></table>'%(d.get('prev','—'), d.get('next','—'))
    body=f"""<div id="content"><h1 class="firstHeading">{d['name']}</h1><div class="article">
<table class="wikitable questbox" dir="ltr"><tr><th colspan="2" class="qb-title">{d['name']}</th></tr>{rows}
<tr><th>Rewards</th><td><ul class="rew">{rew}</ul></td></tr></table>
{nav}
<h2>Walkthrough</h2><ul class="walk">{li(d['steps'])}</ul>
{('<h2>EmberXI changes</h2><ul>'+''.join('<li>%s</li>'%x for x in d['changes'])+'</ul>') if d.get('changes') else ''}
</div><div id="foot">Last edited: 12 September 2026 · EmberXI Wiki</div></div></div></body></html>"""
    open('/home/claude/site/%s.html'%d['slug'],'w',encoding='utf-8').write(head+body)
if __name__=='__main__':
    for f in sys.argv[1:]: build(json.load(open(f)))
