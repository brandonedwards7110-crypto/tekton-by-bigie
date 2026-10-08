#!/usr/bin/env python3
"""Copies the chosen South Walton Academy photos (downloaded from their own public website, 2026-10-07) into the draft
at web-friendly sizes. Child-privacy rule: ONLY photos with no recognizable child (buildings, empty rooms, empty gym and
playground, flyers) plus the staff portraits already shown on their Our Staff page. Run once; needs SRC (the download dir)."""
import os, sys, json
from PIL import Image
SRC = sys.argv[1]          # .../swa/img
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "south-walton-academy", "draft", "assets", "photos")
os.makedirs(OUT, exist_ok=True)

# new name -> (source file, max width)
PICKS = {
    "building-front":   ("2024_07_IMG-20240702-WA0063.jpg", 1600),
    "building-side":    ("2024_07_IMG-20240702-WA0061.jpg", 1600),
    "building-entry":   ("2024_07_IMG-20240702-WA0064.jpg", 1600),
    "classroom-blue":   ("2024_07_IMG-20240702-WA0082.jpg", 1600),
    "classroom-bright": ("2024_07_IMG-20240702-WA0072.jpg", 1600),
    "classroom-color":  ("2024_07_IMG-20240702-WA0074.jpg", 1600),
    "classroom-welcome":("2024_07_IMG-20240702-WA0085.jpg", 1600),
    "classroom-nook":   ("2024_07_IMG-20240702-WA0080.jpg", 1200),
    "classroom-sofa":   ("2024_07_IMG-20240702-WA0091.jpg", 1600),
    "classroom-tree":   ("2024_07_IMG-20240702-WA0092.jpg", 1600),
    "classroom-lights": ("2024_07_IMG-20240702-WA0094.jpg", 1600),
    "speech-room":      ("2024_07_IMG-20240702-WA0087.jpg", 1600),
    "gym-empty":        ("2024_07_WhatsApp-Image-2024-05-18-at-10.27.48_37e06487.jpg", 1600),
    "gym-court":        ("2024_05_campus1-1.jpg", 1200),
    "gym-pickleball":   ("2024_05_campus4.jpg", 1200),
    "playground":       ("2024_07_IMG-20240702-WA0104.jpg", 1600),
    "flyer-teeup":      ("2026_08_WhatsApp-Image-2026-08-31-at-9.17.34-AM-1.jpeg", 1000),
    "flyer-fall-fest":  ("2026_08_WhatsApp-Image-2026-08-31-at-9.17.34-AM-4.jpeg", 1000),
    "flyer-royal-tea":  ("2026_08_WhatsApp-Image-2026-08-31-at-9.17.34-AM.jpeg", 1000),
    "calendar-2026-27": ("2026_10_calendar-26.jpeg", 1400),
}
def save(name, src, maxw, ext="jpg"):
    im = Image.open(os.path.join(SRC, src))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    path = os.path.join(OUT, f"{name}.{ext}")
    if ext == "png": im.save(path, optimize=True)
    else: im.convert("RGB").save(path, quality=84, optimize=True, progressive=True)
    return path, im.size
for n, (s, w) in PICKS.items():
    p, sz = save(n, s, w); print(n, sz, os.path.getsize(p)//1024, "KB")
# gym hall: top strip only of a photo with children in it (y 0-455 holds no people: ceiling, windows, blue padded wall)
im = Image.open(os.path.join(SRC, "2024_07_IMG-20240702-WA0102.jpg")).convert("RGB").crop((0, 0, 1600, 455))
im.save(os.path.join(OUT, "gym-hall.jpg"), quality=85, optimize=True, progressive=True); print("gym-hall", im.size)
# logo (their circle badge, transparent PNG) + horizontal logo
for n, s in [("logo-circle", "2026_07_Circle-Logo-transparent-background.png"), ("logo-wide", "2024_04_logo3_big.png")]:
    p, sz = save(n, s, 320 if n == "logo-circle" else 600, "png"); print(n, sz, os.path.getsize(p)//1024, "KB")
# staff portraits (already public on their Our Staff page) -> 420px wide, mapped by name from the page HTML
rows = json.load(open(os.path.join(SRC, "..", "staff.json")))
staff = []
for src, name, role in rows:
    name, role = name.strip(), " ".join(role.split())
    f = None
    if src and "Circle-Logo" not in src:
        fn = src.split("/uploads/")[-1].replace("/", "_")
        if os.path.exists(os.path.join(SRC, fn)): f = fn
    slug = None
    if f:
        slug = "staff-" + "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-").replace("--", "-")
        save(slug, f, 420)
    staff.append({"name": name, "role": role, "photo": slug})
json.dump(staff, open(os.path.join(os.path.dirname(__file__), "staff.json"), "w"), indent=1, ensure_ascii=False)
print(len(staff), "staff;", sum(1 for s in staff if s["photo"]), "with photos")
