from rest_framework import serializers
from .models import BusinessPartnerMaster, Vendor

class BusinessPartnerMasterSearializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartnerMaster
        fields = ['partner_id', 'employee_id', 'vendor_code', 'customer_id', 'partner_name', 'category', 'contact_info']
        read_only_fields = ['partner_id', 'employee_id', 'vendor_code', 'customer_id']

    def create(self, validated_data):
        # Generate a unique partner_id
        import uuid
        partner_id = f"ADMIN-PARTNER-{uuid.uuid4().hex[:8].upper()}"
        validated_data['partner_id'] = partner_id
        return super().create(validated_data)

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'application_reference', 'vendor_name', 'contact_person', 'status']
        read_only_fields = ['vendor_code']
    
    def create(self, validated_data):
        # Generate a unique vendor_code
        import uuid
        vendor_code = f"ADMIN-VENDOR-{uuid.uuid4().hex[:8].upper()}"
        validated_data['vendor_code'] = vendor_code
        return super().create(validated_data)