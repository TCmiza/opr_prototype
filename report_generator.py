
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor

def _scale_image(path, max_w, max_h):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    scale = min(max_w / iw, max_h / ih)
    return img, iw*scale, ih*scale

def draw_wrapped_paragraph(c, text, x, y, max_width, leading=14, font_name="Helvetica", font_size=11):
    # Use Platypus Paragraph for clean wrapping and bullet support
    style = ParagraphStyle(
        "body",
        fontName=font_name,
        fontSize=font_size,
        leading=leading,
        textColor=HexColor("#222222"),
        alignment=TA_LEFT,
    )
    p = Paragraph(text.replace("\n", "<br/>"), style)
    w, h = p.wrap(max_width, 1000*cm)
    p.drawOn(c, x, y - h)
    return h

def generate_pdf(buffer, data):
    # Page setup
    PAGE_W, PAGE_H = A4
    MARGIN_L = 2.0*cm
    MARGIN_R = 2.0*cm
    CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle("One Page Report")

    # Header bar
    c.setFillColor(HexColor("#0B5ED7"))
    c.rect(0, PAGE_H-2.0*cm, PAGE_W, 2.0*cm, stroke=0, fill=1)

    # Logo (left) if provided
    y_header_mid = PAGE_H-1.0*cm
    x_logo = MARGIN_L
    if data.get("logo_path"):
        try:
            img, w, h = _scale_image(data["logo_path"], 2.0*cm, 1.6*cm)
            c.drawImage(img, x_logo, PAGE_H-1.8*cm + (1.8*cm-h)/2, width=w, height=h, mask='auto')
        except Exception:
            pass

    # Title
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN_L + 2.3*cm, PAGE_H-1.15*cm, "ONE PAGE REPORT (OPR)")

    # Subheader line
    c.setFillColor(HexColor("#0B5ED7"))
    c.rect(0, PAGE_H-2.05*cm, PAGE_W, 0.05*cm, stroke=0, fill=1)

    # Body
    c.setFillColor(HexColor("#111111"))
    y = PAGE_H - 2.6*cm

    # Key info grid (left/right columns)
    left_x = MARGIN_L
    right_x = PAGE_W/2 + 0.3*cm
    line_h = 14

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tajuk Program:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("title","-"))
    y -= line_h

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tarikh / Masa:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, f'{data.get("date","-")} / {data.get("time","-")}')
    y -= line_h

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tempat:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("venue","-"))
    y -= line_h

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Anjuran:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("organiser","-"))
    y -= line_h

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, PAGE_H - 2.6*cm, "Sasaran / Peserta:")
    c.setFont("Helvetica", 11)
    c.drawString(right_x + 3.6*cm, PAGE_H - 2.6*cm, data.get("target","-"))

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, PAGE_H - 2.6*cm - line_h, "Bil. Kehadiran:")
    c.setFont("Helvetica", 11)
    att = data.get("attendance", {})
    att_str = f"Murid {att.get('students','-')}, Guru {att.get('teachers','-')}, Ibu Bapa {att.get('parents','-')}"
    c.drawString(right_x + 3.6*cm, PAGE_H - 2.6*cm - line_h, att_str)

    # Section blocks
    y -= 10
    sect_gap = 6
    label_font = "Helvetica-Bold"
    body_font = "Helvetica"

    def section(label, text):
        nonlocal y
        c.setFont(label_font, 11)
        c.setFillColor(HexColor("#0B5ED7"))
        c.drawString(left_x, y, label)
        y -= 10
        c.setFillColor(HexColor("#222222"))
        h = draw_wrapped_paragraph(c, text or "-", left_x, y, CONTENT_W)
        y -= (h + sect_gap)

    section("Objektif Program", data.get("objectives",""))
    section("Ringkasan Aktiviti / Atur Cara", data.get("activities",""))
    section("Pencapaian / Impak", data.get("outcomes",""))
    section("Cadangan / Penambahbaikan", data.get("recommendations",""))

    # Images row (up to 3)
    imgs = data.get("image_paths", [])[:3]
    if imgs:
        c.setFillColor(HexColor("#0B5ED7"))
        c.setFont(label_font, 11)
        c.drawString(left_x, y, "Gambar Program")
        y -= 12

        gap = 0.5*cm
        each_w = (CONTENT_W - 2*gap) / 3.0 if len(imgs) >= 3 else (CONTENT_W - gap) / 2.0 if len(imgs)==2 else CONTENT_W
        x = MARGIN_L
        max_h = 5.0*cm
        for p in imgs:
            try:
                img, w, h = _scale_image(p, each_w, max_h)
                c.drawImage(img, x, y - h, width=w, height=h, mask='auto')
                x += each_w + gap
            except Exception:
                pass
        y -= (max_h + 6)

    # Footer - prepared by
    c.setStrokeColor(HexColor("#DDDDDD"))
    c.line(MARGIN_L, 2.5*cm, PAGE_W - MARGIN_R, 2.5*cm)
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#555555"))
    c.drawString(MARGIN_L, 2.1*cm, f'Disediakan oleh: {data.get("prepared_by","-")} ({data.get("position","-")})')
    c.drawString(MARGIN_L, 1.6*cm, f'Tarikh Laporan: {data.get("report_date","-")}')
    c.drawRightString(PAGE_W - MARGIN_R, 1.6*cm, "Dijana automatik oleh Sistem OPR")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
