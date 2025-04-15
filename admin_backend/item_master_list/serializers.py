from rest_framework import serializers
from .models import Assets, Policies, Vendor, Products, RawMaterials, ItemMasterData

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ['asset_id', 'asset_name', 'purchase_date', 'purchase_price', 'serial_no', 'content_id']
        read_only_fields = ['asset_id']

    def create(self, validated_data):
        # Generate a unique asset_id
        import uuid
        asset_id = f"ASSET-{uuid.uuid4().hex[:8].upper()}"
        validated_data['asset_id'] = asset_id
        
        # Set content_id to null if empty to avoid FK constraint violation
        if 'content_id' in validated_data and not validated_data['content_id']:
            validated_data['content_id'] = None
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Set content_id to null if empty to avoid FK constraint violation
        if 'content_id' in validated_data and not validated_data['content_id']:
            validated_data['content_id'] = None
            
        return super().update(instance, validated_data)
    
class PoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policies
        fields = ['policy_id', 'policy_name', 'description', 'effective_date', 'status']
        read_only_fields = ['policy_id']
    
    def create(self, validated_data):
        # Generate a unique policy_id
        import uuid
        policy_id = f"POL-{uuid.uuid4().hex[:8].upper()}"
        validated_data['policy_id'] = policy_id
        return super().create(validated_data)

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'application_reference', 'vendor_name', 'contact_person', 'status']
        read_only_fields = ['vendor_code']
    
    def create(self, validated_data):
        # Generate a unique vendor_code
        import uuid
        vendor_code = f"VEN-{uuid.uuid4().hex[:8].upper()}"
        validated_data['vendor_code'] = vendor_code
        return super().create(validated_data)

class ProductsSerializer(serializers.ModelSerializer):
    policy_details = PoliciesSerializer(source='policy', read_only=True)
    
    # Replace the existing policy_id field with this improved version
    policy_id = serializers.PrimaryKeyRelatedField(
        source='policy',
        queryset=Policies.objects.all().order_by('policy_name'),
        required=False,
        allow_null=True,
        label='Policy'
    )
    
    # Add a display field for the dropdown
    policy_name = serializers.SerializerMethodField(read_only=True)
    
    def get_policy_name(self, obj):
        if obj.policy:
            return obj.policy.policy_name
        return None
    
    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'description', 'selling_price', 'stock_level', 
                 'unit_of_measure', 'batch_no', 'item_status', 'warranty_period', 'policy_id', 
                 'policy_name', 'policy_details', 'content_id']
        read_only_fields = ['product_id']
    
    def create(self, validated_data):
        # Generate a unique product_id
        import uuid
        product_id = f"PROD-{uuid.uuid4().hex[:8].upper()}"
        validated_data['product_id'] = product_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Set content_id to null if empty to avoid FK constraint violation
        if 'content_id' in validated_data and not validated_data['content_id']:
            validated_data['content_id'] = None
            
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Only remove policy_id if we're showing full details
        if 'policy_id' in ret:
            pass
        return ret

class RawMaterialsSerializer(serializers.ModelSerializer):
    vendor_details = VendorSerializer(source='vendor_code', read_only=True)

    vendor_id = serializers.PrimaryKeyRelatedField(
        source='vendor_code',
        queryset=Vendor.objects.all(),
        required=False,
        allow_null=True,
        label='Vendor'
    )

    # Add a display field for the dropdown
    vendor_name = serializers.SerializerMethodField(read_only=True)
    
    def get_vendor_name(self, obj):
        if obj.vendor_code:
            return obj.vendor_code.vendor_name
        return None
    
    class Meta:
        model = RawMaterials
        fields = ['material_id', 'material_name', 'description', 'unit_of_measure', 
                 'cost_per_unit', 'vendor_id', 'vendor_name', 'vendor_details']
        read_only_fields = ['material_id']
    
    def create(self, validated_data):
        # Generate a unique material_id
        import uuid
        material_id = f"MAT-{uuid.uuid4().hex[:8].upper()}"
        validated_data['material_id'] = material_id
        return super().create(validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'vendor_id' in ret:
            pass
        return ret

class ItemMasterDataSerializer(serializers.ModelSerializer):
    # asset_details = AssetsSerializer(source='asset', read_only=True)
    # product_details = ProductsSerializer(source='product', read_only=True)
    # material_details = RawMaterialsSerializer(source='material', read_only=True)
    
    # # These fields will be removed from create/edit forms but remain in detail views
    # asset_id = serializers.PrimaryKeyRelatedField(
    #     source='asset',
    #     queryset=Assets.objects.all(),
    #     required=False,
    #     allow_null=True,
    #     label='Asset',
    #     write_only=True  # Hide in output
    # )
    
    # product_id = serializers.PrimaryKeyRelatedField(
    #     source='product',
    #     queryset=Products.objects.all(),
    #     required=False,
    #     allow_null=True,
    #     label='Product',
    #     write_only=True  # Hide in output
    # )
    
    # material_id = serializers.PrimaryKeyRelatedField(
    #     source='material',
    #     queryset=RawMaterials.objects.all(),
    #     required=False,
    #     allow_null=True,
    #     label='Material',
    #     write_only=True  # Hide in output
    # )
    
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
            # Since preferred_vendor is now a relationship, get the name
            try:
                vendor = Vendor.objects.get(vendor_code=obj.preferred_vendor)
                return vendor.vendor_name
            except Vendor.DoesNotExist:
                return None
        return None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate vendor choices
        vendors = Vendor.objects.all().order_by('vendor_name')
        self.fields['preferred_vendor'].choices = [(v.vendor_code, v.vendor_name) for v in vendors]
    
    class Meta:
        model = ItemMasterData
        fields = ['item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type',
                 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor',
                 'preferred_vendor_name', 'purchasing_uom', 'items_per_purchase_unit',
                 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit',
                 'sales_quantity_per_package'] 
                #  'asset_details', 'product_details', 'material_details']
        read_only_fields = ['item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type',
                          'unit_of_measure', 'item_status', 'manage_item_by']
    
    def update(self, instance, validated_data):
        # Ensure we don't try to modify the asset, product, or material relationships
        validated_data.pop('asset', None)
        validated_data.pop('product', None)
        validated_data.pop('material', None)
        
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        # For create/edit forms, remove these fields
        if self.context.get('request') and self.context.get('request').method in ['POST', 'PUT', 'PATCH']:
            ret.pop('asset_details', None)
            ret.pop('product_details', None)
            ret.pop('material_details', None)
        
        return ret

class PolicyChoiceSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Policies
        fields = ['policy_id', 'policy_name']

class VendorChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'vendor_name']