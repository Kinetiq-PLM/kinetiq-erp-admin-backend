from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class Assets(models.Model):
    asset_id = models.CharField(primary_key=True, max_length=255)
    asset_name = models.CharField(max_length=255)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=65535, decimal_places=2)
    serial_no = models.CharField(max_length=225, blank=True, null=True)
    content_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.asset_name

    class Meta:
        db_table = 'assets'
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        managed = False

class Policies(models.Model):

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (BLOCKED, 'Blocked')
    ]

    policy_id = models.CharField(primary_key=True, max_length=255)
    policy_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        managed = False
        db_table = 'policies'

class Vendor(models.Model):
    vendor_code = models.CharField(primary_key=True, max_length=255)
    application_reference = models.CharField(max_length=255, blank=True, null=True)
    vendor_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'vendor'
    
class Products(models.Model):
    KG = 'kg'
    SH = 'sh'
    BX = 'bx'
    L = 'l'
    M = 'm'
    GAL = 'gal'
    PCS = 'pcs'
    SET = 'set'
    MM = 'mm'
    UNIT = 'unit'

    UOM_CHOICES = [
        (KG, 'kg'),
        (SH, 'sh'),
        (BX, 'bx'),
        (L, 'l'),
        (M, 'm'),
        (GAL, 'gal'),
        (PCS, 'pcs'),
        (SET, 'set'),
        (MM, 'mm'),
        (UNIT, 'unit')
    ]

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'

    ITEM_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (BLOCKED, 'Blocked')
    ]

    product_id = models.CharField(primary_key=True, max_length=255)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    selling_price = models.DecimalField(max_digits=65535, decimal_places=2)
    stock_level = models.IntegerField(blank=True, null=True)
    unit_of_measure = models.CharField(max_length=5, choices=UOM_CHOICES, default=SET) 
    batch_no = models.CharField(max_length=255, blank=True, null=True)
    item_status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default=ACTIVE)
    warranty_period = models.IntegerField(blank=True, null=True)
    policy = models.ForeignKey(Policies, models.DO_NOTHING, blank=True, null=True)
    content_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        managed = False

class RawMaterials(models.Model):
    KG = 'kg'
    SH = 'sh'
    BX = 'bx'
    L = 'l'
    M = 'm'
    GAL = 'gal'
    PCS = 'pcs'
    SET = 'set'
    MM = 'mm'
    UNIT = 'unit'

    UOM_CHOICES = [
        (KG, 'kg'),
        (SH, 'sh'),
        (BX, 'bx'),
        (L, 'l'),
        (M, 'm'),
        (GAL, 'gal'),
        (PCS, 'pcs'),
        (SET, 'set'),
        (MM, 'mm'),
        (UNIT, 'unit')
    ]

    material_id = models.CharField(primary_key=True, max_length=255)
    material_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit_of_measure = models.CharField(max_length=5, choices=UOM_CHOICES, default=KG)
    cost_per_unit = models.DecimalField(max_digits=65535, decimal_places=2, blank=True, null=True)
    vendor_code = models.ForeignKey(Vendor, models.DO_NOTHING, db_column='vendor_code', blank=True, null=True)

    def __str__(self):
        return self.material_name

    class Meta:
        db_table = 'raw_materials'
        verbose_name = 'Raw Material'
        verbose_name_plural = 'Raw Materials'
        managed = False

class ItemMasterData(models.Model):
    PRODUCT = 'Product'
    RAW_MAT = 'Raw Material'
    ASSET = 'Asset'

    ITEM_TYPE_CHOICES = [
        (PRODUCT, 'Product'),
        (RAW_MAT, 'Raw Material'),
        (ASSET, 'Asset')
    ]

    KG = 'kg'
    SH = 'sh'
    BX = 'bx'
    L = 'l'
    M = 'm'
    GAL = 'gal'
    PCS = 'pcs'
    SET = 'set'
    MM = 'mm'
    UNIT = 'unit'

    UOM_CHOICES = [
        (KG, 'kg'),
        (SH, 'sh'),
        (BX, 'bx'),
        (L, 'l'),
        (M, 'm'),
        (GAL, 'gal'),
        (PCS, 'pcs'),
        (SET, 'set'),
        (MM, 'mm'),
        (UNIT, 'unit')
    ]

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'

    ITEM_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (BLOCKED, 'Blocked')
    ]

    SERIAL_NO = 'Serial'
    BATCHES = 'Batches'
    NONE = 'None'

    MANAGE_TYPE = [
        (SERIAL_NO, 'Serial Number'),
        (BATCHES, 'Batches'),
        (NONE, 'None')
    ]

    item_id = models.CharField(primary_key=True, max_length=255)
    asset = models.ForeignKey(Assets, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    material = models.ForeignKey('RawMaterials', models.DO_NOTHING, blank=True, null=True)
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default=PRODUCT)
    unit_of_measure = models.CharField(max_length=5, choices=UOM_CHOICES)
    item_status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default=ACTIVE)
    manage_item_by = models.CharField(max_length=20, choices=MANAGE_TYPE, default=BATCHES)
    preferred_vendor = models.CharField(max_length=255, blank=True, null=True)
    purchasing_uom = models.CharField(max_length=5, choices=UOM_CHOICES)
    items_per_purchase_unit = models.IntegerField(blank=True, null=True)
    purchase_quantity_per_package = models.IntegerField(blank=True, null=True)
    sales_uom = models.CharField(max_length=5, choices=UOM_CHOICES)
    items_per_sale_unit = models.IntegerField(blank=True, null=True)
    sales_quantity_per_package = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.item_id

    class Meta:
        db_table = 'item_master_data'
        verbose_name = 'Item Master Data'
        verbose_name_plural = 'Item Master Data'
        managed = False

class ItemMasterDataForm(forms.ModelForm):
    class Meta:
        model = ItemMasterData
        exclude = ['item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type', 'unit_of_measure', 'item_status', 'manage_item_by']

class AssetsForm(forms.ModelForm):
    class Meta:
        model = Assets
        fields = ['asset_name', 'purchase_date', 'purchase_price', 'serial_no', 'content_id']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'description', 'selling_price', 'stock_level', 'unit_of_measure', 
                 'batch_no', 'item_status', 'warranty_period', 'policy', 'content_id']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RawMaterialsForm(forms.ModelForm):
    class Meta:
        model = RawMaterials
        fields = ['material_name', 'description', 'unit_of_measure', 'cost_per_unit', 'vendor_code']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }