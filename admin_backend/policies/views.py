# views.py
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
    queryset = Policies.objects.all()
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
        # Also delete any associated document
        try:
            PolicyDocument.objects.filter(policy_id=instance.policy_id).delete()
        except Exception:
            pass
        instance.delete()

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