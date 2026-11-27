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
    "biznes-jarayonlari": '<rect x="3" y="4" width="6" height="5" rx="1"/><rect x="15" y="4" width="6" height="5" rx="1"/><rect x="9" y="15" width="6" height="5" rx="1"/><path d="M9 6.5h6M6 9v3.5h6V15M18 9v3.5h-6"/>',
    "innovatsiya-loyiha": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    "parallel-hisoblash": '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="M9 9v6M12 8v8M15 9v6"/>',
    "data-mining": '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v6c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-6"/><circle cx="17" cy="17" r="3"/><path d="m19.2 19.2 2.3 2.3"/>',
    "bulutli-texnologiyalar": '<path d="M7 18h10.5a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.3 9.6 4.2 4.2 0 0 0 7 18z"/>',
    "at-loyihalash": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9M13 13h5M13 17h3"/>',
    "cms-tizimlari": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 13h4M7 16h6M15 13h2v3h-2z"/>',
    "mikrokontroller": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 3v3M12 3v3M15 3v3M9 18v3M12 18v3M15 18v3M3 9h3M3 12h3M3 15h3M18 9h3M18 12h3M18 15h3"/><circle cx="12" cy="12" r="2"/>',
    "tarmoq-boshqaruvi": '<rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="14" width="18" height="7" rx="1.5"/><path d="M7 6.5h.01M7 17.5h.01M11 6.5h6M11 17.5h6"/>',
    "texnik-tizimlarda-at": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9 7 7M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "texnik-vositalar": '<rect x="2.5" y="5" width="13" height="9" rx="1.5"/><path d="M6 18h6M9 14v4"/><rect x="17.5" y="7" width="4" height="12" rx="1"/>',
    "texnik-xizmat": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "sunniy-intellekt": '<rect x="5" y="7" width="14" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9.5 15.5h5M2 12h3M19 12h3"/>',
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
