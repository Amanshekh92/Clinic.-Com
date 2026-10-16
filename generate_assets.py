#!/usr/bin/env python3
"""Generates the ORIGINAL illustrated sample images in assets/images/ (needs: playwright+chromium, Pillow).
Usage: python3 tools/generate_assets.py assets/images
Replace any output file with a real, licensed or clinic-owned photo of the same name and size to upgrade the site."""
import os, io, sys, shutil
from playwright.sync_api import sync_playwright
from PIL import Image
D = sys.argv[1] if len(sys.argv) > 1 else "assets/images"
os.makedirs(D, exist_ok=True)
P = "M32 12C26 6 12 8 10 22c-1 10 4 16 5 28 1 10 4 26 9 26 5 0 5-15 8-20 3 5 3 20 8 20 5 0 8-16 9-26 1-12 6-18 5-28C52 8 38 6 32 12z"
TEAL, DT, NAVY = "#13a3a3", "#0f8f8f", "#0b3a5c"
DEFS = f'''<symbol id="th" viewBox="0 0 64 80"><path d="{P}" fill="#fff" stroke="{DT}" stroke-width="3"/></symbol>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef8fa"/><stop offset="1" stop-color="#d3eaef"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f0f3"/><stop offset="1" stop-color="#c5d9e0"/></linearGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b5e1f6"/><stop offset="1" stop-color="#eaf8fd"/></linearGradient>
<linearGradient id="chair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1fbdb9"/><stop offset="1" stop-color="#0b8a8c"/></linearGradient>
<linearGradient id="glow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3fbfd" stop-opacity="1"/><stop offset=".55" stop-color="#f3fbfd" stop-opacity=".96"/><stop offset="1" stop-color="#f3fbfd" stop-opacity="0"/></linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18aeae"/><stop offset="1" stop-color="#0b7f84"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="ds" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0b3a5c" flood-opacity=".25"/></filter>'''
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{DEFS}</defs>{body}</svg>'
def tooth(x, y, w, fill="#fff", st=DT, sw=3):
    k = w / 64
    return f'<g transform="translate({x} {y}) scale({k})"><path d="{P}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/></g>'
def star(x, y, k=1, c="#f5b400"): return f'<g transform="translate({x} {y}) scale({k})"><path d="M0-8 2-2 8 0 2 2 0 8-2 2-8 0-2-2z" fill="{c}"/></g>'
def person(cx, b, s, skin, hair, shirt, kind, coat=False):
    g = f'<g transform="translate({cx} {b}) scale({s})">'
    if kind in ("f", "kf"): g += f'<ellipse cx="0" cy="-150" rx="37" ry="47" fill="{hair}"/>'
    g += f'<path d="M-62 0L-62 -68Q-62 -106 -26 -113L26 -113Q62 -106 62 -68L62 0Z" fill="{shirt}"/>'
    if coat: g += f'<path d="M-24 -113L0 -68L24 -113Z" fill="{TEAL}"/><path d="M-40 -108Q-47 -58 -22 -50M40 -108Q47 -58 22 -50" stroke="{NAVY}" stroke-width="4" fill="none"/><circle cx="-22" cy="-46" r="7" fill="{NAVY}"/>'
    g += f'<rect x="-11" y="-132" width="22" height="24" fill="{skin}"/><ellipse cx="0" cy="-160" rx="27" ry="31" fill="{skin}"/>'
    if kind in ("m", "km"): g += f'<path d="M-29 -162Q-30 -198 0 -197Q30 -198 29 -162Q16 -180 0 -178Q-16 -180 -29 -162Z" fill="{hair}"/>'
    else: g += f'<path d="M-29 -158Q-31 -196 2 -194Q32 -194 29 -158Q18 -178 2 -176Q-18 -176 -29 -158Z" fill="{hair}"/>'
    g += '<circle cx="-10" cy="-162" r="3.2" fill="#2b1d1a"/><circle cx="10" cy="-162" r="3.2" fill="#2b1d1a"/><path d="M-15 -171Q-10 -174 -5 -171M5 -171Q10 -174 15 -171" stroke="#2b1d1a" stroke-width="2" fill="none"/><circle cx="-18" cy="-150" r="5" fill="#f3a6a0" opacity=".5"/><circle cx="18" cy="-150" r="5" fill="#f3a6a0" opacity=".5"/><path d="M-13 -148Q0 -133 13 -148Z" fill="#fff" stroke="#8a3b3b" stroke-width="2.5" stroke-linejoin="round"/></g>'
    return g
def chair(x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#ds)"><ellipse cx="0" cy="6" rx="150" ry="14" fill="{NAVY}" opacity=".18"/>
<rect x="-14" y="-120" width="28" height="116" fill="#6d8a96"/><ellipse cx="0" cy="-4" rx="92" ry="12" fill="#8fa8b3"/>
<g transform="translate(-112 -130) rotate(22)"><rect x="-80" y="0" width="90" height="22" rx="11" fill="url(#chair)"/></g>
<rect x="-120" y="-152" width="240" height="40" rx="20" fill="url(#chair)"/>
<g transform="translate(78 -140) rotate(32)"><rect x="-24" y="-215" width="48" height="225" rx="24" fill="url(#chair)"/><rect x="-20" y="-262" width="40" height="48" rx="16" fill="#0b8a8c"/></g>
<rect x="-70" y="-190" width="120" height="14" rx="7" fill="{NAVY}" opacity=".75"/></g>'''
def lamp(x, y, s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-170 215L-50 215L60 720L-290 720Z" fill="url(#glow)"/><path d="M0 0V90L-95 170" stroke="#9fb4bf" stroke-width="10" fill="none" stroke-linecap="round"/><ellipse cx="-105" cy="188" rx="72" ry="22" fill="#fff" stroke="#9fb4bf" stroke-width="5"/></g>'
def plant(x, y, s=1):
    leaves = "".join(f'<ellipse cx="0" cy="-90" rx="14" ry="62" fill="{c}" transform="rotate({a} 0 0)"/>' for a, c in [(-38, "#4da58a"), (-14, "#2f8f7a"), (12, "#4da58a"), (36, "#2f8f7a")])
    return f'<g transform="translate({x} {y}) scale({s})">{leaves}<path d="M-34 -40H34L26 0H-26Z" fill="#fff" stroke="#c4d8de" stroke-width="3"/></g>'
def window(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#sky)" stroke="#fff" stroke-width="12"/>'
            f'<circle cx="{x+w*.78}" cy="{y+h*.28}" r="{h*.16}" fill="#fff" opacity=".7" filter="url(#bl)"/><ellipse cx="{x+w*.3}" cy="{y+h*.3}" rx="{w*.12}" ry="{h*.05}" fill="#fff" opacity=".85"/>'
            f'<path d="M{x} {y+h*.82}Q{x+w*.3} {y+h*.6} {x+w*.55} {y+h*.8}T{x+w} {y+h*.76}V{y+h}H{x}Z" fill="#9fd8b4"/><path d="M{x+w/2} {y}V{y+h}M{x} {y+h*.5}H{x+w}" stroke="#fff" stroke-width="8"/>')
def cabinet(x, y, w, h):
    return (f'<g filter="url(#ds)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="#d3e6ec" stroke-width="3"/>'
            f'<path d="M{x} {y+h/2}H{x+w}M{x+w/2} {y}V{y+h}" stroke="#d3e6ec" stroke-width="3"/><rect x="{x+w*.2}" y="{y+h*.2}" width="{w*.1}" height="6" rx="3" fill="#9fb4bf"/><rect x="{x+w*.7}" y="{y+h*.2}" width="{w*.1}" height="6" rx="3" fill="#9fb4bf"/>'
            f'<rect x="{x+w*.2}" y="{y+h*.7}" width="{w*.1}" height="6" rx="3" fill="#9fb4bf"/><rect x="{x+w*.7}" y="{y+h*.7}" width="{w*.1}" height="6" rx="3" fill="#9fb4bf"/></g>'
            f'<rect x="{x+w*.15}" y="{y-34}" width="40" height="34" rx="8" fill="#e8f7f7" stroke="{DT}" stroke-width="3"/><circle cx="{x+w*.7}" cy="{y-20}" r="16" fill="#d9ecff" stroke="#8fb6e6" stroke-width="3"/>')
def room(extra, w=1600, h=900):
    fy = h * .72
    return (f'<rect width="{w}" height="{h}" fill="url(#wall)"/><rect y="{fy}" width="{w}" height="{h-fy}" fill="url(#floor)"/><path d="M0 {fy}H{w}" stroke="#fff" stroke-width="6"/>' + extra)

def hero():
    b = room(window(960, 70, 560, 370) + cabinet(600, 585, 190, 170) + lamp(1230, 0, 1.15) + plant(880, 765, 1.2) + chair(1090, 790, 1.4) + person(1505, 900, 2.7, "#d9a07c", "#2b1d1a", "#fff", "f", True))
    b += '<circle cx="300" cy="260" r="240" fill="#13a3a3" opacity=".08"/><circle cx="120" cy="720" r="160" fill="#0b3a5c" opacity=".05"/><rect width="1060" height="900" fill="url(#fade)"/>'
    return svg(1600, 900, b)
def treat_room():
    return svg(1200, 800, room(window(70, 70, 360, 280) + cabinet(780, 470, 330, 210) + lamp(620, 0, 1) + plant(1110, 700, 1.4) + chair(560, 700, 1.35), 1200, 800))
def reception():
    pend = "".join(f'<path d="M{x} 0V{150+d}" stroke="#9fb4bf" stroke-width="4"/><path d="M{x-46} {190+d}Q{x} {120+d} {x+46} {190+d}Z" fill="{NAVY}"/><ellipse cx="{x}" cy="{192+d}" rx="40" ry="8" fill="#ffe8a8"/>' for x, d in [(420, 20), (600, 0), (780, 20)])
    b = room(pend + f'<circle cx="600" cy="290" r="115" fill="#fff" opacity=".9"/>' + tooth(560, 225, 80, TEAL, "none", 0)
             + '<rect x="40" y="520" width="250" height="40" rx="20" fill="#0f8f8f"/><rect x="40" y="540" width="250" height="110" rx="30" fill="#18a5a5"/><rect x="70" y="650" width="12" height="40" fill="#6d8a96"/><rect x="250" y="650" width="12" height="40" fill="#6d8a96"/>'
             + f'<g filter="url(#ds)"><rect x="330" y="505" width="540" height="195" rx="22" fill="url(#desk)"/><rect x="316" y="486" width="568" height="34" rx="14" fill="#fff"/><rect x="560" y="420" width="90" height="62" rx="8" fill="{NAVY}"/><rect x="598" y="482" width="14" height="10" fill="#6d8a96"/></g>' + plant(1040, 720, 1.5)
             + '<rect x="930" y="250" width="110" height="140" rx="10" fill="#fff" stroke="#c4d8de" stroke-width="5"/><rect x="948" y="268" width="74" height="104" rx="6" fill="#bfe6e6"/>', 1200, 800)
    return svg(1200, 800, b)
def dentist():
    b = '<rect width="800" height="1000" fill="url(#sky)"/><rect width="800" height="1000" fill="#13a3a3" opacity=".12"/><circle cx="130" cy="180" r="120" fill="#fff" opacity=".5" filter="url(#bl)"/><circle cx="690" cy="330" r="150" fill="#fff" opacity=".4" filter="url(#bl)"/><circle cx="640" cy="120" r="70" fill="#fff" opacity=".35" filter="url(#bl)"/>'
    b += f'<rect y="760" width="800" height="240" fill="{NAVY}" opacity=".05"/>' + person(400, 1010, 4.7, "#d9a07c", "#2b1d1a", "#fff", "f", True)
    return svg(800, 1000, b)
def family():
    b = '<rect width="1200" height="800" fill="url(#sky)"/><circle cx="170" cy="150" r="140" fill="#fff" opacity=".6" filter="url(#bl)"/><circle cx="1050" cy="220" r="160" fill="#13a3a3" opacity=".15" filter="url(#bl)"/><path d="M0 560Q300 470 600 540T1200 520V800H0Z" fill="#9fd8b4" opacity=".6"/>'
    b += (person(330, 800, 3.1, "#c98f6e", "#2b1d1a", NAVY, "m") + person(560, 800, 2.9, "#e0ae8a", "#4a2c1f", "#13a3a3", "f") + person(790, 800, 2.1, "#c98f6e", "#2b1d1a", "#f5b400", "km") + person(950, 800, 2.1, "#e0ae8a", "#2b1d1a", "#f08fb0", "kf"))
    return svg(1200, 800, b)
def smile():
    mouth = "M230 350Q600 215 970 350Q900 650 600 665Q300 650 230 350Z"
    up = "".join(f'<rect x="{x}" y="{330+abs(i-3.5)*16}" width="86" height="{150-abs(i-3.5)*8}" rx="30" fill="#fff" stroke="#e3edf0" stroke-width="3"/>' for i, x in enumerate(range(238, 940, 90)))
    lo = "".join(f'<rect x="{x}" y="{520-abs(i-2.5)*6}" width="80" height="120" rx="28" fill="#f7fbfc" stroke="#e3edf0" stroke-width="3"/>' for i, x in enumerate(range(300, 860, 96)))
    b = (f'<rect width="1200" height="800" fill="url(#sky)"/><circle cx="1000" cy="130" r="170" fill="#13a3a3" opacity=".18" filter="url(#bl)"/>'
         f'<defs><clipPath id="m"><path d="{mouth}"/></clipPath></defs><path d="{mouth}" fill="#7a1f2b"/><g clip-path="url(#m)">{up}{lo}</g>'
         f'<path d="M205 352Q600 200 995 352" stroke="#e98a97" stroke-width="46" fill="none" stroke-linecap="round"/><path d="M215 372Q600 700 985 372" stroke="#e98a97" stroke-width="52" fill="none" stroke-linecap="round"/>'
         + star(1010, 210, 3) + star(190, 520, 2) + star(1050, 560, 1.6))
    return svg(1200, 800, b)

ART = {  # 120x72 local art per treatment
 "checkup": f'<use href="#th" x="22" y="4" width="42" height="64"/><circle cx="86" cy="26" r="14" fill="#e8f7fb" stroke="{DT}" stroke-width="4"/><path d="M96 37 108 62" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>',
 "cleaning": '<use href="#th" x="38" y="4" width="44" height="64"/>' + star(24, 18, 1.3) + star(98, 26) + star(90, 58, .8),
 "filling": '<use href="#th" x="38" y="4" width="44" height="64"/><circle cx="60" cy="26" r="6" fill="#f5c76b" stroke="#c99a2e" stroke-width="2"/>',
 "root-canal": '<use href="#th" x="38" y="4" width="44" height="64"/><path d="M54 32v28M66 32v28" stroke="#e5566d" stroke-width="4" stroke-linecap="round"/>',
 "extraction": f'<use href="#th" x="26" y="10" width="40" height="60"/><path d="M96 56V14M86 24l10-10 10 10" stroke="{NAVY}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
 "implants": '<use href="#th" x="38" y="0" width="44" height="36"/><rect x="55" y="38" width="10" height="30" rx="3" fill="#8aa0ad"/><path d="M52 46h16M52 54h16M52 62h16" stroke="#5d7685" stroke-width="3"/>',
 "braces-aligners": f'<g fill="#fff" stroke="{DT}" stroke-width="3"><rect x="10" y="12" width="22" height="42" rx="10"/><rect x="35" y="12" width="22" height="42" rx="10"/><rect x="60" y="12" width="22" height="42" rx="10"/><rect x="85" y="12" width="22" height="42" rx="10"/></g><path d="M8 33H110" stroke="{NAVY}" stroke-width="3"/><g fill="#e5566d"><rect x="16" y="28" width="10" height="10" rx="2"/><rect x="41" y="28" width="10" height="10" rx="2"/><rect x="66" y="28" width="10" height="10" rx="2"/><rect x="91" y="28" width="10" height="10" rx="2"/></g>',
 "whitening": '<use href="#th" x="38" y="4" width="44" height="64"/>' + star(28, 16, 1.4) + star(96, 22, 1.1) + star(94, 58, .8),
 "kids": '<use href="#th" x="40" y="6" width="40" height="60"/><circle cx="53" cy="32" r="2.5" fill="#0b3a5c"/><circle cx="67" cy="32" r="2.5" fill="#0b3a5c"/><path d="M52 42Q60 50 68 42" stroke="#0b3a5c" stroke-width="3" fill="none" stroke-linecap="round"/>' + star(22, 22, 1.2) + star(100, 18, .9),
 "cosmetic": '<use href="#th" x="40" y="14" width="40" height="56"/><path d="M44 16L50 4L60 12L70 4L76 16Z" fill="#f5b400" stroke="#c99a2e" stroke-width="2" stroke-linejoin="round"/>' + star(22, 24, 1.3) + star(100, 20, 1) + star(96, 56, .8),
 "gum-care": f'<g fill="#fff" stroke="{DT}" stroke-width="3"><rect x="20" y="8" width="20" height="38" rx="9"/><rect x="42" y="4" width="20" height="42" rx="9"/><rect x="64" y="4" width="20" height="42" rx="9"/><rect x="86" y="8" width="14" height="38" rx="7"/></g><path d="M10 44Q60 30 110 44V70H10Z" fill="#f08fa4"/><path d="M10 44Q60 30 110 44" stroke="#d96b86" stroke-width="3" fill="none"/>',
}
CAT = {"checkup": 0, "cleaning": 0, "filling": 0, "root-canal": 1, "extraction": 1, "implants": 1, "braces-aligners": 2, "whitening": 2, "cosmetic": 2, "kids": 3, "gum-care": 0}
COL = [("#d9f1f2", "#9fd9dc"), ("#dde8f7", "#a9c3ec"), ("#f6e3f1", "#e2b6d4"), ("#e3f5e0", "#b2e0a8")]
def treat(name):
    a, c = COL[CAT[name]]
    return svg(600, 400, f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{c}"/></linearGradient></defs><rect width="600" height="400" fill="url(#g)"/><circle cx="500" cy="60" r="130" fill="#fff" opacity=".35"/><circle cx="70" cy="360" r="110" fill="#fff" opacity=".3"/><g transform="translate(120 92) scale(3)" filter="url(#ds)">{ART[name]}</g>')
def bg_soft():
    return svg(1200, 600, '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3f6f6"/><stop offset="1" stop-color="#f7fcfd"/></linearGradient></defs><rect width="1200" height="600" fill="url(#g)"/><circle cx="1050" cy="80" r="260" fill="#13a3a3" opacity=".10"/><circle cx="120" cy="560" r="220" fill="#0b3a5c" opacity=".05"/>' + "".join(tooth(80 + i * 190, 40 + (i % 2) * 330, 44, "#fff", "#bfe3e3", 3) for i in range(7)))
def bg_navy():
    return svg(1200, 600, f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b2545"/><stop offset="1" stop-color="#0d4a6b"/></linearGradient></defs><rect width="1200" height="600" fill="url(#g)"/><circle cx="1080" cy="520" r="280" fill="#13a3a3" opacity=".22"/><circle cx="90" cy="60" r="200" fill="#13a3a3" opacity=".12"/>' + "".join(tooth(60 + i * 200, 60 + (i % 3) * 190, 34, "#ffffff10", "#ffffff22", 2) for i in range(7)))
ICO = {
 "consultation": '<rect x="30" y="26" width="36" height="46" rx="6"/><rect x="40" y="20" width="16" height="10" rx="3"/><path d="M38 44h20M38 54h20M38 64h12"/>',
 "clear-advice": '<path d="M28 30h40a6 6 0 0 1 6 6v22a6 6 0 0 1-6 6H48l-12 10V64h-8a6 6 0 0 1-6-6V36a6 6 0 0 1 6-6z"/><path d="M38 48l7 7 13-14"/>',
 "easy-booking": '<rect x="26" y="30" width="44" height="40" rx="6"/><path d="M26 44h44M38 24v10M58 24v10M38 58l7 6 12-12"/>',
 "questions": '<circle cx="48" cy="48" r="22"/><path d="M42 42a6 6 0 1 1 9 5c-3 2-3 4-3 6"/><circle cx="48" cy="62" r="2.5" fill="#0f8f8f"/>'}
def write_svg(name, s): open(os.path.join(D, name), "w").write(s)
for k, v in ICO.items():
    write_svg(f"icon-{k}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96"><circle cx="48" cy="48" r="48" fill="#dff8f3"/><g fill="none" stroke="{DT}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{v}</g></svg>')
MARK = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#13a3a3"/><stop offset="1" stop-color="#0b3a5c"/></linearGradient></defs><rect width="80" height="80" rx="20" fill="url(#g)"/><g transform="translate(16 12) scale(.75)"><path d="{P}" fill="#fff"/></g></svg>'
write_svg("logo-mark.svg", MARK)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page()
    def shot(s, w, h, transparent=False):
        pg.set_viewport_size({"width": w, "height": h}); pg.set_content(f'<body style="margin:0;background:transparent">{s}</body>')
        return Image.open(io.BytesIO(pg.screenshot(omit_background=transparent))).convert("RGBA" if transparent else "RGB")
    def save(name, im, q=80):
        path = os.path.join(D, name)
        if name.endswith(".webp"): im.save(path, "WEBP", quality=q, method=6)
        elif name.endswith(".jpg"): im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        else: im.save(path, optimize=True)
    h = shot(hero(), 1600, 900); save("hero-dental-clinic.webp", h, 82); save("hero-dental-clinic-mobile.webp", h.resize((800, 450), Image.LANCZOS), 80)
    save("og-image.jpg", h.crop((400, 135, 1600, 765)), 82)
    # clinic-*.webp are REAL photos from the clinic's Google Maps listing (see SOURCES.md); not generated here
    save("dentist-portrait.webp", shot(dentist(), 800, 1000)); save("family-smile.webp", shot(family(), 1200, 800)); save("smile-closeup.webp", shot(smile(), 1200, 800))
    for n in ART: save(f"treatment-{n}.webp", shot(treat(n), 600, 400), 78)
    save("bg-soft-teal.webp", shot(bg_soft(), 1200, 600), 70); save("bg-navy-pattern.webp", shot(bg_navy(), 1200, 600), 70)
    save("logo-512.png", shot(MARK.replace('width="80" height="80"', 'width="512" height="512"'), 512, 512, True))
    save("logo-192.png", shot(MARK.replace('width="80" height="80"', 'width="192" height="192"'), 192, 192, True))
    save("apple-touch-icon.png", shot(MARK.replace('width="80" height="80"', 'width="180" height="180"').replace('rx="20"', 'rx="0"'), 180, 180))
    br.close()
print("done")
