# SN Dental Clinic, Hoskote: app-style demo (DukaanBoost)
Static HTML, CSS and vanilla JavaScript, no build step, no dependencies. Edit **js/config.js** only.

## Folders
index.html, privacy.html, terms.html, 404.html, robots.txt, manifest.webmanifest, sitemap.xml.example | css/ | js/ (config.js, app.js) | assets/images/ (+ SOURCES.md) | docs/ (AUDIT_AND_CHANGES.md, BACKEND_PLAN.md, TEST_REPORT.md) | tools/ (generate_assets.py, build_preview.py, test_site.py; not needed for hosting)

## Clinic data
The details in js/config.js come from the clinic's public Google Maps listing and are listed with their verification status in docs/CLINIC_DATA_SOURCES.md. WhatsApp, email and doctor details are still empty.

## Configure (js/config.js)
Leave a value `""` until the clinic has verified it. Empty values show "[To be confirmed]" and the matching button stays disabled with a clear message.
- `phone` e.g. `"+919XXXXXXXXX"`. `whatsapp` digits with country code e.g. `"919XXXXXXXXX"` (a 10-digit mobile gets 91 added; spaces and + are removed).
- `address`, `email`, `maps` (https Google Maps link; used only with an address), `reviews` (https verified Google Maps reviews link), `holidays`, `hours`, `doctor` (name, qual, exp, spec).
- `svc`: set `ok:1` for each treatment the clinic confirms; then set `demo:false` to hide Sample tags and the demo banner.
Never put passwords, API secrets or service-role keys in these files.

## What works now (static demo)
Home, Services (search, category filter, empty state), 3-step appointment request (validation, past dates rejected, duplicate blocked, review/edit) handing off to WhatsApp, call/email/directions/review links when configured, dentist profile, appointments empty state, reviews link, profile, About, FAQ, hours, privacy/terms templates, English/Hindi on every screen, browser Back and refresh support.
## Not implemented (needs a backend, see docs/BACKEND_PLAN.md)
Real bookings and confirmation, appointment history, owner dashboard, customer login, reminders, analytics, payments. A WhatsApp message is not a confirmed appointment.
## Before launch (clinic must verify)
All config values above, doctor details and permission for any real photos, which treatments are offered, privacy/terms (lawyer review), then: remove `noindex` (index.html, privacy, terms, 404), add canonical + absolute og:image, copy `sitemap.xml.example` to `sitemap.xml` and uncomment the line in robots.txt.
## Images
Original illustrations (SAMPLE, not real people or the real clinic). Replace any file in assets/images with a licensed or clinic-owned photo of the same name and size; see assets/images/SOURCES.md. `python3 tools/generate_assets.py assets/images` regenerates the illustrations (needs Playwright + Pillow).
## Publish on GitHub Pages (free)
1. Create a repository and upload the contents of this folder (index.html at the repo root). 2. Settings > Pages > Build and deployment > Deploy from a branch > main > / (root). 3. Open https://USERNAME.github.io/REPO/. All paths are relative, so the subpath works. Custom domain (optional, separate): add the domain in Pages settings and a CNAME DNS record; update canonical/sitemap.
## Android check
Open the URL in Chrome: bottom nav, Back key, search/filter, form errors, language toggle, and (with a number configured) the WhatsApp handoff.
## Tests
`python3 tools/test_site.py` (needs Playwright + Chromium) writes docs/TEST_REPORT.md. `python3 tools/build_preview.py preview.html` makes a single-file preview.
