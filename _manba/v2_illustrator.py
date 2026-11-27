# -*- coding: utf-8 -*-
"""Bosh sahifa: Adobe Illustrator ga alohida urg'u.
- rasm atrofidagi belgilar: Illustrator asosiy (katta), Photoshop, Figma, After Effects;
- "Ishlaydigan dasturlarim" bo'limi boshida Illustrator paneli: ishlar, galereya va Illustrator darslari.
Qayta ishga tushirsa xavfsiz (belgilar orasidagi qism almashtiriladi)."""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_manba"))
import importlib.util
_sp = importlib.util.spec_from_file_location("ik", os.path.join(ROOT, "_manba", "v2_ikonlar.py"))
ik = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ik)

G = "https://eduhakimov.github.io/grafika/"
DARS = [  # (yo'l, i18n kalit, o'zbekcha nom)
    ("1_Maruza_darslari/08_Adobe_Illustrator_dasturiga_kirish_va_uning_interfeysi.html", "l1", "8-ma'ruza. Adobe Illustrator dasturiga kirish va uning interfeysi"),
    ("1_Maruza_darslari/09_Adobe_Illustrator_dasturida_qurilmalar_qatori_hamda_ular_bil.html", "l2", "9-ma'ruza. Adobe Illustrator dasturida qurilmalar qatori hamda ular bilan ishlash"),
    ("1_Maruza_darslari/10_Adobe_Illustrator_dasturida_Brand_Book_hamda_eksport_turlari.html", "l3", "10-ma'ruza. Adobe Illustrator dasturida Brand Book hamda eksport turlari"),
    ("2_Amaliy_mashgulotlar/04_Adobe_Illustrator_interfeysi_va_ishchi_maydonni_sozlash.html", "l4", "4-amaliy. Adobe Illustrator dasturiga kirish. Interfeys va ishchi maydonni sozlash"),
    ("2_Amaliy_mashgulotlar/05_Adobe_Illustrator_instrumentlari_va_geometrik_shakllar_bilan.html", "l5", "5-amaliy. Illustrator instrumentlar paneli va geometrik shakllar bilan ishlashning murakkab usullari"),
    ("2_Amaliy_mashgulotlar/06_Adobe_Illustratorda_vektorli_illyustratsiya_va_ikonalar_topl.html", "l6", "6-amaliy. Adobe Illustrator yordamida vektorli illyustratsiya va ikonalar to'plamini yaratish"),
    ("2_Amaliy_mashgulotlar/07_Brend_buk_elementlarini_yaratish_va_fayllarni_eksport_qilish.html", "l7", "7-amaliy. Adobe Illustratorda Brand Book elementlari, vizual identifikatsiya va eksport formatlari (AI, EPS, SVG)"),
]
OQ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'
AI = ik.svg("adobeillustrator")

items = "".join('<li><a href="%s%s"><span class="n">%02d</span><span data-i18n="idx.ai.%s">%s</span></a></li>' % (G, p, i + 1, k, t)
                for i, (p, k, t) in enumerate(DARS))
PANEL = ('<!--AI_BOSHI--><div class="aip">'
         '<div class="aip-l"><div class="aip-logo">' + AI + '</div>'
         '<span class="kick" data-i18n="idx.ai.kick">Asosiy vositam</span>'
         '<h3>Adobe Illustrator</h3>'
         '<p data-i18n="idx.ai.d">Ishlarimning asosiy qismini Illustrator\'da yarataman: logotip, brend-buk, poster, ikonka to\'plamlari va vektor illyustratsiyalar. Talabalarga ham aynan shu dasturni chuqur o\'rgataman.</p>'
         '<div class="btns"><a class="btn btn-ai" href="https://t.me/GrafikDizayn_Hakimov/13"><span data-i18n="idx.ai.b1">Illustrator ishlarim</span>' + OQ + '</a>'
         '<a class="btn btn-g" href="galereya/"><span data-i18n="idx.ai.b2">Dizayn galereyasi</span>' + OQ + '</a></div></div>'
         '<div class="aip-r"><b data-i18n="idx.ai.les">Illustrator darslari · Kompyuter grafikasi</b><ol>' + items + '</ol></div>'
         '</div><!--AI_OXIRI-->')

CHIPS = ('<span class="chip c1 chip-ai"><i style="--b:#FF9A00">' + AI + '</i>Illustrator</span>'
         '<span class="chip c2"><i style="--b:#31A8FF">' + ik.svg("adobephotoshop") + '</i>Photoshop</span>'
         '<span class="chip c3"><i style="--b:#F24E1E">' + ik.svg("figma") + '</i>Figma · UI/UX</span>'
         '<span class="chip c4"><i style="--b:#9999FF">' + ik.svg("adobeaftereffects") + '</i>After Effects</span>')

if __name__ == "__main__":
    P = os.path.join(ROOT, "index.html")
    s = io.open(P, encoding="utf-8").read()
    # rasm atrofidagi belgilar
    s = re.sub(r'(<img src="photo\.jpg"[^>]*>)\s*(<span class="chip.*?</span>)(?=</div>)', lambda m: m.group(1) + "\n" + CHIPS, s, count=1, flags=re.S)
    assert "chip-ai" in s
    # Illustrator paneli asboblar bo'limida, sarlavhadan keyin
    if "<!--AI_BOSHI-->" in s:
        s = re.sub(r"<!--AI_BOSHI-->.*?<!--AI_OXIRI-->", lambda m: PANEL, s, count=1, flags=re.S)
    else:
        s = s.replace('<div class="tools">', PANEL + '\n<div class="tools">', 1)
    # asboblar ro'yxatida Illustrator plitkasini ajratib ko'rsatish
    s = s.replace('<a class="tool" href="https://t.me/GrafikDizayn_Hakimov/13"', '<a class="tool tool-main" href="https://t.me/GrafikDizayn_Hakimov/13"', 1)
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
    print("ok")
