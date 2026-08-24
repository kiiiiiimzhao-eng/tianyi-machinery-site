#!/usr/bin/env python3
"""
Resize a blog/case-study image and export optimized JPG + WebP versions.

Usage:
    python process_blog_image.py <source_image> <output_dir>

Example:
    python process_blog_image.py \
        "C:\\Users\\...\\clipboard-image.jpg" \
        "E:\\...\\tianyi-site\\images\\blog\\gas-tight-en-masse-conveyor"
"""

import sys
import os
from PIL import Image, ImageOps


def process_image(src_path: str, out_dir: str, max_size: int = 1400) -> None:
    os.makedirs(out_dir, exist_ok=True)

    im = Image.open(src_path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    else:
        im = im.convert("RGB")

    # Correct orientation based on EXIF data (important for mobile/clipboard photos)
    im = ImageOps.exif_transpose(im)

    w, h = im.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        im = im.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    jpg_path = os.path.join(out_dir, "main.jpg")
    webp_path = os.path.join(out_dir, "main.webp")

    im.save(jpg_path, "JPEG", quality=85, optimize=True)
    im.save(webp_path, "WEBP", quality=82, method=6)

    print(f"Saved: {jpg_path} ({os.path.getsize(jpg_path)} bytes)")
    print(f"Saved: {webp_path} ({os.path.getsize(webp_path)} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    process_image(sys.argv[1], sys.argv[2])
