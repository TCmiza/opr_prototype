from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import io

# Fungsi helper untuk bungkus teks panjang
def draw_wrapped_paragraph(c, text, x, y, max_width, leading=14, font_name="Helvetica", font_size=11):
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = font_name
    style.fontSize = font_size
    style.leading = leading

    p = Paragraph(text, style)
    w, h = p.wrap(max_width, 1000)  # wrap ikut lebar
    p.drawOn(c, x, y - h)
    return h

def generate_report(data, logo_path=None, images=[]):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Header bar biru ---
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.rect(0, height-50, width, 50, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-35, "LAPORAN RINGKAS PROGRAM")

    # --- Logo (jika ada) ---
    if logo_path:
        try:
            c.drawImage(logo_path, 30, height-80, width=60, height=60, preserveAspectRatio=True, mask="auto")
        except:
            pass

    # --- Kedudukan content ---
    left_x = 2*cm
    right_x = width/2 + 1*cm
    y = height - 100
    line_h = 16
    CONTENT_W = width - 4*cm  # guna untuk wrap text

    # ======================
    # Kolum kiri
    # ======================
    # Tajuk Program (wrap)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tajuk Program:")
    c.setFont("Helvetica", 11)
    title_text = data.get("title", "-")
    max_w_title = CONTENT_W/2.0 - 3.3*cm
    h_title = draw_wrapped_paragraph(
        c, title_text, left_x + 3.3*cm, y, max_w_title,
        leading=13, font_name="Helvetica", font_size=11
    )
    y -= (h_title + 4)

    # Tarikh/Masa
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tarikh / Masa:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("date_time", "-"))
    y -= line_h

    # Tempat
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Tempat:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("place", "-"))
    y -= line_h

    # Penganjur
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "Penganjur:")
    c.setFont("Helvetica", 11)
    c.drawString(left_x + 3.3*cm, y, data.get("organizer", "-"))
    y -= line_h

    # ======================
    # Kolum kanan
    # ======================
    y2 = height - 100

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, y2, "Sasaran / Peserta:")
    c.setFont("Helvetica", 11)
    c.drawString(right_x + 4*cm, y2, data.get("audience", "-"))
    y2 -= line_h

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, y2, "Bilangan Kehadiran:")
    c.setFont("Helvetica", 11)
    c.drawString(right_x + 4*cm, y2, data.get("attendance", "-"))
    y2 -= line_h

    # ======================
    # Bahagian panjang (objektif, aktiviti, impak, cadangan)
    # ======================
    y3 = min(y, y2) - 10
    sections = [
        ("Objektif Program", data.get("objective","-")),
        ("Aktiviti Program", data.get("activities","-")),
        ("Impak Program", data.get("impact","-")),
        ("Cadangan Penambahbaikan", data.get("suggestion","-")),
    ]

    for title, content in sections:
        if y3 < 150:  # kalau nak habis page
            c.showPage()
            y3 = height - 80

        c.setFillColor(colors.HexColor("#3366cc"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_x, y3, title)
        c.setFillColor(colors.black)
        y3 -= 14

        h = draw_wrapped_paragraph(c, content, left_x, y3, width-4*cm, leading=14)
        y3 -= (h + 8)

    # ======================
    # Gambar (jika ada)
    # ======================
    if images:
        y_img = y3 - 20
        img_w = (width - 4*cm) / 3
        img_h = 5*cm
        x_img = left_x
        for img in images[:3]:
            try:
                c.drawImage(img, x_img, y_img, width=img_w, height=img_h, preserveAspectRatio=True, mask="auto")
                x_img += img_w + 0.5*cm
            except:
                pass

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
