from django.contrib import admin
from .models import Policies
# Register your models here.

@admin.register(Policies)
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ('policy_id', 'policy_name', 'description', 'effective_date', 'status')
