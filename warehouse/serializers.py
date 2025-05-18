from warehouse.models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category_id', 'unit_of_measure_id', 'description', 'product_size', 'min_stock_level','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
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
    comments = serializers.CharField(source='operation_id.comments', read_only=True)
    operation_date = serializers.DateTimeField(source='operation_id.operation_date', read_only=True)
    class Meta:
        model = Movement
        fields = ['id', 'product_id',  'operation_id', 'quantity_change', 'balance_after_operation','comments', 'operation_date']
        read_only_fields = ['id']

        
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

