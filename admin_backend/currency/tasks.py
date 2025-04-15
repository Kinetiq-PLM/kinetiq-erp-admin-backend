# currency/tasks.py
from celery import shared_task
import logging
from .exchange_rates import ExchangeRateService

logger = logging.getLogger(__name__)

@shared_task
def update_currency_exchange_rates():
    """Celery task to update exchange rates"""
    logger.info("Starting scheduled exchange rate update")
    result = ExchangeRateService.update_exchange_rates()
    if result:
        logger.info("Scheduled exchange rate update completed successfully")
    else:
        logger.error("Scheduled exchange rate update failed")
    return result