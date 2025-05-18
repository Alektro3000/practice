import csv
from django.shortcuts import HttpResponse

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from warehouse.serializers import *
from warehouse.models import *


class ProductListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Product.objects.all()
        category = request.query_params.get('category_id')  # /products/?category_id=category_id
        if category:
            queryset = queryset.filter(category=category)
        
        name = request.query_params.get('name')  # /products/?name=test
        if name:
            queryset = queryset.filter(name__contains=name)
        
        quantity = request.query_params.get('quantity')  # /products/?quantity=quantity
        if quantity:
            queryset = queryset.filter(quantity=quantity)

        availability = request.query_params.get('availability')  # /products/?availability=availability
        if availability:
            queryset = queryset.filter(availability=availability)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            value = serializer.save()
            value.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
    
class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        return Response(ProductSerializer(Product.objects.get(id = id)).data)
    
    def put(self, request, id):
        serializer = ProductSerializer(Product.objects.get(id=id), data = request.data, partial=True)
        
        if serializer.is_valid():
            value = serializer.save()
            value.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        Product.objects.get(id = id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    


class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(CategorySerializer(Category.objects.all(), many=True).data)

class CategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        return Response(ProductSerializer(Category.objects.get(id = id)))
    
    
class MovementListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Movement.objects.all()
        min_date = request.query_params.get('min_date')  # /products/?min_date=min_date
        if min_date:
            queryset = queryset.filter(min_date__gte=min_date)
        
        max_date = request.query_params.get('max_date')  # /products/?max_date=max_date
        if max_date:
            queryset = queryset.filter(max_date__lte=max_date)
        
        type = request.query_params.get('type')  # /products/?type=type
        if type:
            queryset = queryset.filter(type=type)

        #there is no name
        comments = request.query_params.get('comments')  # /products/?comments=comments
        if comments:
            queryset = queryset.filter(comments__contains=comments)

        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MovementEditSerializer(data = request.data)
        if serializer.is_valid():
            value = serializer.save()
            value.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class MovementView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        return Response(MovementSerializer(Movement.objects.get(id = id)).data)
    
    
    def put(self, request, id):
        serializer = MovementEditSerializer(Movement.objects.get(id=id), data = request.data, partial=True)
        
        if serializer.is_valid():
            value = serializer.save()
            value.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        MovementEditSerializer.objects.get(id = id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class OperationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Operation.objects.all()
        min_date = request.query_params.get('min_date')  # /products/?min_date=min_date
        if min_date:
            queryset = queryset.filter(min_date__gte=min_date)
        
        max_date = request.query_params.get('max_date')  # /products/?max_date=max_date
        if max_date:
            queryset = queryset.filter(max_date__lte=max_date)
        
        type = request.query_params.get('type')  # /products/?type=type
        if type:
            queryset = queryset.filter(type=type)

        #there is no name
        comments = request.query_params.get('comments')  # /products/?comments=comments
        if comments:
            queryset = queryset.filter(comments__contains=comments)

        serializer = OperationSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OperationEditSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            value = serializer.save()
            value.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class OperationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        return Response(OperationSerializer(Operation.objects.get(id = id)).data)
    
    
    def put(self, request, id):
        serializer = OperationEditSerializer(Operation.objects.get(id=id), data = request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            serializer.refresh_from_db()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        Operation.objects.get(id = id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

class ExportCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="products.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Category', 'product_size'])

        for product in Product.objects.all():
            writer.writerow([product.id, product.name, 
                             product.category_id, product.product_size])

        return response
    

class ProductLastListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Product.objects.all().order_by('-updated_at')[:5]

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
class MovementLastListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Movement.objects.all().select_related('operation_id').order_by('-operation_id__operation_date')[:5]

        serializer = MovementSerializer(queryset, many=True)
        return Response(serializer.data)
    
class OperationLastListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Operation.objects.all().order_by('-operation_date')[:5]

        serializer = OperationSerializer(queryset, many=True)
        return Response(serializer.data)