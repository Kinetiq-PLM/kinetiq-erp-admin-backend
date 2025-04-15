# user_manage/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, RolePermission
from .serializers import UserSerializer, RolePermissionSerializer
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    
    # Add built-in search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id', 'first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['created_at', 'first_name', 'last_name', 'email', 'status', 'type']
    ordering = ['first_name']  # Default ordering
    
    def perform_create(self, serializer):
        serializer.save()
            
    def perform_update(self, serializer):
        serializer.save()

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['role_name', 'description']
    ordering_fields = ['role_name', 'permissions']
    ordering = ['role_name']  # Default ordering

    
    def perform_create(self, serializer):
            serializer.save()
            
    def perform_update(self, serializer):
            serializer.save()
            
    def perform_destroy(self, instance):
            instance.delete()