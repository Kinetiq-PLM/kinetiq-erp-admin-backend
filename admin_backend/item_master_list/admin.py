from django.contrib import admin
from .models import ItemMasterData

@admin.register(ItemMasterData)
class ItemMasterDataAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_description', 'item_name', 'item_type', 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor', 'purchasing_uom', 'items_per_purchase_unit', 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit', 'sales_quantity_per_package')