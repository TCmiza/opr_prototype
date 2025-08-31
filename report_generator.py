from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


def generate_report(program_title, date, venue, participants, attendance, objectives, activities, outcome, photo_path, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Tajuk Program (boleh wrap)
    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=14
    )
    elements.append(Paragraph(program_title, title_style))
    elements.append(Spacer(1, 12))

    # Maklumat Asas Program
    info_data = [
        ["Tarikh", date],
        ["Tempat", venue],
    ]
    info_table = Table(info_data, colWidths=[120, 300])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 12))

    # Sasaran/Peserta & Kehadiran (semua di kiri)
    data = [
        ["Sasaran/Peserta:", participants],
        ["Bil. Kehadiran:", attendance]
    ]
    table = Table(data, colWidths=[120, 300])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Objektif Program
    elements.append(Paragraph("<b>Objektif Program:</b>", styles['Heading3']))
    elements.append(Paragraph(objectives, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Aktiviti Program
    elements.append(Paragraph("<b>Aktiviti Program:</b>", styles['Heading3']))
    elements.append(Paragraph(activities, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Hasil Dicapai
    elements.append(Paragraph("<b>Hasil Program:</b>", styles['Heading3']))
    elements.append(Paragraph(outcome, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Gambar
    if photo_path:
        try:
            img = Image(photo_path, width=5*inch, height=3*inch)
            elements.append(img)
        except Exception as e:
            elements.append(Paragraph("Tidak dapat memaparkan gambar.", styles['Normal']))

    doc.build(elements)
