/* global mermaid, Prism */
(function () {
  const STORAGE = {
    theme: 'sdrh-theme',
    progress: 'sdrh-progress',
    bookmarks: 'sdrh-bookmarks',
    recent: 'sdrh-recent'
  };

  const SECTIONS = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'hld', label: 'High-Level Design (HLD)' },
    { id: 'lld', label: 'Low-Level Design (LLD)' },
    { id: 'distributed', label: 'Distributed Systems' },
    { id: 'concurrency', label: 'Concurrency & Multithreading' },
    { id: 'java-library', label: 'Java Implementation Library' },
    { id: 'solid', label: 'SOLID Principles' },
    { id: 'patterns', label: 'Design Patterns' },
    { id: 'decisions', label: 'Architecture Decision Matrix' },
    { id: 'diagrams', label: 'Architecture Diagram Library' },
    { id: 'case-studies', label: 'System Design Case Studies' },
    { id: 'lld-exercises', label: 'LLD Coding Exercises' },
    { id: 'interview', label: 'Interview Questions' },
    { id: 'one-day', label: 'One-Day Revision Cheat Sheet' },
    { id: 'bookmarks', label: 'Bookmarks & Progress' }
  ];

  const el = {
    main: document.getElementById('mainContent'),
    nav: document.getElementById('nav'),
    topicList: document.getElementById('topicList'),
    search: document.getElementById('globalSearch'),
    searchMeta: document.getElementById('searchMeta'),
    progressBar: document.getElementById('progressBar'),
    sidebar: document.getElementById('sidebar'),
    overlay: document.getElementById('overlay')
  };

  const state = {
    section: 'dashboard',
    topicId: null,
    query: ''
  };

  const topics = (window.HUB_TOPICS || []).slice();
  const decisions = window.HUB_DECISIONS || [];
  const diagrams = window.HUB_DIAGRAMS || [];
  const oneDay = window.HUB_ONE_DAY || {};

  function loadJson(key, fallback) {
    try {
      return JSON.parse(localStorage.getItem(key) || 'null') ?? fallback;
    } catch {
      return fallback;
    }
  }

  function saveJson(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  let progress = loadJson(STORAGE.progress, {});
  let bookmarks = loadJson(STORAGE.bookmarks, []);
  let recent = loadJson(STORAGE.recent, []);

  function topicsForSection(sectionId) {
    if (sectionId === 'bookmarks') {
      return topics.filter((t) => bookmarks.includes(t.id));
    }
    if (sectionId === 'lld-exercises') {
      return topics.filter((t) => t.section === 'java-library' && t.exercise);
    }
    if (sectionId === 'solid') {
      return topics.filter((t) => t.section === 'lld' && t.solid);
    }
    if (sectionId === 'distributed') {
      return topics.filter((t) => t.section === 'hld' && t.distributed);
    }
    return topics.filter((t) => t.section === sectionId);
  }

  function topicById(id) {
    return topics.find((t) => t.id === id);
  }

  function sectionProgress(sectionId) {
    const list = sectionId === 'decisions' ? decisions : sectionId === 'diagrams' ? diagrams : topicsForSection(sectionId);
    if (!list.length) return 0;
    const done = list.filter((t) => progress[t.id || t.slug]).length;
    return Math.round((done / list.length) * 100);
  }

  function overallProgress() {
    const ids = [
      ...topics.map((t) => t.id),
      ...decisions.map((d) => d.id),
      ...diagrams.map((d) => d.id)
    ];
    if (!ids.length) return 0;
    const done = ids.filter((id) => progress[id]).length;
    return Math.round((done / ids.length) * 100);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderList(items, title) {
    if (!items?.length) return '';
    return `<h2>${escapeHtml(title)}</h2><ul>${items.map((x) => `<li>${escapeHtml(x)}</li>`).join('')}</ul>`;
  }

  function renderTopicBody(t) {
    const parts = [];
    parts.push(`<span class="badge ${t.status || 'complete'}">${(t.status || 'complete').toUpperCase()}</span>`);
    if (t.definition) parts.push(`<h2>Definition</h2><p>${escapeHtml(t.definition)}</p>`);
    if (t.mechanism) parts.push(`<h2>How it works</h2><p>${escapeHtml(t.mechanism)}</p>`);
    if (t.advantages?.length || t.disadvantages?.length) {
      parts.push('<div class="pros-cons">');
      if (t.advantages?.length) {
        parts.push(`<div class="box"><p class="mini-title">Advantages</p><ul>${t.advantages.map((x) => `<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`);
      }
      if (t.disadvantages?.length) {
        parts.push(`<div class="box"><p class="mini-title">Disadvantages</p><ul>${t.disadvantages.map((x) => `<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`);
      }
      parts.push('</div>');
    }
    if (t.tradeoffs) parts.push(`<h2>Trade-offs</h2><p>${escapeHtml(t.tradeoffs)}</p>`);
    if (t.useCases?.length) parts.push(renderList(t.useCases, 'Real-world use cases'));
    if (t.threadSafety) parts.push(`<h2>Thread-safety</h2><p>${escapeHtml(t.threadSafety)}</p>`);
    if (t.performance) parts.push(`<h2>Performance</h2><p>${escapeHtml(t.performance)}</p>`);
    if (t.mistakes?.length) parts.push(renderList(t.mistakes, 'Common mistakes'));
    if (t.mermaid) {
      parts.push(`<h2>Diagram</h2><div class="mermaid-wrap"><pre class="mermaid">${escapeHtml(t.mermaid)}</pre></div>`);
    }
    if (t.code) {
      parts.push(`<h2>Java example</h2><pre><code class="language-java">${escapeHtml(t.code)}</code></pre>`);
    }
    if (t.extra) parts.push(t.extra);
    if (t.interview?.length) {
      parts.push('<h2>Interview questions</h2>');
      t.interview.forEach((qa, i) => {
        parts.push(`<details class="qa"><summary>${escapeHtml(qa.q)}</summary><p class="muted">${escapeHtml(qa.a)}</p></details>`);
      });
    }
    return parts.join('');
  }

  function neighbors(current) {
    const list = topicsForSection(state.section).filter((t) => matchSearch(t));
    const idx = list.findIndex((t) => t.id === current.id);
    return { prev: list[idx - 1], next: list[idx + 1] };
  }

  function matchSearch(t) {
    if (!state.query) return true;
    const hay = [
      t.title, t.definition, t.mechanism, t.tradeoffs,
      ...(t.advantages || []), ...(t.disadvantages || []),
      ...(t.useCases || []), ...(t.tags || []),
      ...(t.interview || []).flatMap((q) => [q.q, q.a])
    ].join(' ').toLowerCase();
    return hay.includes(state.query);
  }

  function renderDashboard() {
    const cards = SECTIONS.filter((s) => s.id !== 'dashboard').map((s) => {
      const pct = sectionProgress(s.id);
      const count = s.id === 'decisions' ? decisions.length : s.id === 'diagrams' ? diagrams.length : topicsForSection(s.id).length;
      return `<a class="card" href="#/${s.id}" data-section="${s.id}">
        <h3>${escapeHtml(s.label)}</h3>
        <p class="muted">${count} items · ${pct}% revised</p>
        <div class="bar"><span style="width:${pct}%"></span></div>
      </a>`;
    }).join('');

    const checklist = topics.slice(0, 12).map((t) => {
      const checked = progress[t.id] ? 'checked' : '';
      return `<label><input type="checkbox" data-progress="${t.id}" ${checked}> ${escapeHtml(t.title)}</label>`;
    }).join('');

    const recentLinks = recent.slice(0, 8).map((id) => {
      const t = topicById(id);
      if (!t) return '';
      return `<li><a href="#/${t.section}/${t.id}">${escapeHtml(t.title)}</a></li>`;
    }).join('');

    const statusCounts = topics.reduce((acc, t) => {
      const k = t.status || 'complete';
      acc[k] = (acc[k] || 0) + 1;
      return acc;
    }, {});

    el.main.innerHTML = `
      <h1>Dashboard</h1>
      <p class="lead">Local revision hub for senior system design and Java interviews. Bookmarks and checkboxes persist in <code>localStorage</code>.</p>
      <p><strong>Overall progress:</strong> ${overallProgress()}%</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Content status</th><th>Topics</th></tr></thead>
        <tbody>
          <tr><td>Complete</td><td>${statusCounts.complete || 0}</td></tr>
          <tr><td>Partial</td><td>${statusCounts.partial || 0}</td></tr>
          <tr><td>Pending</td><td>${statusCounts.pending || 0}</td></tr>
        </tbody>
      </table></div>
      <div class="cards">${cards}</div>
      <h2>Recently viewed</h2>
      <ul>${recentLinks || '<li class="muted">Open a topic to populate this list.</li>'}</ul>
      <h2>Quick revision (sample)</h2>
      <div class="checklist">${checklist}</div>
      <div class="footer">Press <kbd>/</kbd> to search · <a href="../">Back to portal</a></div>`;

    el.main.querySelectorAll('[data-progress]').forEach((input) => {
      input.addEventListener('change', () => {
        progress[input.dataset.progress] = input.checked;
        saveJson(STORAGE.progress, progress);
        renderNav();
      });
    });
    el.main.querySelectorAll('[data-section]').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        navigate(a.dataset.section);
      });
    });
  }

  function renderDecisionMatrix() {
    const rows = decisions.filter((d) => !state.query || JSON.stringify(d).toLowerCase().includes(state.query));
    el.main.innerHTML = `
      <h1>Architecture Decision Matrix</h1>
      <p class="lead">Side-by-side comparisons for interview trade-off discussions.</p>
      ${rows.map((d) => `
        <section id="${d.id}">
          <h2>${escapeHtml(d.title)}</h2>
          <p>${escapeHtml(d.mechanism)}</p>
          <div class="pros-cons">
            <div class="box"><p class="mini-title">Advantages</p><ul>${d.advantages.map((x) => `<li>${escapeHtml(x)}</li>`).join('')}</ul></div>
            <div class="box"><p class="mini-title">Disadvantages</p><ul>${d.disadvantages.map((x) => `<li>${escapeHtml(x)}</li>`).join('')}</ul></div>
          </div>
          <p><strong>Performance:</strong> ${escapeHtml(d.performance)}</p>
          <p><strong>Scalability:</strong> ${escapeHtml(d.scalability)}</p>
          <p><strong>Complexity:</strong> ${escapeHtml(d.complexity)}</p>
          <p><strong>Best use cases:</strong> ${escapeHtml(d.best)}</p>
          <p><strong>When to avoid:</strong> ${escapeHtml(d.avoid)}</p>
          <label class="checklist"><input type="checkbox" data-progress="${d.id}" ${progress[d.id] ? 'checked' : ''}> Mark revised</label>
        </section>`).join('')}
      <div class="footer"><a href="#/dashboard">← Dashboard</a></div>`;
    bindProgressInputs();
  }

  function renderDiagramLibrary() {
    const rows = diagrams.filter((d) => !state.query || (d.title + d.explain).toLowerCase().includes(state.query));
    el.main.innerHTML = `
      <h1>Architecture Diagram Library</h1>
      <p class="lead">Mermaid diagrams with short technical notes.</p>
      ${rows.map((d) => `
        <section>
          <h2>${escapeHtml(d.title)}</h2>
          <div class="mermaid-wrap"><pre class="mermaid">${escapeHtml(d.mermaid)}</pre></div>
          <p>${escapeHtml(d.explain)}</p>
          <label class="checklist"><input type="checkbox" data-progress="${d.id}" ${progress[d.id] ? 'checked' : ''}> Mark revised</label>
        </section>`).join('')}
      <div class="footer"><a href="#/dashboard">← Dashboard</a></div>`;
    bindProgressInputs();
    renderMermaid();
  }

  function renderOneDay() {
    el.main.innerHTML = `
      <h1>One-Day Revision Cheat Sheet</h1>
      <p class="lead">Printable last-minute pass. Use <strong>Print</strong> in the sidebar.</p>
      ${oneDay.hld || ''}
      ${oneDay.lld || ''}
      ${oneDay.concurrency || ''}
      ${oneDay.questions || ''}
      ${oneDay.checklist || ''}
      ${oneDay.mistakes || ''}
      <div class="footer"><a href="#/dashboard">← Dashboard</a></div>`;
  }

  function renderInterviewSection() {
    const list = topics.filter((t) => t.section === 'interview' && matchSearch(t));
    el.main.innerHTML = `
      <h1>Interview Questions</h1>
      <p class="lead">Expand answers in place. Search filters this list.</p>
      ${list.map((t) => `<section><h2>${escapeHtml(t.title)}</h2>${renderTopicBody(t)}</section>`).join('')}
      <div class="footer"><a href="#/dashboard">← Dashboard</a></div>`;
    enhanceCodeBlocks();
    renderMermaid();
  }

  function renderTopic(t) {
    const { prev, next } = neighbors(t);
    const done = progress[t.id];
    const bookmarked = bookmarks.includes(t.id);
    pushRecent(t.id);

    el.main.innerHTML = `
      <h1>${escapeHtml(t.title)}</h1>
      <div class="topic-actions">
        <label class="checklist"><input type="checkbox" id="topicDone" ${done ? 'checked' : ''}> Revised</label>
        <span class="muted">Section: ${escapeHtml(state.section)}</span>
      </div>
      ${renderTopicBody(t)}
      <div class="nav-row">
        ${prev ? `<a class="btn" href="#/${state.section}/${prev.id}">← ${escapeHtml(prev.title)}</a>` : ''}
        ${next ? `<a class="btn" href="#/${state.section}/${next.id}">${escapeHtml(next.title)} →</a>` : ''}
      </div>
      <div class="footer"><a href="#/${state.section}">← All in section</a> · <a href="../">Portal</a></div>`;

    document.getElementById('topicDone')?.addEventListener('change', (e) => {
      progress[t.id] = e.target.checked;
      saveJson(STORAGE.progress, progress);
      renderTopicList();
    });

    enhanceCodeBlocks();
    renderMermaid();
    updateBookmarkBtn(bookmarked);
  }

  function renderSectionIndex() {
    const list = topicsForSection(state.section).filter((t) => matchSearch(t));
    if (state.section === 'decisions') return renderDecisionMatrix();
    if (state.section === 'diagrams') return renderDiagramLibrary();
    if (state.section === 'one-day') return renderOneDay();
    if (state.section === 'interview' && !state.topicId) return renderInterviewSection();

    const sectionLabel = SECTIONS.find((s) => s.id === state.section)?.label || state.section;
    el.main.innerHTML = `
      <h1>${escapeHtml(sectionLabel)}</h1>
      <p class="lead">${list.length} topics · ${sectionProgress(state.section)}% marked revised</p>
      <ul>${list.map((t) => `<li><a href="#/${state.section}/${t.id}">${escapeHtml(t.title)}</a>${progress[t.id] ? ' ✓' : ''}</li>`).join('')}</ul>
      <div class="footer"><a href="#/dashboard">← Dashboard</a></div>`;
  }

  function bindProgressInputs() {
    el.main.querySelectorAll('[data-progress]').forEach((input) => {
      input.addEventListener('change', () => {
        progress[input.dataset.progress] = input.checked;
        saveJson(STORAGE.progress, progress);
        renderNav();
      });
    });
  }

  function pushRecent(id) {
    recent = [id, ...recent.filter((x) => x !== id)].slice(0, 20);
    saveJson(STORAGE.recent, recent);
  }

  function renderMermaid() {
    if (!window.mermaid) return;
    mermaid.initialize({ startOnLoad: false, theme: document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark' });
    document.querySelectorAll('pre.mermaid').forEach((node, i) => {
      const src = node.textContent;
      const holder = node.parentElement;
      const id = 'mmd-' + Date.now() + '-' + i;
      mermaid.render(id, src).then(({ svg }) => {
        holder.innerHTML = svg;
      }).catch(() => {
        holder.innerHTML = '<p class="muted">Diagram failed to render. Serve over HTTP if opening via file://.</p>';
      });
    });
  }

  function enhanceCodeBlocks() {
    el.main.querySelectorAll('pre').forEach((pre) => {
      if (pre.querySelector('.copy')) return;
      const badge = document.createElement('span');
      badge.className = 'lang-badge';
      badge.textContent = 'Java';
      pre.appendChild(badge);
      const btn = document.createElement('button');
      btn.className = 'copy';
      btn.type = 'button';
      btn.textContent = 'Copy';
      btn.addEventListener('click', async () => {
        const code = pre.querySelector('code');
        const text = (code ? code.textContent : pre.textContent).trim();
        try {
          await navigator.clipboard.writeText(text);
        } catch {
          const area = document.createElement('textarea');
          area.value = text;
          document.body.appendChild(area);
          area.select();
          document.execCommand('copy');
          area.remove();
        }
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = 'Copy'; }, 900);
      });
      pre.appendChild(btn);
    });
    if (window.Prism) Prism.highlightAllUnder(el.main);
  }

  function renderNav() {
    el.nav.innerHTML = SECTIONS.map((s) => {
      const pct = sectionProgress(s.id);
      return `<a href="#/${s.id}" data-nav="${s.id}" class="${s.id === state.section ? 'active' : ''}">${escapeHtml(s.label)} <span class="muted">(${pct}%)</span></a>`;
    }).join('');
    el.nav.querySelectorAll('[data-nav]').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        navigate(a.dataset.nav);
      });
    });
  }

  function renderTopicList() {
    if (['dashboard', 'decisions', 'diagrams', 'one-day'].includes(state.section)) {
      el.topicList.innerHTML = '';
      return;
    }
    const list = topicsForSection(state.section).filter((t) => matchSearch(t));
    el.topicList.innerHTML = list.map((t) => {
      const cls = [state.topicId === t.id ? 'active' : '', progress[t.id] ? 'done' : '', bookmarks.includes(t.id) ? 'bookmarked' : ''].filter(Boolean).join(' ');
      return `<a class="${cls}" href="#/${state.section}/${t.id}">${escapeHtml(t.title)}</a>`;
    }).join('');
    el.topicList.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', closeSidebar);
    });
  }

  function navigate(section, topicId) {
    state.section = section;
    state.topicId = topicId || null;
    if (section === 'dashboard') {
      renderDashboard();
    } else if (topicId) {
      const t = topicById(topicId);
      if (t) renderTopic(t);
      else renderSectionIndex();
    } else {
      renderSectionIndex();
    }
    renderNav();
    renderTopicList();
    window.scrollTo(0, 0);
    updateProgressBar();
  }

  function parseRoute() {
    const hash = location.hash.replace(/^#\/?/, '');
    const parts = hash.split('/').filter(Boolean);
    const section = parts[0] || 'dashboard';
    const topicId = parts[1] || null;
    if (!SECTIONS.some((s) => s.id === section)) {
      navigate('dashboard');
      return;
    }
    navigate(section, topicId);
  }

  function updateBookmarkBtn(active) {
    const btn = document.getElementById('bookmarkBtn');
    if (!btn) return;
    btn.textContent = active ? '★ Bookmarked' : '☆ Bookmark';
  }

  function toggleBookmark() {
    if (!state.topicId) return;
    if (bookmarks.includes(state.topicId)) {
      bookmarks = bookmarks.filter((id) => id !== state.topicId);
    } else {
      bookmarks.push(state.topicId);
    }
    saveJson(STORAGE.bookmarks, bookmarks);
    renderTopicList();
    updateBookmarkBtn(bookmarks.includes(state.topicId));
  }

  function initTheme() {
    const saved = localStorage.getItem(STORAGE.theme);
    if (saved === 'light' || (!saved && window.matchMedia('(prefers-color-scheme: light)').matches)) {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  }

  function toggleTheme() {
    const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next === 'light' ? 'light' : '');
    localStorage.setItem(STORAGE.theme, next);
  }

  function openSidebar() {
    el.sidebar.classList.add('open');
    el.overlay.classList.add('open');
  }

  function closeSidebar() {
    el.sidebar.classList.remove('open');
    el.overlay.classList.remove('open');
  }

  function updateProgressBar() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    el.progressBar.style.width = max > 0 ? ((window.scrollY / max) * 100) + '%' : '0%';
  }

  function runSearch() {
    state.query = el.search.value.trim().toLowerCase();
    const hits = topics.filter((t) => matchSearch(t)).length;
    el.searchMeta.textContent = state.query ? `${hits} topic(s) match` : '';
    renderTopicList();
    if (state.topicId) {
      const t = topicById(state.topicId);
      if (t && !matchSearch(t)) renderSectionIndex();
    } else if (state.section !== 'dashboard') {
      renderSectionIndex();
    }
  }

  document.getElementById('themeBtn')?.addEventListener('click', toggleTheme);
  document.getElementById('themeBtnMobile')?.addEventListener('click', toggleTheme);
  document.getElementById('printBtn')?.addEventListener('click', () => window.print());
  document.getElementById('bookmarkBtn')?.addEventListener('click', toggleBookmark);
  document.getElementById('menuBtn')?.addEventListener('click', openSidebar);
  el.overlay.addEventListener('click', closeSidebar);
  el.search.addEventListener('input', runSearch);
  window.addEventListener('hashchange', parseRoute);
  window.addEventListener('scroll', updateProgressBar, { passive: true });
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== el.search) {
      e.preventDefault();
      el.search.focus();
    }
    if (e.key === 'Escape') {
      el.search.value = '';
      runSearch();
      el.search.blur();
      closeSidebar();
    }
  });

  initTheme();
  parseRoute();
  if (!location.hash) location.hash = '#/dashboard';
})();