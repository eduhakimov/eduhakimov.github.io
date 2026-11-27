# -*- coding: utf-8 -*-
"""Til lug'atlarini yig'adi (repo ildizidan ishga tushiring):

    python _manba/i18n_qurish.py

- i18n.js ichidagi /*COMMON*/ ... /*/COMMON*/ blokini yangilaydi (tarjima_*.COMMON);
- i18n/index.js, i18n/galereya.js, i18n/testlar.js lug'atlarini yozadi.
O'zbekcha qiymatlar sahifa HTML'ining o'zidan olinadi (JS chiqaradigan matnlar tarjima_uz.py'da),
en/ru/zh - tarjima_en.py, tarjima_ru.py, tarjima_zh.py dan.
ishlar/ va yutuqlar/ lug'atlari ishlar_qurish.py tomonidan sahifaning o'ziga yoziladi.
"""
import html, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tarjima_uz, tarjima_en, tarjima_ru, tarjima_zh  # noqa: E402

TR = {"en": tarjima_en, "ru": tarjima_ru, "zh": tarjima_zh}
LANGS = ["uz", "en", "ru", "zh"]

# sahifa -> (HTML fayl, kalit prefiksi, tarjima modulidagi lug'at nomi, chiqish fayli)
SAHIFALAR = [
    ("index.html", "idx.", "INDEX", "i18n/index.js"),
    ("galereya/index.html", "gal.", "GALEREYA", "i18n/galereya.js"),
    ("testlar/index.html", "tst.", "TESTLAR", "i18n/testlar.js"),
    ("ilmiy-ishlar/index.html", "ilm.", "ILMIY", "i18n/ilmiy.js"),
]

TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>")
ATTR_RE = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"')


def js_push(d):
    body = json.dumps(d, ensure_ascii=False, indent=0, sort_keys=True).replace("</", "<\\/")
    return ("/* Avtomatik yaratilgan: _manba/i18n_qurish.py. Qo'lda tahrirlamang. */\n"
            "(window.I18N_D=window.I18N_D||[]).push(" + body + ");\n")


def ochilgan_teglar(src):
    """HTML'dagi data-i18n / data-i18n-attr kalitlari va o'zbekcha qiymatlari."""
    matn, attr = {}, {}
    for m in TAG_RE.finditer(src):
        tag, attrs = m.group(1).lower(), dict(ATTR_RE.findall(m.group(2)))
        if "data-i18n" in attrs:
            key = attrs["data-i18n"]
            end = src.find("</" + tag + ">", m.end())
            assert end > 0, key
            inner = src[m.end():end]
            assert ("<" + tag + " ") not in inner and ("<" + tag + ">") not in inner, "ichma-ich teg: " + key
            matn.setdefault(key, []).append(inner)
        if "data-i18n-attr" in attrs:
            for pair in attrs["data-i18n-attr"].split(";"):
                name, _, key = pair.partition(":")
                name, key = name.strip(), key.strip()
                attr.setdefault(key, []).append(html.unescape(attrs.get(name, "")))
    return matn, attr


def main():
    # 1) i18n.js: COMMON
    common = {"uz": tarjima_uz.COMMON}
    for l in TR:
        common[l] = TR[l].COMMON
    for l in LANGS:
        assert set(common[l]) == set(common["uz"]), ("COMMON kalitlari", l)
    p = os.path.join(ROOT, "i18n.js")
    s = io.open(p, encoding="utf-8").read()
    blob = json.dumps(common, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    s2, n = re.subn(r"/\*COMMON\*/.*?/\*/COMMON\*/", lambda m: "/*COMMON*/" + blob + "/*/COMMON*/", s, flags=re.S)
    assert n == 1
    io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
    print("i18n.js: COMMON", len(common["uz"]), "ta kalit")

    # 2) sahifa lug'atlari
    os.makedirs(os.path.join(ROOT, "i18n"), exist_ok=True)
    for fayl, pre, nom, chiq in SAHIFALAR:
        src = io.open(os.path.join(ROOT, fayl), encoding="utf-8").read()
        matn, attr = ochilgan_teglar(src)
        d = {l: {} for l in LANGS}
        uz_js = getattr(tarjima_uz, nom + "_JS", {})
        kalitlar = set()
        for key, vals in list(matn.items()) + list(attr.items()):
            if key in tarjima_uz.COMMON:
                continue  # umumiy lug'atda bor
            assert key.startswith(pre), (fayl, key)
            assert len(set(vals)) == 1, ("bitta kalit - har xil matn", key)
            d["uz"][key] = vals[0]
            kalitlar.add(key[len(pre):])
        for k, v in uz_js.items():
            d["uz"][pre + k] = v
            kalitlar.add(k)
        for l, mod in TR.items():
            lug = getattr(mod, nom)
            for k in kalitlar:
                assert k in lug, (l, nom, k)
                d[l][pre + k] = lug[k]
            ortiqcha = set(lug) - kalitlar
            assert not ortiqcha, (l, nom, "ishlatilmagan kalitlar", sorted(ortiqcha))
        io.open(os.path.join(ROOT, chiq), "w", encoding="utf-8", newline="\n").write(js_push(d))
        print(chiq + ":", len(kalitlar), "ta kalit")


if __name__ == "__main__":
    main()
