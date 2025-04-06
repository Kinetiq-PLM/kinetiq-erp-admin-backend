from rest_framework import serializers
from .models import ItemMasterData, Products, RawMaterials, Assets

class AssetsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Assets model.
    Handles validation and conversion between JSON and model objects.
    """
    class Meta:
        model = Assets
        fields = ['asset_id', 'asset_name', 'purchase_date', 'purchase_price', 'serial_no', 'content_id']
        read_only_fields = ['asset_id']  # asset_id is auto-generated and shouldn't be edited directly

    def create(self, validated_data):
        """
        Create and return a new Assets instance, given the validated data.
        """
        # The asset_id is handled in the view with raw SQL, so we don't need to set it here
        return Assets(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Assets instance, given the validated data.
        """
        instance.asset_name = validated_data.get('asset_name', instance.asset_name)
        instance.purchase_date = validated_data.get('purchase_date', instance.purchase_date)
        instance.purchase_price = validated_data.get('purchase_price', instance.purchase_price)
        instance.serial_no = validated_data.get('serial_no', instance.serial_no)
        instance.content_id = validated_data.get('content_id', instance.content_id)

        # Note: We don't call save() here because in the views, raw SQL is used for persistence
        return instance


class ProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Products model.
    Handles validation and conversion between JSON and model objects.
    """
    policy_name = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = [
            'product_id', 'product_name', 'description', 'selling_price', 
            'stock_level', 'unit_of_measure', 'batch_no', 'item_status', 
            'warranty_period', 'policy', 'policy_name', 'content_id'
        ]
        read_only_fields = ['product_id']  # product_id is auto-generated

    def get_policy_name(self, obj):
        """Return the name of the policy, if a policy exists."""
        return obj.policy.policy_name if obj.policy else None

    def create(self, validated_data):
        """
        Create and return a new Products instance, given the validated data.
        """
        return Products(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Products instance, given the validated data.
        """
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.description = validated_data.get('description', instance.description)
        instance.selling_price = validated_data.get('selling_price', instance.selling_price)
        instance.stock_level = validated_data.get('stock_level', instance.stock_level)
        instance.unit_of_measure = validated_data.get('unit_of_measure', instance.unit_of_measure)
        instance.batch_no = validated_data.get('batch_no', instance.batch_no)
        instance.item_status = validated_data.get('item_status', instance.item_status)
        instance.warranty_period = validated_data.get('warranty_period', instance.warranty_period)
        instance.policy = validated_data.get('policy', instance.policy)
        instance.content_id = validated_data.get('content_id', instance.content_id)

        return instance

class RawMaterialsSerializer(serializers.ModelSerializer):
    """
    Serializer for the RawMaterials model.
    Handles validation and conversion between JSON and model objects.
    """
    vendor_name = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterials
        fields = [
            'material_id', 'material_name', 'description', 'unit_of_measure',
            'cost_per_unit', 'vendor_code', 'vendor_name'
        ]
        read_only_fields = ['material_id']  # material_id is auto-generated

    def get_vendor_name(self, obj):
        """Return the name of the vendor, if a vendor exists."""
        return obj.vendor_code.vendor_name if obj.vendor_code else None

    def create(self, validated_data):
        """
        Create and return a new RawMaterials instance, given the validated data.
        """
        return RawMaterials(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing RawMaterials instance, given the validated data.
        """
        instance.material_name = validated_data.get('material_name', instance.material_name)
        instance.description = validated_data.get('description', instance.description)
        instance.unit_of_measure = validated_data.get('unit_of_measure', instance.unit_of_measure)
        instance.cost_per_unit = validated_data.get('cost_per_unit', instance.cost_per_unit)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)

        return instance

class ItemMasterDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the ItemMasterData model.
    Handles validation and conversion between JSON and model objects.
    """
    class Meta:
        model = ItemMasterData
        fields = ['item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type', 'unit_of_measure', 'item_status', 'manage_item_by', 
                  'preferred_vendor', 'purchasing_uom', 'items_per_purchase_unit', 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit', 'sales_quantity_per_package']
        read_only_fields = ['item_id', 'asset_id', 'product_id', 'material_id', 'item_name', 'item_type', 'unit_of_measure', 'item_status', 'manage_item_by']  # item_id is auto-generated

    def update(self, instance, validated_data):
        """
        Update and return an existing ItemMasterData instance, given the validated data.
        """
        instance.preferred_vendor = validated_data.get('preferred_vendor', instance.preferred_vendor)
        instance.purchasing_uom = validated_data.get('purchasing_uom', instance.purchasing_uom)
        instance.items_per_purchase_unit = validated_data.get('items_per_purchase_unit', instance.items_per_purchase_unit)
        instance.purchase_quantity_per_package = validated_data.get('purchase_quantity_per_package', instance.purchase_quantity_per_package)
        instance.sales_uom = validated_data.get('sales_uom', instance.sales_uom)
        instance.items_per_sale_unit = validated_data.get('items_per_sale_unit', instance.items_per_sale_unit)
        instance.sales_quantity_per_package = validated_data.get('sales_quantity_per_package', instance.sales_quantity_per_package)
        
        # Note: We don't call save() here because in the views, raw SQL is used for persistence

        return instance