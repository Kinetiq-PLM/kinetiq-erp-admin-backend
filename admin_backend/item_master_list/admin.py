from django.contrib import admin
from .models import Assets, Products, RawMaterials, ItemMasterData

@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'asset_name', 'purchase_date', 'purchase_price', 'serial_no', 'content_id')

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'description', 'selling_price', 'stock_level', 'unit_of_measure', 'batch_no', 'item_status', 'warranty_period', 'policy_id', 'content_id')

@admin.register(RawMaterials)
class RawMaterialsAdmin(admin.ModelAdmin):
    list_display = ('material_id', 'material_name', 'description', 'unit_of_measure', 'cost_per_unit', 'vendor_code')

@admin.register(ItemMasterData)
class ItemMasterDataAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type', 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor', 'purchasing_uom', 'items_per_purchase_unit', 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit', 'sales_quantity_per_package')