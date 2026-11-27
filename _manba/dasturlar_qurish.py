# -*- coding: utf-8 -*-
"""ishlar/ sahifasidagi "Desktop dasturlar" bo'limi va har bir dastur sahifasi (ishlar/d-<slug>.html).

Ma'lumotlar: dasturlar.py (DASTURLAR, KATEGORIYA). ishlar_qurish.py dan chaqiriladi:
    import dasturlar_qurish as DQ
    s += DQ.bolim(L, globals())          # ro'yxat sahifasiga bo'lim
    DQ.sahifalar(OUT, globals())         # har bir dastur sahifasi

ochiq=True: yuklab olish tugmasi, GitHub va hujjatlar havolalari bor.
ochiq=False: faqat tavsif va lavhalar (skrinshotlar); hamkorlik uchun Telegram.
"""
import json
import os

from dasturlar import DASTURLAR, KATEGORIYA

GH = "https://github.com/eduhakimov/"
RAW = "https://raw.githubusercontent.com/eduhakimov/"
LANGS = ("en", "ru", "zh")

# Interfeys yozuvlari (uz, en, ru, zh)
UI = {
    "dst.h2": ("Desktop dasturlar", "Desktop software", "Настольные программы", "桌面软件"),
    "dst.sub": ("Windows 10 va 11 uchun {n} ta dastur. Hammasi internetsiz ishlaydi, o‘zbek, rus va ingliz tillarida, "
                "yorug‘ va qorong‘i mavzuda. Har bir dastur uchun ilmiy maqola, foydalanish qo‘llanmasi va uslubiy "
                "ko‘rsatma tayyorlangan. {o} tasini yuklab olish mumkin, {y} tasining tavsifi va oynalaridan lavhalar "
                "berilgan.",
                "{n} applications for Windows 10 and 11. All of them work offline, in Uzbek, Russian and English, with "
                "light and dark themes. Each comes with a research article, a user guide and teaching guidelines. "
                "{o} can be downloaded; for {y} a description and screenshots are given.",
                "{n} программ для Windows 10 и 11. Все работают без интернета, на узбекском, русском и английском "
                "языках, в светлой и тёмной теме. Для каждой подготовлены научная статья, руководство пользователя и "
                "методические указания. {o} можно скачать, для {y} приведены описание и снимки экрана.",
                "适用于 Windows 10 和 11 的 {n} 款软件。全部可离线运行，支持乌兹别克语、俄语和英语界面以及浅色和深色主题。"
                "每款软件均配有学术论文、用户手册和教学指导。其中 {o} 款可下载，{y} 款提供介绍和界面截图。"),
    "dst.ver": ("Versiya {v}", "Version {v}", "Версия {v}", "版本 {v}"),
    "dst.req": ("Windows 10 (1809+) yoki 11 · internet talab qilinmaydi · o‘zbek, rus, ingliz tillari",
                "Windows 10 (1809+) or 11 · no internet required · Uzbek, Russian, English",
                "Windows 10 (1809+) или 11 · интернет не требуется · узбекский, русский, английский",
                "Windows 10（1809 及以上）或 11 · 无需联网 · 乌兹别克语、俄语、英语"),
    "dst.btn.dl": ("Yuklab olish", "Download", "Скачать", "下载"),
    "dst.btn.gh": ("GitHub sahifasi", "GitHub page", "Страница на GitHub", "GitHub 页面"),
    "dst.h.docs": ("Hujjatlar", "Documentation", "Документация", "文档"),
    "dst.doc.m": ("Ilmiy maqola", "Research article", "Научная статья", "学术论文"),
    "dst.doc.q": ("Foydalanish qo‘llanmasi", "User guide", "Руководство пользователя", "用户手册"),
    "dst.doc.u": ("Uslubiy ko‘rsatma", "Teaching guidelines", "Методические указания", "教学指导"),
    "dst.docs.note": ("Hujjatlar o‘zbek tilida. Word nusxalari dastur arxivida va GitHub sahifasida.",
                      "The documents are in Uzbek. Word versions are included in the program archive and on GitHub.",
                      "Документы на узбекском языке. Версии в формате Word входят в архив программы и есть на GitHub.",
                      "文档为乌兹别克语，Word 版本包含在软件压缩包中，并可在 GitHub 获取。"),
    "dst.h.rasm": ("Dastur oynasidan lavhalar", "Screenshots", "Снимки окна программы", "软件界面截图"),
    "dst.copy": ("© 2026 Bahtiyorjon Hakimov. Barcha huquqlar himoyalangan.",
                 "© 2026 Bahtiyorjon Hakimov. All rights reserved.",
                 "© 2026 Бахтиёржон Хакимов. Все права защищены.",
                 "© 2026 Bahtiyorjon Hakimov。保留所有权利。"),
    "dst.h.tech": ("Texnologiyalar", "Technologies", "Технологии", "技术"),
    "dst.h.kerak": ("Nima uchun kerak", "Why it is needed", "Зачем это нужно", "用途"),
    "dst.b.open": ("Yuklab olish mumkin", "Available for download", "Можно скачать", "可下载"),
    "dst.b.desc": ("Tavsif", "Description only", "Описание", "仅介绍"),
    "dst.box": ("Bu dastur hozircha tavsif sifatida taqdim etilgan: yuklab olish havolasi va hujjatlari ochiq e’lon "
                "qilinmagan. Foydalanish, namoyish yoki hamkorlik uchun <a href=\"{tg}\">Telegram</a> orqali bog‘laning.",
                "This program is presented as a description for now: the download link and documentation are not "
                "published. For use, a demonstration or collaboration, please get in touch via <a href=\"{tg}\">Telegram</a>.",
                "Пока эта программа представлена только описанием: ссылка для скачивания и документация не "
                "опубликованы. Для использования, демонстрации или сотрудничества свяжитесь через "
                "<a href=\"{tg}\">Telegram</a>.",
                "该软件目前仅提供介绍，下载链接和文档暂未公开。如需使用、演示或合作，请通过 <a href=\"{tg}\">Telegram</a> 联系。"),
}

CSS = (".b.d{color:#fff;border-color:transparent}"
       ".bs{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}"
       ".bs>span:not(.b){font:600 11px system-ui,sans-serif;letter-spacing:.03em;padding:3px 9px;border-radius:999px;"
       "border:1px solid var(--line);color:var(--mut)}"
       ".btns{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 6px}"
       ".btn{display:inline-block;padding:9px 16px;border-radius:8px;font:600 14px system-ui,sans-serif;"
       "text-decoration:none;border:1px solid var(--acc)}"
       ".btn.p{background:var(--acc);color:var(--bg)}.btn.s{color:var(--acc);background:var(--card)}"
       ".shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}"
       ".shots img{width:100%;border:1px solid var(--line);border-radius:8px;background:var(--card)}"
       ".cv{font:12px system-ui,sans-serif;color:var(--mut);margin-top:-4px}")


def _ui(key, **kw):
    v = UI[key]
    return v[0].format(**kw), {l: v[i + 1].format(**kw) for i, l in enumerate(LANGS)}


def _el(L, tag, key, attrs=""):
    uz, tr = _ui(key)
    return L.el(tag, key, uz, tr, attrs=attrs)


def _kat_badge(L, d):
    k = KATEGORIYA[d["kat"]]
    return L.el("span", "kat." + d["kat"], k["uz"], {l: k[l] for l in LANGS},
                attrs=' class="b d" style="background:%s"' % k["rang"])


def _open_badge(L, d):
    op = d.get("ochiq", True)
    return _el(L, "span", "dst.b.open" if op else "dst.b.desc", ' class="b %s"' % ("o" if op else "y"))


def bolim(L, g):
    """Ro'yxat sahifasiga qo'shiladigan HTML."""
    n = len(DASTURLAR)
    o = sum(1 for d in DASTURLAR if d.get("ochiq", True))
    h2_uz, h2_tr = _ui("dst.h2")
    sub_uz, sub_tr = _ui("dst.sub", n=n, o=o, y=n - o)
    out = [L.el("h2", "dst.h2", h2_uz, h2_tr, attrs=' id="dasturlar"'),
           L.el("p", "dst.sub", sub_uz, sub_tr, attrs=' class="sub"'),
           "<style>%s</style>" % CSS, '<div class="g">']
    for d in DASTURLAR:
        s = d["slug"]
        ver_uz, ver_tr = _ui("dst.ver", v=d["versiya"])
        out.append('<a class="c" href="d-%s.html">' % g["e"](s)
                   + '<span class="bs" style="margin:0">' + _kat_badge(L, d) + _open_badge(L, d) + "</span>"
                   + L.el("b", "d.%s.nom" % s, d["nom"]["uz"], {l: d["nom"][l] for l in LANGS})
                   + L.el("p", "d.%s.qisqa" % s, d["qisqa"]["uz"], {l: d["qisqa"][l] for l in LANGS})
                   + L.el("span", "d.%s.ver" % s, ver_uz, ver_tr, attrs=' class="cv"')
                   + g["teglar"](d.get("teg", []), L)
                   + '<span class="go" data-i18n="go.more">Batafsil →</span></a>')
    out.append("</div>\n")
    return "".join(out)


def sahifalar(OUT, g):
    """Har bir dastur uchun ishlar/d-<slug>.html. Qaytaradi: yaratilgan sahifalar URL ro'yxati."""
    e, TL = g["e"], g["TL"]
    assert tuple(TL) == LANGS, TL
    urls = []
    for d in DASTURLAR:
        s = d["slug"]
        op = d.get("ochiq", True)
        L = g["Lugat"]()
        url = g["BASE"] + "d-%s.html" % s
        repo = GH + s
        ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": d["nom"]["uz"],
              "description": d["qisqa"]["uz"], "url": url, "operatingSystem": "Windows 10, Windows 11",
              "applicationCategory": "DesktopApplication", "softwareVersion": d["versiya"],
              "inLanguage": ["uz", "ru", "en"],
              "author": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/"}}
        if op:
            ld["downloadUrl"] = repo + "/releases/latest"
        html = g["bosh"](L, "p.title", d["nom"]["uz"] + " – Hakimov B.M.",
                         {l: d["nom"][l] + " – Hakimov B.M." for l in LANGS},
                         "p.desc", d["qisqa"]["uz"], {l: d["qisqa"][l] for l in LANGS}, url,
                         '<script type="application/ld+json">%s</script>\n<style>%s</style>\n'
                         % (json.dumps(ld, ensure_ascii=False), CSS))
        nav = '<nav><a href="./#dasturlar" data-i18n="nav.works_back">← Barcha ishlar</a>' \
              '<a href="../" data-i18n="nav.sci_plain">Ilmiy ishlar</a>'
        if op:
            nav += '<a href="%s">GitHub</a>' % e(repo)
        html += nav + '<a href="%s">Telegram</a></nav>\n' % g["TG"]
        ver_uz, ver_tr = _ui("dst.ver", v=d["versiya"])
        html += ('<div class="bs">' + _kat_badge(L, d) + _open_badge(L, d)
                 + L.el("span", "d.ver", ver_uz, ver_tr) + "<span>Windows 10 · 11</span><span>UZ · RU · EN</span>"
                 + "</div>")
        html += (L.el("h1", "p.nom", d["nom"]["uz"], {l: d["nom"][l] for l in LANGS})
                 + L.el("p", "p.qisqa", d["qisqa"]["uz"], {l: d["qisqa"][l] for l in LANGS}, attrs=' class="sub"'))
        if op:
            html += ('<div class="btns">'
                     + _el(L, "a", "dst.btn.dl", ' class="btn p" href="%s/releases/latest"' % e(repo))
                     + _el(L, "a", "dst.btn.gh", ' class="btn s" href="%s"' % e(repo)) + "</div>")
        html += _el(L, "p", "dst.req", ' class="t"') + "\n"
        html += (L.el("h2", "p.h.nima", "Bu nima", g["S"]("p.h.nima"))
                 + L.el("p", "p.nima", d["nima"]["uz"], {l: d["nima"][l] for l in LANGS}) + "\n")
        if d.get("kerak"):
            html += (_el(L, "h2", "dst.h.kerak")
                     + L.el("p", "d.kerak", d["kerak"]["uz"], {l: d["kerak"][l] for l in LANGS}) + "\n")
        html += (L.el("h2", "p.h.imkon", "Imkoniyatlari", g["S"]("p.h.imkon")) + "<ul>"
                 + "".join(L.el("li", "p.imkon.%d" % k, x["uz"], {l: x[l] for l in LANGS})
                           for k, x in enumerate(d["imkon"])) + "</ul>\n")
        if d.get("tushuncha"):
            html += (L.el("h2", "p.h.tush", "Asosiy tushunchalar", g["S"]("p.h.tush")) + "<dl>"
                     + "".join(L.el("dt", "p.t.%d.a" % k, a["uz"], {l: a[l] for l in LANGS})
                               + L.el("dd", "p.t.%d.b" % k, b["uz"], {l: b[l] for l in LANGS})
                               for k, (a, b) in enumerate(d["tushuncha"])) + "</dl>\n")
        if d.get("rasmlar"):
            html += (_el(L, "h2", "dst.h.rasm") + '<div class="shots">'
                     + "".join('<a href="%s"><img loading="lazy" src="%s" alt="%s"></a>'
                               % (e(RAW + s + "/main/" + r), e(RAW + s + "/main/" + r), e(d["nom"]["uz"]))
                               for r in d["rasmlar"]) + "</div>\n")
        if op:
            docs = GH + s + "/blob/main/docs/materiallar/"
            html += (_el(L, "h2", "dst.h.docs") + "<ul>"
                     + "<li>" + _el(L, "a", "dst.doc.m", ' href="%sILMIY-MAQOLA.md"' % e(docs)) + "</li>"
                     + "<li>" + _el(L, "a", "dst.doc.q", ' href="%sFOYDALANISH-QOLLANMASI.md"' % e(docs)) + "</li>"
                     + "<li>" + _el(L, "a", "dst.doc.u", ' href="%sUSLUBIY-KORSATMA.md"' % e(docs)) + "</li>"
                     + "</ul>" + _el(L, "p", "dst.docs.note", ' class="t"') + "\n")
        else:
            box_uz, box_tr = _ui("dst.box", tg=g["TG"])
            html += L.el("div", "dst.box", box_uz, box_tr, attrs=' class="box"', raw=True) + "\n"
        if d.get("teg"):
            html += _el(L, "h2", "dst.h.tech") + g["teglar"](d["teg"], L) + "\n"
        html += g["foot"](L)
        with open(os.path.join(OUT, "d-%s.html" % s), "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(url)
    return urls
