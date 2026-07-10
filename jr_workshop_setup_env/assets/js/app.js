(function(){
  const steps = Array.isArray(window.SETUP_STEPS) ? window.SETUP_STEPS : [];
  const materials = window.MATERIALS || {tree:[], files:{}};
  const app = document.getElementById('app');
  const resetProgress = document.getElementById('resetProgress');
  const fill = document.getElementById('fill');
  const duck = document.getElementById('duck');
  const progressText = document.getElementById('progressText');
  let lastDone = countDone();
  let duckTimer = null;
  let activeMaterialPath = materials.files['README.md'] ? 'README.md' : Object.keys(materials.files || {})[0];
  const readingDocs = [
    { id: 'onboarding', title: '課前準備與操作小抄', path: '學生閱讀資料/onboarding.md' },
    { id: 'faq', title: '課後 FAQ', path: '學生閱讀資料/faq.md' }
  ];

  function esc(value){
    return String(value ?? '')
      .replace(/&/g,'&amp;')
      .replace(/</g,'&lt;')
      .replace(/>/g,'&gt;')
      .replace(/"/g,'&quot;')
      .replace(/'/g,'&#039;');
  }
  function storeGet(key){ try { return localStorage.getItem(key); } catch (_err) { return null; } }
  function storeSet(key,value){ try { localStorage.setItem(key,value); } catch (_err) {} }
  function storeRemove(key){ try { localStorage.removeItem(key); } catch (_err) {} }
  function stepById(id){ return steps.find(step => step.id === id); }
  function stepIndex(id){ return steps.findIndex(step => step.id === id); }
  function isChecked(id,index){ return storeGet(`check:${id}:${index}`) === '1'; }
  function setChecked(id,index,on){ on ? storeSet(`check:${id}:${index}`,'1') : storeRemove(`check:${id}:${index}`); }
  function isDone(step){ return storeGet(`done:${step.id}`) === '1'; }
  function setDone(step,on){ on ? storeSet(`done:${step.id}`,'1') : storeRemove(`done:${step.id}`); }
  function countDone(){ return steps.filter(isDone).length; }

  function syncStepDone(step){
    const done = step.checklist.length > 0 && step.checklist.every((_item,index) => isChecked(step.id,index));
    setDone(step, done);
    return done;
  }

  function updateProgress(animate){
    const done = countDone();
    const pct = steps.length ? (done / steps.length) * 100 : 0;
    progressText.textContent = `${done} / ${steps.length} 完成`;
    fill.style.width = `${pct}%`;
    duck.style.left = `${pct}%`;
    if (animate && done !== lastDone) {
      duck.classList.remove('sit','walk','left','dance');
      if (done < lastDone) duck.classList.add('left');
      duck.classList.add('walk');
      clearTimeout(duckTimer);
      duckTimer = setTimeout(() => {
        duck.classList.remove('walk','left','sit');
        duck.classList.add('dance');
      }, 5200);
    } else if (!duck.classList.contains('walk')) {
      duck.classList.remove('sit','left');
      duck.classList.add('dance');
    }
    lastDone = done;
  }

  function route(){
    const hash = window.location.hash || '#/';
    const itemMatch = hash.match(/^#\/item\/([^/]+)$/);
    const readingMatch = hash.match(/^#\/reading(?:\/([^/]+))?$/);
    if (itemMatch) {
      const step = stepById(decodeURIComponent(itemMatch[1]));
      if (!step) {
        window.location.hash = '#/';
        return;
      }
      renderDetail(step);
      window.scrollTo(0,0);
    } else if (readingMatch) {
      const docId = readingMatch[1] ? decodeURIComponent(readingMatch[1]) : readingDocs[0].id;
      renderReading(docId);
      window.scrollTo(0,0);
    } else {
      renderMap();
    }
    updateProgress(false);
    updateNavState(hash);
    app.focus({preventScroll:true});
  }

  function updateNavState(hash){
    document.querySelectorAll('[data-nav-route]').forEach(link => {
      const isReading = link.dataset.navRoute === 'reading' && hash.startsWith('#/reading');
      const isHome = link.dataset.navRoute === 'home' && !hash.startsWith('#/reading');
      link.classList.toggle('current', isReading || isHome);
    });
  }

  function renderMap(){
    app.innerHTML = `
      <div class="ds-container">
        <section class="hero">
          <span class="ds-pill ds-pill-accent">學生自學 · macOS 為主</span>
          <h1>Antigravity 幫你把 AI Agent 環境建起來</h1>
          <p>照著 6 個 item 走：先安裝 Antigravity、認識素材，再讓 AI Agent 幫你完成環境、狀態列與 GitHub 工作流。</p>
        </section>
        <section class="item-grid" aria-label="教學項目">
          ${steps.map(renderCard).join('')}
        </section>
      </div>`;
  }

  function renderCard(step){
    const done = isDone(step);
    return `
      <a class="ds-card item-card" href="#/item/${encodeURIComponent(step.id)}">
        <div class="item-card-top">
          <span class="ds-pill">${esc(step.num)}</span>
          <span class="item-badges">
            ${step.badge ? `<span class="badge">${esc(step.badge)}</span>` : ''}
            ${done ? '<span class="ds-pill ds-pill-success">完成</span>' : ''}
          </span>
        </div>
        <h2>${esc(step.title)}</h2>
        <p>${esc(step.goal)}</p>
      </a>`;
  }

  function renderReading(docId){
    const activeDoc = readingDocs.find(doc => doc.id === docId) || readingDocs[0];
    const file = materials.files?.[activeDoc.path];
    const content = file?.content || '';
    const body = activeDoc.id === 'faq' ? renderFaqDoc(content) : renderOnboardingDoc(content);
    app.innerHTML = `
      <div class="ds-container reading-layout">
        <section class="hero reading-hero">
          <span class="ds-pill ds-pill-accent">學員本人讀</span>
          <h1>學員閱讀資料</h1>
          <p>把課前準備與 FAQ 拆成可操作的卡片；該勾選的用 checklist，該複製的用 terminal，該查找的用 FAQ。</p>
        </section>
        <nav class="reading-tabs" aria-label="學員閱讀資料分類">
          ${readingDocs.map(doc => `<a class="reading-tab ${doc.id === activeDoc.id ? 'current' : ''}" href="#/reading/${encodeURIComponent(doc.id)}">${esc(doc.title)}</a>`).join('')}
        </nav>
        ${file ? body : '<div class="ds-card reading-card"><p class="empty-note">找不到這份閱讀資料。</p></div>'}
      </div>`;
    bindReading(activeDoc.id);
  }

  function renderOnboardingDoc(content){
    const title = firstHeading(content) || '課前準備 + 新手操作小抄';
    const intro = collectLeadingBlockquote(content);
    const checklist = sectionBetween(content, '## 一、課前 30 分鐘 checklist', '## 二、操作小抄');
    const shortcuts = sectionBetween(content, '## 二、操作小抄', '## 三、卡關自救三步');
    const rescue = sectionFrom(content, '## 三、卡關自救三步');
    return `
      <article class="reading-stack">
        <section class="ds-card reading-card reading-intro-card">
          <div class="reading-card-head">
            <span class="ds-pill">學生閱讀資料/onboarding.md</span>
            <a class="ds-btn ds-btn-ghost ds-btn-sm" href="#/item/explore-materials">回素材瀏覽器</a>
          </div>
          <h1 class="reading-title">${esc(title)}</h1>
          ${intro ? `<div class="ds-callout reading-lede"><strong>先知道</strong>${renderReaderInlineBlocks(intro)}</div>` : ''}
        </section>
        ${renderOnboardingChecklist(checklist)}
        ${renderShortcutCards(shortcuts)}
        ${renderRescueFlow(rescue)}
      </article>`;
  }

  function renderOnboardingChecklist(section){
    const items = parseChecklistItems(section);
    return `
      <section class="ds-card reading-card" aria-labelledby="precheck-title">
        <div class="reading-section-head">
          <span class="ds-pill ds-pill-accent">互動 checklist</span>
          <h2 id="precheck-title">課前 30 分鐘 checklist</h2>
        </div>
        <div class="reading-checklist">
          ${items.map((item,index) => {
            const checked = storeGet(`reading:onboarding:check:${index}`) === '1';
            return `<div class="reading-check-item ${checked ? 'done' : ''}">
              <label class="ds-check ${checked ? 'done' : ''}">
                <input type="checkbox" data-reading-check="${index}" ${checked ? 'checked' : ''}>
                <span class="ds-check-label">${renderReaderInline(item.text)}</span>
              </label>
              ${item.extra.trim() ? `<div class="reading-check-extra reader-md">${renderReaderMarkdown(stripMarkdownLinks(item.extra))}</div>` : ''}
            </div>`;
          }).join('')}
        </div>
      </section>`;
  }

  function renderShortcutCards(section){
    const cards = parseHeadingCards(section);
    return `
      <section class="reading-cardless" aria-labelledby="shortcut-title">
        <div class="reading-section-head">
          <span class="ds-pill ds-pill-accent">操作小抄</span>
          <h2 id="shortcut-title">最常卡的 8 件事</h2>
        </div>
        <div class="shortcut-grid">
          ${cards.map((card,index) => `<div class="ds-step-block shortcut-card">
            <div class="ds-step-block-head">
              <span class="ds-step-num">${index + 1}</span>
              <h3 class="ds-step-title">${esc(stripNumberPrefix(card.title))}</h3>
            </div>
            <div class="ds-step-body reader-md">${renderReaderMarkdown(card.body)}</div>
          </div>`).join('')}
        </div>
      </section>`;
  }

  function renderRescueFlow(section){
    const body = section.replace(/^##[^\n]*\n?/, '').trim();
    const lines = body.split('\n');
    const steps = [];
    const quotes = [];
    for (const line of lines) {
      if (/^\d+\.\s+/.test(line)) steps.push(line.replace(/^\d+\.\s+/, ''));
      if (/^>\s?/.test(line)) quotes.push(line.replace(/^>\s?/, ''));
    }
    return `
      <section class="ds-card reading-card" aria-labelledby="rescue-title">
        <div class="reading-section-head">
          <span class="ds-pill ds-pill-accent">卡關時</span>
          <h2 id="rescue-title">卡關自救三步</h2>
        </div>
        <div class="ds-flow reading-flow">
          ${steps.map((step,index) => `<div class="ds-step-block">
            <div class="ds-step-block-head"><span class="ds-step-num">${index + 1}</span><h3 class="ds-step-title">${rescueStepTitle(index)}</h3></div>
            <div class="ds-step-body">${renderReaderInline(step)}</div>
          </div>`).join('')}
        </div>
        ${quotes.length ? `<div class="ds-callout reading-lede"><strong>提醒</strong>${renderReaderInlineBlocks(quotes.join('\n'))}</div>` : ''}
      </section>`;
  }

  function renderFaqDoc(content){
    const title = firstHeading(content) || '課後 FAQ';
    const intro = collectLeadingBlockquote(content);
    const faqs = parseFaqItems(content);
    return `
      <article class="reading-stack">
        <section class="ds-card reading-card reading-intro-card">
          <div class="reading-card-head">
            <span class="ds-pill">學生閱讀資料/faq.md</span>
            <a class="ds-btn ds-btn-ghost ds-btn-sm" href="#/item/explore-materials">回素材瀏覽器</a>
          </div>
          <h1 class="reading-title">${esc(title)}</h1>
          ${intro ? `<div class="ds-callout reading-lede"><strong>使用方式</strong>${renderReaderInlineBlocks(intro)}</div>` : ''}
        </section>
        <section class="faq-list" aria-label="課後 FAQ">
          ${faqs.map((item,index) => `<article class="ds-card faq-item ${index === 0 ? 'is-open' : ''}">
            <button class="faq-question" type="button" data-faq-toggle aria-expanded="${index === 0 ? 'true' : 'false'}">
              <span class="ds-pill">${esc(item.num || `Q${index + 1}`)}</span>
              <span>${esc(item.question)}</span>
            </button>
            <div class="faq-answer reader-md">${renderReaderMarkdown(item.answer)}</div>
          </article>`).join('')}
        </section>
      </article>`;
  }

  function firstHeading(content){
    const match = String(content || '').match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : '';
  }

  function collectLeadingBlockquote(content){
    return String(content || '').split('\n').filter(line => line.startsWith('>')).map(line => line.replace(/^>\s?/, '')).join('\n');
  }

  function sectionBetween(content,startHeading,endHeading){
    const start = content.indexOf(startHeading);
    if (start < 0) return '';
    const end = content.indexOf(endHeading, start + startHeading.length);
    return content.slice(start + startHeading.length, end < 0 ? undefined : end).trim();
  }

  function sectionFrom(content,startHeading){
    const start = content.indexOf(startHeading);
    return start < 0 ? '' : content.slice(start).trim();
  }

  function parseChecklistItems(section){
    const items = [];
    let current = null;
    for (const line of String(section || '').split('\n')) {
      const match = line.match(/^- \[ \]\s+(.+)$/);
      if (match) {
        if (current) items.push(current);
        current = { text: match[1], extra: '' };
      } else if (current) {
        current.extra += `${line}\n`;
      }
    }
    if (current) items.push(current);
    return items;
  }

  function parseHeadingCards(section){
    const cards = [];
    let current = null;
    for (const line of String(section || '').split('\n')) {
      const match = line.match(/^###\s+(.+)$/);
      if (match) {
        if (current) cards.push(current);
        current = { title: match[1].trim(), body: '' };
      } else if (current) {
        current.body += `${line}\n`;
      }
    }
    if (current) cards.push(current);
    return cards;
  }

  function parseFaqItems(content){
    const items = [];
    let current = null;
    for (const line of String(content || '').split('\n')) {
      const match = line.match(/^###\s+(Q\d+b?\.)\s*(.+)$/i);
      if (match) {
        if (current) items.push(current);
        current = { num: match[1].replace('.', ''), question: match[2].trim(), answer: '' };
      } else if (current) {
        current.answer += `${line}\n`;
      }
    }
    if (current) items.push(current);
    return items;
  }

  function stripNumberPrefix(title){
    return String(title || '').replace(/^\d+\.\s*/, '').trim();
  }

  function rescueStepTitle(index){
    return ['先問 AI','逐行讀回覆','記下問題'][index] || `第 ${index + 1} 步`;
  }

  function stripMarkdownLinks(markdown){
    return String(markdown || '')
      .replace(/\[`([^`]+)`\]\([^)]+\)/g, '`$1`')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  }


  function renderDetail(step){
    const idx = stepIndex(step.id);
    const prev = steps[idx - 1];
    const next = steps[idx + 1];
    app.innerHTML = `
      <div class="ds-container detail-layout">
        <article class="detail-main">
          <header class="detail-header">
            <span class="ds-pill ds-pill-accent">${esc(step.num)} · ${esc(step.title)}</span>
            <h1>${esc(step.title)}</h1>
            <p class="detail-goal">${esc(step.goal)}</p>
            <div class="detail-meta">
              <span class="ds-pill">${esc(step.mac_win)}</span>
              ${step.badge ? `<span class="badge">${esc(step.badge)}</span>` : ''}
              ${isDone(step) ? '<span class="ds-pill ds-pill-success">完成</span>' : '<span class="ds-pill">尚未完成</span>'}
            </div>
          </header>
          ${renderIntro(step)}
          ${renderGoal(step)}
          ${renderWork(step)}
          ${renderChecklist(step)}
          ${renderPager(prev,next)}
        </article>
        <aside class="detail-aside">${renderAside(step)}</aside>
      </div>`;
    bindDetail(step);
    if (step.kind === 'materials') bindMaterials();
  }

  function renderIntro(step){
    return `
      <section class="detail-section" aria-labelledby="intro-title">
        <h2 id="intro-title">背景介紹</h2>
        <div class="prose"><p>${step.intro || ''}</p></div>
        ${step.analogy ? `<div class="ds-callout"><strong>想像一下</strong>${step.analogy}</div>` : ''}
      </section>`;
  }

  function renderGoal(step){
    return `
      <section class="detail-section" aria-labelledby="goal-title">
        <h2 id="goal-title">達成目標</h2>
        <div class="ds-callout ds-callout--success"><strong>完成這一步後</strong>${esc(step.goal)}</div>
      </section>`;
  }

  function renderWork(step){
    const body = step.kind === 'materials' ? renderMaterialsBrowser() : renderCommands(step);
    return `
      <section class="detail-section" aria-labelledby="work-title">
        <h2 id="work-title">步驟</h2>
        ${body}
      </section>`;
  }

  function renderCommands(step){
    if (!step.commands.length) return '<p class="empty-note">這一步沒有指令。</p>';
    return step.commands.map((command,index) => renderCommand(command,index)).join('');
  }

  function renderCommand(command,index){
    const lang = command.lang || 'text';
    const canToggle = Boolean(command.collapsible);
    const collapsed = canToggle ? 'is-collapsed' : '';
    if (lang === 'text') {
      if (isHintCommand(command)) return renderHintBlock(command,index,canToggle,collapsed);
      return renderStepBlock(command,index,canToggle,collapsed);
    }
    const hasAgentPrompt = Boolean(command.agentPrompt);
    return `
      <div class="cmd-wrap cmd-lang--${esc(lang)} ${collapsed}" data-cmd-index="${index}" data-active-mode="terminal">
        <div class="ds-term">
          <div class="ds-term-chrome cmd-chrome" data-toggle-cmd="${canToggle ? '1' : '0'}">
            <div class="cmd-chrome-main">
              <span class="ds-term-dot cmd-dot-danger"></span>
              <span class="ds-term-dot cmd-dot-warn"></span>
              <span class="ds-term-dot cmd-dot-success"></span>
              <button class="cmd-title ${canToggle ? 'can-toggle' : ''}" type="button" ${canToggle ? '' : 'tabindex="-1"'}>${esc(command.label || '指令')}</button>
              ${hasAgentPrompt ? renderCommandModeSwitch(index) : renderCommandKind(lang)}
            </div>
            <button class="cmd-copy" type="button" data-copy="${index}">複製</button>
          </div>
          ${hasAgentPrompt ? renderCommandPanes(command, lang) : `<pre class="ds-term-body cmd-code"><code>${renderCommandCode(command.code, lang)}</code></pre>`}
        </div>
        ${command.note ? `<div class="cmd-note">${esc(command.note)}</div>` : ''}
      </div>`;
  }

  function renderStepBlock(command,index,canToggle,collapsed){
    return `
      <div class="cmd-wrap cmd-lang--text ${collapsed}" data-cmd-index="${index}">
        <div class="ds-step-block">
          <div class="ds-step-block-head step-block-head" data-toggle-cmd="${canToggle ? '1' : '0'}">
            <div class="step-title-group">
              <span class="ds-step-num">${index + 1}</span>
              <h3 class="ds-step-title">
                <button class="step-title-button ${canToggle ? 'can-toggle' : ''}" type="button" ${canToggle ? '' : 'tabindex="-1"'}>${esc(stripStepPrefix(command.label || '步驟'))}</button>
              </h3>
            </div>
          </div>
          <div class="step-content">
            <div class="ds-step-body">${renderStepText(command.code)}</div>
            ${command.note ? `<div class="ds-step-note">${renderStepText(command.note)}</div>` : ''}
          </div>
        </div>
      </div>`;
  }


  function stripStepPrefix(label){
    return String(label).replace(/^\s*[①②③④⑤⑥⑦⑧⑨⑩]\s*/, '');
  }

  function isHintCommand(command){
    const label = String(command.label || '');
    return Boolean(command.collapsible) && /附註|補充|提示|看這裡/.test(label);
  }

  function renderHintBlock(command,index,canToggle,collapsed){
    return `
      <div class="cmd-wrap cmd-lang--text ${collapsed}" data-cmd-index="${index}">
        <div class="ds-callout step-hint">
          <div class="step-hint-head" data-toggle-cmd="${canToggle ? '1' : '0'}">
            <strong>
              <button class="step-title-button ${canToggle ? 'can-toggle' : ''}" type="button" ${canToggle ? '' : 'tabindex="-1"'}>${esc(command.label || '補充說明')}</button>
            </strong>
          </div>
          <div class="step-content">
            <div>${renderStepText(command.code)}</div>
            ${command.note ? `<div class="ds-step-note">${renderStepText(command.note)}</div>` : ''}
          </div>
        </div>
      </div>`;
  }

  function renderStepText(text){
    const pattern = /(https?:\/\/[^\s]+)/g;
    return String(text ?? '').split('\n').map(line => {
      let out = '';
      let last = 0;
      for (const match of line.matchAll(pattern)) {
        out += esc(line.slice(last, match.index));
        out += `<a href="${esc(match[0])}" target="_blank" rel="noreferrer">${esc(match[0])}</a>`;
        last = match.index + match[0].length;
      }
      out += esc(line.slice(last));
      return out;
    }).join('<br>');
  }


  function renderCommandKind(lang){
    if (lang === 'slash') return '<span class="cmd-kind">貼進 Claude Code</span>';
    if (lang === 'prompt') return '<span class="cmd-kind">貼進 AI Agent</span>';
    return '';
  }

  function renderCommandModeSwitch(index){
    return `
      <span class="cmd-mode-switch" role="tablist" aria-label="選擇複製內容">
        <button class="cmd-mode-tab is-active" type="button" role="tab" aria-selected="true" data-mode-tab="terminal" data-mode-index="${index}">給 Terminal</button>
        <button class="cmd-mode-tab" type="button" role="tab" aria-selected="false" data-mode-tab="agent" data-mode-index="${index}">給 AI Agent</button>
      </span>`;
  }

  function renderCommandPanes(command, lang){
    return `
      <pre class="ds-term-body cmd-code cmd-pane" data-mode-pane="terminal"><code>${renderCommandCode(command.code, lang)}</code></pre>
      <pre class="ds-term-body cmd-code cmd-pane" data-mode-pane="agent" hidden><code>${renderCommandCode(command.agentPrompt, 'prompt')}</code></pre>`;
  }

  function renderCommandCode(code, lang){
    return String(code ?? '').split('\n').map(line => renderCommandLine(line, lang)).join('\n');
  }

  function renderCommandLine(line, lang){
    if (!line.trim()) return esc(line);
    if (line.trim().startsWith('#')) return `<span class="term-comment">${esc(line)}</span>`;
    const match = line.match(/^(\s*)(\S+)(.*)$/);
    if (!match) return esc(line);
    const lead = esc(match[1]);
    const head = esc(match[2]);
    const rest = renderInlineTerm(match[3]);
    const shouldColorHead = lang === 'slash' || /^[A-Za-z_][\w.-]*$/.test(match[2]);
    return `${lead}${shouldColorHead ? `<span class="term-prompt">${head}</span>` : head}${rest}`;
  }

  function renderInlineTerm(text){
    const pattern = /(https?:\/\/[^\s]+|<[^>]+>|"[^"]*"|'[^']*'|&&|\|\||\||>>|>|2>\/dev\/null)/g;
    let out = '';
    let last = 0;
    for (const match of text.matchAll(pattern)) {
      out += esc(text.slice(last, match.index));
      const token = match[0];
      const cls = token.startsWith('http') ? 'term-folder'
        : token.startsWith('<') ? 'term-err'
        : token.startsWith('"') || token.startsWith("'") ? 'term-ok'
        : 'term-dim';
      out += `<span class="${cls}">${esc(token)}</span>`;
      last = match.index + token.length;
    }
    out += esc(text.slice(last));
    return out;
  }

  function renderChecklist(step){
    return `
      <section class="detail-section" aria-labelledby="check-title">
        <h2 id="check-title">完成後檢視</h2>
        ${step.checklist.map((item,index) => {
          const checked = isChecked(step.id,index);
          return `<label class="ds-check ${checked ? 'done' : ''}">
            <input type="checkbox" data-check-index="${index}" ${checked ? 'checked' : ''}>
            <span class="ds-check-label">${esc(item)}</span>
          </label>`;
        }).join('')}
      </section>`;
  }

  function renderPager(prev,next){
    return `
      <nav class="pager" aria-label="item 導覽">
        ${prev ? `<a class="ds-btn ds-btn-ghost" href="#/item/${encodeURIComponent(prev.id)}">← 上一個：${esc(prev.num)}</a>` : '<a class="ds-btn ds-btn-ghost" href="#/">← 回總覽</a>'}
        ${next ? `<a class="ds-btn ds-btn-primary" href="#/item/${encodeURIComponent(next.id)}">下一個：${esc(next.num)} →</a>` : '<a class="ds-btn ds-btn-primary" href="#/">完成，回總覽</a>'}
      </nav>`;
  }

  function renderAside(current){
    return `
      <div class="ds-card aside-card">
        <h3>6 個 item</h3>
        ${steps.map(step => `
          <a class="ds-side-item ${step.id === current.id ? 'current' : ''}" href="#/item/${encodeURIComponent(step.id)}">
            ${esc(step.num)} · ${esc(step.title)}${isDone(step) ? ' ✓' : ''}
          </a>`).join('')}
      </div>`;
  }

  function renderMaterialsBrowser(){
    return `
      <div class="mat-browser">
        <div class="ds-tree mat-tree" data-material-tree>${renderTree(materials.tree || [])}</div>
        <div class="ds-term mat-panel">
          <div class="ds-term-chrome">
            <span class="ds-term-dot cmd-dot-danger"></span>
            <span class="ds-term-dot cmd-dot-warn"></span>
            <span class="ds-term-dot cmd-dot-success"></span>
            <span class="mat-panel-name" data-material-name>${esc(activeMaterialPath || '尚未選檔案')}</span>
          </div>
          <div class="ds-term-body mat-panel-body" data-material-body>${renderMaterialContent(activeMaterialPath)}</div>
        </div>
      </div>`;
  }

  function renderTree(nodes, depth){
    return (nodes || []).map(node => {
      if (node.folder) {
        return `<div class="tree-node" data-depth="${depth || 0}">
          <div class="ds-tree-row tree-row folder" data-folder-path="${esc(node.path)}"><span class="ds-tree-caret open">▶</span><span>📁</span><span class="ds-mono">${esc(node.name)}</span></div>
          <div class="ds-tree-children">${renderTree(node.children || [], (depth || 0) + 1)}</div>
        </div>`;
      }
      return `<div class="ds-tree-row tree-row file ${node.path === activeMaterialPath ? 'active' : ''}" data-file-path="${esc(node.path)}"><span class="ds-tree-caret"></span><span>📄</span><span class="ds-mono">${esc(node.name)}</span></div>`;
    }).join('');
  }

  function renderMaterialContent(path){
    const file = materials.files?.[path];
    if (!file) return '<p class="empty-note">選一個檔案查看內容。</p>';
    if (file.type === 'md') return `<div class="mat-md">${renderTerminalMarkdown(file.content)}</div>`;
    if (file.type === 'binary') return `<p>${esc(file.content || '(二進位檔，不顯示)')}</p>`;
    return `<pre>${esc(file.content)}</pre>`;
  }

  function renderReaderMarkdown(text){
    return renderMarkdownBlocks(text, 'reader');
  }

  function renderTerminalMarkdown(text){
    return renderMarkdownBlocks(text, 'terminal');
  }

  function renderReaderInline(text){
    return renderInlineMarkdown(text, 'reader');
  }

  function renderReaderInlineBlocks(text){
    return String(text || '').split('\n').filter(Boolean).map(line => `<p>${renderReaderInline(line)}</p>`).join('');
  }

  function renderMarkdownBlocks(text, mode){
    const lines = String(text || '').split('\n');
    let html = '';
    let inCode = false;
    let codeLang = '';
    let codeLines = [];
    let listType = null;
    const inline = value => renderInlineMarkdown(value, mode);
    function closeList(){ if (listType) { html += `</${listType}>`; listType = null; } }
    function isTableStart(index){
      return /^\s*\|.+\|\s*$/.test(lines[index] || '') && /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(lines[index + 1] || '');
    }
    function splitTableRow(row){
      return row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(cell => cell.trim());
    }
    function renderTable(index){
      const header = splitTableRow(lines[index]);
      let cursor = index + 2;
      const rows = [];
      while (/^\s*\|.+\|\s*$/.test(lines[cursor] || '')) {
        rows.push(splitTableRow(lines[cursor]));
        cursor += 1;
      }
      const wrapClass = mode === 'terminal' ? 'mat-table-wrap' : 'reader-table-wrap';
      const tableClass = mode === 'terminal' ? 'mat-table' : 'reader-table';
      const head = `<thead><tr>${header.map(cell => `<th>${inline(cell)}</th>`).join('')}</tr></thead>`;
      const body = `<tbody>${rows.map(row => `<tr>${header.map((_h,i) => `<td>${inline(row[i] || '')}</td>`).join('')}</tr>`).join('')}</tbody>`;
      html += `<div class="${wrapClass}"><table class="${tableClass}">${head}${body}</table></div>`;
      return cursor;
    }
    function renderCodeBlock(){
      const label = codeLang ? esc(codeLang) : 'code';
      if (mode === 'terminal') {
        html += `<div class="mat-code-block"><div class="mat-code-label">${label}</div><pre class="mat-code"><code>${esc(codeLines.join('\n'))}</code></pre></div>`;
      } else {
        const codeText = codeLines.join('\n');
        html += `<div class="ds-term reader-code"><div class="ds-term-chrome reader-code-chrome"><div class="reader-code-title"><span class="ds-term-dot cmd-dot-danger"></span><span class="ds-term-dot cmd-dot-warn"></span><span class="ds-term-dot cmd-dot-success"></span><span class="reader-code-label">${label}</span></div><button class="cmd-copy" type="button" data-reader-copy="${esc(codeText)}">複製</button></div><pre class="ds-term-body reader-code-body"><code>${esc(codeText)}</code></pre></div>`;
      }
      codeLines = [];
      codeLang = '';
    }
    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i];
      const trimmed = line.trim();
      if (trimmed.startsWith('```')) {
        if (inCode) {
          renderCodeBlock();
          inCode = false;
        } else {
          closeList();
          inCode = true;
          codeLang = trimmed.replace(/^```/, '').trim();
        }
        continue;
      }
      if (inCode) { codeLines.push(line); continue; }
      if (!trimmed) { closeList(); continue; }
      if (/^---+$/.test(trimmed)) { closeList(); html += mode === 'terminal' ? '<hr class="mat-hr">' : '<hr class="reader-hr">'; continue; }
      if (isTableStart(i)) { closeList(); i = renderTable(i) - 1; continue; }
      if (/^>\s?/.test(line)) {
        closeList();
        const quoteLines = [];
        while (/^>\s?/.test(lines[i] || '')) {
          quoteLines.push((lines[i] || '').replace(/^>\s?/, ''));
          i += 1;
        }
        i -= 1;
        html += mode === 'terminal'
          ? `<div class="mat-callout"><strong>補充說明</strong>${quoteLines.map(item => `<p>${inline(item)}</p>`).join('')}</div>`
          : `<div class="ds-callout reader-quote"><strong>補充說明</strong>${quoteLines.map(item => `<p>${inline(item)}</p>`).join('')}</div>`;
        continue;
      }
      if (/^###\s+/.test(line)) { closeList(); html += `<h3>${inline(line.replace(/^###\s+/, ''))}</h3>`; continue; }
      if (/^##\s+/.test(line)) { closeList(); html += `<h2>${inline(line.replace(/^##\s+/, ''))}</h2>`; continue; }
      if (/^#\s+/.test(line)) { closeList(); html += `<h1>${inline(line.replace(/^#\s+/, ''))}</h1>`; continue; }
      if (/^-\s+/.test(line)) {
        if (listType !== 'ul') { closeList(); listType = 'ul'; html += '<ul>'; }
        html += `<li>${inline(line.replace(/^-\s+/, ''))}</li>`;
        continue;
      }
      if (/^\d+\.\s+/.test(line)) {
        if (listType !== 'ol') { closeList(); listType = 'ol'; html += '<ol>'; }
        html += `<li>${inline(line.replace(/^\d+\.\s+/, ''))}</li>`;
        continue;
      }
      closeList();
      html += `<p>${inline(line)}</p>`;
    }
    closeList();
    if (inCode) renderCodeBlock();
    return html;
  }

  function renderInlineMarkdown(src, mode){
    const linkClass = mode === 'terminal' ? 'mat-link' : '';
    let out = esc(src);
    out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
    out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m,label,href) => {
      const cleanLabel = label.replace(/^`|`$/g, '');
      if (/\.md(?:[#?].*)?$/i.test(href)) return `<code>${esc(cleanLabel)}</code>`;
      return `<a ${linkClass ? `class="${linkClass}" ` : ''}href="${esc(href)}" target="_blank" rel="noreferrer">${label}</a>`;
    });
    out = out.replace(/&lt;(https?:\/\/[^&]+)&gt;/g, (_m,url) => `<a ${linkClass ? `class="${linkClass}" ` : ''}href="${esc(url)}" target="_blank" rel="noreferrer">${esc(url)}</a>`);
    out = out.replace(/(^|[\s(>])((https?:\/\/[^\s<)]+))/g, (_m,prefix,url) => `${prefix}<a ${linkClass ? `class="${linkClass}" ` : ''}href="${esc(url)}" target="_blank" rel="noreferrer">${esc(url)}</a>`);
    return out;
  }


  function bindDetail(step){
    document.querySelectorAll('[data-copy]').forEach(button => {
      button.addEventListener('click', async event => {
        event.stopPropagation();
        const command = step.commands[Number(button.dataset.copy)];
        if (!command) return;
        const wrap = button.closest('.cmd-wrap');
        const activeMode = wrap?.dataset.activeMode || 'terminal';
        const textToCopy = activeMode === 'agent' && command.agentPrompt ? command.agentPrompt : command.code;
        await copyText(textToCopy);
        const old = button.textContent;
        button.textContent = '已複製 ✓';
        setTimeout(() => { button.textContent = old; }, 1500);
      });
    });
    document.querySelectorAll('[data-mode-tab]').forEach(tab => {
      tab.addEventListener('click', event => {
        event.stopPropagation();
        const mode = tab.dataset.modeTab;
        const wrap = tab.closest('.cmd-wrap');
        if (!mode || !wrap) return;
        wrap.dataset.activeMode = mode;
        wrap.querySelectorAll('[data-mode-tab]').forEach(button => {
          const active = button.dataset.modeTab === mode;
          button.classList.toggle('is-active', active);
          button.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        wrap.querySelectorAll('[data-mode-pane]').forEach(pane => {
          pane.hidden = pane.dataset.modePane !== mode;
        });
      });
    });
    document.querySelectorAll('[data-toggle-cmd="1"]').forEach(row => {
      row.addEventListener('click', event => {
        if (event.target.closest('[data-copy], [data-mode-tab]')) return;
        row.closest('.cmd-wrap').classList.toggle('is-collapsed');
      });
    });
    document.querySelectorAll('[data-check-index]').forEach(input => {
      input.addEventListener('change', () => {
        const index = Number(input.dataset.checkIndex);
        setChecked(step.id,index,input.checked);
        input.closest('.ds-check').classList.toggle('done',input.checked);
        syncStepDone(step);
        updateProgress(true);
        routeBadgeRefresh(step);
      });
    });
  }

  function bindReading(_docId){
    document.querySelectorAll('[data-reading-check]').forEach(input => {
      input.addEventListener('change', () => {
        const index = Number(input.dataset.readingCheck);
        input.checked ? storeSet(`reading:onboarding:check:${index}`,'1') : storeRemove(`reading:onboarding:check:${index}`);
        const item = input.closest('.reading-check-item');
        const label = input.closest('.ds-check');
        if (item) item.classList.toggle('done', input.checked);
        if (label) label.classList.toggle('done', input.checked);
      });
    });
    document.querySelectorAll('[data-faq-toggle]').forEach(button => {
      button.addEventListener('click', () => {
        const item = button.closest('.faq-item');
        if (!item) return;
        const open = !item.classList.contains('is-open');
        item.classList.toggle('is-open', open);
        button.setAttribute('aria-expanded', String(open));
      });
    });
    document.querySelectorAll('[data-reader-copy]').forEach(button => {
      button.addEventListener('click', async () => {
        await copyText(button.dataset.readerCopy || '');
        const old = button.textContent;
        button.textContent = '已複製 ✓';
        setTimeout(() => { button.textContent = old; }, 1500);
      });
    });
  }

  function routeBadgeRefresh(step){
    const done = isDone(step);
    const meta = document.querySelector('.detail-meta');
    if (meta) {
      meta.innerHTML = `
        <span class="ds-pill">${esc(step.mac_win)}</span>
        ${step.badge ? `<span class="badge">${esc(step.badge)}</span>` : ''}
        ${done ? '<span class="ds-pill ds-pill-success">完成</span>' : '<span class="ds-pill">尚未完成</span>'}`;
    }
  }

  function bindMaterials(){
    document.querySelectorAll('[data-folder-path]').forEach(row => {
      row.addEventListener('click', () => {
        const caret = row.querySelector('.ds-tree-caret');
        const children = row.parentElement.querySelector(':scope > .ds-tree-children');
        if (!children) return;
        const open = children.style.display !== 'none';
        children.style.display = open ? 'none' : 'block';
        caret.classList.toggle('open', !open);
      });
    });
    document.querySelectorAll('[data-file-path]').forEach(row => {
      row.addEventListener('click', () => {
        activeMaterialPath = row.dataset.filePath;
        document.querySelectorAll('[data-file-path]').forEach(item => item.classList.toggle('active', item === row));
        const name = document.querySelector('[data-material-name]');
        const body = document.querySelector('[data-material-body]');
        if (name) name.textContent = activeMaterialPath;
        if (body) body.innerHTML = renderMaterialContent(activeMaterialPath);
      });
    });
  }

  async function copyText(text){
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly','');
    textarea.style.position = 'fixed';
    textarea.style.inset = '0';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  }

  resetProgress.addEventListener('click', () => {
    if (!confirm('要清除所有勾選進度嗎？')) return;
    try {
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith('done:') || key.startsWith('check:')) localStorage.removeItem(key);
      });
    } catch (_err) {}
    lastDone = 0;
    updateProgress(true);
    route();
  });

  window.addEventListener('hashchange', route);
  steps.forEach(syncStepDone);
  updateProgress(false);
  route();
})();
