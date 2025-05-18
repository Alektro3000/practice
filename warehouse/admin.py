from django.contrib import admin
from warehouse.models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UnitOfMeasure)
admin.site.register(Operation)
admin.site.register(Movement)