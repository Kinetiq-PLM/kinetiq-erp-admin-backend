from django.db import models
from django.contrib.auth.models import User
import uuid

class AuditLog(models.Model):
    log_id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(User, models.DO_NOTHING, db_index=True, blank=True, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # Added index
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = '"admin"."audit_log"'
        indexes = [
            models.Index(fields=['timestamp', 'user']),  # Common query pattern
            models.Index(fields=['action']),  # For search optimization
        ]
        
    @staticmethod
    def generate_log_id():
        return f"LOG-{uuid.uuid4().hex[:8].upper()}"