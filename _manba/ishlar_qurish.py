# -*- coding: utf-8 -*-
"""eduhakimov.github.io/ishlar/ sahifalarini yasaydi."""
import html, json, os, re, sys

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
 dict(bolim="talim", slug="kompyuter-servis-laboratoriyasi", nom="Kompyuter servis laboratoriyasi", turi="ochiq",
      havola="https://eduhakimov.github.io/servis-laboratoriya/", repo=GH+"servis-laboratoriya",
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
      havola="https://eduhakimov.github.io/grammatika-metro/", repo=GH+"grammatika-metro",
      qisqa="Ingliz tili grammatikasini o'zbek tilida bekatma-bekat o'rgatadigan platforma: 14 yo'nalish, 43 dars, 231 mashq.",
      teg=["HTML", "JavaScript", "Ingliz tili"]),
 dict(bolim="talim", slug="lingvix", nom="Lingvix: test va lug'at platformasi", turi="ochiq",
      havola="https://eduhakimov.github.io/lingvix/", repo=GH+"eduhakimov.github.io",
      qisqa="Ingliz tili test va lug'at platformasi: 22 kunlik kurs, grammatika va lug'at kitoblari bo'yicha 2200 dan ortiq test, daraja aniqlash, transkripsiya va talaffuz.",
      teg=["HTML", "JavaScript", "Ingliz tili", "Oflayn"],
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
 dict(bolim="talim", slug="lingvix-listening", nom="Lingvix Listening", turi="ochiq",
      havola="https://eduhakimov.github.io/lingvix-listening/", repo=GH+"eduhakimov.github.io",
      qisqa="Pre-A1 dan B2 gacha 253 ta tinglab tushunish testi: audio, savollar, javoblarni tekshirish va audioskript.",
      teg=["HTML", "Audio", "Ingliz tili"],
      nima="Ingliz tilida tinglab tushunishni mashq qilish uchun oflayn ilovalar to'plami. Har bir daraja (Pre-A1, A1, A2, B1, B2) alohida ilova bo'lib, audio va topshiriqlar ichiga joylangan.",
      imkon=["Darajalar bo'yicha alohida ilovalar: Starters, A1, A2, B1, B2.",
             "Audio yozuvlar va ularga bog'langan topshiriqlar bir faylda.",
             "Internetsiz ishlaydi."],
      tushuncha=[("Darajaga moslash", "Topshiriqlar CEFR darajalariga qarab tuzilgan: o'quvchi o'z darajasidan boshlaydi."),
                 ("Katta media bilan oflayn ishlash", "Audio fayllar ilova ichiga joylangan, shuning uchun ilova yuklab olingach internet kerak bo'lmaydi.")],
      holat="Tayyor ilovalar mavjud.", sabab="audio materiallar mualliflik huquqi"),
 dict(bolim="talim", slug="test-master", nom="Test Master", turi="yopiq",
      qisqa="Lingvix'ning boshlang'ich versiyasi: ingliz tili bo'yicha test topshirish va natijani darhol ko'rish uchun bitta faylli test platformasi.",
      teg=["HTML", "JavaScript", "Test"],
      nima="Bitta HTML fayldan iborat test platformasi. Turli savol turlari (variant tanlash, matn kiritish, son kiritish) bilan ishlaydi, natijani darhol hisoblaydi.",
      imkon=["Bir nechta savol turi: variantli, yozma javob, son kiritish.",
             "Natijalar va xatolar tahlili darhol chiqadi.",
             "Internetsiz, brauzerning o'zida ishlaydi."],
      tushuncha=[("Avtomatik baholash", "Javob kiritilishi bilan tekshiriladi, xato javob uchun to'g'ri variant ko'rsatiladi."),
                 ("Bitta faylli ilova", "O'rnatish talab qilinmaydi: faylni ochish kifoya.")],
      holat="Darslarda ishlatilgan (avgust versiyasi), so'ng Lingvix platformasiga aylantirilgan.", sabab="Lingvix'ning boshlang'ich versiyasi; hozirgi ochiq versiyasi: Lingvix"),
 dict(bolim="talim", slug="master-vocabulary", nom="Master Vocabulary", turi="ochiq",
      havola=GH+"Master_vocabulary", repo=GH+"Master_vocabulary",
      qisqa="Ingliz tilidagi so'zlarni test shaklida yod olish ilovasi.",
      teg=["TypeScript", "React", "Gemini"]),

 # ---------------- Animatsiya, grafika, 3D
 dict(bolim="grafika", slug="galereya", nom="Grafik dizayn galereyasi", turi="ochiq",
      havola="https://eduhakimov.github.io/galereya/", repo=GH+"eduhakimov.github.io",
      qisqa="Fan posterlari seriyasi, tabriknomalar, brosyura, poster va sertifikat dizaynlaridan tanlangan ishlar.",
      teg=["Illustrator", "Photoshop", "Poster"]),
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
 dict(bolim="oyin", slug="kompyuter-ustasi-3d", nom="Kompyuter ustasi 3D", turi="ochiq",
      havola="https://eduhakimov.github.io/kompyuter-ustasi-3d/", repo=GH+"kompyuter-ustasi-3d",
      qisqa="Kompyuter ta'mirlash ustasi rolida 3D simulyator. Brauzerda ishlaydigan demo.",
      teg=["HTML", "WebGL", "3D", "Simulyator"],
      nima="O'yinchi kompyuter ustasi bo'lib, qurilmalarni ochadi, nosozlikni topadi va tuzatadi. Dizayn qurilmalarning o'zidan olingan: tekstolit yashili, oltin kontaktlar, qalay kulrangi.",
      imkon=["3D ish stoli va qurilmalar.",
             "Nosozlikni topish va tuzatish vazifalari.",
             "Brauzerda, o'rnatishsiz ishlaydi."],
      tushuncha=[("Simulyatsiya orqali ta'lim", "Haqiqiy qurilmani buzish xavfisiz, ta'mirlash ketma-ketligini mashq qilish.")],
      holat="2.30 demo versiya.", sabab="ishlab chiqilmoqda"),
 dict(bolim="oyin", slug="afsun-arena", nom="Afsun Arena", turi="ochiq",
      havola="https://eduhakimov.github.io/afsun-arena/", repo=GH+"afsun-arena",
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

 # ---------------- 2026-11-26 Telegram tahlilidan qo'shilganlar
 dict(bolim="talim", slug="test-markazi", nom="Test markazi", turi="ochiq",
      havola="https://eduhakimov.github.io/testlar/", repo=GH+"eduhakimov.github.io",
      qisqa="Ma'lumotlar bazasi, IT asoslari, kiberxavfsizlik, elektronika va sxemotexnika bo'yicha mashq va imtihon rejimli onlayn testlar.",
      teg=["HTML", "JavaScript", "Test"]),
 dict(bolim="talim", slug="interaktiv-trenajyorlar", nom="Interaktiv trenajyorlar to'plami", turi="yopiq",
      qisqa="Darslarda ishlatiladigan bitta faylli interaktiv mashg'ulotlar: PDF trenajyori, Illustrator darslari, konvertatsiya ustaxonasi va boshqalar.",
      teg=["HTML", "JavaScript", "Interaktiv dars"],
      nima="Har biri bitta HTML fayldan iborat, internetsiz ishlaydigan amaliy mashg'ulotlar. Talaba nazariyani o'qib o'tirmasdan, vazifani bajarib o'rganadi.",
      imkon=["Interaktiv PDF trenajyori: PowerPoint va Acrobat yordamida interaktiv PDF yaratish, 3 ta amaliy holat.",
             "Adobe Illustrator interaktiv darslari: shakllar bilan ishlash, ikonalar to'plamini chizish.",
             "Konvertatsiya ustaxonasi: fayl formatlari va ularni o'zaro o'tkazish.",
             "\"Elektron biznes\" fanidan amaliy mashg'ulot.",
             "Stipendiya testiga tayyorgarlik platformasi.",
             "Lug'at boyligini baholash (lexicon assessment), oflayn."],
      tushuncha=[("Bajarib o'rganish", "Har bir qadam vazifa shaklida beriladi, natija darhol tekshiriladi."),
                 ("Bitta faylli dars", "Dars faylini talabaga yuborish kifoya: o'rnatish, server va internet kerak emas.")],
      holat="Darslarda ishlatilmoqda.", sabab="o'quv materiali"),
 dict(bolim="metodik", slug="bitiruv-malakaviy-ishi", nom="Bakalavr bitiruv malakaviy ishi (2025)", turi="yopiq",
      qisqa="Kompyuter animatsiyasi va maxsus effektlar yo'nalishidagi bitiruv malakaviy ishi, himoya taqdimoti bilan.",
      teg=["After Effects", "Animatsiya", "Maxsus effektlar"],
      nima="Bakalavriatni yakunlovchi malakaviy ish. Kompyuter animatsiyasi va maxsus effektlar yaratish texnologiyalari o'rganilgan, amaliy qismida animatsion loyiha tayyorlangan.",
      imkon=["Nazariy qism: kompyuter animatsiyasi va maxsus effektlar texnologiyalari.",
             "Amaliy qism: After Effects muhitida animatsiya va effektlar.",
             "Himoya taqdimoti, ilmiy rahbar xulosasi, ichki va tashqi taqrizlar."],
      tushuncha=[("Maxsus effektlar (VFX)", "Haqiqiy tasvirga kompyuterda yaratilgan elementlarni qo'shish yoki tasvirni o'zgartirish."),
                 ("Kalit kadr animatsiyasi", "Harakatning asosiy holatlari belgilanadi, oraliq kadrlarni dastur o'zi hisoblaydi.")],
      holat="2025-yilda himoya qilingan.", sabab="bitiruv ishi matni"),
 dict(bolim="metodik", slug="kompyuter-grafikasi-darsligi", nom="\"Kompyuter grafikasi\" darsligi (qo'lyozma)", turi="yopiq",
      qisqa="2024-yilgi o'quv qo'llanma asosida kengaytirilgan darslik, nashrga tayyorlanmoqda.",
      teg=["Darslik", "Kompyuter grafikasi"],
      nima="Oliy ta'lim talabalari uchun \"Kompyuter grafikasi\" fanidan darslik qo'lyozmasi. 2024-yilda nashr etilgan o'quv qo'llanma (grif № 571-11) asosida yangilangan va kengaytirilgan.",
      imkon=["Rastr, vektor va fraktal grafika asoslari.",
             "Rang modellari va tasvir formatlari.",
             "Grafik muharrirlar bilan amaliy ishlar.",
             "Animatsiya va 3D modellashtirishga kirish."],
      tushuncha=[("Rastr va vektor grafika", "Rastr tasvir piksellardan, vektor tasvir esa matematik tenglamalar bilan berilgan chiziq va shakllardan tuziladi.")],
      holat="Qo'lyozma, 2026.", sabab="nashrgacha yopiq"),
 dict(bolim="metodik", slug="web-dizayn-qollanma", nom="\"Web dizayn\" o'quv qo'llanmasi", turi="yopiq",
      qisqa="Web dizayn asoslari bo'yicha o'quv qo'llanma, ichki va tashqi taqrizlar bilan.",
      teg=["O'quv qo'llanma", "Web dizayn", "UI/UX"],
      nima="Talabalar uchun web dizayn asoslari bo'yicha o'quv qo'llanma: sahifa tuzilishi, kompozitsiya, rang, tipografiya va maket tayyorlash.",
      imkon=["Web sahifa tuzilishi va kompozitsiya qoidalari.",
             "Rang, tipografiya va tasvir tanlash.",
             "Maket va prototip tayyorlash (Figma, Adobe XD).",
             "Ichki va tashqi taqrizdan o'tgan."],
      tushuncha=[("Foydalanuvchi tajribasi (UX)", "Sahifa nafaqat chiroyli, balki tez tushuniladigan va qulay bo'lishi kerak.")],
      holat="Qo'lyozma, 2025.", sabab="nashrgacha yopiq"),
 dict(bolim="metodik", slug="oquv-uslubiy-majmualar", nom="O'quv-uslubiy majmualar va sillabuslar", turi="yopiq",
      qisqa="\"Kompyuter grafikasi\" va \"Kompyuter animatsiyasi\" fanlari bo'yicha o'quv-uslubiy majmualar, ma'ruza taqdimotlari va sillabuslar.",
      teg=["O'quv-uslubiy majmua", "Sillabus", "Taqdimot"],
      nima="Fanni o'qitish uchun kerakli materiallar to'plami: ishchi dastur, ma'ruza matnlari va taqdimotlari, amaliy topshiriqlar, test savollari va baholash mezonlari.",
      imkon=["\"Kompyuter grafikasi\" o'quv-uslubiy majmuasi (2026).",
             "\"Kompyuter animatsiyasi\" o'quv-uslubiy majmuasi.",
             "Sillabuslar: kompyuter grafikasi, 3D modellashtirish.",
             "Ma'ruza taqdimotlari: Photoshop qatlamlari, CorelDRAW, maxsus effektlar, kompyuter tuzilishi.",
             "Kompyuter qurilmalari bo'yicha mustaqil o'qish qo'llanmalari: operativ xotira, tizim bloki va ona plata, monitor va chiqarish qurilmalari."],
      tushuncha=[("Sillabus", "Fanning maqsadi, mavzular rejasi, topshiriqlar va baholash tartibi yozilgan hujjat.")],
      holat="Darslarda ishlatilmoqda.", sabab="o'quv materiali"),
 dict(bolim="grafika", slug="ui-ux-loyihalar", nom="UI/UX loyihalar (Adobe XD)", turi="yopiq",
      qisqa="Kafedra, HEMIS talaba ilovasi va kibertahlil tizimi uchun interfeys maketlari.",
      teg=["Adobe XD", "UI/UX", "Prototip"],
      nima="Ta'lim tizimlari uchun foydalanuvchi interfeysi maketlari va bosiladigan prototiplar.",
      imkon=["Kafedra faoliyati uchun rollar va sahifalar tuzilmasi.",
             "HEMIS talaba ilovasi uchun interfeys konsepti.",
             "Kibertahlil tizimi uchun boshqaruv paneli."],
      tushuncha=[("Prototip", "Dasturlashdan oldin sahifalarni bosib ko'riladigan maket ko'rinishida sinash."),
                 ("Ko'z harakati tahlili", "UI/UX bo'yicha maqolalarim Sketch, Adobe XD va Figma'ni eye-tracking orqali solishtiradi.")],
      holat="Maketlar.", sabab="tashkilot ichki tizimlari"),
 dict(bolim="grafika", slug="andijon-osm-xaritasi", nom="Andijon viloyati OSM xaritasi", turi="yopiq",
      qisqa="OpenStreetMap ma'lumotlari asosida Andijon viloyati yo'llari va binolarining vektor xaritasi.",
      teg=["OpenStreetMap", "SVG", "GIS"],
      nima="Ochiq OpenStreetMap ma'lumotlaridan Andijon viloyatining yo'llari va binolari ajratib olingan va bosmaga yaroqli vektor (SVG) xaritaga aylantirilgan. Ma'lumotlar GeoPackage (GPKG) formatida ham saqlangan.",
      imkon=["Viloyat yo'llari va binolari alohida qatlamlarda.",
             "Istalgan o'lchamda bosmaga chiqariladigan vektor format.",
             "GIS dasturlarida ochiladigan GPKG ma'lumotlar bazasi."],
      tushuncha=[("OpenStreetMap", "Hamma tahrirlaydigan ochiq xarita: ma'lumotlari ODbL litsenziyasi bilan bepul foydalaniladi.")],
      holat="Tayyor, 2026.", sabab="ish fayllari katta hajmli"),
 dict(bolim="dastur", slug="davomat-botlari", nom="Telegram davomat botlari", turi="yopiq",
      qisqa="Talabalar, tyutorlar va talabalar turar joyi davomatini yuritadigan Telegram botlar. Adliya vazirligida ro'yxatdan o'tgan.",
      teg=["Telegram bot", "Davomat", "Ma'lumotlar bazasi"],
      nima="Davomatni qog'ozsiz, Telegram orqali yuritish uchun botlar. Talaba yoki tyutor botga belgi qo'yadi, mas'ul xodim esa tayyor hisobotni oladi. Hozir to'garak uchun @ADU_KS_davomat_bot vazifalarni tekshirish va davomat uchun ishlatilmoqda.",
      imkon=["Talabalar davomati boti (BGU № 1272).",
             "Talabalar turar joyi davomati boti (BGU № 1271).",
             "Tyutorlar davomatini nazorat qilish boti (BGU № 1270).",
             "To'garak vazifalari va davomati: @ADU_KS_davomat_bot."],
      tushuncha=[("Ma'lumotlar bazasi guvohnomasi", "Bot va uning bazasi O'zbekiston Respublikasi Adliya vazirligida ro'yxatdan o'tkazilgan.")],
      holat="Ishlatilmoqda.", sabab="talabalarning shaxsiy ma'lumotlari"),
]

BOLIMLAR = [("talim", "Ta'lim platformalari va kurslar"),
            ("metodik", "O'quv-metodik ishlar"),
            ("grafika", "Animatsiya, grafika va 3D"),
            ("oyin", "O'yinlar"),
            ("dastur", "Dasturlar va amaliy loyihalar")]

YUTUQLAR = [
    ("Beruniy nomidagi davlat stipendiyasi", "2024–2025 o'quv yili, 11.12.2024, № 4/4-1"),
    ("6 ta dasturiy mahsulot va ma'lumotlar bazasi guvohnomasi", "O'zbekiston Respublikasi Adliya vazirligi, 2024 (DGU/BGU)"),
    ("\"Kompyuter grafikasi\" o'quv qo'llanmasi", "Nashr ruxsatnomasi (grif) № 571-11, 2024"),
    ("47 ta ilmiy maqola va tezis", "2024–2026, ko'pchiligi DOI bilan"),
]
SERTIFIKATLAR = ["Fundamentals of Graphic Design", "Foundations of User Experience (UX) Design", "Get Started with Figma",
    "Design Fundamentals with AI", "Adobe Illustrator CC (Part 2)",
    "Adobe XD tools essential", "Adobe After Effects", "Digital Photography",
    "Digital Marketing", "Introduction to Cyber Attacks",
    "Windows Basics", "macOS Basics", "Kompyuter animatsiyasi (kurs sertifikati)", "3D modellashtirish (kurs sertifikati)"]

# Ranglar va umumiy elementlar ../dizayn.css da (yorug'/qorong'i rejim); bu yerda faqat shu sahifalar joylashuvi.
CSS = """:root{--ok:#1e7a46;--lk:#b45309}
:root[data-theme="dark"]{--ok:#6fcf97;--lk:#f0b35c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ok:#6fcf97;--lk:#f0b35c}}
.w{max-width:1040px;margin:0 auto;padding:44px 20px 64px}
h1{margin:0 0 10px;font:800 clamp(30px,4.6vw,52px)/1.02 var(--fd);letter-spacing:-.03em}
.sub{color:var(--mut);margin:0 0 22px;font-size:15.5px;line-height:1.6;max-width:760px}
nav a{display:inline-block;margin:0 8px 8px 0;padding:8px 15px;border:1px solid var(--line2);border-radius:999px;color:var(--fg);text-decoration:none;font:600 13.5px/1.2 var(--fb);background:var(--card);transition:.2s}
nav a:hover{border-color:var(--acc);color:var(--acct)}
h2{margin:48px 0 16px;font:700 clamp(20px,2.4vw,28px)/1.15 var(--fd);letter-spacing:-.02em}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.c{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;background:var(--card);color:var(--fg);text-decoration:none;box-shadow:var(--shadow);transition:transform .25s,border-color .25s}
.c:hover{border-color:color-mix(in srgb,var(--acc) 55%,var(--line));transform:translateY(-3px)}.c b{font:700 16.5px/1.3 var(--fd);margin:8px 0;letter-spacing:-.01em}.c p{margin:0 0 12px;font-size:14px;line-height:1.55;color:var(--mut);flex:1}
.b{align-self:flex-start;font:700 10.5px/1 var(--fb);letter-spacing:.08em;text-transform:uppercase;padding:5px 9px;border-radius:999px;border:1px solid}
.b.o{color:var(--ok)}.b.y{color:var(--lk)}
.t{font-size:12px;color:var(--mut)}.t span{display:inline-block;margin:0 6px 4px 0;padding:2px 8px;border:1px solid var(--line);border-radius:999px}
.go{font:700 13px var(--fb);color:var(--acct);margin-top:6px}
ul{padding-left:22px}li{margin:0 0 8px}dl dt{font-weight:700;margin-top:14px}dl dd{margin:3px 0 0 0;color:var(--fg)}
.box{border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:var(--r2);padding:14px 18px;background:var(--card);font-size:14px;line-height:1.6;color:var(--mut);margin:24px 0}
img{max-width:100%}footer{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);color:var(--mut);font-size:13px}"""

# Yuqori panel (logotip, til, rejim) va dizayn ulanishi — bosh sahifa bilan bir xil
TEMA_HEAD = ("<script>try{var t=localStorage.getItem('eduhakimov.theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>\n"
             '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Unbounded:wght@600;700;800&display=swap">'
             '<link rel="stylesheet" href="../dizayn.css">\n')
TOP = ('<header class="top"><div class="wrap"><a class="logo" href="../"><i>BH</i><span>Bahtiyorjon Hakimov</span></a>'
       '<div class="tr"><div data-i18n-sw></div><button class="tema" type="button" data-tema aria-label="Qorong\'i rejim">'
       '<svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
       '<svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
       '</button></div></div></header>\n')

# ---------- tillar (i18n): o'zbekcha - asl HTML, en/ru/zh - tarjima_*.py; ../i18n.js almashtiradi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tarjima_en, tarjima_ru, tarjima_zh  # noqa: E402
TR = {"en": tarjima_en, "ru": tarjima_ru, "zh": tarjima_zh}
TL = list(TR)


def tr_all(fn):
    """{til: fn(tarjima_moduli)}"""
    return {l: fn(TR[l]) for l in TL}


def S(key, **kw):
    """SAHIFA matni har bir tilda, o'rinlari to'ldirilgan."""
    return {l: TR[l].SAHIFA[key].format(**kw) for l in TL}


def kalit(x):
    return re.sub(r"[^a-z0-9]+", "-", x.lower()).strip("-")


class Lugat:
    """Bitta sahifa lug'ati: {uz: {...}, en: {...}, ru: {...}, zh: {...}}. Qiymatlar tayyor HTML."""
    def __init__(self):
        self.d = {"uz": {}}
        self.d.update({l: {} for l in TL})

    def add(self, key, uz, tr):
        assert set(tr) == set(TL), key
        if key in self.d["uz"]:
            assert self.d["uz"][key] == uz and all(self.d[l][key] == tr[l] for l in TL), "kalit to'qnashuvi: " + key
        self.d["uz"][key] = uz
        for l in TL:
            self.d[l][key] = tr[l]

    def el(self, tag, key, uz, tr, attrs="", raw=False):
        """<tag attrs data-i18n="key">uz</tag>; raw=False bo'lsa matnlar escape qilinadi."""
        f = (lambda x: x) if raw else e
        self.add(key, f(uz), {l: f(tr[l]) for l in TL})
        return f'<{tag}{attrs} data-i18n="{key}">{f(uz)}</{tag}>'

    def script(self):
        body = json.dumps(self.d, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
        return ('<script>(window.I18N_D=window.I18N_D||[]).push(' + body + ');</script>\n'
                '<script src="../i18n.js"></script>\n<script src="../mavzu.js"></script>\n')


def bosh(L, tkey, title, ttr, dkey, desc, dtr, url, extra=""):
    L.add(tkey, e(title), {l: e(ttr[l]) for l in TL})
    L.add(dkey, desc, dtr)  # atribut qiymati: xom matn
    return f"""<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title data-i18n="{tkey}">{e(title)}</title><meta name="description" data-i18n-attr="content:{dkey}" content="{e(desc)}"><meta name="author" content="{e(MUALLIF)}">
<link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://eduhakimov.github.io/photo.jpg">
{TEMA_HEAD}{extra}<style>{CSS}</style></head><body>
{TOP}<div class="w">
"""


def foot(L):
    import v2_ikonlar  # aloqa belgilari (pochta, Telegram, Discord, YouTube, ORCID ...)
    return (v2_ikonlar.SOC.replace('<div class="soc">', '<div class="soc" style="margin-top:48px">', 1) +
            f'<footer data-i18n="foot.rights">© 2026 {e(MUALLIF)}. Barcha huquqlar himoyalangan.</footer>\n</div>\n'
            + L.script() + '</body></html>\n')


def teglar(t, L):
    out = []
    for x in t:
        if x in tarjima_en.TEG:
            out.append(L.el("span", "teg." + kalit(x), x, tr_all(lambda m: m.TEG[x])))
        else:
            out.append(f"<span>{e(x)}</span>")
    return '<div class="t">' + "".join(out) + "</div>"


def karta(i, L):
    s = i["slug"]
    if i["turi"] == "ochiq":
        href = i["havola"]
        badge = '<span class="b o" data-i18n="badge.open">Ochiq</span>'
        go = '<span class="go" data-i18n="go.open">Ochish ↗</span>'
    else:
        href = s + ".html"
        badge = '<span class="b y" data-i18n="badge.closed">Yopiq · tavsif</span>'
        go = '<span class="go" data-i18n="go.more">Batafsil →</span>'
    return (f'<a class="c" href="{e(href)}">{badge}'
            + L.el("b", f"c.{s}.nom", i["nom"], tr_all(lambda m: m.ISHLAR[s]["nom"]))
            + L.el("p", f"c.{s}.qisqa", i["qisqa"], tr_all(lambda m: m.ISHLAR[s]["qisqa"]))
            + f'{teglar(i["teg"], L)}{go}</a>')


os.makedirs(OUT, exist_ok=True)

# ---------- ro'yxat sahifasi
ochiq = sum(1 for i in ISHLAR if i["turi"] == "ochiq")
yopiq = len(ISHLAR) - ochiq
n = len(ISHLAR)
L = Lugat()
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Hakimov B.M. – loyihalar va ishlar",
      "url": BASE, "author": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/"},
      "hasPart": [{"@type": "CreativeWork", "name": i["nom"], "url": i["havola"] if i["turi"] == "ochiq" else BASE + i["slug"] + ".html"} for i in ISHLAR]}
s = bosh(L, "ish.title", "Ishlarim – Hakimov Bahtiyorjon | loyihalar, platformalar, o'yinlar", S("ish.title"),
         "ish.desc", f"Hakimov Bahtiyorjon Muzaffar o'g'lining {n} ta loyihasi: ta'lim platformalari, After Effects animatsiya moduli, 3D modellar, o'yinlar va dasturlar.",
         S("ish.desc", n=n), BASE, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
s += ('<nav><a href="../" data-i18n="nav.sci">← Ilmiy ishlar</a><a href="https://www.youtube.com/@Bahtiyor_Studio">YouTube</a>'
      '<a href="' + TG + '">Telegram</a><a href="https://github.com/eduhakimov">GitHub</a></nav>\n')
s += (L.el("h1", "ish.h1", "Ishlarim", S("ish.h1"))
      + L.el("p", "ish.sub", f"{MUALLIF} · {n} ta loyiha: {ochiq} tasi ochiq (havola orqali ochiladi), {yopiq} tasi yopiq (manba kodi va materiallari tarqatilmaydi, bu yerda nima ekanligi va asosiy tushunchalari yozilgan).",
             S("ish.sub", author=MUALLIF, n=n, o=ochiq, y=yopiq), attrs=' class="sub"') + "\n")
for kod, sarlavha in BOLIMLAR:
    s += (L.el("h2", "bolim." + kod, sarlavha, tr_all(lambda m: m.BOLIMLAR[kod]))
          + '<div class="g">' + "".join(karta(i, L) for i in ISHLAR if i["bolim"] == kod) + "</div>\n")
import dasturlar_qurish as DQ  # noqa: E402  desktop dasturlar bo'limi (ma'lumotlar: dasturlar.py)
s += DQ.bolim(L, globals())
OCH = '<a class="c" href="../"><span class="b o" data-i18n="badge.open">Ochiq</span>'
s += (L.el("h2", "ish.h.sci", "Ilmiy ishlar", S("ish.h.sci")) + '<div class="g">'
      + OCH + L.el("b", "ish.sci1.b", "47 ta ilmiy maqola va tezis", S("ish.sci1.b", p=47))
      + L.el("p", "ish.sci1.p", "2024–2026 yillar: kompyuter grafikasi, After Effects animatsiyasi, UI/UX, SUMO GUI. Ko'pchiligi DOI bilan.", S("ish.sci1.p"))
      + '<span class="go" data-i18n="go.list">Ro\'yxat →</span></a>'
      + OCH + L.el("b", "ish.sci2.b", "\"Kompyuter grafikasi\" o'quv qo'llanmasi", S("ish.sci2.b"))
      + L.el("p", "ish.sci2.p", "Djuraboyev M.K. bilan hammualliflikda, 2024, 162 bet, grif № 571-11.", S("ish.sci2.p"))
      + '<span class="go" data-i18n="go.more">Batafsil →</span></a>'
      + OCH + L.el("b", "ish.sci3.b", "6 ta DGU/BGU guvohnomasi", S("ish.sci3.b"))
      + L.el("p", "ish.sci3.p", "Adliya vazirligida ro'yxatdan o'tgan dasturlar va ma'lumotlar bazalari: Smart traffic, Smart switch, davomat botlari.", S("ish.sci3.p"))
      + '<span class="go" data-i18n="go.list">Ro\'yxat →</span></a>'
      + '</div>\n')
s += L.el("h2", "ish.h.yutuq", "Yutuqlar va sertifikatlar", S("ish.h.yutuq"), attrs=' id="yutuqlar"') + '<ul>'
for k, (a, b) in enumerate(YUTUQLAR):
    s += ('<li>' + L.el("b", f"ish.y.{k}.a", a, tr_all(lambda m: m.YUTUQLAR[k][0])) + '<br>'
          + L.el("span", f"ish.y.{k}.b", b, tr_all(lambda m: m.YUTUQLAR[k][1]), attrs=' class="t"') + '</li>')
s += '</ul>\n'
s += L.el("p", "ish.sert", "Onlayn kurs sertifikatlari: " + " · ".join(SERTIFIKATLAR) + ".",
          tr_all(lambda m: m.SAHIFA["ish.sert"] + " · ".join(m.SERT.get(x, x) for x in SERTIFIKATLAR) + "."), attrs=' class="t"') + '\n'
s += '<p>' + L.el("a", "ish.all", "Barcha yutuqlar va 45 ta xalqaro sertifikat ro'yxati →", S("ish.all", j=45), attrs=' class="go" href="../yutuqlar/"') + '</p>\n'
s += foot(L)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(s)

# ---------- yopiq ishlar sahifalari
for i in ISHLAR:
    if i["turi"] != "yopiq":
        continue
    sl = i["slug"]
    tt = {l: TR[l].ISHLAR[sl] for l in TL}
    L = Lugat()
    url = BASE + sl + ".html"
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication" if i["bolim"] != "grafika" or "ziyoanim" in sl else "CreativeWork",
          "name": i["nom"], "description": i["qisqa"], "url": url, "inLanguage": "uz",
          "author": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/"},
          "keywords": ", ".join(i["teg"])}
    s = bosh(L, "p.title", f'{i["nom"]} – Hakimov B.M.', {l: tt[l]["nom"] + " – Hakimov B.M." for l in TL},
             "p.desc", i["qisqa"], {l: tt[l]["qisqa"] for l in TL}, url,
             f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    s += ('<nav><a href="./" data-i18n="nav.works_back">← Barcha ishlar</a><a href="../" data-i18n="nav.sci_plain">Ilmiy ishlar</a>'
          '<a href="' + TG + '">Telegram</a></nav>\n')
    s += ('<span class="b y" data-i18n="badge.closedproj">Yopiq loyiha</span>'
          + L.el("h1", "p.nom", i["nom"], {l: tt[l]["nom"] for l in TL})
          + L.el("p", "p.qisqa", i["qisqa"], {l: tt[l]["qisqa"] for l in TL}, attrs=' class="sub"')
          + teglar(i["teg"], L) + "\n")
    s += L.el("h2", "p.h.nima", "Bu nima", S("p.h.nima")) + L.el("p", "p.nima", i["nima"], {l: tt[l]["nima"] for l in TL}) + "\n"
    assert all(len(tt[l]["imkon"]) == len(i["imkon"]) and len(tt[l]["tushuncha"]) == len(i["tushuncha"]) for l in TL), sl
    s += (L.el("h2", "p.h.imkon", "Imkoniyatlari", S("p.h.imkon")) + '<ul>'
          + "".join(L.el("li", f"p.imkon.{k}", x, {l: tt[l]["imkon"][k] for l in TL}) for k, x in enumerate(i["imkon"]))
          + "</ul>\n")
    s += (L.el("h2", "p.h.tush", "Asosiy tushunchalar", S("p.h.tush")) + '<dl>'
          + "".join(L.el("dt", f"p.t.{k}.a", a, {l: tt[l]["tushuncha"][k][0] for l in TL})
                    + L.el("dd", f"p.t.{k}.b", b, {l: tt[l]["tushuncha"][k][1] for l in TL})
                    for k, (a, b) in enumerate(i["tushuncha"]))
          + "</dl>\n")
    s += L.el("h2", "p.h.holat", "Holati", S("p.h.holat")) + L.el("p", "p.holat", i["holat"], {l: tt[l]["holat"] for l in TL}) + "\n"
    box_uz = (f'Bu loyihaning manba kodi va materiallari ochiq e\'lon qilinmagan ({e(i["sabab"])}). '
              f'Sahifada faqat uning nima ekanligi va asosiy g\'oyalari yozilgan. Hamkorlik yoki namoyish uchun '
              f'<a href="{TG}">Telegram</a> orqali bog\'laning.')
    s += L.el("div", "p.box", box_uz, {l: TR[l].SAHIFA["p.box"].format(sabab=e(tt[l]["sabab"]), tg=TG) for l in TL},
              attrs=' class="box"', raw=True) + "\n"
    s += foot(L)
    open(os.path.join(OUT, sl + ".html"), "w", encoding="utf-8").write(s)

DQ_URLS = DQ.sahifalar(OUT, globals())

# YUTUQ_SAHIFA
# ---------- yutuqlar sahifasi (../yutuqlar/)
CV = "https://www.coursera.org/verify/"
DAVLAT = [
    ("Beruniy nomidagi davlat stipendiyasi sohibi", "O'zbekiston Respublikasi Oliy ta'lim, fan va innovatsiyalar vazirligi, 2024/2025 o'quv yili. Guvohnoma: 11.12.2024, № 4/4-1."),
    ("Bakalavriat imtiyozli diplom bilan", "GPA 4.92. Magistraturaga 2025-yilda qo'shimcha davlat granti asosida qabul qilingan."),
    ("Prezident davlat stipendiyasiga nomzod", "2026/2027 o'quv yili, universitet rektori tavsiyanomasi: 20.07.2026, № 01-3066."),
    ("6 ta dasturiy mahsulot va ma'lumotlar bazasi guvohnomasi (DGU/BGU)", "O'zbekiston Respublikasi Adliya vazirligi, 2024: Smart traffic, Smart switch, elektr ta'minotini boshqaruvchi aqlli tizim va 3 ta davomat telegram boti."),
    ("\"Kompyuter grafikasi\" o'quv qo'llanmasi (hammuallif)", "162 bet, ADU nashr ruxsatnomasi 09.07.2024 (buyruq № 0102571). Antiplagiat: originallik 98.15%."),
]
TANLOV = [
    ("\"Yil talabasi\" tanlovi, 2023", "Respublika bosqichi ishtirokchisi."),
    ("\"Mirzo Ulug'bek vorislari\" tanlovi, 2024", "Respublika bosqichi ishtirokchisi, innovatsion loyiha bilan."),
    ("\"Cyber102 Week\" IT tanlovi", "Faxrli o'rin."),
    ("Andijon viloyati IIB tashakkurnomasi", "Yoshlar va voyaga yetmaganlar o'rtasida jinoyatchilikning oldini olishdagi hamkorlik uchun. 03.12.2025, № 01-0023-25."),
    ("ADU rektori tashakkurnomalari (4 ta)", "A'lo o'qish va jamoat ishlaridagi faollik (2024/2025), \"Yoshlar kuni\" va \"Navro'z\" ko'rik-tanlovlari, ommaviy tadbirlardagi tashabbuskorlik uchun."),
    ("Onlayn olimpiada, I darajali diplom", "Telegram orqali o'tkazilgan onlayn olimpiada."),
]
# (platforma, [(kurs, tashkilot, sana, coursera_tekshirish_kodi)])
XALQARO = [
    ("Coursera", [
        ("Adobe Marketing Specialist (Professional Certificate)", "Adobe", "03.2026", "professional-cert/Q49HB9P9ELV9"),
        ("Security Operations Center (SOC)", "Cisco Learning and Certifications", "03.2024", "2PC5R5YKJEDT"),
        ("Foundations of User Experience (UX) Design", "Google", "17.12.2023", "ZN89LEP24TFK"),
        ("Fundamentals of Graphic Design", "California Institute of the Arts", "17.12.2023", "NBKGP66Y9ZCF"),
        ("Introduction to Cybersecurity Tools & Cyber Attacks", "IBM", "15.12.2023", "EEKNY5GU86KK"),
        ("Design Fundamentals with AI", "Adobe", "02.03.2026", "OJUOVPKC6LKE"),
        ("Generative AI Content Creation", "Adobe", "02.03.2026", "DN5TB0NHN4IL"),
        ("Digital Marketing", "Adobe", "02.03.2026", "E7URFOPKUFHU"),
        ("Social Media Content and Strategy", "Adobe", "02.03.2026", "LFTC67EF1EZO"),
        ("Multichannel Content Marketing", "Adobe", "04.03.2026", "EKOCX2KFQYJQ"),
        ("Adobe Illustrator CC: Part 2", "Logical Operations", "04.03.2026", "K8RH4J8LLDXE"),
        ("Agile Leadership: Introduction to Change", "University of Colorado System", "08.04.2024", "TFRX8XPTSFLJ"),
        ("Introduction to Cybersecurity Fundamentals", "Coursera Instructor Network", "08.04.2024", "9UNQ9TN4FY2V"),
        ("Get Started with Figma", "Coursera Project Network", "17.12.2023", "52BX87KJCYGS"),
        ("Create eye-catching logos using Canva for an ebrand", "Coursera Project Network", "17.12.2023", "N55VR7L2LCNR"),
    ]),
    ("Google, Cisco va boshqa xalqaro kompaniyalar", [
        ("Google Certified Educator, Level 1", "Google for Education", "22.01.2022", None),
        ("Get Connected", "Cisco Networking Academy", "08.01.2022", None),
        ("Responsive Web Design (≈300 soat)", "freeCodeCamp", "28.10.2022", None),
        ("Python", "Kaggle", "", None),
        ("Cyber Security Global Virtual Internship", "Clifford Chance · Forage", "30.11.2022", None),
        ("Digital Skills: Digital Marketing", "Accenture · FutureLearn", "", None),
        ("ISO/IEC 27001 Information Security Associate", "SkillFront", "28.01.2023", None),
    ]),
    ("LinkedIn Learning (PMI PDU / NASBA CPE)", [
        ("Communication Foundations", "LinkedIn Learning", "29.11.2022", None),
        ("Managing Projects with Microsoft 365", "LinkedIn Learning", "29.11.2022", None),
        ("What is Graphic Design?", "LinkedIn Learning", "29.11.2022", None),
        ("Writing a Resume", "LinkedIn Learning", "29.11.2022", None),
        ("Video Interview Tips", "LinkedIn Learning", "29.11.2022", None),
        ("Project Management Foundations: Teams", "LinkedIn Learning", "15.06.2023", None),
        ("Building Resilience", "LinkedIn Learning", "09.10.2023", None),
    ]),
    ("GCFGlobal", [
        ("Beginning Graphic Design", "GCFGlobal", "23.03.2024", None),
        ("Photoshop Basics", "GCFGlobal", "23.03.2024", None),
        ("Digital Photography", "GCFGlobal", "23.03.2024", None),
        ("Windows Basics", "GCFGlobal", "23.03.2024", None),
        ("macOS Basics", "GCFGlobal", "23.03.2024", None),
    ]),
    ("Mind Luster", [
        ("Adobe After Effects and Techniques", "Mind Luster", "21.02.2024", None),
        ("Adobe Illustrator", "Mind Luster", "21.02.2024", None),
        ("Adobe XD Tools Essentials", "Mind Luster", "21.02.2024", None),
        ("Professional Photoshop Guide", "Mind Luster", "21.02.2024", None),
        ("Graphic Design", "Mind Luster", "21.02.2024", None),
    ]),
    ("Boshqa xalqaro o'quv markazlari", [
        ("MS Office (short course), baho: Pass", "Oxford Home Study Centre", "29.11.2022", None),
        ("Video editing with Premiere Pro (2 oy)", "Aula.bg, Bolgariya", "28.06.2022", None),
        ("Graphic Design (online course)", "EDUCBA", "", None),
        ("Python for Beginners", "Simplilearn SkillUp", "", None),
        ("Getting Started with Python", "iTronix Solutions", "28.01.2023", None),
        ("Cyber Security certification program", "The Digital Adda", "28.01.2023", None),
    ]),
]
TIL = [("Ingliz tili, B2", "Ibrat Academy · Yoshlar ishlari agentligi, 27.08.2024"),
       ("Rus tili, B2", "Ibrat Academy · Yoshlar ishlari agentligi, 27.08.2024")]
JAMI = sum(len(k) for _, k in XALQARO)
YB = "https://eduhakimov.github.io/yutuqlar/"
YO = os.path.join(os.path.dirname(os.path.abspath(OUT)), "yutuqlar")
os.makedirs(YO, exist_ok=True)
ld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": YB,
      "mainEntity": {"@type": "Person", "name": "Bahtiyorjon Hakimov", "url": "https://eduhakimov.github.io/",
                     "hasCredential": [dict({"@type": "EducationalOccupationalCredential", "name": k,
                                             "recognizedBy": {"@type": "Organization", "name": t}},
                                            **({"url": CV + c} if c else {}))
                                       for _, ks in XALQARO for k, t, d, c in ks]}}
assert JAMI == 45, JAMI  # ishlar/index.html va index.html dagi "45" bilan bir xil bo'lsin
L = Lugat()
s = bosh(L, "yt.title", "Yutuqlar va sertifikatlar – Hakimov Bahtiyorjon", S("yt.title"),
         "yt.desc", f"Hakimov Bahtiyorjon Muzaffar o'g'lining davlat mukofotlari, tanlovlardagi natijalari va {JAMI} ta xalqaro sertifikati: Google, IBM, Adobe, Cisco, Coursera.",
         S("yt.desc", j=JAMI), YB, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
s += ('<nav><a href="../" data-i18n="nav.sci">← Ilmiy ishlar</a><a href="../ishlar/" data-i18n="nav.works">Barcha ishlar</a>'
      '<a href="../galereya/" data-i18n="nav.gallery">Galereya</a><a href="' + TG + '">Telegram</a></nav>\n')
s += (L.el("h1", "yt.h1", "Yutuqlar va sertifikatlar", S("yt.h1"))
      + L.el("p", "yt.sub", f"{MUALLIF} · davlat mukofotlari, tanlovlar va {JAMI} ta xalqaro sertifikat. "
                            "Ma'lumotlar asl hujjatlar asosida yozilgan; Coursera sertifikatlarini havola orqali tekshirish mumkin.",
             S("yt.sub", author=MUALLIF, j=JAMI), attrs=' class="sub"') + "\n")


def li2(key, a, b, tra, trb):
    return ('<li>' + L.el("b", key + ".a", a, tra) + '<br>'
            + L.el("span", key + ".b", b, trb, attrs=' class="t"') + '</li>')


s += (L.el("h2", "yt.h.davlat", "Davlat mukofotlari va rasmiy e'tirof", S("yt.h.davlat")) + "<ul>"
      + "".join(li2(f"yt.d.{k}", a, b, tr_all(lambda m: m.DAVLAT[k][0]), tr_all(lambda m: m.DAVLAT[k][1]))
                for k, (a, b) in enumerate(DAVLAT)) + '</ul>\n')
s += (L.el("h2", "yt.h.tanlov", "Tanlovlar va tashakkurnomalar", S("yt.h.tanlov")) + "<ul>"
      + "".join(li2(f"yt.t.{k}", a, b, tr_all(lambda m: m.TANLOV[k][0]), tr_all(lambda m: m.TANLOV[k][1]))
                for k, (a, b) in enumerate(TANLOV)) + '</ul>\n')
s += L.el("h2", "yt.h.xalqaro", f"Xalqaro sertifikatlar ({JAMI} ta)", S("yt.h.xalqaro", j=JAMI)) + "\n"
for pi, (plat, ks) in enumerate(XALQARO):
    h3_uz = f'{e(plat)} <span class="t">· {len(ks)} ta</span>'
    h3_tr = tr_all(lambda m: e(m.PLATFORMA.get(plat, plat)) + ' <span class="t">' + e(m.SAHIFA["yt.cnt"].format(n=len(ks))) + '</span>')
    s += L.el("h3", f"yt.pl.{pi}", h3_uz, h3_tr, attrs=' style="font-size:17px;margin:22px 0 8px"', raw=True) + '<ul>'
    for ki, (k, t, d, c) in enumerate(ks):
        b = (L.el("b", f"yt.k.{pi}.{ki}", k, tr_all(lambda m: m.KURS[k])) if k in tarjima_en.KURS else f"<b>{e(k)}</b>")
        izoh = " · ".join(x for x in (t, d) if x)
        if t in tarjima_en.TASHKILOT:
            izoh_h = L.el("span", f"yt.o.{pi}.{ki}", izoh, tr_all(lambda m: " · ".join(x for x in (m.TASHKILOT[t], d) if x)))
        else:
            izoh_h = e(izoh)
        tek = f' · <a href="{CV}{c}" data-i18n="verify">tekshirish ↗</a>' if c else ""
        s += f'<li>{b}<br><span class="t">{izoh_h}{tek}</span></li>'
    s += '</ul>\n'
s += (L.el("h2", "yt.h.til", "Til sertifikatlari", S("yt.h.til")) + "<ul>"
      + "".join(li2(f"yt.l.{k}", a, b, tr_all(lambda m: m.TIL[k][0]), tr_all(lambda m: m.TIL[k][1]))
                for k, (a, b) in enumerate(TIL)) + '</ul>\n')
box_uz = ("Sertifikatlarning asl nusxalari muallifda saqlanadi. Hujjatlarni ko'rish yoki tekshirish uchun "
          f'<a href="{TG}">Telegram</a> orqali bog\'laning.')
s += L.el("div", "yt.box", box_uz, S("yt.box", tg=TG), attrs=' class="box"', raw=True) + "\n"
s += foot(L)
open(os.path.join(YO, "index.html"), "w", encoding="utf-8").write(s)

# sitemap uchun ro'yxat
print("\n".join([YB, BASE] + [BASE + i["slug"] + ".html" for i in ISHLAR if i["turi"] == "yopiq"] + DQ_URLS))
