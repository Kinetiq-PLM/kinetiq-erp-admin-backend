from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
import requests
import json
import logging

from .models import Policies
from .serializers import PoliciesSerializer, PolicyDocumentUploadSerializer

# Set up logging
logger = logging.getLogger(__name__)

class PoliciesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Policies
    """
    queryset = Policies.objects.exclude(policy_name__startswith='ARCHIVED_')
    serializer_class = PoliciesSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['policy_id', 'policy_name', 'description']
    ordering_fields = ['policy_name', 'description', 'policy_id', 'effective_date', 'status']
    ordering = ['policy_name']

    def create(self, request, *args, **kwargs):
        """
        Create a new policy
        """
        # Log the incoming data for debugging
        logger.debug(f"Create policy request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing policy
        """
        # Log the incoming data for debugging
        logger.debug(f"Update policy request data: {request.data}")
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_document(self, request, pk=None):
        """
        Upload a document to a policy and store its S3 URL
        """
        policy = self.get_object()
        
        # Debug logging
        logger.info(f"Upload document request for policy {pk}")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Request FILES: {request.FILES}")
        
        serializer = PolicyDocumentUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES.get('file')
        if not file:
            logger.error("No file provided in request")
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Log file details
            logger.info(f"Processing file upload: {file.name}, size: {file.size}, content_type: {file.content_type}")
            
            # Get presigned URL from S3 service
            presign_response = requests.post(
                'https://s9v4t5i8ej.execute-api.ap-southeast-1.amazonaws.com/dev/api/upload-to-s3/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({
                    'filename': file.name,
                    'directory': 'Administration/Policies',
                    'contentType': file.content_type or 'application/octet-stream',  # Provide fallback content type
                })
            )
            
            # Log the presign response status
            logger.info(f"Presign response status: {presign_response.status_code}")
            
            # If there's an error in the presign request, log it
            if presign_response.status_code != 200:
                logger.error(f"Presign error response: {presign_response.text}")
                
            presign_response.raise_for_status()
            presign_data = presign_response.json()

            # Log the presigned URL details (excluding sensitive parts)
            logger.info(f"Got presigned URL for file {file.name}")

            upload_url = presign_data['uploadUrl']
            file_url = presign_data['fileUrl']

            # Upload file to S3 using presigned URL
            upload_response = requests.put(
                upload_url,
                headers={'Content-Type': file.content_type or 'application/octet-stream'},
                data=file.read()
            )
            
            # Log the upload response status
            logger.info(f"S3 upload response status: {upload_response.status_code}")
            
            # If there's an error in the upload, log it
            if upload_response.status_code != 200:
                logger.error(f"S3 upload error response: {upload_response.text}")
                
            upload_response.raise_for_status()

            # Update policy with the file URL
            policy.policy_document = file_url
            policy.save()

            # Return success response
            policy_serializer = PoliciesSerializer(policy)
            return Response(
                {'message': 'Document uploaded successfully', 'policy': policy_serializer.data},
                status=status.HTTP_200_OK
            )

        except requests.RequestException as e:
            logger.error(f"API request failed during file upload: {str(e)}")
            return Response({'error': 'File upload failed', 'details': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        """
        Override the default destroy method to 'archive' policies
        """
        if not instance.policy_name.startswith('ARCHIVED_'):
            instance.policy_name = f'ARCHIVED_{instance.policy_name}'
            instance.save()

    @action(detail=False, methods=['get'])
    def archived(self, request):
        """
        Return all archived policies
        """
        archived_policies = Policies.objects.filter(policy_name__startswith='ARCHIVED_')

        for backend in self.filter_backends:
            archived_policies = backend().filter_queryset(request, archived_policies, self)

        page = self.paginate_queryset(archived_policies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(archived_policies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):
        """
        Restore an archived policy
        """
        policy = get_object_or_404(Policies, pk=pk)
        if policy.policy_name.startswith('ARCHIVED_'):
            policy.policy_name = policy.policy_name[len('ARCHIVED_'):]
            policy.save()

        serializer = self.get_serializer(policy)
        return Response(serializer.data)