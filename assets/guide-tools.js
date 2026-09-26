/* Shared quest/mission navigation. Relationships come from each article's
   existing metadata, never alphabetical order. AF order: local AF index. */
(() => {
  'use strict';
  const article = document.querySelector('article.article');
  if (!article || document.getElementById('zenith-guide-style')) return;
  const style = document.createElement('style');
  style.id = 'zenith-guide-style';
  style.textContent = `
.guide-sequence-nav{clear:both;margin:18px 0;padding:12px;border:1px solid #bac8d8;background:#f8fafc;font-size:14px;line-height:1.5}
.guide-sequence-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(150px,.8fr) minmax(0,1fr);gap:12px;align-items:start}
.guide-sequence-side{min-width:0;display:grid;gap:6px}.guide-sequence-side>a,.guide-series>a{display:block;padding:9px 11px;border:1px solid #c6d3e1;background:#fff;min-height:44px;overflow-wrap:anywhere}
.guide-sequence-side>a:hover,.guide-series>a:hover{background:#edf3fb}.guide-next{text-align:right}.guide-sequence-label{font-weight:700;color:#394f68}.guide-sequence-empty{color:#616c77;padding:9px 0;font-size:13px}.guide-series{text-align:center;min-width:0}.guide-series small{display:block;color:#54595d;margin:5px 0}.guide-af-steps{display:flex;justify-content:center;flex-wrap:wrap;gap:5px;list-style:none;padding:0;margin:7px 0 0}.guide-af-steps li{margin:0}.guide-af-steps a,.guide-af-steps span{display:block;padding:4px 8px;border:1px solid #c6d3e1;background:#fff}.guide-af-steps [aria-current]{background:#e0ebf8;border-color:#4772a0;font-weight:700}
.quest-map-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;clear:both;margin:22px 0}.era-reference .quest-map,.quest-map{float:none!important;max-width:530px!important;min-width:0;margin:0!important;padding:12px;border:1px solid #bac8d8;background:#f8fafc}.quest-map .map-marked{max-width:512px}.quest-map-preview{display:block;line-height:0;cursor:zoom-in}.quest-map img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:contain}.quest-map figcaption{margin:10px 0;font-size:14px;line-height:1.5}.quest-map figcaption strong,.quest-map figcaption span{display:block}.quest-map figcaption small{display:block;font-size:12px;margin-top:7px}.quest-map button{min-height:40px}.scout-map-dialog .quest-map-preview{cursor:default}.scout-map-dialog .map-marked img{max-width:100%;height:auto}
@media(max-width:760px){.guide-sequence-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.guide-series{grid-column:1/-1;grid-row:1}.guide-sequence-nav{padding:10px}.quest-map-grid{grid-template-columns:minmax(0,1fr)}.quest-map{justify-self:center;width:100%}}
@media print{.guide-sequence-nav,.quest-map button{display:none!important}.quest-map-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.quest-map{break-inside:avoid}}
`;
  document.head.append(style);

  // The original image remains a working link when JavaScript is unavailable.
  document.addEventListener('click', event => {
    const preview = event.target.closest?.('.quest-map-preview');
    if (!preview || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const button = preview.closest('figure')?.querySelector('[data-enlarge-map]');
    if (button) { event.preventDefault(); button.click(); }
  });

  const page = (document.body.dataset.page || '') + '.html';
  const base = new URL('.', document.baseURI);
  const entries = window.ZENITH_ARTICLES || [];
  const known = new Map(entries.map(item => [item.url.split('#')[0], item]));
  const norm = text => text.normalize('NFKC').toLowerCase().replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
  const byName = new Map();
  for (const item of entries) {
    const key = norm(item.name);
    if (!byName.has(key)) byName.set(key, []);
    byName.get(key).push(item);
  }
  const afGroups = [{"label":"Bard AF","index":"category-artifact-armor.html#era-Bard","quests":["painful-memory.html","the-requiem.html","the-circle-of-time.html"]},{"label":"Beastmaster AF","index":"category-artifact-armor.html#era-Beastmaster","quests":["wings-of-gold.html","scattered-into-shadow.html","a-new-dawn.html"]},{"label":"Black Mage AF","index":"category-artifact-armor.html#era-Black_Mage","quests":["the-three-magi.html","recollections.html","the-root-of-the-problem.html"]},{"label":"Blue Mage AF","index":"category-artifact-armor.html#era-Blue_Mage","quests":["beginnings.html","omens.html","transformations.html"]},{"label":"Corsair AF","index":"category-artifact-armor.html#era-Corsair","quests":["equipped-for-all-occasions.html","navigating-the-unfriendly-seas.html","against-all-odds.html"]},{"label":"Dark Knight AF","index":"category-artifact-armor.html#era-Dark_Knight","quests":["dark-legacy.html","dark-puppet.html","blade-of-evil.html"]},{"label":"Dragoon AF","index":"category-artifact-armor.html#era-Dragoon","quests":["a-craftsman-s-work.html","chasing-quotas.html","knight-stalker.html"]},{"label":"Monk AF","index":"category-artifact-armor.html#era-Monk","quests":["quest-ghosts-of-the-past.html","the-first-meeting.html","true-strength.html"]},{"label":"Ninja AF","index":"category-artifact-armor.html#era-Ninja","quests":["20-in-pirate-years.html","i-ll-take-the-big-box.html","true-will.html"]},{"label":"Paladin AF","index":"category-artifact-armor.html#era-Paladin","quests":["sharpening-the-sword.html","a-boy-s-dream.html","under-oath.html"]},{"label":"Puppetmaster AF","index":"category-artifact-armor.html#era-Puppetmaster","quests":["the-wayward-automaton.html","operation-teatime.html","puppetmaster-blues.html"]},{"label":"Ranger AF","index":"category-artifact-armor.html#era-Ranger","quests":["sin-hunting.html","fire-and-brimstone.html","unbridled-passion.html"]},{"label":"Red Mage AF","index":"category-artifact-armor.html#era-Red_Mage","quests":["the-crimson-trial.html","enveloped-in-darkness.html","peace-for-the-spirit.html"]},{"label":"Samurai AF","index":"category-artifact-armor.html#era-Samurai","quests":["the-sacred-katana.html","yomi-okuri.html","a-thief-in-norg.html"]},{"label":"Summoner AF","index":"category-artifact-armor.html#era-Summoner","quests":["the-puppet-master.html","class-reunion.html","carbuncle-debacle.html"]},{"label":"Thief AF","index":"category-artifact-armor.html#era-Thief","quests":["the-tenshodo-showdown.html","as-thick-as-thieves.html","hitting-the-marquisate.html"]},{"label":"Warrior AF","index":"category-artifact-armor.html#era-Warrior","quests":["the-doorman.html","the-talekeeper-s-truth.html","the-talekeeper-s-gift.html"]},{"label":"White Mage AF","index":"category-artifact-armor.html#era-White_Mage","quests":["messenger-from-beyond.html","prelude-of-black-and-white.html","pieuje-s-decision.html"]}];
  const af = afGroups.find(group => group.quests.includes(page));
  const tab = document.querySelector('.page-tabs .selected')?.textContent.trim();
  if (tab !== 'Quests' && tab !== 'Missions' && !af) return;
  const kind = tab === 'Missions' ? 'mission' : 'quest';
  const rows = [...article.querySelectorAll('tr')];

  function localLink(anchor) {
    const raw = anchor.getAttribute('href');
    if (!raw) return null;
    try {
      const url = new URL(raw, document.baseURI);
      if (url.origin === base.origin && url.pathname.startsWith(base.pathname)) {
        const path = decodeURIComponent(url.pathname.slice(base.pathname.length));
        if (path !== page && known.has(path)) return {url:path + url.hash, name:known.get(path).name};
      }
    } catch { return null; }
    // Resolve an external wiki reference only when it names one unambiguous local article.
    for (const name of [anchor.textContent, anchor.getAttribute('title') || '']) {
      const matches = byName.get(norm(name)) || [];
      const distinct = [...new Map(matches.map(item => [item.url,item])).values()];
      if (distinct.length === 1 && distinct[0].url !== page) return {url:distinct[0].url,name:distinct[0].name};
    }
    return null;
  }
  function readDirection(direction) {
    const expression = new RegExp('^' + direction + '\\s+(?:quest|mission)s?\\s*:?$', 'i');
    for (const row of rows) {
      const cells = [...row.children].filter(cell => /^(TD|TH)$/.test(cell.tagName));
      if (cells.length < 2 || !expression.test(cells[0].textContent.trim())) continue;
      const anchors = [...cells.slice(1).flatMap(cell => [...cell.querySelectorAll('a[href]')])];
      const links = anchors.map(localLink).filter(Boolean);
      return {found:true, links:[...new Map(links.map(link => [link.url,link])).values()], unresolved:anchors.length > links.length};
    }
    return {found:false,links:[],unresolved:false};
  }
  const previous = readDirection('previous');
  const next = readDirection('next');
  const oldNavs = [...article.querySelectorAll('nav.mission-nav')];
  const oldNav = oldNavs[0];
  if (oldNav) {
    for (const [direction,state] of [['previous',previous],['next',next]]) {
      if (state.found) continue;
      const anchor = [...oldNav.querySelectorAll('a')].find(a => a.textContent.trim().toLowerCase().startsWith(direction));
      const link = anchor && localLink(anchor);
      if (link) { state.found = true; state.links = [link]; }
    }
  }
  // Explicit, locally documented AF order is the fallback for missing metadata.
  if (af) {
    const step = af.quests.indexOf(page);
    for (const [offset,state] of [[-1,previous],[1,next]]) {
      if (state.found) continue;
      const path = af.quests[step+offset];
      state.found = true;
      if (path && known.has(path)) state.links = [{url:path,name:known.get(path).name}];
    }
  }
  if (!previous.found && !next.found && !oldNav) return;
  let series = {url:kind === 'mission' ? 'missions.html' : 'quests.html',name:kind === 'mission' ? 'All missions' : 'All quests'};
  if (af) series = {url:af.index,name:af.label};
  else {
    const candidates = [...(oldNav?.querySelectorAll('a') || []), ...article.querySelectorAll('.breadcrumb a')];
    const link = candidates.find(a => /(?:^|\/)missions-[^/]+\.html(?:#.*)?$/.test(a.getAttribute('href') || ''));
    const local = link && localLink(link);
    if (local) series = local;
    else if (page.startsWith('borghertz-s-')) series = {url:'category-artifact-armor.html',name:'Artifact quests'};
  }
  function makeLink(link, rel) {
    const anchor = document.createElement('a'); anchor.href = link.url; anchor.textContent = link.name;
    if (rel) anchor.rel = rel;
    return anchor;
  }
  function makeNav(position) {
    const nav = document.createElement('nav');
    nav.className = 'guide-sequence-nav'; nav.dataset.guidePosition = position;
    nav.setAttribute('aria-label', `${kind === 'mission' ? 'Mission' : 'Quest'} sequence — ${position}`);
    const grid = document.createElement('div'); grid.className = 'guide-sequence-grid';
    for (const [direction,state] of [['previous',previous],['next',next]]) {
      const side = document.createElement('div'); side.className = 'guide-sequence-side guide-' + direction;
      const label = document.createElement('span'); label.className = 'guide-sequence-label';
      label.textContent = (direction === 'previous' ? '← Previous ' : 'Next ') + kind + (state.links.length > 1 ? 's' : '') + (direction === 'next' ? ' →' : '');
      side.append(label);
      for (const link of state.links) side.append(makeLink(link,state.links.length === 1 ? (direction === 'previous' ? 'prev' : 'next') : null));
      if (state.unresolved) {
        const note = document.createElement('small'); note.textContent = 'Some linked articles are not available locally.'; side.append(note);
      }
      if (!state.links.length && !state.unresolved) {
        const empty = document.createElement('span'); empty.className = 'guide-sequence-empty'; empty.textContent = `No ${direction} ${kind} listed`; side.append(empty);
      }
      if (direction === 'next') {
        const center = document.createElement('div'); center.className = 'guide-series';
        center.append(makeLink(series));
        if (af) {
          const steps = document.createElement('ol'); steps.className = 'guide-af-steps'; steps.setAttribute('aria-label',af.label + ' quests');
          af.quests.forEach((url,i) => {
            const li = document.createElement('li');
            const node = url === page ? document.createElement('span') : document.createElement('a');
            node.textContent = 'AF ' + (i+1);
            if (url === page) node.setAttribute('aria-current','step');
            else { node.href = url; node.title = known.get(url)?.name || 'AF ' + (i+1); }
            li.append(node); steps.append(li);
          });
          center.append(steps);
        }
        grid.append(center);
      }
      grid.append(side);
    }
    nav.append(grid); return nav;
  }
  for (const old of oldNavs) old.remove();
  const beginning = article.querySelector('.article-overview, .article-body');
  beginning?.before(makeNav('top'));
  const bottom = makeNav('bottom');
  const footer = article.querySelector('.category-footer');
  if (footer) footer.before(bottom); else article.append(bottom);
})();
