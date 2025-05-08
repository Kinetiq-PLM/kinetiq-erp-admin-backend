from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_code = models.CharField(primary_key=True, max_length=255)
    company_name = models.CharField(max_length=255, db_index=True)  # Added index
    status = models.CharField(max_length=20, default='Approved')

    def __str__(self):
        return self.company_name

    class Meta:
        managed = False
        db_table = '"purchasing"."vendors"'
        indexes = [
            models.Index(fields=['status']),  # Add index on commonly filtered fields
        ]


class ItemMasterData(models.Model):
    # Use class attributes for constant values to avoid recreation
    PRODUCT = 'Product'
    RAW_MAT = 'Raw Material'
    ASSET = 'Asset'

    ITEM_TYPE_CHOICES = [
        (PRODUCT, 'Product'),
        (RAW_MAT, 'Raw Material'),
        (ASSET, 'Asset')
    ]

    KG, SH, BX, L, M, GAL, PCS, SET, MM, UNIT = 'kg', 'sh', 'bx', 'l', 'm', 'gal', 'pcs', 'set', 'mm', 'unit'

    UOM_CHOICES = [
        (KG, 'kg'), (SH, 'sh'), (BX, 'bx'), (L, 'l'), (M, 'm'),
        (GAL, 'gal'), (PCS, 'pcs'), (SET, 'set'), (MM, 'mm'), (UNIT, 'unit')
    ]

    ACTIVE, INACTIVE, BLOCKED = 'Active', 'Inactive', 'Blocked'

    ITEM_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (BLOCKED, 'Blocked')
    ]

    SERIAL_NO, BATCHES, NONE = 'Serial Number', 'Batches', 'None'

    MANAGE_TYPE = [
        (SERIAL_NO, 'Serial Number'),
        (BATCHES, 'Batches'),
        (NONE, 'None')
    ]

    item_id = models.CharField(primary_key=True, max_length=255)
    item_name = models.CharField(max_length=255, db_index=True)  # Add index for frequent searches
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default=PRODUCT, db_index=True)
    unit_of_measure = models.CharField(max_length=5, choices=UOM_CHOICES, blank=True, null=True)
    item_status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default=ACTIVE, db_index=True)
    manage_item_by = models.CharField(max_length=20, choices=MANAGE_TYPE, default=BATCHES)
    preferred_vendor = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    purchasing_uom = models.CharField(max_length=5, choices=UOM_CHOICES, blank=True, null=True)
    items_per_purchase_unit = models.IntegerField(blank=True, null=True)
    purchase_quantity_per_package = models.IntegerField(blank=True, null=True)
    sales_uom = models.CharField(max_length=5, choices=UOM_CHOICES, blank=True, null=True)
    items_per_sale_unit = models.IntegerField(blank=True, null=True)
    sales_quantity_per_package = models.IntegerField(blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_id

    class Meta:
        db_table = '"admin"."item_master_data"'
        verbose_name = 'Item Master Data'
        verbose_name_plural = 'Item Master Data'
        managed = False
        indexes = [
            models.Index(fields=['item_status']),
            models.Index(fields=['item_type']),
        ]