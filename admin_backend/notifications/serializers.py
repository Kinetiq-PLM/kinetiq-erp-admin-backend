from rest_framework import serializers
from .models import Notifications

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['notifications_id', 'module', 'to_user_id', 'message', 'notifications_status', 'created_at']
        read_only_fields = ['notifications_id', 'created_at']