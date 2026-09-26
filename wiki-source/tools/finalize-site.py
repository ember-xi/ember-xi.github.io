"""Finalize compact static output and enforce the hosting size budget."""
from pathlib import Path
from html import unescape
import json,re,subprocess
R=Path(__file__).resolve().parents[1];D=R/'dist'
# Search keeps every title, URL, category and summary; full article text stays on its page.
index=D/'assets/search-index.js';text=index.read_text();prefix,legacy=text.split(';\nwindow.ZENITH_LEGACY=',1)
entries=json.loads(prefix.split('window.ZENITH_ARTICLES=',1)[1])
for entry in entries:entry['keys']=entry.get('keys','')[:96]
index.write_text('window.ZENITH_ARTICLES='+json.dumps(entries,ensure_ascii=False,separators=(',',':'))+';\nwindow.ZENITH_LEGACY='+legacy)
# Deduplicate identical inline declarations into one stylesheet, preserving precedence.
stylefile=R/'docs/era-import/shared-styles.json';styles=json.loads(stylefile.read_text()) if stylefile.exists() else {}
def shared(match):
 value=unescape(match.group(1))
 if value not in styles:styles[value]=str(len(styles))
 return ' data-ws="'+styles[value]+'"'
for p in D.rglob('*.html'):
 text=p.read_text();updated=re.sub(r' style="([^"]*)"',shared,text)
 if updated!=text and 'assets/shared-styles.css' not in updated:updated=updated.replace('</head>','<link rel="stylesheet" href="assets/shared-styles.css?v=42"></head>')
 if updated!=text:p.write_text(updated)
css='\n'.join('[data-ws="'+i+'"]{'+ ';'.join(d if '!important' in d else d+' !important' for d in s.split(';') if d.strip())+'}' for s,i in styles.items())
(D/'assets/shared-styles.css').write_text(css+'\n');stylefile.write_text(json.dumps(styles,indent=2)+'\n')
# Prune old encodings using actual references in the final HTML, scripts and styles.
used=set()
for ext in ('*.html','*.js','*.css'):
 for p in D.rglob(ext):used.update(re.findall(r'assets/[^"<>\s?#\\]+',p.read_text()))
removed=[]
for p in D.rglob('*'):
 if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif'}:
  rel=p.relative_to(D).as_posix()
  if rel not in used:removed.append((rel,p.stat().st_size));p.unlink()
if removed:
 subprocess.run(['git','rm','--ignore-unmatch','--',*['dist/'+p for p,n in removed]],cwd=R,check=True,stdout=subprocess.DEVNULL)
total=sum(p.stat().st_size for p in D.rglob('*') if p.is_file())
(R/'docs/era-import/final-size.json').write_text(json.dumps({'expanded_file_bytes':total,'removed_unused_images':removed,'indexed_articles':len(entries)},indent=2)+'\n')
print(json.dumps({'expanded_file_bytes':total,'removed_unused_images':len(removed),'indexed_articles':len(entries)}))
assert total<241*1024*1024,'Static output exceeds the safe size budget'
