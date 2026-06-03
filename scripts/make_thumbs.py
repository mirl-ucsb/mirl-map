#!/usr/bin/env python3
"""
Generate web-delivery derivatives for the Lifta photographs.

Every image on the site was being served at full resolution (3-5 MB),
including 52px map markers. This generates two downscaled tiers from
the already-corrected, already-upright photos in photos/:

  photos/thumb/  ~480px longest side  (map markers, search results)
  photos/web/   ~1400px longest side  (gallery grid, map drawer, popups)

Full-resolution photos/ are kept untouched and served only in the
lightbox "Full size" view. EXIF is stripped from derivatives (map
placement comes from photos.js, not image EXIF; orientation is already
baked into the pixels).
"""

import os, glob
from PIL import Image, ImageOps

PHOTOS = "/Users/jeff/Documents/GitHub/lifta/photos"
TIERS = [("thumb", 480, 80), ("web", 1400, 82)]


def main():
    for name, _, _ in TIERS:
        os.makedirs(os.path.join(PHOTOS, name), exist_ok=True)

    files = sorted(glob.glob(os.path.join(PHOTOS, "*.JPG")))
    print(f"Generating derivatives for {len(files)} photos\n")
    totals = {name: 0 for name, _, _ in TIERS}

    for f in files:
        base = os.path.basename(f)
        img = ImageOps.exif_transpose(Image.open(f)).convert("RGB")  # no-op if already upright
        for name, maxdim, q in TIERS:
            d = img.copy()
            d.thumbnail((maxdim, maxdim), Image.LANCZOS)
            out = os.path.join(PHOTOS, name, base)
            d.save(out, "JPEG", quality=q, optimize=True, progressive=True)
            totals[name] += os.path.getsize(out)

    for name, maxdim, _ in TIERS:
        print(f"  photos/{name}/  ({maxdim}px)  total {totals[name]/1048576:.1f} MB")
    print("\nDone. Full-resolution photos/ left untouched.")


if __name__ == "__main__":
    main()
