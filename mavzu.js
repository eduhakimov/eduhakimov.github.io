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
