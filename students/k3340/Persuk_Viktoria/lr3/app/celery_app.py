import os

from celery import Celery


REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery_app = Celery(
    'finance_app',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks'],
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# периодические задачи (Celery Beat) - сбор курса валюи USD раз в час
celery_app.conf.beat_schedule = {
    'fetch-usd-rates-every-hour': {
        'task': 'tasks.parse_exchange_rates_task',
        'schedule': 3600.0,
        'args': ('USD',),
    },
}
