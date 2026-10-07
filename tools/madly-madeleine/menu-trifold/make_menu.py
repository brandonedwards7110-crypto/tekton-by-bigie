#!/usr/bin/env python3
"""Madly Madeleine printed menu: US Letter landscape, tri-fold (two sides), styled like the website.
Run:  python3 tools/madly-madeleine/menu-trifold/make_menu.py   -> out/menu.html, out/Madly-Madeleine-trifold-menu.pdf, out/p-1.png, out/p-2.png

CONTENT RULE: every item and price comes from the photos of their printed menu (2026-10-07). Anything not confirmed shows as a
yellow [confirm] tag so a proof can't be mistaken for final. Page 1 = outside (flap | back | front cover). Page 2 = inside (3 panels).
Print double-sided, flip on the SHORT edge, fold the flap panel in first. Photos are the web-size crops from the draft site;
swap in the owners' original full-size photos before a real print run."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PH = "file://" + os.path.abspath(os.path.join(HERE, "..", "..", "..", "public", "madly-madeleine", "draft", "assets", "photos")) + "/"
os.makedirs(OUT, exist_ok=True)

CONFIRM = '<span class="confirm">confirm</span>'

def rows(items):
    """items: (name, desc, price_html)"""
    return "".join(
        f'<div class="row"><div class="mi"><b>{n}</b>{f"<i>{d}</i>" if d else ""}</div><div class="pr">{p}</div></div>' for n, d, p in items)

def grid(head, items):
    """size grid: head = column labels, items = (name, desc, [prices])"""
    cols = "".join(f"<span>{h}</span>" for h in head)
    body = "".join(
        f'<div class="grow"><div class="mi"><b>{n}</b>{f"<i>{d}</i>" if d else ""}</div>' +
        "".join(f"<span class='gp'>{p}</span>" for p in ps) + "</div>" for n, d, ps in items)
    return f'<div class="ghead"><div></div>{cols}</div>{body}'

CSS = """
@page{size:11in 8.5in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
:root{--cream:#fbf4ee;--blush:#f6e3e5;--pink:#efccd1;--rose:#a45a6a;--rose-dark:#7d3f4f;--cocoa:#3b2427;--gold:#b98a5a;--muted:#7a5d62;--line:rgba(125,63,79,.28)}
body{font-family:"Montserrat",Arial,sans-serif;color:var(--cocoa);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:11in;height:8.5in;display:grid;grid-template-columns:repeat(3,1fr);page-break-after:always;overflow:hidden;position:relative}
.sheet:last-child{page-break-after:auto}
.panel{position:relative;padding:.34in .3in .3in;overflow:hidden;display:flex;flex-direction:column}
.panel + .panel{border-left:0}
.cream{background:var(--cream)}.blush{background:var(--blush)}.pink{background:var(--pink)}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;line-height:1.05;margin:0;color:var(--cocoa)}
h2{font-size:17pt;letter-spacing:.01em}
h2 em,h1 em{font-family:"Pinyon Script",cursive;font-style:normal;font-weight:400;color:var(--rose);font-size:1.25em;line-height:1}
.kicker{font-size:6pt;letter-spacing:.24em;text-transform:uppercase;color:var(--rose);font-weight:600;margin:0 0 5px}
.sub{font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;font-size:9.6pt;color:var(--muted);margin:3px 0 7px;line-height:1.2}
.sec{margin-top:11px}
.sec:first-child{margin-top:0}
.row{display:flex;justify-content:space-between;gap:8px;padding:4.2px 0;border-bottom:1px dotted var(--line)}
.mi{display:flex;flex-direction:column;gap:1px;min-width:0}
.mi b{font-family:"Cormorant Garamond",Georgia,serif;font-size:11.4pt;font-weight:700;line-height:1.1}
.mi i{font-style:normal;font-size:6.5pt;color:var(--muted);line-height:1.35}
.pr{font-weight:600;font-size:8.2pt;color:var(--rose-dark);white-space:nowrap;padding-top:2px}
.ghead{display:grid;grid-template-columns:1.5fr repeat(var(--n,3),.55fr);gap:4px;font-size:5.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--rose);font-weight:600;border-bottom:1px solid var(--rose);padding-bottom:2px;text-align:right}
.ghead span{text-align:right}
.grow{display:grid;grid-template-columns:1.5fr repeat(var(--n,3),.55fr);gap:4px;padding:4px 0;border-bottom:1px dotted var(--line);align-items:start}
.gp{font-weight:600;font-size:8pt;color:var(--rose-dark);text-align:right;padding-top:2px}
.note{font-size:6.3pt;color:var(--muted);margin:3px 0 5px;font-style:italic}
.photo{border-radius:12px;overflow:hidden;box-shadow:0 6px 16px rgba(125,63,79,.22)}
.photo img{display:block;width:100%;height:100%;object-fit:cover}
.arch{border-radius:999px 999px 14px 14px}
.cap{font-size:5.4pt;color:var(--muted);text-align:center;margin-top:4px;letter-spacing:.06em}
.confirm{background:#fff3a3;color:#5c4a00;font-size:5.4pt;font-weight:700;padding:1px 4px;border-radius:3px;letter-spacing:.06em;text-transform:uppercase}
.center{text-align:center}
p{margin:0}
.txt{font-size:7.7pt;line-height:1.55;color:var(--cocoa)}
.hours{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;font-size:7.8pt;margin-top:5px}
.hours b{font-weight:600;color:var(--rose-dark)}
.steps{counter-reset:s;list-style:none;margin:6px 0 0;padding:0;display:grid;gap:5px}
.steps li{counter-increment:s;display:grid;grid-template-columns:16px 1fr;gap:7px;align-items:start;font-size:7.4pt;line-height:1.4}
.steps li::before{content:counter(s);display:grid;place-items:center;width:16px;height:16px;border-radius:50%;background:var(--rose);color:#fff;font-weight:600;font-size:6.5pt}
.steps b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:10.6pt;line-height:1}
.brand{font-family:"Cormorant Garamond",Georgia,serif;letter-spacing:.2em;font-weight:600;color:var(--cocoa)}
.script{font-family:"Pinyon Script",cursive;color:var(--rose)}
.sep{height:1px;background:var(--line);margin:9px 0}
.foot{margin-top:auto;text-align:center;font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;font-size:9.5pt;color:var(--rose-dark)}
.stripes{position:absolute;left:0;right:0;top:0;height:.55in;background:repeating-linear-gradient(90deg,var(--pink) 0 .09in,var(--blush) .09in .18in)}
.stripes.b{top:auto;bottom:0}
"""

# ------------------------------------------------------------------ PAGE 1: OUTSIDE (flap | back | front cover)
flap = f"""
<section class="panel cream">
  <p class="kicker">Bonjour!</p>
  <h2>Welcome to <em>Madly Madeleine</em></h2>
  <p class="sub">Coffee, tea, cold drinks &amp; French madeleines.</p>
  <div class="photo" style="height:2.35in;margin:4px 0 9px"><img src="{PH}piping-by-hand.jpg" alt=""></div>
  <p class="txt">Behind every little shell, there&rsquo;s a pair of hands. Arnaud pipes each madeleine one at a time, the way it&rsquo;s done back home in France.</p>
  <div class="sep"></div>
  <p class="kicker">Hours</p>
  <div class="hours"><b>Tuesday&ndash;Friday</b><span>10 AM &ndash; 5 PM</span><b>Saturday</b><span>10 AM &ndash; 4 PM</span><b>Sunday &amp; Monday</b><span>Closed</span></div>
  <div class="sep"></div>
  <p class="txt" style="font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:10pt;color:var(--rose-dark)">It&rsquo;s a cake, not a cookie.</p>
  <p class="txt" style="margin-top:3px">A madeleine is a small French cake baked in a traditional shell-shaped mold. Enjoy one with coffee, with tea, or as a special break during your day.</p>
  <div style="display:grid;grid-template-columns:1.15in 1fr;gap:10px;align-items:center;margin-top:auto">
    <div class="photo" style="height:1.15in"><img src="{PH}arnaud.jpg" alt=""></div>
    <p class="txt"><b style="font-family:'Cormorant Garamond',Georgia,serif;font-size:11pt;color:var(--rose-dark)">Meet Arnaud</b><br>The chef behind every little shell.</p>
  </div>
</section>"""

back = f"""
<section class="panel blush">
  <div class="photo" style="height:2.45in;margin-bottom:10px"><img src="{PH}interior-espresso.jpg" alt=""></div>
  <p class="kicker">Visit us</p>
  <h2>Come say <em>bonjour.</em></h2>
  <div class="txt" style="margin-top:6px">3906 US Highway 98, #2<br>Santa Rosa Beach, FL 32459<br><b style="color:var(--rose-dark)">(448) 238-2396</b><br>contact@madlymadeleine.com<br>Instagram &amp; Facebook: <b>@madly.madeleine</b></div>
  <div class="sep"></div>
  <p class="kicker">Order ahead</p>
  <ol class="steps">
    <li><span><b>Email your order</b>contact@madlymadeleine.com: what, how many, and the day you need it.</span></li>
    <li><span><b>We confirm</b>We reply to confirm your order.</span></li>
    <li><span><b>48 hours&rsquo; notice</b>Orders need at least 48 hours&rsquo; notice.</span></li>
    <li><span><b>Pay with Square</b>We send you a payment link once it&rsquo;s confirmed.</span></li>
  </ol>
  <div class="sep"></div>
  <p class="txt"><b style="font-family:'Cormorant Garamond',Georgia,serif;font-size:10.5pt;color:var(--rose-dark)">Gifts &amp; business orders</b><br>Petites Attentions: boxes for clients, guests and teams. Ask us.</p>
  <p class="foot">madlymadeleine.com</p>
</section>"""

cover = f"""
<section class="panel pink center" style="padding-top:.62in;padding-bottom:.62in">
  <div class="stripes"></div><div class="stripes b"></div>
  <img src="{PH}logo.png" alt="" style="width:1.25in;height:1.25in;border-radius:50%;margin:0 auto 12px;box-shadow:0 6px 16px rgba(125,63,79,.2)">
  <div class="brand" style="font-size:7pt;letter-spacing:.34em;color:var(--rose-dark)">THE FRENCH TOUCH</div>
  <div class="script" style="font-size:36pt;line-height:.95;margin-top:10px">Madly</div>
  <div class="brand" style="font-size:25pt;margin-top:-2px">MADELEINE</div>
  <div class="photo arch" style="height:3.55in;width:2.6in;margin:16px auto 0"><img src="{PH}chocolate-box.jpg" alt="" style="object-position:50% 40%"></div>
  <p class="script" style="font-size:15pt;margin-top:11px;line-height:1.05">Your little slice of France<br>by the beach</p>
  <p class="kicker" style="margin-top:9px;margin-bottom:0;line-height:1.7">La P&acirc;tisserie Fran&ccedil;aise<br>Santa Rosa Beach, Florida</p>
</section>"""

page1 = f'<div class="sheet">{flap}{back}{cover}</div>'

# ------------------------------------------------------------------ PAGE 2: INSIDE (3 menu panels)
p1 = f"""
<section class="panel cream">
  <div class="sec"><p class="kicker">I.</p><h2>Les Madeleines <em>Artisanales</em></h2>
  <p class="sub">Freshly baked throughout the day in our kitchen &mdash; &ldquo;Tout chaud, tout doux&rdquo;</p>
  {rows([
    ("Single Artisanal Madeleine", "In-store exclusive: let your senses wander and yield to the secret inspiration of the day.", "$3.50"),
    ("Mini Madeleines", "A box of Mini Golden Whimsy. Come with a decadent companion of your choice: a cloak of dark chocolate, a bath of creamy white chocolate, a buttery sweep of caramel or pistachio.", "$5.90"),
  ])}</div>
  <div class="photo" style="height:2.0in;margin:12px 0 4px"><img src="{PH}madeleine-flavors.jpg" alt=""></div>
  <div class="sec" style="margin-top:18px"><p class="kicker">II.</p><h2>Les Coffrets <em>Gourmands</em></h2>
  <p class="sub">Gift &amp; sharing boxes &mdash; compose your own symphony of flavors, ideal for gifting, beach outings, or sweet moments.</p>
  {rows([
    ("Petite Box &middot; box of 3", "A charming assortment of 3 madeleines of your choice, nestled in our signature box.", "$9.50"),
    ("Gourmande Box &middot; box of 6", "Six freshly baked madeleines selected by you: the perfect afternoon indulgence.", "$18.00"),
    ("Grand Coffret &middot; box of 15", "Fifteen artisanal madeleines crafted for celebrations, gatherings, and lovers of French pastry.", "$40.00"),
  ])}</div>
</section>"""

p2 = f"""
<section class="panel blush">
  <div class="sec"><p class="kicker">Les Boissons</p><h2>Le <em>Caf&eacute;</em> &amp; Hot Specialties</h2>
  <p class="note">Crafted with passion &middot; Plant-based milk option (oat or almond): +$1.00</p>
  <div style="--n:3">{grid(["8 oz","12 oz","16 oz"], [
    ("Double Espresso", "Rich &amp; velvety roast extraction", ["$3.75<br><span style='font-size:5.2pt;font-weight:500'>(4 oz)</span>","",""]),
    ("Caf&eacute; Americano", "Double espresso lengthened with hot water", ["$3.75","$4.00","$4.50"]),
    ("Cappuccino", "Traditional airy foam &amp; bold espresso", ["$4.75","$5.25",""]),
    ("Caf&eacute; Mocha", "Espresso, gourmet chocolate &amp; steamed milk", ["$5.00","$5.50",""]),
    ("Hot Matcha Latte", "A vibrant, earthy blend of pure organic matcha and silky milk", ["","$5.75","$6.25"]),
    ("Hot Chocolate", "Velvety French-style gourmet cocoa", ["$4.00","$4.50","$5.00"]),
    ("London Fog Artisanal <span style='font-weight:500;font-size:8pt'>(hot or iced)</span>", "Organic Earl Grey, fragrant vanilla &amp; steamed milk", ["","","$6.00"]),
  ])}</div></div>
  <div class="sec"><p class="kicker">Organic Rishi Teas &middot; 12 oz &middot; $4.50</p>
  <p class="txt" style="font-size:6.6pt;line-height:1.5">Earl Grey &middot; English Breakfast<br>Jade Cloud &middot; Peach Yuzu Green &middot; Jasmine<br>Turmeric Ginger &middot; Blueberry Hibiscus</p></div>
  <div class="photo" style="height:1.9in;margin-top:auto"><img src="{PH}madeleine-and-coffee.jpg" alt=""></div>
</section>"""

p3 = f"""
<section class="panel cream">
  <div class="sec"><p class="kicker">Iced Coffee &amp; Specialty Lattes</p><h2>Les <em>Glac&eacute;s</em></h2>
  <p class="note">Chilled perfection under the Florida sun &middot; Plant-based milk option (oat or almond): +$1.00</p>
  <div style="--n:2">{grid(["16 oz","24 oz"], [
    ("Iced Caf&eacute; Latte", "Double espresso over ice &amp; cold milk", ["$5.75","$6.75"]),
    ("Iced Masala Chai Latte", "Spiced artisanal chai infusion &amp; cold milk", ["$6.00","$7.00"]),
    ("Iced Matcha Latte &middot; Botanique or Macaron", "Organic matcha &amp; soothing lavender notes, or a sweet strawberry-rose blend", ["$6.50","$7.50"]),
  ])}</div></div>
  <div class="sec"><p class="kicker">Refreshments</p>
  <div style="--n:2">{grid(["16 oz","24 oz"], [
    ("Mademoiselle Rose Lemonade", "Homemade lemonade", ["$4.75","$5.75"]),
    ("La Vie en Rose Iced Tea", "Floral &amp; refreshing", ["$5.00","$6.00"]),
  ])}</div>
  {rows([("French Sparkling Drinks &middot; Maison Perrier, 11 oz", "Blackberry &amp; Lemon &middot; Peach &amp; Cherry &middot; Mango &amp; Coconut &middot; Raspberry &amp; Lime", "$3.50")])}
  <p class="note" style="margin-top:5px">Also: soda &middot; organic chocolate milk box $3.50 &middot; organic apple juice $4.50</p></div>
  <div class="sec"><p class="kicker">La Boutique</p><h2>Souvenir</h2>
  <p class="sub">Take a piece of the French touch home with you.</p>
  {rows([
    ("Gift Bag of 6 Classic Madeleines", "Ideal for a refined gift or to pair with your favorite tea.", CONFIRM),
    ("Gift Bag of 18 Mini Madeleines", "Ideal for a refined gift or to pair with your favorite tea.", CONFIRM),
    ("Signature Ceramic Mug", "Adorned with our signature emblem.", "$18.00"),
  ])}</div>
  <p class="foot">Bon App&eacute;tit &amp; Merci de votre visite&nbsp;!</p>
</section>"""

page2 = f'<div class="sheet">{p1}{p2}{p3}</div>'

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Madly Madeleine tri-fold menu (proof)</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@400;500;600&family=Pinyon+Script&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{page1}{page2}</body></html>"""

html_path = os.path.join(OUT, "menu.html")
open(html_path, "w", encoding="utf-8").write(HTML)
pdf = os.path.join(OUT, "Madly-Madeleine-trifold-menu.pdf")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", "--virtual-time-budget=20000", "file://" + html_path],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(OUT, "p")], check=True)
print("built", pdf)
