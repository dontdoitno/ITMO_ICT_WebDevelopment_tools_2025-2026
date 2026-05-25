import requests
from fastapi import FastAPI, HTTPException


app = FastAPI(title='Currency Exchange Rate Parser')


@app.post('/parse')
def parse_exchange_rates(base: str = 'USD'):
    """Fetch and return currency exchange rates for a given base currency.

    Args:
        base: Base currency code (e.g. USD, EUR, RUB)

    Returns:
        Exchange rates relative to the base currency

    Raises:
        HTTPException: 500 if the external API request fails
    """
    try:
        response = requests.get(
            f'https://open.er-api.com/v6/latest/{base}',
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            'message': 'Parsing completed',
            'base': data['base_code'],
            'rates': data['rates'],
            'time_last_update': data.get('time_last_update_utc'),
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
