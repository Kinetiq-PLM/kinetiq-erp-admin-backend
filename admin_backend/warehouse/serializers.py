from rest_framework import serializers
from .models import Warehouse, WarehouseManagers


class WarehouseManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseManagers
        fields = ['user_id', 'employee_id', 'first_name', 'last_name', 'role_id']


class WarehouseManagerChoiceField(serializers.ChoiceField):
    """Custom choice field for warehouse managers that returns the employee_id"""
    
    def __init__(self, **kwargs):
        # Get all warehouse managers with the admin role
        managers = WarehouseManagers.objects.filter(role_id='ADMIN-ROLE-2025-ce28ef')
        
        # Create choices as a list of tuples (employee_id, display_name)
        choices = [(manager.employee_id, f"{manager.first_name} {manager.last_name}") 
                   for manager in managers]
        
        kwargs['choices'] = choices
        super().__init__(**kwargs)
    
    def to_representation(self, value):
        # Return the value (employee_id) directly for serialization
        return value


class WarehouseSerializer(serializers.ModelSerializer):
    # Create a field to display the manager's name for read operations
    manager_name = serializers.SerializerMethodField()
    
    # Use a custom choice field for the warehouse_manager
    warehouse_manager = WarehouseManagerChoiceField(required=True)
    
    class Meta:
        model = Warehouse
        fields = ['warehouse_id', 'warehouse_location', 'warehouse_name', 
                  'warehouse_manager', 'manager_name', 'contact_no']
        read_only_fields = ['warehouse_id']
    
    def get_manager_name(self, obj):
        """Return the full name of the warehouse manager"""
        try:
            manager = WarehouseManagers.objects.get(employee_id=obj.warehouse_manager)
            return f"{manager.first_name} {manager.last_name}"
        except WarehouseManagers.DoesNotExist:
            return None