/* eduhakimov.github.io — til almashtirgich: UZ · EN · RU · 中文.
   Tashqi kutubxonasiz; file:// va GitHub Pages'da ishlaydi.
   Ishlatish:
     <el data-i18n="kalit">o'zbekcha matn</el>                 -> innerHTML almashadi
     <el data-i18n-attr="content:kalit;alt:kalit2">            -> atributlar almashadi
     <div data-i18n-sw></div>                                  -> almashtirgich shu yerga chiziladi
     (window.I18N_D=window.I18N_D||[]).push({uz:{},en:{},ru:{},zh:{}})  -> sahifa lug'ati
   O'zbekcha (uz) asl HTML'ning o'zi: JS o'chiq bo'lsa ham sahifa o'qiladi.
   Tanlov localStorage'da saqlanadi, ?lang=en|ru|zh|uz URL parametri ustun turadi. */
(function () {
  'use strict';
  var LANGS = ['uz', 'en', 'ru', 'zh'];
  var SHORT = { uz: 'UZ', en: 'EN', ru: 'RU', zh: '中文' };
  var FULL = { uz: "O'zbekcha", en: 'English', ru: 'Русский', zh: '简体中文' };
  var HTML_LANG = { uz: 'uz', en: 'en', ru: 'ru', zh: 'zh-Hans' };
  var STORE = 'eduhakimov.lang';

  /* umumiy lug'at: _manba/i18n_qurish.py yozadi, qo'lda tahrirlamang */
  var COMMON = /*COMMON*/{"en": {"badge.closed": "Closed · overview", "badge.closedproj": "Closed project", "badge.open": "Open", "foot.rights": "© 2026 Hakimov Bahtiyorjon Muzaffar o'g'li. All rights reserved.", "go.list": "List →", "go.more": "Details →", "go.open": "Open ↗", "journal": "Journal page", "menu.label": "Menu", "nav.gallery": "Gallery", "nav.home": "← Home page", "nav.sci": "← Publications", "nav.sci_plain": "Publications", "nav.works": "All projects", "nav.works_back": "← All projects", "rang.label": "Design colour", "sw.label": "Language", "tema.dark": "Dark mode", "tema.light": "Light mode", "verify": "verify ↗"}, "ru": {"badge.closed": "Закрытый · описание", "badge.closedproj": "Закрытый проект", "badge.open": "Открытый", "foot.rights": "© 2026 Hakimov Bahtiyorjon Muzaffar o'g'li. Все права защищены.", "go.list": "Список →", "go.more": "Подробнее →", "go.open": "Открыть ↗", "journal": "Страница журнала", "menu.label": "Меню", "nav.gallery": "Галерея", "nav.home": "← Главная страница", "nav.sci": "← Научные работы", "nav.sci_plain": "Научные работы", "nav.works": "Все проекты", "nav.works_back": "← Все проекты", "rang.label": "Цвет оформления", "sw.label": "Язык", "tema.dark": "Тёмная тема", "tema.light": "Светлая тема", "verify": "проверить ↗"}, "uz": {"badge.closed": "Yopiq · tavsif", "badge.closedproj": "Yopiq loyiha", "badge.open": "Ochiq", "foot.rights": "© 2026 Hakimov Bahtiyorjon Muzaffar o'g'li. Barcha huquqlar himoyalangan.", "go.list": "Ro'yxat →", "go.more": "Batafsil →", "go.open": "Ochish ↗", "journal": "Jurnal sahifasi", "menu.label": "Menyu", "nav.gallery": "Galereya", "nav.home": "← Bosh sahifa", "nav.sci": "← Ilmiy ishlar", "nav.sci_plain": "Ilmiy ishlar", "nav.works": "Barcha ishlar", "nav.works_back": "← Barcha ishlar", "rang.label": "Dizayn rangi", "sw.label": "Til", "tema.dark": "Qorong'i rejim", "tema.light": "Yorug' rejim", "verify": "tekshirish ↗"}, "zh": {"badge.closed": "未公开 · 简介", "badge.closedproj": "未公开项目", "badge.open": "公开", "foot.rights": "© 2026 Hakimov Bahtiyorjon Muzaffar o'g'li。保留所有权利。", "go.list": "列表 →", "go.more": "详情 →", "go.open": "打开 ↗", "journal": "期刊页面", "menu.label": "菜单", "nav.gallery": "作品集", "nav.home": "← 首页", "nav.sci": "← 学术成果", "nav.sci_plain": "学术成果", "nav.works": "全部项目", "nav.works_back": "← 全部项目", "rang.label": "设计配色", "sw.label": "语言", "tema.dark": "深色模式", "tema.light": "浅色模式", "verify": "验证 ↗"}}/*/COMMON*/;

  var D = { uz: {}, en: {}, ru: {}, zh: {} };
  var cur = 'uz';
  var listeners = [];
  var started = false;

  function merge(d) {
    if (!d || typeof d !== 'object') return;
    for (var i = 0; i < LANGS.length; i++) {
      var l = LANGS[i], src = d[l];
      if (!src) continue;
      for (var k in src) {
        if (Object.prototype.hasOwnProperty.call(src, k)) D[l][k] = src[k];
      }
    }
  }
  function valid(l) {
    l = String(l || '').toLowerCase();
    return LANGS.indexOf(l) >= 0 ? l : null;
  }
  function fromUrl() {
    try {
      var m = /[?&]lang=([a-zA-Z]{2})(?=&|$)/.exec(window.location.search || '');
      return m ? valid(m[1]) : null;
    } catch (e) { return null; }
  }
  function load() {
    try { return valid(window.localStorage.getItem(STORE)); } catch (e) { return null; }
  }
  function save(l) {
    try { window.localStorage.setItem(STORE, l); } catch (e) { /* saqlab bo'lmadi */ }
  }
  function trim(s) { return String(s == null ? '' : s).replace(/^\s+|\s+$/g, ''); }

  /* kalit bo'yicha matn; topilmasa o'zbekchasi, u ham bo'lmasa def yoki kalitning o'zi */
  function t(key, vars, def) {
    var s = D[cur][key];
    if (s == null) s = D.uz[key];
    if (s == null) s = (def != null ? def : key);
    s = String(s);
    if (vars) {
      s = s.replace(/\{(\w+)\}/g, function (m, k) {
        return Object.prototype.hasOwnProperty.call(vars, k) ? String(vars[k]) : m;
      });
    }
    return s;
  }

  /* ---------- DOM ---------- */
  function applyText(el) {
    var k = el.getAttribute('data-i18n');
    if (!k) return;
    if (el.__i18nOrig === undefined) el.__i18nOrig = el.innerHTML;
    var v = (cur === 'uz') ? null : D[cur][k];
    if (v == null) v = el.__i18nOrig;
    if (el.innerHTML !== v) el.innerHTML = v;
  }
  function applyAttrs(el) {
    var spec = el.getAttribute('data-i18n-attr');
    if (!spec) return;
    if (!el.__i18nAttr) el.__i18nAttr = {};
    var pairs = spec.split(';');
    for (var i = 0; i < pairs.length; i++) {
      var p = pairs[i].split(':');
      var name = trim(p[0]), key = trim(p.slice(1).join(':'));
      if (!name || !key) continue;
      if (!Object.prototype.hasOwnProperty.call(el.__i18nAttr, name)) el.__i18nAttr[name] = el.getAttribute(name);
      var v = (cur === 'uz') ? null : D[cur][key];
      if (v == null) v = el.__i18nAttr[name];
      if (v == null) el.removeAttribute(name);
      else el.setAttribute(name, v);
    }
  }
  function isLocal(h) {
    return !!h && !/^([a-zA-Z][a-zA-Z0-9+.\-]*:|\/\/|#)/.test(h);
  }
  function withLang(h, l) {
    var hash = '', i = h.indexOf('#');
    if (i >= 0) { hash = h.slice(i); h = h.slice(0, i); }
    var q = '', j = h.indexOf('?');
    if (j >= 0) { q = h.slice(j + 1); h = h.slice(0, j); }
    var parts = q ? q.split('&') : [], out = [];
    for (var n = 0; n < parts.length; n++) if (parts[n] && !/^lang=/.test(parts[n])) out.push(parts[n]);
    if (l !== 'uz') out.push('lang=' + l);
    return h + (out.length ? '?' + out.join('&') : '') + hash;
  }
  /* sayt ichidagi nisbiy havolalarga tanlangan tilni qo'shadi (file:// uchun ham) */
  function relink() {
    var as = document.querySelectorAll('a[href]');
    for (var i = 0; i < as.length; i++) {
      var a = as[i], h = a.getAttribute('data-i18n-href');
      if (h == null) {
        h = a.getAttribute('href');
        if (!isLocal(h)) continue;
        a.setAttribute('data-i18n-href', h);
      }
      a.setAttribute('href', withLang(h, cur));
    }
  }
  function updateUrl() {
    try {
      if (!window.history || !window.history.replaceState) return;
      var loc = window.location;
      var next = withLang(loc.pathname + loc.search + loc.hash, cur);
      if (next !== loc.pathname + loc.search + loc.hash) window.history.replaceState(window.history.state, '', next);
    } catch (e) { /* file:// yoki cheklangan muhit */ }
  }

  /* ---------- almashtirgich ---------- */
  var CSS = '' +
    '.i18n-sw{display:flex;justify-content:flex-end;margin:0 0 14px;font:600 12px/1 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
    '.w>.i18n-sw{margin:-26px 0 14px}' +
    '.i18n-g{display:inline-flex;flex:none;border:1px solid var(--line,rgba(127,127,127,.4));border-radius:999px;overflow:hidden;background:var(--card,transparent)}' +
    '.i18n-g button{font:inherit;letter-spacing:.03em;margin:0;border:0;border-radius:0;background:transparent;color:var(--mut,var(--muted,inherit));padding:7px 10px;min-width:40px;min-height:30px;cursor:pointer;-webkit-appearance:none;appearance:none}' +
    '.i18n-g button+button{border-left:1px solid var(--line,rgba(127,127,127,.4))}' +
    '.i18n-g button:hover{color:var(--acc,var(--accent,inherit))}' +
    '.i18n-g button[aria-pressed="true"]{background:var(--acc,var(--accent,#1f5fa8));color:var(--bg,#fff)}' +
    '.i18n-g button:focus-visible{outline:2px solid var(--acc,var(--accent,#1f5fa8));outline-offset:-3px}' +
    '@media print{.i18n-sw{display:none!important}}';
  var group = null;

  function buildSwitcher() {
    if (group) return;
    if (!document.getElementById('i18n-css')) {
      var st = document.createElement('style');
      st.id = 'i18n-css';
      st.appendChild(document.createTextNode(CSS));
      (document.head || document.documentElement).appendChild(st);
    }
    var host = document.querySelector('[data-i18n-sw]');
    if (!host) {
      if (!document.body) return;
      host = document.createElement('div');
      host.setAttribute('data-i18n-sw', '');
      var w = document.querySelector('.w');
      if (w) w.insertBefore(host, w.firstChild);
      else document.body.insertBefore(host, document.body.firstChild);
    }
    host.className = (host.className ? host.className + ' ' : '') + 'i18n-sw';
    group = document.createElement('div');
    group.className = 'i18n-g';
    group.setAttribute('role', 'group');
    for (var i = 0; i < LANGS.length; i++) {
      var l = LANGS[i], b = document.createElement('button');
      b.type = 'button';
      b.textContent = SHORT[l];
      b.title = FULL[l];
      b.setAttribute('lang', HTML_LANG[l]);
      b.setAttribute('data-lang', l);
      b.setAttribute('aria-label', FULL[l]);
      b.addEventListener('click', onClick);
      group.appendChild(b);
    }
    host.appendChild(group);
  }
  function onClick(ev) {
    var l = ev.currentTarget.getAttribute('data-lang');
    if (l && l !== cur) set(l, true);
  }
  function syncSwitcher() {
    if (!group) return;
    group.setAttribute('aria-label', t('sw.label'));
    var bs = group.getElementsByTagName('button');
    for (var i = 0; i < bs.length; i++) {
      bs[i].setAttribute('aria-pressed', bs[i].getAttribute('data-lang') === cur ? 'true' : 'false');
    }
  }

  function apply() {
    var de = document.documentElement;
    de.setAttribute('lang', HTML_LANG[cur]);
    de.setAttribute('data-lang', cur);
    var els = document.querySelectorAll('[data-i18n],[data-i18n-attr]');
    for (var i = 0; i < els.length; i++) {
      applyText(els[i]);
      applyAttrs(els[i]);
    }
    relink();
    buildSwitcher();
    syncSwitcher();
  }

  function set(l, fromUser) {
    l = valid(l) || 'uz';
    cur = l;
    if (fromUser) { save(l); updateUrl(); }
    if (started) apply();
    for (var i = 0; i < listeners.length; i++) {
      try { listeners[i](cur); } catch (e) { if (window.console) window.console.error(e); }
    }
  }

  /* ---------- ishga tushirish ---------- */
  merge(COMMON);
  var queued = window.I18N_D;
  if (queued && queued.length) for (var qi = 0; qi < queued.length; qi++) merge(queued[qi]);
  window.I18N_D = { push: function (d) { merge(d); if (started) apply(); return 0; } };

  var urlLang = fromUrl();
  cur = urlLang || load() || 'uz';
  if (urlLang) save(urlLang);

  window.I18N = {
    langs: LANGS.slice(),
    lang: function () { return cur; },
    t: t,
    set: function (l) { set(l, true); },
    on: function (fn) { if (typeof fn === 'function') listeners.push(fn); },
    apply: function () { if (started) apply(); }
  };

  function start() {
    started = true;
    apply();
  }
  if (document.body) start();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { if (!started) start(); else apply(); });
  } else if (!started) {
    start();
  }
})();
