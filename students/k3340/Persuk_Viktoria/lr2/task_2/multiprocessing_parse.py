"""
Задача 2 — Параллельный парсинг с помощью процессов (multiprocessing).

Каждый URL обрабатывается в отдельном процессе. У каждого процесса своя
память, поэтому движок БД (engine) нельзя передать между процессами —
его нужно создавать заново внутри функции.
"""

import multiprocessing
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

# Подключаем пути к lr1 и lr2
parent_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(parent_dir, '../../lr1/app')
sys.path.append(models_dir)
from models.category import Category

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Список сайтов о финансах для парсинга
URLS = [
    'https://www.dominsoft.ru/articles_temp.php?p=artdb1',
    'https://www.banki.ru/news/daytheme/?id=11003288',
    'https://www.rippling.com/blog/business-expense-categories',
]


def parse_and_save(url: str) -> None:
    """Загружает страницу, извлекает <title> и сохраняет запись в таблицу category.

    Функция выполняется в отдельном процессе. Движок создаётся здесь,
    потому что объекты SQLAlchemy engine нельзя сериализовать и передать
    между процессами через pickle.
    """
    # Загружаем .env внутри процесса — каждый процесс стартует с чистого листа
    load_dotenv(os.path.join(parent_dir, '../.env'))
    db_url = os.getenv('DB_ADMIN')
    if not db_url:
        print(f'[Multiprocessing] DB_ADMIN не задан, пропускаем {url}')
        return

    # Создаём движок внутри функции — у каждого процесса свой пул соединений
    local_engine = create_engine(db_url, echo=False)

    try:
        # Синхронный HTTP-запрос с таймаутом 15 секунд
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # бросает исключение при статусе >= 400

        # Парсим HTML и достаём текст тега <title>
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'Unknown'

        # Используем локальный движок — безопасно в отдельном процессе
        with Session(local_engine) as session:
            category = Category(user_id=1, name=title)
            session.add(category)
            session.commit()

        print(f'[Multiprocessing] Сохранено: {title[:70]}')

    except requests.exceptions.Timeout:
        print(f'[Multiprocessing] Таймаут при запросе к {url}')
    except requests.exceptions.RequestException as e:
        print(f'[Multiprocessing] Ошибка сети для {url}: {e}')
    except Exception as e:
        print(f'[Multiprocessing] Неожиданная ошибка для {url}: {e}')
    finally:
        # Закрываем все соединения в пуле, чтобы не было утечек
        local_engine.dispose()


if __name__ == '__main__':
    start = time.perf_counter()

    # Pool.map() распределяет список URL по процессам
    # На macOS spawn-метод используется по умолчанию, поэтому guard __main__ обязателен
    with multiprocessing.Pool(processes=len(URLS)) as pool:
        pool.map(parse_and_save, URLS)

    elapsed = time.perf_counter() - start
    print(f'\n[Multiprocessing] Время выполнения: {elapsed:.2f} сек')
