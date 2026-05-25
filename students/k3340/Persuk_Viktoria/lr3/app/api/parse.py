import os

import redis
import requests
from fastapi import APIRouter, HTTPException

from celery_app import celery_app
from tasks import parse_exchange_rates_task


PARSER_URL = os.getenv('PARSER_URL', 'http://parser:8001')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
TASKS_KEY = 'parse_task_ids'

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

router = APIRouter(
    prefix='/parse',
    tags=['parser'],
)


@router.post('/sync')
def parse_sync(base: str = 'USD'):
    """Synchronously call the parser service and return exchange rates.

    Args:
        base: Base currency code (e.g. USD, EUR, RUB)

    Returns:
        Exchange rate data from the parser service

    Raises:
        HTTPException: 500 if the parser service request fails
    """
    try:
        response = requests.post(
            f'{PARSER_URL}/parse',
            params={'base': base},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/async')
def parse_async(base: str = 'USD'):
    """Queue an async Celery task to fetch exchange rates.

    Args:
        base: Base currency code (e.g. USD, EUR, RUB)

    Returns:
        Task ID and status message
    """
    task = parse_exchange_rates_task.delay(base)
    redis_client.sadd(TASKS_KEY, task.id)
    return {'task_id': task.id, 'message': 'Task queued successfully'}


@router.get('/tasks')
def list_tasks():
    """List all queued task IDs with their current status.

    Returns:
        List of task objects with id and status
    """
    task_ids = redis_client.smembers(TASKS_KEY)
    tasks = []

    for task_id in task_ids:
        task = celery_app.AsyncResult(task_id)
        tasks.append({'task_id': task_id, 'status': task.state.lower()})

    return tasks


@router.get('/task/{task_id}')
def get_task_result(task_id: str):
    """Check the status and result of an async parsing task.

    Args:
        task_id: Celery task ID returned by POST /parse/async

    Returns:
        Task status and result (if completed)
    """
    task = celery_app.AsyncResult(task_id)

    if task.state == 'PENDING':
        return {'task_id': task_id, 'status': 'pending'}
    elif task.state == 'SUCCESS':
        return {'task_id': task_id, 'status': 'success', 'result': task.result}
    elif task.state == 'FAILURE':
        return {'task_id': task_id, 'status': 'failed', 'error': str(task.result)}
    else:
        return {'task_id': task_id, 'status': task.state}
