from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Assets, Policies, Vendor, Products, RawMaterials, ItemMasterData
from .serializers import (
    AssetsSerializer, PoliciesSerializer, VendorSerializer,
    ProductsSerializer, RawMaterialsSerializer, ItemMasterDataSerializer,
    PolicyChoiceSerializer, VendorChoiceSerializer
)
from django.shortcuts import get_object_or_404

class AssetsViewSet(viewsets.ModelViewSet):
    queryset = Assets.objects.exclude(asset_name__startswith='ARCHIVED_')
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
        if not instance.asset_name.startswith('ARCHIVED_'):
            instance.asset_name = f'ARCHIVED_{instance.asset_name}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_assets = Assets.objects.filter(asset_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_assets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_assets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):    
        asset_id = pk
        asset = get_object_or_404(Assets, pk=asset_id)

        if asset.asset_name.startswith('ARCHIVED_'):
            asset.asset_name = asset.asset_name[9:]
            asset.save()

        serializer = self.get_serializer(asset)
        return Response(serializer.data)

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
    queryset = Products.objects.exclude(product_name__startswith='ARCHIVED_')
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
        if not instance.product_name.startswith('ARCHIVED_'):
            instance.product_name = f'ARCHIVED_{instance.product_name}'
            instance.save()
    
    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_products = Products.objects.filter(product_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):    
        product_id = pk
        product = get_object_or_404(Products, pk=product_id)

        if product.product_name.startswith('ARCHIVED_'):
            product.product_name = product.product_name[9:]
            product.save()

        serializer = self.get_serializer(product)
        return Response(serializer.data)

class RawMaterialsViewSet(viewsets.ModelViewSet):
    queryset = RawMaterials.objects.exclude(material_name__startswith='ARCHIVED_')
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
        if not instance.material_name.startswith('ARCHIVED_'):
            instance.material_name = f'ARCHIVED_{instance.material_name}'
            instance.save()
    
    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_materials = RawMaterials.objects.filter(material_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_materials)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_materials, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):    
        material_id = pk
        material = get_object_or_404(RawMaterials, pk=material_id)

        if material.material_name.startswith('ARCHIVED_'):
            material.material_name = material.material_name[9:]
            material.save()

        serializer = self.get_serializer(material)
        return Response(serializer.data)

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
        if not instance.item_name.startswith('ARCHIVED_'):
            instance.item_name = f'ARCHIVED_{instance.item_name}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_items = ItemMasterData.objects.filter(item_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):    
        item_id = pk
        item = get_object_or_404(ItemMasterData, pk=item_id)

        if item.item_name.startswith('ARCHIVED_'):
            item.item_name = item.item_name[9:]
            item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)