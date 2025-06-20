from django.db import models
from django.contrib.postgres.fields import JSONField

class JiraMapping(models.Model):
    MAPPING_TYPES = [
        ('USER', 'Jira User'),
        ('PROJECT', 'Jira Project'),
        ('ASSIGNMENT', 'Assignment Reference'),
        ('HOSTNAME', 'Hostname-Project Reference')
    ]
    
    key = models.CharField(max_length=255, db_index=True)
    value = JSONField()
    mapping_type = models.CharField(max_length=20, choices=MAPPING_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProcessingHistory(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    input_file = models.FileField(upload_to='uploads/input/')
    output_file = models.FileField(upload_to='uploads/output/', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    logs = models.TextField(blank=True)