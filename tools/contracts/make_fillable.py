#!/usr/bin/env python3
"""Builds Tekton By Bigie's FILLABLE PDF contracts (Website Plan Agreement, Website Financing Agreement), in English and in
English + Français side by side. Source of the wording: the two TEMPLATE Google Docs in Drive (Web Building/Contracts/) and the
Madly bilingual drafts, 2026-10-07. Differences from the Docs: the blanks are collected in a "Details" box at the top (type once;
names also fill the signature block) and the clauses point to the Details instead of having inline [brackets].

Pipeline: HTML (blanks drawn as uniquely colored boxes) -> headless Chrome PDF -> PyMuPDF finds each box -> pdf-lib (Node) puts a real
form field on top of it. Needs: google chrome, `pip3 install pymupdf`, `npm install` in this folder (pdf-lib).
Run:  python3 tools/contracts/make_fillable.py     Output: tools/contracts/out/*.pdf  (then copy to Drive: Web Building/Contracts/)
"""
import os, sys, json, html, subprocess, tempfile
import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)

e = html.escape

# --------------------------------------------------------------------------- field registry
class Fields:
    """Hands out boxes with a unique fill color per box so the PDF can be scanned for them afterwards."""
    def __init__(self):
        self.items = []     # (name, kind, multiline)
    def _color(self, i, kind):
        return (255, 244, 130 + 3 * i) if kind == "text" else (200, 230, 130 + 3 * i)
    def text(self, name, width="3in", height="0.27in", block=False, multiline=False):
        i = len(self.items); self.items.append((name, "text", multiline))
        r, g, b = self._color(i, "text")
        disp = "display:block;" if block else "display:inline-block;vertical-align:-0.06in;"
        return f'<span class="fld" style="{disp}width:{width};height:{height};background:rgb({r},{g},{b})"></span>'
    def check(self, name):
        i = len(self.items); self.items.append((name, "check", False))
        r, g, b = self._color(i, "check")
        return f'<span class="cbx" style="background:rgb({r},{g},{b})"></span>'

# --------------------------------------------------------------------------- wording (EN | FR)
PLAN = {
    "title": ("Website Plan Agreement", "Contrat de forfait de site web"),
    "sub": ("Hosting and updates", "Hébergement et mises à jour"),
    "intro": (
        "This agreement is between Tekton By Bigie LLC, a Florida limited liability company, 46 Parkside St, Freeport, FL 32439 (the “Provider”), and the business named in the Details above (the “Client”), represented by the contact person named there.",
        "Le présent contrat est conclu entre Tekton By Bigie LLC, société à responsabilité limitée de Floride, 46 Parkside St, Freeport, FL 32439 (le « Prestataire »), et l’entreprise indiquée dans les Détails ci-dessus (le « Client »), représentée par la personne-contact qui y figure."),
    "clauses": [
        ("1. The plan", "1. Le forfait",
         ["The Provider hosts the Client’s website at the website address in the Details, keeps it online, and keeps it up to date. This includes what the plan covers, as listed in the Details. The Client pays the monthly fee shown in the Details."],
         ["Le Prestataire héberge le site web du Client à l’adresse indiquée dans les Détails, le maintient en ligne et le tient à jour. Cela comprend ce que couvre le forfait, tel qu’indiqué dans les Détails. Le Client paie la mensualité indiquée dans les Détails."]),
        ("2. Term and renewal", "2. Durée et renouvellement",
         ["The plan starts on the start date in the Details and lasts 12 months. It renews automatically for another 12 months each year unless either side cancels in writing (email is fine) at least 30 days before the end of the current term. Monthly payments stay due through the end of the term."],
         ["Le forfait commence à la date de début indiquée dans les Détails et dure 12 mois. Il est renouvelé automatiquement pour 12 mois supplémentaires chaque année, sauf si l’une des parties l’annule par écrit (un e-mail suffit) au moins 30 jours avant la fin de la période en cours. Les paiements mensuels restent dus jusqu’à la fin de la période."]),
        ("3. Payment", "3. Paiement",
         ["The monthly fee is paid one month ahead. On the 20th of each month the Provider sends an invoice for the following month. Payment is due within 10 days, which is by the end of the month in most cases. The Client pays by the payment method chosen in the Details. Invoices are issued by Tekton By Bigie LLC. If the payment method the Client chooses has a processing fee, the Client pays that fee.",
          "If an invoice is not paid by its due date, the Provider may suspend hosting and take the website offline starting on the 1st of the next month, until the account is current. There is no fee to bring it back online. Taking the website offline only pauses hosting: it does not change who owns the domain, the content or the website, and the Client may ask for a copy of the website files to host elsewhere, as described in section 5."],
         ["La mensualité est payée un mois à l’avance. Le 20 de chaque mois, le Prestataire envoie une facture pour le mois suivant. Le paiement est dû dans les 10 jours, soit à la fin du mois dans la plupart des cas. Le Client paie selon le moyen de paiement choisi dans les Détails. Les factures sont émises par Tekton By Bigie LLC. Si le moyen de paiement choisi par le Client comporte des frais de traitement, le Client les paie.",
          "Si une facture n’est pas payée à l’échéance, le Prestataire peut suspendre l’hébergement et mettre le site hors ligne à partir du 1er du mois suivant, jusqu’à régularisation du compte. La remise en ligne est gratuite. Mettre le site hors ligne ne fait que suspendre l’hébergement : cela ne change pas qui est propriétaire du domaine, du contenu ou du site, et le Client peut demander une copie des fichiers du site pour l’héberger ailleurs, comme décrit à l’article 5."]),
        ("4. What is extra", "4. Ce qui est en supplément",
         ["New pages, a redesign, printed materials such as menus, Google listing work, and other large projects are not part of the plan. The Provider gives a price first, and nothing is done or charged without the Client’s yes."],
         ["Les nouvelles pages, une refonte, les documents imprimés comme les menus, le travail sur la fiche Google et les autres projets importants ne font pas partie du forfait. Le Prestataire donne d’abord un prix, et rien n’est fait ni facturé sans l’accord du Client."]),
        ("5. What belongs to the Client", "5. Ce qui appartient au Client",
         ["The Client owns its domain name, business name, photos, text, and everything else it provides. The Provider never holds the domain. Domain and email settings change only with the Client’s approval, the Client’s email keeps working, and the Client can switch the settings back at any time.",
          "If the plan ends, the Provider gives the Client a copy of the website files on request and helps point the domain elsewhere. If the website is being paid in installments, the copy is provided after the final installment."],
         ["Le Client est propriétaire de son nom de domaine, du nom de son entreprise, de ses photos, de ses textes et de tout ce qu’il fournit. Le Prestataire ne détient jamais le domaine. Les réglages du domaine et de l’e-mail ne changent qu’avec l’accord du Client, l’e-mail du Client continue de fonctionner, et le Client peut remettre les réglages comme avant à tout moment.",
          "Si le forfait prend fin, le Prestataire remet au Client, sur demande, une copie des fichiers du site et l’aide à diriger le domaine ailleurs. Si le site est payé par mensualités, la copie est remise après la dernière mensualité."]),
        ("6. The Client’s part", "6. Le rôle du Client",
         ["The Client provides accurate content and photos it has the right to use, and answers update requests in a reasonable time."],
         ["Le Client fournit un contenu exact et des photos qu’il a le droit d’utiliser, et répond dans un délai raisonnable aux demandes de mise à jour."]),
        ("7. Limits", "7. Limites",
         ["The Provider works to keep the site online but cannot promise it will never be interrupted, because hosting is run by outside companies. The Provider is not responsible for indirect losses, and its total responsibility under this agreement is limited to the amount the Client paid in the previous 3 months."],
         ["Le Prestataire s’efforce de maintenir le site en ligne mais ne peut promettre qu’il ne sera jamais interrompu, car l’hébergement est assuré par des entreprises extérieures. Le Prestataire n’est pas responsable des pertes indirectes, et sa responsabilité totale au titre du présent contrat est limitée au montant payé par le Client au cours des 3 derniers mois."]),
        ("8. General", "8. Dispositions générales",
         ["This is the whole agreement about the plan. Changes must be in writing (email is fine). Florida law applies."],
         ["Ceci constitue l’intégralité de l’accord concernant le forfait. Toute modification doit être faite par écrit (un e-mail suffit). La loi de la Floride s’applique."]),
    ],
    "footer": ("Website Plan Agreement", "Contrat de forfait de site web"),
}
FIN = {
    "title": ("Website Financing Agreement", "Contrat de financement du site web"),
    "sub": ("Paying for the website in monthly installments", "Paiement du site en mensualités"),
    "intro": PLAN["intro"],
    "clauses": [
        ("1. The website", "1. Le site web",
         ["The Provider has built a custom website for the Client, with the number of pages shown in the Details (as shown to the Client), for the website address in the Details. The price is the price shown in the Details."],
         ["Le Prestataire a créé un site web sur mesure pour le Client, avec le nombre de pages indiqué dans les Détails (tel que présenté au Client), pour l’adresse du site indiquée dans les Détails. Le prix est celui indiqué dans les Détails."]),
        ("2. Payment plan", "2. Plan de paiement",
         ["The Client pays the price in the number of monthly payments shown in the Details, each of the installment amount shown in the Details, with no interest and no fees. Each installment is invoiced on the 20th of the month before it is due, together with any monthly plan fee, and is due within 10 days, which is by the end of the month in most cases. The first installment is invoiced on the first invoice date in the Details. The Client pays by the payment method chosen in the Details. Invoices are issued by Tekton By Bigie LLC. If the payment method the Client chooses has a processing fee, the Client pays that fee. The Client may pay the balance early at any time.",
          "These payments are separate from any monthly plan in the Website Plan Agreement. If the Details show that the Client also has a monthly plan, then for the number of months shown in the Details the Client’s monthly total is the combined monthly total shown there, and after that it is the plan fee shown there."],
         ["Le Client paie le prix en le nombre de mensualités indiqué dans les Détails, chacune du montant indiqué dans les Détails, sans intérêts ni frais. Chaque mensualité est facturée le 20 du mois qui précède son échéance, avec tout forfait mensuel, et est due dans les 10 jours, soit à la fin du mois dans la plupart des cas. La première mensualité est facturée à la date indiquée dans les Détails. Le Client paie selon le moyen de paiement choisi dans les Détails. Les factures sont émises par Tekton By Bigie LLC. Si le moyen de paiement choisi par le Client comporte des frais de traitement, le Client les paie. Le Client peut solder le reste à tout moment.",
          "Ces paiements sont distincts de tout forfait mensuel prévu au Contrat de forfait de site web. Si les Détails indiquent que le Client a aussi un forfait mensuel, alors pendant le nombre de mois indiqué dans les Détails le total mensuel du Client est le total mensuel combiné indiqué, puis il est égal au forfait mensuel indiqué."]),
        ("3. Late or missed payments", "3. Retards et paiements manqués",
         ["If an installment is not paid by its due date, the Provider may suspend hosting and take the website offline starting on the 1st of the next month, until the account is current. This only pauses hosting; it does not affect the Client’s domain or email. If the Client stops paying and does not catch up within 30 days after written notice, the Provider may end this agreement. The Client then owes the remaining balance, and the Provider keeps the payments already made."],
         ["Si une mensualité n’est pas payée à l’échéance, le Prestataire peut suspendre l’hébergement et mettre le site hors ligne à partir du 1er du mois suivant, jusqu’à régularisation du compte. Cela ne fait que suspendre l’hébergement et n’affecte ni le domaine ni l’e-mail du Client. Si le Client cesse de payer et ne rattrape pas son retard dans les 30 jours suivant un avis écrit, le Prestataire peut mettre fin au présent contrat. Le Client doit alors le solde restant, et le Prestataire conserve les paiements déjà reçus."]),
        ("4. Ownership", "4. Propriété",
         ["Until the final payment, the Provider keeps ownership of the website files, and the Client has the right to use the website while it is online. After the final payment, the website as built, including its design and the Client’s content, belongs to the Client. The Provider may keep using its own general tools and templates and may show the website in its portfolio."],
         ["Jusqu’au dernier paiement, le Prestataire reste propriétaire des fichiers du site, et le Client a le droit d’utiliser le site tant qu’il est en ligne. Après le dernier paiement, le site tel que construit, y compris sa conception et le contenu du Client, appartient au Client. Le Prestataire peut continuer à utiliser ses propres outils et modèles généraux et peut présenter le site dans son portfolio."]),
        ("5. Domain and email", "5. Domaine et e-mail",
         ["The Client’s domain name and email stay the Client’s. The Provider never holds them."],
         ["Le nom de domaine et l’e-mail du Client restent la propriété du Client. Le Prestataire ne les détient jamais."]),
        ("6. General", "6. Dispositions générales",
         ["This is the whole agreement about the financing. Changes must be in writing (email is fine). Florida law applies."],
         ["Ceci constitue l’intégralité de l’accord concernant le financement. Toute modification doit être faite par écrit (un e-mail suffit). La loi de la Floride s’applique."]),
    ],
    "footer": ("Website Financing Agreement", "Contrat de financement du site web"),
}
ENGLISH_CONTROLS = ("If the English and French versions differ, the English version controls.",
                    "En cas de différence entre les versions anglaise et française, la version anglaise prévaut.")
DETAILS_HEAD = ("Details", "Détails")
LABELS = {   # key -> (EN, FR)
    "business": ("Client business name", "Nom commercial du Client"),
    "legal": ("Client legal name, if different", "Nom légal du Client, s’il est différent"),
    "contact": ("Contact person (signs for the Client), full name", "Personne-contact (signe pour le Client), nom complet"),
    "email": ("Client email", "E-mail du Client"),
    "website": ("Website address", "Adresse du site web"),
    "covers": ("What the monthly plan covers", "Ce que couvre le forfait mensuel"),
    "fee": ("Monthly fee (US$)", "Mensualité du forfait (en $ US)"),
    "start": ("Plan start date", "Date de début du forfait"),
    "pay": ("How the Client pays", "Moyen de paiement du Client"),
    "pages": ("Number of pages", "Nombre de pages"),
    "price": ("Website price (US$)", "Prix du site (en $ US)"),
    "n_pay": ("Number of monthly payments", "Nombre de mensualités"),
    "inst": ("Amount of each payment (US$)", "Montant de chaque mensualité (en $ US)"),
    "first": ("First invoice date", "Date de la première facture"),
    "has_plan": ("Does the Client also have the monthly plan?", "Le Client a-t-il aussi le forfait mensuel ?"),
    "plan_months": ("If yes: number of months at the combined total", "Si oui : nombre de mois au total combiné"),
    "plan_total": ("Combined monthly total for those months (US$)", "Total mensuel combiné pour ces mois (en $ US)"),
    "plan_after": ("Monthly plan fee after that (US$)", "Forfait mensuel ensuite (en $ US)"),
}
PAY_OPTS = [("cash", "Cash", "Espèces"), ("check", "Check", "Chèque"), ("ach", "Bank transfer (ACH)", "Virement bancaire (ACH)"), ("card", "Card", "Carte")]
SIG = {"signature": ("Signature", "Signature"), "name": ("Name", "Nom"), "title": ("Title", "Titre"), "date": ("Date", "Date"),
       "by": ("By:", "Par :"), "client": ("Client", "Client"),
       "prov_line": ("TEKTON BY BIGIE LLC, a Florida limited liability company", "TEKTON BY BIGIE LLC, société à responsabilité limitée de Floride"),
       "prov_by": ("By: BKE Holdings Group, Inc., its Authorized Member", "Par : BKE Holdings Group, Inc., son membre autorisé"),
       "howto": ("To sign: type your full name in the Signature box, or draw it with Preview (Markup) or Adobe Fill & Sign. Both parties sign and date.",
                 "Pour signer : tapez votre nom complet dans la case Signature, ou dessinez-le avec Aperçu (Annotation) ou Adobe Fill & Sign. Les deux parties signent et datent.")}
OTHER = ("Other", "Autre")

CSS = """
@page { size: Letter; margin: 0.7in 0.75in 0.8in 0.75in;
  @bottom-center { content: "Tekton By Bigie LLC  ·  FOOTER  ·  Page " counter(page) " of " counter(pages); font: 8pt Helvetica, Arial, sans-serif; color: #666; } }
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10pt; line-height: 1.38; color: #111; margin: 0; }
.brand { font: 700 8.5pt Helvetica, Arial, sans-serif; letter-spacing: .16em; text-transform: uppercase; color: #082868; margin-bottom: 10px; border-bottom: 2px solid #f09018; padding-bottom: 6px; }
h1 { font: 700 20pt Georgia, serif; color: #082868; margin: 0 0 2px; }
.sub { font-style: italic; color: #444; margin: 0 0 12px; font-size: 11pt; }
h2 { font: 700 10.5pt Georgia, serif; margin: 12px 0 3px; color: #082868; break-after: avoid; }
p { margin: 0 0 6px; break-inside: avoid; }
.details { border: 1.5px solid #082868; border-radius: 6px; padding: 10px 12px 8px; margin: 10px 0 12px; break-inside: avoid; }
.details h3 { font: 700 9pt Helvetica, Arial, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #082868; margin: 0 0 6px; }
.details table { width: 100%; border-collapse: collapse; }
.details td { vertical-align: middle; padding: 3.5px 0; }
.details td.l { width: 2.55in; font: 600 8.6pt Helvetica, Arial, sans-serif; color: #222; padding-right: 8px; line-height: 1.2; }
.details td.l span.fr { display: block; font-weight: 400; color: #555; font-style: italic; }
.fld { border-bottom: 1px solid #8a7a00; }
.cbx { display: inline-block; width: 0.16in; height: 0.16in; border: 1px solid #333; vertical-align: -0.03in; margin: 0 4px 0 0; }
.opts { font: 8.6pt Helvetica, Arial, sans-serif; }
.opts span.o { margin-right: 12px; white-space: nowrap; }
.opts .fr { color: #555; font-style: italic; }
table.bi { width: 100%; border-collapse: collapse; }
table.bi td { width: 50%; vertical-align: top; padding: 0 10px 0 0; }
table.bi td + td { padding: 0 0 0 10px; border-left: 1px solid #ccc; }
table.bi tr { break-inside: avoid; }
table.bi td.fr, .fr-text { color: #1a1a1a; }
.sig { break-inside: avoid; margin-top: 14px; }
.sig .party { font: 700 9.5pt Georgia, serif; margin: 8px 0 2px; }
.sigtable { width: 100%; border-collapse: collapse; margin: 2px 0 6px; }
.sigtable td { padding: 4px 8px 4px 0; vertical-align: bottom; font: 8.6pt Helvetica, Arial, sans-serif; }
.sigtable td.k { white-space: nowrap; width: 1%; font-weight: 600; }
.howto { font: italic 8.3pt Helvetica, Arial, sans-serif; color: #555; margin-top: 4px; }
"""

def build_html(doc, bilingual):
    F = Fields()
    t = doc
    hd = DETAILS_HEAD
    def lab(key):
        en, fr = LABELS[key]
        return f'<td class="l">{e(en)}' + (f'<span class="fr">{e(fr)}</span>' if bilingual else "") + "</td>"
    def row(key, fieldhtml):
        return f"<tr>{lab(key)}<td>{fieldhtml}</td></tr>"
    def pay_row():
        opts = "".join(f'<span class="o">{F.check("pay_" + k)}{e(en)}' + (f' <span class="fr">/ {e(fr)}</span>' if bilingual else "") + "</span>" for k, en, fr in PAY_OPTS)
        opts += f'<span class="o">{F.check("pay_other")}{e(OTHER[0])}{(" <span class=fr>/ " + e(OTHER[1]) + "</span>") if bilingual else ""}: {F.text("pay_other_text", width="1.3in", height="0.22in")}</span>'
        return row("pay", f'<div class="opts">{opts}</div>')
    is_plan = t is PLAN
    rows = [row("business", F.text("business", "4.1in")), row("legal", F.text("legal", "4.1in")),
            row("contact", F.text("contact", "4.1in")), row("email", F.text("email", "4.1in")),
            row("website", F.text("website", "4.1in"))]
    if is_plan:
        rows += [row("covers", F.text("covers", "4.1in", "0.62in", multiline=True)), row("fee", F.text("fee", "1.5in")),
                 row("start", F.text("start", "1.7in")), pay_row()]
    else:
        rows += [row("pages", F.text("pages", "1.0in")), row("price", F.text("price", "1.5in")), row("n_pay", F.text("n_pay", "1.0in")),
                 row("inst", F.text("inst", "1.5in")), row("first", F.text("first", "1.7in")), pay_row()]
        yn = f'<div class="opts"><span class="o">{F.check("plan_yes")}Yes' + (' <span class="fr">/ Oui</span>' if bilingual else "") + f'</span><span class="o">{F.check("plan_no")}No' + (' <span class="fr">/ Non</span>' if bilingual else "") + "</span></div>"
        rows += [row("has_plan", yn), row("plan_months", F.text("plan_months", "1.0in")), row("plan_total", F.text("plan_total", "1.5in")),
                 row("plan_after", F.text("plan_after", "1.5in"))]
    head = f'{e(hd[0])}' + (f' <span style="font-weight:400;letter-spacing:0;text-transform:none;color:#555"> / {e(hd[1])}</span>' if bilingual else "")
    details = f'<div class="details"><h3>{head}</h3><table>{"".join(rows)}</table></div>'

    # body
    if bilingual:
        title = f'<h1>{e(t["title"][0])}</h1><div class="sub">{e(t["sub"][0])}</div>'
        title_fr = f'<h1>{e(t["title"][1])}</h1><div class="sub">{e(t["sub"][1])}</div>'
        body = f'<table class="bi"><tr><td>{title}</td><td class="fr">{title_fr}</td></tr><tr><td><p>{e(t["intro"][0])}</p></td><td class="fr"><p>{e(t["intro"][1])}</p></td></tr></table>'
        body += details
        body += '<table class="bi">'
        for i, (hen, hfr, pen, pfr) in enumerate(t["clauses"]):
            last = i == len(t["clauses"]) - 1
            en_ps = "".join(f"<p>{e(x)}</p>" for x in pen) + (f"<p>{e(ENGLISH_CONTROLS[0])}</p>" if last else "")
            fr_ps = "".join(f"<p>{e(x)}</p>" for x in pfr) + (f"<p>{e(ENGLISH_CONTROLS[1])}</p>" if last else "")
            body += f'<tr><td><h2>{e(hen)}</h2>{en_ps}</td><td class="fr"><h2>{e(hfr)}</h2>{fr_ps}</td></tr>'
        body += "</table>"
    else:
        body = f'<h1>{e(t["title"][0])}</h1><div class="sub">{e(t["sub"][0])}</div><p>{e(t["intro"][0])}</p>' + details
        for hen, hfr, pen, pfr in t["clauses"]:
            body += f"<h2>{e(hen)}</h2>" + "".join(f"<p>{e(x)}</p>" for x in pen)

    # signatures (the Client's business name and contact name are the SAME fields as in the Details, so they fill in automatically)
    def s(key): return e(SIG[key][0]) + (f' <span style="font-weight:400;color:#555;font-style:italic">/ {e(SIG[key][1])}</span>' if bilingual else "")
    sig = f'<div class="sig"><h2>{"Signatures" if not bilingual else "Signatures"}</h2>'
    sig += f'<div class="party">{e(SIG["prov_line"][0])}' + (f'<br><span style="font-weight:400;font-style:italic;color:#555">{e(SIG["prov_line"][1])}</span>' if bilingual else "") + "</div>"
    sig += f'<p style="margin:0 0 2px">{e(SIG["prov_by"][0])}' + (f'<br><span class="fr-text" style="font-style:italic;color:#555">{e(SIG["prov_by"][1])}</span>' if bilingual else "") + "</p>"
    sig += f'<table class="sigtable"><tr><td class="k">{s("signature")}</td><td>{F.text("prov_sign", "2.3in")}</td><td class="k">{s("name")}</td><td>Brandon Edwards</td><td class="k">{s("title")}</td><td>President</td><td class="k">{s("date")}</td><td>{F.text("prov_date", "1.0in")}</td></tr></table>'
    sig += f'<div class="party">{s("client")}: {F.text("business", "3.6in")}</div>'
    sig += f'<table class="sigtable"><tr><td class="k">{s("signature")}</td><td>{F.text("client_sign", "2.3in")}</td><td class="k">{s("name")}</td><td>{F.text("contact", "1.7in")}</td><td class="k">{s("title")}</td><td>{F.text("client_title", "1.0in")}</td><td class="k">{s("date")}</td><td>{F.text("client_date", "1.0in")}</td></tr></table>'
    howto = SIG["howto"][0] + ((" / " + SIG["howto"][1]) if bilingual else "")
    sig += f'<div class="howto">{e(howto)}</div></div>'
    body += sig

    foot = t["footer"][0] + ((" / " + t["footer"][1]) if bilingual else "")
    css = CSS.replace("FOOTER", foot.replace('"', "'"))
    page = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(t["title"][0])}</title><style>{css}</style></head><body><div class="brand">Tekton by Bigie</div>{body}</body></html>'
    return page, F

def chrome_pdf(html_text, pdf_path):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_text); path = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", f"file://{path}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    os.unlink(path)

def locate(pdf_path, F):
    """Find each colored box in the PDF (page index + rectangle in points, origin top-left)."""
    d = fitz.open(pdf_path)
    found = {}
    for pno, page in enumerate(d):
        for dr in page.get_drawings():
            fill = dr.get("fill")
            if not fill: continue
            for i, (name, kind, ml) in enumerate(F.items):
                r, g, b = F._color(i, kind)
                if abs(fill[0] - r / 255) < .006 and abs(fill[1] - g / 255) < .006 and abs(fill[2] - b / 255) < .006:
                    rc = dr["rect"]
                    found.setdefault(i, []).append({"page": pno, "x0": rc.x0, "y0": rc.y0, "x1": rc.x1, "y1": rc.y1, "ph": page.rect.height})
    missing = [F.items[i][0] for i in range(len(F.items)) if i not in found]
    if missing: raise SystemExit(f"boxes not found in PDF: {missing}")
    fields = []
    for i, (name, kind, ml) in enumerate(F.items):
        boxes = found[i]
        bx = max(boxes, key=lambda b: (b["x1"] - b["x0"]) * (b["y1"] - b["y0"]))   # the fill rectangle itself
        fields.append({"name": name, "kind": kind, "multiline": ml, "page": bx["page"], "x": bx["x0"], "y": bx["ph"] - bx["y1"], "w": bx["x1"] - bx["x0"], "h": bx["y1"] - bx["y0"]})
    return fields

VARIANTS = [
    (PLAN, False, "Website Plan Agreement - FILLABLE"),
    (FIN, False, "Website Financing Agreement - FILLABLE"),
    (PLAN, True, "Website Plan Agreement - FILLABLE (English and Français)"),
    (FIN, True, "Website Financing Agreement - FILLABLE (English and Français)"),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for doc, bi, name in VARIANTS:
        if only and not any(o.lower() in name.lower() for o in only): continue
        html_text, F = build_html(doc, bi)
        base = os.path.join(OUT, "_base.pdf")
        chrome_pdf(html_text, base)
        fields = locate(base, F)
        spec = os.path.join(OUT, "_fields.json")
        json.dump({"in": base, "out": os.path.join(OUT, name + ".pdf"), "title": doc["title"][0] + (" / " + doc["title"][1] if bi else ""), "fields": fields}, open(spec, "w"))
        subprocess.run(["node", os.path.join(HERE, "add_fields.mjs"), spec], check=True)
        print("built", name + ".pdf", "-", len(F.items), "boxes,", len({f["name"] for f in fields}), "fields,", len(fitz.open(base)), "pages")
    for f in ("_base.pdf", "_fields.json"):
        try: os.unlink(os.path.join(OUT, f))
        except FileNotFoundError: pass
