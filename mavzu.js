/* eduhakimov.github.io — yorug' / qorong'i rejim almashtirgich.
   <button class="tema" data-tema> bosilganda <html data-theme> almashadi va localStorage'da saqlanadi.
   Sahifa ochilishida miltillamasligi uchun <head>'da qisqa skript data-theme'ni oldindan qo'yadi. */
(function () {
  'use strict';
  var KEY = 'eduhakimov.theme', root = document.documentElement;
  function sys() { return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
  function cur() { return root.getAttribute('data-theme') || sys(); }
  function label(b) {
    var dark = cur() === 'dark', t = window.I18N && window.I18N.t;
    var s = dark ? (t ? t('tema.light', null, "Yorug' rejim") : "Yorug' rejim") : (t ? t('tema.dark', null, "Qorong'i rejim") : "Qorong'i rejim");
    b.setAttribute('aria-label', s); b.setAttribute('title', s);
  }
  function init() {
    var bs = document.querySelectorAll('[data-tema]');
    for (var i = 0; i < bs.length; i++) {
      label(bs[i]);
      bs[i].addEventListener('click', function () {
        var n = cur() === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', n);
        try { localStorage.setItem(KEY, n); } catch (e) { /* saqlab bo'lmadi */ }
        for (var j = 0; j < bs.length; j++) label(bs[j]);
      });
    }
    if (window.I18N && window.I18N.on) window.I18N.on(function () { for (var k = 0; k < bs.length; k++) label(bs[k]); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

/* Tashqi havolalar (boshqa saytga olib boradiganlar) yangi oynada ochiladi */
(function () {
  'use strict';
  function tashqi(a) {
    var h = a.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(h)) { return; }
    try { if (new URL(h).host === location.host) { return; } } catch (e) { return; }
    a.target = '_blank';
    var r = (a.getAttribute('rel') || '').split(/\s+/);
    if (r.indexOf('noopener') < 0) { r.push('noopener'); }
    a.setAttribute('rel', r.join(' ').trim());
  }
  function hammasi(root) { [].forEach.call((root || document).querySelectorAll('a[href]'), tashqi); }
  function ishga() {
    hammasi(document);
    new MutationObserver(function (ms) { ms.forEach(function (m) { [].forEach.call(m.addedNodes, function (n) { if (n.nodeType === 1) { if (n.tagName === 'A') { tashqi(n); } hammasi(n); } }); }); })
      .observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', ishga); } else { ishga(); }
})();

/* Dizayn variantlari (rang) tanlagichi va tor ekran menyusi */
(function () {
  'use strict';
  var KEY = 'eduhakimov.rang', root = document.documentElement;
  var R = [['', '#ff5b1f', 'Olovrang'], ['kok', '#2563eb', "Ko'k"], ['yashil', '#059669', 'Yashil'], ['binafsha', '#7c3aed', 'Binafsha'],
           ['qizil', '#dc2626', 'Qizil'], ['oltin', '#d97706', 'Oltin'], ['pushti', '#db2777', 'Pushti']];
  function qoy(r) { if (r) { root.setAttribute('data-rang', r); } else { root.removeAttribute('data-rang'); } }
  try { qoy(localStorage.getItem(KEY) || ''); } catch (e) { /* saqlanmagan */ }
  function t(k, d) { return (window.I18N && window.I18N.t) ? window.I18N.t(k, null, d) : d; }
  var PAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 1 0 0 18c1 0 1.6-.8 1.6-1.6 0-.5-.2-.9-.5-1.2-.3-.3-.5-.7-.5-1.2 0-.9.7-1.6 1.6-1.6H16a5 5 0 0 0 5-5c0-4-4-7.4-9-7.4z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10.5" cy="7.5" r="1"/><circle cx="15" cy="7.5" r="1"/></svg>';
  var MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  function ishga() {
    var tr = document.querySelector('.top .tr'), tema = document.querySelector('[data-tema]');
    if (tr && tema && !document.querySelector('.rang')) {
      var w = document.createElement('div'); w.className = 'rang';
      var b = document.createElement('button'); b.type = 'button'; b.className = 'rang-b'; b.innerHTML = PAL;
      var p = document.createElement('div'); p.className = 'rang-p'; p.setAttribute('role', 'menu');
      var sar = document.createElement('b'); p.appendChild(sar);
      var joriy = root.getAttribute('data-rang') || '';
      R.forEach(function (x) {
        var k = document.createElement('button'); k.type = 'button'; k.style.setProperty('--c', x[1]); k.title = x[2];
        k.setAttribute('aria-label', x[2]); k.setAttribute('aria-pressed', x[0] === joriy ? 'true' : 'false');
        k.addEventListener('click', function () {
          qoy(x[0]); try { localStorage.setItem(KEY, x[0]); } catch (e) { /* */ }
          [].forEach.call(p.querySelectorAll('button'), function (y) { y.setAttribute('aria-pressed', y === k ? 'true' : 'false'); });
          w.classList.remove('ochiq');
        });
        p.appendChild(k);
      });
      function yorliq() { var s = t('rang.label', 'Dizayn rangi'); b.setAttribute('aria-label', s); b.title = s; sar.textContent = s; }
      yorliq(); if (window.I18N && window.I18N.on) { window.I18N.on(yorliq); }
      b.addEventListener('click', function (e) { e.stopPropagation(); w.classList.toggle('ochiq'); });
      document.addEventListener('click', function (e) { if (!w.contains(e.target)) { w.classList.remove('ochiq'); } });
      w.appendChild(b); w.appendChild(p); tr.insertBefore(w, tema);
    }
    var top = document.querySelector('.top'), tn = document.querySelector('.top .tn');
    if (top && tn && tr && !document.querySelector('.menu-tg')) {
      var m = document.createElement('button'); m.type = 'button'; m.className = 'menu-tg'; m.innerHTML = MENU;
      m.setAttribute('aria-label', t('menu.label', 'Menyu')); m.setAttribute('aria-expanded', 'false');
      m.addEventListener('click', function (e) { e.stopPropagation(); var o = top.classList.toggle('menu-ochiq'); m.setAttribute('aria-expanded', o ? 'true' : 'false'); });
      [].forEach.call(tn.querySelectorAll('a'), function (a) { a.addEventListener('click', function () { top.classList.remove('menu-ochiq'); }); });
      document.addEventListener('click', function (e) { if (!top.contains(e.target)) { top.classList.remove('menu-ochiq'); } });
      tr.appendChild(m);
    }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', ishga); } else { ishga(); }
})();
