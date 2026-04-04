from fastapi import FastAPI
from typing import List, Optional, TypedDict
from models import User, Account, AccountResponse


app = FastAPI()

temp_db = [
    {
        'id': 1,
        'name': 'Основной счёт',
        'currency': 'EUR',
        'balance': 1250.50,
        'created_at': '2026-04-01T10:00:00',
        'user': {
            'id': 1,
            'email': 'user1@example.com',
            'password_hash': '$2a$10$IM0i/PTV2oC6WcVbk1kqVOpgr5YoPhFFH3LXCiRQwQfye0FogUCvm',
            'first_name': 'Иван',
            'middle_name': 'Иванович',
            'last_name': 'Петров',
            'created_at': '2026-03-22T10:00:00',
            'updated_at': '2026-03-22T10:00:00',
        }
    },
    {
        'id': 2,
        'name': 'Наличные',
        'currency': 'RUB',
        'balance': 300.00,
        'created_at': '2026-04-02T12:30:00',
        'user': {
            'id': 1,
            'email': 'user1@example.com',
            'password_hash': '$2a$10$IM0i/PTV2oC6WcVbk1kqVOpgr5YoPhFFH3LXCiRQwQfye0FogUCvm',
            'first_name': 'Иван',
            'middle_name': 'Иванович',
            'last_name': 'Петров',
            'created_at': '2026-03-22T10:00:00',
            'updated_at': '2026-03-22T10:00:00',
        }
    }
]

'''
ACCOUNTS

`POST /accounts` — создать счёт
`GET /accounts` — получить список счетов
`GET /accounts/{id}` — получить конкретный счёт
`PATCH /accounts/{id}` — обновить счёт
`DELETE /accounts/{id}` — удалить счёт
'''

@app.get('/')
def hello():
    return 'Hello!'


@app.get('/accouts')
def accounts_list() -> List[Account]:
    '''
    Получение всех счетов
    '''

    return temp_db


@app.get('/accounts/{id}')
def accounts_list(account_id: int) -> Account:
    '''
    Получение счёта по id
    '''

    return [account for account in temp_db if account.get('id') == account_id]


@app.post('/accounts')
def create_account(account: Account) -> AccountResponse:
    '''
    Создание счёта
    '''

    temp_db.append(account)

    return {
        'status': 200,
        'data': account
    }


@app.patch('/accounts/{id}')
def update_account(account_id: int, account_data: Account) -> AccountResponse:
    '''
    Частичное обновление данных счёта
    '''

    for i, account in enumerate(temp_db):
        if account.get('id') == account_id:
            for key, value in account_data.items():
                if key == 'id':
                    continue

                if key == 'user' and isinstance(value, dict):
                    account['user'] = account_data
                else:
                    account[key] = value

            return {
                'status': 200,
                'data': account
            }

    return {
        'status': 404,
        'message': 'account not found'
    }



@app.delete('/accounts/{id}')
def delete_account(account_id: int) -> AccountResponse:
    '''
    Удаление счёта по id
    '''

    for i, account in enumerate(temp_db):
        if account.get('id') == account_id:
            temp_db.pop(i)
            break

    return {
        'status': 201,
        'message': 'deleted'
    }
