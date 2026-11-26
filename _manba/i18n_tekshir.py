# -*- coding: utf-8 -*-
"""Til lug'atlarini tekshiradi (repo ildizidan):  python _manba/i18n_tekshir.py

1) har bir sahifadagi data-i18n / data-i18n-attr kaliti 4 ta lug'atning (uz, en, ru, zh) hammasida bormi;
2) testlar/ ilovasidagi T('...') kalitlari ham 4 tilda bormi;
3) JS fayllar va ichki skriptlarda qavslar muvozanati (satr, izoh va regex hisobga olinadi);
4) lug'atlardagi JSON to'g'ri o'qiladimi.
Muammo bo'lsa 1 kodi bilan chiqadi."""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["uz", "en", "ru", "zh"]
PUSH_RE = re.compile(r"\(window\.I18N_D=window\.I18N_D\|\|\[\]\)\.push\((\{.*?\})\);", re.S)
xatolar = []


def oqi(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


def qavs_tekshir(nom, src):
    """Satr/izoh/regex'ni chetlab, (), [], {} muvozanatini tekshiradi."""
    juft = {")": "(", "]": "[", "}": "{"}
    stek, i, n, oldingi = [], 0, len(src), ""
    while i < n:
        c = src[i]
        if c in "'\"`":
            q, i = c, i + 1
            while i < n and src[i] != q:
                if src[i] == "\\":
                    i += 1
                elif src[i] == "\n" and q != "`":
                    xatolar.append(f"{nom}: yopilmagan satr ({i})")
                    return
                i += 1
            oldingi = "a"
        elif src.startswith("//", i):
            i = src.find("\n", i)
            i = n if i < 0 else i
            continue
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j < 0:
                xatolar.append(f"{nom}: yopilmagan izoh")
                return
            i = j + 1
        elif c == "/" and (oldingi == "" or oldingi in "(,=:[!&|?{};+-*%<>~^" or src[max(0, i - 7):i].rstrip().endswith("return")):
            i += 1
            sinf = False
            while i < n and (src[i] != "/" or sinf):
                if src[i] == "\\":
                    i += 1
                elif src[i] == "[":
                    sinf = True
                elif src[i] == "]":
                    sinf = False
                elif src[i] == "\n":
                    xatolar.append(f"{nom}: yopilmagan regex ({i})")
                    return
                i += 1
            oldingi = "a"
        elif c in "([{":
            stek.append((c, i))
            oldingi = c
        elif c in ")]}":
            if not stek or stek[-1][0] != juft[c]:
                xatolar.append(f"{nom}: kutilmagan '{c}' ({i}): ...{src[max(0, i - 60):i + 1]}")
                return
            stek.pop()
            oldingi = c
        elif not c.isspace():
            oldingi = c if c in "(,=:[!&|?{};+-*%<>~^" else "a"
        i += 1
    if stek:
        xatolar.append(f"{nom}: yopilmagan '{stek[-1][0]}' ({stek[-1][1]})")


def main():
    # umumiy lug'at
    eng = oqi("i18n.js")
    m = re.search(r"/\*COMMON\*/(.*?)/\*/COMMON\*/", eng, re.S)
    common = json.loads(m.group(1))
    qavs_tekshir("i18n.js", eng)
    for l in LANGS:
        if set(common.get(l, {})) != set(common["uz"]):
            xatolar.append(f"i18n.js COMMON: {l} kalitlari uz bilan mos emas")

    sahifalar = ["index.html", "galereya/index.html", "testlar/index.html", "yutuqlar/index.html"] + \
        sorted(p.replace("\\", "/") for p in glob.glob(os.path.join(ROOT, "ishlar", "*.html")))
    sahifalar = [os.path.relpath(p, ROOT).replace("\\", "/") if os.path.isabs(p) else p for p in sahifalar]
    jami_kalit = 0
    for sp in sahifalar:
        src = oqi(sp)
        d = {l: dict(common.get(l, {})) for l in LANGS}
        manbalar = []
        for js in re.findall(r'<script src="([^"]*i18n/[^"]+\.js)"', src):
            yol = os.path.normpath(os.path.join(os.path.dirname(sp), js)).replace("\\", "/")
            jsrc = oqi(yol)
            qavs_tekshir(yol, jsrc)
            manbalar += PUSH_RE.findall(jsrc)
        manbalar += PUSH_RE.findall(src)
        if 'src="i18n.js"' not in src and 'src="../i18n.js"' not in src:
            xatolar.append(f"{sp}: i18n.js ulanmagan")
        for blob in manbalar:
            try:
                o = json.loads(blob)
            except ValueError as ex:
                xatolar.append(f"{sp}: lug'at JSON xato: {ex}")
                continue
            for l in LANGS:
                d[l].update(o.get(l, {}))
        kalitlar = set(re.findall(r'\sdata-i18n="([^"]+)"', src))
        for spec in re.findall(r'\sdata-i18n-attr="([^"]+)"', src):
            for pair in spec.split(";"):
                kalitlar.add(pair.partition(":")[2].strip())
        if sp == "testlar/index.html":
            b0 = src.rindex("<script>") + len("<script>")
            app = src[b0:src.index("</script>", b0)]
            qavs_tekshir(sp + " (ilova)", app)
            kalitlar |= set(re.findall(r"'(js\.[a-z_0-9]+)'", app)) - {"js.g"}
            kalitlar |= {"js.g%d" % g for g in (2, 3, 4, 5)}
            for sid in re.findall(r'\{"id":"([a-z]+)","tag"', src):
                kalitlar |= {f"subj.{sid}.{f}" for f in ("tag", "title", "desc")}
            kalitlar = {k if k.startswith(("tst.", "nav.", "sw.")) or k in common["uz"] else "tst." + k for k in kalitlar}
        for k in sorted(kalitlar):
            for l in LANGS:
                if d[l].get(k) is None:
                    xatolar.append(f"{sp}: '{k}' kaliti {l} lug'atida yo'q")
        jami_kalit += len(kalitlar)
        print(f"{sp}: {len(kalitlar)} ta kalit, 4 tilda tekshirildi")
    print(f"Jami: {len(sahifalar)} ta sahifa, {jami_kalit} ta kalit.")
    if xatolar:
        print("\nMUAMMOLAR:")
        for x in xatolar:
            print(" -", x)
        sys.exit(1)
    print("OK: barcha kalitlar 4 ta lug'atda bor, qavslar muvozanatda.")


if __name__ == "__main__":
    main()
