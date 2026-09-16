import re
tpl=open('the-puppet-master.html',encoding='utf-8').read()
HEAD=tpl[:tpl.find('<div id="content">')]; TAIL=tpl[tpl.find('<div id="foot">'):]
def page(fname,title,rows,rewards,prev,nxt,walk,note=None):
    h=HEAD.replace('The Puppet Master — EmberXI Wiki',f'{title} — EmberXI Wiki')
    ib='<table class="wikitable questbox" dir="ltr"><tr><th colspan="2" class="qb-title">%s</th></tr>'%title
    for k,v in rows: ib+=f'<tr><th>{k}</th><td>{v}</td></tr>'
    ib+='<tr><th>Rewards</th><td><ul class="rew">'+''.join(f'<li>{r}</li>' for r in rewards)+'</ul></td></tr></table>'
    nav=f'<table class="wikitable questnav" dir="ltr"><tr><th>&larr; Previous quest</th><th>Next quest &rarr;</th></tr><tr><td>{prev}</td><td>{nxt}</td></tr></table>'
    nb=f'<div class="mech"><b>EmberXI changes</b><ul>{note}</ul></div>' if note else ''
    body=f'<div id="content"><h1 class="firstHeading">{title}</h1><div class="article">\n{ib}\n{nav}\n{nb}<h2>Walkthrough</h2><ul class="walk">{walk}</ul></div>'
    open(fname,'w',encoding='utf-8').write(h+body+TAIL)
def L(t,u): return f'<a href="{u}">{t}</a>'
def unlock(job,html):
    p=open(f'job-{job}.html',encoding='utf-8').read()
    p=re.sub(r'<tr><td class="ib-label">How to Unlock</td><td>.*?</td></tr>','<tr><td class="ib-label">How to Unlock</td><td>'+html+'</td></tr>',p,count=1,flags=re.S)
    open(f'job-{job}.html','w',encoding='utf-8').write(p)
