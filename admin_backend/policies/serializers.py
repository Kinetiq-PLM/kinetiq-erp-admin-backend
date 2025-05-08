from rest_framework import serializers
from .models import Policies

class PoliciesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Policies model
    """
    # Make policy_document read-only in the main serializer
    policy_document = serializers.URLField(read_only=True)
    
    class Meta:
        model = Policies
        fields = ['policy_id', 'policy_name', 'description', 'effective_date', 'status', 'policy_document']
        read_only_fields = ['policy_id', 'policy_document']

    def create(self, validated_data):
        # Generate a unique vendor_code
        import uuid
        item_id = f"ADMIN-POLICY-{uuid.uuid4().hex[:8].upper()}"
        validated_data['item_id'] = item_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data)

class PolicyDocumentUploadSerializer(serializers.Serializer):
    """
    Serializer for handling file uploads.
    This will prompt for file input in API forms or frontend.
    """
    file = serializers.FileField(required=True)