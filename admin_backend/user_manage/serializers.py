# user_manage/serializers.py
from rest_framework import serializers
from .models import User, RolePermission

class RolePermissionSerializer(serializers.ModelSerializer):
    # Add a new field for the UI that is not part of the model
    department_permissions = serializers.MultipleChoiceField(
        choices=[
            ('Accounting', 'Accounting'),
            ('Administration', 'Administration'),
            ('Distribution', 'Distribution'),
            ('Finance', 'Finance'),
            ('Human Resources', 'Human Resources'),
            ('Inventory', 'Inventory'),
            ('Management', 'Management'),
            ('MRP', 'MRP'),
            ('Operations', 'Operations'),
            ('Production', 'Production'),
            ('Project Management', 'Project Management'),
            ('Purchasing', 'Purchasing'),
            ('Sales', 'Sales'),
            ('Services', 'Services'),
            ('Solution Customizing', 'Solution Customizing'),
        ],
        required=False
    )
    
    class Meta:
        model = RolePermission
        fields = ['role_id', 'role_name', 'description', 'permissions', 'department_permissions']
        read_only_fields = ['role_id', 'permissions']  # Make original permissions read-only

    def to_representation(self, instance):
        """Convert stored comma-separated string to list for UI"""
        representation = super().to_representation(instance)
        
        # Parse the stored permissions string into a list
        if instance.permissions:
            representation['department_permissions'] = instance.permissions.split(',')
        else:
            representation['department_permissions'] = []
            
        # Remove the original permissions field from the output
        representation.pop('permissions', None)
        
        return representation
    
    def create(self, validated_data):
        # Extract the department_permissions list
        department_permissions = validated_data.pop('department_permissions', [])
        
        # Convert to comma-separated string
        permissions_string = ','.join(department_permissions)
        validated_data['permissions'] = permissions_string
        
        # Generate a unique role_id
        import uuid
        role_id = f"ADMIN-ROLE-{uuid.uuid4().hex[:6]}"
        validated_data['role_id'] = role_id
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Extract the department_permissions list
        department_permissions = validated_data.pop('department_permissions', None)
        
        if department_permissions is not None:
            # Convert to comma-separated string
            permissions_string = ','.join(department_permissions)
            validated_data['permissions'] = permissions_string
        
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    role_details = RolePermissionSerializer(source='role', read_only=True)
    # Replace the CharField with a PrimaryKeyRelatedField to create a dropdown
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=RolePermission.objects.all().order_by('role_name'),
        required=False,
        allow_null=True,
        label='Role'
    )

    # Add this field to make password optional during updates
    password = serializers.CharField(
        write_only=True,  # Hide password in responses
        required=False,   # Make it optional for updates
        style={'input_type': 'password'}  # For UI rendering as password field
    )
    
    # Add a display field for showing role names in the dropdown
    role_display = serializers.SerializerMethodField(read_only=True)
    
    def get_role_display(self, obj):
        if obj.role:
            return obj.role.role_name
        return None
    
    class Meta:
        model = User
        fields = ['user_id', 'employee_id', 'first_name', 'last_name', 'email', 
                 'password', 'role_id', 'role_display', 'role_details', 'status', 'type', 
                 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'employee_id', 'created_at', 'updated_at', 'role_display']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
    
    def create(self, validated_data):
        # Generate a unique user_id
        import uuid
        user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"
        validated_data['user_id'] = user_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # For update: if password is empty or not provided, remove it from validated_data
        # to avoid updating the password field
        if 'password' in validated_data and not validated_data['password']:
            validated_data.pop('password')

        # Preserve the role if not provided in the update data
        if 'role' in validated_data and not validated_data['role']:
            validated_data.pop('role')
        
        # For update: Since there's no trigger for update password hashing,
        # we need to explicitly call the hash_user_passwords function
        updated_instance = super().update(instance, validated_data)
        
        # If password was updated, call the hash function
        from django.db import connection
        if 'password' in validated_data:
            with connection.cursor() as cursor:
                cursor.execute("SELECT admin.hash_user_passwords();")
        
        return updated_instance
    
    def validate_password(self, value):
        """
        Add custom validation for password if needed.
        For example, enforce password strength requirements.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def to_representation(self, instance):
        # This customizes the output representation
        ret = super().to_representation(instance)
        
        # Instead of removing role_id, include it in the response
        # BUT rename it to clarify it's for form submission
        if 'role_id' in ret:
            # Optionally: rename to make it clear this is for forms
            # ret['role_form_value'] = ret['role_id']
            # del ret['role_id']
            
            # Or simply keep role_id as is
            pass
            
        return ret

    # def to_representation(self, instance):
    #     # This customizes the output representation
    #     ret = super().to_representation(instance)
    #     # Remove role_id from output to avoid confusion
    #     # since we're now passing the whole role object
    #     if 'role_id' in ret and ret['role_id'] is not None:
    #         del ret['role_id']
    #     return ret


# If you want to provide a list of roles for a dropdown in the frontend,
# you can create a simple serializer like this:
class RoleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['role_id', 'role_name']