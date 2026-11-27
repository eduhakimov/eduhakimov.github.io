# -*- coding: utf-8 -*-
"""Lingvix ochiq nusxasini tayyorlaydi (to'liq versiya, mazmuni o'zgarmaydi).

Muallif qarori (2026-11-28): hamma materiallar, jumladan kitob mashqlari, ta'lim maqsadida,
bepul va notijorat ochiq qo'yiladi; foydalanilgan kitoblar va nashriyotlar "Manbalar" bo'limida
ko'rsatiladi.

Qo'shiladi: mualliflik meta teglari, har sahifada (c) yozuvi va bosh saytga havola, himoya skripti,
"O'rganish > Platforma" bo'limida "Manbalar" bandi, LICENSE.txt.

Ishga tushirish (repo ildizidan):
    python -X utf8 _manba/lingvix_tozalash.py <asl_lingvix.html>
Natija: lingvix/index.html va lingvix/LICENSE.txt  (lingvix/sw.js alohida fayl, qo'lda yoziladi)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilovalar_qurish import himoyala, litsenziya, FONTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://eduhakimov.github.io/lingvix/"
NOM = "Lingvix"

MANBALAR = [
    "Destination A1+, B1, B2 (Malcolm Mann, Steve Taylore-Knowles; Macmillan Education)",
    "Test Your Vocabulary 1-3 (Peter Watcyn-Jones; Penguin / Pearson Longman)",
    "Enterprise Grammar 1-4 (Virginia Evans, Jenny Dooley; Express Publishing)",
    "4000 Essential English Words (Paul Nation; Compass Publishing)",
    "IELTS vocabulary and reading vocabulary books",
    "Test Master Book 1-4 test collections",
]

MANBA_UZ = ("Lingvix bepul va notijorat o'quv platformasi. Mashqlar quyidagi kitoblar asosida tuzilgan, "
            "ularning mualliflik huquqi muallif va nashriyotlarga tegishli:\\n• " + "\\n• ".join(MANBALAR) +
            "\\nUstoz ro'yxatlari, o'zbekcha tarjimalar, lug'at, transkripsiya va platforma kodi: "
            "© 2026 Hakimov B.M.")
MANBA_EN = ("Lingvix is a free, non-commercial learning platform. Exercises are based on these books; "
            "their copyright belongs to the authors and publishers: " + "; ".join(MANBALAR) +
            ". Teacher lists, Uzbek translations, dictionary, IPA and platform code: (c) 2026 Hakimov B.M.")


def almashtir(s, eski, yangi):
    if s.count(eski) != 1:
        raise SystemExit(f"topilmadi yoki bir nechta: {eski[:60]!r} ({s.count(eski)})")
    return s.replace(eski, yangi)


def qoshimchalar(s):
    # "O'rganish > Platforma" ro'yxati oxiriga "Manbalar" bandi
    i = s.find("const GUIDE = [")
    j = s.find("\n];", i)
    if i < 0 or j < 0:
        raise SystemExit("GUIDE topilmadi")
    band = ('\n  {t:{uz:"Manbalar",ru:"Источники",en:"Sources"}, p:{uz:"%s",en:"%s"}},' % (MANBA_UZ, MANBA_EN))
    return s[:j] + band + s[j:]


def main():
    manba = sys.argv[1]
    with open(manba, encoding="utf-8") as f:
        s = f.read()
    s = himoyala(qoshimchalar(s), NOM, URL)
    with open(os.path.join(ROOT, "lingvix", "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    uchinchi = ["Exercise content based on: " + "; ".join(MANBALAR) +
                " - copyright of their respective authors and publishers; used for free, non-commercial education.",
                FONTS]
    with open(os.path.join(ROOT, "lingvix", "LICENSE.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(litsenziya(NOM, URL, uchinchi))
    print("tayyor:", len(s), "bayt")


if __name__ == "__main__":
    main()
