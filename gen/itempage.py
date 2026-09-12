import json,sys
def build(d):
    src=open('/home/claude/site/job-smn.html',encoding='utf-8').read()
    head=src[:src.index('<div id="content">')].replace('<title>Summoner — EmberXI Wiki</title>','<title>%s — EmberXI Wiki</title>'%d['name'])
    img='<div class="itemshot"><img src="%s" alt="%s"></div>'%(d['img'],d['name']) if d.get('img') else ''
    extra=''.join('<li>%s</li>'%x for x in d.get('effects',[]))
    other=''.join('<tr><th>%s</th><td>%s</td></tr>'%(k,v) for k,v in d.get('other',[]))
    body=f"""<div id="content"><h1 class="firstHeading">{d['name']}</h1><div class="article">
{img}
<h2>Statistics</h2>
<div class="itemstats"><b>{d['name']}</b> <span class="flags">{d.get('flags','')}</span><br>
<b>[{d['slot']}]</b> {d.get('races','All Races')}<br>
{d['stats']}<br>
<b>Lv.</b> {d['level']} <b>{d['jobs']}</b></div>
{('<ul class="itemeff">'+extra+'</ul>') if extra else ''}
{('<p><i>View the entire <a href="%s">%s</a>.</i></p>'%(d['set_href'],d['set'])) if d.get('set') else ''}
<h2>EmberXI changes</h2><p>{d.get('changes','<i>none</i>')}</p>
<h2>Other Uses</h2><table class="wikitable" dir="ltr">{other}</table>
<h2>How to Obtain</h2><p><i>Cannot be auctioned, traded, bazaared, or delivered.</i></p>
<h3>Quest</h3><ul><li><a href="{d['quest_href']}">{d['quest']}</a></li></ul>
</div><div id="foot">Last edited: 12 September 2026 · EmberXI Wiki</div></div></div></body></html>"""
    open('/home/claude/site/%s.html'%d['slug'],'w',encoding='utf-8').write(head+body)
if __name__=='__main__':
    for f in sys.argv[1:]: build(json.load(open(f)))
