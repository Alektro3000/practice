import csv
import time
import io
from django.core.files.base import ContentFile
from django.http import FileResponse

from warehouse.models import Movement

from summary.serializers import *
from summary.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateProductSummaryCSVView(APIView):
    def post(self, request):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Название товара', 'Категория', 'Остаток'])
        total_quantity=0
        for product in ProductSummary.objects.all():
            writer.writerow([product.product_name, product.category, product.current_quantity])
            total_quantity += product.current_quantity
        writer.writerow(["", "", "Итого: "+str(total_quantity)])
        
        csv_content = output.getvalue()
        output.close()
        summary = SummaryFile(name = "Product" + str(time.time()) + ".csv", type = "Product", format = "csv")
        summary.file.save( "Product" + str(time.time()) + ".csv", ContentFile(csv_content.encode('utf-8-sig')))
        summary.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CreateProductRunOutSummaryCSVView(APIView):
    def post(self, request):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Название товара', 'Категория', 'Остаток'])
        for product in ProductRunOutSummary.objects.all():
            writer.writerow([product.product_name, product.category, product.stock_difference])
        
        csv_content = output.getvalue()
        output.close()
        summary = SummaryFile(name = "RunOut" + str(time.time()) + ".csv", type = "RunOut", format = "csv")
        summary.file.save( "RunOut" + str(time.time()) + ".csv", ContentFile(csv_content.encode('utf-8-sig')))
        summary.save()

        return Response(status=status.HTTP_204_NO_CONTENT)



class CreateMovementSummaryCSVView(APIView):
    def post(self, request):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Тип операции', 'Дата'])
        
        movements = MovementSummary.objects.all()

        min_date = request.query_params.get('min_date') 
        if min_date:
            movements = movements.filter(min_date__gt=min_date)
        
        max_date = request.query_params.get('max_date')
        if max_date:
            movements = movements.filter(max_date__lt=max_date)

        for movement in movements:
            writer.writerow([movement.operation_type, movement.operation_date])
        
        csv_content = output.getvalue()
        output.close()
        summary = SummaryFile(name = "Movement" + str(time.time()) + ".csv", type = "Movement", format = "csv")
        summary.file.save( "Movement" + str(time.time()) + ".csv", ContentFile(csv_content.encode('utf-8-sig')))
        summary.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
        
class CreateProductMovementFullSummaryCSVView(APIView):
    def post(self, request):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Тип операции', 'Изменение товара',  'Дата', 'Текущий остаток '])
        
        movements = ProductMovementSummary.objects.all()

        min_date = request.query_params.get('min_date') 
        if min_date:
            movements = movements.filter(min_date__gt=min_date)
        
        max_date = request.query_params.get('max_date')
        if max_date:
            movements = movements.filter(max_date__lt=max_date)

        product = request.query_params.get('product')
        if product:
            movements = movements.filter(product_id=product)

        for movement in movements:
            writer.writerow([movement.operation_type, movement.quantity_change, movement.operation_date, movement.balance_after_operation ])
        
        csv_content = output.getvalue()
        output.close()
        summary = SummaryFile(name = "ProductMovement" + str(time.time()) + ".csv", type = "ProductMovement", format = "csv")
        summary.file.save( "ProductMovement" + str(time.time()) + ".csv", ContentFile(csv_content.encode('utf-8-sig')))
        summary.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SummaryLoadView(APIView):
    def get(self, request, id):
        file_instance = SummaryFile.objects.get(id=id)
        return FileResponse(file_instance.file.open(), as_attachment=True, filename=file_instance.name)
    
    
class SummaryListView(APIView):
    def get(self, request):
        return Response(SummaryFileSerializer(SummaryFile.objects.all(), many=True).data)