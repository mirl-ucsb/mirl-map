#!/usr/bin/env python3
"""
add_photo.py — Add a new photo to the Lifta map.

Usage:
    python3 add_photo.py photos/IMG_1234.JPG

The script will:
  1. Read GPS coordinates from the photo's EXIF data
  2. Prompt you for an optional caption and context paragraph
  3. Append the entry to js/data/photos.js
  4. Refresh your browser to see the new marker on the map
"""

import sys, os, re, json
from pathlib import Path

# --------------------------------------------------------------------------
PHOTOS_DIR = Path(__file__).parent / 'photos'
PHOTOS_JS  = Path(__file__).parent / 'js' / 'data' / 'photos.js'
# --------------------------------------------------------------------------


def dms_to_decimal(dms, ref):
    """Convert degrees/minutes/seconds tuple + N/S/E/W ref to decimal degrees."""
    d, m, s = dms
    decimal = d + m / 60 + s / 3600
    if ref in ('S', 'W'):
        decimal = -decimal
    return round(decimal, 6)


def read_gps(filepath):
    """Return (lat, lon) from EXIF, or None if not found."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip3 install Pillow")
        sys.exit(1)

    img = Image.open(filepath)
    exif = img._getexif()
    if not exif:
        return None

    for tag, val in exif.items():
        if TAGS.get(tag) == 'GPSInfo':
            gps = {GPSTAGS.get(k, k): v for k, v in val.items()}
            if 'GPSLatitude' in gps and 'GPSLongitude' in gps:
                lat = dms_to_decimal(gps['GPSLatitude'],  gps.get('GPSLatitudeRef',  'N'))
                lon = dms_to_decimal(gps['GPSLongitude'], gps.get('GPSLongitudeRef', 'E'))
                return lat, lon
    return None


def load_photos_js():
    """Parse js/data/photos.js and return the Python list."""
    content = PHOTOS_JS.read_text()
    json_str = re.sub(r'^const photoInfo\s*=\s*', '', content.strip().rstrip(';'))
    return json.loads(json_str)


def save_photos_js(photo_list):
    """Write the updated list back to js/data/photos.js."""
    json_str = json.dumps(photo_list, ensure_ascii=False, indent=2)
    PHOTOS_JS.write_text(f'const photoInfo  = {json_str};\n')


def prompt(label, default=''):
    val = input(f'{label}{" [leave blank to skip]" if not default else ""}: ').strip()
    return val or default


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]
    # Accept bare filename or full path
    filepath = Path(arg)
    if not filepath.is_absolute():
        filepath = Path(__file__).parent / filepath
    filepath = filepath.resolve()

    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    if filepath.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.heic', '.heif'):
        print(f"ERROR: Unsupported file type: {filepath.suffix}")
        sys.exit(1)

    filename = filepath.name

    # Ensure the photo is in the photos/ directory
    dest = PHOTOS_DIR / filename
    if filepath != dest:
        import shutil
        shutil.copy2(filepath, dest)
        print(f"Copied {filename} → photos/")

    # Check for duplicates
    photos = load_photos_js()
    existing = [p['file'] for p in photos]
    if filename in existing:
        print(f"'{filename}' is already in the map (entry #{existing.index(filename)+1}). Nothing to do.")
        sys.exit(0)

    # Read GPS
    coords = read_gps(dest)
    if coords:
        lat, lon = coords
        print(f"GPS found: {lat:.6f}°N, {lon:.6f}°E")
    else:
        print("No GPS data found in EXIF.")
        try:
            lat = float(prompt("Enter latitude  (e.g. 31.798022)"))
            lon = float(prompt("Enter longitude (e.g. 35.196517)"))
        except ValueError:
            print("ERROR: Invalid coordinates.")
            sys.exit(1)

    # Caption and context
    print("\nAdd metadata (press Enter to skip any field):")
    caption = prompt("Caption (short description)")
    context = prompt("Context (historical paragraph)")
    source_ids = []  # could extend later

    new_entry = {
        "file":       filename,
        "lat":        lat,
        "lon":        lon,
        "caption":    caption,
        "context":    context,
        "source_ids": source_ids
    }

    photos.append(new_entry)
    save_photos_js(photos)

    print(f"\nDone! '{filename}' added as entry #{len(photos)}.")
    print("Refresh your browser to see the new marker on the map.")


if __name__ == '__main__':
    main()
