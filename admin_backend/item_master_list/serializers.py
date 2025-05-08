from rest_framework import serializers
from .models import Vendor, ItemMasterData
from django.core.cache import cache
import uuid

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'company_name', 'status']
        read_only_fields = ['vendor_code', 'status']
    
    def create(self, validated_data):
        # Generate a unique vendor_code
        vendor_code = f"VEN-{uuid.uuid4().hex[:8].upper()}"
        validated_data['vendor_code'] = vendor_code
        return super().create(validated_data)


class ItemMasterDataSerializer(serializers.ModelSerializer):
    # Convert preferred_vendor to dropdown using vendor choices
    preferred_vendor = serializers.ChoiceField(
        choices=[], 
        required=False,
        allow_null=True,
        allow_blank=True
    )
    
    # Add a display field for vendor name
    preferred_vendor_name = serializers.SerializerMethodField(read_only=True)

    def get_preferred_vendor_name(self, obj):
        if obj.preferred_vendor:
            # Cache the vendor name lookup
            cache_key = f'vendor_name_{obj.preferred_vendor}'
            vendor_name = cache.get(cache_key)
            
            if vendor_name is None:
                try:
                    vendor = Vendor.objects.only('company_name').get(vendor_code=obj.preferred_vendor)
                    vendor_name = vendor.company_name
                    # Cache for 10 minutes
                    cache.set(cache_key, vendor_name, 600)
                except Vendor.DoesNotExist:
                    return None
            return vendor_name
        return None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache vendor choices for 5 minutes
        cache_key = 'vendor_choices'
        vendor_choices = cache.get(cache_key)
        
        if vendor_choices is None:
            # Use only() to fetch just the needed fields
            vendors = Vendor.objects.only('vendor_code', 'company_name').order_by('company_name')
            vendor_choices = [(v.vendor_code, v.company_name) for v in vendors]
            cache.set(cache_key, vendor_choices, 300)  # Cache for 5 minutes
            
        self.fields['preferred_vendor'].choices = vendor_choices
    
    class Meta:
        model = ItemMasterData
        fields = ['item_id', 'item_name', 'item_description', 'item_type',
                 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor',
                 'preferred_vendor_name', 'purchasing_uom', 'items_per_purchase_unit',
                 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit',
                 'sales_quantity_per_package']
        read_only_fields = ['item_id']

    def create(self, validated_data):
        # Generate a unique vendor_code
        item_id = f"ADMIN-ITEM-{uuid.uuid4().hex[:8].upper()}"
        validated_data['item_id'] = item_id
        return super().create(validated_data)


class VendorChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'company_name', 'status']