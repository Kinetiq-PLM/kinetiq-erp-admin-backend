# serializers.py
from django.conf import settings
from rest_framework import serializers
from .models import Policies, PolicyDocument

class PoliciesSerializer(serializers.ModelSerializer):
    document = serializers.FileField(write_only=True, required=False)
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Policies
        fields = ['policy_id', 'policy_name', 'description', 'effective_date', 'status', 'document', 'document_url']
        read_only_fields = ['policy_id', 'document_url']
    
    def get_document_url(self, obj):
        try:
            doc = PolicyDocument.objects.filter(policy_id=obj.policy_id).first()
            if doc and doc.document:
                if settings.DEBUG:
                    # For development, return the actual file path
                    return f"/media/{doc.document.name}"
                else:
                    request = self.context.get('request')
                    if request:
                        return request.build_absolute_uri(doc.document.url)
        except Exception as e:
            print(f"Error getting document URL: {e}")
        return None

    def create(self, validated_data):
        # Extract document data before creating the policy
        document_file = validated_data.pop('document', None)
        
        # Generate a unique policy_id
        import uuid
        policy_id = f"ADMIN-POLICY-{uuid.uuid4().hex[:8].upper()}"
        validated_data['policy_id'] = policy_id
        
        # Create the policy - use raw SQL if needed
        policy = Policies.objects.create(**validated_data)
        
        # Create document if provided
        if document_file:
            PolicyDocument.objects.create(policy_id=policy.policy_id, document=document_file)
        
        return policy
    
    def update(self, instance, validated_data):
        # Extract document data before updating the policy
        document_file = validated_data.pop('document', None)
        
        # Update the policy fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create document if provided
        if document_file:
            PolicyDocument.objects.update_or_create(
                policy_id=instance.policy_id,
                defaults={'document': document_file}
            )
        
        return instance