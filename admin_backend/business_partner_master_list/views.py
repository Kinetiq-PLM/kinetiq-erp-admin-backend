from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import BusinessPartnerMaster
from .serializers import BusinessPartnerMasterSearializer
from rest_framework.decorators import action

class BusinessPartnerMasterViewSet(viewsets.ModelViewSet):
    queryset = BusinessPartnerMaster.objects.all()
    serializer_class = BusinessPartnerMasterSearializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['partner_id', 'partner_name', 'category', 'contact_info']
    ordering_fields = ['partner_id', 'partner_name', 'category', 'contact_info']
    ordering = ['partner_name']  # Default ordering
