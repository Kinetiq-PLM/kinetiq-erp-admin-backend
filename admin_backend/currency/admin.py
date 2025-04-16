from django.contrib import admin
from .models import Currency
# Register your models here.

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_id', 'currency_name', 'exchange_rate', 'is_active')
