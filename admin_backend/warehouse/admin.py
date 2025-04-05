from django.contrib import admin
from .models import Warehouse
# Register your models here.

@admin.register(Warehouse)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('warehouse_id', 'warehouse_location', 'stored_materials')