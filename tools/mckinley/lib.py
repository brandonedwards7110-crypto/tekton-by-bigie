"""Shared templates for the McKinley Co multi-page site (static HTML generator)."""
import html, json

BASE = "/mckinley-co-heating-cooling/draft/"          # change to "/" when the site gets its own domain
ORIGIN = "https://tektonbybigie.com"                   # change at launch
NAME = "McKinley Co. Heating & Cooling"
PHONE = "(334) 782-0347"
TEL = "+13347820347"
EMAIL = "mckinleyco23@gmail.com"
STREET = "1102 Coosa River Pkwy"
LICENSE = "2025301"
FB = "https://www.facebook.com/profile.php?id=61585419263815"
IG = "https://www.instagram.com/mckinleyco.hvac/"
TT = "https://www.tiktok.com/@mckinleyco.hvac"
GMAPS = "https://www.google.com/maps/search/McKinley+Co+Heating+%26+Cooling+Wetumpka+AL"
OG_IMAGE = ORIGIN + BASE + "assets/trucks-hero-clean.png"


# Draft-only notes for the owner ("[Draft preview ...]"). Set DRAFT_NOTES = False when the site goes live, and also remove the
# two form-note lines (contact + careers) -- grep the output for "Draft preview" to be sure none are left.
DRAFT_NOTES = True


def photo_slot(text):
    """A dashed 'photo goes here' box that tells the owner exactly what to send. Shown only while DRAFT_NOTES is on."""
    if not DRAFT_NOTES:
        return ""
    return f'<div class="photo-slot">[Draft preview &mdash; {text}]</div>'


def e(s):
    return html.escape(s, quote=True)


def u(path=""):
    return BASE + path


PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'

NAV = [
    ("Services", "services/"),
    ("Comfort Club", "comfort-club/"),
    ("Reviews", "reviews/"),
    ("Service Area", "areas/"),
    ("About", "about/"),
    ("Careers", "careers/"),
    ("Contact", "contact/"),
]

# icon paths (24x24 stroke icons)
ICONS = {
    "ac": '<path d="M12 2v20M4.2 7l15.6 10M4.2 17L19.8 7M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
    "heat": '<path d="M12 3c2.5 3 5 5.2 5 9a5 5 0 0 1-10 0c0-1.8.8-3 1.8-4.2.4 1.2 1.2 2 2.2 2.2C10.6 8 10.9 5.6 12 3z"/>',
    "home": '<path d="M3 11.5L12 4l9 7.5M5.5 10v10h13V10M10 20v-6h4v6"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/>',
    "duct": '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h8"/>',
    "bell": '<path d="M6 17V11a6 6 0 0 1 12 0v6M4 17h16M12 3V2M10 20.5a2 2 0 0 0 4 0"/>',
}

SERVICE_LINKS = [
    ("A/C Repair", "services/ac-repair/"),
    ("Heating & Furnace Repair", "services/heating-furnace-repair/"),
    ("New HVAC Systems", "services/new-hvac-systems/"),
    ("Maintenance & Tune-Ups", "services/maintenance-tune-ups/"),
    ("Duct Work", "services/duct-work/"),
    ("Emergency HVAC", "services/emergency-hvac/"),
]
AREA_LINKS = [
    ("Wetumpka", "areas/wetumpka/"),
    ("Millbrook", "areas/millbrook/"),
    ("Montgomery", "areas/montgomery/"),
    ("Lake Martin", "areas/lake-martin/"),
]


def head(title, desc, path, ld_blocks):
    ld = "\n".join(
        '<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>" for b in ld_blocks
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b0d12">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{ORIGIN}{u(path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('assets/logo.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/site.css')}">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = "".join(
        f'<a href="{u(p)}"{" class=on" if active == p else ""}>{e(n)}</a>' for n, p in NAV
    )
    m = ['<a href="%s">Home</a>' % u("")]
    m.append('<div class="grp">Services</div>')
    m += [f'<a class="sub" href="{u(p)}">{e(n)}</a>' for n, p in SERVICE_LINKS]
    m.append(f'<a href="{u("comfort-club/")}">Comfort Club</a>')
    m.append(f'<a href="{u("reviews/")}">Reviews</a>')
    m.append('<div class="grp">Service Area</div>')
    m += [f'<a class="sub" href="{u(p)}">{e(n)}</a>' for n, p in AREA_LINKS]
    m.append(f'<a href="{u("about/")}">About</a>')
    m.append(f'<a href="{u("careers/")}">Careers</a>')
    m.append(f'<a href="{u("contact/")}">Contact</a>')
    return f"""<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{u('')}" aria-label="{e(NAME)} home">
      <img src="{u('assets/logo.png')}" alt="{e(NAME)} logo" width="46" height="46">
      <span class="brand-name">McKinley Co.<small>HEATING &amp; COOLING</small></span>
    </a>
    <nav class="main" aria-label="Main">{links}</nav>
    <div class="top-cta">
      <a class="btn btn-ghost" href="tel:{TEL}" aria-label="Call {PHONE}">{PHONE_SVG}<span>{PHONE}</span></a>
      <a class="btn btn-primary" href="{u('contact/')}">Schedule Now</a>
      <button class="menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile">{''.join(m)}</nav>
<main id="main">
"""


def footer():
    svc = "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in SERVICE_LINKS)
    areas = "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in AREA_LINKS)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>{e(NAME)}</h4>
        <p>Locally owned HVAC sales, service and installation.</p>
        <p>{e(STREET)}<br>Wetumpka, AL 36092<br>Open 24 hours</p>
        <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>Licensed &middot; Local &middot; AL HVAC #{LICENSE}</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Service area</h4><ul>{areas}<li><a href="{u('areas/')}">All areas</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{u('about/')}">About Dylan</a></li>
        <li><a href="{u('comfort-club/')}">Comfort Club</a></li>
        <li><a href="{u('reviews/')}">Reviews</a></li>
        <li><a href="{u('careers/')}">Careers</a></li>
        <li><a href="{u('contact/')}">Contact</a></li>
        <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="{TT}" target="_blank" rel="noopener">TikTok</a></li>
      </ul></div>
    </div>
    <div class="foot-base">&copy; {e(NAME)} &middot; AL HVAC License #{LICENSE}</div>
  </div>
</footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons">
    <span class="ghost-chevron down"><span></span><span></span></span>
    <span class="ghost-chevron up"><span></span><span></span></span>
  </div>
  <p>tektonbybigie.com/mckinley-co-heating-cooling/draft &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def biz_ld(full=True):
    d = {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": ORIGIN + u("#business"),
        "name": NAME,
        "url": ORIGIN + u(""),
        "telephone": "+1-334-782-0347",
        "email": EMAIL,
        "image": OG_IMAGE,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": "Wetumpka",
            "addressRegion": "AL",
            "postalCode": "36092",
            "addressCountry": "US",
        },
        "areaServed": [
            {"@type": "City", "name": "Wetumpka, AL"},
            {"@type": "City", "name": "Millbrook, AL"},
            {"@type": "City", "name": "Montgomery, AL"},
            {"@type": "Place", "name": "Lake Martin, AL"},
            {"@type": "AdministrativeArea", "name": "Elmore County, AL"},
        ],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        },
        "founder": {"@type": "Person", "name": "Dylan Hammonds"},
        "sameAs": [FB, IG, TT],
    }
    if full:
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "42"}
    return d


def crumbs_ld(trail):
    """trail = [(name, path), ...] starting at Home."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u(p)} for i, (n, p) in enumerate(trail)
        ],
    }


def faq_ld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }


def service_ld(name, desc, path, areas=None):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": name,
        "name": name,
        "description": desc,
        "url": ORIGIN + u(path),
        "provider": {"@type": "HVACBusiness", "@id": ORIGIN + u("#business"), "name": NAME},
        "areaServed": areas or [{"@type": "City", "name": "Wetumpka, AL"}, {"@type": "City", "name": "Millbrook, AL"}, {"@type": "City", "name": "Montgomery, AL"}],
    }


def crumbs_html(trail):
    parts = []
    for i, (n, p) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f"<b>{e(n)}</b>")
        else:
            parts.append(f'<a href="{u(p)}">{e(n)}</a>')
    return '<p class="crumbs">' + "<span>/</span>".join(parts) + "</p>"


def page_hero(trail, h1, lede, facts=None, ctas=True):
    f = ""
    if facts:
        f = '<div class="facts">' + "".join(f'<span class="badge">{x}</span>' for x in facts) + "</div>"
    c = ""
    if ctas:
        c = f"""<div class="hero-cta">
        <a class="btn btn-primary" href="{u('contact/')}">Schedule Service</a>
        <a class="btn btn-ghost" href="tel:{TEL}">{PHONE_SVG}Call or text {PHONE}</a>
      </div>"""
    return f"""<section class="page-hero">
  <div class="wrap">
    {crumbs_html(trail)}
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {c}
    {f}
  </div>
</section>
"""


def cta_band(heading="Need a hand with your A/C or heat?", text="Call or text Dylan, or send a request. Open 24 hours."):
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="tel:{TEL}">{PHONE_SVG}Call or text {PHONE}</a>
      <a class="btn btn-ghost" href="{u('contact/')}">Request service online</a>
    </div>
  </div>
</section>
"""


def aside(current=None):
    rel = "".join(
        f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in SERVICE_LINKS if p != current
    )
    areas = "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in AREA_LINKS if p != current)
    return f"""<aside class="side">
  <div class="aside-card cta">
    <h3>Talk to Dylan</h3>
    <p>Call or text any time. We're open 24 hours.</p>
    <a class="btn btn-primary" href="tel:{TEL}">{PHONE_SVG}{PHONE}</a>
    <a class="btn btn-ghost" href="{u('contact/')}">Request service</a>
    <div class="aside-meta"><b>AL HVAC License #{LICENSE}</b><br>Licensed &middot; Local<br>5.0 &#9733; on 42 Google reviews</div>
  </div>
  <div class="aside-card"><h3>Services</h3><ul class="rel">{rel}</ul></div>
  <div class="aside-card"><h3>Where we work</h3><ul class="rel">{areas}</ul></div>
</aside>
"""


def quote(text, who, source="Google review"):
    by = e(who) + (", " + e(source) if source else "")
    return f'<blockquote class="quote"><p>&ldquo;{e(text)}&rdquo;</p><cite>&mdash; {by} &middot; <a href="{u("reviews/")}">see all reviews</a></cite></blockquote>'


def faq_html(faqs):
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    return f'<div class="faq">{items}</div>'


def tick(items):
    return '<ul class="tick">' + "".join(f"<li><span>{e(i)}</span></li>" for i in items) + "</ul>"


def steps(items):
    return '<ol class="steps">' + "".join(f"<li><div><b>{e(b)}</b> {e(t)}</div></li>" for b, t in items) + "</ol>"


def assemble(path, title, desc, active, body, ld_blocks):
    return head(title, desc, path, ld_blocks) + header(active) + body + footer()


# ---- reusable blocks used on more than one page ----

REVIEW_ITEMS = [
    ("google-andrew-kelly.png", "Andrew Kelly &middot; Google review", "Google review by Andrew Kelly, 5 stars: Great HVAC technician! Very affordable, professional, and knowledgeable. He was friendly, easy to talk to, and explained everything clearly. The bottom line is he is honest, does quality work at a fair price. Definitely someone I recommend!", ""),
    ("google-morgan-murphy.png", "Morgan Murphy &middot; Google review", "Google review by Morgan Murphy, 5 stars: Dylan with McKinley Co. Heating & Cooling was great! He came out on a Sunday within 15 minutes and quickly diagnosed the problem with our air conditioner. Very professional and responsive. Will be using him for all of our air conditioning needs! Highly recommend!", ""),
    ("google-charlene-wilson.png", "Charlene Wilson &middot; Google review", "Google review by Charlene Wilson, 5 stars: Dylan is an incredible young man. He came out as soon as I called him. He's dependable, dedicated and honest and a very hard worker. He replaced our furnace and it works fantastic. When I had an air conditioner problem he came out at 8:00 at night and repaired it. I would give him a five star rating.", ""),
    ("google-chelsea-blackerby.png", "Chelsea Blackerby &middot; Google review", "Google review by Chelsea Blackerby, 5 stars: Great prices. Great service. Professional and showed up in a timely manner. Had the a/c repaired in less than 5 minutes! Will recommend to anyone needing the service.", ""),
    ("google-sharon-venable.png", "Sharon Venable &middot; Google review", "Google review by Sharon Venable, 5 stars: I just can't say enough good things about this company! Dylan is so personable and professional. I had never used this company and they didn't know me. He came to fix my A/C issue shortly after I called him. He had cool air running very quickly. His prices are VERY reasonable. Call this company for your A/C needs. You will be happy you did!", ""),
    ("facebook-bo-bishop.png", "Bo Bishop &middot; Facebook comment", "Facebook comment by Bo Bishop: Known Dylan for years. He's a pro! Want to keep from dying from heat exhaustion... Talk to Dylan. He doesn't mess around. He takes care of my personal home and my Rental properties.", "fb"),
]


def carousel():
    items = []
    for img, who, alt, fb in REVIEW_ITEMS:
        src = "Facebook comment" if fb else "Google review"
        items.append(f"""<div class="cf-item" data-who="{who}">
            <div class="cf-card">
              <img src="{u('assets/reviews/' + img)}" draggable="false" alt="{e(alt)}" loading="lazy">
              <div class="src"><i class="{fb}"></i> {src}</div>
            </div>
          </div>""")
    return f"""<div class="cf-wrap">
        <div class="cf-stage" id="cf" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Customer reviews">
          {''.join(items)}
        </div>
        <button class="cf-arrow cf-prev" id="cfPrev" aria-label="Previous review"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button class="cf-arrow cf-next" id="cfNext" aria-label="Next review"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
      <div class="cf-dots" id="cfDots" aria-label="Choose review"></div>
      <p class="cf-hint">Swipe or tap the arrows to browse &middot; every review is screenshotted straight from Google and Facebook.</p>"""


def request_form(prefix="f", heading="Request service", intro="Tell us what's going on and we'll reach out to confirm a time."):
    return f"""<div class="form-card">
        <h3>{heading}</h3>
        <p>{intro}</p>
        <div class="row">
          <div><label for="{prefix}-name">Your name</label><input id="{prefix}-name" type="text" placeholder="Jane Smith"></div>
          <div><label for="{prefix}-phone">Cell phone</label><input id="{prefix}-phone" type="tel" placeholder="(334) 555-0100"></div>
        </div>
        <div class="row">
          <div><label for="{prefix}-email">Email (optional)</label><input id="{prefix}-email" type="email" placeholder="jane@email.com"></div>
          <div>
            <label for="{prefix}-svc">What do you need?</label>
            <select id="{prefix}-svc">
              <option>A/C not cooling</option>
              <option>Heating / furnace issue</option>
              <option>Tune-up / maintenance</option>
              <option>New system quote</option>
              <option>Duct work</option>
              <option>Comfort Club membership</option>
              <option>Emergency &mdash; need help now</option>
              <option>Something else</option>
            </select>
          </div>
        </div>
        <div style="margin-bottom:16px">
          <label for="{prefix}-town">Town</label>
          <input id="{prefix}-town" type="text" placeholder="Wetumpka, Millbrook, Montgomery, Lake Martin...">
        </div>
        <div style="margin-bottom:16px">
          <label for="{prefix}-msg">Tell us more</label>
          <textarea id="{prefix}-msg" rows="4" placeholder="What's happening, and when's a good time?"></textarea>
        </div>
        <button class="btn btn-primary" type="button" style="width:100%">Send Request</button>
        <p class="form-note">[Draft preview &mdash; form submission gets wired to Dylan's email once the site goes live. Structure and fields are ready now.]</p>
      </div>"""
