from django.contrib import admin
from .models import Policies, PolicyDocument

@admin.register(Policies)
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ('policy_id', 'policy_name', 'status', 'effective_date')
    search_fields = ('policy_id', 'policy_name')

@admin.register(PolicyDocument)
class PolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ('policy', 'uploaded_at')
