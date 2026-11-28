# -*- coding: utf-8 -*-
"""Bir martalik: eski index.html (dizayn-v1) dan mazmunni olib, yangi dizayndagi index.html'ni yozadi.
Mazmun (kurs kartochkalari, nashrlar ro'yxati, meta/SEO) o'zgarmaydi, faqat joylashuv va uslub."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()
assert "dizayn.css" not in s, "allaqachon yangi dizaynda"

head = s[:s.index("<style>")]
kurs = s[s.index('<div class="kurslar">'):s.index("<!--KURSLAR_OXIRI-->")] + "<!--KURSLAR_OXIRI-->\n</div>"
def par(lang):
    m = re.search(r'<p class="n" lang="%s">(.*?)</p>' % lang, s, re.S); return m.group(1)
alt = re.search(r'<p class="n" data-i18n="idx.altnames">(.*?)</p>', s, re.S).group(1)
def blok(key):
    i = s.index('<h2 data-i18n="%s">' % key)
    j = s.index("</ol>", i) + 5
    b = s[i:j]
    h2 = b[:b.index("</h2>") + 5]
    return h2, b[len(h2):]
foot = re.search(r'<footer data-i18n="idx.foot">(.*?)</footer>', s, re.S).group(1)
sub = re.search(r'<p class="sub" data-i18n="idx.sub">(.*?)</p>', s, re.S).group(1)
def nav(key):
    return re.search(r'data-i18n="%s">(.*?)</a>' % re.escape(key), s).group(1)

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'
MOON = '<svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
SUN = '<svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'

pubs = ""
for key, opn in (("idx.h.2026", True), ("idx.h.2024", False), ("idx.h.book", True), ("idx.h.cert", True)):
    h2, ol = blok(key)
    pubs += '<details class="pub"%s><summary>%s</summary>%s</details>\n' % (" open" if opn else "", h2, ol)

out = head + """<script>try{var t=localStorage.getItem('eduhakimov.theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);var r=localStorage.getItem('eduhakimov.rang');if(r)document.documentElement.setAttribute('data-rang',r)}catch(e){}</script>
<meta name="theme-color" content="#0a0a0c" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#f4f2ee" media="(prefers-color-scheme: light)">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Unbounded:wght@600;700;800&display=swap">
<link rel="stylesheet" href="dizayn.css">
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="#"><i>BH</i><span>Bahtiyorjon Hakimov</span></a>
<nav class="tn"><a href="#darsliklar" data-i18n="idx.tn.courses">Darsliklar</a><a href="ishlar/" data-i18n="idx.tn.works">Ishlarim</a><a href="yutuqlar/" data-i18n="idx.tn.awards">Yutuqlar</a><a href="#nashrlar" data-i18n="idx.tn.papers">Maqolalar</a><a href="#aloqa" data-i18n="idx.tn.contact">Aloqa</a></nav>
<div class="tr"><div data-i18n-sw></div><button class="tema" type="button" data-tema aria-label="Qorong'i rejim">""" + MOON + SUN + """</button></div>
</div></header>
<main class="wrap">
<section class="hero">
<div>
<span class="eyebrow"><b></b><span data-i18n="idx.hero.eyebrow">Kompyuter grafikasi o'qituvchisi · ADU</span></span>
<h1><span class="h-a">Hakimov</span><span>Bahtiyorjon</span><span class="h-c">Muzaffar o'g'li</span></h1>
<p class="sub" data-i18n="idx.sub">""" + sub + """</p>
<div class="btns"><a class="btn btn-p" href="#darsliklar"><span data-i18n="idx.btn.courses">Interaktiv darsliklar</span>""" + ARROW + """</a><a class="btn btn-g" href="ishlar/"><span data-i18n="idx.btn.works">Barcha ishlarim</span>""" + ARROW + """</a></div>
</div>
<div class="ph"><img src="photo.jpg" alt="Bahtiyorjon Hakimov" width="400" height="400">
<span class="chip c1"><i class="t-ae">Ae</i>After Effects</span><span class="chip c2"><i class="t-ps">Ps</i>Photoshop</span><span class="chip c3"><i class="t-fg">Fg</i>Figma · UI/UX</span></div>
</section>
<section class="stats">
<div><b>47</b><span data-i18n="idx.st.papers">Ilmiy maqola va tezis</span></div>
<div><b>7</b><span data-i18n="idx.st.courses">Interaktiv darslik</span></div>
<div><b>25<em>+</em></b><span data-i18n="idx.st.projects">Loyiha va 40 ta dastur</span></div>
<div><b>45</b><span data-i18n="idx.st.certs">Xalqaro sertifikat</span></div>
</section>

<section class="sec" id="darsliklar">
<div class="sh"><div><span class="kick" data-i18n="idx.k.courses">O'quv platforma</span><h2 data-i18n="idx.h.courses">Interaktiv darsliklar</h2></div>
<p data-i18n="idx.courses.sub">""" + re.search(r'data-i18n="idx.courses.sub">(.*?)</p>', s).group(1) + """</p></div>
""" + kurs + """
</section>

<section class="sec">
<div class="sh"><div><span class="kick" data-i18n="idx.k.tools">Asboblar</span><h2 data-i18n="idx.h.tools">Ishlaydigan dasturlarim</h2></div></div>
<div class="tools">
<div class="tool"><i class="t-ps">Ps</i>Photoshop</div><div class="tool"><i class="t-ai">Ai</i>Illustrator</div><div class="tool"><i class="t-ae">Ae</i>After Effects</div><div class="tool"><i class="t-id">Id</i>InDesign</div>
<div class="tool"><i class="t-pr">Pr</i>Premiere Pro</div><div class="tool"><i class="t-cd">Cdr</i>CorelDRAW</div><div class="tool"><i class="t-fg">Fg</i>Figma</div><div class="tool"><i class="t-bl">3D</i>Blender · 3ds Max</div>
</div>
</section>

<section class="sec">
<div class="sh"><div><span class="kick" data-i18n="idx.k.links">Profillar</span><h2 data-i18n="idx.h.links">Ilmiy profillar va tarmoqlar</h2></div></div>
<nav class="pr">
<a class="big" href="ishlar/" data-i18n="idx.nav.works">""" + nav("idx.nav.works") + """</a><a class="big" href="yutuqlar/" data-i18n="idx.nav.awards">""" + nav("idx.nav.awards") + """</a>
<a href="https://orcid.org/0009-0001-7222-3508">ORCID 0009-0001-7222-3508</a><a href="https://scholar.google.com/citations?user=kTUbDqIAAAAJ">Google Scholar</a><a href="https://www.researchgate.net/profile/Bahtiyor-Hakimov-2">ResearchGate</a><a href="https://www.lens.org/lens/profile/711013301">Lens.org</a>
<a href="https://www.youtube.com/@Bahtiyor_Studio">YouTube · Bahtiyor Studio</a><a href="https://t.me/IT_yangi_qadam">Telegram · IT yangi qadam</a><a href="https://t.me/GrafikDizayn_Hakimov">Telegram · Grafik dizayn</a><a href="https://www.linkedin.com/in/bahtiyorjon-hakimov-6489a4337/">LinkedIn</a>
<a href="https://github.com/eduhakimov">GitHub</a><a href="https://www.adu.uz/oqituvchilar/581" data-i18n="idx.nav.adu">""" + nav("idx.nav.adu") + """</a>
</nav>
</section>

<section class="sec" id="nashrlar">
<div class="sh"><div><span class="kick" data-i18n="idx.k.papers">Nashrlar</span><h2 data-i18n="idx.h.papers">Ilmiy ishlar</h2></div><p data-i18n="idx.papers.sub">47 ta ilmiy ish, o'quv qo'llanma va 6 ta dasturiy guvohnoma. Ro'yxatni ochish uchun sarlavhani bosing.</p></div>
""" + pubs + """</section>

<section class="sec">
<div class="sh"><div><span class="kick" data-i18n="idx.k.about">Men haqimda</span><h2 data-i18n="idx.h.about">Qisqacha</h2></div></div>
<div class="about"><p lang="en">""" + par("en") + """</p><p lang="ru">""" + par("ru") + """</p><p lang="zh-Hans">""" + par("zh-Hans") + """</p></div>
<p class="alt" data-i18n="idx.altnames">""" + alt + """</p>
</section>

<section class="cta" id="aloqa">
<h2 data-i18n="idx.cta.title">Keling, birga yaratamiz</h2>
<div><p data-i18n="idx.cta.text">Interaktiv darslik, animatsiya yoki dizayn loyihasi bo'yicha hamkorlikka ochiqman.</p><a class="btn" href="https://t.me/GrafikDizayn_Hakimov"><span data-i18n="idx.cta.btn">Telegram'da yozish</span>""" + ARROW + """</a></div>
</section>
<footer class="foot"><p data-i18n="idx.foot">""" + foot + """</p><p>© 2026 Bahtiyorjon Hakimov. Barcha huquqlar himoyalangan.</p></footer>
</main>
<script src="i18n/index.js"></script>
<script src="i18n.js"></script>
<script src="mavzu.js"></script>
</body></html>
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(out)
print("yozildi", len(out))
