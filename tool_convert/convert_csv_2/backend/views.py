from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from .models import ProcessingHistory
from .serializers import FileUploadSerializer
import pandas as pd
import uuid
import os

class FileUploadView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Lưu file upload
        uploaded_file = serializer.validated_data['file']
        file_ext = os.path.splitext(uploaded_file.name)[1]
        new_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Tạo bản ghi lịch sử
        history = ProcessingHistory.objects.create(
            user=request.user,
            original_filename=uploaded_file.name,
            input_file=uploaded_file,
            status='PENDING'
        )
        
        # Xử lý bất đồng bộ với Celery
        process_file.delay(history.id)
        
        return Response(
            {"message": "File đang được xử lý", "history_id": history.id},
            status=status.HTTP_202_ACCEPTED
        )