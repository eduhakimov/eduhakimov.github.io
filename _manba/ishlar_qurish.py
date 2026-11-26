# -*- coding: utf-8 -*-
"""eduhakimov.github.io/ishlar/ sahifalarini yasaydi."""
import html, json, os, sys

OUT = sys.argv[1]  # .../eduhakimov.github.io/ishlar
BASE = "https://eduhakimov.github.io/ishlar/"
GH = "https://github.com/eduhakimov/"
MUALLIF = "Hakimov Bahtiyorjon Muzaffar o'g'li"
TG = "https://t.me/IT_yangi_qadam"
e = html.escape

# turi: "ochiq" -> havola, "yopiq" -> alohida sahifa
ISHLAR = [
 # ---------------- Ta'lim platformalari
 dict(bolim="talim", slug="savodxonlik", nom="Kompyuter savodxonligi: 72 interaktiv dars", turi="ochiq",
      havola="https://eduhakimov.github.io/savodxonlik/", repo=GH+"savodxonlik",
      qisqa="9 modul, 72 interaktiv dars: kompyuter qurilmalaridan Excel tahlilida yakuniy loyihagacha. Darslar videosi YouTube'da.",
      teg=["HTML", "JavaScript", "Interaktiv dars"]),
 dict(bolim="talim", slug="kompyuter-servis-laboratoriyasi", nom="Kompyuter servis laboratoriyasi", turi="yopiq",
      qisqa="Kompyuter qurilmalari va ularga xizmat ko'rsatishni o'rgatadigan oflayn o'quv platformasi, 480 dan ortiq qurilmadan iborat 3D atlas bilan.",
      teg=["HTML", "Three.js", "3D", "Oflayn"],
      nima="Bitta HTML fayldan iborat o'quv platformasi: internet va o'rnatish talab qilinmaydi, brauzerda ochiladi. Kompyuter tuzilishi, qismlari, yig'ish va nosozliklarni topishni bosqichma-bosqich o'rgatadi.",
      imkon=["Olti bo'lim bo'yicha darslar, har biri uch darajada: sodda, o'rtacha, mukammal.",
             "3D atlas: 480 dan ortiq qurilma (protsessor, xotira, disk, videokarta, ona plata, quvvat bloki, sovutgich, korpus, tashqi qurilmalar). Modelni aylantirib ko'rish, qismiga bosilganda izohi chiqadi.",
             "Mashqlar: kunlik chaqiriq, o'yinlar, nosozlik topish trenajyori, kompyuter yig'ish stendi.",
             "Atamalar lug'ati va ma'lumotnoma jadvallari."],
      tushuncha=[("Oflayn platforma", "Hamma resurs (shriftlar, rasmlar, 3D modellar) faylning ichiga joylangan, shuning uchun internet bo'lmagan sinfxonada ham ishlaydi."),
                 ("Protsedurali 3D modellar", "Qurilmalar kod yordamida yasalgan: 415 ta model GLB formatida ham chiqarilgan. Firma logotiplari va aniq mahsulot dizayni ko'chirilmagan."),
                 ("Uch darajali ta'lim", "Bitta mavzu boshlovchi, o'rta va ilg'or o'quvchi uchun alohida chuqurlikda yoritiladi.")],
      holat="7.38 versiya. Darslarda ishlatilmoqda.", sabab="o'quv materiali"),
 dict(bolim="talim", slug="grammatika-metro", nom="Grammatika Metro", turi="ochiq",
      havola=GH+"grammatika-metro", repo=GH+"grammatika-metro",
      qisqa="Ingliz tili grammatikasini o'zbek tilida bekatma-bekat o'rgatadigan platforma: 14 yo'nalish, 43 dars, 231 mashq.",
      teg=["HTML", "JavaScript", "Ingliz tili"]),
 dict(bolim="talim", slug="lingvix", nom="Lingvix: test va lug'at platformasi", turi="yopiq",
      qisqa="Ingliz tili bo'yicha talaba, o'qituvchi va admin rollari bor test va lug'at platformasi. Javoblar faqat serverda saqlanadi.",
      teg=["Node.js", "PostgreSQL", "Docker", "Ingliz tili"],
      nima="Guruhlarda ingliz tili o'qitish uchun veb-platforma. Talaba ro'yxatdan o'tadi, o'qituvchi tasdiqlaydi va guruhlarga vazifa beradi. Talabalar tayyorlanish va topshirish rejimlarida ishlaydi, o'qituvchi natijalar va yo'qlamani yuritadi.",
      imkon=["Uch rol: super admin, o'qituvchi, talaba. Ruxsatlar alohida beriladi.",
             "Tayyorlanish va topshirish rejimlari, qulflangan test ekrani.",
             "Guruhlar, vazifalar, natijalar va yo'qlama jurnali.",
             "O'qituvchi bergan so'z ro'yxatlari (inglizcha va o'zbekcha) va Listening kitobi audio bilan.",
             "Oflayn bitta faylli variant (20 kunlik kurs) ham bor."],
      tushuncha=[("Javoblar serverda", "To'g'ri javoblar brauzerga yuborilmaydi: tekshirish serverda bajariladi, shuning uchun talaba javobni kod ichidan topa olmaydi."),
                 ("Umumiy tekshirish moduli", "Javobni baholash kodi brauzer va server uchun bitta, natijalar har ikki tomonda bir xil chiqadi."),
                 ("Konteynerda joylash", "Dockerfile orqali Railway, Render yoki istalgan VPS'ga joylanadi; migratsiya va kontent importi o'zi bajariladi.")],
      holat="Ishlab chiqilmoqda.", sabab="o'quv materiali va test savollari himoyasi"),
 dict(bolim="talim", slug="lingvix-listening", nom="Lingvix Listening", turi="yopiq",
      qisqa="Pre-A1 dan B2 gacha darajalar bo'yicha ingliz tilida tinglab tushunish ilovalari.",
      teg=["HTML", "Audio", "Ingliz tili"],
      nima="Ingliz tilida tinglab tushunishni mashq qilish uchun oflayn ilovalar to'plami. Har bir daraja (Pre-A1, A1, A2, B1, B2) alohida ilova bo'lib, audio va topshiriqlar ichiga joylangan.",
      imkon=["Darajalar bo'yicha alohida ilovalar: Starters, A1, A2, B1, B2.",
             "Audio yozuvlar va ularga bog'langan topshiriqlar bir faylda.",
             "Internetsiz ishlaydi."],
      tushuncha=[("Darajaga moslash", "Topshiriqlar CEFR darajalariga qarab tuzilgan: o'quvchi o'z darajasidan boshlaydi."),
                 ("Katta media bilan oflayn ishlash", "Audio fayllar ilova ichiga joylangan, shuning uchun ilova yuklab olingach internet kerak bo'lmaydi.")],
      holat="Tayyor ilovalar mavjud.", sabab="audio materiallar mualliflik huquqi"),
 dict(bolim="talim", slug="test-master", nom="Test Master", turi="yopiq",
      qisqa="Ingliz tili bo'yicha test topshirish va natijani darhol ko'rish uchun oflayn test platformasi.",
      teg=["HTML", "JavaScript", "Test"],
      nima="Bitta HTML fayldan iborat test platformasi. Turli savol turlari (variant tanlash, matn kiritish, son kiritish) bilan ishlaydi, natijani darhol hisoblaydi.",
      imkon=["Bir nechta savol turi: variantli, yozma javob, son kiritish.",
             "Natijalar va xatolar tahlili darhol chiqadi.",
             "Internetsiz, brauzerning o'zida ishlaydi."],
      tushuncha=[("Avtomatik baholash", "Javob kiritilishi bilan tekshiriladi, xato javob uchun to'g'ri variant ko'rsatiladi."),
                 ("Bitta faylli ilova", "O'rnatish talab qilinmaydi: faylni ochish kifoya.")],
      holat="Darslarda ishlatilgan (avgust versiyasi).", sabab="test savollari himoyasi"),
 dict(bolim="talim", slug="master-vocabulary", nom="Master Vocabulary", turi="ochiq",
      havola=GH+"Master_vocabulary", repo=GH+"Master_vocabulary",
      qisqa="Ingliz tilidagi so'zlarni test shaklida yod olish ilovasi.",
      teg=["TypeScript", "React", "Gemini"]),

 # ---------------- Animatsiya, grafika, 3D
 dict(bolim="grafika", slug="ziyoanim-ik", nom="ZiyoAnim IK: After Effects uchun animatsiya moduli", turi="yopiq",
      qisqa="Adobe After Effects uchun o'zbek tilidagi personaj animatsiyasi moduli: IK, FK, overlap, yuz ifodalari, yurish generatori va bake bitta panelda.",
      teg=["ExtendScript", "After Effects", "Animatsiya", "IK"],
      nima="Magistrlik tadqiqotim doirasida yaratilgan modul. 2D personajni Illustrator'dan import qilishdan tortib tayyor videoga chiqarishgacha bo'lgan ishni bitta paneldan bajaradi. Personajni sichqoncha bilan pozalash, yurish sikli va ustma-ust harakatni avtomatik yaratish mumkin.",
      imkon=["Rig: qatlamlarni nomidan aniqlash, bo'g'in nuqtalarini tuzatish, bir tugma bilan riglash.",
             "Animatsiya: sichqonchada pozalash, pozalar orasida o'tish, videoga chiqarish.",
             "IK: sakrashsiz IK va FK almashinuvi, cho'zilish, rubber-hose qo'llar.",
             "Harakat: yurish sikli, silliq to'xtash, salom, tayyor sahna.",
             "Overlap: ustma-ust harakat va follow-through, umurtqa, dum va soch zanjirlari.",
             "Bake: ifodalarni kalit kadrlarga aylantirish va ortiqcha kalitlarni xato chegarasi bilan qisqartirish.",
             "5 ta o'zimiz chizgan personaj: Aziz, Malika, Bobur ota, Nilufar, Jasur."],
      tushuncha=[("Teskari kinematika (IK)", "Qo'l yoki oyoqning uchini sudrasangiz, yelka va tirsak burchaklari analitik formula bilan o'zi hisoblanadi."),
                 ("Ikkilamchi harakat (overlap)", "Asosiy harakatdan keyin soch, kiyim yoki dum kechikib, so'nib tebranadi. Bu kalit kadrlarga asoslangan model bilan hisoblanadi."),
                 ("Xato chegaralangan bake", "Ifodalar kalit kadrlarga aylantiriladi, so'ng ko'rinishni berilgan xatodan ortiq o'zgartirmaydigan ortiqcha kalitlar olib tashlanadi."),
                 ("Avtomatik sinov", "After Effects 2027 da 419 ta avtomatik tekshiruvdan o'tgan.")],
      holat="2.3 versiya. Ilmiy maqolalarda yoritilgan.", sabab="dissertatsiya ishi, himoyagacha yopiq"),
 dict(bolim="grafika", slug="adu-binolari-3d", nom="ADU binolari: CAD chizmalar va 3D modellar", turi="yopiq",
      qisqa="Andijon davlat universiteti o'quv binolari va turar joylarining tartiblangan chizmalari, CAD fayllari va interaktiv 3D modellari.",
      teg=["Python", "JavaScript", "CAD", "3D"],
      nima="Universitet binolari bo'yicha hujjatlar to'plami: asl chizmalardan CAD fayllar, rangli va rangsiz chizmalar hamda brauzerda aylantirib ko'riladigan 3D modellar yasalgan. Universitetning umumiy gen plani va 3D modeli ham bor.",
      imkon=["O'quv binolari (1800, 1600, 1000, 500, ARM) va talabalar turar joylari.",
             "Har bir bino uchun: asl chizmalar, DXF/PDF/PNG chizmalar, 3D model (HTML, GLB, OBJ), haqiqiy rasmlar.",
             "Topografik va sputnik asosidagi gen plan."],
      tushuncha=[("2D dan 3D ga", "Qavat rejalaridagi devor va xonalar chiziqlaridan avtomatik ravishda hajmli model quriladi."),
                 ("Internetsiz 3D ko'ruvchi", "Har bir bino modeli bitta HTML faylda ochiladi, server talab qilinmaydi.")],
      holat="Ish davom etmoqda.", sabab="universitet binolari chizmalari ochiq tarqatilmaydi"),

 # ---------------- O'yinlar
 dict(bolim="oyin", slug="ovozla", nom="Ovozla!", turi="yopiq",
      qisqa="Do'stlar bilan kulgili dublyaj o'yini: video sahnadagi personajlarni o'z ovozingiz bilan qayta ovozlaysiz va videoga saqlaysiz.",
      teg=["Godot 4", "GDScript", "FFmpeg", "Steam"],
      nima="Bahtiyor Studio nomidan Steam uchun tayyorlanayotgan o'yin. Sahnani tanlaysiz, asl ovozni eshitib, karaoke matn bo'yicha o'z ovozingizni yozasiz, so'ng butun sahnani sizning ovozingiz bilan tomosha qilasiz. Interfeys o'zbek, rus va ingliz tillarida.",
      imkon=["Yozish ekrani: asl ovoz, karaoke matn, to'lqin shakli, 6 ta ovoz effekti.",
             "Tomosha va videoni saqlash: 16:9, 9:16 yoki asl format.",
             "Davra rejimi: bitta kompyuterda 2–12 kishi navbatma-navbat.",
             "Pak ustaxonasi: istalgan videodan sahna yasash, gaplar avtomatik topiladi.",
             "Faqat litsenziyasi aniq sahnalar (Sintel, Elephants Dream, CC BY)."],
      tushuncha=[("Ovozni ajratish", "Videodagi nutq fon musiqasidan neyron tarmoq (Demucs) bilan ajratiladi, gaplar vaqti esa nutqni tanish (Whisper) bilan topiladi."),
                 ("Litsenziya nazorati", "Reliz yig'ilayotganda litsenziyasi aniq bo'lmagan sahna tushib qolsa, yig'ish to'xtaydi.")],
      holat="1.0.0: Steam'ga birinchi nomzod.", sabab="tijorat mahsuloti"),
 dict(bolim="oyin", slug="chip-depo", nom="Chip Depo", turi="yopiq",
      qisqa="Kompyuter qismlari omborida tanib, saralab, joyiga terish o'yini. Birinchi shaxs nomidan, Unity 6 da.",
      teg=["Unity 6", "C#", "3D"],
      nima="O'yinchi kompyuter qismlari omborida ishlaydi: kelgan buyumni tanib oladi, turiga qarab saralaydi va javonga joylaydi. O'yin davomida 745 turdagi kompyuter qismlari bilan tanishiladi.",
      imkon=["745 turdan iborat buyumlar katalogi.",
             "Birinchi shaxs nomidan 3D ombor.",
             "Windows uchun bitta faylli o'rnatuvchi."],
      tushuncha=[("O'yin orqali o'rganish", "Qismlarni tanish va saralash orqali o'yinchi kompyuter apparat ta'minotini yodlab oladi."),
                 ("Ochiq modellar", "3D modellar CC BY 4.0 litsenziyali ochiq manbalardan olingan, mualliflari ko'rsatilgan.")],
      holat="0.3 versiya, ishlab chiqilmoqda.", sabab="ishlab chiqilmoqda"),
 dict(bolim="oyin", slug="kompyuter-ustasi-3d", nom="Kompyuter ustasi 3D", turi="yopiq",
      qisqa="Kompyuter ta'mirlash ustasi rolida 3D simulyator. Brauzerda ishlaydigan demo.",
      teg=["HTML", "WebGL", "3D", "Simulyator"],
      nima="O'yinchi kompyuter ustasi bo'lib, qurilmalarni ochadi, nosozlikni topadi va tuzatadi. Dizayn qurilmalarning o'zidan olingan: tekstolit yashili, oltin kontaktlar, qalay kulrangi.",
      imkon=["3D ish stoli va qurilmalar.",
             "Nosozlikni topish va tuzatish vazifalari.",
             "Brauzerda, o'rnatishsiz ishlaydi."],
      tushuncha=[("Simulyatsiya orqali ta'lim", "Haqiqiy qurilmani buzish xavfisiz, ta'mirlash ketma-ketligini mashq qilish.")],
      holat="2.30 demo versiya.", sabab="ishlab chiqilmoqda"),
 dict(bolim="oyin", slug="afsun-arena", nom="Afsun Arena", turi="yopiq",
      qisqa="O'zbek tilidagi avto-jang strategiya o'yini: qahramon sotib olasiz, maydonga terasiz, sinergiyalarni yig'asiz.",
      teg=["HTML", "JavaScript", "Strategiya"],
      nima="Navbatma-navbat strategiya o'yini. Do'kondan qahramonlar sotib olinadi, maydonga joylanadi va jang o'zi o'tadi. Bir xil qahramonlar birlashib kuchayadi, bir sinf yoki unsurdagi qahramonlar sinergiya beradi.",
      imkon=["Do'kon, oltin va daraja tizimi.",
             "Qahramonlarni birlashtirib kuchaytirish.",
             "Sinf va unsur sinergiyalari.",
             "Brauzerda ishlaydi."],
      tushuncha=[("Avto-jang (auto-battler)", "O'yinchi jangni boshqarmaydi, faqat jamoani tuzadi: g'alaba to'g'ri tanlov va joylashuvga bog'liq.")],
      holat="O'ynaladigan versiya.", sabab="shaxsiy loyiha"),

 # ---------------- Dasturlar va amaliy loyihalar
 dict(bolim="dastur", slug="qiyos-jadval", nom="Qiyos Jadval", turi="ochiq",
      havola=GH+"Qiyos-Jadval", repo=GH+"Qiyos-Jadval",
      qisqa="Antiplagiat va sun'iy intellekt detektori hisobotlaridagi parchalarni qirqib, Word hujjatdagi qiyosiy jadvalga joylaydigan Windows dasturi.",
      teg=["Python", "PySide6", "Windows"]),
 dict(bolim="dastur", slug="oracle-integratsiya", nom="Oracle integratsiya ishlari", turi="ochiq",
      havola=GH+"oracle-integratsiya", repo=GH+"oracle-integratsiya",
      qisqa="Oracle ma'lumotlar bazasi bilan veb-sayt interfeysini integratsiyalash (Lingvix test platformasi misolida): hisobot, taqdimot, kodlar.",
      teg=["Oracle", "SQL", "Veb"]),
]

BOLIMLAR = [("talim", "Ta'lim platformalari va kurslar"),
            ("grafika", "Animatsiya, grafika va 3D"),
            ("oyin", "O'yinlar"),
            ("dastur", "Dasturlar va amaliy loyihalar")]

CSS = """:root{--bg:#fbfaf7;--fg:#1d1d1f;--mut:#5f6368;--acc:#1f5fa8;--line:#e3e1dc;--card:#fff;--ok:#1e7a46;--lk:#8a5a00}
@media (prefers-color-scheme:dark){:root{--bg:#141517;--fg:#e8e8e6;--mut:#a0a3a8;--acc:#7fb2f0;--line:#2c2e33;--card:#1b1c1f;--ok:#6fcf97;--lk:#e0b45c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,"Times New Roman",serif}
.w{max-width:860px;margin:0 auto;padding:40px 16px 64px}
h1{font-size:30px;margin:0 0 6px}.sub{color:var(--mut);margin:0 0 18px;font:15px/1.5 system-ui,sans-serif}
nav a{display:inline-block;margin:0 8px 8px 0;padding:6px 12px;border:1px solid var(--line);border-radius:999px;color:var(--acc);text-decoration:none;font:14px system-ui,sans-serif;background:var(--card)}
h2{font-size:21px;margin:36px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.c{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--card);color:var(--fg);text-decoration:none}
.c:hover{border-color:var(--acc)}.c b{font-size:17px;line-height:1.3;margin:6px 0}.c p{margin:0 0 10px;font:14px/1.5 system-ui,sans-serif;color:var(--mut);flex:1}
.b{align-self:flex-start;font:600 11px system-ui,sans-serif;letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:999px;border:1px solid}
.b.o{color:var(--ok)}.b.y{color:var(--lk)}
.t{font:12px system-ui,sans-serif;color:var(--mut)}.t span{display:inline-block;margin:0 6px 4px 0;padding:1px 7px;border:1px solid var(--line);border-radius:6px}
.go{font:13px system-ui,sans-serif;color:var(--acc);margin-top:6px}
ul{padding-left:22px}li{margin:0 0 8px}dl dt{font-weight:600;margin-top:12px}dl dd{margin:2px 0 0 0;color:var(--fg)}
.box{border:1px solid var(--line);border-left:3px solid var(--lk);border-radius:8px;padding:12px 16px;background:var(--card);font:14px/1.55 system-ui,sans-serif;color:var(--mut);margin:24px 0}
footer{margin-top:40px;color:var(--mut);font:13px system-ui,sans-serif}"""

def bosh(title, desc, url, extra=""):
    return f"""<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="author" content="{e(MUALLIF)}">
<link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://eduhakimov.github.io/photo.jpg">
{extra}<style>{CSS}</style></head><body><div class="w">
"""

FOOT = f'<footer>© 2026 {e(MUALLIF)}. Barcha huquqlar himoyalangan.</footer>\n</div></body></html>\n'

def teglar(t):
    return '<div class="t">' + "".join(f"<span>{e(x)}</span>" for x in t) + "</div>"

def karta(i):
    if i["turi"] == "ochiq":
        href, badge, go = i["havola"], '<span class="b o">Ochiq</span>', "Ochish ↗"
    else:
        href, badge, go = i["slug"] + ".html", '<span class="b y">Yopiq · tavsif</span>', "Batafsil →"
    return (f'<a class="c" href="{e(href)}">{badge}<b>{e(i["nom"])}</b><p>{e(i["qisqa"])}</p>'
            f'{teglar(i["teg"])}<span class="go">{go}</span></a>')

os.makedirs(OUT, exist_ok=True)

# ---------- ro'yxat sahifasi
ochiq = sum(1 for i in ISHLAR if i["turi"] == "ochiq")
yopiq = len(ISHLAR) - ochiq
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Hakimov B.M. – loyihalar va ishlar",
      "url": BASE, "author": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/"},
      "hasPart": [{"@type": "CreativeWork", "name": i["nom"], "url": i["havola"] if i["turi"] == "ochiq" else BASE + i["slug"] + ".html"} for i in ISHLAR]}
s = bosh("Ishlarim – Hakimov Bahtiyorjon | loyihalar, platformalar, o'yinlar",
         f"Hakimov Bahtiyorjon Muzaffar o'g'lining {len(ISHLAR)} ta loyihasi: ta'lim platformalari, After Effects animatsiya moduli, 3D modellar, o'yinlar va dasturlar.",
         BASE, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
s += '<nav><a href="../">← Ilmiy ishlar</a><a href="https://www.youtube.com/@Bahtiyor_Studio">YouTube</a><a href="' + TG + '">Telegram</a><a href="https://github.com/eduhakimov">GitHub</a></nav>\n'
s += f'<h1>Ishlarim</h1><p class="sub">{e(MUALLIF)} · {len(ISHLAR)} ta loyiha: {ochiq} tasi ochiq (havola orqali ochiladi), {yopiq} tasi yopiq (manba kodi va materiallari tarqatilmaydi, bu yerda nima ekanligi va asosiy tushunchalari yozilgan).</p>\n'
for kod, sarlavha in BOLIMLAR:
    s += f'<h2>{e(sarlavha)}</h2><div class="g">' + "".join(karta(i) for i in ISHLAR if i["bolim"] == kod) + "</div>\n"
s += ('<h2>Ilmiy ishlar</h2><div class="g">'
      '<a class="c" href="../"><span class="b o">Ochiq</span><b>47 ta ilmiy maqola va tezis</b><p>2024–2026 yillar: kompyuter grafikasi, After Effects animatsiyasi, UI/UX, SUMO GUI. Ko\'pchiligi DOI bilan.</p><span class="go">Ro\'yxat →</span></a>'
      '<a class="c" href="../"><span class="b o">Ochiq</span><b>"Kompyuter grafikasi" o\'quv qo\'llanmasi</b><p>Djuraboyev M.K. bilan hammualliflikda, 2024, 162 bet, grif № 571-11.</p><span class="go">Batafsil →</span></a>'
      '<a class="c" href="../"><span class="b o">Ochiq</span><b>6 ta DGU/BGU guvohnomasi</b><p>Adliya vazirligida ro\'yxatdan o\'tgan dasturlar va ma\'lumotlar bazalari: Smart traffic, Smart switch, davomat botlari.</p><span class="go">Ro\'yxat →</span></a>'
      '</div>\n')
s += FOOT
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(s)

# ---------- yopiq ishlar sahifalari
for i in ISHLAR:
    if i["turi"] != "yopiq":
        continue
    url = BASE + i["slug"] + ".html"
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication" if i["bolim"] != "grafika" or "ziyoanim" in i["slug"] else "CreativeWork",
          "name": i["nom"], "description": i["qisqa"], "url": url, "inLanguage": "uz",
          "author": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/"},
          "keywords": ", ".join(i["teg"])}
    s = bosh(f'{i["nom"]} – Hakimov B.M.', i["qisqa"], url, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    s += '<nav><a href="./">← Barcha ishlar</a><a href="../">Ilmiy ishlar</a><a href="' + TG + '">Telegram</a></nav>\n'
    s += f'<span class="b y">Yopiq loyiha</span><h1>{e(i["nom"])}</h1><p class="sub">{e(i["qisqa"])}</p>{teglar(i["teg"])}\n'
    s += f'<h2>Bu nima</h2><p>{e(i["nima"])}</p>\n'
    s += '<h2>Imkoniyatlari</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in i["imkon"]) + "</ul>\n"
    s += '<h2>Asosiy tushunchalar</h2><dl>' + "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in i["tushuncha"]) + "</dl>\n"
    s += f'<h2>Holati</h2><p>{e(i["holat"])}</p>\n'
    s += (f'<div class="box">Bu loyihaning manba kodi va materiallari ochiq e\'lon qilinmagan ({e(i["sabab"])}). '
          f'Sahifada faqat uning nima ekanligi va asosiy g\'oyalari yozilgan. Hamkorlik yoki namoyish uchun '
          f'<a href="{TG}">Telegram</a> orqali bog\'laning.</div>\n')
    s += FOOT
    open(os.path.join(OUT, i["slug"] + ".html"), "w", encoding="utf-8").write(s)

# sitemap uchun ro'yxat
print("\n".join([BASE] + [BASE + i["slug"] + ".html" for i in ISHLAR if i["turi"] == "yopiq"]))
