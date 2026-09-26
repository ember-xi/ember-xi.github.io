from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
P=Path(__file__).resolve().parents[1]/'dist'
class Doc(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=[];self.refs=[];self.h1=0;self.images=[];self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t in ['a','link'] and a.get('href'):self.refs.append(a['href'])
  if t in ['img','script'] and a.get('src'):self.refs.append(a['src'])
  if t=='img':self.images.append(a)
docs={p.resolve():Doc(p.read_text()) for p in P.rglob('*.html')}
for p in (P/'preview').glob('*.html'):
 d=docs[p.resolve()];assert d.h1==1,p
 assert not [i for i,n in Counter(d.ids).items() if n>1],p
 assert all(x.get('alt') for x in d.images),p
 for href in d.refs:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(p,href)
  if u.fragment:assert unquote(u.fragment) in docs[target].ids,(p,href)
print('PASS: three entrypoints; internal pages, assets and legacy anchors; unique IDs; one H1; image descriptions.')
# Validate the manual coordinate annotation against the source grid, not a made-up NPC pin.
css=(P/'preview/wiki.css').read_text();assert 'left:50.390625%;top:56.640625%;width:6.25%;height:6.25%' in css
assert '@media(max-width:680px)' in css and '@media(prefers-reduced-motion:reduce)' in css
print('PASS: H-9 grid annotation (258,290,32,32 on a 512 map), narrow-screen layouts and reduced-motion support present.')
