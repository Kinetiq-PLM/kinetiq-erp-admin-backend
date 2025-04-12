from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Currency
from .serializers import CurrencySerializer
from rest_framework.decorators import action

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['currency_id', 'currency_name']
    ordering_fields = ['currency_name', 'valid_from']
    ordering = ['currency_name']  # Default ordering

    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()
        
    def perform_destroy(self, instance):
        instance.delete()