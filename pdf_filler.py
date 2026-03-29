import io
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from COORD_MAP import COORD_MAP

try:
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    FONT_NAME = 'Arial'
except Exception:
    FONT_NAME = 'Helvetica'

def fill_sti_163(user_data, template_path="template_sti_163.pdf"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, template_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Шаблон не найден: {full_path}")

    existing_pdf = PdfReader(open(full_path, "rb"))
    output = PdfWriter()

    # Создаём слой для наложения текста
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont(FONT_NAME, 10)

    # Проходим по всем полям из COORD_MAP
    for field, (x, y, page) in COORD_MAP.items():
        # Если поле предназначено для страницы 0 (первая страница)
        if page == 0:
            if field in user_data and user_data[field]:
                can.drawString(x, y, str(user_data[field]))
            # Галочка для регистрации ИП
            if field == "check_ip" and user_data.get("is_ip", False):
                can.drawString(x, y, "X")

    can.save()
    packet.seek(0)

    # Накладываем текст на первую страницу
    overlay_pdf = PdfReader(packet)
    page = existing_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    output.add_page(page)

    # Копируем остальные страницы без изменений
    for i in range(1, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[i])

    final_buffer = io.BytesIO()
    output.write(final_buffer)
    final_buffer.seek(0)
    return final_buffer