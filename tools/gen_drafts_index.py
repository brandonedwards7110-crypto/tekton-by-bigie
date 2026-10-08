#!/usr/bin/env python3
"""Writes public/_meta/draft/drafts.json: the list of every client draft (public/<slug>/draft/index.html) with its display name.
The Worker reads it (admin page: per-viewer draft checkboxes). It lives under a path with a 'draft' segment, so the Worker's
login gate keeps it private. Runs automatically before every `wrangler deploy` / `wrangler dev` ([build] in wrangler.toml)."""
import os, re, json, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUB = os.path.join(ROOT, "public")
out = []
for slug in sorted(os.listdir(PUB)):
    idx = os.path.join(PUB, slug, "draft", "index.html")
    if slug.startswith("_") or not os.path.isfile(idx):
        continue
    h = open(idx, encoding="utf-8", errors="ignore").read()
    m = re.search(r'property="og:site_name"\s+content="([^"]+)"', h)
    name = html.unescape(m.group(1)).strip() if m else ""
    if not name:
        t = re.search(r"<title>([^<]+)</title>", h)
        name = re.split(r"\s+[|—–-]\s+", html.unescape(t.group(1)).strip())[0] if t else ""
    if not name:
        name = slug.replace("-", " ").title()
    out.append({"slug": slug, "name": name})
dest = os.path.join(PUB, "_meta", "draft")
os.makedirs(dest, exist_ok=True)
json.dump(out, open(os.path.join(dest, "drafts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("drafts index:", ", ".join(d["slug"] for d in out))
