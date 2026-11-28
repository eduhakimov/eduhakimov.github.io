# -*- coding: utf-8 -*-
"""Dizayn variantlari (rang mavzulari) va tor ekran menyusi.
- dizayn.css dagi qattiq yozilgan olovrang qiymatlarni o'zgaruvchilarga (--acc, --acc2, --acct) o'tkazadi;
- har bir variant uchun yorug'/qorong'i rejimdagi ranglarni yozadi: <html data-rang="...">;
- SVG strelkalar (data-URI) har bir variant rangida qayta yoziladi.
Qayta ishga tushirsa xavfsiz (variantlar bloki belgilar orasida almashtiriladi)."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, "dizayn.css")
s = io.open(C, encoding="utf-8").read()
s = re.sub(r"\n/\* ===RANGLAR=== \*/.*?/\* ===RANGLAR_OXIRI=== \*/\n", "\n", s, flags=re.S)

# 1) :root ta'riflaridan tashqaridagi qattiq olovrang qiymatlar -> o'zgaruvchilar
qatorlar = s.split("\n")
for n, q in enumerate(qatorlar):
    if q.lstrip().startswith("--acc") or q.startswith(":root{") and "--acc" in q:
        continue
    def rgba(m):
        r, g, b, a = m.group(1), m.group(2), m.group(3), float(m.group(4))
        v = {"255,91,31": "--acc", "255,106,43": "--acc", "255,138,61": "--acc2", "255,154,0": "--acc2", "255,178,122": "--acc2"}.get("%s,%s,%s" % (r, g, b))
        if not v:
            return m.group(0)
        return "color-mix(in srgb,var(%s) %d%%,transparent)" % (v, round(a * 100))
    q = re.sub(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\.\d+|0?\.\d+|1)\)", rgba, q)
    for h, v in (("#ff5b1f", "var(--acc)"), ("#ff6a2b", "var(--acc)"), ("#ff8a3d", "var(--acc2)"), ("#ff9a4d", "var(--acc2)"),
                 ("#ff8b3d", "var(--acc2)"), ("#ffad66", "var(--acc2)"), ("#c2410c", "var(--acct)"),
                 ("#ffb27a", "color-mix(in srgb,var(--acc2) 65%,#fff)"), ("#ffd6b3", "color-mix(in srgb,var(--acc2) 35%,#fff)"),
                 ("#ffcf9f", "color-mix(in srgb,var(--acc2) 45%,#fff)"), ("#ffb84d", "color-mix(in srgb,var(--acc2) 65%,#fff)")):
        if "%23" not in q:  # data-URI ichidagi ranglar alohida yoziladi
            q = q.replace(h, v)
    qatorlar[n] = q
s = "\n".join(qatorlar)

# 2) variantlar
V = {  # nom: (yorug': acc, acc2, acct), (qorong'i: acc, acc2, acct)
    "kok": (("#2563eb", "#3b82f6", "#1d4ed8"), ("#3b82f6", "#60a5fa", "#93c5fd")),
    "yashil": (("#059669", "#10b981", "#047857"), ("#10b981", "#34d399", "#6ee7b7")),
    "binafsha": (("#7c3aed", "#8b5cf6", "#6d28d9"), ("#8b5cf6", "#a78bfa", "#c4b5fd")),
    "qizil": (("#dc2626", "#ef4444", "#b91c1c"), ("#ef4444", "#f87171", "#fca5a5")),
    "oltin": (("#d97706", "#f59e0b", "#b45309"), ("#f59e0b", "#fbbf24", "#fcd34d")),
    "pushti": (("#db2777", "#ec4899", "#be185d"), ("#ec4899", "#f472b6", "#f9a8d4")),
}
QORONGI = [':root[data-theme="dark"][data-rang="%s"]', '@media (prefers-color-scheme:dark){:root:not([data-theme="light"])[data-rang="%s"]{%s}}']
ARR = "url(\"data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%%23%s' stroke-width='2.2' stroke-linecap='round'%%3E%%3Cpath d='M7 17 17 7M8 7h9v9'/%%3E%%3C/svg%%3E\")"
CHEV = "url(\"data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%%23%s' stroke-width='2.2' stroke-linecap='round'%%3E%%3Cpath d='m6 9 6 6 6-6'/%%3E%%3C/svg%%3E\")"
out = ["/* ===RANGLAR=== dizayn variantlari: <html data-rang=\"kok|yashil|binafsha|qizil|oltin|pushti\"> (standart: olovrang) */"]
for nom, (yr, qr) in V.items():
    yv = "--acc:%s;--acc2:%s;--acct:%s;--glow:color-mix(in srgb,%s 16%%,transparent)" % (yr[0], yr[1], yr[2], yr[0])
    qv = "--acc:%s;--acc2:%s;--acct:%s;--glow:color-mix(in srgb,%s 26%%,transparent)" % (qr[0], qr[1], qr[2], qr[0])
    out.append(':root[data-rang="%s"]{%s}' % (nom, yv))
    out.append((QORONGI[0] % nom) + "{%s}" % qv)
    out.append(QORONGI[1] % (nom, qv))
    h = qr[0].lstrip("#")
    out.append(':root[data-rang="%s"] .kc::after{background-image:%s}' % (nom, ARR % h))
    out.append(':root[data-rang="%s"] .pub>summary::after{background-image:%s}' % (nom, CHEV % h))
# rang tanlagich va tor ekran menyusi
out.append("""
.rang{position:relative}
.rang-b{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;border:1px solid var(--line2);background:var(--card);color:var(--fg);cursor:pointer;padding:0;transition:.2s}
.rang-b:hover{border-color:var(--acc);color:var(--acc)}.rang-b svg{width:18px;height:18px}
.rang-p{position:absolute;right:0;top:calc(100% + 10px);z-index:60;display:none;grid-template-columns:repeat(4,30px);gap:10px;padding:14px;border-radius:16px;border:1px solid var(--line2);background:var(--card);box-shadow:var(--shadow)}
.rang.ochiq .rang-p{display:grid}
.rang-p button{width:30px;height:30px;border-radius:50%;border:2px solid transparent;cursor:pointer;padding:0;background:var(--c);box-shadow:0 0 0 1px var(--line2)}
.rang-p button[aria-pressed="true"]{border-color:var(--fg)}
.rang-p b{grid-column:1/-1;font:700 11px/1 var(--fb);letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.menu-tg{display:none;place-items:center;width:38px;height:38px;border-radius:50%;border:1px solid var(--line2);background:var(--card);color:var(--fg);cursor:pointer;padding:0}
.menu-tg svg{width:18px;height:18px}
@media (max-width:1080px){
  .menu-tg{display:grid}
  .top .tn{display:none;position:absolute;left:16px;right:16px;top:calc(100% + 8px);flex-direction:column;gap:2px;padding:8px;border-radius:18px;background:var(--card);box-shadow:var(--shadow);z-index:55}
  .top.menu-ochiq .tn{display:flex}
  .top .tn a{padding:12px 14px;font-size:15px;border-radius:12px}
  .top .wrap{position:relative}
}
""")
out.append("/* ===RANGLAR_OXIRI=== */")
s = s.rstrip("\n") + "\n" + "\n".join(out) + "\n"
# eski "@media (max-width:1080px){.tn{display:none}}" qoidasi menyuni butunlay yashirardi
s = s.replace("@media (max-width:1080px){.tn{display:none}}\n", "")
s = s.replace("@media (max-width:1000px){.tn{display:none}", "@media (max-width:1000px){")
io.open(C, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
