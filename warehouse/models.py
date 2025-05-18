from django.db import models
from django.http import HttpResponse


        
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = '"warehouse"."category"'

class UnitOfMeasure(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = '"warehouse"."unit_of_measure"'

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT,  db_column='category_id')
    unit_of_measure_id = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT,  db_column='unit_of_measure_id')
    description = models.TextField()
    product_size = models.CharField(max_length=10)
    min_stock_level = models.IntegerField()
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now_add=True)

    current_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_quantity_view"'


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    operation_type = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT,  db_column='product_id')
    quantity = models.IntegerField()
    operation_date = models.DateTimeField()
    user_id = models.TextField()
    comments = models.TextField()

    class Meta:
        managed = False
        db_table = '"warehouse"."operation"'


class Movement(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT,  db_column='product_id')
    operation_id = models.ForeignKey(Operation, on_delete=models.PROTECT,  db_column='operation_id')
    quantity_change = models.IntegerField()
    balance_after_operation = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_movement"'
