from rest_framework import serializers
from .models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['warehouse_id', 'warehouse_location', 'stored_materials']
        read_only_fields = ['warehouse_id']

    def create(self, validated_data):
        # Generate a unique warehouse_id
        import uuid
        warehouse_id = f"ADMIN-WARE-{uuid.uuid4().hex[:8].upper()}"
        validated_data['warehouse_id'] = warehouse_id
        return super().create(validated_data)