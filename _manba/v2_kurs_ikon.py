# -*- coding: utf-8 -*-
"""index.html kurs kartochkalaridagi emojilarni chiziqli SVG belgilarga almashtiradi (saytda emoji ishlatilmaydi).
Yangi kurs qo'shilganda KURS ga slug -> belgi yozing va qayta ishga tushiring."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
KURS = {
    "savodxonlik": '<rect x="2.5" y="4" width="19" height="12.5" rx="2"/><path d="M8 20.5h8M12 16.5v4"/>',
    "grafika": '<path d="M12 3 5 10l3.5 9h7L19 10z"/><circle cx="12" cy="11" r="1.6"/><path d="M12 3v6.4M8.5 19h7"/>',
    "animatsiya": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9h19M2.5 15h19M7 5v4M12 5v4M17 5v4M7 15v4M12 15v4M17 15v4"/>',
    "dasturlash": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "raqamli-texnologiyalar": '<path d="M3 21h18"/><rect x="5" y="11" width="3" height="7" rx=".6"/><rect x="10.5" y="6" width="3" height="12" rx=".6"/><rect x="16" y="13" width="3" height="5" rx=".6"/>',
    "algoritmlar": '<rect x="9" y="2.5" width="6" height="4.5" rx="1"/><rect x="2.5" y="17" width="6" height="4.5" rx="1"/><rect x="15.5" y="17" width="6" height="4.5" rx="1"/><path d="M12 7v4.5M5.5 17v-2.5a1 1 0 0 1 1-1h11a1 1 0 0 1 1 1V17"/>',
    "iqtisodiyotda-akt": '<path d="M3 3v18h18"/><path d="m6.5 15 4-4.5 3 3L20 7"/><path d="M15.5 7H20v4.5"/>',
    "malumotlar-bazasi": '<ellipse cx="12" cy="5.5" rx="7.5" ry="3"/><path d="M4.5 5.5v13c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-13M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>',
    "veb-dasturlash": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
    "tarmoqlar": '<rect x="9" y="2.5" width="6" height="5" rx="1"/><rect x="2.5" y="16.5" width="6" height="5" rx="1"/><rect x="15.5" y="16.5" width="6" height="5" rx="1"/><path d="M12 7.5V12M5.5 16.5V12h13v4.5"/>',
    "kompyuter-tashkil-etish": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6" rx=".8"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "operatsion-tizimlar": '<rect x="2.5" y="3.5" width="19" height="15" rx="2"/><path d="M2.5 7.5h19M6 5.5h.01M8.5 5.5h.01M8 21h8"/>',
    "oyd": '<path d="M12 3 2 8l10 5 10-5-10-5z"/><path d="M6 10.5V16c0 1.4 2.7 3 6 3s6-1.6 6-3v-5.5M22 8v6"/>',
    "mashinali-oqitish": '<circle cx="12" cy="12" r="2.5"/><circle cx="4.5" cy="5" r="1.8"/><circle cx="19.5" cy="5" r="1.8"/><circle cx="4.5" cy="19" r="1.8"/><circle cx="19.5" cy="19" r="1.8"/><path d="m6 6.4 4.2 4M18 6.4l-4.2 4M6 17.6l4.2-4M18 17.6l-4.2-4"/>',
    "_tez": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}

if __name__ == "__main__":
    P = os.path.join(ROOT, "index.html")
    s = io.open(P, encoding="utf-8").read()

    def kart(m):
        a = m.group(0)
        h = re.search(r'href="https://eduhakimov\.github\.io/([^/"]+)/"', a)
        k = h.group(1) if h else ("_tez" if "kc-tez" in a else None)
        if k not in KURS:
            raise SystemExit("belgi yo'q: %s" % k)
        return re.sub(r'<span class="ki">.*?</span>', '<span class="ki">%s</span>' % (S % KURS[k]), a, count=1)

    # faqat "Interaktiv darsliklar" bo'limi (Ingliz tili bo'limidagi kartochkalarning o'z belgilari bor)
    i = s.index('<section class="sec" id="darsliklar">'); j = s.index("</section>", i)
    s = s[:i] + re.sub(r'<(?:a|div) class="kc[^"]*".*?<span class="ki">.*?</span>', kart, s[i:j], flags=re.S) + s[j:]
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
    print("ok")
