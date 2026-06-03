/* ============================================================================
   photos.js — the photographs (REQUIRED)
   ----------------------------------------------------------------------------
   One block per photograph. Only file / lat / lon / caption are required.
     bearing + fov  → draw the camera "sightline" cone (features.sightlines)
     taken_at       → enable the walking-trail animation (features.walkingTrail)
     source_ids     → citation tokens, keyed into js/data/sources.js
   add_photo.py fills lat / lon / taken_at from a photo's EXIF automatically.

   The four entries below are a neutral placeholder demo near UC Santa Barbara.
   Replace them with your own. See CONTENT-GUIDE.md.
   ============================================================================ */
const photoInfo = [
  {
    "file": "sample-01.jpg",
    "lat": 34.41386,
    "lon": -119.84905,
    "caption": "EDIT ME — a one or two sentence caption, shown beneath the photo.",
    "source_ids": ["SAMP"],
    "bearing": 205,
    "fov": 62,
    "taken_at": "2026:05:01 14:10:00"
  },
  {
    "file": "sample-02.jpg",
    "lat": 34.41452,
    "lon": -119.84758,
    "caption": "EDIT ME — replace this with your own caption and coordinates.",
    "source_ids": [],
    "bearing": 95,
    "fov": 55,
    "taken_at": "2026:05:01 14:18:00"
  },
  {
    "file": "sample-03.jpg",
    "lat": 34.41291,
    "lon": -119.85016,
    "caption": "EDIT ME — captions can carry citation tokens like [SAMP] too.",
    "source_ids": ["SAMP"],
    "bearing": 318,
    "fov": 66,
    "taken_at": "2026:05:01 14:25:00"
  },
  {
    "file": "sample-04.jpg",
    "lat": 34.41524,
    "lon": -119.85050,
    "caption": "EDIT ME — a photo without bearing/fov simply has no sightline cone.",
    "source_ids": [],
    "taken_at": "2026:05:01 14:33:00"
  }
];
