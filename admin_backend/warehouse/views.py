# warehouse/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Warehouse, WarehouseManagers
from .serializers import WarehouseSerializer, WarehouseManagerSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class WarehouseManagerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting warehouse managers.
    """
    queryset = WarehouseManagers.objects.filter(role_id='ADMIN-ROLE-2025-ce28ef')
    serializer_class = WarehouseManagerSerializer
    
    def get_queryset(self):
        """
        Optionally filter warehouse managers by role_id
        """
        queryset = WarehouseManagers.objects.filter(role_id='ADMIN-ROLE-2025-ce28ef')
        role_id = self.request.query_params.get('role_id', None)
        if role_id is not None:
            queryset = queryset.filter(role_id=role_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def choices(self, request):
        """
        Return a list of managers formatted for dropdown choices with employee_id as the value
        """
        queryset = self.get_queryset()
        choices = [
            {
                'value': manager.employee_id,
                'display': f"{manager.first_name} {manager.last_name}"
            }
            for manager in queryset
        ]
        return Response(choices)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.exclude(warehouse_location__startswith='ARCHIVED_')
    serializer_class = WarehouseSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['warehouse_id', 'warehouse_name', 'warehouse_location', 'warehouse_manager', 'contact_no']
    ordering_fields = ['warehouse_id', 'warehouse_name', 'warehouse_location', 'warehouse_manager', 'contact_no']
    ordering = ['warehouse_name']  # Default ordering

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