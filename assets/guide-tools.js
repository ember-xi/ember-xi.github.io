/* v45: progress through documented quest/mission chains, never alphabetical order. */
(() => {
  'use strict';
  if (window.ZenithGuideTools) return;
  window.ZenithGuideTools = {version: 45};
  const article = document.querySelector('article.article');
  if (!article) return;
  const source = document.currentScript?.src || new URL('assets/guide-tools.js', document.baseURI).href;
  if (!document.querySelector('link[href*="wiki-progression.css"]')) {
    const style = document.createElement('link');
    style.rel = 'stylesheet'; style.href = new URL('wiki-progression.css?v=45', source).href;
    document.head.append(style);
  }
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
  // AF 1–3: local Artifact Armor index and the existing Dancer/Scholar quest guides.
  const afGroups = [{"name":"Bard AF","url":"category-artifact-armor.html#era-Bard","quests":["painful-memory.html","the-requiem.html","the-circle-of-time.html"]},{"name":"Beastmaster AF","url":"category-artifact-armor.html#era-Beastmaster","quests":["wings-of-gold.html","scattered-into-shadow.html","a-new-dawn.html"]},{"name":"Black Mage AF","url":"category-artifact-armor.html#era-Black_Mage","quests":["the-three-magi.html","recollections.html","the-root-of-the-problem.html"]},{"name":"Blue Mage AF","url":"category-artifact-armor.html#era-Blue_Mage","quests":["beginnings.html","omens.html","transformations.html"]},{"name":"Corsair AF","url":"category-artifact-armor.html#era-Corsair","quests":["equipped-for-all-occasions.html","navigating-the-unfriendly-seas.html","against-all-odds.html"]},{"name":"Dark Knight AF","url":"category-artifact-armor.html#era-Dark_Knight","quests":["dark-legacy.html","dark-puppet.html","blade-of-evil.html"]},{"name":"Dragoon AF","url":"category-artifact-armor.html#era-Dragoon","quests":["a-craftsman-s-work.html","chasing-quotas.html","knight-stalker.html"]},{"name":"Monk AF","url":"category-artifact-armor.html#era-Monk","quests":["quest-ghosts-of-the-past.html","the-first-meeting.html","true-strength.html"]},{"name":"Ninja AF","url":"category-artifact-armor.html#era-Ninja","quests":["20-in-pirate-years.html","i-ll-take-the-big-box.html","true-will.html"]},{"name":"Paladin AF","url":"category-artifact-armor.html#era-Paladin","quests":["sharpening-the-sword.html","a-boy-s-dream.html","under-oath.html"]},{"name":"Puppetmaster AF","url":"category-artifact-armor.html#era-Puppetmaster","quests":["the-wayward-automaton.html","operation-teatime.html","puppetmaster-blues.html"]},{"name":"Ranger AF","url":"category-artifact-armor.html#era-Ranger","quests":["sin-hunting.html","fire-and-brimstone.html","unbridled-passion.html"]},{"name":"Red Mage AF","url":"category-artifact-armor.html#era-Red_Mage","quests":["the-crimson-trial.html","enveloped-in-darkness.html","peace-for-the-spirit.html"]},{"name":"Samurai AF","url":"category-artifact-armor.html#era-Samurai","quests":["the-sacred-katana.html","yomi-okuri.html","a-thief-in-norg.html"]},{"name":"Summoner AF","url":"category-artifact-armor.html#era-Summoner","quests":["the-puppet-master.html","class-reunion.html","carbuncle-debacle.html"]},{"name":"Thief AF","url":"category-artifact-armor.html#era-Thief","quests":["the-tenshodo-showdown.html","as-thick-as-thieves.html","hitting-the-marquisate.html"]},{"name":"Warrior AF","url":"category-artifact-armor.html#era-Warrior","quests":["the-doorman.html","the-talekeeper-s-truth.html","the-talekeeper-s-gift.html"]},{"name":"White Mage AF","url":"category-artifact-armor.html#era-White_Mage","quests":["messenger-from-beyond.html","prelude-of-black-and-white.html","pieuje-s-decision.html"]},{"name":"Dancer AF","url":"dancer.html","quests":["the-unfinished-waltz.html","the-road-to-divadom.html","comeback-queen.html"]},{"name":"Scholar AF","url":"scholar.html","quests":["on-sabbatical.html","downward-helix.html","seeing-blood-red.html"]}];
  const af = afGroups.find(group => group.quests.includes(page));

  function localLink(anchor) {
    const raw = anchor.getAttribute('href');
    if (!raw) return null;
    try {
      const url = new URL(raw, document.baseURI);
      if (url.origin === base.origin && url.pathname.startsWith(base.pathname)) {
        const path = decodeURIComponent(url.pathname.slice(base.pathname.length));
        if (path !== page && known.has(path)) return {url: path + url.hash, name: known.get(path).name};
        return null;
      }
      if (!['horizonffxi.wiki', 'edenxi.miraheze.org'].includes(url.hostname)) return null;
    } catch { return null; }
    // An external wiki relationship becomes local only when the name is unique.
    for (const name of [anchor.textContent, anchor.getAttribute('title') || '']) {
      const matches = [...new Map((byName.get(norm(name)) || []).map(item => [item.url, item])).values()];
      if (matches.length === 1 && matches[0].url !== page) return {url: matches[0].url, name: matches[0].name};
    }
    return null;
  }
  const unique = links => [...new Map(links.map(link => [link.url, link])).values()];
  function readDirection(direction) {
    const matches = text => new RegExp('^' + direction + '\\s+(?:quest|mission)s?\\s*:?$', 'i').test(text.replace(/[←→]/g, '').trim());
    const collect = cells => {
      const anchors = cells.flatMap(cell => [...cell.querySelectorAll('a[href]')]);
      const resolved = anchors.map(localLink).filter(Boolean);
      return {found:true, links:unique(resolved), unresolved:resolved.length < anchors.length};
    };
    for (const row of article.querySelectorAll('tr')) {
      const cells = [...row.children].filter(cell => /^(TD|TH)$/.test(cell.tagName));
      const column = cells.findIndex(cell => matches(cell.textContent));
      if (column < 0) continue;
      // Imported wikis use both vertical key/value and horizontal Previous/Next tables.
      const labels = cells.filter(cell => /^(?:previous|next)\s+(?:quest|mission)/i.test(cell.textContent.replace(/[←→]/g, '').trim()));
      if (labels.length > 1) {
        const values = row.nextElementSibling?.children;
        if (values?.[column]) return collect([values[column]]);
      } else if (column === 0 && cells.length > 1) return collect(cells.slice(1));
    }
    // Some concise guides document the next step beneath a dedicated heading.
    const heading = [...article.querySelectorAll('h2, h3')].find(h => norm(h.textContent) === direction || matches(h.textContent));
    if (heading) {
      const cells = []; let node = heading.nextElementSibling;
      while (node && !/^H[1-6]$/.test(node.tagName) && cells.length < 4) {
        cells.push(node); node = node.nextElementSibling;
      }
      return collect(cells);
    }
    return {found:false, links:[], unresolved:false};
  }
  function makeLink(link) {
    const a = document.createElement('a'); a.href = link.url; a.textContent = link.name; return a;
  }
  function addProgression() {
    const tab = document.querySelector('.page-tabs .selected')?.textContent.trim();
    if (!['Quests', 'Missions'].includes(tab) && !af) return;
    const kind = tab === 'Missions' ? 'mission' : 'quest';
    const previous = readDirection('previous'); const next = readDirection('next');
    const oldNavs = [...article.querySelectorAll('nav.mission-nav')];
    const old = oldNavs[0];
    for (const [direction, state] of [['previous', previous], ['next', next]]) {
      if (state.found) continue;
      const anchor = [...(old?.querySelectorAll('a') || [])].find(a => a.textContent.trim().toLowerCase().startsWith(direction));
      const link = anchor && localLink(anchor);
      if (link) { state.found = true; state.links = [link]; }
    }
    let related = [];
    if (af) {
      const step = af.quests.indexOf(page);
      const following = af.quests[step + 1];
      // Hands/coffer branches are related AF tasks, not a mandatory AF 4.
      related = next.links.filter(link => !af.quests.includes(link.url.split('#')[0]));
      next.links = following && known.has(following) ? [{url:following, name:known.get(following).name}] : [];
      next.found = true; next.unresolved = false;
      const preceding = af.quests[step - 1];
      if (preceding && known.has(preceding)) {
        previous.links = [{url:preceding, name:known.get(preceding).name}];
        previous.found = true; previous.unresolved = false;
      } else if (!previous.found) previous.found = true;
    }
    // Unrelated standalone quests have no invented next/previous quest.
    if (!previous.found && !next.found && !old) return;
    let series = {url: kind === 'mission' ? 'missions.html' : 'quests.html', name: kind === 'mission' ? 'All missions' : 'All quests'};
    if (af) series = af;
    else {
      const candidates = [...(old?.querySelectorAll('a') || []), ...article.querySelectorAll('.breadcrumb a')];
      const link = candidates.find(a => /(?:^|\/)missions-[^/]+\.html(?:#.*)?$/.test(a.getAttribute('href') || ''));
      const local = link && localLink(link);
      if (local) series = local;
      else if (page.startsWith('borghertz-s-')) series = {url: 'category-artifact-armor.html', name: 'Artifact quests'};
    }
    function makeNav(position) {
      const nav = document.createElement('nav'); nav.className = 'wiki-progression'; nav.dataset.position = position;
      nav.setAttribute('aria-label', `${kind === 'mission' ? 'Mission' : 'Quest'} sequence — ${position}`);
      for (const [direction, state] of [['previous', previous], ['next', next]]) {
        if (direction === 'next') {
          const center = document.createElement('div'); center.className = 'progression-index'; center.append(makeLink(series));
          if (af) {
            const line = document.createElement('div'); line.className = 'progression-label'; line.style.marginTop = '6px';
            af.quests.forEach((url, i) => {
              if (i) line.append(' · ');
              if (url === page) {
                const current = document.createElement('strong'); current.textContent = 'AF ' + (i + 1); current.setAttribute('aria-current', 'step'); line.append(current);
              } else if (known.has(url)) {
                const link = makeLink({url, name: 'AF ' + (i + 1)}); link.title = known.get(url).name; line.append(link);
              }
            });
            center.append(line);
          }
          nav.append(center);
        }
        const side = document.createElement('div'); side.className = 'progression-' + direction;
        const label = document.createElement('span'); label.className = 'progression-label';
        label.textContent = (direction === 'previous' ? '← Previous ' : 'Next ') + kind + (state.links.length > 1 ? 's' : '') + (direction === 'next' ? ' →' : ''); side.append(label);
        for (const link of state.links) {
          const anchor = makeLink(link);
          if (state.links.length === 1) anchor.rel = direction === 'previous' ? 'prev' : 'next';
          side.append(anchor);
        }
        if (!state.links.length || state.unresolved) {
          const empty = document.createElement('span'); empty.className = 'progression-empty';
          empty.textContent = state.unresolved ? 'Some linked guides are not available locally.' : `No ${direction} ${kind} listed`; side.append(empty);
        }
        nav.append(side);
      }
      if (related.length) {
        const branch = document.createElement('div'); branch.className = 'progression-branches';
        const label = document.createElement('span'); label.textContent = 'Related artifact quests: '; branch.append(label);
        related.forEach((link, i) => { if (i) branch.append(' · '); branch.append(makeLink(link)); });
        nav.append(branch);
      }
      return nav;
    }
    for (const item of oldNavs) item.remove();
    const start = article.querySelector('.article-overview, .article-body'); start?.before(makeNav('top'));
    const footer = article.querySelector('.category-footer');
    if (footer) footer.before(makeNav('bottom')); else article.append(makeNav('bottom'));
  }

  function addMapViewer() {
    let dialog, title, viewport, caption, zoom, original, opener;
    function createDialog() {
      dialog = document.createElement('dialog');
      if (typeof dialog.showModal !== 'function') { dialog = null; return false; }
      dialog.className = 'wiki-map-dialog'; dialog.setAttribute('aria-labelledby', 'wiki-map-title');
      const header = document.createElement('header'); title = document.createElement('strong'); title.id = 'wiki-map-title';
      const close = document.createElement('button'); close.type = 'button'; close.textContent = 'Close'; close.addEventListener('click', () => dialog.close()); header.append(title, close);
      const controls = document.createElement('div'); controls.className = 'wiki-map-controls';
      zoom = document.createElement('button'); zoom.type = 'button'; zoom.textContent = 'Zoom in'; zoom.setAttribute('aria-pressed', 'false');
      original = document.createElement('a'); original.textContent = 'Open original image'; original.target = '_blank'; original.rel = 'noopener'; controls.append(zoom, original);
      viewport = document.createElement('div'); viewport.className = 'wiki-map-viewport'; viewport.tabIndex = 0; viewport.setAttribute('aria-label', 'Map image. Scroll to pan when zoomed.');
      caption = document.createElement('p'); caption.className = 'wiki-map-caption';
      dialog.append(header, controls, viewport, caption); document.body.append(dialog);
      zoom.addEventListener('click', () => {
        const expanded = viewport.classList.toggle('is-zoomed'); zoom.textContent = expanded ? 'Fit to screen' : 'Zoom in'; zoom.setAttribute('aria-pressed', String(expanded));
      });
      dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
      dialog.addEventListener('close', () => { opener?.focus(); });
      return true;
    }
    document.addEventListener('click', event => {
      const link = event.target.closest?.('.quest-map-enlarge, .quest-map-image, .mission-maps figure > a');
      if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const figure = link.closest('figure'); const image = figure?.querySelector('img');
      if (!image || (!dialog && !createDialog())) return;
      event.preventDefault(); opener = link;
      title.textContent = figure.dataset.mapTitle || image.alt || 'Area map';
      const map = figure.querySelector('.map-marked')?.cloneNode(true) || document.createElement('div'); map.className = 'map-marked';
      if (!map.querySelector('img')) map.append(image.cloneNode(true));
      const enlarged = map.querySelector('img'); enlarged.loading = 'eager'; enlarged.removeAttribute('id');
      viewport.replaceChildren(map); viewport.classList.remove('is-zoomed'); viewport.scrollTop = 0; viewport.scrollLeft = 0;
      zoom.textContent = 'Zoom in'; zoom.setAttribute('aria-pressed', 'false'); original.href = image.currentSrc || image.src;
      caption.textContent = figure.querySelector('.quest-map-target')?.textContent || image.alt || '';
      dialog.showModal();
    });
  }
  addMapViewer();
  addProgression();
})();
