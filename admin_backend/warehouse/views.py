from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Warehouse
from .serializers import WarehouseSerializer
from rest_framework.decorators import action

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
        instance.delete()