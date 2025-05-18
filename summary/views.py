from django.core.files.base import ContentFile
from django.http import FileResponse

from summary.serializers import *
from summary.models import *
from summary.file import createAndSaveFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.http import FileResponse

from summary.serializers import *
from summary.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SummaryLoadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        file_instance = SummaryFile.objects.get(id=id)
        return FileResponse(file_instance.file.open(), as_attachment=True, filename=file_instance.name)
    
    
class SummaryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(SummaryFileSerializer(SummaryFile.objects.all(), many=True).data)
    


def getProductSummary():
    header = [
        ['Название товара', 'Категория', 'Остаток'],
    ]
    data = [ [product.product_name, product.category, product.current_quantity] for product in ProductSummary.objects.all()]
    footer = [ ['', '', 'Итого: '+str(sum([i[2] for i in data]))] ] 
    return header + data + footer

class ProductSummaryCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getProductSummary(), "Product", 'csv')
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductSummaryPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getProductSummary(), "Product", 'pdf')
        return Response(status=status.HTTP_204_NO_CONTENT)


def getRunOutSummary():
    header = [
        ['Название товара', 'Категория', 'Нехватка'],
    ]
    data = [ [product.product_name, product.category, product.stock_difference] \
            for product in ProductRunOutSummary.objects.all()]
    return header + data


class RunOutSummaryCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getRunOutSummary(), "RunOut", 'csv')
        return Response(status=status.HTTP_204_NO_CONTENT)

class RunOutSummaryPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getRunOutSummary(), "RunOut", 'pdf')
        return Response(status=status.HTTP_204_NO_CONTENT)

def getMovementSummary(request):
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

        return header + data


class MovementSummaryCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getMovementSummary(request), "Movement", 'csv')
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovementSummaryPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getMovementSummary(request), "Movement", 'pdf')
        return Response(status=status.HTTP_204_NO_CONTENT)

def getProductMovementSummary(request):
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
        return header + data
        

class MovementFullSummaryCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getProductMovementSummary(request), "MovementFull", 'csv')
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MovementFullSummaryPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        createAndSaveFile(getProductMovementSummary(request), "MovementFull", 'pdf')
        return Response(status=status.HTTP_204_NO_CONTENT)


    