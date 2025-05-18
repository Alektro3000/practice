from warehouse.models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category_id', 'unit_of_measure_id', 'description', 'product_size', 'min_stock_level','created_at', 'updated_at' , 'current_quantity']
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_quantity']
        depth = 1
        
class ProductEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category_id', 'unit_of_measure_id', 'description', 'product_size', 'min_stock_level','created_at']
        read_only_fields = ['id', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        
class MovementSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Movement
        fields = ['id', 'operation_id', 'balance_after_operation']
        read_only_fields = ['id']
        depth = 3

        
class OperationSerializer(serializers.ModelSerializer):    
    def create(self, validated_data):
        # Automatically add username from request.user
        user =  self.context['request'].user.username
        validated_data['user_id'] = user
        return super().create(validated_data)
    
    class Meta:
        model = Operation
        fields = ['id', 'operation_type', 'product_id', 'quantity', 'operation_date', 'user_id', 'comments']
        read_only_fields = ['id', 'user_id']
        depth = 2

