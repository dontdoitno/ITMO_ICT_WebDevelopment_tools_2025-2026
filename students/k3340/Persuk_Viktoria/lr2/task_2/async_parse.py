"""
Задача 2 — Параллельный парсинг с помощью asyncio (async/await).

asyncio — это однопоточная конкурентность: один поток переключается между
задачами в момент ожидания I/O. Для HTTP используется httpx (async),
для БД — AsyncSession с драйвером asyncpg (postgresql+asyncpg://).
"""

import asyncio
import os
import sys

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Подключаем путь к lr1, чтобы использовать модели из той же БД
parent_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(parent_dir, '../../lr1/app')
sys.path.append(models_dir)
from models.category import Category

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import time

load_dotenv(os.path.join(parent_dir, '../.env'))

# Строка подключения для asyncpg: postgresql -> postgresql+asyncpg
_sync_url = os.getenv('DB_ADMIN', '')
if not _sync_url:
    raise ValueError('DB_ADMIN не задан в .env')

# Меняем схему на asyncpg — SQLAlchemy требует другой драйвер для async
async_db_url = _sync_url.replace('postgresql://', 'postgresql+asyncpg://')

# Создаём асинхронный движок (один на всё приложение)
async_engine = create_async_engine(async_db_url, echo=False)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Список сайтов о финансах для парсинга
URLS = [
    'https://www.dominsoft.ru/articles_temp.php?p=artdb1',
    'https://www.banki.ru/news/daytheme/?id=11003288',
    'https://www.rippling.com/blog/business-expense-categories',
]


async def parse_and_save(url: str, client: httpx.AsyncClient) -> None:
    """Загружает страницу асинхронно, извлекает <title> и сохраняет в БД.

    await client.get() не блокирует цикл событий — пока ждём ответ сервера,
    asyncio переключается на другую корутину из asyncio.gather()
    """
    try:
        # Асинхронный HTTP-запрос — не блокирует event loop
        response = await client.get(url, timeout=15.0)
        response.raise_for_status()  # бросает исключение при статусе >= 400

        # Парсим HTML синхронно (BeautifulSoup не поддерживает async)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'Unknown'

        # Асинхронная сессия — await нужен при commit
        async with AsyncSessionLocal() as session:
            category = Category(user_id=1, name=title)
            session.add(category)
            await session.commit()  # не блокирует event loop

        print(f'[Async] Сохранено: {title[:70]}')

    except httpx.TimeoutException:
        print(f'[Async] Таймаут при запросе к {url}')
    except httpx.HTTPError as e:
        print(f'[Async] HTTP-ошибка для {url}: {e}')
    except Exception as e:
        print(f'[Async] Неожиданная ошибка для {url}: {e}')


async def main() -> None:
    """Запускает все корутины параллельно через asyncio.gather."""
    # Один клиент httpx на все запросы — переиспользует TCP-соединения
    # User-Agent имитирует браузер: некоторые сайты (banki.ru) блокируют python-httpx
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    async with httpx.AsyncClient(headers=headers) as client:
        # gather запускает все корутины одновременно и ждёт завершения каждой
        await asyncio.gather(*[parse_and_save(url, client) for url in URLS])


if __name__ == '__main__':
    start = time.perf_counter()

    asyncio.run(main())

    elapsed = time.perf_counter() - start
    print(f'\n[Async] Время выполнения: {elapsed:.2f} сек')
