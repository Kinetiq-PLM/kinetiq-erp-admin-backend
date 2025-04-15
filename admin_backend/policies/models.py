from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.policy_name
    
    class Meta:
        db_table = '"admin"."policies"'
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        managed = False

class PolicyDocument(models.Model):
    policy_id = models.CharField(primary_key=True, max_length=255)
    document = models.FileField(upload_to='policy_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Document for {self.policy_id}"
    
    def policy(self):
        try:
            return Policies.objects.get(policy_id=self.policy_id)
        except Policies.DoesNotExist:
            return None
    
    class Meta:
        managed = False  # Make this model unmanaged as well
        db_table = 'policies_policydocument'
