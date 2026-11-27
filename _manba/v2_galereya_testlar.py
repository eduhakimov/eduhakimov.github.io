# -*- coding: utf-8 -*-
"""Bir martalik: galereya/ va testlar/ sahifalarini yangi dizaynga (v2) o'tkazadi.
Galereya ../dizayn.css ni ulaydi; testlar o'z klasslari to'qnashmasligi uchun faqat ranglar/shriftlarni oladi."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ishlar_qurish.py import qilinsa butun saytni qayta yozadi, shuning uchun faqat TEMA_HEAD va TOP qismini olamiz
_src = io.open(os.path.join(ROOT, "_manba", "ishlar_qurish.py"), encoding="utf-8").read()
_ns = {}
exec(_src[_src.index("TEMA_HEAD = ("):_src.index("# ---------- tillar (i18n)")], _ns)
TEMA_HEAD, TOP = _ns["TEMA_HEAD"], _ns["TOP"]

ERTA = "<script>try{var t=localStorage.getItem('eduhakimov.theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>\n"
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Unbounded:wght@600;700;800&display=swap">\n')
TUGMA = TOP[TOP.index('<button class="tema"'):TOP.index('</button>') + 9]


def yoz(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)


# ---------- galereya ----------
p = os.path.join(ROOT, "galereya", "index.html")
s = io.open(p, encoding="utf-8").read()
if "dizayn.css" not in s:
    a, b = s.index("<style>"), s.index("</style>") + 8
    css = """<style>
.w{max-width:1180px;margin:0 auto;padding:44px 20px 64px}
h1{margin:0 0 10px;font:800 clamp(30px,4.6vw,52px)/1.02 var(--fd);letter-spacing:-.03em}
.sub{color:var(--mut);margin:0 0 22px;font-size:15.5px;line-height:1.6;max-width:760px}
nav a{display:inline-block;margin:0 8px 8px 0;padding:8px 15px;border:1px solid var(--line2);border-radius:999px;color:var(--fg);text-decoration:none;font:600 13.5px/1.2 var(--fb);background:var(--card);transition:.2s}
nav a:hover{border-color:var(--acc);color:var(--acct)}
h2{margin:48px 0 16px;font:700 clamp(20px,2.4vw,28px)/1.15 var(--fd);letter-spacing:-.02em}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;cursor:zoom-in;box-shadow:var(--shadow);transition:transform .25s,border-color .25s}
figure:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--acc) 55%,var(--line))}
figure img{display:block;width:100%;height:220px;object-fit:cover;object-position:top;-webkit-user-drag:none;user-select:none}
figcaption{padding:12px 14px;font:600 14px/1.4 var(--fb)}figcaption span{display:block;margin-top:3px;color:var(--mut);font-weight:500;font-size:12px}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;padding:16px;z-index:90}
#lb.on{display:flex}#lb img{max-width:100%;max-height:100%;border-radius:10px;-webkit-user-drag:none}
#lb button{position:absolute;top:12px;right:16px;background:none;border:0;color:#fff;font:32px system-ui;cursor:pointer}
footer{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);color:var(--mut);font-size:13px}
@media print{body{display:none}}
</style>"""
    s = s[:a] + TEMA_HEAD + css + s[b:]
    s = s.replace('</head><body><div class="w">\n<div data-i18n-sw></div>', '</head><body>\n' + TOP + '<div class="w">', 1)
    assert TOP in s
    s = s.replace("color:var(--bg);text-decoration:none", "color:#fff;text-decoration:none", 1)
    s = s.replace('<script src="../i18n.js"></script>', '<script src="../i18n.js"></script>\n<script src="../mavzu.js"></script>', 1)
    yoz(p, s)
    print("galereya ok")

# ---------- testlar ----------
p = os.path.join(ROOT, "testlar", "index.html")
s = io.open(p, encoding="utf-8").read()
if "mavzu.js" not in s:
    eski = s[s.index(":root{\n  --bg:#fbfaf7"):s.index("*{box-sizing:border-box}")]
    YORUG = "--bg:#f4f2ee;--fg:#131313;--muted:#5d5a55;--accent:#c2410c;--accent-fg:#fff;--line:rgba(19,19,19,.13);--card:#ffffff;--soft:#ebe8e2;--ok:#1e7a3c;--ok-bg:#e8f5ec;--bad:#b3261e;--bad-bg:#fbeaea;--warn:#b45309;"
    QORONGI = "--bg:#0a0a0c;--fg:#f3f1ed;--muted:#9d998f;--accent:#ff6a2b;--accent-fg:#140a05;--line:rgba(255,255,255,.10);--card:#141418;--soft:#1b1b20;--ok:#6fcf8e;--ok-bg:#16291d;--bad:#f28b82;--bad-bg:#2e1a1a;--warn:#f0b35c;color-scheme:dark;"
    yangi = (":root{" + YORUG + "\n  --serif:\"Unbounded\",\"Manrope\",system-ui,sans-serif;\n"
             "  --ui:\"Manrope\",system-ui,-apple-system,\"Segoe UI\",Roboto,\"PingFang SC\",\"Microsoft YaHei\",Arial,sans-serif;\n"
             "  --mono:ui-monospace,Consolas,\"Courier New\",monospace;\n}\n"
             ":root[data-theme=\"dark\"]{" + QORONGI + "}\n"
             "@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){" + QORONGI + "}}\n"
             "h1,h2,h3{letter-spacing:-.02em}h1{font-weight:800!important}.btn{border-radius:999px!important}"
             ".btn.primary{background:linear-gradient(135deg,#ff5b1f,#ff8b3d)!important;border-color:transparent!important;color:#fff!important}"
             ".tema{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;padding:0}"
             ".tema:hover{border-color:var(--accent);color:var(--accent)}.tema svg{width:18px;height:18px}.tema .ic-sun{display:none}"
             ":root[data-theme=\"dark\"] .tema .ic-sun{display:block}:root[data-theme=\"dark\"] .tema .ic-moon{display:none}"
             "@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]) .tema .ic-sun{display:block}:root:not([data-theme=\"light\"]) .tema .ic-moon{display:none}}\n")
    s = s.replace(eski, yangi, 1)
    s = s.replace("<style>", ERTA + FONT + "<style>", 1)
    s = s.replace('<div data-i18n-sw></div></div>', '<div data-i18n-sw></div>' + TUGMA + '</div>', 1)
    s = s.replace('<script src="../i18n.js"></script>', '<script src="../i18n.js"></script>\n<script src="../mavzu.js"></script>', 1)
    assert TUGMA in s and "mavzu.js" in s
    yoz(p, s)
    print("testlar ok")
