#!/usr/bin/env python3
"""Builds the Southern Lumber & Supply spec-draft site into public/southern-lumber-supply/draft/.
Run from the repo root:  python3 tools/southern-lumber-supply/build.py   (photos: tools/southern-lumber-supply/photos.py, run once)

FACT RULE: everything below comes from the business's own website (southernlumbersupply.com, read 2026-10-09), its Facebook/Instagram,
its Google listings, or Brandon's own direction. Anything not confirmed is a visible yellow "[Draft preview ...]" note or a [placeholder].
NAME: Brandon's direction (2026-10-09): the wordmark reads "Southern Lumber & Supply" with "Lumber & Building Supplies" big beside it.
The business's current name everywhere else is "Southern Lumber Supply"; this draft shows the proposed lockup.
"""
import os, json, html, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "southern-lumber-supply", "draft")
BASE = "/southern-lumber-supply/draft/"
ORIGIN = "https://tektonbybigie.com"
NAME = "Southern Lumber & Supply"
LIVE = "https://www.southernlumbersupply.com"
PORTAL = "https://southernlumberportal.epicoranywhere.com/Signin.aspx"
FB = "https://www.facebook.com/SouthernLumberSupply"
IG = "https://www.instagram.com/southernlumbersupply/"
LI = "https://www.linkedin.com/company/southern-lumber-supply/"
PH_AL, TEL_AL = "334-489-WOOD", "+13344899663"
PH_FL, TEL_FL = "(850) 788-5300", "+18507885300"
OG_IMAGE = ORIGIN + BASE + "assets/photos/hero-framing.jpg"

e = lambda s: html.escape(s, quote=True)
u = lambda p="": BASE + p
PH = lambda t: f'<span style="background:#fff3b0;border-radius:3px;padding:0 5px">[{e(t)}]</span>'
DRAFT_NOTES = True
DN = lambda t: f'<p class="note">[Draft preview &mdash; {t}]</p>' if DRAFT_NOTES else ""
written = []

STORES = [
    dict(slug="dothan-zenith-road", short="Dothan, Zenith Road", name="Lumber, Pro Desk &amp; Door Shop", full="Southern Lumber &amp; Supply, Zenith Road",
         addr="114 Zenith Rd", city="Dothan, AL 36303", phone=PH_AL, tel=TEL_AL, hours="Mon&ndash;Fri 7:00 AM &ndash; 4:30 PM", closed="Sat &amp; Sun closed",
         img="store-zenith", lat=31.2549716, lng=-85.4067209, stype="HardwareStore",
         blurb="Our main lumber yard and Pro Desk. The Zenith Road store also has one of the area&rsquo;s only interior and exterior door shops, where we build new door units and &ldquo;retrofit&rdquo; units for any replacement job."),
    dict(slug="dothan-bic-road", short="Dothan, Bic Road", name="Vinyl &amp; Roofing", full="Southern Lumber &amp; Supply, Vinyl &amp; Roofing",
         addr="519 Bic Rd", city="Dothan, AL 36303", phone=PH_AL, tel=TEL_AL, hours="Mon&ndash;Fri 7:00 AM &ndash; 4:00 PM", closed="Sat &amp; Sun closed",
         img="store-bic", lat=31.2478, lng=-85.3839, stype="HardwareStore",
         blurb="The professional source for roofing and vinyl-siding materials, with in-stock soffit and vinyl siding, trim coil, shingles and other materials. We also specialize in screen rooms: stop in for a free project estimate."),
    dict(slug="dothan-installit", short="Dothan, Installit! Showroom", name="Installit! Showroom", full="Installit! by Southern Lumber &amp; Supply",
         addr="3246 Ross Clark Cir #1", city="Dothan, AL 36303", phone=PH_AL, tel=TEL_AL, hours="Mon&ndash;Fri 9:00 AM &ndash; 5:00 PM", closed="Sat &amp; Sun closed",
         img="store-installit", lat=31.2355924, lng=-85.4311893, stype="HomeAndConstructionBusiness",
         blurb="Our showroom and installation team. You pick it out and our pros install it: windows, doors, cabinets, siding, decks and more, for homeowners and commercial customers."),
    dict(slug="lynn-haven", short="Lynn Haven (Panama City area)", name="Lynn Haven Store", full="Southern Lumber &amp; Supply, Lynn Haven",
         addr="201 Mosley Dr", city="Lynn Haven, FL 32444", phone=PH_FL, tel=TEL_FL, hours="Mon&ndash;Fri 6:30 AM &ndash; 4:30 PM", closed="Sat &amp; Sun closed",
         img="store-lynnhaven", lat=30.2109, lng=-85.6478, stype="HardwareStore",
         blurb="Our Florida Panhandle store, serving Panama City, Panama City Beach and the surrounding area with building materials, custom doors and windows."),
]
S = {s["slug"]: s for s in STORES}
dirs = lambda s: "https://www.google.com/maps/dir/?api=1&destination=" + urllib.parse.quote(f'{html.unescape(s["addr"])}, {s["city"]}')

NAV_PRODUCTS = [("Lumber &amp; Building Materials", "lumber-building-materials/"), ("Vinyl &amp; Roofing", "vinyl-roofing/"),
                ("Doors, Windows &amp; Cabinets", "doors-windows-cabinets/"), ("Pro Desk for Contractors", "pro-desk/")]
NAV_ABOUT = [("Our Story", "about/"), ("Meet the Team", "team/"), ("Careers", "careers/")]


def ld(blocks):
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>" for b in blocks)


def org_ld():
    return {"@context": "https://schema.org", "@type": "Organization", "@id": ORIGIN + u("#org"), "name": NAME, "url": ORIGIN + u(""),
            "logo": ORIGIN + u("assets/photos/their-logo.png"), "foundingDate": "1977",
            "sameAs": [FB, IG, LI], "description": "Lumber and building supplies, custom doors, windows, cabinets, roofing, vinyl siding and installation in Dothan, AL and Lynn Haven, FL."}


def store_ld(s):
    return {"@context": "https://schema.org", "@type": s["stype"], "name": html.unescape(s["full"]), "url": ORIGIN + u(f"locations/{s['slug']}/"),
            "telephone": s["tel"], "image": ORIGIN + u(f"assets/photos/{s['img']}.jpg"),
            "address": {"@type": "PostalAddress", "streetAddress": html.unescape(s["addr"]), "addressLocality": s["city"].split(",")[0],
                        "addressRegion": s["city"].split(",")[1].strip().split(" ")[0], "postalCode": s["city"].split(" ")[-1], "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lng"]},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}],
            "parentOrganization": {"@id": ORIGIN + u("#org")}}


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": html.unescape(n), "item": ORIGIN + u(p)} for i, (n, p) in enumerate(trail)]}


def head(title, desc, path, blocks, bc=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#90182a">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{ORIGIN}{u(path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&family=Playfair+Display:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/site.css')}">
{ld(blocks)}
</head>
<body{(' class="' + bc + '"') if bc else ""}>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    def dd(label, items, key, href):
        subs = "".join(f'<a href="{u(p)}">{n}</a>' for n, p in items)
        cls = ' class="on"' if active and active.startswith(key) else ""
        return f'<div class="dd"><a href="{u(href)}"{cls}>{label}</a><div class="sub">{subs}</div></div>'
    prod = dd("Products", NAV_PRODUCTS, "prod", "lumber-building-materials/")
    locs = dd("Locations", [(s["short"], f"locations/{s['slug']}/") for s in STORES] + [("All locations", "locations/")], "loc", "locations/")
    about = dd("About", NAV_ABOUT, "about", "about/")
    on = lambda k: ' class="on"' if active == k else ""
    links = (prod + f'<a href="{u("installit/")}"{on("installit")}>Installit!</a><a href="{u("projects/")}"{on("projects")}>Projects</a>'
             + locs + about + f'<a href="{u("contact/")}"{on("contact")}>Contact</a>')
    m = "".join(f'<a href="{u(p)}">{n}</a>' for n, p in [("Home", "")] + NAV_PRODUCTS + [("Installit!", "installit/"), ("Projects", "projects/"), ("Locations", "locations/")] + NAV_ABOUT + [("Contact", "contact/")])
    return f"""<div class="util"><div class="wrap">
  <div class="l"><a href="tel:{TEL_AL}">Dothan, AL &middot; {PH_AL}</a><a href="tel:{TEL_FL}">Lynn Haven, FL &middot; {PH_FL}</a></div>
  <div class="r"><a href="{LIVE}/" target="_blank" rel="noopener">Shop online</a><a href="{PORTAL}" target="_blank" rel="noopener">Customer portal</a><a href="{u('careers/')}">Careers</a></div>
</div></div>
<header class="top"><div class="wrap top-inner">
  <a class="brand" href="{u()}" aria-label="{e(NAME)}, home"><span class="mark"><b>Southern</b><i>Lumber &amp; Supply</i></span><span class="tag">Lumber &amp; Building Supplies<small>Dothan, AL &middot; Lynn Haven, FL</small></span></a>
  <nav class="main" aria-label="Main">{links}</nav>
  <div class="top-cta"><a class="btn" href="{u('locations/')}">Find a store</a><button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mnav">Menu</button></div>
</div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">{m}</nav>
<main id="main">
"""


def footer():
    stores = "".join(f'<li><a href="{u("locations/" + s["slug"] + "/")}">{s["short"]}</a></li>' for s in STORES)
    return f"""</main>
<footer class="site-footer"><div class="wrap">
  <div class="fgrid">
    <div><span class="mark" style="margin-bottom:14px"><b>Southern</b><i>Lumber &amp; Supply</i></span>
      <p class="small">Lumber &amp; building supplies for the Wiregrass and the Florida Panhandle. Since 1977.</p>
      <p class="small">Dothan, AL: <a href="tel:{TEL_AL}">{PH_AL}</a><br>Lynn Haven, FL: <a href="tel:{TEL_FL}">{PH_FL}</a></p>
      <div class="social"><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></div></div>
    <div><h4>Products</h4><ul>{"".join(f'<li><a href="{u(p)}">{n}</a></li>' for n, p in NAV_PRODUCTS)}<li><a href="{u('installit/')}">Installit!</a></li></ul></div>
    <div><h4>Locations</h4><ul>{stores}</ul></div>
    <div><h4>Company</h4><ul>{"".join(f'<li><a href="{u(p)}">{n}</a></li>' for n, p in NAV_ABOUT)}<li><a href="{u('projects/')}">Projects</a></li><li><a href="{u('contact/')}">Contact</a></li></ul></div>
    <div><h4>Customers</h4><ul><li><a href="{LIVE}/" target="_blank" rel="noopener">Shop online</a></li><li><a href="{PORTAL}" target="_blank" rel="noopener">Customer portal</a></li><li><a href="{LIVE}/privacy-policy" target="_blank" rel="noopener">Privacy policy</a></li><li><a href="{LIVE}/terms-conditions" target="_blank" rel="noopener">Terms &amp; conditions</a></li></ul></div>
  </div>
  <div class="fbase">&copy; 2026 Southern Lumber &amp; Supply &middot; Lumber &amp; Building Supplies &middot; Dothan, AL &amp; Lynn Haven, FL
    <p class="note" style="margin-top:16px">[Draft preview &mdash; the name and logo lockup in this draft (&ldquo;Southern Lumber &amp; Supply&rdquo; with &ldquo;Lumber &amp; Building Supplies&rdquo; beside it) is our proposal. Your current logo, for comparison: <img src="{u('assets/photos/their-logo.png')}" alt="Current Southern Lumber Supply logo" style="display:inline-block;height:34px;width:auto;vertical-align:middle;margin-left:8px;border-radius:3px">]</p></div>
</div></footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons"><span class="ghost-chevron down"><span></span><span></span></span><span class="ghost-chevron up"><span></span><span></span></span></div>
  <p>tektonbybigie.com/southern-lumber-supply/draft &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def photo(name, alt, cls="", cap="", ext="jpg", eager=False):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="photo {cls}"><img src="{u("assets/photos/" + name + "." + ext)}" alt="{e(alt)}"{"" if eager else " loading=lazy"}>{c}</figure>'


def crumbs(trail):
    parts = [f"<b>{n}</b>" if i == len(trail) - 1 else f'<a href="{u(p)}">{n}</a>' for i, (n, p) in enumerate(trail)]
    return '<p class="crumbs">' + "<span>/</span>".join(parts) + "</p>"


SHARP = {"hero-framing", "store-zenith"}   # only these photos are big enough to use as full-width banners


def page_hero(trail, h1, lede, bg):
    style = f' style="background-image:url(\'{u("assets/photos/" + bg + ".jpg")}\')"' if bg in SHARP else ""
    plain = "" if bg in SHARP else " plain"
    return f"""<section class="page-hero{plain}"{style}><div class="wrap">
  {crumbs(trail)}<h1>{h1}</h1><p class="lede">{lede}</p></div></section>
"""


def assemble(path, title, desc, active, body, blocks):
    return head(title, desc, path, blocks) + header(active) + body + footer()


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    written.append(path or "(home)")


def cta_band(h="Stop in or give us a call", t="Dothan, AL &middot; 334-489-WOOD &nbsp;|&nbsp; Lynn Haven, FL &middot; (850) 788-5300"):
    return f"""<section class="section red cta"><div class="wrap"><h2>{h}</h2><p class="lede" style="margin-inline:auto;color:#f3d9dc">{t}</p>
  <div class="btns"><a class="btn light" href="{u('locations/')}">Find a store</a><a class="btn outline-w" href="{u('contact/')}">Send us a message</a></div></div></section>"""


def store_card(s, detail=True):
    return f"""<article class="card store">
  <img src="{u('assets/photos/' + s['img'] + '.jpg')}" alt="{e(html.unescape(s['full']))} storefront" loading="lazy">
  <h3>{s['short']}</h3><p class="addr">{s['addr']}<br>{s['city']}</p>
  <dl><dt>Call</dt><dd><a href="tel:{s['tel']}">{s['phone']}</a></dd><dt>Hours</dt><dd>{s['hours']}<br>{s['closed']}</dd></dl>
  <div class="btns"><a class="btn" href="{u('locations/' + s['slug'] + '/')}">Store details</a><a class="btn ghost" href="{dirs(s)}" target="_blank" rel="noopener">Directions</a></div></article>"""


REVIEWS = [
    ("Stephen M.", "Great staff from in the office to out in the field and in the warehouse. Great people all around."),
    ("Charles M.", "Southern Lumber supply is excellent to work with and will get you your product in a timely fashion. I have been nothing but satisfied dealing with them."),
    ("Clay A.", "From what I did see the store is well stocked up and the aisles are clean and free of clutter. The staff seems to be knowledgeable and helpful."),
]


def reviews_block():
    cards = "".join(f'<div class="review"><div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;{e(t)}&rdquo;</p><p class="who">{e(n)} &middot; Google review</p></div>' for n, t in REVIEWS)
    return f'<div class="reviews">{cards}</div><p class="rating-line">4.3 on Google from 40 reviews at the Zenith Road store (checked Oct 9, 2026).</p>'


# ================================================================== HOME
def home():
    desc = "Lumber & building supplies in Dothan, AL and Lynn Haven, FL: lumber, siding, roofing, custom doors, windows, cabinets, hardware and installation. Delivery up to 125 miles."
    body = f"""<section class="hero" style="background-image:url('{u('assets/photos/hero-framing.jpg')}')"><div class="wrap">
  <p class="kicker" style="color:#f0b8bf"><span style="display:none"></span>Since 1977 &middot; Dothan, AL &amp; Lynn Haven, FL</p>
  <h1>Everything to build it. <em>Everyone to install it.</em></h1>
  <p class="lede">Professional-grade lumber and building supplies, siding and roofing, custom doors, windows and cabinets, plus a team that installs them. We deliver up to 125 miles.</p>
  <div class="btns"><a class="btn" href="{u('locations/')}">Find a store</a><a class="btn outline-w" href="tel:{TEL_AL}">Call {PH_AL}</a><a class="btn outline-w" href="{LIVE}/" target="_blank" rel="noopener">Shop online</a></div>
</div></section>

<section class="finder"><div class="wrap"><div class="finder-card">
  <h2>Find your store</h2>
  <div class="stores">{"".join(f'<a href="{u("locations/" + s["slug"] + "/")}">{s["short"]}</a>' for s in STORES)}</div>
  <a class="phone" href="tel:{TEL_AL}"><small>Dothan &amp; everywhere</small>{PH_AL}</a>
</div></div></section>

<section class="section"><div class="wrap">
  <div class="head"><p class="kicker">What do you need?</p><h2>Lumber &amp; building supplies, <span style="color:var(--red)">and the people who install them.</span></h2></div>
  <div class="tiles">
    <a class="tile" href="{u('lumber-building-materials/')}"><img src="{u('assets/photos/hero-framing.jpg')}" alt="A new house framed with roof trusses at dusk" loading="lazy"><div class="t"><h3>Lumber &amp; Building Materials</h3><p>Framing lumber, plywood, engineered wood, trusses, millwork, hardware and more.</p><span class="go">Explore &rarr;</span></div></a>
    <a class="tile" href="{u('vinyl-roofing/')}"><img src="{u('assets/photos/roof-aerial.jpg')}" alt="Aerial view of a new shingle roof with vinyl siding" loading="lazy"><div class="t"><h3>Vinyl &amp; Roofing</h3><p>In-stock shingles, soffit, vinyl siding and trim coil, plus screen rooms.</p><span class="go">Explore &rarr;</span></div></a>
    <a class="tile" href="{u('doors-windows-cabinets/')}"><img src="{u('assets/photos/doors-boxes.jpg')}" alt="Packaged doors and windows stacked at a job site" loading="lazy"><div class="t"><h3>Doors, Windows &amp; Cabinets</h3><p>Custom doors built in our on-site door shop, windows and cabinets.</p><span class="go">Explore &rarr;</span></div></a>
    <a class="tile" href="{u('installit/')}"><img src="{u('assets/photos/install-door.jpg')}" alt="An Installit! installer fitting a sliding glass door" loading="lazy"><div class="t"><h3>Installit!</h3><p>Pick it out and our installers do the rest. Free consultations.</p><span class="go">Explore &rarr;</span></div></a>
  </div>
</div></section>

<section class="stats"><div class="wrap"><ul>
  <li><b>Since 1977</b><span>family-owned</span></li><li><b>4 stores</b><span>Dothan, AL &amp; Lynn Haven, FL</span></li>
  <li><b>125 miles</b><span>jobsite delivery</span></li><li><b>Free takeoffs</b><span>for your project</span></li></ul></div></section>

<section class="section dark pro"><div class="wrap">
  <div class="head"><p class="kicker" style="color:#f0b8bf">The Pro Desk</p><h2>Contractors count on us.</h2>
    <p class="lede">A complete selection of building materials, a Pro Desk that knows your job, and delivery to the site.</p></div>
  <div class="feature-grid">
    <div class="feature"><h3>Free takeoffs</h3><p>Send us the plans and we price the materials for the job.</p></div>
    <div class="feature"><h3>Jobsite delivery</h3><p>We deliver building supplies up to 125 miles.</p></div>
    <div class="feature"><h3>One-stop selection</h3><p>Lumber, plywood, engineered wood, millwork and trusses, plus insulation, roofing, siding, jobsite tools and grab-and-go snacks and drinks.</p></div>
  </div>
  <div class="btns"><a class="btn light" href="{u('pro-desk/')}">Visit the Pro Desk</a><a class="btn outline-w" href="{PORTAL}" target="_blank" rel="noopener">Customer portal sign-in</a></div>
</div></section>

<section class="section"><div class="wrap split">
  {photo('doors-boxes', 'Packaged doors and windows stacked at a job site', 'tall')}
  <div><p class="kicker">Door Shop</p><h2>Built here. Made to fit.</h2>
    <p>The Zenith Road store has one of the area&rsquo;s only interior and exterior door shops. We build new door units and &ldquo;retrofit&rdquo; units for any replacement job, and design and build customized solutions for any home.</p>
    <ul class="checks"><li>Steel, fiberglass and aluminum-clad doors</li><li>Impact and non-impact options</li><li>Windows in vinyl, wood and aluminum clad</li><li>In-store showroom</li></ul>
    <div class="btns"><a class="btn" href="{u('doors-windows-cabinets/')}">See doors &amp; windows</a></div></div>
</div></section>

<section class="section cream"><div class="wrap split rev">
  <div><img class="logo-chip" src="{u('assets/photos/installit-logo.png')}" alt="Installit!">
    <h2>You pick it out. We install it.</h2>
    <p>Installit! by Southern Lumber &amp; Supply is the area&rsquo;s one-stop shop for home improvement. We sell and install windows, doors, cabinets, siding, decks and so much more, for homeowners and commercial customers.</p>
    <ul class="checks"><li>Free consultations at your home or in our showroom</li><li>Experienced sales staff and elite installers</li><li>Financing available upon request</li></ul>
    <div class="btns"><a class="btn" href="{u('installit/')}">See Installit!</a><a class="btn ghost" href="tel:{TEL_AL}">Call {PH_AL}</a></div></div>
  {photo('store-installit', 'The Installit! showroom storefront in Dothan', 'wide')}
</div></section>

<section class="section"><div class="wrap">
  <div class="head"><p class="kicker">Recent jobs</p><h2>Work we&rsquo;ve supplied.</h2></div>
  <div class="gallery">
    <figure class="tall"><img src="{u('assets/photos/project-exterior.jpg')}" alt="A two-story exterior being finished with white trim and tall windows, Inlet Beach" loading="lazy"><figcaption>Exterior details, Inlet Beach</figcaption></figure>
    <figure><img src="{u('assets/photos/roofer.jpg')}" alt="A roofer nailing roof sheathing" loading="lazy"><figcaption>Roof decking</figcaption></figure>
    <figure><img src="{u('assets/photos/house-porch.jpg')}" alt="A new home with columns and a covered front porch" loading="lazy"><figcaption>Columns &amp; porch</figcaption></figure>
    <figure><img src="{u('assets/photos/roof-aerial.jpg')}" alt="A shingle roof from above" loading="lazy"><figcaption>Shingles &amp; siding</figcaption></figure>
  </div>
  <div class="btns"><a class="btn ghost" href="{u('projects/')}">See all projects</a></div>
  {DN("these photos come from your website and Instagram. Send your best full-size job photos (with the town and what we supplied) and we will fill this gallery.")}
</div></section>

<section class="section sand"><div class="wrap">
  <div class="head"><p class="kicker">What customers say</p><h2>Great staff, well stocked.</h2></div>
  {reviews_block()}
  {DN("these three quotes are from your Google reviews. Ratings change, so we will refresh them before launch.")}
</div></section>

<section class="section"><div class="wrap">
  <div class="head"><p class="kicker">Four stores</p><h2>Find us.</h2></div>
  <div class="cards four">{"".join(store_card(s) for s in STORES)}</div>
</div></section>

<section class="section cream"><div class="wrap">
  <div class="head center"><p class="kicker">Brands we carry</p><h2>Names you know.</h2></div>
  <div class="brands"><img src="{u('assets/photos/brand-milwaukee.png')}" alt="Milwaukee" loading="lazy"><img src="{u('assets/photos/brand-midwest.png')}" alt="Midwest Fastener" loading="lazy"><img src="{u('assets/photos/brand-sierra.png')}" alt="Sierra Pacific Windows" loading="lazy"><img src="{u('assets/photos/brand-diablo.png')}" alt="Diablo" loading="lazy"></div>
  <div class="brandtext"><span>Huber ZIP System</span><span>Advantech</span><span>LP</span><span>House of Forgings</span><span>Novo</span><span>LJ Smith</span><span>Maytag water softeners</span></div>
</div></section>
{cta_band()}"""
    write("", assemble("", "Lumber & Building Supplies in Dothan, AL and Lynn Haven, FL | Southern Lumber & Supply", desc, None, body, [org_ld()] + [store_ld(s) for s in STORES]))


# ================================================================== PRODUCT PAGES
def products_page(path, title, h1, lede, bg, desc, intro_html, items, side_photo, side_alt, extra=""):
    trail = [("Home", ""), ("Products", "lumber-building-materials/"), (title, path)]
    prod = "".join(f"<div><h3>{n}</h3><p>{t}</p></div>" for n, t in items)
    body = page_hero(trail, h1, lede, bg) + f"""
<section class="section"><div class="wrap split">
  <div>{intro_html}<div class="btns"><a class="btn" href="{u('locations/')}">Find a store</a><a class="btn ghost" href="tel:{TEL_AL}">Call {PH_AL}</a></div></div>
  {photo(side_photo, side_alt, 'tall')}
</div></section>
<section class="section cream"><div class="wrap"><div class="head"><p class="kicker">What we carry</p><h2>The details.</h2></div><div class="prod">{prod}</div>{extra}</div></section>
{cta_band()}"""
    write(path, assemble(path, f"{title} in Dothan, AL and Lynn Haven, FL | Southern Lumber & Supply", desc, "prod" + path, body,
                         [crumbs_ld(trail), org_ld()]))


def products():
    products_page("lumber-building-materials/", "Lumber & Building Materials", "Lumber &amp; building materials",
        "Framing lumber to finishing touches, with free takeoffs and jobsite delivery.", "hero-framing",
        "Framing lumber, plywood, engineered wood, trusses, millwork, foundation products, decks and hardware in Dothan, AL and Lynn Haven, FL. Free takeoffs and delivery up to 125 miles.",
        "<p class=\"kicker\">From the foundation up</p><h2>Everything for the build.</h2><p>We believe every exceptional home deserves exceptional building supplies. Contractors, builders and homeowners rely on us for new homes, renovations and large-scale construction, from the foundation to the finishing touches.</p><ul class=\"checks\"><li>Free estimates and free takeoffs</li><li>Jobsite delivery up to 125 miles</li><li>On-site custom door shop and in-store showroom</li><li>Hardware, fasteners and key cutting</li></ul>",
        [("Lumber, engineered wood &amp; trusses", "Yellow pine, treated yellow pine (MCA and CCA treated), spruce, spruce studs, pine studs and Framer Series studs."),
         ("Sheathing", "Plywood, birch plywood, fire-rated plywood, treated plywood, AC and MVF plywood, OSB, Huber ZIP System and T1-11 pine siding."),
         ("Subfloor", "Advantech, LP 350 and Edge Gold, plus cypress and cedar products."),
         ("Millwork", "Trim and moulding (primed and clear), baseboards, crown molding, chair rail, window and door casing, shoe molding, window stool, rosettes and decorative moldings."),
         ("Foundation products", "Block, rebar, wire mesh, loop tie, mesh chairs, rod chairs, metal grade stakes and anchor bolts."),
         ("Stairs &amp; railings", "House of Forgings stair and railing, Novo and LJ Smith."),
         ("Decks &amp; patios", "Composite decking and screen rooms."),
         ("Exterior finishes", "Columns, siding, roofing and exterior products."),
         ("Hardware &amp; fasteners", "A full range of building and hardware supplies."),
         ("Cabinets &amp; showroom supplies", "Cabinets and showroom supplies, with an in-store window and door showroom.")],
        "doors-boxes", "Packaged doors and windows stacked at a job site")
    products_page("vinyl-roofing/", "Vinyl & Roofing", "Vinyl &amp; roofing",
        "The professional source for roofing and vinyl-siding materials, in stock on Bic Road in Dothan.", "roof-aerial",
        "Roofing, shingles, soffit, vinyl siding, trim coil and screen rooms at our Bic Road store in Dothan, AL. Free screen-room estimates, contractor services and delivery.",
        "<p class=\"kicker\">Bic Road, Dothan</p><h2>In stock and ready to go.</h2><p>We are the professional source for roofing and vinyl-siding materials, with in-stock soffit and vinyl siding, trim coil, shingles and other materials. We also specialize in screen rooms: see us for a free project estimate.</p><ul class=\"checks\"><li>Contractor services</li><li>Delivery</li><li>Doors &amp; windows</li><li>Free assembly</li></ul><p><b>519 Bic Rd, Dothan, AL 36303</b><br>Mon&ndash;Fri 7:00 AM &ndash; 4:00 PM &middot; <a href=\"tel:" + TEL_AL + "\">" + PH_AL + "</a></p>",
        [("Roofing", "Shingles and roofing materials, available for contractors and homeowners."),
         ("Vinyl siding", "In-stock vinyl siding with matching soffit and trim coil."),
         ("Soffit &amp; trim", "In-stock soffit and trim coil for a clean exterior finish."),
         ("Screen rooms", "Free project estimates on screen rooms."),
         ("Exterior products", "Roofing, siding, vinyl and exterior products, including columns."),
         ("Delivery &amp; contractor services", "Jobsite delivery and contractor services from the Bic Road store.")],
        "store-bic", "The inside of the Vinyl & Roofing store counter and showroom")
    products_page("doors-windows-cabinets/", "Doors, Windows & Cabinets", "Doors, windows &amp; cabinets",
        "Custom doors built in our own door shop, plus windows, cabinets and a showroom.", "doors-boxes",
        "Custom interior and exterior doors, windows and cabinets in Dothan, AL: on-site door shop, in-store showroom, steel, fiberglass, aluminum-clad, impact and non-impact options.",
        "<p class=\"kicker\">The Door Shop &middot; Zenith Road</p><h2>One of the area&rsquo;s only door shops.</h2><p>The Zenith Road location features one of the area&rsquo;s only interior and exterior door shops, where we build new door units and &ldquo;retrofit&rdquo; units for any replacement job. We design and build customized solutions for any home.</p><ul class=\"checks\"><li>On-site custom door shop</li><li>In-store window and door showroom</li><li>Free estimates</li><li>Installation by Installit!</li></ul>",
        [("Custom interior &amp; exterior doors", "Steel, fiberglass, aluminum clad, impact and non-impact."),
         ("Windows &amp; shutters", "Vinyl, wood, aluminum clad, Turtle Glass, impact and non-impact."),
         ("Cabinets", "A curated cabinet selection from respected manufacturers."),
         ("Stairs &amp; railings", "House of Forgings stair and railing, Novo and LJ Smith."),
         ("Showroom", "See the products in person at our window and door showroom."),
         ("Installation", "Our Installit! team can install what you pick out.")],
        "doors-boxes", "Packaged doors and windows stacked at a job site",
        extra=DN("custom door builds and your window brands come from your Services &amp; Products page. Tell us your most-requested door styles and which window brands you stock, and we will feature them."))


# ================================================================== INSTALLIT!
II_LOGO = lambda cls="": f'<img class="{cls}" src="{u("assets/photos/installit-logo.png")}" alt="Installit! by Southern Lumber &amp; Supply">'


def ii_header():
    links = [("What we install", "#install"), ("How it works", "#how"), ("Showroom", "#showroom"), ("Free consultation", "#consult")]
    nav = "".join(f'<a href="{h}">{n}</a>' for n, h in links)
    m = "".join(f'<a href="{h}">{n}</a>' for n, h in links) + f'<a href="{u()}">Southern Lumber &amp; Supply home</a>'
    return f"""<div class="util ii-util"><div class="wrap">
  <div class="l"><a href="tel:{TEL_AL}">Call {PH_AL}</a><span>Showroom: 3246 Ross Clark Cir #1, Dothan, AL</span></div>
  <div class="r"><a href="{u()}">&larr; Southern Lumber &amp; Supply</a></div>
</div></div>
<header class="top"><div class="wrap top-inner">
  <a class="brand" href="{u('installit/')}" aria-label="Installit! by Southern Lumber &amp; Supply, home">{II_LOGO('ii-logo')}</a>
  <nav class="main" aria-label="Installit!">{nav}</nav>
  <div class="top-cta"><a class="btn" href="tel:{TEL_AL}">Call {PH_AL}</a><button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mnav">Menu</button></div>
</div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">{m}</nav>
<main id="main">
"""


def ii_footer():
    return f"""</main>
<footer class="site-footer ii-footer"><div class="wrap">
  <div class="ii-fgrid">
    <div><span class="ii-logo-chip">{II_LOGO('ii-logo')}</span>
      <p class="small">Windows, doors, cabinets, siding and decks: you pick it out and our pros install it. Serving the Wiregrass area and the Florida Panhandle.</p>
      <div class="social"><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a></div></div>
    <div><h4>Showroom</h4><p class="small">3246 Ross Clark Cir #1<br>Dothan, AL 36303<br><a href="tel:{TEL_AL}">{PH_AL}</a><br>Mon&ndash;Fri 9:00 AM &ndash; 5:00 PM<br>Sat &amp; Sun closed</p>
      <p class="small"><a href="{dirs(S['dothan-installit'])}" target="_blank" rel="noopener">Get directions</a></p></div>
    <div><h4>Installit!</h4><ul><li><a href="#install">What we install</a></li><li><a href="#how">How it works</a></li><li><a href="#showroom">Showroom</a></li><li><a href="#consult">Free consultation</a></li></ul></div>
    <div><h4>By Southern Lumber &amp; Supply</h4><ul><li><a href="{u()}">Southern Lumber &amp; Supply home</a></li><li><a href="{u('locations/')}">All four stores</a></li><li><a href="{u('pro-desk/')}">Pro Desk for contractors</a></li><li><a href="{LIVE}/" target="_blank" rel="noopener">Shop online</a></li></ul></div>
  </div>
  <div class="fbase">&copy; 2026 Installit! by Southern Lumber &amp; Supply &middot; Dothan, AL
    <p class="note" style="margin-top:16px">[Draft preview &mdash; Installit! is built here as its own brand with its own look, navigation and footer, and it stays linked to Southern Lumber &amp; Supply. It can live at southernlumbersupply.com/installit or, if you want, on its own web address.]</p></div>
</div></footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons"><span class="ghost-chevron down"><span></span><span></span></span><span class="ghost-chevron up"><span></span><span></span></span></div>
  <p>tektonbybigie.com/southern-lumber-supply/draft/installit &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def installit():
    path = "installit/"; trail = [("Home", ""), ("Installit!", path)]
    what = [("Windows &amp; doors", "Sold and installed by our team."),
            ("Cabinets", "Pick them out in the showroom; our installers fit them."),
            ("Siding", "For homeowners and commercial customers."),
            ("Decks", "Installed by our crew."),
            ("Screen rooms", "Free project estimates at our Bic Road store.")]
    tiles = "".join(f'<div class="card ii-tile"><h3>{n}</h3><p>{t}</p></div>' for n, t in what)
    body = f"""
<section class="ii-hero"><div class="wrap ii-hero-in">
  <div><p class="kicker">Installit! &middot; Dothan, AL &amp; the Florida Panhandle</p>
    <h1>You pick it out.<br><em>We install it.</em></h1>
    <p class="lede">Windows, doors, cabinets, siding, decks and more, sold and installed by one team. Free consultations at your home or in our showroom.</p>
    <div class="btns"><a class="btn" href="tel:{TEL_AL}">Call {PH_AL}</a><a class="btn outline-w" href="#consult">Free consultation</a></div>
    <ul class="ii-points"><li>Free consultations</li><li>Financing available upon request</li><li>Homeowners &amp; commercial</li></ul></div>
  {photo('install-door', 'An Installit! installer fitting a sliding glass door', 'ii-hero-photo', eager=True)}
</div></section>

<section class="section" id="install"><div class="wrap"><div class="head"><p class="kicker">What we install</p><h2>One call. Sold, installed, done.</h2>
  <p class="lede">Proudly serving the Wiregrass area and the Florida Panhandle, we sell and install windows, doors, cabinets, siding, decks and so much more. Our customers range from homeowners to commercial businesses.</p></div>
  <div class="cards ii-tiles">{tiles}</div>
  {DN("the list of what you install comes from your current Installit! page and your Instagram. Tell us anything to add or remove, and send before-and-after photos of finished installs.")}</div></section>

<section class="section cream" id="how"><div class="wrap"><div class="head"><p class="kicker">How it works</p><h2>From idea to installed.</h2></div>
  <div class="cards"><div class="card"><h3>1. Free consultation</h3><p>Meet with our sales staff at your home or in the showroom. We help you complete your project on time and within budget.</p></div>
  <div class="card"><h3>2. Pick it out</h3><p>Choose windows, doors, cabinets, siding or decking from the showroom and our supplier network.</p></div>
  <div class="card"><h3>3. We install it</h3><p>Our experienced installers handle the installation, so the finished job is done right.</p></div></div>
  <p style="margin-top:26px">No matter the project, Installit! by Southern Lumber &amp; Supply has relationships with nationwide suppliers to fit your needs, and if you like, we will take care of the installation. Contractor services and free assembly are available too.</p></div></section>

<section class="section" id="showroom"><div class="wrap split">
  <div><p class="kicker">The showroom</p><h2>Come see it in person.</h2>
    <p>Our Installit! showroom is at 3246 Ross Clark Cir #1 in Dothan. Stop in Monday to Friday, 9:00 AM to 5:00 PM, or call and we will set a time to meet at your home.</p>
    <div class="btns"><a class="btn" href="{dirs(S['dothan-installit'])}" target="_blank" rel="noopener">Get directions</a><a class="btn ghost" href="tel:{TEL_AL}">Call {PH_AL}</a></div></div>
  {photo('store-installit', 'The Installit! showroom storefront on Ross Clark Circle in Dothan', 'wide')}
</div></section>

<section class="section red cta" id="consult"><div class="wrap"><h2>Ready for a free consultation?</h2>
  <p class="lede" style="margin-inline:auto;color:#f3d9dc">{PH_AL} &middot; 3246 Ross Clark Cir #1, Dothan, AL</p>
  <div class="btns"><a class="btn light" href="tel:{TEL_AL}">Call {PH_AL}</a><a class="btn outline-w" href="{u('contact/')}">Send a message</a></div></div></section>
"""
    full = head("Installit! Window, Door & Cabinet Installation in Dothan, AL | Installit! by Southern Lumber & Supply",
                "Installit! by Southern Lumber & Supply sells and installs windows, doors, cabinets, siding and decks in Dothan, AL and the Florida Panhandle. Free consultations.",
                path, [crumbs_ld(trail), org_ld(), store_ld(S['dothan-installit'])], bc="ii") + ii_header() + body + ii_footer()
    write(path, full)


# ================================================================== PRO DESK
def pro_desk():
    path = "pro-desk/"; trail = [("Home", ""), ("Pro Desk", path)]
    body = page_hero(trail, "The Pro Desk", "Contractors count on our complete selection, free takeoffs and delivery to the jobsite.", "roofer") + f"""
<section class="section"><div class="wrap split">
  <div><p class="kicker">For builders &amp; contractors</p><h2>We know your job.</h2>
    <p>Contractors and homeowners alike rely on us for a comprehensive selection of building materials, including lumber, plywood, engineered wood products, millwork, trusses, windows, doors, roofing, siding and hardware.</p>
    <ul class="checks"><li>Free takeoffs on any project</li><li>Jobsite delivery up to 125 miles</li><li>Customer portal to manage your account</li><li>Jobsite tools, plus grab-and-go snacks and drinks</li><li>Contractor services and free assembly</li></ul>
    <div class="btns"><a class="btn" href="{PORTAL}" target="_blank" rel="noopener">Customer portal sign-in</a><a class="btn ghost" href="tel:{TEL_AL}">Call the Pro Desk</a></div>
    {DN("how does a contractor open an account (credit application, tax-exempt forms, a contact at the Pro Desk)? Tell us and we will add a clear step-by-step with the right forms. The Pro Desk phone on Google is (334) 792-1131, while your website shows 334-489-WOOD. Which should we publish?")}</div>
  {photo('roofer', 'A roofer nailing down roof sheathing', 'wide')}
</div></section>
<section class="section dark"><div class="wrap"><div class="head"><p class="kicker" style="color:#f0b8bf">Send us the plans</p><h2>Free takeoffs.</h2></div>
  <div class="feature-grid"><div class="feature"><h3>1. Send the plans</h3><p>Email or drop off your plans at the Pro Desk.</p></div><div class="feature"><h3>2. We price the job</h3><p>We take off the materials and give you a clear list.</p></div><div class="feature"><h3>3. We deliver</h3><p>Materials arrive at the jobsite, up to 125 miles away.</p></div></div></div></section>
{cta_band("Talk to the Pro Desk", "Dothan, AL &middot; 334-489-WOOD &nbsp;|&nbsp; Lynn Haven, FL &middot; (850) 788-5300")}"""
    write(path, assemble(path, "Pro Desk for Contractors: Free Takeoffs & Jobsite Delivery | Southern Lumber & Supply",
                         "Contractor services at Southern Lumber & Supply in Dothan, AL and Lynn Haven, FL: free takeoffs, jobsite delivery up to 125 miles, a full building-materials selection and a customer portal.", "prod" + path, body, [crumbs_ld(trail), org_ld()]))


# ================================================================== PROJECTS
def projects():
    path = "projects/"; trail = [("Home", ""), ("Projects", path)]
    ph = lambda t: f'<div class="ph">{t}</div>'
    body = page_hero(trail, "Projects", "Real jobs we have supplied and installed across the Wiregrass and the Florida Panhandle.", "hero-framing") + f"""
<section class="section"><div class="wrap">
  <div class="gallery">
    <figure class="tall"><img src="{u('assets/photos/project-exterior.jpg')}" alt="A two-story exterior being finished with white trim and tall windows, Inlet Beach" loading="lazy"><figcaption>Exterior details, Inlet Beach FL</figcaption></figure>
    <figure><img src="{u('assets/photos/hero-framing.jpg')}" alt="A new house framed with roof trusses at dusk" loading="lazy"><figcaption>Framing package</figcaption></figure>
    <figure><img src="{u('assets/photos/roof-aerial.jpg')}" alt="A shingle roof from above" loading="lazy"><figcaption>Roofing &amp; siding</figcaption></figure>
    <figure><img src="{u('assets/photos/install-door.jpg')}" alt="An installer fitting a sliding glass door" loading="lazy"><figcaption>Door installation</figcaption></figure>
    <figure><img src="{u('assets/photos/house-porch.jpg')}" alt="A new home with columns and a covered front porch" loading="lazy"><figcaption>Columns &amp; porch</figcaption></figure>
    <figure><img src="{u('assets/photos/roofer.jpg')}" alt="A roofer nailing down roof sheathing" loading="lazy"><figcaption>Roof decking</figcaption></figure>
    {ph("Your next project photo goes here")}{ph("Bay Point, Panama City")}
  </div>
  {DN("we filled this page with photos from your website and one from your Instagram. Your Instagram highlights are PCB, Custom Doors, Installit, Community, Projects and Lumber: send full-size photos from each (with the town and what we supplied) and we will organize this page the same way, with filters.")}
</div></section>
{cta_band("Have a project in mind?", "Call 334-489-WOOD (Dothan) or (850) 788-5300 (Lynn Haven)")}"""
    write(path, assemble(path, "Projects: Building Supplies, Doors & Roofing Jobs | Southern Lumber & Supply",
                         "Photos of jobs supplied and installed by Southern Lumber & Supply in Dothan, AL, Panama City, Panama City Beach and Inlet Beach, FL.", "projects", body, [crumbs_ld(trail), org_ld()]))


# ================================================================== LOCATIONS
def locations():
    path = "locations/"; trail = [("Home", ""), ("Locations", path)]
    body = page_hero(trail, "Four stores. One name.", "Three in Dothan, Alabama and one in Lynn Haven, Florida. Same people, same service.", "store-zenith") + f"""
<section class="section"><div class="wrap"><div class="cards four">{"".join(store_card(s) for s in STORES)}</div>
  {DN("the Lynn Haven store is called &ldquo;Panama City&rdquo; on your current website but Lynn Haven on Google and Facebook. We used Lynn Haven (the address is 201 Mosley Dr, Lynn Haven, FL 32444) and mention Panama City as the area. Your Google profile for the old Marianna store still says &ldquo;Temporarily closed&rdquo; and your home page still mentions Marianna: tell us whether it is closed for good and we will handle it.")}</div></section>
<section class="section cream"><div class="wrap"><div class="head"><p class="kicker">Where we deliver</p><h2>Delivery up to 125 miles.</h2><p class="lede">We deliver the building supplies for your entire home, up to 125 miles, across the Wiregrass area and the Florida Panhandle.</p></div></div></section>
{cta_band("Not sure which store?", "Call 334-489-WOOD and we will point you to the right one.")}"""
    write(path, assemble(path, "Locations: Dothan, AL and Lynn Haven, FL | Southern Lumber & Supply",
                         "Southern Lumber & Supply stores: 114 Zenith Rd, 519 Bic Rd and 3246 Ross Clark Cir in Dothan, AL, and 201 Mosley Dr in Lynn Haven, FL. Hours, phone and directions.", "loc", body, [crumbs_ld(trail), org_ld()] + [store_ld(s) for s in STORES]))
    for s in STORES:
        store_page(s)


def store_page(s):
    path = f"locations/{s['slug']}/"; trail = [("Home", ""), ("Locations", "locations/"), (s["short"], path)]
    mapq = urllib.parse.quote(f'{html.unescape(s["addr"])}, {s["city"]}')
    extra = {
        "dothan-zenith-road": ["Lumber, plywood, engineered wood, millwork and trusses", "Custom interior and exterior door shop", "Pro Desk, contractor services and free takeoffs", "Delivery, key cutting and free assembly"],
        "dothan-bic-road": ["In-stock soffit, vinyl siding, trim coil and shingles", "Screen rooms with free project estimates", "Contractor services, delivery and free assembly", "Doors &amp; windows"],
        "dothan-installit": ["Installation of windows, doors, cabinets, siding and decks", "In-store showroom", "Free consultations at your home or in the showroom", "Financing available upon request"],
        "lynn-haven": ["Building materials, custom doors and windows", "Lumber, molding and trim, roofing and siding", "Cabinets, hardware, decks and patios, stairs and railing", "Fences, screened rooms and installation"],
    }[s["slug"]]
    note = ("Your Instagram and Facebook list what you offer in Florida, but we do not have a store-by-store stock list: tell us what the Lynn Haven store carries and what is delivered from Dothan, and send a photo of the store, the team and the Pro Desk contact."
            if s["slug"] == "lynn-haven" else
            "hours and services come from your Find Us and store pages. Please check them, tell us the store manager&rsquo;s name and direct line, and send a few inside photos." if s["slug"] != "dothan-bic-road" else
            "hours and services come from your Vinyl &amp; Roofing page. Please check them, tell us the store manager&rsquo;s name and direct line, and send more photos (the inside photo here is small).")
    body = page_hero(trail, s["short"], s["blurb"], s["img"]) + f"""
<section class="section"><div class="wrap split">
  <div><p class="kicker">{s['name']}</p><h2>Visit us.</h2>
    <ul class="info"><li><b>Address</b><span>{s['addr']}<br>{s['city']}</span></li><li><b>Call</b><span><a href="tel:{s['tel']}">{s['phone']}</a></span></li><li><b>Hours</b><span>{s['hours']}<br>{s['closed']}</span></li></ul>
    <h3 style="margin-top:28px">What you will find</h3><ul class="checks">{"".join(f"<li>{x}</li>" for x in extra)}</ul>
    <div class="btns"><a class="btn" href="{dirs(s)}" target="_blank" rel="noopener">Get directions</a><a class="btn ghost" href="tel:{s['tel']}">Call this store</a></div>
    {DN(note)}</div>
  <div class="mapbox"><iframe title="Map to {e(html.unescape(s['full']))}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={mapq}&z=15&output=embed"></iframe></div>
</div></section>
<section class="section cream"><div class="wrap"><div class="head"><p class="kicker">The other stores</p><h2>Also near you.</h2></div><div class="cards">{"".join(store_card(o) for o in STORES if o is not s)}</div></div></section>
{cta_band()}"""
    write(path, assemble(path, f"{html.unescape(s['name'])}: {html.unescape(s['addr'])}, {s['city']} | Southern Lumber & Supply",
                         f"{html.unescape(s['full'])}: {html.unescape(s['addr'])}, {s['city']}. {html.unescape(s['hours'])}. Call {s['phone']}.", "loc" + path, body, [crumbs_ld(trail), store_ld(s)]))


# ================================================================== ABOUT, TEAM, CAREERS, CONTACT
def about():
    path = "about/"; trail = [("Home", ""), ("Our Story", path)]
    body = page_hero(trail, "Our story", "Founded in 1977 as Ansley&rsquo;s Building Materials. Family-owned and rooted in respect, service and integrity.", "store-zenith") + f"""
<section class="section"><div class="wrap split">
  <div><p class="kicker">Who we are</p><h2>Built on relationships.</h2>
    <p>Founded in 1977 as Ansley&rsquo;s Building Materials, our family-owned business has served homeowners, builders and contractors for decades. In 2013 we became Southern Lumber Supply, expanding our vision while honoring the values that built our reputation. Today we have four locations, and we still put our relationships first.</p>
    <p>We offer an elevated selection of premium building materials, complemented by generations of expertise and an uncompromising standard of personalized service.</p>
    {DN("your current About page says the business has served customers &ldquo;for nearly three decades,&rdquo; which does not match 1977, and an older page said &ldquo;more than 150 years.&rdquo; We used 1977. Please confirm the founding story and who is in the family.")}</div>
  {photo('store-zenith', 'The Zenith Road store in Dothan, Alabama', 'wide')}
</div></section>
<section class="section dark"><div class="wrap"><div class="head"><p class="kicker" style="color:#f0b8bf">Our mission</p><h2>&ldquo;An experience rooted in respect, service, and integrity.&rdquo;</h2>
  <p class="lede">To provide our customers, vendors, and associates with an experience rooted in respect, service, and integrity, as we work together to help realize the American dream.</p></div>
  <div class="feature-grid"><div class="feature"><h3>Respect</h3><p>We treat everyone with courtesy, politeness, and kindness, and value sharing opinions and ideas.</p></div>
  <div class="feature"><h3>Integrity</h3><p>We do the right thing, upholding honest and ethical standards in every part of our business.</p></div>
  <div class="feature"><h3>Accountability</h3><p>We take ownership of our actions and hold ourselves to the highest standards.</p></div></div></div></section>
{cta_band("Come meet us", "Four stores, one team.")}"""
    write(path, assemble(path, "Our Story: Since 1977 | Southern Lumber & Supply, Dothan AL",
                         "Southern Lumber & Supply started in 1977 as Ansley's Building Materials. Family-owned, with four locations in Dothan, AL and Lynn Haven, FL.", "about" + path, body, [crumbs_ld(trail), org_ld()]))


def team():
    path = "team/"; trail = [("Home", ""), ("Our Story", "about/"), ("Meet the Team", path)]
    people = [("staff-jay", "Jay Shipman", "President"), ("staff-brantley", "Brantley Brockett", "Vice President"),
              ("staff-donna", "Donna McDaniel", "Office Manager"), ("staff-steve", "Steve Hemendinger", "Director of Operations")]
    cards = "".join(f'<div class="person"><img src="{u("assets/photos/" + p + ".jpg")}" alt="Portrait of {n}, {r}" loading="lazy"><div class="b"><h3>{n}</h3><div class="role">{r}</div><div class="contact">Direct line: {PH("phone")}<br>Email: {PH("email")}</div></div></div>' for p, n, r in people)
    body = page_hero(trail, "Meet the team", "The people behind the counter, on the phone and out at the jobsite.", "store-zenith") + f"""
<section class="section"><div class="wrap">
  <div class="staff">{cards}</div>
  {DN("names, titles and photos are the ones on your current Staff page. Send each person&rsquo;s direct line and email (if they want it public), plus the Pro Desk lead, the door shop lead, the Installit! sales lead and the manager of each store, and we will add them with photos so customers know who to call.")}
</div></section>
<section class="section cream"><div class="wrap"><div class="head"><p class="kicker">Who to call</p><h2>Straight to the right person.</h2></div>
  <div class="cards four"><div class="card"><h3>Pro Desk &amp; takeoffs</h3><p><a href="tel:{TEL_AL}">{PH_AL}</a></p><p class="note" style="margin:0">{PH("contact name")}</p></div>
  <div class="card"><h3>Door shop</h3><p><a href="tel:{TEL_AL}">{PH_AL}</a></p><p class="note" style="margin:0">{PH("contact name")}</p></div>
  <div class="card"><h3>Installit!</h3><p><a href="tel:{TEL_AL}">{PH_AL}</a></p><p class="note" style="margin:0">{PH("contact name")}</p></div>
  <div class="card"><h3>Lynn Haven, FL</h3><p><a href="tel:{TEL_FL}">{PH_FL}</a></p><p class="note" style="margin:0">{PH("contact name")}</p></div></div></div></section>
{cta_band("Want to join them?", "See open positions on our careers page.")}"""
    write(path, assemble(path, "Meet the Team | Southern Lumber & Supply, Dothan AL & Lynn Haven FL",
                         "Meet the leadership team at Southern Lumber & Supply: Jay Shipman, Brantley Brockett, Donna McDaniel and Steve Hemendinger. Who to call for the Pro Desk, door shop and Installit!.", "about" + path, body, [crumbs_ld(trail), org_ld()]))


def careers():
    path = "careers/"; trail = [("Home", ""), ("Our Story", "about/"), ("Careers", path)]
    body = page_hero(trail, "Careers", "Join a family-owned team that puts relationships first.", "hero-framing") + f"""
<section class="section"><div class="wrap split">
  <div><p class="kicker">Work with us</p><h2>Come build with us.</h2>
    <p>We are a family-owned building-supply company with stores in Dothan, Alabama and Lynn Haven, Florida. We value respect, integrity and accountability, and we are always glad to meet good people.</p>
    <ul class="checks"><li>Sales and Pro Desk</li><li>Yard, warehouse and delivery</li><li>Door shop and millwork</li><li>Installation (Installit!)</li><li>Office and accounting</li></ul>
    {DN("your site has no careers page, and people search for &ldquo;Southern Lumber Supply careers.&rdquo; Tell us which roles are open at which stores and how to apply (email, application form or walk in), and we will list them here.")}</div>
  <div class="form"><h3>Tell us about yourself</h3>
    <div class="row"><div><label for="c-n">Name</label><input id="c-n" type="text" autocomplete="name"></div><div><label for="c-p">Phone</label><input id="c-p" type="tel" autocomplete="tel"></div></div>
    <label for="c-e">Email</label><input id="c-e" type="email" autocomplete="email">
    <label for="c-s">Store you would like to work at</label><select id="c-s"><option>Dothan, AL</option><option>Lynn Haven, FL</option><option>Either</option></select>
    <label for="c-m">What kind of work are you looking for?</label><textarea id="c-m" rows="4"></textarea>
    <button class="btn" type="button">Send</button><p style="margin:12px 0 0;font-size:.9rem;color:var(--steel)">Preview only: this form does not send yet.</p></div>
</div></section>
{cta_band("Prefer to stop in?", "Ask for the manager at any of our four stores.")}"""
    write(path, assemble(path, "Careers at Southern Lumber & Supply | Dothan, AL & Lynn Haven, FL",
                         "Jobs at Southern Lumber & Supply, a family-owned building-supply company in Dothan, AL and Lynn Haven, FL: sales, yard, door shop, installation and office.", "about" + path, body, [crumbs_ld(trail), org_ld()]))


def contact():
    path = "contact/"; trail = [("Home", ""), ("Contact", path)]
    body = page_hero(trail, "Contact us", "Call a store, send a message, or stop in.", "store-lynnhaven") + f"""
<section class="section"><div class="wrap split">
  <div><p class="kicker">Call or visit</p><h2>We are here Monday to Friday.</h2>
    <ul class="info"><li><b>Dothan</b><span><a href="tel:{TEL_AL}">{PH_AL}</a><br>Zenith Road &middot; Bic Road &middot; Installit! Showroom</span></li>
    <li><b>Lynn Haven</b><span><a href="tel:{TEL_FL}">{PH_FL}</a><br>201 Mosley Dr, Lynn Haven, FL 32444</span></li>
    <li><b>Email</b><span>{PH("general contact email")}</span></li>
    <li><b>Follow</b><span><a href="{FB}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{IG}" target="_blank" rel="noopener">Instagram</a> &middot; <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></span></li></ul>
    <div class="btns"><a class="btn" href="{u('locations/')}">All store hours</a><a class="btn ghost" href="{u('team/')}">Who to call</a></div></div>
  <div class="form"><h3>Send a message</h3>
    <div class="row"><div><label for="m-n">Name</label><input id="m-n" type="text" autocomplete="name"></div><div><label for="m-p">Phone</label><input id="m-p" type="tel" autocomplete="tel"></div></div>
    <label for="m-e">Email</label><input id="m-e" type="email" autocomplete="email">
    <label for="m-r">What can we help with?</label><select id="m-r"><option>A quote or takeoff</option><option>Doors, windows or cabinets</option><option>Installation (Installit!)</option><option>Roofing or vinyl</option><option>An order or account</option><option>Something else</option></select>
    <label for="m-m">Message</label><textarea id="m-m" rows="4"></textarea>
    <button class="btn" type="button">Send message</button></div>
</div>
{DN("this form is a preview and does not send anything yet. At launch it will email the address you choose. Your current Contact page has a form too; tell us where messages should go and who answers them.")}</section>
{cta_band()}"""
    write(path, assemble(path, "Contact Southern Lumber & Supply | Dothan, AL & Lynn Haven, FL",
                         "Contact Southern Lumber & Supply: Dothan, AL 334-489-WOOD, Lynn Haven, FL (850) 788-5300. Request a quote, a takeoff or an Installit! consultation.", "contact", body, [crumbs_ld(trail), org_ld()]))


if __name__ == "__main__":
    home(); products(); installit(); pro_desk(); projects(); locations(); about(); team(); careers(); contact()
    print(f"built {len(written)} pages into {OUT}:"); [print("  /" + w) for w in written]
