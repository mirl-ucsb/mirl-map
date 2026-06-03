# Content guide

How to fill in your own content. You do not need to know how to code: every file
below is a list you edit by copying a block and changing the values. Keep the
commas and quotation marks exactly as shown.

After any change, reload the page. If nothing changes, bump the small `?v=1`
number on that file's `<script>` tag in `index.html` (and `gallery.html`) so the
browser stops using its cached copy.

> **Golden rule for the data files:** one entry per `{ ... }` block, separated by
> commas, inside the `[ ... ]` list. The **last** entry has no trailing comma.

> **Using the `/admin` CMS?** Then photographs are edited in the CMS (or in
> `content/photos/*.md`), and `js/data/photos.js` + `narratives/*.md` are
> generated for you — don't hand-edit those. See [`ADMIN-SETUP.md`](ADMIN-SETUP.md).
> Everything else below (sources, modules, languages) works the same either way.

---

## 1. Settings — `js/config.js`

The one file that makes the map yours. Open it and edit the values marked
`EDIT ME`:

- **`site.title` / `site.subtitle`** — shown in the header and browser tab.
- **`map.center`** — `[latitude, longitude]`. Right-click a spot in Google Maps
  to copy its coordinates.
- **`map.zoom`** — 1 (whole world) to about 18 (a single street).
- **`baseLayers`** — the map-style buttons. The defaults (OpenStreetMap + Esri)
  are fine for most projects.
- **`languages.second`** — leave `null` for one language; see section 8 to add a
  second.
- **`features`** — turn modules on (`true`) or off (`false`). Turn one on only
  once you have added its data.

---

## 2. Photographs — `js/data/photos.js` (required)

The heart of the map. Only `file`, `lat`, `lon`, and `caption` are required.

```js
{
  "file": "my-photo.jpg",          // the filename in photos/
  "lat": 34.41386,                  // decimal degrees
  "lon": -119.84905,
  "caption": "One or two sentences shown under the photo.",
  "source_ids": ["SAMP"],          // optional: citation tokens (section 3)
  "bearing": 205,                   // optional: compass degrees the lens faced
  "fov": 62,                        // optional: horizontal field of view, degrees
  "taken_at": "2026:05:01 14:10:00" // optional: enables the walking-trail feature
}
```

The easiest way to add one is `python3 add_photo.py photos/my-photo.jpg`, which
fills `lat` / `lon` / `taken_at` from the photo's EXIF for you. Then run
`python3 scripts/make_thumbs.py` to make the small versions the site serves.

`bearing` + `fov` draw the "sightline" cone showing where the camera pointed.

---

## 3. Sources / citations — `js/data/sources.js` (optional)

A small library of sources. A **token** is 2 to 8 capital letters.

```js
const srcLib = {
  "SAMP": { "label": "Author, Title (Publisher, Year)", "url": "https://example.org/" },
  "ARCH": { "label": "City Archive, Box 12", "url": "" }   // url:"" = no link (e.g. a book)
};
```

Then anywhere in a caption, a narrative, a timeline entry, or a stats row, write
`[SAMP]` or `[SAMP p.27]`. It becomes a small superscript link, and a tidy source
list appears automatically under each narrative. The **Sources** panel lists
every entry here.

---

## 4. Narratives — `narratives/<filename>.md` (optional)

One Markdown file per photo, named after the photo without its extension:
`photos/my-photo.jpg` → `narratives/my-photo.md`. A photo with no file just shows
its caption.

- Blank line between paragraphs.
- `**bold**`, `*italic*`.
- Citation tokens like `[SAMP]` as above.

---

## 5. Landmarks — `js/data/landmarks.js`

Named points of interest. Set `features.landmarks: true` once you add some.

```js
var landmarks = [
  {
    "id": "overlook", "name_en": "The Overlook", "name_ar": "",
    "lat": 34.4140, "lon": -119.8489,
    "status": "extant",          // extant | ruins | destroyed | occupied  (sets the colour)
    "emoji": "📍", "desc": "A short popup description."
  }
];
```

---

## 6. Areas, timeline, statistics, places, line, voices, historical photos

Each is an optional module: add data, set its `features.X` flag to `true`.

- **`js/data/geodata.js`** — four area-polygon slots (`vBound`, `vResid`,
  `vOlive`, `vTerr`), each a closed ring of `[lat, lon]` points. Feature:
  `polygons`.
- **`js/data/timeline.js`** — `{ date, text }` entries. Feature: `timeline`.
- **`js/data/stats.js`** — sections of `[label, value, sourceToken]` rows.
  Feature: `statistics`.
- **`js/data/places.js`** — a context layer of nearby places. Feature:
  `regionalPlaces`.
- **`js/data/greenline.js`** — one or more polylines (a boundary or route).
  Feature: `greenLine`.
- **`js/data/testimonies.js`** — first-person voice pins. **Never add an
  `excerpt` without a real source**; leave it `null` and paraphrase in `notes`.
  Feature: `testimonies`.
- **`js/data/matson.js`** — archival photos pinned with a "view nearest modern
  photo" button. Feature: `historicalPhotos`.

Each file has a commented example showing its exact shape.

---

## 7. Historical map overlays — `js/config.js`

To overlay a georeferenced historical map (and enable side-by-side compare),
add an entry to `CONFIG.historicalLayers` and set `features.compare: true`. A
worked example (public-domain tiles) is commented in `config.js`.

---

## 8. A second language

1. In `js/config.js`, set, for example:
   `languages.second = { code: "es", rtl: false, label: "Español" }`
   (use `rtl: true` for right-to-left scripts like Arabic).
2. In `js/data/i18n.js`, add a field named with that code to each key:
   `"nav.search": { en: "Search", es: "Buscar" }`.
3. Translate narratives into `narratives/ar/<filename>.md` (the folder is named
   `ar/` as the shipped example; keep that name or update the one path in
   `js/narratives.js`). A missing translation falls back to the default language.

The language toggle appears automatically once a second language is set.

---

## A good default content policy

For documentary work: cite every factual claim, and never invent a quotation. If
you cannot source something, leave it out. mirl-map does not enforce this — set
your own editorial voice — but it is a strong default.
