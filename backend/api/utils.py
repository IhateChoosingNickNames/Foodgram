import io

from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def draw_headers_and_footers(object, x_size, y_size, text, header=True):
    line_y_cor = 778
    line_y_cor_next = 780

    if not header:
        line_y_cor = 23
        line_y_cor_next = 25

    object.drawString(x_size, y_size, text)
    object.line(0, line_y_cor, 1000, line_y_cor)
    object.line(0, line_y_cor_next, 1000, line_y_cor_next)


def pdf_response_creator(data):
    """Создание ответа в виде ПДФ-файла."""

    buffer = io.BytesIO()
    pdf_object = canvas.Canvas(buffer, pagesize=A4)
    pdf_object.setFont("Helvetica", 15, leading=None)

    draw_headers_and_footers(
        pdf_object, 250, 800, _("Ваша продуктовая корзина:")
    )

    y_coord = 750
    page = 1

    pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))
    pdf_object.setFont("Verdana", 10, leading=None)

    for ingr_name, ingr_data in sorted(data.items()):

        pdf_object.drawString(100, y_coord, f"{ingr_name}:")

        if ingr_data["measurement_unit"] == "по вкусу":
            to_draw = f"{ingr_data['measurement_unit']}"
        else:
            to_draw = (
                f"{ingr_data['amount']} ({ingr_data['measurement_unit']})"
            )

        pdf_object.drawString(450, y_coord, to_draw)
        y_coord -= 40
        if y_coord < 60:
            draw_headers_and_footers(
                pdf_object, 500, 10, f"Page {page}", header=False
            )
            pdf_object.showPage()
            y_coord = 750
            page += 1

    draw_headers_and_footers(
        pdf_object, 250, 10, _("Спасибо, что выбрали наш сервис"), header=False
    )

    pdf_object.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename="shopping_card.pdf"
    )
