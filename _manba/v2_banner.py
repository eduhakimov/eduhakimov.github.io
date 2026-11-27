# -*- coding: utf-8 -*-
"""Bosh sahifadagi "Ilmiy ishlar" bo'limi: barcha maqolalar aylanib turadigan keng banner (karusel).
Maqolalar ilmiy-ishlar/index.html dan olinadi (to'liq ro'yxat o'sha sahifada). Qayta ishga tushirsa xavfsiz."""
import io, os, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import importlib.util
_sp = importlib.util.spec_from_file_location("ik", os.path.join(ROOT, "_manba", "v2_ikonlar.py"))
ik = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ik)
src = io.open(os.path.join(ROOT, "ilmiy-ishlar", "index.html"), encoding="utf-8").read()

slides = []
for blok_key in ("ilm.h.2026", "ilm.h.2024"):
    i = src.index('data-i18n="%s"' % blok_key); j = src.index("</ol>", i)
    for li in re.findall(r"<li>(.*?)</li>", src[i:j], flags=re.S):
        t = re.search(r'<span class="t">(.*?)</span>', li).group(1)
        a = re.search(r'<span class="a">(.*?)</span>', li).group(1)
        jr = re.search(r'<span class="j">(.*?)</span>', li).group(1)
        doi = re.search(r'<a href="(https://doi\.org/[^"]+)">DOI: ([^<]+)</a>', li)
        page = re.search(r'<a href="([^"]+)" data-i18n="journal">', li)
        href = doi.group(1) if doi else (page.group(1) if page else "ilmiy-ishlar/")
        yil = (re.search(r"(20\d\d)", jr) or [None, ""])[1]
        slides.append((t, a, jr, href, doi.group(2) if doi else "", yil))

OQ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'
CH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>'
CR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>'
n = len(slides)
items = []
for k, (t, a, jr, href, doi, yil) in enumerate(slides):
    items.append(
        '<article class="bn-s%s" aria-roledescription="slide" aria-label="%d / %d">'
        '<div class="bn-yil">%s</div>'
        '<div class="bn-m"><span class="bn-k"><span data-i18n="idx.bn.art">Ilmiy maqola</span> · %02d/%02d</span>'
        '<h3>%s</h3><p class="bn-a">%s</p><p class="bn-j">%s</p>'
        '<div class="bn-f">%s<a class="btn bn-open" href="%s"><span data-i18n="idx.bn.open">Maqolani ochish</span>%s</a></div></div>'
        '</article>' % (" on" if k == 0 else "", k + 1, n, yil, k + 1, n, t, a, jr,
                         ('<span class="bn-doi">DOI: %s</span>' % doi) if doi else "", href, OQ))
BANNER = ('<!--BANNER_BOSHI--><div class="bn" id="bn" aria-roledescription="carousel" tabindex="0">'
          '<div class="bn-t">' + "".join(items) + '</div>'
          '<button type="button" class="bn-o bn-l" aria-label="Oldingi">' + CH + '</button>'
          '<button type="button" class="bn-o bn-r" aria-label="Keyingi">' + CR + '</button>'
          '<div class="bn-ft"><span class="bn-st" data-i18n="idx.bn.st">47 ta maqola va tezis · 1 ta o\'quv qo\'llanma · 6 ta guvohnoma</span>'
          '<span class="bn-ln"><a class="bn-all" href="ilmiy-ishlar/"><span data-i18n="idx.pb.all">Barcha ilmiy ishlar</span><b class="cnt">54</b>' + OQ + '</a>'
          '<a class="bn-ic" href="https://orcid.org/0009-0001-7222-3508" title="ORCID" style="--b:#A6CE39">' + ik.svg("orcid") + '</a>'
          '<a class="bn-ic" href="https://scholar.google.com/citations?user=kTUbDqIAAAAJ" title="Google Scholar" style="--b:#4285F4">' + ik.svg("googlescholar") + '</a></span></div>'
          '<div class="bn-bar"><i></i></div></div>'
          '<script>(function(){var b=document.getElementById("bn");if(!b)return;var s=b.querySelectorAll("article"),i=0,t,bar=b.querySelector(".bn-bar i"),'
          'rm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches,D=7000;'
          'function go(k){s[i].classList.remove("on");i=(k+s.length)%s.length;s[i].classList.add("on");if(bar){bar.style.transition="none";bar.style.width="0";'
          'void bar.offsetWidth;if(!rm){bar.style.transition="width "+D+"ms linear";bar.style.width="100%"}}}'
          'function play(){stop();if(!rm)t=setInterval(function(){go(i+1)},D);go(i)}function stop(){clearInterval(t)}'
          'b.querySelector(".bn-l").onclick=function(){go(i-1);play()};b.querySelector(".bn-r").onclick=function(){go(i+1);play()};'
          'b.addEventListener("mouseenter",function(){stop();if(bar){bar.style.transition="none"}});b.addEventListener("mouseleave",play);'
          'b.addEventListener("keydown",function(e){if(e.key==="ArrowLeft"){go(i-1);play()}if(e.key==="ArrowRight"){go(i+1);play()}});'
          'var x0=null;b.addEventListener("touchstart",function(e){x0=e.touches[0].clientX},{passive:true});'
          'b.addEventListener("touchend",function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40){go(i+(dx<0?1:-1));play()}x0=null});'
          'play()})();</script><!--BANNER_OXIRI-->')

if __name__ == "__main__":
    P = os.path.join(ROOT, "index.html")
    s = io.open(P, encoding="utf-8").read()
    i = s.index('<section class="sec" id="nashrlar">'); j = s.index("</section>", i)
    sec = s[i:j]
    if "<!--BANNER_BOSHI-->" in sec:
        sec = re.sub(r"<!--BANNER_BOSHI-->.*?<!--BANNER_OXIRI-->", lambda m: BANNER, sec, flags=re.S)
    else:
        sec = re.sub(r'<div class="pubs">.*?</div>\n<div class="pubn">.*?</div>\n', lambda m: BANNER + "\n", sec, count=1, flags=re.S)
    assert "<!--BANNER_BOSHI-->" in sec
    sec = re.sub(r'\n?<div class="btns" style="margin-top:18px">.*?</div>\n', "\n", sec, count=1, flags=re.S)
    s = s[:i] + sec + s[j:]
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
    print("ok", n, "ta maqola")
