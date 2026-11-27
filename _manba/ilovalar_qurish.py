# -*- coding: utf-8 -*-
"""Bitta faylli veb-ilovalarni ochiq joylash uchun tayyorlaydi (mualliflik himoyasi bilan).

Har bir ilova uchun: index.html (asl faylga meta teglar, © belgisi va himoya skripti
qo'shiladi), LICENSE.txt va README.md yoziladi.

Ishga tushirish:
    python -X utf8 _manba/ilovalar_qurish.py            # hammasi
    python -X utf8 _manba/ilovalar_qurish.py afsun-arena  # bittasi
"""
import os, re, sys

SAYTLAR = r"D:\Bahtiyor\Saytlar"
MAT = os.path.join(SAYTLAR, "oquv-materiallar")
MUALLIF = "Hakimov Bahtiyorjon Muzaffar o'g'li"
MUALLIF_EN = "Bahtiyorjon Hakimov"
BELGI = "eduhakimov-himoya"  # takror qo'shilmasligi uchun belgi

FONTS = "Google Fonts loaded from fonts.googleapis.com - SIL Open Font License 1.1, (c) their respective designers."
THREE = "three.js (https://threejs.org) - MIT License, (c) three.js authors."

ILOVALAR = [
    dict(slug="servis-laboratoriya", nom="Kompyuter servis laboratoriyasi",
         manba=os.path.join(MAT, "Kompyuter servis", "Kompyuter servis laboratoriyasi.html"),
         tavsif="Kompyuter qurilmalari va ularga xizmat ko'rsatishni o'rgatadigan interaktiv o'quv platformasi: "
                "olti bo'lim, uch darajali darslar, 480 dan ortiq qurilmadan iborat 3D atlas, mashqlar va nosozlik topish trenajyori.",
         uchinchi=[THREE, FONTS], joy="right"),
    dict(slug="kompyuter-ustasi-3d", nom="Kompyuter ustasi 3D",
         manba=os.path.join(MAT, "Kompyuter servis", "Kompyuter ustasi 3D demo.html"),
         tavsif="Kompyuter ta'mirlash ustasi rolida 3D simulyator (demo): qurilmani ochish, nosozlikni topish va tuzatish.",
         uchinchi=[THREE, FONTS]),
    dict(slug="afsun-arena", nom="Afsun Arena",
         manba=os.path.join(MAT, "Boshqa", "Afsun Arena.html"),
         tavsif="O'zbek tilidagi avto-jang strategiya o'yini: qahramon sotib olasiz, maydonga terasiz, sinergiyalarni yig'asiz.",
         uchinchi=[THREE,
                   "3D character models (Adventurers & Skeletons) by Kay Lousberg (kaylousberg.com) - CC0 1.0 (public domain).",
                   FONTS]),
]


# Test Master bu yerga kiritilmagan: savollar bazasida "Destination B1" (Macmillan) va
# "Test Your Vocabulary" (Penguin) kitoblaridan olingan mashqlar bor (begona mualliflik).


def himoya_kodi(nom, url, joy="left"):
    """<head> ga meta teglar, </body> oldiga © belgisi va himoya skripti."""
    meta = (f'\n<!-- {BELGI} -->\n'
            f'<meta name="author" content="{MUALLIF}">\n'
            f'<meta name="copyright" content="(c) 2026 {MUALLIF}. Barcha huquqlar himoyalangan. All rights reserved.">\n'
            f'<meta name="rights" content="All rights reserved">\n'
            f'<link rel="license" href="LICENSE.txt">\n')
    js = r"""
<!-- %(belgi)s -->
<style>
.eh-mualliflik{position:fixed;%(joy)s:8px;bottom:6px;z-index:2147483000;font:11px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;
  color:#fff;background:rgba(20,22,26,.55);padding:3px 8px;border-radius:999px;text-decoration:none;opacity:.7;
  -webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
.eh-mualliflik:hover{opacity:1}
.eh-ogoh{position:fixed;inset:0;z-index:2147483646;background:#141517;color:#e8e8e6;display:flex;align-items:center;
  justify-content:center;text-align:center;padding:24px;font:16px/1.6 system-ui,sans-serif}
.eh-ogoh a{color:#7fb2f0}
@media print{body>*{display:none!important}body:after{content:"Bu material mualliflik huquqi bilan himoyalangan. Chop etish taqiqlangan.";display:block;padding:40px;font:16px sans-serif}}
</style>
<script>
(function () {
  var NOM = %(nom)s, ASL = %(url)s, MUALLIF = %(muallif)s;
  var host = location.hostname;
  var ruxsat = host === "eduhakimov.github.io" || host === "localhost" || host === "127.0.0.1";
  try { if (window.top !== window.self) { window.top.location = window.self.location.href; } } catch (e) { }
  function maydon(t) { return t && t.closest && t.closest("input,textarea,select,[contenteditable]"); }
  document.addEventListener("contextmenu", function (e) { if (!maydon(e.target)) { e.preventDefault(); } });
  ["copy", "cut"].forEach(function (ev) {
    document.addEventListener(ev, function (e) { if (!maydon(e.target)) { e.preventDefault(); } });
  });
  document.addEventListener("keydown", function (e) {
    var k = (e.key || "").toLowerCase(), c = e.ctrlKey || e.metaKey;
    if ((c && (k === "s" || k === "u" || k === "p")) || (c && e.shiftKey && (k === "i" || k === "j"))) {
      e.preventDefault();
    }
  }, true);
  function qur() {
    if (!ruxsat) {
      var w = document.createElement("div");
      w.className = "eh-ogoh";
      w.innerHTML = "<div><b>Bu nusxa ruxsatsiz ko'chirilgan.</b><br>\u201c" + NOM +
        "\u201d mualliflik huquqi bilan himoyalangan.<br>Muallif: " + MUALLIF +
        "<br><br>Asl manba: <a href='" + ASL + "'>" + ASL + "</a></div>";
      document.body.appendChild(w);
      return;
    }
    var a = document.createElement("a");
    a.className = "eh-mualliflik";
    a.href = "https://eduhakimov.github.io/";
    a.target = "_blank";
    a.rel = "noopener";
    a.title = "Muallif: " + MUALLIF + ". Barcha huquqlar himoyalangan.";
    a.textContent = "\u00a9 2026 Hakimov B.M.";
    document.body.appendChild(a);
  }
  if (document.body) { qur(); } else { document.addEventListener("DOMContentLoaded", qur); }
})();
</script>
"""
    import json
    js = js % dict(joy=joy, belgi=BELGI, nom=json.dumps(nom), url=json.dumps(url), muallif=json.dumps(MUALLIF))
    return meta, js


def himoyala(html, nom, url, joy="left"):
    if BELGI in html:
        return html
    meta, js = himoya_kodi(nom, url, joy)
    m = re.search(r"<head[^>]*>", html, re.I)
    if not m:
        raise SystemExit(f"{nom}: <head> topilmadi")
    html = html[:m.end()] + meta + html[m.end():]
    i = html.lower().rfind("</body>")
    if i < 0:
        html = html + js
    else:
        html = html[:i] + js + html[i:]
    return html


def litsenziya(nom, url, uchinchi):
    tp = "\n".join("  - " + u for u in uchinchi)
    return f"""{nom}
Copyright (c) 2026 {MUALLIF_EN} ({MUALLIF})

All rights reserved.
Barcha huquqlar himoyalangan.
Все права защищены.

--------------------------------------------------------------------------
O'ZBEKCHA (qisqacha)
Ushbu ilova va uning barcha materiallari (dastur kodi, matnlar, rasmlar,
dizayn, interaktiv mashqlar, testlar va boshqalar) muallifning mulki bo'lib,
O'zbekiston Respublikasining mualliflik huquqi to'g'risidagi qonunlari va
xalqaro shartnomalar bilan himoyalangan. Ilovadan {url}
manzilida shaxsiy o'rganish uchun bepul foydalanish mumkin. Muallifning
yozma ruxsatisiz nusxa ko'chirish, boshqa joyga qayta joylash, o'zgartirish,
tarqatish va tijorat maqsadida foydalanish taqiqlanadi.

РУССКИЙ (кратко)
Это приложение и все его материалы (программный код, тексты, изображения,
дизайн, интерактивные упражнения, тесты и прочее) являются собственностью
автора и охраняются законодательством Республики Узбекистан об авторском
праве и международными договорами. Пользоваться приложением по адресу
{url} для личного обучения можно бесплатно. Копирование,
размещение в другом месте, изменение, распространение и коммерческое
использование без письменного разрешения автора запрещены.
--------------------------------------------------------------------------

ENGLISH (governing text)

1. Ownership. All contents of this repository, including source code,
   text, images, audio, designs, interactive exercises, tests and
   documentation, are the property of {MUALLIF_EN} ({MUALLIF}),
   except for the third-party components listed in section 4.

2. Legal protection. These materials are protected by the copyright laws
   of the Republic of Uzbekistan (including the Law "On Copyright and
   Related Rights") and by international treaties, including the Berne
   Convention for the Protection of Literary and Artistic Works.

3. Permitted and prohibited use. You may use the application free of
   charge at {url} for personal study, and view the
   contents of this repository. Without the prior written permission of
   the copyright holder you may NOT copy, reproduce, re-host, modify,
   translate, adapt, publish, distribute, sublicense, sell, or otherwise
   use these materials, in whole or in part, for any purpose, including
   commercial purposes. Short quotations are allowed only with clear
   attribution to the author and a link to the original source.

4. Third-party components. The following components are not owned by the
   copyright holder and remain under their own licenses and copyrights:
{tp}
   Nothing in this notice restricts any rights granted by those licenses.

5. No warranty. The materials are provided "as is", without warranty of
   any kind.

Contact for permissions / Ruxsat uchun murojaat / Контакт для разрешений:
https://t.me/IT_yangi_qadam · https://github.com/eduhakimov
"""


def readme(nom, url, tavsif):
    return f"""# {nom}

{tavsif}

**Ilovani ochish:** {url}

Bitta HTML fayldan iborat: o'rnatish va server talab qilinmaydi, brauzerda ishlaydi.

## Mualliflik huquqi / Copyright

© 2026 {MUALLIF_EN} ({MUALLIF}). Barcha huquqlar himoyalangan. All rights reserved.
Ilovadan shaxsiy o'rganish uchun bepul foydalanish mumkin; nusxa ko'chirish, boshqa joyga
joylash va tarqatish muallifning yozma ruxsatisiz taqiqlanadi. Batafsil: [LICENSE.txt](LICENSE.txt)
"""


def yoz(yol, matn):
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(matn)


def qur(i):
    url = f"https://eduhakimov.github.io/{i['slug']}/"
    papka = os.path.join(SAYTLAR, i["slug"])
    os.makedirs(papka, exist_ok=True)
    with open(i["manba"], encoding="utf-8") as f:
        html = f.read()
    yoz(os.path.join(papka, "index.html"), himoyala(html, i["nom"], url, i.get("joy", "left")))
    yoz(os.path.join(papka, "LICENSE.txt"), litsenziya(i["nom"], url, i["uchinchi"]))
    yoz(os.path.join(papka, "README.md"), readme(i["nom"], url, i["tavsif"]))
    yoz(os.path.join(papka, "robots.txt"), "User-agent: *\nAllow: /\n")
    print("tayyor:", papka)


if __name__ == "__main__":
    kerak = set(sys.argv[1:])
    for i in ILOVALAR:
        if not kerak or i["slug"] in kerak:
            qur(i)
