from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import BusinessPartnerMaster, Vendor  
from .serializers import BusinessPartnerMasterSearializer, VendorSerializer
from rest_framework.decorators import action

class BusinessPartnerMasterViewSet(viewsets.ModelViewSet):
    queryset = BusinessPartnerMaster.objects.all()
    serializer_class = BusinessPartnerMasterSearializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['partner_id', 'employee_id', 'vendor_code__vendor_name', 'customer_id', 'partner_name']
    ordering_fields = ['partner_id', 'employee_id', 'vendor_code__vendor_name', 'customer_id', 'partner_name']
    ordering = ['partner_name']  # Default ordering
                
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vendor_code', 'application_reference', 'vendor_name', 'contact_person']
    ordering_fields = ['vendor_code', 'application_reference', 'vendor_name', 'contact_person']
    ordering = ['vendor_name']  # Default ordering
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()