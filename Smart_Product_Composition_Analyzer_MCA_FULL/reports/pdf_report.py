from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

def build_report(product, values, ingredients, score, category, factors, created_at):
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=16*mm, leftMargin=16*mm,
                            topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11))
    story = [
        Paragraph("SMART PRODUCT COMPOSITION ANALYZER", styles["Title"]),
        Paragraph("MCSP-232 • MCA Project", styles["Heading2"]),
        Spacer(1, 5*mm),
        Paragraph(f"<b>Product:</b> {product['name']} &nbsp;&nbsp; <b>Brand:</b> {product.get('brand') or '-'}", styles["BodyText"]),
        Paragraph(f"<b>Category:</b> {product['category']} &nbsp;&nbsp; <b>Analysis date:</b> {created_at}", styles["BodyText"]),
        Spacer(1, 4*mm),
        Paragraph(f"<b>Composition Index:</b> {score}/100 &nbsp;&nbsp; <b>Assessment:</b> {category}", styles["Heading2"]),
        Paragraph("Informational academic index; not a medical diagnosis, regulatory certification, or individualized dietary recommendation.", styles["Small"]),
        Spacer(1, 5*mm),
        Paragraph("Nutrition Values", styles["Heading2"])
    ]
    nutrient_rows = [["Field","Value"]]
    for k,v in values.items():
        nutrient_rows.append([k.replace("_"," ").title(), str(v) if v is not None else "Missing"])
    t = Table(nutrient_rows, colWidths=[70*mm, 60*mm])
    t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.4,colors.grey),
                           ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#183B56")),
                           ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                           ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")]))
    story += [t, Spacer(1,5*mm), Paragraph("Ingredient Detection", styles["Heading2"])]
    ing_rows = [["Ingredient","Category","Flag"]]
    for x in ingredients:
        ing_rows.append([x["ingredient_name"], x["ingredient_category"], x["risk_flag"]])
    if len(ing_rows) == 1:
        ing_rows.append(["No ingredient records", "-", "-"])
    it = Table(ing_rows, colWidths=[80*mm,55*mm,35*mm])
    it.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.4,colors.grey),
                            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2E7D32")),
                            ("TEXTCOLOR",(0,0),(-1,0),colors.white)]))
    story += [it, Spacer(1,5*mm), Paragraph("Contributing Factors", styles["Heading2"])]
    fac_rows = [["Factor","Value","Contribution"]]
    for f in factors:
        fac_rows.append([f["name"], str(f.get("value") or "-"), str(f["contribution"])])
    if len(fac_rows) == 1:
        fac_rows.append(["No rule factor triggered","-","0"])
    ft = Table(fac_rows, colWidths=[95*mm,35*mm,35*mm])
    ft.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.4,colors.grey),
                            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#6A1B9A")),
                            ("TEXTCOLOR",(0,0),(-1,0),colors.white)]))
    story += [ft, Spacer(1,6*mm),
              Paragraph("Method: Score = clamp(50 + sum of triggered rule weights, 0, 100). "
                        "Positive weights increase the index and negative weights decrease it. "
                        "Thresholds and weights are configurable knowledge-base values.", styles["Small"])]
    doc.build(story)
    out.seek(0)
    return out.getvalue()
