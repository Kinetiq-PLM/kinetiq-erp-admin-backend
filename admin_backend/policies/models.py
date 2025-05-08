from django.db import models

class Policies(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    policy_id = models.CharField(primary_key=True, max_length=255)
    policy_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    # Store URL to document in S3
    policy_document = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.policy_name
    
    class Meta:
        db_table = '"admin"."policies"'
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        managed = False