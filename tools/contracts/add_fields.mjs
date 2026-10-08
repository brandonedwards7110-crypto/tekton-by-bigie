// Adds real PDF form fields on top of the boxes found by make_fillable.py. Boxes with the same name share ONE field
// (type the client's business name once and it also appears in the signature block).
import { PDFDocument, StandardFonts, rgb } from "pdf-lib";
import fs from "node:fs";

const spec = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const pdf = await PDFDocument.load(fs.readFileSync(spec.in));
const form = pdf.getForm();
const font = await pdf.embedFont(StandardFonts.Helvetica);
const pages = pdf.getPages();
const made = new Map();

for (const f of spec.fields) {
  const page = pages[f.page];
  if (f.kind === "check") {
    const cb = form.createCheckBox(f.name);
    cb.addToPage(page, { x: f.x, y: f.y, width: f.w, height: f.h, borderColor: rgb(0.2, 0.2, 0.2), borderWidth: 1, backgroundColor: rgb(1, 1, 1) });
    continue;
  }
  let tf = made.get(f.name);
  const first = !tf;
  if (first) {
    tf = form.createTextField(f.name);
    if (f.multiline) { tf.enableMultiline(); }
    made.set(f.name, tf);
  }
  tf.addToPage(page, {
    x: f.x, y: f.y, width: f.w, height: f.h, font,
    textColor: rgb(0.05, 0.1, 0.3), backgroundColor: rgb(1, 0.957, 0.6), borderWidth: 0,
  });
  if (first) tf.setFontSize(f.multiline ? 9.5 : 10);
}

pdf.setTitle(spec.title);
pdf.setAuthor("Tekton By Bigie LLC");
pdf.setSubject("Fillable contract. Type in the yellow fields, then sign.");
form.updateFieldAppearances(font);
fs.writeFileSync(spec.out, await pdf.save());
