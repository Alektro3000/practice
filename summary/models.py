from django.db import models
from django.http import HttpResponse

# Create your models here.

class SummaryFile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='product_summary/')
    type = models.CharField(max_length=20)
    format = models.CharField(max_length=3)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ProductSummary(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(255)
    category = models.CharField(10)
    current_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_inventory_view"'

        
class ProductRunOutSummary(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(255)
    category = models.CharField(120)
    stock_difference = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_availability_view"'


class MovementSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    operation_type = models.CharField()
    operation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_movement_view"'

    
class ProductMovementSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField()
    operation_type = models.CharField()
    operation_date = models.DateTimeField()
    quantity_change = models.IntegerField()
    balance_after_operation = models.IntegerField()

    class Meta:
        managed = False
        db_table = '"warehouse"."product_movement_full_view"'