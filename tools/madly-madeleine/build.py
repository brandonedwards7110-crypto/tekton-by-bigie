#!/usr/bin/env python3
"""Builds the Madly Madeleine spec-draft site into public/madly-madeleine/draft/.
Run from the repo root:  python3 tools/madly-madeleine/build.py

FACT RULE: every claim on these pages must come from the business's own Facebook/Instagram posts,
Google listing or the photos themselves (see PROJECT-SUMMARY.md). Anything unconfirmed is a visible
[bracketed placeholder] so it can't be mistaken for fact on a pitch call.
"""
import os, json, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "madly-madeleine", "draft")
BASE = "/madly-madeleine/draft/"            # becomes "/" when the site gets its own domain
ORIGIN = "https://tektonbybigie.com"        # becomes https://madlymadeleine.com at launch

NAME = "Madly Madeleine"
PHONE, TEL = "(448) 238-2396", "+14482382396"
EMAIL = "contact@madlymadeleine.com"   # listed on their own Facebook About page
STREET, CITY, ZIP = "3906 US-98 #2", "Santa Rosa Beach", "32459"
LAT, LNG = 30.3748913, -86.242683
FB = "https://www.facebook.com/profile.php?id=61593156342905"
IG = "https://www.instagram.com/madly.madeleine/"
GMAPS = "https://www.google.com/maps/place/Madly+Madeleine/@30.3748913,-86.242683,17z"
OG_IMAGE = ORIGIN + BASE + "assets/photos/madeleine-flavors.jpg"

e = lambda s: html.escape(s, quote=True)
u = lambda p="": BASE + p
PH = lambda t: f'<span class="ph">[{e(t)}]</span>'     # visible placeholder marker

# Owner-facing "[Draft preview ...]" notes: tell the owner exactly what we need from them (Brandon's rule, 2026-10-06).
# Set DRAFT_NOTES = False at launch, then grep the output for "Draft preview" until none are left (also the form note,
# the placeholder review cards and every PH() placeholder).
DRAFT_NOTES = True
DN = lambda t: f'<p class="note draft-note">[Draft preview &mdash; {e(t)}]</p>' if DRAFT_NOTES else ""

NAV = [("Menu", "menu/"), ("Our Story", "our-story/"), ("News", "news/"), ("Visit", "visit/")]
written = []


def ld(blocks):
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>" for b in blocks)


def biz_ld():
    return {
        "@context": "https://schema.org", "@type": ["CafeOrCoffeeShop", "Bakery"], "@id": ORIGIN + u("#business"),
        "name": NAME, "url": ORIGIN + u(""), "telephone": "+1-448-238-2396", "email": EMAIL, "image": OG_IMAGE,
        "description": "French café and pâtisserie in Santa Rosa Beach, Florida: coffee, tea, cold drinks and French madeleines.",
        "servesCuisine": "French",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressRegion": "FL", "postalCode": ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "sameAs": [FB, IG],
    }


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u(p)} for i, (n, p) in enumerate(trail)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def head(title, desc, path, blocks):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f6e3e5">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{ORIGIN}{u(path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('assets/photos/logo.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Montserrat:wght@400;500;600&family=Pinyon+Script&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/site.css')}">
{ld(blocks)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = "".join(f'<a href="{u(p)}"{" class=on" if active == p else ""}>{e(n)}</a>' for n, p in NAV)
    m = f'<a href="{u()}">Home</a>' + "".join(f'<a href="{u(p)}">{e(n)}</a>' for n, p in NAV)
    return f"""<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{u()}" aria-label="{e(NAME)} home">
      <img src="{u('assets/photos/logo.png')}" alt="Madly Madeleine logo: a hand-drawn madeleine on pink stripes" width="48" height="48">
      <span class="brand-name"><i>Madly</i> MADELEINE<small>The French touch</small></span>
    </a>
    <nav class="main" aria-label="Main">{links}</nav>
    <div class="top-cta">
      <a class="btn btn-ghost" href="tel:{TEL}" aria-label="Call {PHONE}"><span>{PHONE}</span></a>
      <a class="btn btn-primary" href="{u('visit/')}">Visit us</a>
      <button class="menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile">{m}</nav>
<main id="main">
"""


def footer():
    ln = "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in NAV)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <h4>Madly Madeleine</h4>
      <p>Your little slice of France by the beach.</p>
      <p>{e(STREET)}<br>{CITY}, FL {ZIP}<br><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><h4>Explore</h4><ul><li><a href="{u()}">Home</a></li>{ln}</ul></div>
    <div><h4>Follow along</h4><ul><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li><li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{GMAPS}" target="_blank" rel="noopener">Google Maps</a></li></ul></div>
  </div>
  <div class="wrap foot-base">&copy; Madly Madeleine &middot; {e(STREET)}, {CITY}, FL {ZIP}</div>
</footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons">
    <span class="ghost-chevron down"><span></span><span></span></span>
    <span class="ghost-chevron up"><span></span><span></span></span>
  </div>
  <p>tektonbybigie.com/madly-madeleine/draft &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def crumbs_html(trail):
    parts = [f"<b>{e(n)}</b>" if i == len(trail) - 1 else f'<a href="{u(p)}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<p class="crumbs">' + "<span>/</span>".join(parts) + "</p>"


def page_hero(trail, h1, lede, kicker=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return f"""<section class="page-hero"><div class="wrap">
  {crumbs_html(trail)}{k}
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></section>
"""


def photo(name, alt, cls="", caption="", ext="jpg"):
    cap = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
    return f'<figure class="photo {cls}"><img src="{u("assets/photos/" + name + "." + ext)}" alt="{e(alt)}" loading="lazy">{cap}</figure>'


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div>"


def carousel():
    cards = [
        ("Your first review goes here", "Google review"), ("Reviews from real guests appear here", "Facebook review"),
        ("A line from a happy customer", "Google review"), ("Another guest, another madeleine moment", "Google review"),
        ("Showcase the best ones here", "Facebook review"),
    ]
    items = "".join(f"""<div class="cf-item"><div class="cf-card ph-card">
          <div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="ph-quote">&ldquo;{e(t)}&rdquo;</p>
          <p class="ph-who">{PH("reviewer name")}</p>
          <div class="src"><i></i> {e(s)} &middot; placeholder</div></div></div>""" for t, s in cards)
    return f"""<div class="cf-wrap">
        <div class="cf-stage" id="cf" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Customer reviews">{items}</div>
        <button class="cf-arrow cf-prev" id="cfPrev" aria-label="Previous review"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="cf-arrow cf-next" id="cfNext" aria-label="Next review"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="cf-dots" id="cfDots" aria-label="Choose review"></div>
      <p class="cf-hint">[Draft preview &mdash; these five cards are placeholders. Real Google and Facebook reviews go here, shown exactly as written. You don&rsquo;t have any reviews yet, so ask a few happy customers to leave you a Google review and we&rsquo;ll add them.]</p>"""


def assemble(path, title, desc, active, body, blocks):
    return head(title, desc, path, blocks) + header(active) + body + footer()


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    written.append(path or "(home)")


def cta_band(h="Come say bonjour", t=f"{STREET}, {CITY}"):
    return f"""<section class="cta-band"><div class="wrap"><h2>{h}</h2><p>{e(t)} &middot; <a href="tel:{TEL}">{PHONE}</a></p>
  <div class="btns"><a class="btn btn-primary" href="{u('visit/')}">Hours &amp; directions</a><a class="btn btn-ghost" href="{u('menu/')}">See the menu</a></div></div></section>"""


# ================================================================== FAQ (their own words, from their posts)
FAQS = [
    ("What is a madeleine?", "A madeleine is a small French cake baked in its traditional shell-shaped mold. It is soft and buttery inside, lightly golden around the edges and recognized by the small hump that forms during baking."),
    ("Is a madeleine a cake or a cookie?", "It's a cake, not a cookie. A madeleine is a small French cake baked in a traditional shell-shaped mold."),
    ("Why the shell shape?", "The traditional mold gives each madeleine its signature shape and lightly golden edges."),
    ("What about the little hump?", "A well-baked madeleine rises in the center, creating its characteristic hump and soft interior."),
    ("How do you enjoy a madeleine?", "With coffee, with tea or as a special break during your day."),
]


# ================================================================== HOME
def home():
    desc = "A French café and pâtisserie on US-98 in Santa Rosa Beach, FL. Coffee, tea, cold drinks and French madeleines, piped by hand. Now open."
    body = f"""<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="kicker">Bonjour, Santa Rosa Beach!</p>
    <h1><span class="h1-kicker">French café &amp; pâtisserie in Santa Rosa Beach</span> <em>Your little slice of France by the beach.</em></h1>
    <p class="lede">Coffee, tea, cold drinks &amp; French madeleines. Every madeleine is piped by hand.</p>
    <div class="btns"><a class="btn btn-primary" href="{u('menu/')}">See the menu</a><a class="btn btn-ghost" href="{u('visit/')}">Find us on US-98</a></div>
    <ul class="badges"><li>Now open</li><li>Piped by hand</li><li>{e(STREET)}, {CITY}</li></ul>
  </div>
  <div class="hero-art">{photo('chocolate-box', 'Dark-chocolate-dipped madeleines in a mint-green Madly Madeleine box on a marble table', 'arch')}</div>
</div></section>

<section class="intro"><div class="wrap">
  <p class="eyebrow">What we&rsquo;re madly about</p>
  <h2 class="section-title">Madeleines, coffee &amp; <em>a moment to slow down.</em></h2>
  <div class="cards3">
    <a class="card" href="{u('menu/')}">{photo('madeleine-plate', 'A golden French madeleine with its ridged shell on a white scalloped plate')}<h3>French madeleines</h3><p>Small French cakes baked in the traditional shell-shaped mold. Discover today&rsquo;s flavors.</p><span class="more">See the menu &rarr;</span></a>
    <a class="card" href="{u('menu/')}">{photo('madeleine-and-coffee', 'A chocolate-glazed madeleine beside an espresso in a navy cup')}<h3>Coffee &amp; tea</h3><p>With coffee, with tea or as a special break during your day.</p><span class="more">See the menu &rarr;</span></a>
    <a class="card" href="{u('visit/')}">{photo('interior-espresso', 'Espresso and two madeleines on a marble table beside a banquette with pink pillows')}<h3>A little place to sit</h3><p>Houndstooth walls, marble tables and bistro chairs, right on US-98 in Santa Rosa Beach.</p><span class="more">Plan your visit &rarr;</span></a>
  </div>
  {DN("these photos come from your Facebook and Instagram. Send your original, full-size photos from your phone and we will swap in sharper ones, plus anything you want featured: the café, the display case, you and the team.")}
</div></section>

<section class="split"><div class="wrap split-grid">
  {photo('piping-by-hand', 'A gloved hand piping madeleine batter into a shell-shaped mold', 'round')}
  <div>
    <p class="eyebrow">One shell at a time</p>
    <h2 class="section-title">Every madeleine is <em>piped by hand.</em></h2>
    <p>Behind every little shell, there&rsquo;s a pair of hands. <a href="{u('our-story/')}">Arnaud</a> pipes each madeleine one at a time, the way it&rsquo;s done back home in France.</p>
    <p><a class="btn btn-ghost" href="{u('our-story/')}">Meet Arnaud</a></p>
  </div>
</div></section>

<section class="split alt"><div class="wrap split-grid rev">
  <div>
    <p class="eyebrow">New to madeleines?</p>
    <h2 class="section-title">It&rsquo;s a <em>cake,</em> not a cookie.</h2>
    <p>A madeleine is a small French cake baked in a traditional shell-shaped mold. The mold gives each one its signature shape and lightly golden edges, and a well-baked madeleine rises in the center, creating its characteristic hump and soft interior.</p>
    <p><a class="btn btn-ghost" href="{u('menu/#faq')}">More about madeleines</a></p>
  </div>
  {photo('madeleine-cut', 'A madeleine cut in half to show its soft golden interior', 'round')}
</div></section>

<section class="reviews"><div class="wrap">
  <p class="eyebrow">Straight from our guests</p>
  <h2 class="section-title">Kind <em>words.</em></h2>
  {carousel()}
</div></section>

<section class="visit-strip"><div class="wrap visit-grid">
  <div><h2 class="section-title">Visit <em>us.</em></h2>
    <ul class="info">
      <li><b>Where</b><a href="{GMAPS}" target="_blank" rel="noopener">{e(STREET)}<br>{CITY}, FL {ZIP}</a></li>
      <li><b>Call</b><a href="tel:{TEL}">{PHONE}</a></li>
      <li><b>Hours</b><span>Tue&ndash;Fri 10 AM&ndash;5 PM &middot; Sat 10 AM&ndash;4 PM &middot; Closed Sun &amp; Mon</span></li>
    </ul>
    <p><a class="btn btn-primary" href="{u('visit/')}">Hours &amp; directions</a></p></div>
  <div class="follow"><p class="eyebrow">Follow along</p><p>See what&rsquo;s fresh on <a href="{IG}" target="_blank" rel="noopener">Instagram</a> and <a href="{FB}" target="_blank" rel="noopener">Facebook</a>.</p></div>
</div></section>
"""
    write("", assemble("", "Madly Madeleine | French Café & Pâtisserie, Santa Rosa Beach", desc, None, body, [biz_ld()]))


# ================================================================== MENU
def menu():
    path = "menu/"; trail = [("Home", ""), ("Menu", path)]
    desc = "French madeleines, coffee, tea and cold drinks at Madly Madeleine in Santa Rosa Beach, FL. Learn what a madeleine is and how to enjoy one."
    body = page_hero(trail, "Madeleines, coffee &amp; tea", "Coffee, tea, cold drinks &amp; French madeleines. Discover today&rsquo;s flavors at Madly Madeleine in Santa Rosa Beach.", "Menu") + f"""
<section><div class="wrap">
  {DN("send us your flavor names and prices and we will list them here. Do you sell boxes, take pre-orders or do catering? Tell us what is real and we will add it, and only that.")}

  <h2 class="section-title">French <em>madeleines</em></h2>
  <p class="lede-dark">Small French cakes baked in a traditional shell-shaped mold, piped by hand. Today&rsquo;s flavors vary &mdash; discover them when you visit.</p>
  <div class="gallery">
    {photo('madeleine-flavors', 'An open white box of assorted madeleines in pink, green, dark chocolate and golden, with more on plates', '', 'An assortment of madeleines')}
    {photo('chocolate-box', 'Dark-chocolate-dipped madeleines in a mint-green Madly Madeleine box', '', 'Chocolate-dipped, boxed to go')}
    {photo('madeleine-hump', 'A classic golden madeleine showing its characteristic hump', '', 'The classic, with its signature hump')}
  </div>
  <ul class="menu-list ph-list">
    <li>{PH('flavor name')} <span>{PH('price')}</span></li><li>{PH('flavor name')} <span>{PH('price')}</span></li><li>{PH('box sizes & prices')}</li>
  </ul>

  <h2 class="section-title">Coffee &amp; <em>tea</em></h2>
  <div class="split-grid tight">
    {photo('madeleine-and-coffee', 'A chocolate-glazed madeleine on a plate beside an espresso in a navy cup', 'round')}
    <div><p class="lede-dark">A proper espresso, hot tea and a little place to slow down. Enjoy a madeleine with coffee, with tea or as a special break during your day.</p>
    <ul class="menu-list ph-list"><li>{PH('your espresso and coffee drinks go here. We saw a noisette on your Facebook: what else do you serve?')}</li><li>{PH('your teas go here')}</li></ul></div>
  </div>

  <h2 class="section-title">Cold <em>drinks</em></h2>
  <ul class="menu-list ph-list"><li>{PH('your cold drinks and iced coffee go here')}</li></ul>
</div></section>

<section class="alt" id="faq"><div class="wrap narrow">
  <p class="eyebrow">Madeleine questions</p>
  <h2 class="section-title">All about <em>madeleines</em></h2>
  {faq_html(FAQS)}
</div></section>
{cta_band("Your first madeleine is waiting")}"""
    write(path, assemble(path, "Menu: French Madeleines, Coffee & Tea | Madly Madeleine", desc, path, body, [crumbs_ld(trail), faq_ld(FAQS), biz_ld()]))


# ================================================================== OUR STORY
def story():
    path = "our-story/"; trail = [("Home", ""), ("Our Story", path)]
    desc = "Meet Arnaud, the chef behind every little shell at Madly Madeleine in Santa Rosa Beach. Every French madeleine is piped by hand."
    body = page_hero(trail, "Meet <em>Arnaud.</em>", "The chef behind every little shell.", "Our story") + f"""
<section><div class="wrap split-grid">
  {photo('arnaud', 'Arnaud, the chef at Madly Madeleine, in a black chef coat', 'round')}
  <div>
    <h2 class="section-title">One shell <em>at a time.</em></h2>
    <blockquote class="story-quote">&ldquo;We left France, lived five years in Quebec, and came here on vacation. The Gulf Coast stole our hearts, so we stayed.&rdquo;</blockquote>
    <p class="cite">&mdash; Madly Madeleine, in the opening-day reel on Instagram</p>
    <p>Behind every little shell, there&rsquo;s a pair of hands. Arnaud pipes each madeleine one at a time, the way it&rsquo;s done back home in France. Then we pour the coffee, set the table and wait for you.</p>
    {DN("add your full names and a line or two about who we are. Is Arnaud the owner? Is there anyone else to introduce? A photo of you together would go well here.")}
  </div>
</div></section>

<section class="split alt"><div class="wrap split-grid rev">
  <div>
    <p class="eyebrow">The café</p>
    <h2 class="section-title">A little slice of <em>France.</em></h2>
    <p>Houndstooth walls, marble tables, bistro chairs and pink pillows: a little place to slow down on US-98 in Santa Rosa Beach, with coffee, tea, cold drinks and French madeleines.</p>
    <p><a class="btn btn-ghost" href="{u('visit/')}">Plan your visit</a></p>
  </div>
  {photo('interior-espresso', 'Espresso and two madeleines on a marble table beside a banquette with pink pillows', 'round')}
</div></section>
{cta_band("Come meet the madeleines")}"""
    write(path, assemble(path, "Meet Arnaud, the Chef Behind Every Madeleine | Madly Madeleine", desc, path, body, [crumbs_ld(trail), biz_ld()]))


# ================================================================== NEWS
def news():
    path = "news/"; trail = [("Home", ""), ("News", path)]
    desc = "Madly Madeleine opened its doors in Santa Rosa Beach on US-98. Read the opening announcement and follow along for updates."
    body = page_hero(trail, "Now open in <em>Santa Rosa Beach.</em>", "Bonjour, Santa Rosa Beach! The doors are open.", "News") + f"""
<section><div class="wrap split-grid">
  {photo('news-opening-graphic', 'Madly Madeleine announcement: Then it is your turn to slow down. Opening Wednesday, Sept 30', 'round', 'Our opening announcement')}
  <div>
    <h2 class="section-title">Opening day: <em>Wednesday, Sept 30</em></h2>
    <p><strong>Doors open at 9 AM.</strong> &ldquo;A little corner of France opens on US 98: madeleines in every flavor, good coffee and time to slow down. Come say bonjour.&rdquo;</p>
    <p>Madly Madeleine opened its doors at {e(STREET)} in {CITY}: a French café and pâtisserie with coffee, tea, cold drinks and French madeleines.</p>
    <p>Follow along on <a href="{IG}" target="_blank" rel="noopener">Instagram</a> and <a href="{FB}" target="_blank" rel="noopener">Facebook</a> to see what&rsquo;s fresh.</p>
    {DN("this page is for your news: new flavors, seasonal specials, events. Tell us when you have something to share and we will add it.")}
  </div>
</div></section>
{cta_band("Your first madeleine is waiting")}"""
    write(path, assemble(path, "Now Open in Santa Rosa Beach | Madly Madeleine News", desc, path, body, [crumbs_ld(trail), biz_ld()]))


# ================================================================== VISIT & CONTACT
def visit():
    path = "visit/"; trail = [("Home", ""), ("Visit", path)]
    desc = f"Find Madly Madeleine at {STREET} in {CITY}, FL {ZIP}. Call {PHONE} for hours and directions."
    body = page_hero(trail, "Visit <em>Madly Madeleine</em>", f"{e(STREET)}, {CITY}, FL {ZIP}", "Hours, directions &amp; contact") + f"""
<section><div class="wrap visit-page">
  <div>
    <ul class="info big">
      <li><b>Address</b><a href="{GMAPS}" target="_blank" rel="noopener">{e(STREET)}<br>{CITY}, FL {ZIP}</a></li>
      <li><b>Call</b><a href="tel:{TEL}">{PHONE}</a></li>
      <li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><b>Hours</b><span>Tue&ndash;Fri 10 AM&ndash;5 PM &middot; Sat 10 AM&ndash;4 PM &middot; Closed Sun &amp; Mon</span></li>
      <li><b>Find us</b><span>On US Highway 98 in {CITY}, near La Canosa Blvd.</span></li>
      <li><b>Follow</b><span><a href="{IG}" target="_blank" rel="noopener">Instagram</a> &middot; <a href="{FB}" target="_blank" rel="noopener">Facebook</a></span></li>
    </ul>
    {DN("these are the hours on your Google listing. Are they right, including closed Sunday and Monday? Tell us any changes, like holidays or summer hours.")}
    <p><a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&destination={LAT},{LNG}" target="_blank" rel="noopener">Get directions</a></p>
  </div>
  <div class="mapbox"><iframe title="Map to Madly Madeleine" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={LAT},{LNG}&z=16&output=embed"></iframe></div>
</div></section>

<section class="alt"><div class="wrap narrow">
  <h2 class="section-title">Say <em>bonjour.</em></h2>
  <p class="lede-dark">Questions, orders or ideas? Send a note and we&rsquo;ll get back to you.</p>
  <div class="form-card">
    <div class="row"><div><label for="c-name">Your name</label><input id="c-name" type="text" placeholder="Jane Smith"></div>
    <div><label for="c-email">Email</label><input id="c-email" type="email" placeholder="jane@email.com"></div></div>
    <div><label for="c-msg">Message</label><textarea id="c-msg" rows="4" placeholder="How can we help?"></textarea></div>
    <button class="btn btn-primary" type="button">Send message</button>
    <p class="form-note">[Draft preview &mdash; the form gets wired to your email when the site goes live.]</p>
  </div>
</div></section>"""
    write(path, assemble(path, "Visit Madly Madeleine | 3906 US-98 #2, Santa Rosa Beach, FL", desc, path, body, [crumbs_ld(trail), biz_ld()]))


if __name__ == "__main__":
    home(); menu(); story(); news(); visit()
    print(f"built {len(written)} pages into {OUT}:"); [print("  /" + w) for w in written]
