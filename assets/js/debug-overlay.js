/*
 * html-debug-overlay — drop-in visual text-debug tool for any HTML product.
 *
 * What it does (no build step required):
 *   1. Adds a 🐞 toggle button (bottom-left). Click → debug mode on/off.
 *   2. In debug mode: SELECT any text on the page (圈選) to capture it, or
 *      click a leaf element to capture its whole text.
 *   3. A right-side panel lists each capture with: locator + original text +
 *      a "想怎麼改?" input. "複製全部" copies a markdown fix-list to paste
 *      back into Claude Code, which then edits the source.
 *
 * Locator strategy is HYBRID:
 *   - element has [data-loc]  → use that stable id (e.g. "concept.points[0]")
 *   - otherwise               → compute a tag:nth-of-type DOM path
 *   Either way the captured "選取" string is the precise find/replace target,
 *   so source edits stay exact even when the DOM path is fuzzy.
 *
 * Auto-on: append ?debug to the URL, or set window.__DEBUG_OVERLAY__ = true
 * before this script loads.
 */
(function () {
  'use strict';
  var items = [], panel = null, list = null, btn = null;

  function esc(x) {
    return (x || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function snippet(s, n) {
    return (s || '').trim().replace(/\s+/g, ' ').slice(0, n || 200);
  }
  function active() {
    return document.body.classList.contains('dbg-active');
  }

  // ---------- locator computation ----------
  function seg(n) {
    var t = (n.tagName || '').toLowerCase();
    if (n.id) return t + '#' + n.id;
    var p = n.parentNode;
    if (p && p.children) {
      var same = [].filter.call(p.children, function (c) { return c.tagName === n.tagName; });
      if (same.length > 1) t += ':nth-of-type(' + ([].indexOf.call(same, n) + 1) + ')';
    }
    return t;
  }
  function domPath(node) {
    var parts = [], n = node;
    while (n && n.nodeType === 1 && n.tagName !== 'BODY') {
      parts.unshift(seg(n));
      if (n.id) break;        // an id is unique enough — stop climbing
      n = n.parentNode;
    }
    return parts.join('>');
  }
  function relPath(root, node) {
    var parts = [], n = node;
    while (n && n !== root && n.nodeType === 1) { parts.unshift(seg(n)); n = n.parentNode; }
    return parts.join('>');
  }
  // Prefer a [data-loc] ancestor; fall back to a computed DOM path.
  function locate(el, deepTarget) {
    var anchor = el.closest && el.closest('[data-loc]');
    if (anchor) {
      var loc = anchor.getAttribute('data-loc');
      if (deepTarget && deepTarget !== anchor) {
        var rp = relPath(anchor, deepTarget);
        if (rp) loc += ' › ' + rp;
      }
      return { loc: loc, kind: 'data-loc' };
    }
    return { loc: domPath(deepTarget || el), kind: 'dom-path' };
  }

  // ---------- capture ----------
  function add(it) {
    if (items.some(function (x) { return x.loc === it.loc && x.sel === it.sel; })) return;
    items.push(it);
    render();
  }

  // Text-range selection (圈選). Returns true if a selection was handled.
  function captureSelection() {
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) return false;
    var node = sel.getRangeAt(0).commonAncestorContainer;
    var el = node.nodeType === 1 ? node : node.parentNode;
    if (!el || (el.closest && el.closest('#dbg-panel'))) return true; // ignore our own UI
    var loc = locate(el, el);
    add({
      loc: loc.loc, kind: loc.kind,
      context: snippet(el.textContent, 240),
      sel: snippet(sel.toString(), 240),
      acts: [{ name: '改文字', val: '' }]
    });
    sel.removeAllRanges();
    return true;
  }

  // Click fallback: only capture a [data-loc] element or a leaf element,
  // never a big container (push the user toward selecting text instead).
  function captureClick(target) {
    var anchor = target.closest && target.closest('[data-loc]');
    var el = anchor || (target.children && target.children.length === 0 ? target : null);
    if (!el || el === document.body) return;
    var loc = locate(el, target);
    var text = snippet(el.textContent, 240);
    add({ loc: loc.loc, kind: loc.kind, context: text, sel: text, acts: [{ name: '改文字', val: '' }] });
  }

  // ---------- panel ----------
  var ACTIONS = ['改文字', '刪除', '樣式(顏色/字級/粗細)', '位置/排版', '其他'];

  function ph(name) { return name === '改文字' ? '想改成什麼?' : '說明想怎麼改'; }

  function render() {
    if (!list) return;
    list.innerHTML = items.length ? items.map(function (it, k) {
      var badge = '<span class="dbg-kind dbg-kind-' + it.kind + '">' + it.kind + '</span>';
      // multi-select chips: a row can carry several actions at once
      var chips = ACTIONS.map(function (a) {
        var on = it.acts.some(function (x) { return x.name === a; });
        return '<button class="dbg-chip' + (on ? ' on' : '') + '" data-k="' + k + '" data-a="' + esc(a) + '">' + a + '</button>';
      }).join('');
      // one instruction input per chosen action
      var fields = it.acts.map(function (x) {
        return '<div class="dbg-field"><span class="dbg-flabel">' + esc(x.name) + '</span>' +
          '<textarea class="dbg-fix" data-k="' + k + '" data-a="' + esc(x.name) + '" placeholder="' + ph(x.name) + '">' + esc(x.val) + '</textarea></div>';
      }).join('');
      return '<div class="dbg-row">' +
        '<button class="dbg-del" data-k="' + k + '" title="移除">×</button>' +
        '<div class="dbg-loc">' + badge + esc(it.loc) + '</div>' +
        '<div class="dbg-cur">選取: <b>' + esc(it.sel) + '</b></div>' +
        '<div class="dbg-chips">' + chips + '</div>' + fields +
        '</div>';
    }).join('') : '<div class="dbg-empty">圈選頁面文字加入清單,或點擊單一文字元件。</div>';
  }

  function copyAll() {
    var text = items.map(function (it) {
      var acts = it.acts.length
        ? it.acts.map(function (x) { return '    - ' + x.name + ' → ' + (x.val || '(待填)'); }).join('\n')
        : '    - (未指定動作)';
      return '- loc: ' + it.loc + '  [' + it.kind + ']\n' +
        '  context: ' + it.context + '\n' +
        '  選取: ' + it.sel + '\n' +
        '  動作:\n' + acts;
    }).join('\n');
    if (navigator.clipboard) navigator.clipboard.writeText(text);
    var b = panel.querySelector('#dbg-copy');
    b.textContent = '已複製!'; setTimeout(function () { b.textContent = '複製全部'; }, 1500);
  }

  function buildPanel() {
    if (panel) return;
    panel = document.createElement('div');
    panel.id = 'dbg-panel';
    panel.innerHTML =
      '<div class="dbg-h">🐞 修正清單' +
      '<button id="dbg-clear">清空</button>' +
      '<button id="dbg-copy">複製全部</button></div>' +
      '<div id="dbg-list"></div>';
    document.body.appendChild(panel);
    list = panel.querySelector('#dbg-list');
    list.addEventListener('input', function (e) {
      if (!e.target.classList.contains('dbg-fix')) return;
      var it = items[e.target.dataset.k];
      var a = it.acts.filter(function (x) { return x.name === e.target.dataset.a; })[0];
      if (a) a.val = e.target.value;
    });
    list.addEventListener('click', function (e) {
      var t = e.target;
      if (t.classList.contains('dbg-del')) { items.splice(+t.dataset.k, 1); render(); return; }
      if (t.classList.contains('dbg-chip')) {
        var it = items[t.dataset.k], name = t.dataset.a;
        var i = it.acts.map(function (x) { return x.name; }).indexOf(name);
        if (i >= 0) it.acts.splice(i, 1); else it.acts.push({ name: name, val: '' });
        render();
      }
    });
    panel.querySelector('#dbg-clear').onclick = function () { items.length = 0; render(); };
    panel.querySelector('#dbg-copy').onclick = copyAll;
    render();
  }

  // ---------- hover highlight ----------
  // A single floating box that tracks the element under the cursor, so the user
  // sees the bounds of the component that will be captured — works for any HTML,
  // not just [data-loc] elements.
  var hl = null;
  function hlTarget(t) {
    return (t.closest && t.closest('[data-loc]')) || t; // box what would be captured
  }
  function moveHl(e) {
    if (!active() || !hl) return;
    var t = e.target;
    if (t === btn || t === hl || (t.closest && t.closest('#dbg-panel'))) { hl.style.display = 'none'; return; }
    var r = hlTarget(t).getBoundingClientRect();
    if (!r.width && !r.height) { hl.style.display = 'none'; return; }
    hl.style.cssText = 'display:block;left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;height:' + r.height + 'px;';
  }

  function setDebug(on) {
    document.body.classList.toggle('dbg-active', on);
    btn.classList.toggle('on', on);
    if (on) {
      buildPanel(); panel.style.display = 'block';
      if (!hl) { hl = document.createElement('div'); hl.id = 'dbg-hl'; document.body.appendChild(hl); }
    } else {
      if (panel) panel.style.display = 'none';
      if (hl) hl.style.display = 'none';
    }
  }

  // ---------- wiring ----------
  btn = document.createElement('button');
  btn.id = 'dbg-btn'; btn.type = 'button'; btn.textContent = '🐞';
  btn.title = 'Debug 模式:點我切換,再圈選頁面文字定位';
  document.body.appendChild(btn);
  btn.addEventListener('click', function () { setDebug(!active()); });

  document.addEventListener('mousemove', moveHl);
  window.addEventListener('scroll', function () { if (hl) hl.style.display = 'none'; }, true);

  // A drag-select ends on mouseup; a plain click also fires mouseup (collapsed
  // selection) → treat as element-click fallback. setTimeout lets the selection settle.
  document.addEventListener('mouseup', function (e) {
    if (!active()) return;
    if ((e.target.closest && e.target.closest('#dbg-panel')) || e.target === btn) return;
    setTimeout(function () {
      if (!captureSelection()) captureClick(e.target);
    }, 0);
  });

  // Stop links/buttons from navigating while in debug mode.
  document.addEventListener('click', function (e) {
    if (!active()) return;
    if ((e.target.closest && e.target.closest('#dbg-panel')) || e.target === btn) return;
    e.preventDefault(); e.stopPropagation();
  }, true);

  if (location.search.indexOf('debug') >= 0 || window.__DEBUG_OVERLAY__) setDebug(true);
})();
