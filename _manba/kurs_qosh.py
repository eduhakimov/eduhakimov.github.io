# -*- coding: utf-8 -*-
"""Bosh sahifaga yangi kurs kartochkasini qo'shadi (4 tilda), belgisini qo'yadi va i18n'ni yig'adi.
  python _manba/kurs_qosh.py kurslar.json [--boshiga]
kurslar.json: [{"slug","key","uz":[nom,meta,tavsif],"en":[...],"ru":[...],"zh":[...],"til":"UZ"}]
--boshiga: kartochka "Interaktiv darsliklar" ro'yxatining eng boshiga qo'yiladi (aks holda oxiriga)."""
import io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()
for k in json.load(io.open(sys.argv[1], encoding="utf-8")):
    url = "https://eduhakimov.github.io/%s/" % k["slug"]
    if url in s:
        continue
    n, m, d = k["uz"]
    card = ('<a class="kc" href="%s"><span class="ki"></span><b data-i18n="idx.c.%s">%s</b><span class="km" data-i18n="idx.c.%s.m">%s</span>'
            '<span class="kd" data-i18n="idx.c.%s.d">%s</span><span class="kt">%s</span></a>\n') % (url, k["key"], n, k["key"], m, k["key"], d, k.get("til", "UZ"))
    if "--boshiga" in sys.argv or k.get("boshiga"):
        s = re.sub(r'(<section class="sec" id="darsliklar">.*?<div class="kurslar[^"]*">\n)', lambda m: m.group(1) + card, s, count=1, flags=re.S)
    else:
        s = s.replace("<!--KURSLAR_OXIRI-->", card + "<!--KURSLAR_OXIRI-->", 1)
    for l in ("en", "ru", "zh"):
        q = os.path.join(ROOT, "_manba", "tarjima_%s.py" % l)
        t = io.open(q, encoding="utf-8").read()
        if '"c.%s"' % k["key"] not in t:
            j = t.index("INDEX = {") + len("INDEX = {")
            a, b, c = [x.replace('"', '\\"') for x in k[l]]
            t = t[:j] + '\n    "c.%s": "%s",\n    "c.%s.m": "%s",\n    "c.%s.d": "%s",' % (k["key"], a, k["key"], b, k["key"], c) + t[j:]
            io.open(q, "w", encoding="utf-8", newline="\n").write(t)
# darsliklar soni (faqat "Interaktiv darsliklar" bo'limidagi havolali kartochkalar)
i = s.index('<section class="sec" id="darsliklar">'); j = s.index("</section>", i)
n = s[i:j].count('<a class="kc" href="https://eduhakimov.github.io/')
s = re.sub(r'<div><b>\d+</b><span data-i18n="idx.st.courses">', '<div><b>%d</b><span data-i18n="idx.st.courses">' % n, s, count=1)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
for c in (["_manba/v2_kurs_ikon.py"], ["_manba/i18n_qurish.py"], ["_manba/i18n_tekshir.py"]):
    r = subprocess.run([sys.executable, "-X", "utf8"] + c, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print(c[0], (r.stdout.strip().splitlines() or [""])[-1], r.stderr[-300:])
print("darsliklar:", n)
