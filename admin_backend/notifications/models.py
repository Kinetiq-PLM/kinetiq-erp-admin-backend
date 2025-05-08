from django.db import models

class NotificationsStatusEnum(models.TextChoices):
    READ = 'read', 'Read'
    UNREAD = 'unread', 'Unread'
    DELETED = 'deleted', 'Deleted'

class Notifications(models.Model):
    notifications_id = models.CharField(max_length=255, primary_key=True)
    module = models.CharField(max_length=255)
    to_user_id = models.CharField(max_length=255)
    message = models.TextField()
    notifications_status = models.CharField(
        max_length=10,
        choices=NotificationsStatusEnum.choices,
        default=NotificationsStatusEnum.UNREAD
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"admin"."notifications"'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification {self.notifications_id} to user {self.to_user_id}"