#!/usr/bin/env python3
"""
add_photo.py — add a photograph to the map.

Usage:
    python3 add_photo.py photos/my-photo.jpg

The script will:
  1. Read GPS coordinates (and the capture time) from the photo's EXIF.
     If there is no GPS (phones often strip it on share; many cameras have
     none), it asks you to type the latitude and longitude.
  2. Prompt for an optional caption.
  3. Append an entry to js/data/photos.js (preserving its header comment).
  4. Remind you to generate the web/thumb tiers and, optionally, write a
     narrative.

Then run  python3 scripts/make_thumbs.py  and reload the page.

Requires Pillow:  pip3 install Pillow
"""

import sys, os, re, json
from pathlib import Path

# Paths are relative to this file (the repo root). If you change CONFIG.images
# in js/config.js, change "photos" here to match.
REPO       = Path(__file__).resolve().parent
PHOTOS_DIR = REPO / 'photos'
PHOTOS_JS  = REPO / 'js' / 'data' / 'photos.js'
EXTS       = ('.jpg', '.jpeg', '.png', '.heic', '.heif')


def dms_to_decimal(dms, ref):
    """Convert a degrees/minutes/seconds tuple + N/S/E/W ref to decimal degrees."""
    d, m, s = dms
    decimal = d + m / 60 + s / 3600
    if ref in ('S', 'W'):
        decimal = -decimal
    return round(decimal, 6)


def read_exif(filepath):
    """Return {'coords': (lat, lon) or None, 'taken_at': 'YYYY:MM:DD HH:MM:SS' or None}."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip3 install Pillow")
        sys.exit(1)

    out = {'coords': None, 'taken_at': None}
    try:
        exif = Image.open(filepath)._getexif() or {}
    except Exception:
        return out

    named = {TAGS.get(k, k): v for k, v in exif.items()}
    if named.get('DateTimeOriginal'):
        out['taken_at'] = named['DateTimeOriginal']

    gpsinfo = named.get('GPSInfo')
    if gpsinfo:
        gps = {GPSTAGS.get(k, k): v for k, v in gpsinfo.items()}
        if 'GPSLatitude' in gps and 'GPSLongitude' in gps:
            lat = dms_to_decimal(gps['GPSLatitude'],  gps.get('GPSLatitudeRef',  'N'))
            lon = dms_to_decimal(gps['GPSLongitude'], gps.get('GPSLongitudeRef', 'E'))
            out['coords'] = (lat, lon)
    return out


def load_photos_js():
    """Parse js/data/photos.js into a Python list, tolerating a leading comment."""
    content = PHOTOS_JS.read_text()
    start = content.find('[')
    end = content.rfind(']')
    if start < 0 or end < 0:
        return []
    return json.loads(content[start:end + 1])


def save_photos_js(photo_list):
    """Write the list back, preserving any header comment before the assignment."""
    json_str = json.dumps(photo_list, ensure_ascii=False, indent=2)
    header = ''
    if PHOTOS_JS.exists():
        m = re.search(r'^(.*?)const\s+photoInfo\s*=', PHOTOS_JS.read_text(), re.S)
        if m:
            header = m.group(1)
    PHOTOS_JS.write_text(f'{header}const photoInfo = {json_str};\n')


def prompt(label):
    return input(f'{label} [Enter to skip]: ').strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.is_absolute():
        filepath = REPO / filepath
    filepath = filepath.resolve()

    if not filepath.exists():
        print(f"ERROR: file not found: {filepath}")
        sys.exit(1)
    if filepath.suffix.lower() not in EXTS:
        print(f"ERROR: unsupported file type: {filepath.suffix}")
        sys.exit(1)

    filename = filepath.name
    PHOTOS_DIR.mkdir(exist_ok=True)
    dest = PHOTOS_DIR / filename
    if filepath != dest:
        import shutil
        shutil.copy2(filepath, dest)
        print(f"Copied {filename} -> photos/")

    photos = load_photos_js()
    existing = [p['file'] for p in photos]
    if filename in existing:
        print(f"'{filename}' is already on the map (entry #{existing.index(filename) + 1}). Nothing to do.")
        sys.exit(0)

    meta = read_exif(dest)
    if meta['coords']:
        lat, lon = meta['coords']
        print(f"GPS found: {lat:.6f}, {lon:.6f}")
    else:
        print("No GPS in EXIF. Enter coordinates (decimal degrees; "
              "right-click a spot in Google Maps to copy them).")
        try:
            lat = float(prompt("Latitude  (e.g. 34.41386)") or "nan")
            lon = float(prompt("Longitude (e.g. -119.84905)") or "nan")
            if lat != lat or lon != lon:  # NaN check
                raise ValueError
        except ValueError:
            print("ERROR: latitude and longitude are required.")
            sys.exit(1)

    caption = prompt("Caption (one or two sentences)")

    entry = {"file": filename, "lat": lat, "lon": lon, "caption": caption, "source_ids": []}
    if meta['taken_at']:
        entry["taken_at"] = meta['taken_at']

    photos.append(entry)
    save_photos_js(photos)

    base = Path(filename).stem
    print(f"\nDone. '{filename}' added as entry #{len(photos)}.")
    print("Next:")
    print("  1. python3 scripts/make_thumbs.py     (generate web/thumb tiers)")
    print(f"  2. (optional) write narratives/{base}.md   (its narrative)")
    print("  3. reload the page.")


if __name__ == '__main__':
    main()
