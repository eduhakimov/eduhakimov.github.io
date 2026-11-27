# -*- coding: utf-8 -*-
"""Bir martalik: to'liq nashrlar ro'yxatini bosh sahifadan alohida ilmiy-ishlar/index.html sahifasiga ko'chiradi,
bosh sahifada esa qisqa umumlashma qoldiradi. Tarjimalar: INDEX -> ILMIY (ilm.*)."""
import io, os, re, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, "_manba")
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()
assert "ilmiy-ishlar/" not in s.split('<section class="sec" id="nashrlar">')[1].split("</section>")[0], "allaqachon"

_sp = importlib.util.spec_from_file_location("ik", os.path.join(M, "v2_ikonlar.py"))
ik = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ik)
_src = io.open(os.path.join(M, "ishlar_qurish.py"), encoding="utf-8").read()
_ns = {}; exec(_src[_src.index("TEMA_HEAD = ("):_src.index("# ---------- tillar (i18n)")], _ns)
TEMA_HEAD, TOP = _ns["TEMA_HEAD"], _ns["TOP"]

i = s.index('<section class="sec" id="nashrlar">'); j = s.index("</section>", i) + len("</section>")
sec = s[i:j]
pubs = "".join(re.findall(r'<details class="pub".*?</details>\n?', sec, flags=re.S))
pubs_full = pubs.replace('<details class="pub">', '<details class="pub" open>')
# kalitlar: idx.* -> ilm.* (journal umumiy lug'atda qoladi)
for k in ("h.2026", "h.2024", "h.book", "book.j", "h.cert", "certpre"):
    pubs_full = pubs_full.replace('data-i18n="idx.%s"' % k, 'data-i18n="ilm.%s"' % k)

# eng so'nggi 3 ta maqola (2026 ro'yxatidan)
d26 = re.search(r'<details class="pub" open><summary><h2 data-i18n="idx.h.2026">.*?</details>', sec, flags=re.S).group(0)
lis = re.findall(r"<li>(.*?)</li>", d26, flags=re.S)[:3]
def li(x):
    t = re.search(r'<span class="t">(.*?)</span>', x).group(1)
    jr = re.search(r'<span class="j">(.*?)</span>', x).group(1)
    a = re.search(r'<a href="([^"]+)"', x)
    h = a.group(1) if a else "ilmiy-ishlar/"
    return '<a class="pubk" href="%s"><b>%s</b><span>%s</span></a>' % (h, t, jr)
yangi = "".join(li(x) for x in lis)

OQ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'
QISQA = ('<section class="sec" id="nashrlar">\n'
         '<div class="sh"><div><span class="kick" data-i18n="idx.k.papers">Nashrlar</span><h2 data-i18n="idx.h.papers">Ilmiy ishlar</h2></div>'
         '<p data-i18n="idx.papers.sub2">Kompyuter grafikasi, 2D animatsiyani avtomatlashtirish, UI/UX va tasvirga ishlov berish bo\'yicha ilmiy ishlar.</p></div>\n'
         '<div class="pubs">'
         '<div><b>13</b><span data-i18n="idx.pb.26">maqola va tezis · 2026 (magistratura)</span></div>'
         '<div><b>34</b><span data-i18n="idx.pb.24">maqola · 2024 (bakalavriat)</span></div>'
         '<div><b>1</b><span data-i18n="idx.pb.bk">o\'quv qo\'llanma · «Kompyuter grafikasi»</span></div>'
         '<div><b>6</b><span data-i18n="idx.pb.dgu">dasturiy mahsulot guvohnomasi</span></div>'
         '</div>\n'
         '<div class="pubn"><span class="kick" data-i18n="idx.pb.new">So\'nggi maqolalar</span>' + yangi + '</div>\n'
         '<div class="btns" style="margin-top:18px"><a class="btn btn-p" href="ilmiy-ishlar/"><span data-i18n="idx.pb.all">Barcha ilmiy ishlar</span>' + OQ + '</a>'
         '<a class="btn btn-g" href="https://orcid.org/0009-0001-7222-3508"><span>ORCID</span>' + OQ + '</a>'
         '<a class="btn btn-g" href="https://scholar.google.com/citations?user=kTUbDqIAAAAJ"><span>Google Scholar</span>' + OQ + '</a></div>\n'
         '</section>')
s = s[:i] + QISQA + s[j:]
s = s.replace('<a href="#nashrlar" data-i18n="idx.tn.papers">', '<a href="#nashrlar" data-i18n="idx.tn.papers">', 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)

# ---------- alohida sahifa ----------
os.makedirs(os.path.join(ROOT, "ilmiy-ishlar"), exist_ok=True)
foot = re.search(r'<p data-i18n="idx.foot">(.*?)</p>', s).group(1)
html = ('<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title data-i18n="ilm.title">Ilmiy ishlar – Hakimov Bahtiyorjon Muzaffar o\'g\'li | Andijon davlat universiteti</title>\n'
        '<meta name="description" data-i18n-attr="content:ilm.desc" content="Hakimov B.M. ilmiy ishlarining to\'liq ro\'yxati: 47 ta maqola va tezis, o\'quv qo\'llanma va dasturiy mahsulot guvohnomalari.">\n'
        '<meta name="author" content="Hakimov Bahtiyorjon Muzaffar o\'g\'li"><meta name="copyright" content="(c) Hakimov B.M. Barcha huquqlar himoyalangan">\n'
        '<link rel="canonical" href="https://eduhakimov.github.io/ilmiy-ishlar/"><meta property="og:image" content="https://eduhakimov.github.io/photo.jpg">\n'
        + TEMA_HEAD +
        '<style>.w{max-width:1040px;margin:0 auto;padding:44px 20px 64px}h1{margin:0 0 10px;font:800 clamp(30px,4.6vw,52px)/1.02 var(--fd);letter-spacing:-.03em}'
        '.sub{color:var(--mut);margin:0 0 26px;font-size:15.5px;line-height:1.6;max-width:760px}.pub{margin-bottom:16px}'
        '.foot{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin:40px 0 0;padding:26px 0 0;border-top:1px solid var(--line);color:var(--mut);font-size:13px}.foot p{margin:0}</style>\n'
        '</head><body>\n' + TOP + '<div class="w">\n'
        '<h1 data-i18n="ilm.h1">Ilmiy ishlar</h1>\n'
        '<p class="sub" data-i18n="ilm.sub">47 ta ilmiy maqola va tezis, o\'quv qo\'llanma va 6 ta dasturiy mahsulot guvohnomasi. Ro\'yxat ORCID va jurnal sahifalari bo\'yicha tuzilgan.</p>\n'
        + pubs_full +
        '<footer class="foot">' + ik.SOC + '<p data-i18n="ilm.foot">' + foot + '</p><p data-i18n="foot.rights">© 2026 Hakimov Bahtiyorjon Muzaffar o\'g\'li. Barcha huquqlar himoyalangan.</p></footer>\n'
        '</div>\n<script src="../i18n/ilmiy.js"></script>\n<script src="../i18n.js"></script>\n<script src="../mavzu.js"></script>\n</body></html>\n')
io.open(os.path.join(ROOT, "ilmiy-ishlar", "index.html"), "w", encoding="utf-8", newline="\n").write(html)
print("ok", len(lis))
