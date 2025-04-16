from celery import shared_task
from .exchange_rates import ExchangeRateService
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_exchange_rates_task():
    """Celery task to update exchange rates daily"""
    logger.info("Running scheduled exchange rate update")
    result = ExchangeRateService.update_exchange_rates()
    if result:
        logger.info("Scheduled exchange rate update completed successfully")
    else:
        logger.error("Scheduled exchange rate update failed")
    return result