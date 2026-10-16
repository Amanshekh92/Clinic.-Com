#!/usr/bin/env python3
"""Builds a single self-contained preview HTML (images inlined) for quick sharing. Not needed for GitHub Pages."""
import re, base64, os, json, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
out = sys.argv[1] if len(sys.argv) > 1 else "preview.html"
h = open("index.html", encoding="utf-8").read()
mime = {"webp": "image/webp", "svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg"}
data = lambda p: "data:%s;base64,%s" % (mime[p.rsplit(".", 1)[1]], base64.b64encode(open(p, "rb").read()).decode())
css = re.sub(r"url\(\.\./(assets/images/[^)]+)\)", lambda m: "url(%s)" % data(m.group(1)), open("css/styles.css", encoding="utf-8").read())
h = re.sub(r'<link rel="manifest"[^>]*>', "", h)
h = h.replace('<link rel="stylesheet" href="css/styles.css">', "<style>" + css + "</style>").replace('<script src="js/config.js"></script>', "").replace('<script src="js/app.js" defer></script>', "")
h = re.sub(r'(src|srcset|href)="(assets/images/[^"]+\.(?:webp|svg|png|jpg))"', lambda m: '%s="%s"' % (m.group(1), data(m.group(2))), h)
js = open("js/config.js", encoding="utf-8").read() + "\n" + open("js/app.js", encoding="utf-8").read()
js = js.replace('"assets/images/treatment-"+(IMG[s.id]||s.id)+".webp"', "window.__IMG[(IMG[s.id]||s.id)]")
imgs = {f[10:-5]: data("assets/images/" + f) for f in os.listdir("assets/images") if f.startswith("treatment-")}
h = h.replace("</body>", "<script>window.__IMG=" + json.dumps(imgs) + ";" + js.replace("</script>", "<\\/script>") + "</script></body>")
open(out, "w", encoding="utf-8").write(h)
