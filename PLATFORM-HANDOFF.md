# Handoff: turning Lifta into a reusable mapping platform

This document is a brief for a **new** project. It describes how to take the
Lifta site (a bespoke documentary photo-map) and generalize it into a reusable
template that anyone can fork to document their own place: a neighborhood, a
trail, a building, an archaeological site, a memory map, a field survey.

You can hand this whole file to a fresh Claude Code session as its first
instruction. A ready-to-use `CLAUDE.md` for the new repository is included at
the end (see "Seed CLAUDE.md for the new repo").

The working name below is **Fieldmap**. Rename it to whatever you choose.
(This repository realized that brief as **mirl-map**.)

---

## 1. What you are building

A small, **no-build** static website that pairs **geolocated photographs** with
**per-photo written narratives**, presented two ways:

- an **interactive Leaflet map** (photos as clustered markers, click for a
  detail drawer), and
- a **sequential photo essay** (the same material, read top to bottom).

On top of that core sit optional modules the owner turns on as needed:
historical map overlays, a side-by-side layer compare, a documented timeline, a
statistics panel, a sources/citations apparatus, first-person testimony pins,
a "before/after" archival-photo layer, polygon overlays, a walking-trail
animation, KML export, full-text search, a bilingual (LTR/RTL) interface, and a
full accessibility panel.

The Lifta site is the **reference implementation**. Your job is to separate the
**engine** (reusable) from the **content** (Lifta-specific), put every site-level
constant behind one config file, replace the content with a small neutral
sample, and document the data contracts so a non-coder can fill them in.

### Why this is a good template

- **No toolchain.** Plain HTML + CSS + vanilla JS + Leaflet from a CDN. No npm,
  no bundler, no framework. Open `index.html` or run `python3 -m http.server`.
- **Content is already isolated** in `js/data/*.js` and `narratives/*.md`.
- **Deploys free** on GitHub Pages (or any static host).
- **Accessible and bilingual** out of the box.

---

## 2. Start here (first session)

1. **Duplicate the Lifta repo** into a new directory and re-init git:
   ```
   cp -R lifta fieldmap && cd fieldmap
   rm -rf .git && git init
   ```
   (Or use GitHub's "Use this template" once Lifta is marked a template repo.)
2. **Delete the Lifta content** you do not own or want to ship (see section 8,
   "What NOT to carry over"): the photos, narratives, source list, place data,
   testimonies, `CITATION.cff`, and the Lifta `README.md`/`CLAUDE.md`.
3. **Drop in the seed `CLAUDE.md`** from the end of this document.
4. **Work through the phases** in section 6, committing after each.
5. **Verify in a browser** after every phase (`python3 -m http.server 8766`).

Do not try to keep the site "live" with Lifta content while you strip it. Start
from a known-empty state with a 3-to-5 photo neutral sample, get that working
end to end, then document.

---

## 3. Architecture at a glance

```
index.html        Map page. Header controls, panels, drawer, intro screen.
gallery.html      Photo-essay page + a scrollytelling mini-map.
css/
  style.css       All map-page styling, panels, RTL rules.
  gallery.css     Essay-page styling.
  a11y.css        Accessibility (focus rings, contrast, motion).
js/
  map.js          Map controller: base/overlay layers, markers + clustering,
                  detail drawer, timeline/stats/sources panels, compare mode,
                  view cones ("sightlines"), walking trail/pace, search wiring.
  gallery.js      Essay builder + scrollytelling mini-map (view cone + nearest
                  testimony surfaced beside the photo you are reading).
  narratives.js   Loads narratives/<id>.md, renders Markdown, resolves [TOKEN]
                  citations to superscript links, renders the per-photo source
                  list. Handles the Arabic narrative fallback.
  a11y.js         Text size / high contrast / reduced motion, persisted.
  i18n.js         Bilingual runtime (capture-based; English from the DOM,
                  Arabic from the dictionary), persisted, shared across pages.
  help.js         Help panel.
  kml.js          "Download .kml" export for Google Earth.
  lib/leaflet-side-by-side.js   Compare-mode plugin (vendored).
js/data/          ALL content + the i18n dictionary (see section 5).
narratives/       One Markdown file per photo. narratives/ar/ for Arabic.
photos/           Full-res images. photos/web/ (1400px) and photos/thumb/
                  (480px) are generated tiers.
add_photo.py      Ingest one photo: read its EXIF GPS, append a photos.js entry.
scripts/          color_correct.py, make_thumbs.py (image pipeline).
```

**Page load order matters** (scripts are at the end of `<body>`): data files
first, then `a11y.js`, `i18n.js`, then the page controller (`map.js` /
`gallery.js`). Cache-busting is manual via `?v=` query strings on `<script>` and
`<link>` tags; bump them when a file changes.

State is persisted in `localStorage`: `lifta-a11y` (accessibility),
`lifta-lang` (language). Rename these keys to your project's prefix.

---

## 4. The core / content / module split

| Layer | Files | Action |
|---|---|---|
| **Engine (keep as-is)** | `js/map.js`, `js/gallery.js`, `js/narratives.js`, `js/a11y.js`, `js/i18n.js`, `js/help.js`, `js/kml.js`, `css/*`, `js/lib/*` | Keep. Touch only to read config and to delete hard-coded Lifta strings. |
| **Content (replace)** | `js/data/photos.js`, `js/data/sources.js`, `narratives/**`, `photos/**`, the prose in `index.html`/`gallery.html` (intro, about) | Replace with a small neutral sample + clear "EDIT ME" markers. |
| **Domain modules (optional, off by default)** | `js/data/landmarks.js`, `places.js`, `testimonies.js`, `matson.js`, `geodata.js`, `greenline.js`, `timeline.js`, `stats.js` | Keep the code paths, gate each behind a config flag, ship empty or with one sample row, and document. |
| **Site constants (extract to config)** | map center/zoom, default base layer, tile URLs + attributions, title, languages, feature flags | Pull out of `map.js`/HTML into a single `config.js`. This is the main refactor. |

The single most valuable change is **section 7: the config surface.** Everything
else is deletion and documentation.

---

## 5. Data contracts (the heart of the template)

Every content file is a plain `.js` that assigns a global, formatted **one
entry per block** so GitHub diffs stay readable. Preserve that formatting.

### `js/data/photos.js` — the photographs (required)
```js
const photoInfo = [
  {
    "file": "IMG_1569.JPG",      // filename in photos/ (and photos/web, photos/thumb)
    "lat": 31.800806,            // decimal degrees
    "lon": 35.199781,
    "caption": "One or two sentences shown under the photo.",
    "source_ids": ["GOR", "MEE"],// optional: keys into sources.js
    "bearing": 349.9,            // optional: compass degrees the lens faced (view cone)
    "fov": 57.2,                 // optional: horizontal field of view in degrees
    "taken_at": "2017:04:23 12:22:08"  // optional EXIF datetime; powers trail/pace
  }
]
```
`lat`/`lon`/`caption`/`file` are the only required fields. `bearing` + `fov`
enable the "sightline" view cones; `taken_at` enables the walking-trail
animation and pace heatmap. `add_photo.py` fills `lat`/`lon`/`taken_at` from
EXIF automatically.

### `js/data/sources.js` — the citation library (optional but recommended)
```js
const srcLib = {
  "GOR": { "label": "Author, Title (Publisher, Year)", "url": "https://..." }
  // url: "" renders a non-link (e.g. a print-only book)
};
```
Tokens are 2 to 8 uppercase letters. In any narrative, timeline entry, or stats
row, `[GOR]` or `[GOR p.27]` renders as a superscript link; a deduplicated
source list is auto-appended under each narrative. The "Sources" colophon panel
lists every entry in `srcLib`.

### `narratives/<id>.md` — per-photo prose (optional)
Plain Markdown, where `<id>` is the photo filename without extension
(`IMG_1569.JPG` -> `narratives/IMG_1569.md`). Blank line separates paragraphs;
`**bold**` and `*italic*`; `[TOKEN]` citations as above. Arabic versions go in
`narratives/ar/<id>.md` and fall back to the English file when absent.

### `js/data/landmarks.js` — named points of interest (module)
```js
const landmarks = [
  { "id": "spring", "name_en": "The Spring", "name_ar": "العين",
    "lat": 31.7942, "lon": 35.1971,
    "status": "extant",      // extant | ruins | destroyed | occupied (drives marker color)
    "emoji": "💧", "desc": "Popup description." }
];
```

### `js/data/geodata.js` — area polygons (module)
```js
const vBound = [[lat,lon], [lat,lon], ...];  // closed ring; one const per overlay
```
Lifta ships four (boundary, residential, olives, terraces). Rename/repurpose or
drop. The layer panel toggles and `map.js` colors are wired to these names.

### `js/data/timeline.js` — chronology panel (module)
```js
var siteTimeline = [ { date: "1948", text: "Event, with optional [TOKEN]." } ];
```

### `js/data/stats.js` — statistics panel (module)
```js
var siteStats = [
  { heading: "Population", rows: [ ["1945", "2,550", "VIL"] ] }  // [label, value, sourceToken]
];
```

### `js/data/testimonies.js` — first-person voice pins (module)
Fields: `id, speaker_en, speaker_ar?, role_en, lat, lon, location_note?,
excerpt?, source_id, source_url?, source_label?, audio_url?, notes`. The
project rule: **never insert an `excerpt` without an attestable source**; leave
it null and paraphrase in `notes` if unsure.

### `js/data/matson.js` — archival "before/after" photo pins (module)
Historical photos pinned to coordinates, each with a "view nearest modern photo"
button. Fields: `id, title, date, date_range, photographer, lat, lon,
location_note?, image_url, image_thumb`, source fields. The global is named
`matsonPhotos` for legacy reasons; rename if you like.

### `js/data/places.js`, `greenline.js` — regional context (very domain-specific)
Lifta uses these for nearby depopulated villages and the 1949 Green Line. Most
projects will delete them. Keep as an example of "context layer" if useful.

### `js/data/i18n.js` — interface dictionary (module)
```js
var siteI18N = { "nav.search": { en: "Search", ar: "بحث" } };
```
The runtime renders English from the live DOM and the second language from this
dictionary, so the English site is never altered by translation. HTML elements
opt in with `data-i18n="key"` (text), `data-i18n-html="key"` (markup), or
`data-i18n-placeholder` / `data-i18n-aria-label` / `data-i18n-title`. To support
a non-Arabic second language, swap the `ar` field and the RTL handling.

---

## 6. The templatization plan (phased, commit after each)

**Phase 0 - Fork and rename.** Duplicate, re-init git, global-replace the
`lifta-` localStorage prefixes and the `liftaTimeline`/`liftaStats`/`liftaI18N`
globals with neutral names. Update `<title>`, meta tags, favicon.

**Phase 1 - Extract `config.js`.** Create `js/config.js` (loaded first) holding
every site-level constant (see section 7). Replace the hard-coded values in
`map.js`, `gallery.js`, and the HTML with reads from it. This is the core work.

**Phase 2 - Strip to a sample.** Reduce `photos.js` to 3 to 5 neutral sample
photos (use any CC0/your-own images), write 1 to 2 sample narratives, reduce
`sources.js` to 1 to 2 sample entries. Empty or sample every module data file.
Replace intro/about prose with generic placeholder copy marked `EDIT ME`.

**Phase 3 - Gate the modules.** Behind config flags
(`features.timeline`, `features.testimonies`, etc.), hide the header button,
the layer-panel row, and skip the build step when a module is off or its data
array is empty. Each module must degrade to "simply not there," never error.

**Phase 4 - Generalize the layers.** Make base layers and historical overlays
fully config-driven: any XYZ tile URL, any georeferenced image overlay, with
its own attribution. Ship OpenStreetMap + Esri World Imagery as the safe
defaults (see the tile-terms gotcha in section 9). Keep Lifta's Palestine Open
Maps layers only as a commented example.

**Phase 5 - Documentation.** Write three docs: a `README.md` (what it is, quick
start, deploy), a `CONTENT-GUIDE.md` (how a non-coder fills in each data file,
with copy-paste templates from section 5), and keep this architecture note.

**Phase 6 - The photo pipeline.** Generalize `add_photo.py`,
`scripts/color_correct.py`, `scripts/make_thumbs.py` to read paths/quality from
config. Document the EXIF-GPS dependency and the manual-coordinate fallback for
photos without GPS.

**Phase 7 - Sample dataset + deploy.** Ship a coherent tiny demo (a park, a
campus walk, anything neutral) so a forker sees a working site immediately, then
write the GitHub Pages deploy steps.

---

## 7. The config surface to design

One file, `js/config.js`, loaded before everything. Sketch:
```js
const CONFIG = {
  site: {
    title: "Fieldmap",
    subtitle: "A documentary map",
    titleAlt: "",                 // second-language/script title, optional
    storagePrefix: "fieldmap",    // localStorage key prefix
    ogImage: "photos/IMG_0001.jpg"
  },
  map: {
    center: [31.796, 35.197],
    zoom: 17,
    defaultBase: "satellite"
  },
  baseLayers: [
    // { id, label, url, attribution, maxZoom, subdomains?, langVariants? }
  ],
  historicalLayers: [ /* optional XYZ or image overlays, each with attribution */ ],
  languages: { default: "en", second: null /* e.g. {code:"ar", rtl:true, label:"العربية"} */ },
  features: {
    timeline: false, statistics: false, sources: true,
    testimonies: false, historicalPhotos: false, compare: false,
    sightlines: true, walkingTrail: false, polygons: false,
    regionalPlaces: false, greenLine: false, kmlExport: true, search: true
  },
  images: { full: "photos/", web: "photos/web/", thumb: "photos/thumb/" }
};
```
When `features.X` is false, the engine hides that button/panel/layer and skips
its build. When a language's `second` is null, the language toggle disappears
and RTL never engages.

---

## 8. What NOT to carry over

These are Lifta-specific and either copyrighted, place-specific, or voice-specific:

- **`photos/`** - © Jeff O'Brien. Do not redistribute under the template.
- **`narratives/**`** - the written passages (drawn from a dissertation).
- **`js/data/sources.js`, `places.js`, `testimonies.js`, `matson.js`,
  `timeline.js`, `stats.js`, `geodata.js`, `greenline.js`** - Lifta content.
- **`CITATION.cff`, `README.md`** - rewrite from scratch.
- **The voice.** Lifta's first-person, restrained register and its "no em
  dashes" rule are editorial choices for that project, not platform rules. The
  template should not impose them; document them as "set your own voice."
- **The evidence-first content policy** (every claim sourced, no fabricated
  quotes) is worth recommending in the CONTENT-GUIDE as a strong default, but it
  is a content rule, not engine behavior.

Keep: all `js/*.js` engine code, `css/*`, `add_photo.py`, `scripts/*`, the
`data-i18n` wiring, the page structure.

---

## 9. Risks and gotchas to flag in the new project

- **Tile provider terms.** Lifta pulls Google map/hybrid tiles directly
  (`mt{s}.google.com/vt/...`). That is convenient but **not sanctioned for
  production embedding** under Google's terms. For a template others will host,
  default to **OpenStreetMap** raster and **Esri World Imagery** (already used
  here), or a keyed provider (MapTiler, Stadia, Mapbox). Make this a config
  choice and call it out in the README.
- **EXIF GPS dependency.** `add_photo.py` needs photos that carry GPS EXIF.
  Provide a manual `lat`/`lon` entry path for photos without it (phones strip
  GPS on share/screenshot; many cameras have no GPS).
- **Image weight.** The three-tier system (full / 1400px web / 480px thumb)
  exists because full-res sets are hundreds of MB. Keep it; document
  `make_thumbs.py` as a required step, not optional.
- **Manual cache-busting.** The `?v=` strings are hand-bumped. Document this, or
  optionally automate with a tiny pre-deploy script.
- **i18n is capture-based and chrome-only.** It translates interface strings,
  not the per-photo narratives (those use the `narratives/ar/` fallback). RTL
  layout is a solid first pass, not pixel-perfect (the photo drawer still slides
  from the right). Note both.
- **Globals, not modules.** The engine uses script-tag globals and inline
  `onclick` handlers, not ES modules. That is deliberate (no build step). Keep
  the pattern; do not "modernize" it into a bundler setup unless you want to
  give up the zero-toolchain property.

---

## 10. Seed CLAUDE.md for the new repo

The shipped `CLAUDE.md` in this repository is the realization of the seed
described in the original brief, adapted for mirl-map. Edit it for your fork.

---

## 11. Effort estimate

A capable session can reach a working, documented, deployable template in
roughly the phases above: Phase 1 (config extraction) is the bulk of the
thinking; Phases 2 to 3 are mostly deletion and flag-gating; Phases 5 to 7 are
writing and a sample dataset. None of it requires new dependencies.

The end state: someone clones the repo, edits `js/config.js`, drops photos in
`photos/`, runs `add_photo.py` and `make_thumbs.py`, writes a few `.md` files,
and has their own documentary map live on GitHub Pages within an afternoon.
