import re, os, time, glob
v = str(int(time.time()))
names = {'rng':'Ranger','sam':'Samurai','nin':'Ninja','drg':'Dragoon','smn':'Summoner','blu':'Blue Mage','cor':'Corsair','pup':'Puppetmaster','dnc':'Dancer','sch':'Scholar'}
jobs = open('jobs.html', encoding='utf-8').read()
for f in glob.glob('img/job-*.png'):
    m = re.search(r'job-([a-z]+)\.png', f)
    if not m: continue
    ab = m.group(1)
    if ab not in names: continue
    n = names[ab]
    ph = f'<a href="job-{ab}.html" class="jobpic"><div class="ph job"></div></a>'
    if ph in jobs:
        jobs = jobs.replace(ph, f'<a href="job-{ab}.html" class="jobpic"><img src="img/job-{ab}.png?v={v}" alt="{n}"></a>')
    p = f'job-{ab}.html'; h = open(p, encoding='utf-8').read()
    if 'class="jobart"' not in h:
        h = h.replace('</table><div><p>', f'</table><div><img class="jobart" src="img/job-{ab}.png?v={v}" alt="{n}"><p>', 1)
        open(p,'w',encoding='utf-8').write(h)
    print('placed', ab)
open('jobs.html','w',encoding='utf-8').write(jobs)
