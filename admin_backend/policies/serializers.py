from rest_framework import serializers
from .models import Policies

class PoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policies
        fields = ['policy_id', 'policy_name', 'description', 'effective_date', 'status']
        read_only_fields = ['policy_id']

    def create(self, validated_data):
        # Generate a unique policy_id
        import uuid
        policy_id = f"ADMIN-POLICY-{uuid.uuid4().hex[:8].upper()}"
        validated_data['policy_id'] = policy_id
        return super().create(validated_data)
    
    