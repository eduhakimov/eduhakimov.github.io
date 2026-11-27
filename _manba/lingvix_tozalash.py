# -*- coding: utf-8 -*-
"""Lingvix ochiq nusxasini tayyorlaydi: nashriyot kitoblaridan olingan mashqlarni olib tashlaydi
va mualliflik himoyasini qo'shadi.

Qoladi: "Ustoz ro'yxatlari" (20+ kunlik kurs) va "Vocabulary Lists" (muallif tuzgan so'z ro'yxatlari,
o'zbekcha tarjimalari bilan), shaxsiy lug'at (Lug'atim), talaffuz qo'llanmasi, o'z testlarini qo'shish.
Olib tashlanadi: Destination A1+/B1/B2, Test Your Vocabulary 1-3, Enterprise Grammar 1-4,
4000 Essential English Words, IELTS Vocabulary / IELTS Reading Vocabulary, Speaking Grammar,
Word Formation, Test Master Book 1-4 mashqlari; ularga tayangan "Daraja" (placement) testi.

Ishga tushirish (repo ildizidan):
    python -X utf8 _manba/lingvix_tozalash.py <manba.html>
Natija: lingvix/index.html va lingvix/LICENSE.txt
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilovalar_qurish import himoyala, litsenziya, FONTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://eduhakimov.github.io/lingvix/"
NOM = "Lingvix"
QOLADI = {"Ustoz roʻyxatlari", "Vocabulary Lists"}


def almashtir(s, eski, yangi):
    if s.count(eski) != 1:
        raise SystemExit(f"topilmadi yoki bir nechta: {eski[:60]!r} ({s.count(eski)})")
    return s.replace(eski, yangi)


def tozala(s):
    # 1) savollar bazasi: faqat muallifning o'z bo'limlari qoladi
    m = re.search(r'<script id="testdata" type="application/json">', s)
    st = m.end()
    e = s.find("</script>", st)
    data = json.loads(s[st:e])
    qoldi = [t for t in data if t.get("book") in QOLADI]
    print(f"testlar: {len(data)} -> {len(qoldi)}")
    s = s[:st] + json.dumps(qoldi, ensure_ascii=False, separators=(",", ":")) + s[e:]

    # 2) kitob javonlari (Destination, IELTS, Test Master, TYV, Enterprise) bo'sh
    i = s.find("const SHELVES = [")
    j = s.find("];", i)
    s = s[:i] + "const SHELVES = [" + s[j:]

    # 3) "Daraja" testi butunlay kitoblarga tayangan: menyudan olinadi, eski havolalar bosh sahifaga
    s = almashtir(s, """{id:'placement', icon:'target', label:L({uz:'Daraja',ru:'Уровень',en:'Level'}), action:"openPlacementIntro()"},""", "")
    s = almashtir(s, "function openPlacementIntro(){ stopTimer(); state.screen='placement'; render(); }",
                  "function openPlacementIntro(){ goHome(); }")

    # 4) Listening bo'limi bo'sh (yashirin); begona sayt nomi olib tashlanadi
    s = almashtir(s, '"title":"Practice Listening Tests for B1 · englishpracticetest.net"', '"title":"Listening"')
    return s


def main():
    manba = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "lingvix", "index.html")
    with open(manba, encoding="utf-8") as f:
        s = f.read()
    s = himoyala(tozala(s), NOM, URL)
    with open(os.path.join(ROOT, "lingvix", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    with open(os.path.join(ROOT, "lingvix", "LICENSE.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(litsenziya(NOM, URL, [FONTS]))
    print("tayyor:", len(s), "bayt")


if __name__ == "__main__":
    main()
