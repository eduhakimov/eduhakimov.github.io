# -*- coding: utf-8 -*-
"""Lingvix Listening'ning uchta oflayn faylidan (Starters/A1/B1, A2, B2) bitta veb-ilova yig'adi.

- darajalar bitta ilovaga birlashtiriladi (Pre-A1, A1, A2, B1, B2);
- rasmlar img/ ga, audio audio/ ga alohida fayl bo'lib chiqadi (base64 emas);
- audio ASL sifatida saqlanadi, qayta siqilmaydi (muallif yozuvlarni o'zi tayyorlagan);
  faqat 95 MB dan katta klip bo'lsa, o'shanisi qayta siqiladi;
- GitHub Pages 1 GB chegarasi uchun audio darajalar bo'yicha uch repoga bo'linadi:
  lingvix-listening (ilova, rasmlar, Starters/A1/B1 audio), lingvix-listening-a2, lingvix-listening-b2.
  Hammasi bitta eduhakimov.github.io manzilida: ilova ularni ../<repo>/audio/ orqali yuklaydi;
- testlar va audio manbasi (englishpracticetest.net) ko'rsatiladi, mualliflik himoyasi qo'shiladi.

Ishga tushirish:  python -X utf8 _manba/listening_qurish.py
Natija: D:/Bahtiyor/Saytlar/lingvix-listening, lingvix-listening-a2, lingvix-listening-b2
"""
import base64, json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilovalar_qurish import himoyala, litsenziya, readme, FONTS  # noqa: E402

MANBA = r"D:\Bahtiyor\10_Arxiv\Ish stoli nusxalari\rab stol 08.11.2026\Lingvix"
SAYTLAR = r"D:\Bahtiyor\Saytlar"
ASOSIY = "lingvix-listening"
# (manba fayl, audio joylanadigan repo)
FAYLLAR = [("Lingvix-Listening-Starters-A1-B1.html", ASOSIY),
           ("Lingvix-Listening-A2.html", "lingvix-listening-a2"),
           ("Lingvix-Listening-B2.html", "lingvix-listening-b2")]
CHIQ = os.path.join(SAYTLAR, ASOSIY)
URL = "https://eduhakimov.github.io/lingvix-listening/"
NOM = "Lingvix Listening"
DARAJALAR = ["Pre-A1", "A1", "A2", "B1", "B2"]
ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
MAX_FAYL = 95 * 2**20

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = "ffmpeg"

UCHINCHI = ["Listening tests, audioscripts, images and audio recordings: englishpracticetest.net "
            "(https://www.englishpracticetest.net/) - copyright of their respective owners; "
            "used here for free, non-commercial education with attribution.", FONTS]

MANBA_YOZUV = r"""
<!-- lsn-manba -->
<style>
.lsn-manba{position:fixed;right:8px;bottom:6px;z-index:2147483000;font:11px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;
  color:#fff;background:rgba(20,22,26,.55);padding:3px 8px;border-radius:999px;text-decoration:none;opacity:.7}
.lsn-manba:hover,.lsn-manba:focus{opacity:1;text-decoration:underline}
</style>
<script>
document.addEventListener("DOMContentLoaded", function () {
  var a = document.createElement("a");
  a.className = "lsn-manba";
  a.href = "https://www.englishpracticetest.net/";
  a.target = "_blank"; a.rel = "noopener";
  a.title = "Testlar, matnlar va audio manbasi: englishpracticetest.net (bepul, notijorat, ta'lim maqsadida)";
  a.textContent = "Testlar va audio: englishpracticetest.net";
  document.body.appendChild(a);
});
</script>
"""

AUDIO_URL_ESKI = "const el = document.getElementById('lsn-a-' + id); if(!el) return '';"
AUDIO_URL_YANGI = ("const el = document.getElementById('lsn-a-' + id); if(!el){ if(!window.LSN_AUD){ try{ "
                   "window.LSN_AUD = JSON.parse(document.getElementById('lsn-aud').textContent); }catch(e){ "
                   "window.LSN_AUD = {}; } } return (window.LSN_AUD[id] || '') + 'audio/' + encodeURIComponent(id) + '.mp3'; }")


def skript(s, sid):
    m = re.search(r'<script id="%s"[^>]*>' % re.escape(sid), s)
    e = s.find("</script>", m.end())
    return m, e


def yoz(yol, matn):
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(matn)


def chiqar(vazifa):
    """Asl audio baytlarini o'zgartirmasdan yozadi; 95 MB dan katta bo'lsagina qayta siqadi."""
    b64, chiq = vazifa
    data = base64.b64decode(re.sub(r"\s+", "", b64))
    if len(data) <= MAX_FAYL:
        with open(chiq, "wb") as f:
            f.write(data)
        return
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as t:
        t.write(data)
        kir = t.name
    try:
        subprocess.run([FFMPEG, "-v", "error", "-y", "-i", kir, "-b:a", "64k", chiq], check=True)
    finally:
        os.remove(kir)
    print("  qayta siqildi (95 MB dan katta):", chiq, flush=True)


def main():
    os.makedirs(os.path.join(CHIQ, "img"), exist_ok=True)
    darajalar, rasmlar, aud, qobiq = {}, {}, {}, None
    for nom, repo in FAYLLAR:
        papka = os.path.join(SAYTLAR, repo)
        os.makedirs(os.path.join(papka, "audio"), exist_ok=True)
        print("o'qilmoqda:", nom, "->", repo, flush=True)
        with open(os.path.join(MANBA, nom), encoding="utf-8") as f:
            s = f.read()
        m, e = skript(s, "lsn-book")
        for lv in json.loads(s[m.end():e])["levels"]:
            if lv["tests"]:
                assert lv["id"] not in darajalar, lv["id"]
                darajalar[lv["id"]] = lv
        m, e = skript(s, "lsn-img")
        for k, v in json.loads(s[m.end():e]).items():
            assert ID_RE.match(k), k
            mime, data = re.match(r"data:image/([a-z+]+);base64,(.*)$", v, re.S).groups()
            ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(mime, mime)
            yol = "img/%s.%s" % (k, ext)
            with open(os.path.join(CHIQ, yol), "wb") as f:
                f.write(base64.b64decode(data))
            rasmlar[k] = yol
        vazifalar, oxiri = [], 0
        for am in re.finditer(r'<script id="lsn-a-([^"]+)"[^>]*>', s):
            aid = am.group(1)
            assert ID_RE.match(aid), aid
            ae = s.find("</script>", am.end())
            oxiri = ae + len("</script>")
            vazifalar.append((s[am.end():ae], os.path.join(papka, "audio", aid + ".mp3")))
            if repo != ASOSIY:
                aud[aid] = "../%s/" % repo
        print("  audio:", len(vazifalar), flush=True)
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
            list(ex.map(chiqar, vazifalar))
        if qobiq is None:
            qobiq = (s[:s.find("<!--LSN-DATA-START-->")], s[oxiri:])
        del s

    kitob = {"title": NOM, "levels": [darajalar.get(d, {"id": d, "tests": []}) for d in DARAJALAR]}
    data = ("<!--LSN-DATA-START-->\n"
            '<script id="lsn-book" type="application/json">'
            + json.dumps(kitob, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>\n"
            '<script id="lsn-img" type="application/json">' + json.dumps(rasmlar, separators=(",", ":")) + "</script>\n"
            '<script id="lsn-aud" type="application/json">' + json.dumps(aud, separators=(",", ":")) + "</script>\n")
    html = qobiq[0] + data + qobiq[1]
    assert html.count(AUDIO_URL_ESKI) == 1
    html = html.replace(AUDIO_URL_ESKI, AUDIO_URL_YANGI)
    html = himoyala(html, NOM, URL)
    i = html.lower().rfind("</body>")
    html = html[:i] + MANBA_YOZUV + html[i:]
    yoz(os.path.join(CHIQ, "index.html"), html)
    yoz(os.path.join(CHIQ, "LICENSE.txt"), litsenziya(NOM, URL, UCHINCHI))
    tavsif = ("Ingliz tilida tinglab tushunish mashqlari: Pre-A1 dan B2 gacha darajalar, audio, savollar, "
              "javoblarni tekshirish va audioskript. Testlar va audio manbasi: englishpracticetest.net.")
    yoz(os.path.join(CHIQ, "README.md"), readme(NOM, URL, tavsif).replace(
        "Bitta HTML fayldan iborat: o'rnatish va server talab qilinmaydi, brauzerda ishlaydi.",
        "Brauzerda ishlaydi. `index.html` ilova, `img/` rasmlar, `audio/` Starters/A1/B1 audiosi (asl MP3). "
        "A2 va B2 audiosi [lingvix-listening-a2](https://github.com/eduhakimov/lingvix-listening-a2) va "
        "[lingvix-listening-b2](https://github.com/eduhakimov/lingvix-listening-b2) repolarida "
        "(GitHub Pages hajm chegarasi uchun)."))
    yoz(os.path.join(CHIQ, "robots.txt"), "User-agent: *\nAllow: /\n")

    for _, repo in FAYLLAR[1:]:
        papka = os.path.join(SAYTLAR, repo)
        daraja = repo.split("-")[-1].upper()
        yoz(os.path.join(papka, "index.html"),
            '<!doctype html><html lang="uz"><meta charset="utf-8"><title>%s: %s audio</title>'
            '<meta name="author" content="Hakimov Bahtiyorjon Muzaffar o\'g\'li">'
            '<meta http-equiv="refresh" content="0; url=%s"><link rel="canonical" href="%s">'
            '<p>%s darajasi audio fayllari. Ilova: <a href="%s">%s</a></p>'
            '<p>&copy; 2026 Hakimov B.M. &middot; <a href="https://eduhakimov.github.io/">Bosh sahifa</a></p></html>\n'
            % (NOM, daraja, URL, URL, daraja, URL, URL))
        yoz(os.path.join(papka, "LICENSE.txt"), litsenziya("%s (%s audio)" % (NOM, daraja), URL, UCHINCHI))
        yoz(os.path.join(papka, "README.md"),
            "# %s: %s audio\n\n%s ilovasining %s darajasi audio fayllari (asl MP3).\n\n"
            "**Ilova:** %s\n\nTestlar va audio manbasi: englishpracticetest.net. Bepul, notijorat, ta'lim maqsadida.\n\n"
            "## Mualliflik huquqi / Copyright\n\n(c) 2026 Bahtiyorjon Hakimov (ilova). Batafsil: [LICENSE.txt](LICENSE.txt)\n"
            % (NOM, daraja, NOM, daraja, URL))
        yoz(os.path.join(papka, "robots.txt"), "User-agent: *\nDisallow: /audio/\n")

    n = sum(len(lv["tests"]) for lv in kitob["levels"])
    print("tayyor:", n, "test,", len(rasmlar), "rasm,", len(aud), "tashqi audio, index.html", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
