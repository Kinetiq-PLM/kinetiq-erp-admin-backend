from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Policies
from .serializers import PoliciesSerializer
from rest_framework.decorators import action

class PoliciesViewSet(viewsets.ModelViewSet):
    queryset = Policies.objects.all()
    serializer_class = PoliciesSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['policy_id', 'policy_name']
    ordering_fields = ['policy_name', 'effective_date']
    ordering = ['policy_name']  # Default ordering

    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()
        
    def perform_destroy(self, instance):
        instance.delete()
