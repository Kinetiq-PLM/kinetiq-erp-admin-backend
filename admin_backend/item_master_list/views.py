from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Assets, Policies, Vendor, Products, RawMaterials, ItemMasterData
from .serializers import (
    AssetsSerializer, PoliciesSerializer, VendorSerializer,
    ProductsSerializer, RawMaterialsSerializer, ItemMasterDataSerializer,
    PolicyChoiceSerializer, VendorChoiceSerializer
)

class AssetsViewSet(viewsets.ModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['asset_id', 'asset_name', 'serial_no']
    ordering_fields = ['asset_name', 'purchase_date', 'purchase_price']
    ordering = ['asset_name']  # Default ordering
    
    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class PoliciesViewSet(viewsets.ModelViewSet):
    queryset = Policies.objects.all()
    serializer_class = PoliciesSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['policy_id', 'policy_name', 'description']
    ordering_fields = ['policy_name', 'effective_date', 'status']
    ordering = ['policy_name']  # Default ordering
    

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['vendor_code', 'vendor_name', 'contact_person']
    # ordering_fields = ['vendor_name', 'status']
    # ordering = ['vendor_name']  # Default ordering

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_id', 'product_name', 'description', 'batch_no']
    ordering_fields = ['product_name', 'selling_price', 'stock_level', 'item_status']
    ordering = ['product_name']  # Default ordering

    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class RawMaterialsViewSet(viewsets.ModelViewSet):
    queryset = RawMaterials.objects.all()
    serializer_class = RawMaterialsSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['material_id', 'material_name', 'description']
    ordering_fields = ['material_name', 'cost_per_unit', 'unit_of_measure']
    ordering = ['material_name']  # Default ordering

    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class ItemMasterDataViewSet(viewsets.ModelViewSet):
    queryset = ItemMasterData.objects.all()
    serializer_class = ItemMasterDataSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item_id', 'item_name', 'item_type', 'preferred_vendor']
    ordering_fields = ['item_name', 'item_type', 'item_status', 'manage_item_by']
    ordering = ['item_name']  # Default ordering
    
    
    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()