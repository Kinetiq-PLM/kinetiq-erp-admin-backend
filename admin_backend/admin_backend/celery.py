import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_backend.settings')

app = Celery('admin_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule the exchange rate update task to run daily at 1:00 AM
app.conf.beat_schedule = {
    'update-exchange-rates-daily': {
        'task': 'currency.tasks.update_exchange_rates_task',
        'schedule': 86400.0,  # 24 hours in seconds
        # Alternatively, use crontab: 
        # 'schedule': crontab(hour=1, minute=0),  # Run daily at 1:00 AM
    },
}