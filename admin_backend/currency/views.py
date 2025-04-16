# currency/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action

from .models import Currency
from .serializers import CurrencySerializer
from .exchange_rates import ExchangeRateService

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing currencies and triggering exchange rate updates
    """
    queryset = Currency.objects.all().order_by('currency_name')
    serializer_class = CurrencySerializer
    http_method_names = ['get', 'post', 'patch']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Cache currency list for 1 hour to improve performance
    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # Allow filtering active currencies
    def get_queryset(self):
        queryset = Currency.objects.all().order_by('currency_name')
        
        # Filter by active status if requested
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            if is_active.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(is_active=Currency.ACTIVE)
            elif is_active.lower() in ['false', '0', 'no']:
                queryset = queryset.filter(is_active=Currency.INACTIVE)
                
        return queryset
    
    @action(detail=False, methods=['post', 'get'], permission_classes=[AllowAny])
    def update_rates(self, request):
        """
        Endpoint to manually trigger exchange rate updates.
        Accessible to all users with both GET and POST methods.
        """
        success = ExchangeRateService.update_exchange_rates()
        
        if success:
            return Response(
                {"message": "Exchange rates updated successfully"}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Failed to update exchange rates. Check server logs for details"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Endpoint to get only active currencies"""
        queryset = Currency.objects.filter(is_active=Currency.ACTIVE).order_by('currency_name')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)