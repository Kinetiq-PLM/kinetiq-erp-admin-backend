from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Currency
from .serializers import CurrencySerializer
from .exchange_rates import ExchangeRateService
from .tasks import update_currency_exchange_rates 

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
    
    @action(detail=False, methods=['post'])
    def update_rates(self, request):
        """API endpoint to manually trigger exchange rate updates"""
        # Run synchronously since you're having Celery issues
        success = ExchangeRateService.update_exchange_rates()
        
        if success:
            return Response({
                "message": "Exchange rates updated successfully"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Failed to update exchange rates"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)