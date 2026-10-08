#!/usr/bin/env python3
"""Builds the South Walton Academy spec-draft site into public/south-walton-academy/draft/.
Run from the repo root:  python3 tools/south-walton-academy/build.py   (photos: tools/south-walton-academy/photos.py, run once)

FACT RULE (same as every draft): every claim comes from the school's OWN website, flyers and calendar (read 2026-10-07).
Anything we could not confirm is a visible yellow "[Draft preview - ...]" note addressed to the owner.
CHILD-PRIVACY RULE: no photo, name, story or diagnosis of any child. Photos are buildings, empty rooms, the empty gym and
playground, flyers, and staff portraits that are already on their public Our Staff page. The old "Sponsor a Student" page
names one child and his diagnosis: this draft has a general version instead.
LEFT OUT ON PURPOSE: their FAQ item "Did South Walton Academy close?" (see Brandon's private review Doc, section 5).
"""
import os, json, html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "public", "south-walton-academy", "draft")
BASE = "/south-walton-academy/draft/"       # becomes "/" when the site gets its own domain
ORIGIN = "https://tektonbybigie.com"        # becomes https://southwaltonacademy.com at launch

NAME = "South Walton Academy"
TAGLINE = "Helping Every Child Succeed"      # printed on their own circle logo
PHONE, TEL = "(850) 213-4595", "+18502134595"
FAX = "(850) 213-4596"
EMAIL, GYM_EMAIL, TEE_EMAIL = "info@southwaltonacademy.com", "gym@southwaltonacademy.com", "teeupforautism@southwaltonacademy.com"
STREET, CITY, ZIP = "305 Mack Bayou Rd", "Santa Rosa Beach", "32459"
ADDR_Q = "305+Mack+Bayou+Rd,+Santa+Rosa+Beach,+FL+32459"
GMAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=" + ADDR_Q
FB = "https://www.facebook.com/southwaltonacademy"
IG = "https://www.instagram.com/southwaltonacademy/"
YT = "https://www.youtube.com/@SouthWaltonAcademy"
LI = "https://www.linkedin.com/company/south-walton-academy/"
# every external link below was fetched and returned 200 on 2026-10-07 (the footer "School Enrollment" link on their live site is a 404 typo, so it is not reused)
ENROLL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSc06LUp4_KVffIFrKWDM0aBTWtbVk7aU6w5U6NDWtavzmN2dg/viewform"
PARENT_LOGIN = "https://app.praxischool.com/parent_login.php"
SUMMER_SIGNUP = "https://app.praxischool.com"
DONATE = "https://givebutter.com/SWAdonation"
SPONSOR = "https://givebutter.com/sponsorachild26"
# the next three come from the QR codes printed on their own flyers (decoded 2026-10-07); all load and match the event.
# Their current website still points its Register button at last year's page (7thAnnualTeeup).
TEEUP = "https://givebutter.com/8th-annual-tee-up-for-autism"
FALLFEST = "https://givebutter.com/7th-annual-fall-fest"
ROYALTEA = "https://givebutter.com/SWARoyalTeaParty"
SHOP = "https://south-walton-academy.myshopify.com"
GYM_WAIVER = "https://docs.google.com/forms/d/e/1FAIpQLSdNnuYjE-GA3Xp_ST5AnY-Dg3URfBfVtBx5svzxWr8ptOC-qQ/viewform"
AMERICAN_DREAM = "https://vimeo.com/1153582724"
STEPUP = "https://www.stepupforstudents.org/"
NEWS30A_2026 = "https://30a-tv.com/30a/2026/01/prohibition-repeal-wine-dinner-raises-record-breaking-26260/"
NEWS_WJHG = "https://www.wjhg.com/2024/06/23/7th-annual-hog-bash-back-beach-barbeque-raises-money-area-academy/"
NEWS30A_2021 = "https://30a-tv.com/30a/2021/03/south-walton-academy-to-host-second-annual-tee-up-for-autism-golf-tournament/"
OG_IMAGE = ORIGIN + BASE + "assets/photos/building-front.jpg"

e = lambda s: html.escape(s, quote=True)
u = lambda p="": BASE + p
DRAFT_NOTES = True    # set False at launch, then grep the output for "Draft preview" until none are left
DN = lambda t: f'<p class="note">[Draft preview &mdash; {t}]</p>' if DRAFT_NOTES else ""
NAV = [("The School", "the-school/"), ("Therapy", "therapy/"), ("Admissions", "admissions/"),
       ("Camps &amp; Clubs", "camps-clubs/"), ("Gym", "gym/"), ("Events &amp; Giving", "events/"), ("Contact", "contact/")]
written = []

ICONS = {
    "school": '<path d="M3 10l9-6 9 6"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9L7 7M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M5 12v8h14v-8"/><path d="M12 8c-1-4-6-4-5-1.5.8 1.8 5 1.5 5 1.5zM12 8c1-4 6-4 5-1.5-.8 1.8-5 1.5-5 1.5z"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20v-1a5 5 0 0 1 10 0v1"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2a4.5 4.5 0 0 1 5.5 4.3V20"/>',
    "plan": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 3h6v3H9zM9 12h6M9 16h4"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "book": '<path d="M12 6c-2-1.5-5-2-8-2v14c3 0 6 .5 8 2 2-1.5 5-2 8-2V4c-3 0-6 .5-8 2z"/><path d="M12 6v14"/>',
    "wave": '<path d="M3 10c3-4 6-4 9 0s6 4 9 0"/><path d="M3 16c3-4 6-4 9 0s6 4 9 0"/>',
    "key": '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v4M15 12v3"/>',
}
icon = lambda n: f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[n]}</svg>'
WAVE_PATH = "M0,40 C240,80 480,0 720,32 C960,64 1200,16 1440,48 L1440,80 L0,80 Z"
wave = lambda color, cls="wave": f'<svg class="{cls}" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" focusable="false" style="color:{color}"><path d="{WAVE_PATH}"/></svg>'
SAND, SKY, PAPER, NAVY = "#fff6e6", "#e8f1fa", "#fffdf9", "#082868"


def ld(blocks):
    return "\n".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>" for b in blocks)


def org_ld():
    return {
        "@context": "https://schema.org", "@type": ["School", "EducationalOrganization"], "@id": ORIGIN + u("#school"),
        "name": NAME, "slogan": TAGLINE, "url": ORIGIN + u(""), "telephone": "+1-850-213-4595", "faxNumber": "+1-850-213-4596",
        "email": EMAIL, "image": OG_IMAGE, "logo": ORIGIN + u("assets/photos/logo-circle.png"),
        "description": "Private, non-profit, inclusive school and pediatric therapy center in Santa Rosa Beach, Florida, serving children from PreK 3 through 12th grade.",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressRegion": "FL", "postalCode": ZIP, "addressCountry": "US"},
        "sameAs": [FB, IG, YT, LI],
    }


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": html.unescape(n), "item": ORIGIN + u(p)} for i, (n, p) in enumerate(trail)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in faqs]}


def head(title, desc, path, blocks):
    return f"""<!DOCTYPE html>
<html lang="en" data-size="1">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#082868">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{ORIGIN}{u(path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('assets/photos/logo-circle.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,500;0,700;1,400&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/site.css')}">
{ld(blocks)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    links = "".join(f'<a href="{u(p)}"{" class=on aria-current=page" if active == p else ""}>{n}</a>' for n, p in NAV)
    m = f'<a href="{u()}">Home</a>' + "".join(f'<a href="{u(p)}">{n}</a>' for n, p in NAV) + f'<a href="{u("contact/#tour")}" style="color:#a24a00">Request a tour</a>'
    return f"""<div class="util-wrap">
<div class="util"><div class="wrap">
  <div class="left"><a href="tel:{TEL}" aria-label="Call {PHONE}">&#9990;&nbsp;{PHONE}</a><a href="{PARENT_LOGIN}" target="_blank" rel="noopener">Parent login</a><a href="{DONATE}" target="_blank" rel="noopener">Donate</a></div>
  <div class="right"><a class="tour" href="{u('contact/#tour')}">Request a tour</a><button type="button" id="rsBtn" aria-expanded="false" aria-controls="rs"><span aria-hidden="true">Aa</span> Reading settings</button></div>
</div></div>
<div class="rs" id="rs" role="dialog" aria-label="Reading settings">
  <h2>Make this site easier to read</h2>
  <p class="small">Your choices are remembered on this device only.</p>
  <div class="row"><b id="rs-size">Text size</b>
    <button type="button" data-rs="size-1" aria-pressed="true" aria-label="Normal text size">A</button>
    <button type="button" data-rs="size-2" aria-pressed="false" aria-label="Larger text">A+</button>
    <button type="button" data-rs="size-3" aria-pressed="false" aria-label="Largest text">A++</button></div>
  <div class="row"><button type="button" data-rs="contrast" aria-pressed="false">High contrast</button>
    <button type="button" data-rs="spacing" aria-pressed="false">Roomier spacing</button>
    <button type="button" data-rs="calm" aria-pressed="false">Calm mode (no motion)</button></div>
  <div class="row"><button type="button" class="reset" data-rs="reset">Reset</button></div>
</div>
</div>
<header class="top">
  <div class="wrap top-inner">
    <a class="brand" href="{u()}" aria-label="{e(NAME)}, home">
      <img src="{u('assets/photos/logo-circle.png')}" alt="" width="62" height="62">
      <span class="brand-name">South Walton Academy<small>Private school &amp; pediatric therapy center</small></span>
    </a>
    <nav class="main" aria-label="Main">{links}</nav>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mnav"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span class="lbl">Menu</span></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile">{m}</nav>
<main id="main">
"""


def footer():
    ln = "".join(f'<li><a href="{u(p)}">{n}</a></li>' for n, p in NAV)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <div class="foot-brand"><img src="{u('assets/photos/logo-circle.png')}" alt="" width="64" height="64"><b>South Walton<br>Academy</b></div>
      <p>{TAGLINE}.</p>
      <p>{e(STREET)}<br>{CITY}, FL {ZIP}<br><a href="tel:{TEL}">{PHONE}</a> &middot; Fax {FAX}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><h4>Explore</h4><ul><li><a href="{u()}">Home</a></li>{ln}</ul></div>
    <div><h4>Families</h4><ul>
      <li><a href="{u('contact/#tour')}">Request a tour</a></li>
      <li><a href="{ENROLL_FORM}" target="_blank" rel="noopener">Enrollment inquiry form</a></li>
      <li><a href="{PARENT_LOGIN}" target="_blank" rel="noopener">Parent login</a></li>
      <li><a href="{u('events/#calendar')}">School calendar</a></li></ul></div>
    <div><h4>Support &amp; follow</h4><ul>
      <li><a href="{DONATE}" target="_blank" rel="noopener">Donate</a></li>
      <li><a href="{SHOP}" target="_blank" rel="noopener">SWA Swag shop</a></li>
      <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
      <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
      <li><a href="{YT}" target="_blank" rel="noopener">YouTube</a></li>
      <li><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></li></ul></div>
  </div>
  <div class="wrap foot-base">&copy; South Walton Academy &middot; A private, non-profit school and pediatric therapy center &middot; Built to be calm and easy to read: use &ldquo;Reading settings&rdquo; at the top of any page.</div>
</footer>

<div class="ghost-bar">
  <div class="ghost-bar-chevrons"><span class="ghost-chevron down"><span></span><span></span></span><span class="ghost-chevron up"><span></span><span></span></span></div>
  <p>tektonbybigie.com/south-walton-academy/draft &mdash; Powered by <a href="https://tektonbybigie.com" target="_blank" rel="noopener noreferrer">Tekton by Bigie</a></p>
</div>
<script src="{u('assets/site.js')}"></script>
</body>
</html>
"""


def crumbs_html(trail):
    parts = [f"<b>{n}</b>" if i == len(trail) - 1 else f'<a href="{u(p)}">{n}</a>' for i, (n, p) in enumerate(trail)]
    return '<p class="crumbs">' + "<span>/</span>".join(parts) + "</p>"


def page_hero(trail, h1, lede, kicker=""):
    k = f'<p class="eyebrow">{kicker}</p>' if kicker else ""
    return f"""<section class="page-hero"><div class="sunmark" aria-hidden="true"></div><div class="wrap">
  {crumbs_html(trail)}{k}
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div>{wave(PAPER)}</section>
"""


def photo(name, alt, cls="", caption="", ext="jpg", eager=False):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    ld_ = "" if eager else ' loading="lazy"'
    return f'<figure class="photo {cls}"><img src="{u("assets/photos/" + name + "." + ext)}" alt="{e(alt)}"{ld_}>{cap}</figure>'


def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="ans">{a_html}</div></details>' for q, _, a_html in faqs) + "</div>"


def assemble(path, title, desc, active, body, blocks):
    return head(title, desc, path, blocks) + header(active) + body + footer()


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    written.append(path or "(home)")


def tour_band(h="Come see the school", t="Schedule a tour and meet the team."):
    return f"""<section class="band band-navy section cta-band">{wave(NAVY, "wave wave-in")}<div class="wrap narrow"><h2>{h}</h2><p class="lede">{t}</p>
  <div class="btns"><a class="btn btn-primary" href="{u('contact/#tour')}">Request a tour</a><a class="btn btn-light" href="tel:{TEL}">Call {PHONE}</a></div></div></section>"""


# ====================================================================== FAQ (their own FAQ; "Did SWA close?" left out on purpose)
FAQS = [
    ("What is South Walton Academy?", "South Walton Academy is a private, non-profit, inclusive school and therapy clinic in Santa Rosa Beach, Florida. It integrates education and therapy to meet each child's needs.",
     "<p>South Walton Academy is a private, non-profit, inclusive school and therapy clinic in Santa Rosa Beach, Florida. We offer a supportive environment that brings education and therapy together to meet each child&rsquo;s needs.</p>"),
    ("What ages and grades do you serve?", "The school serves PreK 3 through 12th grade. Therapy serves children of all ages, including early intervention for infants and toddlers.",
     "<p>The school serves PreK 3 through 12th grade, with elementary, middle and high school tracks, dual enrollment, and life skills and vocational support for older students.</p><p>Our therapy clinic serves children of all ages, including early intervention and therapy for infants and toddlers.</p>"),
    ("What makes your school different?", "Small classes with two teachers, on-site therapy, individualized plans, an inclusive environment for neurodiverse learners, and a focus on academics and life skills.",
     "<ul><li>Small class sizes with low student-to-teacher ratios</li><li>On-site therapy services: speech, occupational and behavioral</li><li>Individualized education plans and a flexible curriculum</li><li>A supportive, inclusive environment for neurodiverse learners</li><li>A focus on both academics and life skills</li></ul>"),
    ("Do you offer therapy to children who don't attend the school?", "Yes. The therapy clinic is open to the public for children of all ages, regardless of school enrollment.",
     "<p>Yes. Our therapy clinic is open to the public and serves children of all ages, whether or not they attend the school. Services include speech therapy, occupational therapy, behavioral therapy and ABA, plus evaluations and treatment plans.</p>"),
    ("What scholarship or tuition support is available?", "South Walton Academy accepts Step Up For Students scholarships, including FES-UA and FES-EO, and helps families navigate scholarship applications and funding options.",
     f"<p>We accept Step Up For Students scholarships, including FES-UA (unique abilities, ages 3 and up) and FES-EO (open to students in Florida age 5 and up). We also help families navigate scholarship applications and funding options. <a href=\"{u('admissions/#scholarships')}\">See the scholarship guide.</a></p>"),
    ("How do I enroll my child?", "Enrollment is open year-round as space allows: contact us to schedule a tour, complete an application and student intake, then submit documentation and any scholarship applications.",
     f"<p>Enrollment is open year-round as space allows. To get started:</p><ol><li>Contact us to schedule a tour</li><li>Complete an application and student intake</li><li>Submit documentation and scholarship applications, if applicable</li></ol><p><a href=\"{u('contact/#tour')}\">Request a tour</a> or call <a href=\"tel:{TEL}\">{PHONE}</a>.</p>"),
    ("Where are you located?", f"{STREET}, {CITY}, FL {ZIP}. Phone {PHONE}.",
     f"<p>{e(STREET)}, {CITY}, FL {ZIP}. Call <a href=\"tel:{TEL}\">{PHONE}</a>. <a href=\"{u('contact/')}\">Hours and directions</a>.</p>"),
]


# ====================================================================== HOME
def home():
    desc = "South Walton Academy is a private, non-profit, inclusive school and pediatric therapy center in Santa Rosa Beach, FL for children from PreK 3 through 12th grade."
    body = f"""<section class="hero band"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Santa Rosa Beach, Florida</p>
    <h1>Helping every child <em>succeed.</em></h1>
    <p class="lede">South Walton Academy is a private, non-profit, inclusive school and pediatric therapy center for children from PreK 3 through 12th grade.</p>
    <div class="btns"><a class="btn btn-primary" href="{u('contact/#tour')}">Request a tour</a><a class="btn btn-ghost" href="{u('the-school/')}">Explore the school</a></div>
    <ul class="chips"><li>Non-profit</li><li>Two teachers in every classroom</li><li>Therapy on campus</li></ul>
  </div>
  <div class="hero-art"><div class="sun" aria-hidden="true"></div>
    {photo('building-front', 'The front of the South Walton Academy campus building under a blue sky, with the sun-and-water logo above the entrance', '', '', eager=True)}
  </div>
</div>{wave(PAPER)}</section>

<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Where would you like to start?</p><h2>Find what you need <em>in one tap.</em></h2></div>
  <ul class="doors">
    <li><a class="door" href="{u('the-school/')}"><span class="ic">{icon('school')}</span><h3>A school for my child</h3><p>Small classes, two teachers in every room, and a plan built around each student.</p><span class="go">See the school &rarr;</span></a></li>
    <li><a class="door" href="{u('therapy/')}"><span class="ic">{icon('heart')}</span><h3>Therapy for my child</h3><p>Speech, occupational, ABA and more, open to the public whether or not your child attends our school.</p><span class="go">See therapy &rarr;</span></a></li>
    <li><a class="door" href="{u('camps-clubs/')}"><span class="ic">{icon('sun')}</span><h3>Camps &amp; clubs</h3><p>Summer camp for ages 3 to 14, plus after-school clubs for fishing, crafting and Dungeons and Dragons.</p><span class="go">See camps &amp; clubs &rarr;</span></a></li>
    <li><a class="door" href="{u('events/')}"><span class="ic">{icon('gift')}</span><h3>Support the school</h3><p>Give, sponsor a student, or join an event. We are a non-profit and community support carries our mission.</p><span class="go">Events &amp; giving &rarr;</span></a></li>
  </ul>
</div></section>

<section class="band band-navy section tight">{wave(NAVY, "wave wave-in")}<div class="wrap">
  <ul class="stats">
    <li><b>PreK 3&ndash;12</b><span>grades served</span></li>
    <li><b>2</b><span>teachers in every classroom</span></li>
    <li><b>12&ndash;14</b><span>students per class</span></li>
    <li><b>10 years</b><span>serving our community</span></li>
  </ul>
  {DN("these numbers come from your current website (About page and home page). Please check each one. Your current site also says &ldquo;Accredited.&rdquo; Tell us the accrediting body and we will name it, with a link, right here.")}
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">What makes us different</p><h2>A school and a therapy center, <em>under one roof.</em></h2>
    <p class="lede">Learning goes further when the people who teach and the people who support your child work side by side.</p></div>
  <div class="tiles">
    <div class="tile"><span class="ic">{icon('users')}</span><h3>Small classes</h3><p>Two teachers in every classroom with 12 to 14 students, so every child is seen and known.</p></div>
    <div class="tile"><span class="ic">{icon('plan')}</span><h3>A plan for every student</h3><p>Individualized Care and Academic Plans (ICAPS) set goals around your child, from foundations to career and college planning.</p></div>
    <div class="tile"><span class="ic">{icon('chat')}</span><h3>Therapy on campus</h3><p>Speech, occupational and behavioral therapists work on campus, alongside the classroom.</p></div>
    <div class="tile"><span class="ic">{icon('heart')}</span><h3>Inclusive by design</h3><p>A supportive, welcoming environment for neurodiverse learners, with room to be curious and to grow.</p></div>
    <div class="tile"><span class="ic">{icon('book')}</span><h3>Academics and life skills</h3><p>Discussion-based and project-based learning builds independent thinkers, with life skills and vocational support for older students.</p></div>
    <div class="tile"><span class="ic">{icon('key')}</span><h3>Families welcome</h3><p>We help families navigate scholarship applications and funding options, and enrollment is open year-round as space allows.</p></div>
  </div>
</div></section>

<section class="band band-sky section">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">A look around</p><h2>Rooms made for <em>learning and play.</em></h2></div>
  <div class="gallery">
    {photo('classroom-bright', 'A bright classroom with round tables and blue chairs', '', 'A classroom')}
    <div class="tall">{photo('classroom-nook', 'A cozy corner of a classroom with floor cushions and a soft rug', '', 'A cozy corner')}</div>
    {photo('gym-empty', 'A room with a polished floor, large windows and soft foam obstacle shapes', '', 'A movement room')}
    {photo('playground', 'The playground with climbing bars, a slide and balance stones on turf', '', 'The playground')}
  </div>
  {DN("these photos come from your current website. We chose rooms, the building and the gym, and left out photos of children, because we would want signed photo releases before any child appears on a website. Send your best original, full-size photos and we will swap them in.")}
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head center"><p class="eyebrow">Getting started</p><h2>Enrolling is <em>three simple steps.</em></h2>
    <p class="lede">Enrollment is open year-round as space allows.</p></div>
  <ol class="steps">
    <li><b>Schedule a tour</b><p>Come see the classrooms, meet the team and ask your questions.</p></li>
    <li><b>Apply and complete intake</b><p>Fill out an application and a student intake so we can learn about your child.</p></li>
    <li><b>Send documents and scholarship forms</b><p>Submit documentation and any scholarship applications. We help families through the funding options.</p></li>
  </ol>
  <div class="btns" style="justify-content:center"><a class="btn btn-primary" href="{u('contact/#tour')}">Request a tour</a><a class="btn btn-ghost" href="{u('admissions/')}">Admissions &amp; scholarships</a></div>
</div></section>

<section class="band band-navy section">{wave(NAVY, "wave wave-in")}<div class="wrap">
  <p class="mission">&ldquo;Our mission is to give every child the tools to be successful by providing a broad range of individualized, educational, and therapeutic opportunities for all children.&rdquo;</p>
  <p class="mission-by">South Walton Academy mission statement</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">In the community</p><h2>Neighbors who <em>show up.</em></h2></div>
  <div class="cards3">
    <a class="card newscard" href="{NEWS30A_2026}" target="_blank" rel="noopener"><span class="src">30A Television &middot; January 2026</span><h3>A record-breaking night of support</h3><p>Restaurant Paradis&rsquo; 10th Annual Prohibition Repeal Wine Dinner raised a record-breaking $26,260 for South Walton Academy.</p><span class="go">Read the story &rarr;</span></a>
    <a class="card newscard" href="{AMERICAN_DREAM}" target="_blank" rel="noopener"><span class="src">The American Dream TV: Florida</span><h3>Featured on television</h3><p>The show visited the school and the South Walton community. Watch the feature to learn more about our mission.</p><span class="go">Watch the feature &rarr;</span></a>
    <a class="card newscard" href="{NEWS_WJHG}" target="_blank" rel="noopener"><span class="src">WJHG NewsChannel 7 &middot; June 2024</span><h3>The 7th Annual Hog Bash</h3><p>WJHG featured the Hog Bash benefiting South Walton Academy, a non-profit private school serving children of all abilities.</p><span class="go">Read the story &rarr;</span></a>
  </div>
</div></section>

<section class="band band-sand section tight">{wave(SAND, "wave wave-in")}<div class="wrap">
  <div class="calm-line">{icon('wave')}<p><b>This site is built to be calm.</b> No autoplay, no flashing, and text you can enlarge. Tap <b>&ldquo;Reading settings&rdquo;</b> at the top of any page for bigger text, high contrast, roomier spacing and a no-motion mode.</p></div>
</div></section>
{tour_band()}"""
    write("", assemble("", "South Walton Academy | Private School & Therapy Center, Santa Rosa Beach FL", desc, None, body, [org_ld()]))


# ====================================================================== TEAM data (from their Our Staff page)
def team_html():
    staff = json.load(open(os.path.join(os.path.dirname(__file__), "staff.json"), encoding="utf-8"))
    def card(s, big=False):
        name, role = s["name"], s["role"].replace(" | ", " &middot; ")
        if s["photo"]:
            img = f'<img src="{u("assets/photos/" + s["photo"] + ".jpg")}" alt="Portrait of {e(name)}" loading="lazy">'
        else:
            ini = "".join(w[0] for w in name.replace('"', "").split()[:2]).upper()
            img = f'<div class="ini" aria-hidden="true">{e(ini)}</div>'
        return f'<li class="person">{img}<div class="nm">{e(name)}</div><div class="rl">{role}</div></li>'
    leaders = [s for s in staff if s["name"] in ("Calley Middlebrooks", "Jennifer Filippone")]
    rest = [s for s in staff if s not in leaders]
    def grp(s):
        r = s["role"]
        if "Instructor" in r or "Teaching" in r: return "class"
        if any(k in r for k in ("Therapist", "Speech", "Occupational", "Behavior", "RBT")): return "therapy"
        return "office"
    groups = [("class", "Teachers &amp; instructors"), ("therapy", "Therapy &amp; behavior team"), ("office", "Office &amp; support")]
    out = f'<ul class="leaders" style="list-style:none;padding:0">{"".join(card(s) for s in leaders)}</ul>'
    for key, title in groups:
        cards = "".join(card(s) for s in rest if grp(s) == key)
        out += f'<div class="team-group"><h3>{title}</h3><ul class="team-grid" style="list-style:none;padding:0;margin:0">{cards}</ul></div>'
    return out


# ====================================================================== THE SCHOOL
def school():
    path = "the-school/"; trail = [("Home", ""), ("The School", path)]
    desc = "A private, non-profit, inclusive school in Santa Rosa Beach, FL for PreK 3 through 12th grade: two teachers per classroom, 12 to 14 students, and individualized plans."
    body = page_hero(trail, "A school built around <em>each child.</em>", "Small classes, two teachers in every room, and a plan for every student. Students work at or above grade level with the support of a whole team.", "The school") + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>Grades <em>PreK 3 through 12.</em></h2>
    <p>We offer a seamless educational journey from early childhood through high school graduation, so your child can grow with people who already know them.</p>
    <ul class="ticks"><li>PreK 3 &amp; 4 years old</li><li>Elementary school</li><li>Middle school</li><li>High school</li><li>Dual enrollment (high school + college)</li></ul>
    <div class="btns"><a class="btn btn-primary" href="{u('contact/#tour')}">Request a tour</a><a class="btn btn-ghost" href="{u('admissions/')}">How to enroll</a></div>
  </div>
  {photo('classroom-blue', 'A classroom with round tables, blue chairs and a whiteboard', '', 'Two teachers share every classroom')}
</div></section>

<section class="band band-sky section">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">How learning works here</p><h2>Four things <em>that set us apart.</em></h2></div>
  <div class="cards2">
    <div class="card"><h3>Small class sizes</h3><p>We have two teachers per classroom with 12 to 14 students per class. Lessons are differentiated in every subject and at every level of learning, so students can work at or above their grade level.</p></div>
    <div class="card"><h3>Discussion and project-based learning</h3><p>Students take part in group discussions to explore and deepen their understanding of a topic, and work on projects over time to solve real-world problems or create a final product. Both build critical thinking, collaboration and creativity, and help students become independent thinkers.</p></div>
    <div class="card"><h3>ICAPS: a plan for each student</h3><p>Individualized Care and Academic Plans are created for every student, so teaching meets your child&rsquo;s own goals. In high school this is the start of a career and post-secondary plan. In elementary and middle school it focuses on foundational, developmental and educational building blocks.</p></div>
    <div class="card"><h3>Professionals from many backgrounds</h3><p>Certified teaching instructors with specialties including autism, early childhood education, Orton-Gillingham, dyslexia, math, science, history, psychology, agriculture, aeronautics, English and behavior. Therapists on campus specialize in DIR Floortime, speech, occupational and behavioral therapy.</p></div>
  </div>
  {DN("this page uses the wording from your About and Programs pages, tidied up. Please read each card and tell us anything that is out of date or not exactly how it works today.")}
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Inside the building</p><h2>Calm rooms with <em>space to settle.</em></h2></div>
  <div class="gallery three">
    {photo('classroom-welcome', 'A classroom with a welcome board, a calendar wall and tidy rows of desks', '', 'A classroom ready for the day')}
    {photo('classroom-sofa', 'A small classroom with a sofa, a window and colorful wall decorations', '', 'A small learning room')}
    {photo('classroom-tree', 'A quiet room with a curved table and a tree mural on the wall', '', 'A quiet room for focused work')}
  </div>
  <div class="gallery three" style="margin-top:16px">
    {photo('classroom-color', 'A colorful classroom with blue chairs, curved tables and a daily schedule board', '', 'A colorful classroom')}
    {photo('classroom-lights', 'A room with string lights along the ceiling and a round table', '', 'A softly lit room')}
    {photo('building-entry', 'The front entrance of the school with navy doors', '', 'The front entrance')}
  </div>
</div></section>

<section class="band band-sand section" id="team">{wave(SAND, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">Our team</p><h2>The people who <em>show up every day.</em></h2>
    <p class="lede">Our dedicated staff are passionate people committed to nurturing every student&rsquo;s potential, each bringing their own expertise.</p></div>
  {team_html()}
  {DN("names, roles and portraits are the ones on your current Our Staff page (first name and last initial). Tell us if anyone should be added, removed or listed differently. We still need a proper portrait for Dr. Ashley P. (the photo on your current site is a full-length group photo) to match everyone else&rsquo;s, and portraits for Emily D. (ED) and Life Skills (LS), who show initials for now.")}
</div></section>
{tour_band("Meet the team in person")}"""
    write(path, assemble(path, "The School | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


# ====================================================================== THERAPY
def therapy():
    path = "therapy/"; trail = [("Home", ""), ("Therapy", path)]
    desc = "Pediatric therapy open to the public in Santa Rosa Beach, FL: speech, occupational, ABA, developmental and psychological services, feeding and sensory integration."
    services = [
        ("Speech therapy", "Helps children communicate: speech sounds, language, fluency, voice, social communication, literacy and vocabulary, apraxia of speech, and augmentative and alternative communication.", "chat"),
        ("Occupational therapy", "Helps children build the skills for daily living: fine motor skills and handwriting, sensory processing, visual-motor integration, balance and coordination, play and social skills, and self-care.", "plan"),
        ("ABA therapy", "Applied Behavior Analysis teaches positive, functional skills such as social interaction, play, communication, self-help and daily living. At our school it uses Natural Environment Teaching, which uses play in places a child knows and enjoys.", "users"),
        ("Feeding therapy", "Supports children with picky eating, food aversions, texture sensitivities and oral-motor difficulties, and builds a better relationship with food.", "heart"),
        ("Sensory integration", "Supports how a child&rsquo;s brain organizes information from the senses, which affects learning, behavior and well-being, including focus, regulation and coordination.", "wave"),
        ("Also offered", "Developmental therapy, psychological services, and Integrated Listening Systems (iLs).", "book"),
    ]
    tiles = "".join(f'<div class="tile"><span class="ic">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for t, d, i in services)
    body = page_hero(trail, "Pediatric therapy, <em>open to the public.</em>", "Giving children the tools to succeed. You do not need to attend our school to be part of our therapy center.", "Pediatric therapy center") + f"""
<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">What we offer</p><h2>Therapy that <em>fits your child.</em></h2>
    <p class="lede">Our therapy clinic serves children of all ages, regardless of school enrollment. Services include evaluations and treatment plans.</p></div>
  <div class="tiles">{tiles}</div>
  {DN("service descriptions are based on your Private Therapy page. Please check each one. Do you accept insurance? Do you have a waitlist? Tell us and we will add a clear answer.")}
</div></section>

<section class="band band-sky section">{wave(SKY, "wave wave-in")}<div class="wrap split">
  {photo('speech-room', 'A small therapy room with a child-size table and chairs, shelves of materials and a window', '', 'A therapy room')}
  <div>
    <h2>Therapy and school, <em>side by side.</em></h2>
    <p>For students, therapy happens on the same campus as the classroom, so the people supporting your child can work as a team.</p>
    <p>For families who only need therapy, the clinic is open to the public, with speech, occupational and behavioral services for children of all ages.</p>
    <div class="btns"><a class="btn btn-primary" href="{ENROLL_FORM}" target="_blank" rel="noopener">Clinic inquiry form</a><a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></div>
  </div>
</div></section>
{tour_band("Questions about therapy?", "Call or send a note. We are happy to talk it through.")}"""
    write(path, assemble(path, "Pediatric Therapy Center | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


# ====================================================================== ADMISSIONS & SCHOLARSHIPS
def admissions():
    path = "admissions/"; trail = [("Home", ""), ("Admissions", path)]
    desc = "How to enroll at South Walton Academy in Santa Rosa Beach, FL, plus a plain-language guide to Step Up For Students scholarships (FES-UA, FES-EO, FTC and PEP)."
    sch = [
        ("FES-UA", "Family Empowerment Unique Abilities", "An education savings account (ESA) you can direct to approved providers: schools, therapists, specialists, curriculum, technology and more.", "For students age 3 through grade 12 (or age 22, whichever comes first) who have a specific diagnosis (see the Step Up website for the list). Funds can go to private school tuition and fees, homeschooling options, therapies, tutoring and more."),
        ("FES-EO", "Family Empowerment Education Options", "Pays first toward private school tuition and related fees.", "Available to Florida residents, regardless of household income, who are eligible to attend a K-12 public school. Open to students age 5 and up."),
        ("FTC", "Florida Tax Credit", "Pays first toward private school tuition and related fees.", "Available to Florida residents, regardless of household income, who are eligible to attend a K-12 public school."),
        ("PEP", "Personalized Education Program (part-time students)", "An education savings account (ESA) that works like a bank account to fund a student's educational needs.", "For K-12 Florida residents who are not enrolled in full-time private or public school, regardless of household income. Students must be at least 5 by September 1 of the school year."),
    ]
    sch_html = "".join(f'<div class="card"><h3><span class="abbr">{a}</span> {n}</h3><p><b>What it is:</b> {w}</p><p><b>Who it is for:</b> {who}</p></div>' for a, n, w, who in sch)
    body = page_hero(trail, "Starting here is <em>simple.</em>", "Enrollment is open year-round as space allows. Here is how it works and how families pay for it.", "Admissions &amp; scholarships") + f"""
<section class="section"><div class="wrap">
  <div class="sec-head center"><p class="eyebrow">How to enroll</p><h2>Three steps, <em>and we are with you.</em></h2></div>
  <ol class="steps">
    <li><b>Contact us to schedule a tour</b><p>Call {PHONE} or send a request. Tours are the best way to see if we are the right fit.</p></li>
    <li><b>Complete an application and student intake</b><p>This helps us learn about your child and plan how to support them.</p></li>
    <li><b>Submit documentation and scholarship applications</b><p>If you are using a scholarship, we help families navigate the applications and funding options.</p></li>
  </ol>
  <div class="btns" style="justify-content:center"><a class="btn btn-primary" href="{u('contact/#tour')}">Request a tour</a><a class="btn btn-ghost" href="{ENROLL_FORM}" target="_blank" rel="noopener">Enrollment inquiry form</a></div>
</div></section>

<section class="band band-sky section" id="scholarships">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">Paying for school</p><h2>Step Up For Students <em>scholarships.</em></h2>
    <p class="lede">Families in Florida may be eligible for private school tuition assistance through one of these scholarships. You cannot use more than one scholarship at a time.</p></div>
  <div class="sch">{sch_html}</div>
  <p style="margin-top:22px">Rules and eligibility can change. Always confirm on <a href="{STEPUP}" target="_blank" rel="noopener">stepupforstudents.org</a>, and ask us anything. We are here to help.</p>
  {DN("this guide follows your current Scholarships page. Your FAQ says you accept FES-UA and FES-EO. Please tell us exactly which of these four programs South Walton Academy is approved to accept, and we will mark them here.")}
</div></section>

<section class="section" id="faq"><div class="narrow">
  <div class="sec-head"><p class="eyebrow">Questions</p><h2>Answers <em>for families.</em></h2></div>
  {faq_html(FAQS)}
</div></section>
{tour_band("Ready when you are", "Call us or request a tour. We will walk you through every step.")}"""
    write(path, assemble(path, "Admissions & Scholarships | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), faq_ld(FAQS), org_ld()]))


# ====================================================================== CAMPS & CLUBS
def camps():
    path = "camps-clubs/"; trail = [("Home", ""), ("Camps & Clubs", path)]
    desc = "Summer camp for ages 3 to 14 and after-school clubs at South Walton Academy in Santa Rosa Beach, FL. Fishing club, Dungeons and Dragons, crafting, STEM and 4-H."
    body = page_hero(trail, "Summer camp &amp; <em>after-school clubs.</em>", "Giving children the tools to succeed in fun and creative ways.", "Camps &amp; clubs") + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>Summer <em>camp.</em></h2>
    <p>Designed for various age groups, our camp offers a diverse range of activities that will engage and inspire your child: arts and crafts, sports, science and outdoor adventures. There is something for everyone.</p>
    <ul class="facts">
      <li><b>Ages</b><span>3 to 14 years old</span></li>
      <li><b>Hours</b><span>8:30 to 3:30</span></li>
      <li><b>Themes</b><span>New weekly themes</span></li>
      <li><b>Registration</b><span>$25 non-refundable fee</span></li>
      <li><b>Siblings</b><span>10% sibling discount</span></li>
    </ul>
    <p>Exploration through play, dance, mess and general silliness. Hands-on and interactive, in a safe, inclusive and supportive environment. Space is limited.</p>
    <div class="btns"><a class="btn btn-primary" href="{SUMMER_SIGNUP}" target="_blank" rel="noopener">Summer enrollment</a><a class="btn btn-ghost" href="tel:{TEL}">Call {PHONE}</a></div>
  </div>
  {photo('playground', 'The playground with climbing bars, a slide and balance stones on turf', '', 'The campus playground')}
</div>
<div class="wrap">{DN("camp details are from your Programs page. Send the dates and weekly themes for next summer, and we will add them.")}</div></section>

<section class="band band-sky section">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">After school</p><h2>Clubs <em>kids look forward to.</em></h2>
    <p class="lede">We offer after-school programs and clubs, including but not limited to:</p></div>
  <div class="cards3">
    <div class="card"><h3>Fishing Club</h3><p>After-school club.</p></div>
    <div class="card"><h3>Dungeons and Dragons</h3><p>After-school club.</p></div>
    <div class="card"><h3>Crafting Club</h3><p>After-school club.</p></div>
  </div>
  {DN("your Programs page lists these three clubs by name only. Send the days, times, ages and cost for each, plus any new clubs, and we will add a short description to every card.")}
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Hands-on learning</p><h2>STEM projects &amp; <em>4-H.</em></h2></div>
  <div class="cards2">
    <div class="card"><h3>STEM projects</h3><p>Dynamic, hands-on learning in science, technology, engineering and math to ignite curiosity and a passion for discovery.</p>
      <ul class="ticks"><li><b>Science:</b> experiments in biology, chemistry, physics and environmental science</li><li><b>Technology:</b> coding, robotics and digital media</li><li><b>Engineering:</b> design challenges and building projects</li><li><b>Math:</b> activities that show the real-world uses of math</li></ul></div>
    <div class="card"><h3>4-H programs</h3><p>Youth programs that build skills in agriculture, science, health and citizenship.</p>
      <ul class="ticks"><li><b>Agriculture and animal science:</b> farming, animal care and sustainable practices</li><li><b>STEM exploration:</b> projects and experiments</li><li><b>Healthy living:</b> nutrition, fitness and mental health</li><li><b>Leadership and citizenship:</b> service and leadership opportunities</li></ul></div>
  </div>
  {DN("STEM and 4-H are described on your Programs page. Are both running this year? If so, tell us the schedule and we will add it. If not, we will take them off.")}
</div></section>
{tour_band("Sign up for a summer to remember", "Space is limited. Call us or start your summer enrollment.")}"""
    write(path, assemble(path, "Summer Camp & After-School Clubs | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


# ====================================================================== GYM
def gym():
    path = "gym/"; trail = [("Home", ""), ("Gym", path)]
    desc = "Rent the South Walton Gymnasium in Santa Rosa Beach, FL for birthday parties, team athletics, pickleball, basketball, volleyball and community events."
    uses = [("Community events", "A facility that can be tailored to your next event."), ("Birthday packages", "Birthday parties in the gym."),
            ("Team athletics", "Team sports such as basketball and volleyball."), ("Pickleball", "Pickleball in the gym. Ask about open-play days and times."),
            ("Weekend play", "Ask us about weekend play.")]
    uses_html = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in uses)
    body = page_hero(trail, "The South Walton <em>Gymnasium.</em>", "A diverse range of activities and a facility that can be tailored to your next event. Open to the community on select days and times.", "Gym") + f"""
<section class="section"><div class="wrap">
  {photo('gym-hall', 'Inside the gymnasium: a high steel-beam ceiling with bright lights, tall windows and a blue padded wall', '', 'Inside the gymnasium: high ceilings and natural light', eager=True)}
  {DN("we cropped this photo to show only the building. Your original shows students playing, and we do not put a child&rsquo;s face on a website without a signed photo release from a parent or guardian. That protects the children and the school. Do you have signed photo releases on file, and which children or events do they cover? If you do, we can use the full photo. If you do not, we can use photos with no children in them, or you can get releases signed. Ask your attorney if you want to be sure what your school needs.")}
</div></section>

<section class="section" style="padding-top:0"><div class="wrap split">
  {photo('gym-empty', 'A room with a polished floor, large windows and soft foam obstacle shapes', '', 'A movement and play room on campus')}
  <div>
    <h2>How our gym <em>works.</em></h2>
    <ol class="steps" style="grid-template-columns:1fr;gap:30px;margin-top:34px">
      <li><b>Open to the community</b><p>The gym is open to the community on select days and times.</p></li>
      <li><b>Rentals for private events</b><p>Birthday parties and sports including pickleball, basketball and volleyball, among others.</p></li>
      <li><b>Large space rental</b><p>Contact us for your next large space rental.</p></li>
    </ol>
  </div>
</div></section>

<section class="band band-sky section">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">Ways to use the gym</p><h2>Play, celebrate, <em>practice.</em></h2></div>
  <div class="cards3">{uses_html}</div>
  {DN("these five uses come from the cards on your Our Gym page, and the descriptions are ours. Send your real rental rates, open-play days and times, and what a birthday package includes, and we will replace these lines with exact details.")}
</div></section>

<section class="section"><div class="narrow">
  <div class="card">
    <h2>Book the gym</h2>
    <p>Email or call us for booking information.</p>
    <ul class="info"><li><b>Email</b><a href="mailto:{GYM_EMAIL}">{GYM_EMAIL}</a></li><li><b>Call</b><a href="tel:{TEL}">{PHONE}</a></li><li><b>Address</b><span>{e(STREET)}, {CITY}, FL {ZIP}</span></li></ul>
    <div class="btns"><a class="btn btn-primary" href="mailto:{GYM_EMAIL}?subject=Gym%20booking">Email about the gym</a><a class="btn btn-ghost" href="{GYM_WAIVER}" target="_blank" rel="noopener">Facility waiver</a></div>
  </div>
</div></section>"""
    write(path, assemble(path, "Gym Rentals & Community Play | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


# ====================================================================== EVENTS & GIVING
CAL = [   # (month, [(date, text, kind)]) transcribed from their 2026-2027 school calendar (revised 6/1/26); kind: "", "half", "closed"
    ("August", [("Aug 3&ndash;7", "Drop-In Program open", ""), ("Aug 11&ndash;14", "Professional development / campus closed", "closed"), ("Fri, Aug 14", "Open House &amp; School Party, 2:00&ndash;4:00 PM", ""), ("Mon, Aug 17", "First day of school", "")]),
    ("September", [("Fri, Sep 4", "Professional development / half day, dismissal 11:30 AM", "half"), ("Mon, Sep 7", "Labor Day / campus closed", "closed")]),
    ("October", [("Fri, Oct 9", "Professional development / half day, dismissal 11:30 AM", "half"), ("Mon, Oct 12", "Columbus Day / no school, no clinic / drop-in open", "closed"), ("Fri, Oct 16", "End of 1st nine weeks", ""), ("Fri, Oct 23", "Fall Fest / half day, dismissal 11:30 AM", "half"), ("Fri, Oct 30", "Parent-teacher conferences &amp; report cards / no school / clinic open", "closed")]),
    ("November", [("Wed, Nov 11", "Veterans Day / no school, no clinic / drop-in open", "closed"), ("Fri, Nov 20", "Staff Thanksgiving gathering / half day, dismissal 11:30 AM", "half"), ("Nov 23&ndash;27", "Thanksgiving break / no school, no clinic / drop-in open", "closed")]),
    ("December", [("Fri, Dec 18", "End of 2nd nine weeks / half day, dismissal 11:30 AM / staff celebration", "half"), ("Dec 21&ndash;Jan 4", "Winter break / no school, no clinic", "closed"), ("TBA", "Winter Drop-In Program", "")]),
    ("January", [("Mon, Jan 4", "Staff professional development, 9:00 AM&ndash;4:00 PM / no school", "closed"), ("Tue, Jan 5", "Students return", ""), ("Fri, Jan 8", "Report cards go home", ""), ("Mon, Jan 18", "Martin Luther King Jr. Day / no school, no clinic / drop-in open", "closed"), ("Thu, Jan 28", "100th day of school", "")]),
    ("February", [("Fri, Feb 12", "Valentine&rsquo;s Day class party", ""), ("Mon, Feb 15", "Presidents&rsquo; Day / no school, no clinic / drop-in open", "closed")]),
    ("March", [("Mar 1&ndash;12", "IOWA state testing (eligible students only)", ""), ("Fri, Mar 5", "End of 3rd nine weeks", ""), ("Fri, Mar 12", "Report cards go home", ""), ("Fri, Mar 19", "Professional development / half day, dismissal 11:30 AM", "half"), ("Mar 22&ndash;26", "Spring break / closed", "closed")]),
    ("April", [("Fri, Apr 16", "Professional development day / no school", "closed"), ("Fri, Apr 30", "Professional development / half day, dismissal 11:30 AM", "half")]),
    ("May", [("Fri, May 7", "Parent-teacher conferences / end of 4th nine weeks / no school / clinic open", "closed"), ("Fri, May 14", "Report cards go home", ""), ("Tue, May 18", "Yearbook party", ""), ("Thu, May 20", "Last day of school / half day, dismissal 11:30 AM / clinic open / teacher work day", "half")]),
]


def cal_html():
    lab = {"closed": '<span class="lab">No school</span>', "half": '<span class="lab">Half day</span>', "": ""}
    months = ""
    for m, rows in CAL:
        li = "".join(f'<li class="{k}"><b>{d}</b><span>{lab[k]}{t}</span></li>' for d, t, k in rows)
        months += f'<div class="month"><h3>{m}</h3><ul>{li}</ul></div>'
    return f"""<div class="key" aria-hidden="true"><span><i style="background:#fff"></i>Regular day or event</span><span><i style="background:#e9f2fb;border-color:#2a7fbf"></i>Early dismissal</span><span><i style="background:#fff3e2;border-color:#f09018"></i>No school / closed</span></div>
  <div class="cal">{months}</div>
  <p style="margin-top:18px"><b>Important notes:</b> No aftercare on early dismissal days. Field trips TBA. Drop-in days are available by appointment only. Calendar subject to change (revised 6/1/26).</p>"""


def events():
    path = "events/"; trail = [("Home", ""), ("Events & Giving", path)]
    desc = "Upcoming South Walton Academy events (Fall Festival, Royal Tea Party, Tee Up for Autism), the 2026-2027 school calendar, and ways to give in Santa Rosa Beach, FL."
    body = page_hero(trail, "Events, calendar &amp; <em>ways to give.</em>", "As a non-profit, we rely on community support to carry out our mission of giving children the tools to succeed.", "Events &amp; giving") + f"""
<section class="section"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Coming up</p><h2>Join us at <em>the next event.</em></h2></div>

  <div class="event">
    {photo('flyer-fall-fest', 'Flyer: South Walton Academy Fall Festival fundraiser, October 23, 5:00 to 8:00, wristband $20, with a bounce house, haunted house, games, trunk-or-treat and food', '')}
    <div><span class="when">Friday, October 23</span><h3 style="font-size:1.6rem">Fall Festival fundraiser</h3>
      <ul class="facts"><li><b>Time</b><span>5:00&ndash;8:00 PM</span></li><li><b>Wristband</b><span>$20</span></li><li><b>Where</b><span>{e(STREET)}, {CITY}</span></li></ul>
      <p>Bounce house, haunted house, games, trunk-or-treat and food.</p>
      <div class="btns" style="margin-top:0"><a class="btn btn-primary" href="{FALLFEST}" target="_blank" rel="noopener">Get wristbands</a><a class="btn btn-ghost" href="mailto:{EMAIL}?subject=Fall%20Festival">Questions? Email us</a></div></div>
  </div>

  <div class="event">
    {photo('flyer-royal-tea', 'Flyer: Royal Tea Party, a magical evening of tea, treats and royal fun, November 13, 5:00 to 7:00 PM, $25 per person, come dressed to impress', '')}
    <div><span class="when">Friday, November 13</span><h3 style="font-size:1.6rem">Royal Tea Party</h3>
      <ul class="facts"><li><b>Time</b><span>5:00&ndash;7:00 PM</span></li><li><b>Cost</b><span>$25 per person</span></li></ul>
      <p>A magical evening of tea, treats and royal fun. Come dressed to impress!</p>
      <div class="btns" style="margin-top:0"><a class="btn btn-primary" href="{ROYALTEA}" target="_blank" rel="noopener">Sign up</a><a class="btn btn-ghost" href="mailto:{EMAIL}?subject=Royal%20Tea%20Party">Questions? Email us</a></div></div>
  </div>

  <div class="event">
    {photo('flyer-teeup', 'Flyer: 8th Annual Tee Up For Autism golf tournament, April 24, 8:00 AM registration, 9:00 AM shotgun start, The Links Golf Club, Sandestin, accepting sponsorships and teams', '')}
    <div><span class="when">Saturday, April 24, 2027</span><h3 style="font-size:1.6rem">8th Annual Tee Up For Autism</h3>
      <ul class="facts"><li><b>Registration</b><span>8:00 AM</span></li><li><b>Shotgun start</b><span>9:00 AM</span></li><li><b>Where</b><span>The Links Golf Club, Sandestin</span></li></ul>
      <p>Grab your clubs and get ready for a day of fun, friends and giving back. Teams and sponsorships are open now.</p>
      <div class="btns" style="margin-top:0"><a class="btn btn-primary" href="{TEEUP}" target="_blank" rel="noopener">Register or sponsor</a><a class="btn btn-ghost" href="mailto:{TEE_EMAIL}">Email the tournament team</a></div></div>
  </div>
  {DN("event details come from your three flyers and your home page, and every button goes to the same page as the QR code on that flyer. Your current website&rsquo;s Register button for Tee Up For Autism still goes to last year&rsquo;s (7th annual) page, so we pointed ours at this year&rsquo;s. Please check every date, time and price.")}
</div></section>

<section class="band band-sky section" id="calendar">{wave(SKY, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">School calendar</p><h2>2026&ndash;2027 <em>academic year.</em></h2>
    <p class="lede">Every date below is as printed on your current calendar, now as real text that is easy to read, search and use with a screen reader.</p></div>
  {cal_html()}
  <p style="margin-top:14px"><a href="{u('assets/photos/calendar-2026-27.jpg')}" target="_blank" rel="noopener">Open the original calendar image</a></p>
  {DN("we typed this from your calendar image so it works on a phone. When the calendar changes, tell us (or we can show you how to update it yourself). Please check every date.")}
</div></section>

<section class="section" id="give"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Ways to give</p><h2>Every gift <em>reaches a child.</em></h2></div>
  <div class="cards3">
    <div class="card"><h3>Donate</h3><p>Make a tax-exempt donation to help students of all abilities succeed. South Walton Academy is a non-profit private school and pediatric therapy center (EIN 37-1802451).</p><p><a class="btn btn-primary" href="{DONATE}" target="_blank" rel="noopener">Donate</a></p></div>
    <div class="card"><h3>Sponsor a student</h3><p>Sponsoring a student helps provide academic support, specialized therapies, and inclusion and belonging. Any amount, any help, can transform a life.</p><p><a class="btn btn-primary" href="{SPONSOR}" target="_blank" rel="noopener">Sponsor a student</a></p></div>
    <div class="card"><h3>Sponsor an event</h3><p>Sponsor Tee Up For Autism, register a team, or volunteer on the day. Sponsors are recognized in the program and on social media.</p><p><a class="btn btn-primary" href="{TEEUP}" target="_blank" rel="noopener">Tee Up For Autism</a></p></div>
  </div>
  <p style="margin-top:22px">Prefer to shop? Visit the <a href="{SHOP}" target="_blank" rel="noopener">SWA Swag shop</a>.</p>
  {DN("we wrote the Sponsor a Student section without any child&rsquo;s name, photo, diagnosis or family story. If a family agrees in writing, we can share their story with their permission. Your current page names one student and describes his diagnosis and his family&rsquo;s finances, and we recommend taking that down.")}
</div></section>

<section class="band band-sand section" id="news">{wave(SAND, "wave wave-in")}<div class="wrap">
  <div class="sec-head"><p class="eyebrow">In the news</p><h2>Celebrating <em>10 years</em> of inclusion, education &amp; community.</h2></div>
  <div class="cards3">
    <a class="card newscard" href="{NEWS30A_2026}" target="_blank" rel="noopener"><span class="src">30A Television &middot; January 2026</span><h3>Record-breaking community support</h3><p>Restaurant Paradis&rsquo; 10th Annual Prohibition Repeal Wine Dinner raised a record-breaking $26,260 for South Walton Academy, celebrating a decade of community support.</p><span class="go">Read the story &rarr;</span></a>
    <a class="card newscard" href="{NEWS_WJHG}" target="_blank" rel="noopener"><span class="src">WJHG NewsChannel 7 &middot; June 2024</span><h3>7th Annual Hog Bash</h3><p>WJHG featured the Hog Bash benefiting South Walton Academy as a non-profit private school serving children of all abilities.</p><span class="go">Read the story &rarr;</span></a>
    <a class="card newscard" href="{NEWS30A_2021}" target="_blank" rel="noopener"><span class="src">30A Television &middot; March 2021</span><h3>Tee Up for Autism</h3><p>30A Television featured the Tee Up for Autism Golf Tournament and our commitment to autism awareness, inclusive education and access to pediatric therapy.</p><span class="go">Read the story &rarr;</span></a>
  </div>
  <p style="margin-top:22px"><a class="btn btn-ghost" href="{AMERICAN_DREAM}" target="_blank" rel="noopener">Watch: South Walton Academy on The American Dream TV: Florida</a></p>
</div></section>"""
    write(path, assemble(path, "Events, Calendar & Giving | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


# ====================================================================== CONTACT / VISIT
def contact():
    path = "contact/"; trail = [("Home", ""), ("Contact", path)]
    desc = f"Visit South Walton Academy at {STREET}, {CITY}, FL {ZIP}. Call {PHONE} or request a tour."
    body = page_hero(trail, "Come and <em>see us.</em>", "Feel free to contact us to schedule a visit. We would love to meet you and your child.", "Visit &amp; contact") + f"""
<section class="section"><div class="wrap visit-grid">
  <div>
    <ul class="info">
      <li><b>Address</b><a href="{GMAPS_DIR}" target="_blank" rel="noopener">{e(STREET)}<br>{CITY}, FL {ZIP}</a></li>
      <li><b>Call</b><span><a href="tel:{TEL}">{PHONE}</a> &middot; Fax {FAX}</span></li>
      <li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><b>Hours</b><span>Monday&ndash;Friday 7:45 AM&ndash;5:30 PM<br>Saturday 8:30 AM&ndash;2:30 PM<br>Sunday 1:00 PM&ndash;5:30 PM</span></li>
      <li><b>Gym</b><a href="mailto:{GYM_EMAIL}">{GYM_EMAIL}</a></li>
      <li><b>Tee Up</b><a href="mailto:{TEE_EMAIL}">{TEE_EMAIL}</a></li>
      <li><b>Follow</b><span><a href="{FB}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{IG}" target="_blank" rel="noopener">Instagram</a> &middot; <a href="{YT}" target="_blank" rel="noopener">YouTube</a> &middot; <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></span></li>
    </ul>
    {DN("these are the hours on your current website. Another site lists different hours for Monday and Tuesday. Please tell us the hours for the school, the therapy clinic and the gym, and any holiday hours.")}
    <div class="btns"><a class="btn btn-primary" href="{GMAPS_DIR}" target="_blank" rel="noopener">Get directions</a><a class="btn btn-ghost" href="{PARENT_LOGIN}" target="_blank" rel="noopener">Parent login</a></div>
  </div>
  <div class="mapbox"><iframe title="Map to South Walton Academy" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={ADDR_Q}&z=15&output=embed"></iframe></div>
</div></section>

<section class="band band-sky section" id="tour">{wave(SKY, "wave wave-in")}<div class="narrow">
  <div class="sec-head"><p class="eyebrow">Request a tour</p><h2>Tell us about <em>your child.</em></h2>
    <p class="lede">Tell us a little about your child and what you are looking for.</p></div>
  <div class="form-card">
    <div class="row"><div><label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="name"></div>
    <div><label for="f-phone">Phone</label><input id="f-phone" type="tel" autocomplete="tel"></div></div>
    <label for="f-email">Email</label><input id="f-email" type="email" autocomplete="email">
    <label for="f-int">I am interested in</label>
    <select id="f-int"><option>The school</option><option>Therapy</option><option>Summer camp or clubs</option><option>The gym</option><option>Something else</option></select>
    <label for="f-msg">Your child&rsquo;s age or grade, and any questions</label><textarea id="f-msg" rows="4"></textarea>
    <button class="btn btn-primary" type="button">Send request</button>
    <p class="muted" style="margin:14px 0 0;font-size:.95rem">Prefer to call? Reach us at <a href="tel:{TEL}">{PHONE}</a>. You can also use your <a href="{ENROLL_FORM}" target="_blank" rel="noopener">enrollment inquiry form</a>.</p>
  </div>
  {DN(f"this form is a preview and does not send anything yet. At launch it will email {EMAIL} so your contact form works every time. The form on your current Contact page shows raw code instead of a form.")}
</div></section>"""
    write(path, assemble(path, "Contact & Tours | South Walton Academy, Santa Rosa Beach FL", desc, path, body, [crumbs_ld(trail), org_ld()]))


if __name__ == "__main__":
    home(); school(); therapy(); admissions(); camps(); gym(); events(); contact()
    print(f"built {len(written)} pages into {OUT}:"); [print("  /" + w) for w in written]
