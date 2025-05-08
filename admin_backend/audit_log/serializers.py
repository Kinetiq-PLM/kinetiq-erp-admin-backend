# serializers.py
from rest_framework import serializers
from .models import AuditLog
from django.contrib.auth.models import User

class UserBasicSerializer(serializers.ModelSerializer):
    """Minimal user serializer for embedding in audit logs"""
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']

class AuditLogSerializer(serializers.ModelSerializer):
    # For GET requests, add username to output
    username = serializers.SerializerMethodField(read_only=True)
    
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return None
    
    class Meta:
        model = AuditLog
        fields = ['log_id', 'user_id', 'username', 'action', 'timestamp', 'ip_address']
        read_only_fields = ['log_id', 'timestamp', 'username']