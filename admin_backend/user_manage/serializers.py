from rest_framework import serializers
from .models import User, RolePermission

class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the RolePermission model.
    Handles validation and conversion between JSON and model objects.
    """
    class Meta:
        model = RolePermission
        fields = ['role_id', 'role_name', 'description', 'permissions', 'access_level']
        read_only_fields = ['role_id']  # role_id is auto-generated and shouldn't be edited directly

    def create(self, validated_data):
        """
        Create and return a new RolePermission instance, given the validated data.
        """
        # The role_id is handled in the view with raw SQL, so we don't need to set it here
        return RolePermission(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing RolePermission instance, given the validated data.
        """
        instance.role_name = validated_data.get('role_name', instance.role_name)
        instance.description = validated_data.get('description', instance.description)
        instance.permissions = validated_data.get('permissions', instance.permissions)
        instance.access_level = validated_data.get('access_level', instance.access_level)
        
        # Note: We don't call save() here because in the views, raw SQL is used for persistence
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles validation and conversion between JSON and model objects.
    """
    role_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'employee_id', 'first_name', 'last_name', 
            'email', 'password', 'role', 'role_name', 'status', 
            'type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at']  # These fields are auto-generated

    def get_role_name(self, obj):
        """Return the name of the role, if a role exists."""
        return obj.role.role_name if obj.role else None

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        # The user_id is handled in the view with raw SQL, so we don't need to set it here
        return User(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance, given the validated data.
        """
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.role = validated_data.get('role', instance.role)
        instance.status = validated_data.get('status', instance.status)
        instance.type = validated_data.get('type', instance.type)
        
        # Note: We don't call save() here because in the views, raw SQL is used for persistence
        return instance

    def validate_password(self, value):
        """
        Add custom validation for password if needed.
        For example, enforce password strength requirements.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value