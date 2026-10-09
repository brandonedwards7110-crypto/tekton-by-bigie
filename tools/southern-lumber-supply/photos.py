#!/usr/bin/env python3
"""Copies the photos used by the Southern Lumber Supply spec draft into the draft folder.
Sources (all the business's own, public): images on southernlumbersupply.com (builder.io CDN, downloaded 2026-10-09 at full size)
and one cropped screenshot of their Instagram post DePNOBAjmhv (Inlet Beach exterior job). SRC = folder with the downloaded b00..b25 files.
Run:  python3 tools/southern-lumber-supply/photos.py <SRC> <IG_PNG>"""
import os, sys
from PIL import Image
SRC, IG = sys.argv[1], sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "southern-lumber-supply", "draft", "assets", "photos")
os.makedirs(OUT, exist_ok=True)

def save(name, img, maxw, ext="jpg", q=84):
    if img.width > maxw: img = img.resize((maxw, round(img.height * maxw / img.width)), Image.LANCZOS)
    p = os.path.join(OUT, f"{name}.{ext}")
    if ext == "png": img.save(p, optimize=True)
    else: img.convert("RGB").save(p, quality=q, optimize=True, progressive=True)
    print(f"{name}.{ext}", img.size, os.path.getsize(p) // 1024, "KB")

P = {  # name -> (source b-file, max width)
    "hero-framing": ("b09", 2000), "store-zenith": ("b02", 1600), "store-bic": ("b04", 800), "store-installit": ("b07", 800),
    "store-lynnhaven": ("b06", 800), "install-door": ("b08", 800), "roofer": ("b10", 800), "roof-aerial": ("b16", 800),
    "house-porch": ("b17", 800), "doors-boxes": ("b11", 1200),
    "staff-jay": ("b12", 640), "staff-brantley": ("b13", 640), "staff-donna": ("b14", 640), "staff-steve": ("b15", 640),
}
for n, (b, w) in P.items():
    save(n, Image.open(os.path.join(SRC, b)), w)
# their current logo, the Installit! logo and four brand logos (kept as PNG for transparency)
for n, b, w in [("their-logo", "b00", 800), ("installit-logo", "b05", 800), ("brand-midwest", "b22", 600), ("brand-milwaukee", "b23", 500),
                ("brand-sierra", "b24", 400), ("brand-diablo", "b25", 600)]:
    save(n, Image.open(os.path.join(SRC, b)).convert("RGBA"), w, "png")
# Instagram job photo: crop away the Instagram arrow button and avatar icon that were on the screenshot
im = Image.open(IG).convert("RGB"); im = im.crop((0, 4, 880, 1090)); save("project-exterior", im, 880)
