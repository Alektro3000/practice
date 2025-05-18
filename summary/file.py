import csv
import time
import io

import os
from django.core.files.base import ContentFile

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.conf import settings
from summary.models import SummaryFile

def createPDF(data):
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

def createCSV(data):
    output = io.StringIO()
    writer = csv.writer(output)

    for row in data:
        writer.writerow(row)
        
    csv_content = output.getvalue()
    output.close()
    return csv_content.encode("utf-8-sig")
    
def createFile(data, format: str):
    if(format == "pdf"):
    # Build the PDF
        return createPDF(data)
    elif(format == "csv"):
     # Build the CSV
        return createCSV(data)
    
def saveFile(file, type: str, format: str):
    summary = SummaryFile(name = type + str(time.time()) + "." + format, type = type, format = format)
    summary.file.save(type + str(time.time()) + "." + format, ContentFile(file))
    summary.save()
    
def createAndSaveFile(data, type: str, format: str):
    file = createFile(data, format)
    saveFile(file, type, format)
