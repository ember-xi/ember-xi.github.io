const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert');
const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
const source=fs.readFileSync(path.join(dist,'assets/sidebar.js'),'utf8');
for(const key of ['index','jobs','warrior','zone-qufim-island']){
 const nodes={};const document={body:{dataset:{page:key}},getElementById:id=>(nodes[id]??={innerHTML:''})};
 vm.runInNewContext(source,{document});
 assert(nodes['shared-sidebar'].innerHTML.includes('aria-label="Wiki navigation"'));
 assert(nodes['shared-topbar'].innerHTML.includes('id="wiki-search"'));
 assert(nodes['shared-footer'].innerHTML.includes('SQUARE ENIX'));
 if(['index','jobs'].includes(key))assert(nodes['shared-sidebar'].innerHTML.includes(`href="${key}.html" aria-current="page"`));
 for(const node of Object.values(nodes))for(const match of node.innerHTML.matchAll(/href="([^"#?]+)"/g)){
  if(!/^(?:https?:|data:)/.test(match[1]))assert(fs.existsSync(path.join(dist,match[1])),match[1]);
 }
}
const manifest=JSON.parse(fs.readFileSync(path.join(root,'content/page-manifest.json'),'utf8'));
for(const key of Object.keys(manifest)){
 const text=fs.readFileSync(path.join(dist,key+'.html'),'utf8');
 assert(/assets\/sidebar\.js\?v=\d+/.test(text),key);
 assert(text.indexOf('assets/sidebar.js')<text.indexOf('assets/wiki.js'),key);
}
console.log('PASS: shared header, navigation, active links, footer and script order on every article.');
