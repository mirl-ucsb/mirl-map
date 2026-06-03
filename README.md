# mirl-map

A reusable, no-build documentary photo-map. It pairs **geolocated photographs**
with **per-photo written narratives** and presents them two ways: an interactive
**Leaflet map** and a sequential **photo essay**. Fork it to document a place,
a trail, a building, an archaeological site, a memory map, or a field survey.

Built and maintained by the [Material / Image Research Lab (MIRL)](https://mirl.arthistory.ucsb.edu)
at UC Santa Barbara, generalized from the bespoke "Lifta" project. MIRL forks it
per project; you can too.

- **No toolchain.** Plain HTML, CSS, and vanilla JavaScript with Leaflet from a
  CDN. No npm, no bundler, no framework.
- **One config file.** Everything site-specific lives in
  [`js/config.js`](js/config.js): title, map center, tile layers, feature flags,
  languages.
- **Deploys free** on GitHub Pages (or any static host).
- **Accessible and bilingual-capable** out of the box.

The repository ships a small neutral placeholder demo (four generated images
near UC Santa Barbara) so it runs the moment you open it.

---

## See it locally

No build step. Serve the folder and open it:

```bash
git clone https://github.com/YOUR-USER/mirl-map.git
cd mirl-map
python3 -m http.server 8766
```

Open <http://localhost:8766>. (Opening `index.html` directly mostly works, but a
local server is needed for the narratives, which load over `fetch`.)

---

## Make it yours

1. **Edit [`js/config.js`](js/config.js).** Set the title, the map `center` and
   `zoom`, pick your base layers, and turn features on or off. Look for the
   `EDIT ME` markers.
2. **Add your photographs.** Drop full-resolution images in `photos/`, then:
   ```bash
   python3 add_photo.py photos/your-photo.jpg   # reads EXIF GPS, appends to photos.js
   python3 scripts/make_thumbs.py               # generate the web/thumb tiers (required)
   ```
   No GPS in the photo? `add_photo.py` asks you to type the coordinates.
3. **Write the words.** Edit captions in [`js/data/photos.js`](js/data/photos.js)
   and add a narrative per photo in `narratives/<filename>.md`.
4. **Replace the demo prose** (the intro and "about" text marked `EDIT ME` in
   `index.html` / `gallery.html`).
5. **Reload.** Bump the `?v=` numbers on the `<script>`/`<link>` tags when a file
   changes, so browsers fetch the new version.

For a field-by-field walkthrough aimed at non-coders, see
[`CONTENT-GUIDE.md`](CONTENT-GUIDE.md).

---

## Features (each toggled in `config.js`)

Always on: the interactive map with clustered photo markers, the photo drawer
with per-photo narratives and citation export (Chicago / MLA / APA / BibTeX),
shareable `?photo=` permalinks, and the accessibility panel (text size, high
contrast, reduced motion).

Optional modules (`CONFIG.features`): full-text **search**, **sightline** view
cones, the **photo-essay** gallery with a scrollytelling mini-map, **KML** export
for Google Earth, a documented **timeline**, a **statistics** panel, a **sources**
citation apparatus, first-person **testimony** pins, archival **before/after**
photo pins, side-by-side layer **compare**, a **walking-trail** animation, area
**polygons**, regional **places**, and a second **language** with full RTL
support. An off module simply is not there: no button, no error.

---

## Project structure

```
index.html          Map page.
gallery.html        Photo-essay page + scrollytelling mini-map.
js/config.js        ← the one file you edit. Every site-level setting.
js/                 The engine (map.js, gallery.js, narratives.js, i18n.js,
                    a11y.js, help.js, kml.js, lib/). You rarely touch these.
js/data/            All content: photos.js, sources.js, the i18n dictionary,
                    and the optional module data files.
narratives/         One Markdown file per photo (and ar/ for a second language).
photos/             Full-res images, with generated web/ and thumb/ tiers.
scripts/            color_correct.py (optional), make_thumbs.py (required).
add_photo.py        Ingest a photo from its EXIF.
```

Scripts load at the end of `<body>` in this order: data files, then engine, then
the page controller. `js/config.js` loads first, in `<head>`. State persists in
`localStorage` under `CONFIG.site.storagePrefix`.

---

## Deploy to GitHub Pages

1. Push the repository to GitHub.
2. Set `CONFIG.site.baseUrl` in `js/config.js` to your Pages URL (it is used by
   citation permalinks and the KML export), and update the `<meta>` tags + the
   canonical URL in `index.html` / `gallery.html`.
3. In the repo's **Settings → Pages**, set the source to **GitHub Actions**. The
   included workflow ([`.github/workflows/static.yml`](.github/workflows/static.yml))
   publishes the site on every push to `main`.

Any static host works too (Netlify, Cloudflare Pages, S3, a plain web server) —
there is nothing to build.

---

## A note on tiles

The defaults are **OpenStreetMap** (streets) and **Esri World Imagery / Topo**
(satellite and topographic), which are fine to embed. If you need heavier usage
or vector tiles, plug in a keyed provider (MapTiler, Stadia, Mapbox) in
`CONFIG.baseLayers`. Always keep each layer's `attribution`.

---

## Lineage and reuse

mirl-map is generalized from "Lifta," a documentary map of a depopulated
Palestinian village. The architecture and data contracts are documented in
[`PLATFORM-HANDOFF.md`](PLATFORM-HANDOFF.md).

The **engine** (everything in `js/`, `css/`, the scripts, the page structure) is
yours to reuse and adapt. The **content** you add — your photographs, your
narratives — is yours; set your own license for it. The shipped placeholder
images are generated filler with no rights attached.
