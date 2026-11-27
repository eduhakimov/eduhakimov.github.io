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
