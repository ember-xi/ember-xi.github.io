import json,sys
def build(d):
    src=open('/home/claude/site/job-smn.html',encoding='utf-8').read()
    head=src[:src.index('<div id="content">')].replace('<title>Summoner — EmberXI Wiki</title>','<title>%s — EmberXI Wiki</title>'%d['name'])
    rows=''.join('<tr><td class="ib-label">%s</td><td>%s</td></tr>'%(k,v) for k,v in d['box'])
    steps=''.join('<li>%s</li>'%x for x in d['steps'])
    fight=''.join('<li>%s</li>'%x for x in d.get('fight',[]))
    ch=''.join('<li>%s</li>'%x for x in d.get('changes',[]))
    body=f"""<div id="content"><h1 class="firstHeading">{d['name']}</h1><div class="article">
<div class="lead"><table class="infobox"><tr><th colspan="2" class="ib-title">{d['name']}</th></tr>{rows}</table><p>{d['intro']}</p></div>
<h2>Walkthrough</h2><ol>{steps}</ol>
{('<h2>The Fight</h2><ul>'+fight+'</ul>') if fight else ''}
{('<h2>EmberXI changes</h2><ul>'+ch+'</ul>') if ch else ''}
<p><a href="job-smn.html#af">&lsaquo; Back to Summoner equipment</a></p>
</div><div id="foot">Last edited: 12 September 2026 · EmberXI Wiki</div></div></div></body></html>"""
    open('/home/claude/site/%s.html'%d['slug'],'w',encoding='utf-8').write(head+body)
if __name__=='__main__':
    for f in sys.argv[1:]: build(json.load(open(f)))
