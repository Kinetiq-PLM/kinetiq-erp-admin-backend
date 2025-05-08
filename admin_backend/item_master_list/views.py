
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vendor, ItemMasterData
from .serializers import (
    VendorSerializer, ItemMasterDataSerializer
)
from django.shortcuts import get_object_or_404

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(status='Approved')
    serializer_class = VendorSerializer
    http_method_names = ['get']


class ItemMasterDataViewSet(viewsets.ModelViewSet):
    queryset = ItemMasterData.objects.exclude(item_name__startswith='ARCHIVED_')
    serializer_class = ItemMasterDataSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  # Added 'post' method
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item_id', 'item_name', 'item_description', 'item_type',
                 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor',
                 'purchasing_uom', 'items_per_purchase_unit',
                 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit',
                 'sales_quantity_per_package']
    ordering_fields = ['item_id', 'item_name', 'item_description', 'item_type',
                 'unit_of_measure', 'item_status', 'manage_item_by', 'preferred_vendor',
                 'preferred_vendor', 'purchasing_uom', 'items_per_purchase_unit',
                 'purchase_quantity_per_package', 'sales_uom', 'items_per_sale_unit',
                 'sales_quantity_per_package']
    ordering = ['item_name']  # Default ordering
    
    def perform_destroy(self, instance):
        if not instance.item_name.startswith('ARCHIVED_'):
            instance.item_name = f'ARCHIVED_{instance.item_name}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_items = ItemMasterData.objects.filter(item_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_items)

        # Apply filter backends manually
        for backend in list(self.filter_backends):
            archived_items = backend().filter_queryset(self.request, archived_items, self)

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