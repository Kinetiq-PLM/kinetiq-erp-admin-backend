# policies/views.py
import os
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Policies, PolicyDocument
from .serializers import PoliciesSerializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

class PoliciesViewSet(viewsets.ModelViewSet):
    queryset = Policies.objects.exclude(policy_name__startswith='ARCHIVED_')
    serializer_class = PoliciesSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['policy_id', 'policy_name']
    ordering_fields = ['policy_name', 'effective_date']
    ordering = ['policy_name']  # Default ordering
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(detail=True, methods=['get'])
    def download_document(self, request, pk=None):
        policy = self.get_object()
        try:
            policy_document = PolicyDocument.objects.get(policy_id=policy.policy_id)
            if policy_document.document:
                return FileResponse(
                    policy_document.document.open(),
                    as_attachment=True,
                    filename=f"{policy.policy_name}_document.pdf"
                )
        except PolicyDocument.DoesNotExist:
            pass
            
        return Response(
            {"error": "No document found"},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_document(self, request, pk=None):
        policy = self.get_object()
        if 'document' in request.FILES:
            policy_document, created = PolicyDocument.objects.update_or_create(
                policy_id=policy.policy_id,
                defaults={'document': request.FILES['document']}
            )
            serializer = self.get_serializer(policy, context={'request': request})
            return Response(serializer.data)
        return Response(
            {"error": "No document provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_destroy(self, instance):
        # Instead of deleting, prefix the policy name with 'ARCHIVED_'
        if not instance.policy_name.startswith('ARCHIVED_'):
            instance.policy_name = f'ARCHIVED_{instance.policy_name}'
            instance.save()
        # Note: We don't delete the associated document

    @action(detail=False, methods=['get'])
    def archived(self, request):
        archived_policies = Policies.objects.filter(policy_name__startswith='ARCHIVED_')
        page = self.paginate_queryset(archived_policies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(archived_policies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):
        from django.shortcuts import get_object_or_404
        
        # Get the policy directly from the database, bypassing the filtered queryset
        policy_id = pk
        policy = get_object_or_404(Policies, policy_id=policy_id)
        
        if policy.policy_name.startswith('ARCHIVED_'):
            policy.policy_name = policy.policy_name[9:]  # Remove "ARCHIVED_" prefix
            policy.save()
        
        serializer = self.get_serializer(policy)
        return Response(serializer.data)

    def debug_file_path(request, filename):
        try:
            document = PolicyDocument.objects.filter(document__contains=filename).first()
            if document:
                path = document.document.path
                exists = os.path.exists(path)
                readable = os.access(path, os.R_OK)
                return HttpResponse(f"File path: {path}\nExists: {exists}\nReadable: {readable}")
            return HttpResponse("File not found in database")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")