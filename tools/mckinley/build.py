#!/usr/bin/env python3
"""Builds the McKinley Co multi-page draft site into public/mckinley-co-heating-cooling/draft/.
Run:  python3 tools/mckinley/build.py
Every fact on these pages must trace to a source in PROJECT-SUMMARY.md (Google/Facebook/Instagram/flyers/reviews).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "public", "mckinley-co-heating-cooling", "draft")
OUT = os.path.abspath(OUT)
written = []


def write(path, content):
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    written.append(path or "(home)")


HOME = ("Home", "")

# ------------------------------------------------------------------ verbatim review quotes (all from screenshots/captures)
Q = {
    "sharon": ("He came to fix my A/C issue shortly after I called him. He had cool air running very quickly. His prices are VERY reasonable.", "Sharon Venable", "Google review"),
    "morgan": ("He came out on a Sunday within 15 minutes and quickly diagnosed the problem with our air conditioner. Very professional and responsive.", "Morgan Murphy", "Google review"),
    "charlene": ("He replaced our furnace and it works fantastic. When I had an air conditioner problem he came out at 8:00 at night and repaired it.", "Charlene Wilson", "Google review"),
    "chelsea": ("Great prices. Great service. Professional and showed up in a timely manner.", "Chelsea Blackerby", "Google review"),
    "andrew": ("He was friendly, easy to talk to, and explained everything clearly. The bottom line is he is honest, does quality work at a fair price.", "Andrew Kelly", "Google review"),
    "brent": ("He recently serviced my unit at Lake Martin, and I couldn't be more pleased with the experience. His response time was outstanding, and he provided professional, top-quality service from start…", "Brent E.", "Google review"),
    "yelp": ("Dylan Hammonds was the very personification of professional, hardworking, and HONEST. He answered my emergency plea for help when my AC drain plug was clogged.", "Yelp review", ""),
    "bo": ("Known Dylan for years... He's a pro! ... He takes care of my personal home and my Rental properties.", "Bo Bishop", "Facebook comment"),
}


def qs(*keys):
    return "".join(quote(*Q[k]) for k in keys)


# ------------------------------------------------------------------ services
SERVICES = [
    dict(
        slug="ac-repair", name="A/C Repair", icon="ac",
        h1="A/C repair in Wetumpka, AL", title="A/C Repair in Wetumpka, AL | No-Cool Calls | McKinley Co. HVAC",
        desc="Air conditioner not cooling? McKinley Co. diagnoses and repairs A/C in Wetumpka, Millbrook, Montgomery and Lake Martin. Open 24 hours. Call (334) 782-0347.",
        card="Fast, reliable repairs and no-cool service calls to get you cool again.",
        lede="When your house won't cool down, you want someone who answers the phone, shows up, finds the real problem and fixes it. That's what we do for homeowners in Wetumpka and across the River Region.",
        signs=["Warm air coming out of the vents, or weak airflow", "The system runs constantly but the house never cools", "Ice on the refrigerant lines or the indoor unit", "Water leaking around the indoor unit, or a clogged drain line", "Strange noises, burning smells, or a breaker that keeps tripping", "Power bills climbing with no change in how you use the A/C"],
        does=["No-cool service calls and full system diagnostics", "Air conditioner repairs, including clogged drain lines", "Straight talk on whether a repair makes sense"],
        steps=[("Call or text.", "Reach Dylan at (334) 782-0347. We're open 24 hours."), ("We diagnose it.", "We check the system and find what's actually wrong, not just the symptom."), ("You get a clear explanation.", "We walk you through what we found and what it will take to fix it."), ("We fix it.", "We make the repair and make sure you're cool again.")],
        quotes=["sharon", "chelsea", "yelp"],
        faqs=[
            ("Why is my A/C running but blowing warm air?", "Common causes include a dirty air filter, thermostat settings, a frozen evaporator coil, a failed capacitor or fan motor, or low refrigerant from a leak. Check that the thermostat is set to cool and the filter is clean. If the air is still warm, shut the system off and call us rather than letting it run, because a struggling system can turn a small problem into a bigger one."),
            ("My outdoor unit isn't running. What should I check?", "Check the thermostat first, then the breaker, and make sure nothing is blocking the unit. If the breaker trips again after you reset it once, stop resetting it and call us."),
            ("Should I repair or replace my air conditioner?", "It depends on the age of the system, the cost of the repair, and how often it has been breaking down. Many systems last roughly 15 to 20 years with good care. We'll tell you straight whether a repair makes sense, and if it doesn't we'll walk you through replacement options."),
            ("Do you come out at night and on weekends?", "Yes. Our Google listing shows we're open 24 hours, and customers have written about us coming out on a Sunday and at 8 p.m. Call or text (334) 782-0347."),
        ],
        img=("condenser-unit-clean.png", "Outdoor condenser unit and wiring on a home we service"), imgcap="An outdoor condenser unit on a job.",
        related=["maintenance-tune-ups", "emergency-hvac", "new-hvac-systems"],
    ),
    dict(
        slug="heating-furnace-repair", name="Heating & Furnace Repair", icon="heat",
        h1="Heating and furnace repair in Wetumpka, AL", title="Heating & Furnace Repair in Wetumpka, AL | McKinley Co. HVAC",
        desc="No heat? McKinley Co. repairs and replaces furnaces and heating systems in Wetumpka, Millbrook and Montgomery. Open 24 hours. Call or text (334) 782-0347.",
        card="Furnace repair and replacement before the cold sets in.",
        lede="Alabama winters don't last long, but a cold night with no heat feels like forever. We repair and replace heating systems for homeowners across the River Region.",
        signs=["No heat, or the system blows cool air", "Weak airflow from the vents", "Banging, squealing or rattling when it starts up", "The furnace turns on and off too often", "Rooms that never warm up evenly", "Heating bills climbing without a change in how you use it"],
        does=["Furnace and heating system diagnostics and repair", "Furnace replacement, from the assessment to the install", "Fall heating tune-ups to catch problems before the first cold snap"],
        steps=[("Call or text.", "Reach Dylan at (334) 782-0347 any time."), ("We find the problem.", "We test the system and tell you what failed and why."), ("You choose the fix.", "We lay out repair and replacement options in plain English."), ("Back to warm.", "We make the repair or install the replacement.")],
        quotes=["charlene"],
        faqs=[
            ("How do I know if my furnace needs repair?", "No heat, weak airflow, new noises, a furnace that cycles on and off, and rising bills are the usual signs. If you ever smell gas, leave the house right away and call your gas utility or 911 from outside."),
            ("When should I schedule a heating tune-up?", "In the fall, before you need the heat. Our Comfort Club memberships include a fall heating visit and a spring cooling visit every year."),
            ("Should I repair or replace an older furnace?", "Furnaces often last around 15 to 20 years with good care. If yours is older and needs a major repair, we'll show you the numbers for both so you can decide."),
            ("Do you offer emergency heating service?", "Yes. We're open 24 hours, including nights, weekends and holidays. Call or text (334) 782-0347."),
        ],
        img=None, imgcap="",
        related=["maintenance-tune-ups", "emergency-hvac", "new-hvac-systems"],
    ),
    dict(
        slug="new-hvac-systems", name="New HVAC Systems", icon="home",
        h1="New HVAC systems and installation in Wetumpka, AL", title="New HVAC Systems & Installation | Wetumpka, AL | McKinley Co.",
        desc="HVAC replacement and new system installs in Wetumpka, Millbrook, Montgomery and Lake Martin from McKinley Co. Licensed AL #2025301. Call (334) 782-0347.",
        card="High-efficiency systems sized right for maximum comfort.",
        lede="A new system is a big decision. We help you figure out whether it's time, what size and type fit your home, and then install it right.",
        signs=["The system is 15 or more years old", "Repair bills are adding up", "Some rooms are always too hot or too cold", "Higher power bills every season", "The system runs on older R-22 refrigerant, which was phased out of production in 2020 and gets more expensive to service", "You're building, adding on, or finishing a space"],
        does=["Replacement of air conditioning and heating systems", "System sizing based on your home, not a guess", "Installation of high-efficiency systems sized for your home"],
        steps=[("We look at your home.", "We assess the current system, the ductwork and what your home actually needs."), ("You see your options.", "We explain the choices in plain English, with no pressure."), ("We install it.", "We go over the timeline with you once we've seen your home."), ("We make sure it's right.", "We start the system up and check that it's performing.")],
        quotes=["charlene"],
        faqs=[
            ("How do I know it's time to replace my system?", "Age, repair history and efficiency all matter. A system past 15 years that needs a major repair is often a good candidate. We'll give you an honest recommendation, and if repair makes more sense, we'll say so."),
            ("How long does an installation take?", "That depends on the home and the system. We'll go over the timeline with you once we've seen your home."),
            ("Does my Comfort Club membership help with a new system?", "Yes. Priority members earn $100 per year toward a new system (up to $500 in credit) and Chaos-Free VIP members earn $200 per year (up to $1,000 in credit), applied to a complete HVAC system replacement by McKinley Co."),
            ("Will you look at my ductwork too?", "We'll look at it. Ducts that are leaking or poorly sized can keep a brand-new system from performing, so it's worth checking. See our duct work page for more."),
        ],
        img=None, imgcap="",
        related=["duct-work", "maintenance-tune-ups", "ac-repair"],
    ),
    dict(
        slug="maintenance-tune-ups", name="Maintenance & Tune-Ups", icon="gear",
        h1="HVAC maintenance and tune-ups in Wetumpka, AL", title="HVAC Maintenance & Tune-Ups | Wetumpka, AL | McKinley Co.",
        desc="Seasonal HVAC tune-ups from McKinley Co. in Wetumpka, AL. Join the Chaos-Free Comfort Club from $19.99/month. Call (334) 782-0347.",
        card="Seasonal tune-ups that keep your system running strong all year.",
        lede="Most big HVAC repairs start as small problems nobody caught. Two visits a year, spring for cooling and fall for heating, is the simplest way to keep your system healthy and avoid surprise breakdowns.",
        signs=["It's been more than a year since anyone looked at your system", "Your A/C or furnace is more than five years old", "You've had repeated small problems", "You want to catch issues before summer or winter hits", "You manage rental property and want fewer emergency calls"],
        does=["Condenser coil cleaning", "Drain-line maintenance and flush", "A complete system performance check", "A standard filter during the visit", "Maintenance reminders", "A digital system condition report (Comfort Club members)"],
        steps=[("Spring cooling tune-up.", "Get the A/C ready before the Alabama heat arrives."), ("Fall heating tune-up.", "Get the furnace ready before the first cold snap."), ("Priority when you need us.", "Comfort Club members move to the front of the line.")],
        quotes=["bo", "andrew"],
        faqs=[
            ("How often should an HVAC system be serviced?", "Twice a year is the common recommendation: one visit for cooling in the spring and one for heating in the fall. That's how our Comfort Club plans are built."),
            ("What does a tune-up include?", "Our Comfort Club tune-ups include condenser coil cleaning, drain-line maintenance and flush, a complete system performance check and a standard filter, plus a digital system condition report."),
            ("Is maintenance worth paying for?", "It's meant to catch small problems before they become expensive ones. Some equipment warranties also ask for regular maintenance, so it's worth checking yours."),
            ("What's the Chaos-Free Comfort Club?", "It's our membership plan starting at $19.99 a month, with two seasonal tune-ups, priority scheduling and savings on repairs. See the Comfort Club page for the three plans."),
        ],
        img=None, imgcap="",
        related=["ac-repair", "heating-furnace-repair", "new-hvac-systems"],
    ),
    dict(
        slug="duct-work", name="Duct Work", icon="duct",
        h1="Duct work repair and installation in Wetumpka, AL", title="Duct Work Repair & Installation | Wetumpka, AL | McKinley Co.",
        desc="Duct work installation, repair and sealing in Wetumpka, Millbrook, Montgomery and Lake Martin from McKinley Co. HVAC. Licensed AL #2025301. Call (334) 782-0347.",
        card="Ductwork built, repaired and sealed so the air goes where it should.",
        lede="Your ducts are the part of your HVAC system you never see, and when they leak or are the wrong size, the whole system pays for it. We install and repair duct work for homes across the River Region.",
        signs=["Some rooms are hot while others are cold", "High power bills even with a newer system", "Weak airflow at certain vents", "Dust that returns right after cleaning", "Noisy airflow or rattling in the walls and ceiling", "Visible damage, kinks or disconnected ducts in the attic or crawlspace"],
        does=["Ductwork built, repaired and sealed so the air goes where it should", "Honest answers on whether your ducts are the problem"],
        steps=[("We inspect the ducts.", "We look at the layout, the condition and where the air is going."), ("We tell you what we find.", "You see what's wrong and what it would take to fix it."), ("We repair or install.", "We seal, repair, or build new duct work."), ("We check the airflow.", "We make sure the air is reaching the rooms it should.")],
        quotes=["andrew"],
        faqs=[
            ("How do I know if my ducts are the problem?", "Uneven temperatures between rooms, weak airflow, high bills and visible damage in the attic or crawlspace are the usual signs. A quick inspection will tell us."),
            ("Can leaky ducts really affect my power bill?", "Yes. Air that leaks out of the ducts is air you paid to cool or heat that never reaches the room."),
            ("Do you build new duct work?", "Yes. Ductwork built, repaired and sealed is part of what we do. Call or text us to talk about your project."),
            ("Should the ducts be checked when I replace my system?", "We think so. A new system connected to bad ducts won't perform the way it should."),
        ],
        img=("duct-work-clean.png", "McKinley Co. technician working on ductwork outside a home"), imgcap="On the job: duct work across the River Region.",
        related=["new-hvac-systems", "ac-repair", "maintenance-tune-ups"],
    ),
    dict(
        slug="emergency-hvac", name="Emergency HVAC", icon="bell",
        h1="24-hour emergency HVAC service in Wetumpka, AL", title="24-Hour Emergency HVAC Service | Wetumpka, AL | McKinley Co.",
        desc="Emergency A/C and heating repair in Wetumpka, Millbrook, Montgomery and Lake Martin. McKinley Co. is open 24 hours. Call or text (334) 782-0347.",
        card="We're here when you need us most: nights, weekends and holidays.",
        lede="Your A/C doesn't pick a good time to quit. We're open 24 hours, and customers have written about us coming out on a Sunday and at 8 p.m.",
        signs=["No cooling during dangerous heat, especially with infants, older adults, pets or medical needs in the home", "No heat during a cold snap", "Water leaking from the unit or ceiling", "A burning smell or a breaker that keeps tripping", "A system that stopped working suddenly and won't restart"],
        does=["24-hour call or text line: (334) 782-0347", "Same-day service whenever we can", "A plain-English explanation of what's wrong and your options"],
        steps=[("Call or text.", "Dylan answers at (334) 782-0347, any hour."), ("We get to you fast.", "We head your way as soon as we can."), ("We find the problem.", "Quick diagnosis, plain-English explanation."), ("We get you running again.", "We make the repair as quickly as we can.")],
        quotes=["morgan", "charlene"],
        faqs=[
            ("What counts as an HVAC emergency?", "No cooling in dangerous heat, no heat in the cold, water leaking from the system, a burning smell, or an electrical problem like repeated tripping. If you smell gas, leave the house and call your gas utility or 911 from outside."),
            ("Is there an extra charge for after-hours calls?", "After-hours service can carry a premium. Comfort Club members get a break: Priority members get 25% off the after-hours premium, and Chaos-Free VIP members pay no after-hours premium."),
            ("How fast can you get to me?", "It depends on where we are and what's on the schedule, but customers have written about us coming out within 15 minutes on a Sunday and at 8 p.m. We can't promise a time, but we'll tell you honestly when we can be there."),
            ("What areas do you cover for emergencies?", "Wetumpka, Millbrook, Montgomery, the Lake Martin area and the surrounding River Region. Call to confirm for your address."),
        ],
        img=None, imgcap="",
        related=["ac-repair", "heating-furnace-repair", "maintenance-tune-ups"],
    ),
]
SVC = {s["slug"]: s for s in SERVICES}
# readable phrases ("Signs you need ...", "We provide ... in <town>")
NEED = {"ac-repair": "A/C repair", "heating-furnace-repair": "heating or furnace repair", "new-hvac-systems": "a new HVAC system",
        "maintenance-tune-ups": "HVAC maintenance", "duct-work": "duct work", "emergency-hvac": "emergency HVAC service"}
PROVIDE = {"ac-repair": "A/C repair", "heating-furnace-repair": "heating and furnace repair", "new-hvac-systems": "new HVAC system installation",
           "maintenance-tune-ups": "HVAC maintenance and tune-ups", "duct-work": "duct work", "emergency-hvac": "24-hour emergency HVAC service"}


def service_page(s):
    path = f"services/{s['slug']}/"
    trail = [HOME, ("Services", "services/"), (s["name"], path)]
    related = "".join(f'<li><a href="{u("services/" + r + "/")}">{e(SVC[r]["name"])}</a></li>' for r in s["related"])
    fig = ""
    if s["img"]:
        fig = f'<figure><img src="{u("assets/" + s["img"][0])}" alt="{e(s["img"][1])}" loading="lazy"><figcaption>{e(s["imgcap"])}</figcaption></figure>'
    areas = "".join(f'<a class="chip" href="{u(p)}">{e(n)}</a>' for n, p in AREA_LINKS)
    body = page_hero(trail, e(s["h1"]), e(s["lede"]), facts=["Open 24 hours", "AL HVAC #" + LICENSE, "5.0 &#9733; on 42 Google reviews"])
    body += f"""<div class="wrap content-grid">
  <article class="prose">
    <h2>Signs you need {e(NEED[s['slug']])}</h2>
    {tick(s['signs'])}
    <h2>What we do</h2>
    {tick(s['does'])}
    {fig}
    <h2>What to expect</h2>
    {steps(s['steps'])}
    <h2>What customers say</h2>
    {qs(*s['quotes'])}
    <h2>Common questions</h2>
    {faq_html(s['faqs'])}
    <h2>Where we do this work</h2>
    <p>We provide {e(PROVIDE[s['slug']])} in <a href="{u('areas/wetumpka/')}">Wetumpka</a>, <a href="{u('areas/millbrook/')}">Millbrook</a>, <a href="{u('areas/montgomery/')}">Montgomery</a> and around <a href="{u('areas/lake-martin/')}">Lake Martin</a>.</p>
    <div class="chips" style="margin-bottom:18px">{areas}</div>
    <h2>Related services</h2>
    <ul class="rel">{related}</ul>
  </article>
  {aside(path)}
</div>
{cta_band()}"""
    ld = [service_ld(s["name"], s["desc"], path), crumbs_ld([(n, p) for n, p in trail]), faq_ld(s["faqs"])]
    write(path, assemble(path, s["title"], s["desc"], "services/", body, ld))


def services_hub():
    path = "services/"
    trail = [HOME, ("Services", path)]
    cards = "".join(
        f'<a class="svc" href="{u("services/" + s["slug"] + "/")}"><div class="ico"><svg viewBox="0 0 24 24">{ICONS[s["icon"]]}</svg></div><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p><span class="more">Learn more &rarr;</span></a>'
        for s in SERVICES
    )
    desc = "A/C repair, heating and furnace repair, new HVAC systems, maintenance tune-ups, duct work and 24-hour emergency service from McKinley Co. in Wetumpka, AL."
    body = page_hero(trail, "HVAC services in Wetumpka, AL", "Residential HVAC sales, service and installation. Here's everything we do, and how to reach us when something breaks.", facts=["Open 24 hours", "AL HVAC #" + LICENSE])
    body += f"""<section><div class="wrap"><div class="services-grid c3">{cards}</div>
    <p style="margin-top:30px;color:var(--muted)">Not sure what you need? Call or text Dylan at <a href="tel:{TEL}" style="color:var(--flame)">{PHONE}</a> and describe what's going on. We'll point you in the right direction.</p></div></section>
{cta_band()}"""
    write(path, assemble(path, "HVAC Services in Wetumpka, AL | McKinley Co. Heating & Cooling", desc, "services/", body, [crumbs_ld(trail), biz_ld(False)]))


# ------------------------------------------------------------------ areas
AREAS = [
    dict(slug="wetumpka", name="Wetumpka", drive="Home base", driveKm="Our shop is on Coosa River Pkwy", mi=None,
         intro="Wetumpka is home. Our shop is at 1102 Coosa River Pkwy, and Wetumpka, the Elmore County seat, is where most of our calls start.",
         facts=[("Home base", "Our shop"), ("24 hrs", "Open any hour"), ("5.0 &#9733;", "42 Google reviews")],
         quote=["morgan"], extra="Our shop is right here in Wetumpka, so you're as close to us as it gets."),
    dict(slug="millbrook", name="Millbrook", drive="17 min", mi="11.6 miles via AL-14 W",
         intro="We serve Millbrook and the surrounding Elmore County communities. It's about a 17 minute drive from our Wetumpka shop.",
         facts=[("17 min", "From our shop"), ("11.6 mi", "Via AL-14 W"), ("24 hrs", "Open any hour")],
         quote=["sharon"], extra="Millbrook is on the list of towns we serve."),
    dict(slug="montgomery", name="Montgomery", drive="28 min", mi="20.6 miles via AL-14 W and Coosada Pkwy",
         intro="We serve the Montgomery area from our shop in Wetumpka. It's about a 28 minute drive from our shop to Montgomery.",
         facts=[("28 min", "From our shop"), ("20.6 mi", "Via AL-14 W"), ("24 hrs", "Open any hour")],
         quote=["chelsea"], extra="Montgomery is a big area. Call or text with your address and we'll tell you honestly how soon we can be there."),
    dict(slug="lake-martin", name="Lake Martin", drive="About 31 min", mi="22.9 miles via AL-170 E and AL-63 N",
         intro="We service homes around Lake Martin. It's about a 31 minute drive from our Wetumpka shop, and customers there have already put it in writing.",
         facts=[("31 min", "From our shop"), ("22.9 mi", "Via AL-170 E"), ("24 hrs", "Open any hour")],
         quote=["brent"], qhead="What a Lake Martin customer says", extra="Lake Martin covers a lot of shoreline, so give us your address when you call and we'll confirm we can get to you."),
]


def area_page(a):
    path = f"areas/{a['slug']}/"
    trail = [HOME, ("Service Area", "areas/"), (a["name"], path)]
    title = f"HVAC Service in {a['name']}, AL | A/C & Heating | McKinley Co."
    desc = f"A/C repair, heating, new HVAC systems, tune-ups and 24-hour emergency service for {a['name']}, AL homeowners from McKinley Co. Call or text (334) 782-0347."
    facts = "".join(f'<div class="fact"><strong>{x}</strong><span>{e(y)}</span></div>' for x, y in a["facts"])
    svc = "".join(f'<li><a href="{u("services/" + s["slug"] + "/")}">{e(s["name"])} in {e(a["name"])}</a> &mdash; <span style="color:var(--muted)">{e(s["card"])}</span></li>' for s in SERVICES)
    body = page_hero(trail, f"HVAC service in {e(a['name'])}, AL", e(a["intro"]))
    body += f"""<div class="wrap content-grid">
  <article class="prose">
    <h2>Getting to you</h2>
    <div class="fact-row">{facts}</div>
    <p style="font-size:.78rem;color:var(--muted)">Drive times are from our shop at {e(STREET)}, Wetumpka, per Google Maps with usual traffic.</p>
    <p>{e(a['extra'])}</p>
    <h2>HVAC services in {e(a['name'])}</h2>
    <ul class="rel">{svc}</ul>
    <h2>{e(a.get('qhead', 'What River Region customers say'))}</h2>
    {qs(*a['quote'])}
    <h2>Call or text first</h2>
    <p>The fastest way to get on the schedule is to call or text Dylan at <a href="tel:{TEL}">{PHONE}</a>. Tell us what's going on and your address, and we'll let you know when we can be there. You can also <a href="{u('contact/')}">send a request online</a>.</p>
  </article>
  {aside(path)}
</div>
{cta_band(f"Need HVAC help in {e(a['name'])}?")}"""
    ld = [service_ld("HVAC service", desc, path, areas=[{"@type": "City", "name": a["name"] + ", AL"}]), crumbs_ld(trail)]
    write(path, assemble(path, title, desc, "areas/", body, ld))


def areas_hub():
    path = "areas/"
    trail = [HOME, ("Service Area", path)]
    cards = "".join(
        f'<a class="area-card-link" href="{u("areas/" + a["slug"] + "/")}"><h3>{e(a["name"])}</h3><span class="drive">{e(a["drive"])} from our shop</span><p>{e(a["intro"])}</p></a>'
        for a in AREAS
    )
    desc = "McKinley Co. serves Wetumpka, Millbrook, Montgomery, Lake Martin and the surrounding River Region with A/C, heating and HVAC service. Open 24 hours."
    body = page_hero(trail, "Proudly serving the River Region", "Based in Wetumpka and on the road across Elmore County and the Montgomery area, including the Lake Martin shoreline.")
    body += f"""<section><div class="wrap"><div class="area-cards">{cards}</div>
    <p style="margin-top:30px;color:var(--muted)">Don't see your town? Just ask. Call or text <a href="tel:{TEL}" style="color:var(--flame)">{PHONE}</a> and we'll tell you whether we can get to you.</p></div></section>
{cta_band()}"""
    write(path, assemble(path, "HVAC Service Area: Wetumpka, Millbrook, Montgomery | McKinley Co.", desc, "areas/", body, [crumbs_ld(trail), biz_ld(False)]))


# ------------------------------------------------------------------ comfort club
def comfort_club():
    path = "comfort-club/"
    trail = [HOME, ("Comfort Club", path)]
    desc = "The Chaos-Free Comfort Club from McKinley Co.: HVAC maintenance plans from $19.99/month with seasonal tune-ups and priority scheduling in Wetumpka, AL."
    faqs = [
        ("What is the Chaos-Free Comfort Club?", "It's our HVAC maintenance membership. Members get seasonal tune-ups, priority scheduling and savings on repairs, with three levels so you can pick what fits your home."),
        ("How much does it cost?", "Comfort is $19.99 a month or $219 a year. Priority is $29.99 a month or $329 a year. Chaos-Free VIP is $39.99 a month or $439 a year."),
        ("Can I cover more than one system?", "Yes. You can add another system to your membership for $9.99 a month on Comfort, $14.99 a month on Priority, or $19.99 a month on VIP."),
        ("How does the loyalty credit work?", "Priority members earn $100 per year toward their next HVAC system, up to a $500 credit, and VIP members earn $200 per year, up to $1,000. The credit applies toward a complete HVAC system replacement by McKinley Co. Full terms are provided when you join."),
        ("Where can I read the full terms?", "Full terms are provided when you join. Call or text Dylan at (334) 782-0347 with any questions first."),
    ]
    body = page_hero(trail, "The Chaos-Free <span class='grad-text'>Comfort Club</span>", "Comfort shouldn't be a one-time thing. Catch small problems before they become expensive ones, and move to the front of the line when you need us most.", facts=["3 membership levels", "From $19.99/month"])
    body += f"""<section><div class="wrap">
      <div class="plans">
        <article class="plan">
          <h3>Comfort</h3><p class="tag">Perfect for preventive maintenance.</p>
          <div class="price"><sup>$</sup>19.99<small> /month</small></div><div class="price-year">or $219/year</div>
          <ul class="perks"><li>2 seasonal HVAC maintenance visits (cooling in spring, heating in fall)</li><li>Priority scheduling</li><li>10% off qualifying repairs</li><li>$20 off diagnostic fee</li><li>Standard filter during maintenance</li><li>Condenser coil cleaning</li><li>Drain-line maintenance &amp; flush</li><li>Complete system performance check</li><li>Maintenance reminders</li><li>Digital system condition report</li></ul>
          <a class="btn btn-ghost" href="{u('contact/')}">Join Comfort</a>
        </article>
        <article class="plan featured"><span class="pop">Most popular</span>
          <h3>Priority</h3><p class="tag">More protection. More savings.</p>
          <div class="price"><sup>$</sup>29.99<small> /month</small></div><div class="price-year">or $329/year</div>
          <ul class="perks"><li class="lead">Everything in Comfort, plus:</li><li>Enhanced priority scheduling</li><li>15% off qualifying repairs</li><li>50% off diagnostic fee</li><li>Annual indoor air quality evaluation</li><li>Preferred pricing on HVAC accessories &amp; upgrades</li><li>12-month workmanship coverage on qualifying repairs</li><li>25% off after-hours premium</li><li>Member-only replacement pricing</li><li>$100/year toward your next HVAC system (up to $500 credit)</li></ul>
          <a class="btn btn-primary" href="{u('contact/')}">Join Priority</a>
        </article>
        <article class="plan vip">
          <h3>Chaos-Free VIP</h3><p class="tag">Our highest level of care &amp; priority.</p>
          <div class="price"><sup>$</sup>39.99<small> /month</small></div><div class="price-year">or $439/year</div>
          <ul class="perks"><li class="lead">Everything in Priority, plus:</li><li>First-priority scheduling</li><li>$0 standard-hours diagnostic fee</li><li>No after-hours premium &mdash; we pre-authorize</li><li>Up to 4 standard filters per system annually</li><li>24-month workmanship coverage on qualifying repairs</li><li>Annual HVAC health report</li><li>Annual indoor air quality evaluation</li><li>$200/year toward your next HVAC system (up to $1,000 credit)</li></ul>
          <a class="btn btn-ghost" href="{u('contact/')}">Join VIP</a>
        </article>
      </div>
      <p class="club-notes"><b>Add another system</b> to your membership for +$9.99 (Comfort), +$14.99 (Priority) or +$19.99 (VIP) per month. Loyalty credit applies toward a complete HVAC system replacement by McKinley Co. See full terms when you join.</p>
    </div></section>
    <section style="padding-top:0"><div class="wrap prose" style="max-width:860px">
      <h2>Questions about the Club</h2>{faq_html(faqs)}
      <p>Learn more about <a href="{u('services/maintenance-tune-ups/')}">what a tune-up includes</a> or <a href="{u('services/new-hvac-systems/')}">how your loyalty credit helps with a new system</a>.</p>
    </div></section>
{cta_band("Ready to join the Club?", "Call or text Dylan and we'll get you set up.")}"""
    write(path, assemble(path, "Chaos-Free Comfort Club | HVAC Maintenance Plans | McKinley Co.", desc, "comfort-club/", body, [crumbs_ld(trail), faq_ld(faqs), service_ld("HVAC maintenance membership", desc, path)]))


# ------------------------------------------------------------------ reviews
def reviews_page():
    path = "reviews/"
    trail = [HOME, ("Reviews", path)]
    desc = "Read real McKinley Co. Heating & Cooling reviews: 5.0 stars on 42 Google reviews from Wetumpka, Millbrook, Montgomery and Lake Martin homeowners."
    body = page_hero(trail, "Real reviews. Real customers.", "Swipe through screenshots taken straight from Google and Facebook.", facts=["&#9733; 5.0 &middot; 42 Google reviews"], ctas=False)
    body += f"""<section class="reviews" style="border-top:none"><div class="wrap">{carousel()}
      <p class="reviews-link"><a class="btn btn-ghost" href="{GMAPS}" target="_blank" rel="noopener">Read all 42 Google reviews</a></p></div></section>
    <section><div class="wrap prose" style="max-width:860px">
      <h2>What people keep saying</h2>
      {qs('morgan', 'charlene', 'andrew', 'brent', 'bo')}
      <p>See what these customers hired us for: <a href="{u('services/ac-repair/')}">A/C repair</a>, <a href="{u('services/heating-furnace-repair/')}">furnace replacement</a>, <a href="{u('services/emergency-hvac/')}">emergency service</a>, and <a href="{u('services/maintenance-tune-ups/')}">tune-ups</a>.</p>
    </div></section>
{cta_band("Join the happy customers", "Call or text Dylan, or send a request online.")}"""
    write(path, assemble(path, "McKinley Co. Reviews | 5.0 Stars on Google | Wetumpka, AL", desc, "reviews/", body, [crumbs_ld(trail), biz_ld(True)]))


# ------------------------------------------------------------------ about
def about_page():
    path = "about/"
    trail = [HOME, ("About", path)]
    desc = "Meet Dylan Hammonds, owner of McKinley Co. Heating & Cooling in Wetumpka, AL: locally owned, honest work, fair prices, no shortcuts. Licensed AL #2025301."
    body = page_hero(trail, "Meet Dylan. Your local HVAC guy.", "McKinley Co. is a locally owned, detail-driven HVAC company serving Wetumpka and the River Region.", ctas=False, facts=["Locally owned", "AL HVAC #" + LICENSE, "10+ years experience"])
    body += f"""<div class="wrap content-grid">
  <article class="prose">
    <h2>How we work</h2>
    <p>When your air goes out in an Alabama summer, you want someone who shows up fast, tells you the truth, and charges a fair price. That's the whole business.</p>
    {tick(["Fast response: customers tell us we've been out within 15 minutes on a Sunday and at 8 p.m.", "Honest answers: we diagnose it, explain it clearly, and fix what's actually broken", "Fair prices: customers call our pricing reasonable", "Licensed and insured: Alabama HVAC license #" + LICENSE])}
    <figure><img src="{u('assets/duct-work-clean.png')}" alt="McKinley Co. technician working on ductwork outside a home" loading="lazy"><figcaption>On the job across the River Region.</figcaption></figure>
    <h2>What we do</h2>
    <p>We handle <a href="{u('services/ac-repair/')}">A/C repair</a>, <a href="{u('services/heating-furnace-repair/')}">heating and furnace repair</a>, <a href="{u('services/new-hvac-systems/')}">new system installs</a>, <a href="{u('services/maintenance-tune-ups/')}">maintenance</a>, <a href="{u('services/duct-work/')}">duct work</a> and <a href="{u('services/emergency-hvac/')}">24-hour emergency service</a>, for homeowners in <a href="{u('areas/wetumpka/')}">Wetumpka</a>, <a href="{u('areas/millbrook/')}">Millbrook</a>, <a href="{u('areas/montgomery/')}">Montgomery</a> and around <a href="{u('areas/lake-martin/')}">Lake Martin</a>.</p>
    <h2>What customers say</h2>
    {qs('bo', 'andrew')}
    <h2>Join the team</h2>
    <p>We're growing. See our <a href="{u('careers/')}">open positions</a>.</p>
  </article>
  {aside(path)}
</div>
{cta_band()}"""
    write(path, assemble(path, "About McKinley Co. | Dylan Hammonds, Wetumpka AL HVAC", desc, "about/", body, [crumbs_ld(trail), biz_ld(False)]))


# ------------------------------------------------------------------ careers
def careers_page():
    path = "careers/"
    trail = [HOME, ("Careers", path)]
    desc = "McKinley Co. Heating & Cooling is hiring HVAC installers and service techs in Wetumpka, AL. Helpers and apprentices welcome. Text or call (334) 782-0347."
    perks = [
        ("Competitive pay", "dollar", '<path d="M12 3v18M16 7.5c0-1.7-1.8-3-4-3s-4 1.1-4 3 1.7 2.7 4 3.2 4 1.2 4 3.1-1.8 3.2-4 3.2-4-1.3-4-3"/>'),
        ("Bonuses & performance incentives", "star", '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>'),
        ("Top-of-the-line tools & equipment", "tool", '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L3 17.7 6.3 21l6.3-6.3a4 4 0 0 0 5.1-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
        ("Ongoing training & growth", "up", '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>'),
        ("Service, maintenance & installs", "gear", ICONS["gear"]),
        ("A team that values pride, loyalty & hard work", "team", '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M17 11a3 3 0 1 0 0-6M21 20c0-2.6-1.5-4.8-3.7-5.6"/>'),
    ]
    pk = "".join(f'<div class="perk"><span class="ico"><svg viewBox="0 0 24 24">{svg}</svg></span><div><strong>{e(t)}</strong></div></div>' for t, _, svg in perks)
    body = page_hero(trail, "Join the team that turns chaos into comfort", "We're looking for HVAC installers and service techs. Helpers and apprentices are welcome. If you've got the drive, we'll bring the training.", ctas=False, facts=["Now hiring", "Helpers / apprentices welcome"])
    body += f"""<section class="careers" style="padding-top:54px"><div class="wrap careers-grid">
      <div>
        <h2 class="section-title">What you get</h2>
        <div class="perk-grid">{pk}</div>
        <p class="pledge">Built on hard work. <em>Backed by experience.</em></p>
        <p class="lede" style="margin-bottom:18px">If you take pride in quality work, customer service, and doing the job right, let's talk.</p>
        <div class="apply-alt">
          <a class="btn btn-primary" href="tel:{TEL}">Text or call {PHONE}</a>
          <a class="btn btn-ghost" href="{IG}" target="_blank" rel="noopener">DM @mckinleyco.hvac</a>
        </div>
      </div>
      <div class="form-card">
        <h3>Apply now</h3>
        <p>Tell us a little about you and we'll reach out. Prefer to just text? Use the number on the left.</p>
        <div class="row">
          <div><label for="a-name">Your name</label><input id="a-name" type="text" placeholder="John Smith"></div>
          <div><label for="a-phone">Cell phone</label><input id="a-phone" type="tel" placeholder="(334) 555-0100"></div>
        </div>
        <div class="row">
          <div><label for="a-email">Email (optional)</label><input id="a-email" type="email" placeholder="john@email.com"></div>
          <div><label for="a-role">Role you're interested in</label><select id="a-role"><option>HVAC installer</option><option>Service technician</option><option>Helper / apprentice</option></select></div>
        </div>
        <div class="row">
          <div><label for="a-exp">HVAC experience</label><select id="a-exp"><option>New to HVAC</option><option>1&ndash;2 years</option><option>3&ndash;5 years</option><option>5+ years</option></select></div>
          <div><label for="a-city">Where do you live?</label><input id="a-city" type="text" placeholder="Wetumpka, Millbrook..."></div>
        </div>
        <div style="margin-bottom:16px"><label for="a-msg">Tell us about yourself</label><textarea id="a-msg" rows="4" placeholder="Work history, certifications, what you're looking for..."></textarea></div>
        <button class="btn btn-primary" type="button" style="width:100%">Send Application</button>
        <p class="form-note">[Draft preview &mdash; applications get wired to Dylan's email once the site goes live. Structure and fields are ready now.]</p>
      </div>
    </div></section>"""
    write(path, assemble(path, "HVAC Jobs in Wetumpka, AL | Now Hiring | McKinley Co.", desc, "careers/", body, [crumbs_ld(trail)]))


# ------------------------------------------------------------------ contact
def contact_page():
    path = "contact/"
    trail = [HOME, ("Contact", path)]
    desc = "Contact McKinley Co. Heating & Cooling in Wetumpka, AL. Call or text (334) 782-0347, 1102 Coosa River Pkwy. Open 24 hours. Request HVAC service online."
    info = f"""<ul class="info-list">
          <li><span class="ico"><svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg></span><div><b>Call or text</b><a href="tel:{TEL}">{PHONE}</a></div></li>
          <li><span class="ico"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
          <li><span class="ico"><svg viewBox="0 0 24 24"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span><div><b>Shop</b><a href="{GMAPS}" target="_blank" rel="noopener">{e(STREET)}<br>Wetumpka, AL 36092</a></div></li>
          <li><span class="ico"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><div><b>Hours</b><a href="tel:{TEL}">Open 24 hours &mdash; emergency calls welcome</a></div></li>
        </ul>
        <div class="socials"><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{TT}" target="_blank" rel="noopener">TikTok</a></div>"""
    body = page_hero(trail, "Let's get you comfortable", "Call, text or send a request. We'll get back to you fast.", ctas=False, facts=["Open 24 hours", "AL HVAC #" + LICENSE])
    body += f"""<section class="contact" style="border-top:none"><div class="wrap contact-grid"><div>{info}</div>{request_form('c')}</div></section>"""
    write(path, assemble(path, "Contact McKinley Co. HVAC | Wetumpka, AL | (334) 782-0347", desc, "contact/", body, [crumbs_ld(trail), biz_ld(False)]))


# ------------------------------------------------------------------ home
def home_page():
    desc = "Locally owned HVAC sales, service and installation in Wetumpka, Millbrook, Montgomery and Lake Martin. 5.0 stars on Google. Licensed AL #2025301."
    cards = "".join(
        f'<a class="svc{" emergency" if s["slug"] == "emergency-hvac" else ""}" href="{u("services/" + s["slug"] + "/")}"><div class="ico"><svg viewBox="0 0 24 24">{ICONS[s["icon"]]}</svg></div><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p><span class="more">Learn more &rarr;</span></a>'
        for s in SERVICES
    )
    chips = "".join(f'<a class="chip{" home" if n == "Wetumpka" else ""}" href="{u(p)}">{e(n)}</a>' for n, p in AREA_LINKS)
    body = f"""<section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">Wetumpka &middot; Millbrook &middot; Montgomery River Region</p>
        <h1>We turn <span class="grad-text">chaos</span> into comfort.</h1>
        <p class="sub">Locally owned, detail-driven HVAC sales, service and installation for Wetumpka and the River Region. Honest work. Fair prices.</p>
        <div class="hero-cta">
          <a class="btn btn-primary" href="{u('contact/')}">Schedule Service</a>
          <a class="btn btn-ghost" href="tel:{TEL}">{PHONE_SVG}Call {PHONE}</a>
        </div>
        <div class="badges">
          <span class="badge"><b>&#9733; 5.0</b> on Google &middot; 42 reviews</span>
          <span class="badge">Licensed &middot; AL #{LICENSE}</span>
          <span class="badge">Open 24 hours</span>
        </div>
      </div>
      <div class="hero-photo">
        <img src="{u('assets/trucks-hero-clean.png')}" alt="McKinley Co. Heating &amp; Cooling service truck and van parked at the shop">
        <div class="hero-tag"><strong>Licensed &middot; Insured &middot; Local</strong><span>10+ years experience</span></div>
      </div>
    </div>
  </section>
  <div class="trust"><div class="wrap trust-grid">
    <div class="trust-item"><strong>5.0 &#9733;</strong><span>Google rating</span></div>
    <div class="trust-item"><strong>10+ YRS</strong><span>In the trade</span></div>
    <div class="trust-item"><strong>24 HRS</strong><span>Emergency service</span></div>
    <div class="trust-item"><strong>#{LICENSE}</strong><span>AL HVAC license</span></div>
  </div></div>
  <div class="hire-strip"><div class="wrap"><b>Now hiring</b><span>HVAC installers &amp; service techs &mdash; helpers and apprentices welcome.</span><a href="{u('careers/')}">See the openings &rarr;</a></div></div>

  <section><div class="wrap">
    <p class="eyebrow">What we do</p>
    <h2 class="section-title">HVAC service done <span class="grad-text">right.</span></h2>
    <p class="lede">From a house that won't cool down to a full system replacement &mdash; one local team, straight answers, and fair prices.</p>
    <div class="services-grid c3">{cards}</div>
  </div></section>

  <section class="about"><div class="wrap about-grid">
    <figure class="about-photo" style="margin:0"><img src="{u('assets/duct-work-clean.png')}" alt="McKinley Co. technician working on ductwork outside a home"><figcaption>On the job across the River Region.</figcaption></figure>
    <div>
      <p class="eyebrow">About McKinley Co.</p>
      <h2 class="section-title">Meet Dylan. <span class="grad-text">Your local HVAC guy.</span></h2>
      <p>McKinley Co. is a locally owned, detail-driven HVAC company serving Wetumpka and the River Region. When your air goes out in an Alabama summer, you want someone who shows up fast, tells you the truth, and charges a fair price &mdash; that's the whole business.</p>
      <ul class="promise-list">
        <li><span class="dot"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><div><strong>Fast response</strong><span>Customers tell us we've been out within 15 minutes, even on a Sunday.</span></div></li>
        <li><span class="dot"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><div><strong>Honest answers</strong><span>We diagnose it, explain it clearly, and fix what's actually broken.</span></div></li>
        <li><span class="dot"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><div><strong>Fair prices</strong><span>Customers call our prices reasonable. Licensed and insured, AL #{LICENSE}.</span></div></li>
      </ul>
      <p style="margin-top:20px"><a class="btn btn-ghost" href="{u('about/')}">More about us</a></p>
    </div>
  </div></section>

  <section><div class="wrap">
    <div class="club-head"><p class="eyebrow">Maintenance membership</p>
    <h2 class="section-title">The Chaos-Free <span class="grad-text">Comfort Club</span></h2>
    <p class="lede">Comfort shouldn't be a one-time thing. Catch small problems before they become expensive ones.</p></div>
    <div class="club-mini">
      <a href="{u('comfort-club/')}"><h3>Comfort</h3><div class="p">$19.99<small> /month</small></div><p>Two seasonal tune-ups, priority scheduling, and savings on repairs.</p></a>
      <a class="feat" href="{u('comfort-club/')}"><h3>Priority <span style="font-size:.7rem;color:var(--flame);letter-spacing:.12em">MOST POPULAR</span></h3><div class="p">$29.99<small> /month</small></div><p>More savings, air quality evaluation, and credit toward your next system.</p></a>
      <a href="{u('comfort-club/')}"><h3>Chaos-Free VIP</h3><div class="p">$39.99<small> /month</small></div><p>First-priority scheduling, no after-hours premium, and our highest level of care.</p></a>
    </div>
    <p style="text-align:center;margin-top:24px"><a class="btn btn-primary" href="{u('comfort-club/')}">See every perk</a></p>
  </div></section>

  <section class="reviews" id="reviews"><div class="wrap">
    <div class="reviews-head">
      <p class="eyebrow">Straight from your neighbors</p>
      <h2 class="section-title">Real reviews. <span class="grad-text">Real customers.</span></h2>
      <div class="rating-pill"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 &middot; 42 Google reviews</div>
    </div>
    {carousel()}
    <p class="reviews-link"><a class="btn btn-ghost" href="{u('reviews/')}">More reviews</a></p>
  </div></section>

  <section><div class="wrap area-grid">
    <div>
      <p class="eyebrow">Where we work</p>
      <h2 class="section-title">Proudly serving the <span class="grad-text">River Region.</span></h2>
      <p class="lede">Based in Wetumpka and out on the road across Elmore County and the Montgomery area &mdash; including the Lake Martin shoreline.</p>
      <div class="chips">{chips}</div>
    </div>
    <div class="area-card">
      <h3>Not sure if we cover you?</h3>
      <p>Just ask. If you're anywhere near the River Region, give Dylan a call or send a message &mdash; if we can get to you, we'll be there.</p>
      <a class="btn btn-primary" href="tel:{TEL}">Call {PHONE}</a>
    </div>
  </div></section>

  <section class="contact" id="contact"><div class="wrap contact-grid">
    <div>
      <p class="eyebrow">Get on the schedule</p>
      <h2 class="section-title">Let's get you <span class="grad-text">comfortable.</span></h2>
      <p class="lede">Call, text or send a request. We'll get back to you fast.</p>
      <ul class="info-list">
        <li><span class="ico"><svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg></span><div><b>Call or text</b><a href="tel:{TEL}">{PHONE}</a></div></li>
        <li><span class="ico"><svg viewBox="0 0 24 24"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span><div><b>Shop</b><a href="{GMAPS}" target="_blank" rel="noopener">{e(STREET)}<br>Wetumpka, AL 36092</a></div></li>
        <li><span class="ico"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><div><b>Hours</b><a href="tel:{TEL}">Open 24 hours &mdash; emergency calls welcome</a></div></li>
      </ul>
    </div>
    {request_form('f')}
  </div></section>"""
    write("", assemble("", "McKinley Co. Heating & Cooling | HVAC in Wetumpka, AL", desc, None, body, [biz_ld(True)]))


if __name__ == "__main__":
    home_page()
    services_hub()
    for s in SERVICES:
        service_page(s)
    areas_hub()
    for a in AREAS:
        area_page(a)
    comfort_club()
    reviews_page()
    about_page()
    careers_page()
    contact_page()
    print(f"built {len(written)} pages into {OUT}:")
    for w in written:
        print("  ", "/" + w)
