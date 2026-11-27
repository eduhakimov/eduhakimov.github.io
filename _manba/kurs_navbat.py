# -*- coding: utf-8 -*-
"""Navbatdagi kurslardan internetda ochilganlarini (HTTP 200) bosh sahifaga va profil README'ga qo'shadi, keyin push qiladi.
  python _manba/kurs_navbat.py
Chiqish: qo'shilgan sluglar ro'yxati (Discord/offline sessiyalariga xabar berish uchun)."""
import io, json, os, subprocess, sys, tempfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFIL = r"C:\Users\ASUSRO~1\AppData\Local\Temp\claude\0fa2f3b7e932577a\e964627a-1dff-413d-ba09-06e9f9926802\scratchpad\profil"
GIT = ["git", "-c", "user.name=Bahtiyorjon Hakimov", "-c", "user.email=258009478+eduhakimov@users.noreply.github.com"]
N = json.load(io.open(os.path.join(ROOT, "_manba", "kurs_navbat.json"), encoding="utf-8"))
idx = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()


def jonli(slug):
    try:
        return urllib.request.urlopen("https://eduhakimov.github.io/%s/" % slug, timeout=15).status == 200
    except Exception:
        return False


yangi = [k for k in N if "https://eduhakimov.github.io/%s/" % k["slug"] not in idx and jonli(k["slug"])]
if not yangi:
    print("yangi jonli kurs yo'q"); sys.exit(0)
tmp = os.path.join(tempfile.gettempdir(), "kurs_navbat_tmp.json")
json.dump(yangi, io.open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "_manba", "kurs_qosh.py"), tmp], cwd=ROOT, check=True)
fayllar = ["index.html", "i18n/index.js", "_manba/tarjima_en.py", "_manba/tarjima_ru.py", "_manba/tarjima_zh.py"]
subprocess.run(["git", "add"] + fayllar, cwd=ROOT, check=True)
nomlar = ", ".join(k["uz"][0] for k in yangi)
subprocess.run(GIT + ["commit", "-q", "-m", "Interaktiv darsliklar: %s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" % nomlar], cwd=ROOT, check=True)
subprocess.run(["git", "push", "-q"], cwd=ROOT, check=True)
# profil README
subprocess.run(["git", "pull", "-q"], cwd=PROFIL, check=True)
rp = os.path.join(PROFIL, "README.md"); r = io.open(rp, encoding="utf-8").read()
qator = ""
for k in yangi:
    if k["slug"] not in r:
        qator += '\n- Interactive course **"%s"** (%s) — [eduhakimov.github.io/%s](https://eduhakimov.github.io/%s/)' % (k["readme"][0], k["readme"][1], k["slug"], k["slug"])
if qator:
    oxirgi = r.rfind("- Interactive course")
    e = r.index("\n", oxirgi) if "\n" in r[oxirgi:] else len(r)
    r = r[:e] + qator + r[e:]
    io.open(rp, "w", encoding="utf-8").write(r)
    subprocess.run(["git", "add", "README.md"], cwd=PROFIL, check=True)
    subprocess.run(GIT + ["commit", "-q", "-m", "Profile: %s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" % nomlar], cwd=PROFIL, check=True)
    subprocess.run(["git", "push", "-q"], cwd=PROFIL, check=True)
print("QOSHILDI:", " ".join(k["slug"] for k in yangi))
