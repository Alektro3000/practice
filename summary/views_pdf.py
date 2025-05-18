import csv
import time
import io
import os
from django.core.files.base import ContentFile
from django.http import FileResponse

from summary.serializers import *
from summary.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.conf import settings

def CreatePDF(data):
        pdfmetrics.registerFont(TTFont('TimesNewRoman', os.path.join(settings.BASE_DIR, 'summary', 'static',  'fonts',  'DejaVuSans.ttf')))
        # Create PDF document
        buffer = io.BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=letter)

        # Create the table
        table = Table(data)

        # Add style to the table
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'TimesNewRoman'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(style)
        # Build the PDF
        document.build([table])
        buffer.seek(0)
        return buffer.getvalue()
    


class CreateProductSummaryPDFView(APIView):
    def post(self, request):


        # Table data (list of lists)
        header = [
            ['Название товара', 'Категория', 'Chárlie雷'],
        ]
        data = [ [product.product_name, product.category, product.current_quantity] for product in ProductSummary.objects.all()]

        # Build the PDF
        pdf = CreatePDF(header + data)

        summary = SummaryFile(name = "RunOut" + str(time.time()) + ".pdf")
        summary.file.save( "RunOut" + str(time.time()) + ".pdf", ContentFile(pdf))
        summary.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
