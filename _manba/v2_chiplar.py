# -*- coding: utf-8 -*-
"""Rasm atrofidagi dastur belgilari: doira bo'ylab teng burchaklarda joylashadi.
Ro'yxatni o'zgartirib qayta ishga tushiring: python _manba/v2_chiplar.py"""
import io, math, os, re, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = importlib.util.spec_from_file_location("ik", os.path.join(ROOT, "_manba", "v2_ikonlar.py"))
ik = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ik)

CHIP = [  # (logo, nom, rang) — soat strelkasi bo'yicha, tepadan boshlab
    ("adobeillustrator", "Illustrator", "#FF9A00"),
    ("adobephotoshop", "Photoshop", "#31A8FF"),
    ("claude", "Claude", "#D97757"),
    ("adobeaftereffects", "After Effects", "#9999FF"),
    ("microsoftword", "Word", "#2B579A"),
    ("googlegemini", "Gemini", "#8E75B2"),
    ("figma", "Figma", "#F24E1E"),
]
R = 50  # doira radiusi (% hisobida, rasm halqasi chizig'i)
html, css = [], []
n = len(CHIP)
for i, (logo, nom, rang) in enumerate(CHIP):
    a = -90 + (i + 0.5) * 360 / n  # tepada belgi bo'lmasin (yuqori panel bilan to'qnashmaydi)
    x = 50 + R * math.cos(math.radians(a)); y = 50 + R * math.sin(math.radians(a))
    html.append('<span class="chip ch%d" title="%s"><i style="--b:%s">%s</i><span class="cn">%s</span></span>' % (i + 1, nom, rang, ik.svg(logo), nom))
    css.append(".chip.ch%d{left:%.1f%%;top:%.1f%%;animation-delay:%.1fs}" % (i + 1, x, y, -i * 6.0 / n))

if __name__ == "__main__":
    P = os.path.join(ROOT, "index.html")
    s = io.open(P, encoding="utf-8").read()
    s = re.sub(r'(<img src="photo\.jpg"[^>]*>)\s*(<span class="chip.*?</span>)(?=</div>)', lambda m: m.group(1) + "\n" + "".join(html), s, count=1, flags=re.S)
    assert 'class="chip ch1"' in s
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
    C = os.path.join(ROOT, "dizayn.css")
    c = io.open(C, encoding="utf-8").read()
    c = re.sub(r"\n/\* rasm atrofidagi .*$", "", c, flags=re.S)
    c += ("\n/* rasm atrofidagi belgilar: doira bo'ylab teng burchaklarda (_manba/v2_chiplar.py yozadi) */\n"
          ".chip{transform:translate(-50%,-50%);white-space:nowrap;animation:suz 6s ease-in-out infinite;padding:9px;border-radius:50%}\n"
          ".chip i{width:28px;height:28px}.chip i svg{width:26px;height:26px}\n"
          ".chip .cn{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}\n"
          ".chip:hover{z-index:5}.chip:hover .cn{width:auto;height:auto;clip:auto;left:50%;top:calc(100% + 6px);transform:translateX(-50%);padding:4px 8px;border-radius:8px;background:var(--card);border:1px solid var(--line2);font:600 11px/1 var(--fb)}\n"
          "@media (max-width:760px){.chip{padding:7px}.chip i{width:22px;height:22px}.chip i svg{width:20px;height:20px}}\n"
          + "\n".join(css) + "\n")
    io.open(C, "w", encoding="utf-8", newline="\n").write(c)
    print("ok", n)
