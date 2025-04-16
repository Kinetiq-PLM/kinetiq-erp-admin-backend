from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Warehouse
from .serializers import WarehouseSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['warehouse_id', 'warehouse_location', 'stored_materials']
    ordering_fields = ['warehouse_name', 'warehouse_location', 'stored_materials']
    ordering = ['warehouse_location']  # Default ordering

    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()
        
    def perform_destroy(self, instance):
        # Check if already archived
        if not instance.warehouse_location.startswith('ARCHIVED_'):
            instance.warehouse_location = f'ARCHIVED_{instance.warehouse_location}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_warehouses = Warehouse.objects.filter(warehouse_location__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_warehouses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_warehouses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):    
        warehouse_id = pk
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        if warehouse.warehouse_location.startswith('ARCHIVED_'):
            warehouse.warehouse_location = warehouse.warehouse_location[9:]
            warehouse.save()

        serializer = self.get_serializer(warehouse)
        return Response(serializer.data)