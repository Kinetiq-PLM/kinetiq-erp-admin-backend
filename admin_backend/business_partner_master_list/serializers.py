from rest_framework import serializers
from .models import BusinessPartnerMaster

class BusinessPartnerMasterSearializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartnerMaster
        fields = ['partner_id', 'partner_name', 'category', 'contact_info']
        read_only_fields = ['partner_id']

    def create(self, validated_data):
        # Generate a unique partner_id
        import uuid
        partner_id = f"ADMIN-PARTNER-{uuid.uuid4().hex[:8].upper()}"
        validated_data['partner_id'] = partner_id
        return super().create(validated_data)

