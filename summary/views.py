import csv
import time
import io
from django.core.files.base import ContentFile
from django.http import FileResponse

from summary.serializers import *
from summary.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

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
        pdfmetrics.registerFont(TTFont('TimesNewRoman', os.path.join(settings.BASE_DIR, 'summary', 'static',  'fonts',  'times.ttf')))
        # Create PDF document
        buffer = io.BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=letter)

        # Create the table
        table = Table(data)

        # Add style to the table
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'TimesNewRoman'),
            ('FONTSIZE', (0,0), (-1,0), 16),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(style)
        # Build the PDF
        document.build([table])
        buffer.seek(0)
        return buffer.getvalue()

def CreateCSV(data):
    output = io.StringIO()
    writer = csv.writer(output)

    for row in data:
        writer.writerow(row)
        
    csv_content = output.getvalue()
    output.close()
    return csv_content.encode("utf-8-sig")
    

def CreateFile(data, format: str):
    if(format == "pdf"):
    # Build the PDF
        return CreatePDF(data)
    elif(format == "csv"):
     # Build the CSV
        return CreateCSV(data)
    
def SaveFile(file, type: str, format: str):
    summary = SummaryFile(name = type + str(time.time()) + "." + format, type = type, format = format)
    summary.file.save(type + str(time.time()) + "." + format, ContentFile(file))
    summary.save()



class CreateProductSummaryView(APIView):
    def post(self, request, format):
        # Table data (list of lists)
        header = [
            ['Название товара', 'Категория', 'Остаток'],
        ]
        data = [ [product.product_name, product.category, product.current_quantity] for product in ProductSummary.objects.all()]
        footer = ["", "", "Итого: "+str(sum(data[::,2:2]))]
        file = CreateFile(header + data + footer, format)
        SaveFile(file, "Product", format)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateRunOutSummaryView(APIView):
    def post(self, request, format):


        # Table data (list of lists)
        header = [
            ['Название товара', 'Категория', 'Нехватка'],
        ]
        data = [ [product.product_name, product.category, product.stock_difference] \
                for product in ProductRunOutSummary.objects.all()]

        file = CreateFile(header + data, format)
        SaveFile(file, "RunOut", format)

        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateMovementSummaryView(APIView):
    def post(self, request, format):


        # Table data (list of lists)
        header = [
            ['Тип операции', 'Дата'],
        ]
        movements = MovementSummary.objects.all()

        min_date = request.query_params.get('min_date') 
        if min_date:
            movements = movements.filter(min_date__gte=min_date)
        
        max_date = request.query_params.get('max_date')
        if max_date:
            movements = movements.filter(max_date__lte=max_date)


        data = [ [product.product_name, product.category, product.stock_difference] \
                for product in movements]

        file = CreateFile(header + data, format)
        SaveFile(file, "Movement", format)

        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateMovementFullSummaryView(APIView):
    def post(self, request, format):


        # Table data (list of lists)
        header = [
            ['Тип операции', 'Изменение товара',  'Дата', 'Текущий остаток '],
        ]
        movements = ProductMovementSummary.objects.all()

        min_date = request.query_params.get('min_date') 
        if min_date:
            movements = movements.filter(min_date__gte=min_date)
        
        max_date = request.query_params.get('max_date')
        if max_date:
            movements = movements.filter(max_date__lte=max_date)

        product = request.query_params.get('product')
        if product:
            movements = movements.filter(product_id=product)


        data = [ [product.product_name, product.category, product.stock_difference] \
                for product in movements]
        

        file = CreateFile(header + data, format)
        SaveFile(file, "ProductMovement", format)

        return Response(status=status.HTTP_204_NO_CONTENT)


    
class SummaryLoadView(APIView):
    def get(self, request, id):
        file_instance = SummaryFile.objects.get(id=id)
        return FileResponse(file_instance.file.open(), as_attachment=True, filename=file_instance.name)
    
    
class SummaryListView(APIView):
    def get(self, request):
        return Response(SummaryFileSerializer(SummaryFile.objects.all(), many=True).data)