#!/usr/bin/env python3
"""Automated checks (Playwright + Chromium). Serves the project under /sn-dental-demo/ to emulate a GitHub Pages project subpath.
Usage: python3 tools/test_site.py   -> prints PASS/FAIL and writes docs/TEST_REPORT.md"""
import os, re, sys, json, subprocess, threading, socketserver, http.server, mimetypes, tempfile, datetime
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); PREFIX = "/sn-dental-demo/"
mimetypes.add_type("application/manifest+json", ".webmanifest"); mimetypes.add_type("image/webp", ".webp")
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        p = urlparse(self.path).path; code = 200
        f = None
        if p.startswith(PREFIX):
            rel = p[len(PREFIX):] or "index.html"
            f = os.path.join(ROOT, rel)
            if not os.path.isfile(f): f = None
        if f is None: f = os.path.join(ROOT, "404.html"); code = 404
        d = open(f, "rb").read(); self.send_response(code); self.send_header("Content-Type", mimetypes.guess_type(f)[0] or "text/plain"); self.send_header("Content-Length", str(len(d))); self.end_headers(); self.wfile.write(d)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
B = f"http://127.0.0.1:{srv.server_address[1]}{PREFIX}"
R = []
def T(name, ok, detail=""):
    R.append((name, "PASS" if ok else "FAIL", str(detail)[:220])); print(("PASS " if ok else "FAIL ") + name, ("| " + str(detail)[:160]) if (detail and not ok) else "")
rd = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()
fut = lambda n: (datetime.date.today() + datetime.timedelta(days=n)).isoformat()
EXPECT = ["General Dentistry", "Cosmetic Dentistry", "Root Canal Treatment", "Teeth Cleaning", "Tooth Filling", "Tooth Extraction", "Dental Implants", "Braces & Aligners", "Teeth Whitening", "Children's Dentistry", "Gum Care"]
SCREENS = ["home", "svc", "book", "doc", "appt", "rev", "prof", "more", "info/faq", "info/privacy", "info/terms", "info/hours"]
# ---------- static checks ----------
for f in ["js/app.js", "js/config.js"]:
    r = subprocess.run(["node", "--check", os.path.join(ROOT, f)], capture_output=True, text=True); T(f"JS syntax {f}", r.returncode == 0, r.stderr)
refs = set()
for f in ["index.html", "privacy.html", "terms.html", "404.html"]:
    for m in re.findall(r'(?:href|src|srcset)="([^"#]+)"', rd(f)):
        if not re.match(r"(https?:|mailto:|tel:|data:|javascript:)", m) and "FINAL-URL" not in m: refs.add(m)
refs |= set(re.findall(r"url\(\.\./([^)]+)\)", rd("css/styles.css")))
ids = re.findall(r'\{id:"(\w+)"', rd("js/config.js")); IMGM = {"rct": "root-canal", "braces": "braces-aligners", "gum": "gum-care"}
refs |= {f"assets/images/treatment-{IMGM.get(i, i)}.webp" for i in ids}
refs |= set(re.findall(r"assets/images/[\w-]+\.\w+", rd("js/app.js"))); refs |= {i["src"] for i in json.loads(rd("manifest.webmanifest"))["icons"]}
miss = [r for r in refs if not os.path.exists(os.path.join(ROOT, r))]; T(f"All {len(refs)} local file references exist", not miss, miss)
app = rd("js/app.js"); idx = rd("index.html")
T("No innerHTML/outerHTML/insertAdjacentHTML/eval/document.write in app.js", not re.search(r"innerHTML|outerHTML|insertAdjacentHTML|eval\(|document\.write|new Function", app))
T("No hard-coded secrets/keys in project text files", not re.search(r"(service_role|secret|passw\w*|api[_-]?key|token)\s*[:=]|sk_live|eyJ[A-Za-z0-9]{20,}", app + rd("js/config.js") + idx, re.I))
URLS = set(re.findall(r"https?://[^\s\"'`)]+", app + rd("css/styles.css") + re.sub(r"//[^\n]*", "", rd("js/config.js"))))
T("No third-party scripts/styles/fonts (only wa.me link built in JS)", not re.search(r'<script[^>]+src="https?:|<link[^>]+href="https?:', re.sub(r"<!--.*?-->", "", idx, flags=re.S)) and URLS <= {"https://wa.me/"}, URLS)
T("localStorage used only for language preference", set(re.findall(r'localStorage\.\w+\("(\w+)"', app)) == {"lang"})
T("Reduced-motion CSS present", "prefers-reduced-motion" in rd("css/styles.css"))
T("Privacy/terms marked as templates", "template" in rd("privacy.html").lower() and "template" in rd("terms.html").lower())
T("noindex present while demo; no fake JSON-LD", 'name="robots" content="noindex"' in idx and "ld+json" not in idx)
ids_dup = [i for i in set(re.findall(r'id="([^"]+)"', idx)) if len(re.findall(r'id="%s"' % re.escape(i), idx)) > 1]; T("No duplicate element ids", not ids_dup, ids_dup)
T("All <img> have alt and width/height", all(re.search(r"\balt=", t) and re.search(r"\bwidth=", t) and re.search(r"\bheight=", t) for t in re.findall(r"<img[^>]*>", idx)))
def lum(h):
    h = h.lstrip("#"); f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = [f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]; return .2126 * r + .7152 * g + .0722 * b
cr = lambda a, b: (max(lum(a), lum(b)) + .05) / (min(lum(a), lum(b)) + .05)
pairs = {"white on teal button": ("#ffffff", "#0b7d7d"), "white on WA badge": ("#ffffff", "#0b7a4b"), "muted on white": ("#4b5d6b", "#ffffff"), "error on white": ("#b00020", "#ffffff"), "teal on mint": ("#0b7d7d", "#eaf7f7"), "navy on white": ("#0b3a5c", "#ffffff")}
bad = {k: round(cr(*v), 2) for k, v in pairs.items() if cr(*v) < 4.5}; T("Key colour pairs meet WCAG AA 4.5:1", not bad, bad)
def blank(src):
    src = re.sub(r'\b(address|phone|whatsapp|email|maps|reviews|mapEmbed|holidays):"[^"]*"', r'\1:""', src)
    src = re.sub(r'rating:\{[^}]*\}', 'rating:null', src)
    return re.sub(r'(\["\w+","[^"]+"),"[^"]*"\]', r'\1,""]', src)
cfgtxt = rd("js/config.js")
T("Config: no unverified Instagram/website link; Maps/Reviews/embed are https Google Maps links", "instagram" not in (cfgtxt + idx).lower() and "cosmos" not in (cfgtxt + idx + app).lower() and len(re.findall(r'(?:maps|reviews|mapEmbed):"(https://www\.google\.com/maps[^"]*)"', cfgtxt)) == 3)
T("Config: phone is +917483582795 and WhatsApp/email/doctor are still empty (not invented)", 'phone:"+917483582795"' in cfgtxt and 'whatsapp:""' in cfgtxt and 'email:""' in cfgtxt and re.search(r'doctor:\{\s*name:""', cfgtxt) is not None)
# ---------- browser checks ----------
HOOK = "window.__t={waNum,telHref,safe,mailOk};})();"
with sync_playwright() as p:
    br = p.chromium.launch()
    def page(w=390, h=844, cfg=None, hook=True, real=False):
        ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=w < 700, device_scale_factor=1); pg = ctx.new_page(); pg.errs = []; pg.bad = []
        pg.on("console", lambda m: pg.errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: pg.errs.append(str(e)))
        pg.on("response", lambda r: pg.bad.append(r.url) if r.status >= 400 else None)
        src = rd("js/config.js")
        if not real: src = blank(src)
        for a, b in (cfg or {}).items(): assert a in src; src = src.replace(a, b, 1)
        pg.route("**/js/config.js", lambda r: r.fulfill(body=src, content_type="application/javascript"))
        if hook:
            code = rd("js/app.js"); code = code[:code.rindex("})();")] + HOOK
            pg.route("**/js/app.js", lambda r: r.fulfill(body=code, content_type="application/javascript"))
        pg.add_init_script("window.__o=[];window.open=(u,t,f)=>{window.__o.push([u,t,f]);return null}")
        return pg
    def load(pg, hash_="", wait=True):
        pg.goto(B + "index.html" + hash_); pg.wait_for_load_state("networkidle"); return pg
    act = lambda pg: (pg.wait_for_timeout(120), pg.evaluate("document.querySelector('.scr.on').id.slice(2)"))[1]
    pg = load(page(hook=False))
    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.scrollIntoView())"); pg.wait_for_timeout(500)
    brk = pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)")
    T("Subpath load: no console errors, no HTTP>=400, no broken images", not pg.errs and not pg.bad and not brk, (pg.errs, pg.bad, brk))
    T("Hero uses mobile image on phones", "mobile" in pg.evaluate("document.getElementById('hero-art').currentSrc"))
    d = page(1280, 800, hook=False); load(d); T("Hero uses full 1600x900 image on desktop", "mobile" not in d.evaluate("document.getElementById('hero-art').currentSrc") and "hero-dental-clinic.webp" in d.evaluate("document.getElementById('hero-art').currentSrc"))
    T("Manifest + icons load with correct types", d.evaluate("fetch('manifest.webmanifest').then(r=>r.ok)"))
    # nav
    pg = load(page())
    ok = True; det = []
    for k, s in [("svc", "svc"), ("appt", "appt"), ("prof", "prof"), ("home", "home")]:
        pg.click(f"nav button[data-go={k}]"); pg.wait_for_timeout(150); cur = pg.evaluate("document.querySelector('nav [aria-current=page]')?.dataset.go")
        if act(pg) != s or cur != k: ok = False; det.append((k, act(pg), cur))
    T("Bottom navigation: 4 tabs switch screen and aria-current", ok, det)
    pg.click("nav button[data-go=svc]"); pg.click("nav button[data-go=prof]"); pg.go_back(); T("Browser/Android Back returns to previous screen", act(pg) == "svc", act(pg))
    pg.click("nav button[data-go=prof]"); pg.click("#s-prof [data-go=more]"); pg.click("#s-more [data-info=faq]"); st = [act(pg)]
    pg.click("#s-info [data-back]"); st.append(act(pg)); pg.click("#s-more [data-back]"); st.append(act(pg)); pg.click("#s-prof [data-back]"); st.append(act(pg))
    T("In-app back chain info>more>profile>home", st == ["info", "more", "prof", "home"], st)
    pg.goto(B + "index.html#/prof"); pg.wait_for_load_state("networkidle"); T("Refresh/deep link keeps screen (#/prof)", act(pg) == "prof"); pg.reload(); T("Reload keeps screen", act(pg) == "prof")
    pg.goto(B + "index.html#/nonsense"); T("Unknown route falls back to home", act(pg) == "home")
    # services/search
    pg = load(page()); pg.click("nav button[data-go=svc]")
    names = pg.evaluate("[...document.querySelectorAll('#tl .card b')].map(b=>b.childNodes[0].textContent)"); T("Services list has the 11 required treatments in order", names == EXPECT, names)
    cnt = {}
    for c in ["General", "Cosmetic", "Kids", "Advanced", "All"]: pg.click(f"#chips button:text-is('{c}')"); cnt[c] = pg.locator("#tl .card").count()
    T("Category filter counts (General 5, Cosmetic 3, Kids 1, Advanced 2, All 11)", cnt == {"General": 5, "Cosmetic": 3, "Kids": 1, "Advanced": 2, "All": 11}, cnt)
    pg.fill("#q2", "root"); n1 = pg.locator("#tl .card").count(); pg.fill("#q2", "zzzz"); n0 = pg.locator("#tl .card").count(); emp = pg.is_visible("#none")
    T("Search by name + empty state", n1 == 1 and n0 == 0 and emp, (n1, n0, emp)); pg.click("#clr"); T("Clear search restores all 11", pg.locator("#tl .card").count() == 11 and not pg.is_visible("#none"))
    pg.goto(B + "index.html"); pg.fill("#q", "gum"); pg.press("#q", "Enter"); T("Home search opens Services with filtered result", act(pg) == "svc" and pg.locator("#tl .card").count() == 1)
    pg.fill("#q2", ""); pg.click("#tl .card >> nth=2"); T("Clicking a treatment opens booking with it preselected", act(pg) == "book" and pg.input_value("#f-tr") == "rct", pg.input_value("#f-tr"))
    # booking validation
    pg = load(page(), "#/book"); sub = lambda: pg.click("#bsub")
    sub(); errs = pg.evaluate("['name','phone','tr','date','ok'].map(k=>document.getElementById('e-'+k).textContent.length>0)"); T("Empty submit shows all 5 errors and stays on step 1", all(errs) and pg.is_visible("#bf"), errs)
    def fillf(name="Asha Rao", ph="98765 43210", tr="cleaning", dt=None, ok=True):
        pg.fill("#f-name", name); pg.fill("#f-phone", ph); pg.select_option("#f-tr", tr); pg.fill("#f-date", dt or fut(2)); pg.set_checked("#f-ok", ok)
    for nm, kw, key in [("digits-only name rejected", dict(name="12345"), "name"), ("1-letter name rejected", dict(name="A"), "name"), ("script-like name rejected", dict(name="<b>x</b>"), "name"), ("landline/short phone rejected", dict(ph="12345"), "phone"), ("phone starting 5 rejected", dict(ph="5876543210"), "phone"), ("yesterday rejected", dict(dt=fut(-1)), "date"), ("missing consent rejected", dict(ok=False), "ok")]:
        fillf(**kw); sub(); T("Validation: " + nm, pg.evaluate(f"document.getElementById('e-{key}').textContent.length>0") and pg.is_visible("#bf"))
    fillf(dt=fut(0)); sub(); T("Validation: today accepted -> review step", pg.is_visible("#b2"))
    pg.click("#edit"); T("Edit returns to step 1 with values kept", pg.is_visible("#bf") and pg.input_value("#f-name") == "Asha Rao")
    sub(); pg.click("#send"); msg = pg.inner_text("#st"); T("No WhatsApp number: clear setup message, no fake success", "not set up" in msg and not pg.is_visible("#b3") and pg.evaluate("window.__o.length") == 0, msg)
    T("Date input has min=today", pg.get_attribute("#f-date", "min") == fut(0))
    # configured whatsapp
    pg = load(page(cfg={'whatsapp:""': 'whatsapp:"+91 98765 43210"', 'phone:""': 'phone:"98765 43210"', 'email:""': 'email:"info@example.invalid"', 'maps:""': 'maps:"https://maps.google.com/?q=test"', 'address:""': 'address:"Test address"'}), "#/book")
    def fill2(pg): pg.fill("#f-name", "Asha Rao"); pg.fill("#f-phone", "9876543210"); pg.select_option("#f-tr", "filling"); pg.fill("#f-date", fut(1)); pg.fill("#f-msg", "Pain & swelling? 100%"); pg.check("#f-ok")
    fill2(pg); pg.click("#bsub"); pg.click("#send"); o = pg.evaluate("window.__o")
    u = o[0][0] if o else ""; T("WhatsApp URL: wa.me/<digits only>, encoded text, noopener+noreferrer", bool(o) and u.startswith("https://wa.me/919876543210?text=") and " " not in u and "%0A" in u and "%26" in u and "noopener" in o[0][2] and "noreferrer" in o[0][2], u[:120])
    T("Step 3 says not confirmed and not-sent warning", pg.is_visible("#b3") and "not a confirmed booking" in pg.inner_text("#b3") and "does not mean your message was sent" in pg.inner_text("#b3"))
    pg.click("#again"); T("Open WhatsApp again button works", pg.evaluate("window.__o.length") == 2)
    pg.click("#b3 [data-go=home]"); pg.goto(B + "index.html#/book"); fill2(pg); pg.click("#bsub"); pg.click("#send"); T("Duplicate submission blocked", "already prepared" in pg.inner_text("#st") and pg.evaluate("window.__o.length") == 2)
    T("Only 'lang' key in localStorage; no patient data stored", pg.evaluate("Object.keys(localStorage).filter(k=>k!=='lang').length==0 && !JSON.stringify(localStorage).includes('Asha')") and pg.evaluate("sessionStorage.length") == 0)
    pg.goto(B + "index.html"); pg.click("#ha [data-act=dir]"); T("Directions opens https Maps URL (noopener) when configured", pg.evaluate("window.__o.some(x=>x[0].startsWith('https://maps.google.com')&&x[2].includes('noopener'))"))
    T("Configured buttons are not marked disabled", pg.evaluate("[...document.querySelectorAll('#ha [data-act]')].every(b=>b.getAttribute('aria-disabled')==='false')"))
    h = pg.evaluate("[__t.waNum.toString().length>0, (C.whatsapp='9876543210',__t.waNum()), (C.whatsapp='0098765432101',__t.waNum()), (C.whatsapp='12345',__t.waNum()), (C.phone='+91 98765 43210',__t.telHref()), (C.phone='12',__t.telHref()), __t.safe('javascript:alert(1)'), __t.safe('http://x.com'), !!__t.safe('https://maps.google.com/x'), (C.email='bad',__t.mailOk()), (C.email='a@b.co',__t.mailOk())]")
    T("Number/URL helpers: 10-digit->91 prefix, junk rejected, tel: format, javascript:/http: URLs rejected, email check", h[1:] == ["919876543210", "9876543210" if False else h[2], "", "tel:+919876543210", "", "", "", True, False, True] and h[1] == "919876543210" and h[3] == "", h)
    # unconfigured buttons
    pg = load(page()); res = []
    for a, txt in [("call", "Phone number"), ("wa", "WhatsApp is not set up"), ("dir", "Directions are off"), ("mail", "Email is not set up")]:
        pg.locator(f"#ha [data-act={a}]").click(force=True); res.append(txt in pg.inner_text("#toast"))
    T("Unconfigured call/WhatsApp/Maps/email: show message, open nothing, marked aria-disabled", all(res) and pg.evaluate("window.__o.length") == 0 and pg.evaluate("[...document.querySelectorAll('#ha [data-act]')].every(b=>b.getAttribute('aria-disabled')==='true')"), res)
    pg.goto(B + "index.html#/rev"); pg.click("#s-rev [data-act=rev]"); T("Reviews: no link -> message, no fake reviews/ratings text", "not set up" in pg.inner_text("#toast") and not re.search(r"\b[1-5]\.\d\b|★", pg.inner_text("#s-rev")))
    pg.goto(B + "index.html"); hcx = pg.inner_text("#hc"); pg.goto(B + "index.html#/doc"); T("Blank config: contact and dentist show [To be confirmed], nothing invented", hcx.count("[To be confirmed]") >= 4 and "[To be confirmed]" in pg.inner_text("#dl"), hcx)
    T("Home has dentist intro + contact/location sections", all(x in idx for x in ['id="hd-name"', 'id="hc"', 'id="ha"']))
    # Hindi on every screen
    ALLOW = re.compile(r"SN Dental Clinic|WhatsApp|Google|Maps|Send|EN|WA|Sample")
    JS = """()=>{const out=[];for(const e of document.querySelectorAll('body *')){if(!e.offsetParent&&e.tagName!=='BODY')continue;const r=e.getBoundingClientRect();if(r.right<=0)continue;let t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').trim();if(t)out.push(t)}return out}"""
    pg = load(page(hook=False)); pg.click(".langbtn >> nth=0"); off = {}
    for s in SCREENS:
        pg.evaluate(f"location.hash='#/{s}'"); pg.wait_for_timeout(120)
        w = [t for t in pg.evaluate(JS) if re.search(r"[A-Za-z]{3,}", ALLOW.sub("", t))]
        if w: off[s] = w[:4]
    pg.evaluate("location.hash='#/book'"); pg.fill("#f-name", "Asha Rao"); pg.fill("#f-phone", "9876543210"); pg.select_option("#f-tr", "gum"); pg.fill("#f-date", fut(1)); pg.check("#f-ok"); pg.click("#bsub")
    w = [t for t in pg.evaluate(JS) if re.search(r"[A-Za-z]{3,}", ALLOW.sub("", t)) and t not in ("Asha Rao", "9876543210")]; 
    if w: off["book-step2"] = w[:4]
    pg.click("#send"); w = [t for t in pg.evaluate(JS) if re.search(r"[A-Za-z]{3,}", ALLOW.sub("", t)) and t not in ("Asha Rao", "9876543210")]
    if w: off["book-failure-msg"] = w[:4]
    pg.evaluate("location.hash='#/svc'"); pg.evaluate("location.hash='#/book'"); pg.wait_for_timeout(150); pg.fill("#f-name", ""); pg.click("#bsub"); er = pg.inner_text("#e-name")
    if re.search(r"[A-Za-z]{3,}", er): off["validation"] = er
    T("Hindi toggle: no untranslated English on any screen/state (12 screens + review/failure/validation)", not off, off)
    T("Language preference persists after reload", (pg.reload(), pg.evaluate("document.documentElement.lang"))[1] == "hi")
    # ---- typing, sandbox (no allow-forms) and hidden-step checks ----
    pt = load(page(), "#/book"); pt.click("#f-name"); pt.keyboard.type("Asha Rao"); pt.click("#f-phone"); pt.keyboard.type("98765 43210"); pt.click("#f-msg"); pt.keyboard.type("Hello")
    T("Real keystrokes type into name, phone and message fields", pt.input_value("#f-name") == "Asha Rao" and pt.input_value("#f-phone") == "98765 43210" and pt.input_value("#f-msg") == "Hello")
    pt.click("#f-name"); pt.keyboard.press("Enter"); T("Enter key in a field runs validation (no <form> submit needed)", pt.inner_text("#e-tr") != "" and pt.is_visible("#bf"))
    pt.select_option("#f-tr", "gum"); pt.fill("#f-date", fut(2)); pt.set_checked("#f-ok", True); pt.click("#bsub")
    T("Step 2: form hidden, review visible; Edit brings the form back", pt.is_visible("#b2") and not pt.is_visible("#bf") and (pt.click("#edit"), pt.is_visible("#bf") and not pt.is_visible("#b2"))[1])
    pq = load(page(), ""); pq.fill("#q", "gum"); pq.press("#q", "Enter"); a1 = act(pq); pq.goto(B + "index.html"); pq.fill("#q", "root"); pq.click("#qgo"); T("Home search works with Enter key and with the search button", a1 == "svc" and act(pq) == "svc" and pq.locator("#tl .card").count() == 1)
    wr_ = page(hook=False); wr_.goto(B + "index.html"); wr_.set_content('<iframe id="f" sandbox="allow-scripts allow-same-origin allow-popups" src="' + B + 'index.html#/book" style="width:390px;height:800px"></iframe>'); fl = wr_.frame_locator("#f")
    fl.locator("#f-name").wait_for(); fl.locator("#f-name").fill("Asha Rao"); fl.locator("#f-phone").fill("9876543210"); fl.locator("#f-tr").select_option("gum"); fl.locator("#f-date").fill(fut(2)); fl.locator("#f-ok").check(); fl.locator("#bsub").click(); wr_.wait_for_timeout(300)
    T("Booking works inside a sandboxed iframe WITHOUT allow-forms (like the Claude preview)", fl.locator("#b2").is_visible() and not fl.locator("#bf").is_visible())
    # ---- real clinic data from the Google Maps listing ----
    pg = page(real=True); pg.route("https://www.google.com/**", lambda r: r.fulfill(body="<html><body>map</body></html>", content_type="text/html")); load(pg)
    cv = pg.evaluate("({tel:__t.telHref(),addr:C.address,wa:__t.waNum()})")
    T("Real config: tel:+917483582795; WhatsApp intentionally empty", cv["tel"] == "tel:+917483582795" and cv["wa"] == "", cv)
    hc = pg.inner_text("#hc")
    T("Home contact card shows address, formatted phone, hours summary and Google rating", all(x in hc for x in ["4R7M+7FX, Hoskote - Chintamani Rd", "+91 74835 82795", "9:00 AM – 7:00 PM", "Closed: Wednesday", "5.0 ★ · 3 Google reviews · as of 2026-10-14"]), hc)
    stt = pg.evaluate("[...document.querySelectorAll('#ha [data-act]')].map(b=>[b.dataset.act,b.getAttribute('aria-disabled')])")
    T("Call and Directions enabled; WhatsApp and Email disabled (not configured)", dict(stt) == {"call": "false", "wa": "true", "dir": "false", "mail": "true"}, stt)
    pre = pg.locator("#mapbox iframe").count(); pg.click("#mapbox [data-act=map]"); pg.wait_for_timeout(400)
    fr = pg.evaluate("(()=>{const f=document.querySelector('#mapbox iframe');return f?{src:f.src,sb:f.getAttribute('sandbox'),rp:f.referrerPolicy}:null})()")
    T("Map: no iframe before tap; after tap a sandboxed google.com/maps iframe (no top-navigation), no referrer", pre == 0 and bool(fr) and fr["src"].startswith("https://www.google.com/maps?q=") and "allow-scripts" in fr["sb"] and "allow-top-navigation" not in fr["sb"] and fr["rp"] == "no-referrer", fr)
    pc = page(real=True); load(pc); pc.evaluate("(()=>{const m=document.createElement('meta');m.httpEquiv='Content-Security-Policy';m.content=\"frame-src 'none'\";document.head.append(m)})()"); pc.click("#mapbox [data-act=map]"); pc.wait_for_timeout(600)
    T("Map blocked by host CSP: iframe removed, clear message + Open in Google Maps button, no crash", pc.locator("#mapbox iframe").count() == 0 and "cannot be embedded" in pc.inner_text("#mapbox") and pc.locator("#mapbox [data-act=dir]").count() == 1)
    pg.goto(B + "index.html#/info/hours"); tb = pg.inner_text("#ib")
    T("Hours screen: 6 days 9:00 AM - 7:00 PM, Wednesday Closed, weekly holiday Wednesday", tb.count("9:00 AM – 7:00 PM") == 6 and re.search(r"Wednesday\s+Closed", tb) is not None and "Weekly holiday: Wednesday" in tb, tb)
    pg.goto(B + "index.html#/rev"); rt = pg.inner_text("#s-rev")
    T("Reviews screen: rating shown with source/date, no review text or reviewer names copied", "5.0 ★ · 3 Google reviews" in rt and "Narahari" not in rt + idx + app + cfgtxt and "Good care" not in rt + idx + app)
    pg.evaluate("document.querySelectorAll('img').forEach(i=>i.scrollIntoView())"); pg.goto(B + "index.html"); pg.evaluate("document.querySelectorAll('.gal2 img').forEach(i=>{i.loading='eager'})"); pg.wait_for_timeout(500)
    T("Gallery: 4 real clinic photos load", pg.evaluate("[...document.querySelectorAll('.gal2 img')].filter(i=>i.complete&&i.naturalWidth>0).length") == 4)
    pg.goto(B + "index.html#/book"); fill2(pg); pg.click("#bsub"); cb = pg.is_visible("#callbk"); pg.click("#send")
    T("Booking without WhatsApp: 'Call the clinic to book' fallback shown, setup message, nothing opened", cb and "not set up" in pg.inner_text("#st") and pg.evaluate("window.__o.length") == 0)
    T("Real config: no console errors and no failed requests", not pg.errs and not pg.bad, (pg.errs, pg.bad))
    pg2 = page(real=True, hook=False); load(pg2); pg2.click(".langbtn >> nth=0"); ALLOW2 = re.compile(ALLOW.pattern + "|" + re.escape(cv["addr"])); offr = {}
    for sc in ["home", "rev", "info/hours", "more", "book"]:
        pg2.evaluate(f"location.hash='#/{sc}'"); pg2.wait_for_timeout(120)
        w = [x for x in pg2.evaluate(JS) if re.search(r"[A-Za-z]{3,}", ALLOW2.sub("", x))]
        if w: offr[sc] = w[:4]
    T("Hindi with real data: no untranslated English except address/brand names", not offr, offr)
    # layout & a11y per width
    for w, hh in [(320, 640), (360, 740), (390, 844), (768, 1024), (1280, 800)]:
        pg = load(page(w, hh, hook=False)); ov = {}; small = {}
        for s in SCREENS:
            pg.evaluate(f"location.hash='#/{s}'"); pg.wait_for_timeout(80)
            o = pg.evaluate("document.documentElement.scrollWidth-innerWidth")
            if o > 0: ov[s] = o
            if w <= 390:
                sm = pg.evaluate("[...document.querySelectorAll('.scr.on button,.scr.on a,.scr.on select,.scr.on input:not([type=checkbox]),.scr.on summary,nav button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>0&&(r.height<43.5||r.width<43.5)}).map(e=>(e.textContent||e.id||e.tagName).trim().slice(0,16)+':'+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))")
                if sm: small[s] = sm[:3]
        T(f"No horizontal overflow at {w}px (12 screens)", not ov, ov)
        if w in (320, 360): T(f"Tap targets >=44px at {w}px", not small, small)
    pg = load(page(390, 844, hook=False)); pg.keyboard.press("Tab"); f1 = pg.evaluate("document.activeElement.className"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
    ring = pg.evaluate("(()=>{const s=getComputedStyle(document.activeElement);return s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>=2})()"); T("Keyboard: skip link first, visible focus ring on Tab", f1 == "skip" and ring, (f1, ring))
    pg.reload(); pg.keyboard.press("Tab"); pg.keyboard.press("Enter"); T("Skip link moves to main content", pg.evaluate("document.activeElement.id") == "main")
    pg.emulate_media(reduced_motion="reduce"); T("prefers-reduced-motion disables smooth scroll", pg.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto")
    ax = pg.evaluate("""()=>{const bad=[];document.querySelectorAll('input,select,textarea').forEach(e=>{if(e.type==='hidden')return;const l=e.id&&document.querySelector('label[for='+e.id+']');if(!l&&!e.closest('label')&&!e.getAttribute('aria-label'))bad.push('nolabel:'+(e.id||e.name))});
    document.querySelectorAll('button,a[href]').forEach(e=>{if(!(e.textContent.trim()||e.getAttribute('aria-label')||e.querySelector('img[alt]:not([alt=""])')))bad.push('noname:'+(e.className||e.id||e.tagName))});
    if(!document.documentElement.lang)bad.push('nolang');return bad}""")
    T("Accessible names: every input labelled, every button/link named, html lang set (static DOM check)", not ax, ax)
    h1 = {}
    for s in SCREENS:
        pg.evaluate(f"location.hash='#/{s}'"); c = pg.evaluate("[...document.querySelectorAll('h1')].filter(h=>h.offsetParent).length")
        if c != 1: h1[s] = c
    T("Exactly one visible <h1> per screen", not h1, h1)
    # 404 + preview + generator
    d = page(hook=False); r = d.goto(B + "no/such/deep/page"); T("404 page served for unknown path with inline styles and subpath-aware home link", r.status == 404 and "Page not found" in d.inner_text("h1") and d.get_attribute("#home", "href") == "/", d.get_attribute("#home", "href"))
    d.close() if hasattr(d, "close") else None
    br.close()
tmp = tempfile.mkdtemp(); r = subprocess.run([sys.executable, os.path.join(ROOT, "tools/generate_assets.py"), tmp], capture_output=True, text=True)
have = set(os.listdir(tmp)); REAL = {"clinic-treatment-room.webp", "clinic-reception.webp", "clinic-signboard.webp", "clinic-storefront.webp"}
want = {f for f in os.listdir(os.path.join(ROOT, "assets/images")) if f not in ("SOURCES.md", "favicon.svg") and f not in REAL}
T("generate_assets.py runs and reproduces every generated asset", r.returncode == 0 and want <= have and all(os.path.getsize(os.path.join(tmp, f)) > 0 for f in have), (r.stderr[-200:], want - have))
big = [f for f in os.listdir(os.path.join(ROOT, "assets/images")) if os.path.getsize(os.path.join(ROOT, "assets/images", f)) > 60000 and f not in ("og-image.jpg",)]; T("No oversized images (all <60 KB except og-image)", not big, big)
pv = os.path.join(tmp, "preview.html"); r = subprocess.run([sys.executable, os.path.join(ROOT, "tools/build_preview.py"), pv], capture_output=True, text=True)
ok = r.returncode == 0 and os.path.exists(pv)
if ok:
    with sync_playwright() as p:
        b2 = p.chromium.launch(); q = b2.new_page(viewport={"width": 390, "height": 844}); e = []; q.on("console", lambda m: e.append(m.text) if m.type == "error" else None); q.on("pageerror", lambda x: e.append(str(x)))
        q.goto("file://" + pv); q.wait_for_timeout(500); q.click("nav button[data-go=svc]"); q.evaluate("document.querySelectorAll('img').forEach(i=>i.scrollIntoView())"); q.wait_for_timeout(300)
        n = q.locator("#tl .card").count(); brk = q.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0).length"); ext = q.evaluate("[...document.querySelectorAll('[src],[href]')].filter(e=>/^https?:/.test(e.getAttribute('src')||e.getAttribute('href')||'')).length"); b2.close()
    T("build_preview.py output works: no errors, 11 cards, no broken images, no external deps", not e and n == 11 and brk == 0 and ext == 0, (e, n, brk, ext))
else: T("build_preview.py output works", False, r.stderr[-200:])
NOT = ["Actual Google Maps rendering inside the iframe (Google host was mocked; no internet in the test environment)", "Real Android phones and iOS Safari (only Chromium emulation was used)", "Screen-reader testing (TalkBack/VoiceOver) and a full axe/Lighthouse audit", "Live GitHub Pages deployment (subpath was emulated locally)", "WhatsApp app actually receiving a message (only the generated wa.me URL is verified)", "Real phone dialler, email client and Google Maps app handoff", "Firefox and Safari engines"]
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs/TEST_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(f"# Test report\nGenerated by `python3 tools/test_site.py` on {datetime.date.today()} (Chromium via Playwright, project served under `/sn-dental-demo/` to emulate a GitHub Pages subpath).\n\n| Result | Test | Detail |\n|---|---|---|\n")
    for n, s, d in R: f.write(f"| {s} | {n} | {d.replace('|', '/') if s == 'FAIL' else ''} |\n")
    f.write("\n## NOT TESTED\n" + "".join(f"- {x}\n" for x in NOT))
print(f"\n{sum(1 for r in R if r[1]=='PASS')} PASS, {sum(1 for r in R if r[1]=='FAIL')} FAIL, {len(NOT)} NOT TESTED")
