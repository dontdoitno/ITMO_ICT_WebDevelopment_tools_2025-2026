import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

# Подключаем пути к lr1 и lr2, чтобы использовать модели и движок из той же БД
parent_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(parent_dir, '../../lr1/app')
sys.path.append(models_dir)
from models.category import Category

connector_dir = os.path.join(parent_dir, '..')
sys.path.append(connector_dir)
from connector import engine

from sqlmodel import Session

# Список сайтов о финансах для парсинга
URLS = [
    'https://www.dominsoft.ru/articles_temp.php?p=artdb1',
    'https://www.banki.ru/news/daytheme/?id=11003288',
    'https://www.rippling.com/blog/business-expense-categories',
]


def parse_and_save(url: str) -> None:
    """Загружает страницу, извлекает <title> и сохраняет запись в таблицу category.

    requests.get() блокирует поток, но GIL освобождается на время I/O —
    остальные потоки продолжают выполняться параллельно.
    """
    try:
        # Синхронный HTTP-запрос с таймаутом 15 секунд
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # бросает исключение при статусе >= 400

        # Парсим HTML и достаём текст тега <title>
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'Unknown'

        # Каждый поток создаёт свою сессию — общий движок (engine) это поддерживает
        with Session(engine) as session:
            category = Category(user_id=1, name=title)
            session.add(category)
            session.commit()

        print(f'[Threads] Сохранено: {title[:70]}')

    except requests.exceptions.Timeout:
        print(f'[Threads] Таймаут при запросе к {url}')
    except requests.exceptions.RequestException as e:
        print(f'[Threads] Ошибка сети для {url}: {e}')
    except Exception as e:
        print(f'[Threads] Неожиданная ошибка для {url}: {e}')


if __name__ == '__main__':
    start = time.perf_counter()

    # ThreadPoolExecutor запускает parse_and_save в отдельных потоках параллельно
    with ThreadPoolExecutor(max_workers=len(URLS)) as executor:
        executor.map(parse_and_save, URLS)

    elapsed = time.perf_counter() - start
    print(f'\n[Threads] Время выполнения: {elapsed:.2f} сек')
