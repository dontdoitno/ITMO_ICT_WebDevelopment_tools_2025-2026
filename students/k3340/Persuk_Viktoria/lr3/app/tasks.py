import os

import requests

from celery_app import celery_app


PARSER_URL = os.getenv('PARSER_URL', 'http://parser:8001')


@celery_app.task(name='tasks.parse_exchange_rates_task')
def parse_exchange_rates_task(base: str = 'USD') -> dict:
    """Celery task that calls the parser service to fetch exchange rates.

    Args:
        base: Base currency code (e.g. USD, EUR, RUB)

    Returns:
        Parsed exchange rate data from the parser service
    """
    response = requests.post(
        f'{PARSER_URL}/parse',
        params={'base': base},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
