from django.core.management.base import BaseCommand
from currency.exchange_rates import ExchangeRateService

class Command(BaseCommand):
    help = 'Updates currency exchange rates from external API'

    def handle(self, *args, **options):
        self.stdout.write('Updating exchange rates...')
        
        success = ExchangeRateService.update_exchange_rates()
        
        if success:
            self.stdout.write(self.style.SUCCESS('Exchange rates updated successfully!'))
        else:
            self.stdout.write(self.style.ERROR('Failed to update exchange rates.'))