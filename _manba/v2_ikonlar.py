# -*- coding: utf-8 -*-
"""index.html: dasturlar va profillar bo'limlarini brend logolari bilan qayta yozadi, aloqa ma'lumotlarini qo'shadi.
Logolar: simple-icons (CC0) yo'llari _manba/ikonlar/*.svg dan olinadi.
  python _manba/v2_ikonlar.py          (qayta ishga tushirsa ham xavfsiz: bo'limlar belgilar orasida almashtiriladi)
Dastur kartochkalari Telegram guruhidagi mavzularga havola: MAVZU lug'atini to'ldiring."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IK = os.path.join(ROOT, "_manba", "ikonlar")
GURUH = "https://t.me/GrafikDizayn_Hakimov"
POCHTA = "eduhakimov@gmail.com"

# Telegram guruhidagi mavzu (topic) havolalari: bo'sh bo'lsa guruhning o'ziga olib boradi
MAVZU = {}


def yol(nom):
    s = io.open(os.path.join(IK, nom + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', s).group(1)


def svg(nom=None, d=None):
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s"/></svg>' % (d or yol(nom))


# o'z ikoni yo'qlar uchun oddiy chiziqli belgilar
LENS = "M10.5 3a7.5 7.5 0 1 0 4.55 13.46l4.75 4.74 1.41-1.41-4.74-4.75A7.5 7.5 0 0 0 10.5 3zm0 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11zm-3 5.5h2v-3h2v3h2v2h-2v3h-2v-3h-2z"
UNI = "M12 2 1 7.5V10h22V7.5L12 2zm-8 10v7H2v3h20v-3h-2v-7h-3v7h-3v-7h-4v7H7v-7H4z"
PAPKA = "M3 5a2 2 0 0 1 2-2h4.6l2 2H19a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5zm2 4v9h14V9H5z"
KUBOK = "M6 2h12v2h3v3a5 5 0 0 1-4.6 5A6 6 0 0 1 13 15.9V19h4v3H7v-3h4v-3.1A6 6 0 0 1 7.6 12 5 5 0 0 1 3 7V4h3V2zm0 4H5v1a3 3 0 0 0 1.2 2.4A6 6 0 0 1 6 8V6zm12 0v2c0 .5-.1.9-.2 1.4A3 3 0 0 0 19 7V6h-1z"
MAX3D = "M12 1.5 2.5 7v10L12 22.5 21.5 17V7L12 1.5zm0 2.3 7.2 4.2L12 12.2 4.8 8 12 3.8zM4.5 9.7l6.5 3.8v6.6l-6.5-3.8V9.7zm15 0v6.6L13 20.1v-6.6l6.5-3.8z"

DASTUR = [  # (logo, nom, rang, telegram mavzu kaliti)
    ("adobephotoshop", "Photoshop", "#31A8FF", "ps"), ("adobeillustrator", "Illustrator", "#FF9A00", "ai"),
    ("adobeaftereffects", "After Effects", "#9999FF", "ae"), ("adobeindesign", "InDesign", "#FF3366", "id"),
    ("adobepremierepro", "Premiere Pro", "#EA77FF", "pr"), ("coreldraw", "CorelDRAW", "#44D88D", "cdr"),
    ("figma", "Figma", "#F24E1E", "fg"), ("blender", "Blender", "#E87D0D", "bl"), (None, "3ds Max", "#37A5CC", "max"),
]
tools = []
for logo, nom, rang, k in DASTUR:
    href = MAVZU.get(k, GURUH)
    tools.append('<a class="tool" href="%s" style="--b:%s"><i>%s</i>%s</a>' % (href, rang, svg(logo, None if logo else MAX3D), nom))
TOOLS = '<div class="tools">\n' + "\n".join(tools) + "\n</div>"

PROFIL = [  # (href, logo yoki yo'l, rang, matn, i18n kaliti)
    ("ishlar/", ("d", PAPKA), "var(--acc)", None, "idx.nav.works"),
    ("yutuqlar/", ("d", KUBOK), "#F5B400", None, "idx.nav.awards"),
    ("https://orcid.org/0009-0001-7222-3508", "orcid", "#A6CE39", "ORCID", None),
    ("https://scholar.google.com/citations?user=kTUbDqIAAAAJ", "googlescholar", "#4285F4", "Google Scholar", None),
    ("https://www.researchgate.net/profile/Bahtiyor-Hakimov-2", "researchgate", "#00CCBB", "ResearchGate", None),
    ("https://www.lens.org/lens/profile/711013301", ("d", LENS), "#2E8B57", "Lens.org", None),
    ("https://www.adu.uz/oqituvchilar/581", ("d", UNI), "#1F5FA8", None, "idx.nav.adu"),
    ("https://www.linkedin.com/in/bahtiyorjon-hakimov-6489a4337/", "linkedin", "#0A66C2", "LinkedIn", None),
    ("https://github.com/eduhakimov", "github", "var(--fg)", "GitHub", None),
    ("https://www.youtube.com/@Bahtiyor_Studio", "youtube", "#FF0000", "YouTube", None),
    ("https://t.me/GrafikDizayn_Hakimov", "telegram", "#26A5E4", "Telegram", None),
    ("https://t.me/IT_yangi_qadam", "telegram", "#26A5E4", "Telegram", None),
    ("https://discord.gg/vdVWnAvY7k", "discord", "#5865F2", "Discord", None),
    ("mailto:" + POCHTA, "gmail", "#EA4335", "E-mail", None),
]
SUB = {"https://orcid.org/0009-0001-7222-3508": "0009-0001-7222-3508", "https://www.youtube.com/@Bahtiyor_Studio": "@Bahtiyor_Studio",
       "https://t.me/GrafikDizayn_Hakimov": "Grafik dizayn", "https://t.me/IT_yangi_qadam": "IT yangi qadam",
       "https://github.com/eduhakimov": "eduhakimov", "https://www.lens.org/lens/profile/711013301": "Lens ID 711013301",
       "https://scholar.google.com/citations?user=kTUbDqIAAAAJ": "Citations", "https://www.researchgate.net/profile/Bahtiyor-Hakimov-2": "Profile",
       "https://www.linkedin.com/in/bahtiyorjon-hakimov-6489a4337/": "Bahtiyorjon Hakimov",
       "https://discord.gg/vdVWnAvY7k": "bahtiyor_hakimov", "mailto:" + POCHTA: POCHTA}


def profil_html(s):
    out = []
    for href, logo, rang, matn, key in PROFIL:
        ik = svg(d=logo[1]) if isinstance(logo, tuple) else svg(logo)
        if key:
            uz = re.search(r'data-i18n="%s">(.*?)</' % re.escape(key), s).group(1)
            txt = '<b data-i18n="%s">%s</b>' % (key, uz)
        else:
            txt = "<b>%s</b>" % matn
        if href in SUB:
            txt += "<small>%s</small>" % SUB[href]
        big = ' class="big"' if key in ("idx.nav.works", "idx.nav.awards") else ""
        out.append('<a%s href="%s" style="--b:%s"><i>%s</i><span>%s</span></a>' % (big, href, rang, ik, txt))
    return '<nav class="pr">\n' + "\n".join(out) + "\n</nav>"


ALOQA = ('<div class="kont">'
         '<a href="mailto:%s" style="--b:#EA4335"><i>%s</i><span><small data-i18n="idx.kn.mail">Elektron pochta</small><b>%s</b></span></a>'
         '<a href="%s" style="--b:#26A5E4"><i>%s</i><span><small>Telegram</small><b>@GrafikDizayn_Hakimov</b></span></a>'
         '<a href="https://discord.gg/vdVWnAvY7k" style="--b:#5865F2"><i>%s</i><span><small>Discord</small><b>bahtiyor_hakimov</b></span></a>'
         '<a href="https://www.youtube.com/@Bahtiyor_Studio" style="--b:#FF0000"><i>%s</i><span><small>YouTube</small><b>@Bahtiyor_Studio</b></span></a>'
         '</div>') % (POCHTA, svg("gmail"), POCHTA, GURUH, svg("telegram"), svg("discord"), svg("youtube"))

SOC = ('<div class="soc">' + "".join('<a href="%s" aria-label="%s" style="--b:%s">%s</a>' % (h, n, c, svg(i)) for h, n, c, i in [
    ("mailto:" + POCHTA, "E-mail", "#EA4335", "gmail"), (GURUH, "Telegram", "#26A5E4", "telegram"),
    ("https://discord.gg/vdVWnAvY7k", "Discord", "#5865F2", "discord"), ("https://www.youtube.com/@Bahtiyor_Studio", "YouTube", "#FF0000", "youtube"),
    ("https://orcid.org/0009-0001-7222-3508", "ORCID", "#A6CE39", "orcid"), ("https://github.com/eduhakimov", "GitHub", "var(--fg)", "github"),
    ("https://www.linkedin.com/in/bahtiyorjon-hakimov-6489a4337/", "LinkedIn", "#0A66C2", "linkedin")]) + "</div>")

if __name__ == "__main__":
    P = os.path.join(ROOT, "index.html")
    s = io.open(P, encoding="utf-8").read()
    s = re.sub(r'<div class="tools">.*?\n</div>', lambda m: TOOLS, s, count=1, flags=re.S)
    s = re.sub(r'<nav class="pr">.*?\n</nav>', lambda m: profil_html(s), s, count=1, flags=re.S)
    # aloqa bloki CTA ichida
    if 'class="kont"' in s:
        s = re.sub(r'<div class="kont">.*?</div>', lambda m: ALOQA, s, count=1, flags=re.S)
    else:
        s = s.replace('</a></div>\n</section>\n<footer', '</a></div>\n' + ALOQA + '\n</section>\n<footer', 1)
    assert 'class="kont"' in s
    # footer ijtimoiy belgilar
    if 'class="soc"' in s:
        s = re.sub(r'<div class="soc">.*?</div>', lambda m: SOC, s, count=1, flags=re.S)
    else:
        s = s.replace('<footer class="foot">', '<footer class="foot">' + SOC, 1)
    # JSON-LD: pochta
    if '"email"' not in s:
        s = s.replace('"url": "https://eduhakimov.github.io/", "identifier"', '"url": "https://eduhakimov.github.io/", "email": "mailto:%s", "identifier"' % POCHTA, 1)
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
    print("ok")
