
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
  
