# currency/management/commands/update_exchange_rates.py
from django.core.management.base import BaseCommand
from currency.exchange_rates import ExchangeRateService
import time

class Command(BaseCommand):
    help = 'Update currency exchange rates from external API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting exchange rate update...'))
        
        start_time = time.time()
        success = ExchangeRateService.update_exchange_rates()
        end_time = time.time()
        
        duration = end_time - start_time
        
        if success:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully updated exchange rates in {duration:.2f} seconds'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f'Failed to update exchange rates after {duration:.2f} seconds'
            ))