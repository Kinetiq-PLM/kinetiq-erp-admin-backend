from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['currency_id', 'currency_name', 'exchange_rate', 'is_active']
        read_only_fields = ['currency_id']

    # def create(self, validated_data):
    #     # Generate a unique currency_id
    #     import uuid
    #     currency_id = f"ADMIN-CUR-{uuid.uuid4().hex[:8].upper()}"
    #     validated_data['currency_id'] = currency_id
    #     return super().create(validated_data)