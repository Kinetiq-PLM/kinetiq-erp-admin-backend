# currency/exchange_rates.py
import requests
from datetime import date
from decimal import Decimal
import logging

from .models import Currency

logger = logging.getLogger(__name__)

class ExchangeRateService:
    """Service to fetch and update currency exchange rates"""
    
    # Free exchange rate API that doesn't require authentication
    BASE_URL = 'https://open.er-api.com/v6/latest/PHP' 
    BACKUP_URL = 'https://open.er-api.com/v6/latest/PHP'  
    
    @classmethod
    def fetch_latest_rates(cls):
        """Fetch latest exchange rates from free API services"""
        apis = [
            {'url': cls.BASE_URL, 'params': {'base': 'PHP'}},
            {'url': cls.BACKUP_URL, 'params': {}}
        ]
        
        for api in apis:
            try:
                response = requests.get(api['url'], params=api['params'], timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                # Handle different API response structures
                if 'rates' in data or 'conversion_rates' in data:
                    logger.info(f"Successfully fetched rates from {api['url']}")
                    return {
                        'base_code': data.get('base_code', data.get('base', 'PHP')),
                        'rates': data.get('conversion_rates', data.get('rates', {})),
                        'date': data.get('date', date.today().isoformat())
                    }
                
                logger.warning(f"API response format not recognized: {api['url']}")
                
            except Exception as e:
                logger.warning(f"Failed to fetch rates from {api['url']}: {str(e)}")
        
        # If we get here, all APIs failed
        logger.error("All exchange rate APIs failed")
        return None
    
    @classmethod
    def update_exchange_rates(cls):
        """Update exchange rates in the database"""
        rates_data = cls.fetch_latest_rates()
        if not rates_data:
            logger.error("Failed to update exchange rates: No data received")
            return False
        
        success_count = 0
        unchanged_count = 0
        error_count = 0
        
        # Process each currency rate
        for currency_code, rate in rates_data['rates'].items():
            try:
                decimal_rate = Decimal(str(rate))
                currency_name = f"{currency_code}"
                
                # Try to get existing currency record by currency_name instead of currency_id
                try:
                    # Look for a match by currency_name rather than currency_id
                    current_currency = Currency.objects.filter(currency_name=currency_name).first()
                    
                    if current_currency:
                        # Currency exists, check if rate has changed
                        if current_currency.exchange_rate != decimal_rate:
                            # Update existing currency with new rate
                            logger.info(f"Rate changed for {currency_name}: {current_currency.exchange_rate} -> {decimal_rate}")
                            current_currency.exchange_rate = decimal_rate
                            current_currency.save()
                            success_count += 1
                        else:
                            # Rate hasn't changed, no need to update
                            logger.debug(f"Rate unchanged for {currency_name}: {decimal_rate}")
                            unchanged_count += 1
                    else:
                        # Currency doesn't exist, create a new one
                        Currency.objects.create(
                            currency_name=currency_name,
                            exchange_rate=decimal_rate,
                            is_active=Currency.ACTIVE
                        )
                        success_count += 1
                        logger.info(f"Created new record for {currency_name}: {decimal_rate}")
                        
                except Exception as e:
                    logger.error(f"Error finding/updating currency {currency_name}: {str(e)}")
                    
                    # Attempt to create if there was an error finding
                    try:
                        Currency.objects.create(
                            currency_name=currency_name,
                            exchange_rate=decimal_rate,
                            is_active=Currency.ACTIVE
                        )
                        success_count += 1
                        logger.info(f"Created new record for {currency_name} after lookup error: {decimal_rate}")
                    except Exception as create_error:
                        logger.error(f"Failed to create currency {currency_name}: {str(create_error)}")
                        error_count += 1
                
            except Exception as e:
                logger.error(f"Error processing {currency_code}: {str(e)}")
                error_count += 1
        
        logger.info(f"Exchange rate update completed: {success_count} updated, {unchanged_count} unchanged, {error_count} failed")
        return success_count > 0 or unchanged_count > 0