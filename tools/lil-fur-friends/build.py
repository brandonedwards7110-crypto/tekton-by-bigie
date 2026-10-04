#!/usr/bin/env python3
"""Builds the Lil Fur Friends spec-draft site into public/lil-fur-friends/draft/.
Run from the repo root:  python3 tools/lil-fur-friends/build.py

FACT RULE: every claim comes from the owners' Facebook page (About panels, services bio, flyer copy),
their Google listing, or real customer reviews captured on 2026-10-03 (see the Drive PROJECT-SUMMARY.md).
Anything unconfirmed is a visible [bracketed placeholder]. NO street address anywhere (home-based
service-area business; Google currently shows it publicly, which the owners should look at).
"""
import os, json, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "lil-fur-friends", "draft")
BASE = "/lil-fur-friends/draft/"
ORIGIN = "https://tektonbybigie.com"

NAME = "Lil Fur Friends"
PHONE, TEL = "(309) 402-2974", "+13094022974"
EMAIL = "lilfurfriends2026@gmail.com"
FB = "https://www.facebook.com/profile.php?id=61588548386359"
GOOGLE_REVIEWS = "https://www.google.com/maps/search/Lil+Fur+Friends+Freeport+FL"
OG_IMAGE = ORIGIN + BASE + "assets/photos/robyn-ken-in-park.jpg"
AREAS = ["Freeport", "Santa Rosa Beach", "DeFuniak Springs"]

e = lambda s: html.escape(s, quote=True)
u = lambda p="": BASE + p
PH = lambda t: f'<span class="ph">[{e(t)}]</span>'
NAV = [("Services", "services/"), ("Areas", "areas/"), ("About", "about/"), ("Reviews", "reviews/"), ("Contact", "contact/")]
written = []

# ---------------------------------------------------------------- real reviews (verbatim as visible; "..." = text cut off by the platform)
REVIEWS = [
    dict(who="Reese Jordan", src="Facebook", when="Sept 15", text="We are so happy we found Lil Fur Friends! Robyn and Ken were responsive, welcoming, and a pleasure to meet. This was our first time leaving our dogs away from home, and they made sure they were well cared for and loved on. We’re so thankful they were available in a pinch and would definitely recommend them!"),
    dict(who="Rafael Martinez", src="Google", when="3 months ago", text="We are so thankful for Lil Fur Friends. This is the village you want to leave your fur babies with. Not only do they treat your baby as their own but their own fur babies loved on my baby. The multitude of texts and photos are so …"),
    dict(who="Mary Kay Williams", src="Google", when="3 months ago", text="Trust me when we say Ken and Robyn are the absolute BEST dog sitters in the whole Florida Panhandle!!! We moved here 5 years ago and have been hesitant to hire anyone for our 3 “four legged children”. We set up an in home interview, and …"),
    dict(who="Jenni Smith", src="Google", when="3 months ago", text="Robin and Ken are truly the kindest people you could ever trust with your fur babies. From the beginning, they were so flexible, patient, and caring. They took the time to really get to know our babies, their personalities, and what made …"),
]
HIGHLIGHTS = ["Peace of mind to know your dogs are cared for like family while away.", "We couldn’t be happier with the care our pets received!", "We set up an in home interview, and fell in love with them!"]


def ld(blocks):
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>" for b in blocks)


def biz_ld():
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": ORIGIN + u("#business"), "name": NAME, "url": ORIGIN + u(""),
            "telephone": "+1-309-402-2974", "email": EMAIL, "image": OG_IMAGE,
            "description": "Professional pet sitting in Freeport, Santa Rosa Beach and DeFuniak Springs, Florida: in-home pet sitting, boarding and drop-in visits.",
            "address": {"@type": "PostalAddress", "addressLocality": "Freeport", "addressRegion": "FL", "postalCode": "32439", "addressCountry": "US"},
            "areaServed": [{"@type": "City", "name": a + ", FL"} for a in AREAS], "sameAs": [FB],
            "founder": [{"@type": "Person", "name": "Robyn Aites"}, {"@type": "Person", "name": "Ken Aites"}]}


def service_ld(name, desc, path):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": name, "description": desc, "url": ORIGIN + u(path),
            "provider": {"@type": "LocalBusiness", "@id": ORIGIN + u("#business"), "name": NAME}, "areaServed": [{"@type": "City", "name": a + ", FL"} for a in AREAS]}


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u(p)} for i, (n, p) in enumerate(trail)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def head(title, desc, path, blocks):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#e6f3f5">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{ORIGIN}{u(path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('assets/photos/paw-logo.png')}" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/site.css')}">
{ld(blocks)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = "".join(f'<a href="{u(p)}"{" class=on" if active == p else ""}>{e(n)}</a>' for n, p in NAV)
    m = f'<a href="{u()}">Home</a>' + "".join(f'<a href="{u(p)}">{e(n)}</a>' for n, p in NAV) + f'<a href="{u("services/in-home-pet-sitting/")}">&nbsp;&nbsp;In-home pet sitting</a><a href="{u("services/pet-boarding/")}">&nbsp;&nbsp;Pet boarding</a><a href="{u("services/drop-in-visits/")}">&nbsp;&nbsp;Drop-in visits</a>'
    return f"""<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{u()}" aria-label="{e(NAME)} home">
      <img src="{u('assets/photos/paw-logo.png')}" alt="Lil Fur Friends paw print logo" height="46">
      <span class="brand-name">Lil <b>Fur</b> Friends<small>Pet sitting &amp; walking</small></span>
    </a>
    <nav class="main" aria-label="Main">{links}</nav>
    <div class="top-cta">
      <a class="btn btn-ghost" href="tel:{TEL}" aria-label="Call {PHONE}"><span>{PHONE}</span></a>
      <a class="btn btn-primary" href="{u('contact/')}">Book a sitter</a>
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
    <div><h4>Lil Fur Friends</h4><p>Professional pet sitting services. Loving your fur babies like they&rsquo;re one of our own.</p>
      <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>Serving {e(', '.join(AREAS[:-1]))} &amp; {AREAS[-1]}, FL</p></div>
    <div><h4>Explore</h4><ul><li><a href="{u()}">Home</a></li>{ln}</ul></div>
    <div><h4>Services</h4><ul><li><a href="{u('services/in-home-pet-sitting/')}">In-home pet sitting</a></li><li><a href="{u('services/pet-boarding/')}">Pet boarding</a></li><li><a href="{u('services/drop-in-visits/')}">Drop-in visits</a></li></ul>
      <h4 style="margin-top:16px">Follow</h4><ul><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
  </div>
  <div class="wrap foot-base">&copy; Lil Fur Friends &middot; Member of NAPPS &middot; Bonded &amp; insured by Pet Sitters Associates</div>
</footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons">
    <span class="ghost-chevron down"><span></span><span></span></span>
    <span class="ghost-chevron up"><span></span><span></span></span>
  </div>
  <p>tektonbybigie.com/lil-fur-friends/draft &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def crumbs_html(trail):
    return '<p class="crumbs">' + "<span>/</span>".join(f"<b>{e(n)}</b>" if i == len(trail) - 1 else f'<a href="{u(p)}">{e(n)}</a>' for i, (n, p) in enumerate(trail)) + "</p>"


def page_hero(trail, h1, lede, kicker=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return f'<section class="page-hero"><div class="wrap">{crumbs_html(trail)}{k}<h1>{h1}</h1><p class="lede">{lede}</p></div></section>\n'


def photo(name, alt, cls="", caption=""):
    cap = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
    return f'<figure class="photo {cls}"><img src="{u("assets/photos/" + name + ".jpg")}" alt="{e(alt)}" loading="lazy">{cap}</figure>'


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div>"


def quote_card(r):
    return f'<div class="quote-card"><div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div><blockquote>&ldquo;{e(r["text"])}&rdquo;</blockquote><cite>&mdash; {e(r["who"])}, {e(r["src"])} review &middot; {e(r["when"])}</cite></div>'


def carousel():
    items = "".join(f"""<div class="cf-item"><div class="cf-card"><div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <p class="ph-quote">&ldquo;{e(r['text'][:230] + ('…' if len(r['text']) > 230 and not r['text'].endswith('…') else ''))}&rdquo;</p>
          <p class="ph-who">&mdash; {e(r['who'])}</p><div class="src"><i></i> {e(r['src'])} review &middot; {e(r['when'])}</div></div></div>""" for r in REVIEWS)
    return f"""<div class="cf-wrap"><div class="cf-stage" id="cf" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Customer reviews">{items}</div>
        <button class="cf-arrow cf-prev" id="cfPrev" aria-label="Previous review"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="cf-arrow cf-next" id="cfNext" aria-label="Next review"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button></div>
      <div class="cf-dots" id="cfDots" aria-label="Choose review"></div>
      <p class="cf-hint">Real reviews from Facebook and Google, word for word. Swipe or tap the arrows to browse.</p>"""


def assemble(path, title, desc, active, body, blocks):
    return head(title, desc, path, blocks) + header(active) + body + footer()


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    written.append(path or "(home)")


def cta_band(h="Heading out of town?", t="Tell us about your pet and when you&rsquo;ll be away."):
    return f"""<section class="cta-band"><div class="wrap"><h2>{h}</h2><p>{t} &middot; <a href="tel:{TEL}">{PHONE}</a></p>
  <div class="btns"><a class="btn btn-primary" href="{u('contact/')}">Book a sitter</a><a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></div></div></section>"""


INSURED = ("Are you insured?", "Lil Fur Friends is a member of NAPPS and is bonded and insured by Pet Sitters Associates.")
BOOK = ("How do I book?", f"Call or text {PHONE}, email {EMAIL}, or send a message on Facebook. Tell us about your pet and the dates you need care.")
WHERE = ("Where do you work?", "We serve Freeport, Santa Rosa Beach and DeFuniak Springs, FL.")


# ================================================================== HOME
def home():
    desc = "Professional pet sitting in Freeport, Santa Rosa Beach and DeFuniak Springs, FL. In-home pet sitting, boarding and drop-in visits. Bonded and insured."
    body = f"""<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="kicker">Pet sitting &amp; walking &middot; Freeport, Santa Rosa Beach &amp; DeFuniak Springs</p>
    <h1><span class="h1-kicker">Professional pet sitting in Freeport, FL</span> <em>Loving your fur babies like they&rsquo;re one of our own.</em></h1>
    <p class="lede">Putting your mind at ease while you&rsquo;re away.</p>
    <div class="btns"><a class="btn btn-primary" href="{u('contact/')}">Book a sitter</a><a class="btn btn-ghost" href="{u('services/')}">See our services</a></div>
    <ul class="badges"><li>Member of NAPPS</li><li>Bonded &amp; insured by Pet Sitters Associates</li><li>100% recommend on Facebook</li><li>5.0 on Google</li></ul>
  </div>
  <div class="hero-art">{photo('robyn-ken-in-park', 'Robyn and Ken smiling together in a park with three schnauzers on the grass in front of them', 'round', 'Robyn and Ken with three of their furry friends')}</div>
</div></section>

<section class="intro"><div class="wrap">
  <p class="eyebrow">How we care for your pet</p>
  <h2 class="section-title">Care that fits <em>your pet &amp; your trip.</em></h2>
  <div class="cards3">
    <a class="card" href="{u('services/in-home-pet-sitting/')}">{photo('three-dogs-with-bows', 'Three small dogs wearing hair bows sitting on a quilted bed')}<h3>In-home pet sitting</h3><p>Your pet stays comfortable in their own home while you&rsquo;re away.</p><span class="more">Learn more &rarr;</span></a>
    <a class="card" href="{u('services/pet-boarding/')}">{photo('dogs-on-kitchen-mats', 'Six dogs looking up from teal mats on a kitchen floor')}<h3>Pet boarding</h3><p>Your dog stays at Robyn and Ken&rsquo;s home with their own fur babies.</p><span class="more">Learn more &rarr;</span></a>
    <a class="card" href="{u('services/drop-in-visits/')}">{photo('sleeping-dog', 'A fluffy white and tan dog asleep on a paw-print blanket')}<h3>Drop-in visits</h3><p>Check-ins while you&rsquo;re at work or away for the day.</p><span class="more">Learn more &rarr;</span></a>
  </div>
  <p class="note" style="margin-top:22px">Also on the list: dog walks, cats too, and medication if needed. {PH('confirm details, rates and what each visit includes')}</p>
</div></section>

<section class="alt"><div class="wrap">
  <p class="eyebrow">What customers say</p>
  <h2 class="section-title">Why families <em>choose us.</em></h2>
  <div class="why">
    <div><h3>Responsive &amp; welcoming</h3><p>&ldquo;Robyn and Ken were responsive, welcoming, and a pleasure to meet.&rdquo;</p><small>Reese Jordan &middot; Facebook</small></div>
    <div><h3>Flexible, patient &amp; caring</h3><p>&ldquo;From the beginning, they were so flexible, patient, and caring.&rdquo;</p><small>Jenni Smith &middot; Google</small></div>
    <div><h3>Treated like family</h3><p>&ldquo;Not only do they treat your baby as their own but their own fur babies loved on my baby.&rdquo;</p><small>Rafael Martinez &middot; Google</small></div>
  </div>
</div></section>

<section class="split"><div class="wrap split-grid">
  {photo('robyn-bathing-cavalier', 'Robyn giving a wet Cavalier King Charles spaniel a bath in a tub', 'round')}
  <div>
    <p class="eyebrow">Meet your sitters</p>
    <h2 class="section-title">Robyn &amp; Ken <em>Aites</em></h2>
    <p>Letting your fur babies feel like they&rsquo;re on vacation while you are on vacation. Lil Fur Friends is a member of NAPPS and is bonded and insured by Pet Sitters Associates.</p>
    <p><a class="btn btn-ghost" href="{u('about/')}">More about us</a></p>
  </div>
</div></section>

<section class="reviews"><div class="wrap">
  <p class="eyebrow">Straight from our customers</p>
  <h2 class="section-title">Kind <em>words.</em></h2>
  {carousel()}
  <p class="reviews-link" style="text-align:center;margin-top:18px"><a class="btn btn-ghost" href="{u('reviews/')}">Read more reviews</a></p>
</div></section>

<section><div class="wrap"><div class="offer">
  <h2>20% off your first booking</h2>
  <p>{PH('confirm this offer is still running and its dates before publishing')}</p>
  <div class="btns" style="justify-content:center"><a class="btn btn-primary" href="{u('contact/')}">Book a sitter</a></div>
</div></div></section>
{cta_band()}"""
    write("", assemble("", "Lil Fur Friends | Pet Sitting in Freeport, FL", desc, None, body, [biz_ld()]))


# ================================================================== SERVICES
SERVICES = [
    dict(slug="in-home-pet-sitting", name="In-Home Pet Sitting", h1="In-home pet sitting in Freeport, FL",
         title="In-Home Pet Sitting in Freeport, FL | Lil Fur Friends",
         desc="In-home pet sitting in Freeport, Santa Rosa Beach and DeFuniak Springs, FL from Robyn and Ken. Member of NAPPS, bonded and insured.",
         card="Your pet stays comfortable in their own home while you&rsquo;re away.",
         lede="Your pet stays in their own home, on their own routine, while you&rsquo;re away. Robyn and Ken look after them like they&rsquo;re one of their own.",
         img=("three-dogs-with-bows", "Three small dogs wearing hair bows sitting on a quilted bed"),
         quotes=[0, 2],
         body=[("What in-home pet sitting means", f"<p>Instead of moving your pet to a kennel, a sitter cares for them at home, where their bed, toys and routine are. That&rsquo;s the service Lil Fur Friends is known for. {PH('what each visit or stay includes: feeding, walks, play, updates, hours')}</p>"),
               ("Getting started", "<p>Customers mention setting up an in-home interview before booking, and getting plenty of texts and photos while they&rsquo;re away. " + PH("confirm: meet-and-greet process and how updates are sent") + "</p>")],
         faqs=[("What is in-home pet sitting?", "A sitter cares for your pet in your own home while you are away, so your pet keeps their usual surroundings and routine."), WHERE, INSURED, BOOK,
               ("Can you care for more than one pet?", "Customers have trusted Lil Fur Friends with multiple pets, including a family with three “four legged children.”")],
         related=["pet-boarding", "drop-in-visits"]),
    dict(slug="pet-boarding", name="Pet Boarding", h1="Dog boarding in Freeport, FL",
         title="Dog Boarding in Freeport, FL | Lil Fur Friends",
         desc="Dog boarding at Robyn and Ken's home in Freeport, FL, with their own fur babies. Serving Santa Rosa Beach and DeFuniak Springs. Bonded and insured.",
         card="Your dog stays at Robyn and Ken&rsquo;s home with their own fur babies.",
         lede="Your dog stays at Robyn and Ken&rsquo;s home, with plenty of company and attention. A customer said it best: &ldquo;This is the village you want to leave your fur babies with.&rdquo;",
         img=("dogs-on-kitchen-mats", "Six dogs looking up from teal mats on a kitchen floor"),
         quotes=[1, 0],
         body=[("Boarding in a real home", "<p>Boarding with Lil Fur Friends happens at Robyn and Ken&rsquo;s own home. One customer wrote that Lil Fur Friends&rsquo; own fur babies loved on their dog and that the &ldquo;multitude of texts and photos&rdquo; kept them in the loop. " + PH("rates, sizes and breeds accepted, vaccination requirements, drop-off and pick-up times") + "</p>"),
               ("First time away from home?", "<p>One customer wrote that it was their first time leaving their dogs away from home, and that Robyn and Ken &ldquo;made sure they were well cared for and loved on.&rdquo;</p>")],
         faqs=[("Where do the dogs stay?", "Boarding is at Robyn and Ken&rsquo;s home, alongside their own fur babies.".replace("&rsquo;", "’")), WHERE, INSURED, BOOK,
               ("Will I get updates while I'm away?", "Customers mention receiving lots of texts and photos while their pets are boarding.")],
         related=["in-home-pet-sitting", "drop-in-visits"]),
    dict(slug="drop-in-visits", name="Drop-In Visits", h1="Pet drop-in visits in Freeport, FL",
         title="Pet Drop-In Visits in Freeport, FL | Lil Fur Friends",
         desc="Pet drop-in visits in Freeport, Santa Rosa Beach and DeFuniak Springs, FL. Dogs and cats, medication if needed. Bonded and insured pet sitters.",
         card="Check-ins while you&rsquo;re at work or away for the day.",
         lede="A visit from a sitter who knows your pet, when you can&rsquo;t be home. Cats too, and medication if needed.",
         img=("sleeping-dog", "A fluffy white and tan dog asleep on a paw-print blanket"),
         quotes=[3, 0],
         body=[("Quick visits, full attention", "<p>Drop-in visits are one of the services Lil Fur Friends lists, along with dog walks, overnight stays, cats, and medication if needed. " + PH("visit lengths, what's included, rates, and how to schedule recurring visits") + "</p>")],
         faqs=[("What is a drop-in visit?", "A sitter stops by your home for a visit while you are away or at work to care for your pet."), ("Do you care for cats?", "Yes. Cats are on the Lil Fur Friends service list."), ("Can you give medication?", "Medication is on the Lil Fur Friends service list (“medication if needed”)."), WHERE, INSURED, BOOK],
         related=["in-home-pet-sitting", "pet-boarding"]),
]
SVC = {s["slug"]: s for s in SERVICES}


def service_page(s):
    path = f"services/{s['slug']}/"; trail = [("Home", ""), ("Services", "services/"), (s["name"], path)]
    sec = "".join(f"<h2>{e(h)}</h2>{b}" for h, b in s["body"])
    rel = "".join(f'<li><a href="{u("services/" + r + "/")}">{e(SVC[r]["name"])}</a></li>' for r in s["related"])
    areas = "".join(f'<a class="chip" href="{u("areas/")}">{e(a)}</a>' for a in AREAS)
    body = page_hero(trail, e(s["h1"]), s["lede"], "Lil Fur Friends") + f"""<section><div class="wrap narrow prose">
  <figure class="photo round" style="max-width:520px;margin:0 0 26px"><img src="{u('assets/photos/' + s['img'][0] + '.jpg')}" alt="{e(s['img'][1])}" loading="lazy"></figure>
  {sec}
  <h2>What customers say</h2>{''.join(quote_card(REVIEWS[i]) for i in s['quotes'])}
  <h2>Common questions</h2>{faq_html(s['faqs'])}
  <h2>Where we work</h2><p>We serve {e(', '.join(AREAS[:-1]))} and {AREAS[-1]}, FL. <a href="{u('areas/')}">See the areas we serve</a>.</p>
  <h2>Other services</h2><ul class="rel">{rel}</ul>
</div></section>
{cta_band()}"""
    write(path, assemble(path, s["title"], s["desc"], "services/", body, [service_ld(s["name"], s["desc"], path), crumbs_ld(trail), faq_ld(s["faqs"]), biz_ld()]))


def services_hub():
    path = "services/"; trail = [("Home", ""), ("Services", path)]
    desc = "In-home pet sitting, boarding, drop-in visits, dog walks and more from Lil Fur Friends in Freeport, FL. Cats too. Bonded and insured."
    cards = "".join(f'<a class="card" href="{u("services/" + s["slug"] + "/")}">{photo(s["img"][0], s["img"][1])}<h3>{e(s["name"])}</h3><p>{s["card"]}</p><span class="more">Learn more &rarr;</span></a>' for s in SERVICES)
    body = page_hero(trail, "Pet sitting services in Freeport, FL", "In-home pet sitting, dog walks, overnight stays, drop-in visits, cats too, and medication if needed. Bonded and insured.", "Services") + f"""
<section><div class="wrap"><div class="cards3">{cards}</div>
  <p class="note" style="margin-top:24px">Also on the list: <b>dog walks</b>, <b>overnight stays</b>, <b>cats too</b> and <b>medication if needed</b>. {PH('confirm details and rates for each; add pages if they want them')}</p>
</div></section>
{cta_band()}"""
    write(path, assemble(path, "Pet Sitting Services in Freeport, FL | Lil Fur Friends", desc, path, body, [crumbs_ld(trail), biz_ld()]))


# ================================================================== AREAS / ABOUT / REVIEWS / CONTACT
def areas():
    path = "areas/"; trail = [("Home", ""), ("Areas", path)]
    desc = "Lil Fur Friends serves Freeport, Santa Rosa Beach and DeFuniak Springs, FL with pet sitting, boarding and drop-in visits."
    body = page_hero(trail, "Areas we serve", "Pet sitting for Freeport, Santa Rosa Beach and DeFuniak Springs, Florida.", "Service area") + f"""
<section><div class="wrap">
  <div class="areas3">
    <div><h3>Freeport</h3><p>Home base for Lil Fur Friends. In-home sitting, boarding and drop-in visits.</p></div>
    <div><h3>Santa Rosa Beach</h3><p>In-home pet sitting and drop-in visits for Santa Rosa Beach families.</p></div>
    <div><h3>DeFuniak Springs</h3><p>In-home pet sitting and drop-in visits in DeFuniak Springs.</p></div>
  </div>
  <p class="note">{PH('confirm which services are offered in which town. Real local content (jobs, photos, reviews that name the town) goes here as it comes in')}</p>
  <h2 class="section-title" style="margin-top:34px">Not sure we cover you?</h2>
  <p class="lede-dark">Call or text <a href="tel:{TEL}">{PHONE}</a> and tell us where you live.</p>
</div></section>
{cta_band()}"""
    write(path, assemble(path, "Areas We Serve: Freeport, Santa Rosa Beach, DeFuniak Springs", desc, path, body, [crumbs_ld(trail), biz_ld()]))


def about():
    path = "about/"; trail = [("Home", ""), ("About", path)]
    desc = "Meet Robyn and Ken Aites of Lil Fur Friends in Freeport, FL: professional pet sitters, NAPPS members, bonded and insured by Pet Sitters Associates."
    body = page_hero(trail, "Meet Robyn &amp; Ken <em>Aites</em>", "Loving your fur babies like they&rsquo;re one of our own, putting your mind at ease while you&rsquo;re away.", "About") + f"""
<section><div class="wrap split-grid">
  {photo('robyn-ken-with-nine-dogs', 'Robyn and Ken sitting on a couch surrounded by nine small dogs', 'round', 'Robyn and Ken with a houseful of furry friends')}
  <div>
    <h2 class="section-title">Pet sitting, <em>done like family.</em></h2>
    <p>Lil Fur Friends is a professional pet sitting service run by Robyn and Ken Aites in Freeport, Florida. Their goal: &ldquo;Letting your fur babies feel like they&rsquo;re on vacation while you are on vacation.&rdquo;</p>
    <ul class="info"><li><b>Member of</b><span>NAPPS</span></li><li><b>Bonded &amp; insured</b><span>by Pet Sitters Associates</span></li><li><b>Serving</b><span>{e(', '.join(AREAS[:-1]))} &amp; {AREAS[-1]}, FL</span></li></ul>
    <p class="note">{PH("Robyn & Ken's story, in their own words: how they started, their own pets, why pet sitting")}</p>
  </div>
</div></section>
<section class="split alt"><div class="wrap split-grid rev">
  <div><p class="eyebrow">What customers notice</p><h2 class="section-title">Kind, flexible &amp; <em>patient.</em></h2>
    <p>&ldquo;Robin and Ken are truly the kindest people you could ever trust with your fur babies. From the beginning, they were so flexible, patient, and caring.&rdquo; &mdash; Jenni Smith, Google review</p>
    <p><a class="btn btn-ghost" href="{u('reviews/')}">Read the reviews</a></p></div>
  {photo('robyn-bathing-cavalier', 'Robyn giving a wet Cavalier King Charles spaniel a bath in a tub', 'round')}
</div></section>
{cta_band("Meet your sitters")}"""
    write(path, assemble(path, "Meet Robyn & Ken | Lil Fur Friends Pet Sitters, Freeport FL", desc, path, body, [crumbs_ld(trail), biz_ld()]))


def reviews():
    path = "reviews/"; trail = [("Home", ""), ("Reviews", path)]
    desc = "Real reviews of Lil Fur Friends pet sitting in Freeport, FL: 100% recommend on Facebook and 5.0 stars on Google."
    hl = "".join(f"<li>&ldquo;{e(h)}&rdquo;</li>" for h in HIGHLIGHTS)
    body = page_hero(trail, "What customers say", "Real reviews from Facebook and Google, word for word.", "Reviews") + f"""
<section><div class="wrap narrow">
  <div class="stat-row"><div class="stat"><span>Facebook</span>100% recommend (13)</div><div class="stat"><span>Google</span>5.0 stars (8 reviews)</div></div>
  {''.join(quote_card(r) for r in REVIEWS)}
  <h2 class="section-title">More from Google reviews</h2><ul class="tick-list">{hl}</ul>
  <div class="btns"><a class="btn btn-primary" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">Read &amp; write Google reviews</a><a class="btn btn-ghost" href="{FB}" target="_blank" rel="noopener">See us on Facebook</a></div>
  <p class="note" style="margin-top:22px">Written reviews shown are the ones readable on each platform on the day they were collected; text is shortened (&hellip;) where the platform cut it off. {PH('swap in screenshots and add new reviews as they arrive')}</p>
</div></section>
{cta_band("Join our happy customers")}"""
    write(path, assemble(path, "Reviews | Lil Fur Friends Pet Sitting, Freeport FL", desc, path, body, [crumbs_ld(trail), biz_ld()]))


def contact():
    path = "contact/"; trail = [("Home", ""), ("Contact", path)]
    desc = f"Contact Lil Fur Friends for pet sitting in Freeport, Santa Rosa Beach and DeFuniak Springs, FL. Call or text {PHONE}."
    body = page_hero(trail, "Book a sitter", "Tell us about your pet and the dates you&rsquo;ll be away. We&rsquo;ll get back to you.", "Contact") + f"""
<section><div class="wrap visit-page">
  <div><ul class="info big">
    <li><b>Call or text</b><a href="tel:{TEL}">{PHONE}</a></li>
    <li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><b>Facebook</b><a href="{FB}" target="_blank" rel="noopener">Send us a message</a></li>
    <li><b>Serving</b><span>{e(', '.join(AREAS[:-1]))} &amp; {AREAS[-1]}, FL</span></li>
    <li><b>Hours</b><span>{PH('confirm: Facebook currently says &ldquo;Always open&rdquo;')}</span></li>
  </ul></div>
  <div class="form-card"><h3>Request a sitter</h3>
    <div class="row"><div><label for="c-name">Your name</label><input id="c-name" type="text" placeholder="Jane Smith"></div><div><label for="c-phone">Phone</label><input id="c-phone" type="tel" placeholder="(850) 555-0100"></div></div>
    <div class="row"><div><label for="c-email">Email</label><input id="c-email" type="email" placeholder="jane@email.com"></div><div><label for="c-town">Town</label><input id="c-town" type="text" placeholder="Freeport, Santa Rosa Beach, DeFuniak Springs"></div></div>
    <div><label for="c-pets">Your pet(s) and the dates you need care</label><textarea id="c-pets" rows="4" placeholder="Two dogs, Dec 20&ndash;27..."></textarea></div>
    <button class="btn btn-primary" type="button">Send request</button>
    <p class="form-note">[Draft preview &mdash; the form gets wired to the owners&rsquo; email when the site goes live.]</p></div>
</div></section>"""
    write(path, assemble(path, "Contact Lil Fur Friends | (309) 402-2974 | Freeport, FL", desc, path, body, [crumbs_ld(trail), biz_ld()]))


if __name__ == "__main__":
    home(); services_hub(); [service_page(s) for s in SERVICES]; areas(); about(); reviews(); contact()
    print(f"built {len(written)} pages into {OUT}:"); [print("  /" + w) for w in written]
