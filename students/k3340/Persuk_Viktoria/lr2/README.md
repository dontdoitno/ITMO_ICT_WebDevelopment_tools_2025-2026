# Task 1

Multiprocessing
500000000500000000
Total time: 10.56 seconds

Threading
500000000500000000
Total time: 32.68 seconds

async
500000000500000000
Total time: 32.72 seconds


# Task 2

```
(.venv) (base) MacBook-Air-18:lr2 vikafg$ /Users/vikafg/Documents/Gi
tHub/ITMO_ICT_WebDevelopment_tools_2025-2026/students/k3340/Persuk_Viktoria/lr2/.venv/bin/python /Users/vikafg/Doc
uments/GitHub/ITMO_ICT_WebDevelopment_tools_2025-2026/students/k3340/Persuk_Viktoria/lr2/task_2/async_parse.py
[Async] HTTP-ошибка для https://www.banki.ru/news/daytheme/?id=11003288: Client error '403 Forbidden' for url
'https://www.banki.ru/news/daytheme/?id=11003288'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
[Async] Сохранено: Семейные расходы и доходы: выбираем статьи бюджета
[Async] Сохранено: 35 Business Expense Categories for Businesses | Rippling

[Async] Время выполнения: 0.86 сек
(.venv) (base) MacBook-Air-18:lr2 vikafg$ /Users/vikafg/Documents/GitHub/ITMO_ICT_WebDevelopment_tools_2025-2026/s
tudents/k3340/Persuk_Viktoria/lr2/.venv/bin/python /Users/vikafg/Documents/GitHub/ITMO_ICT_WebDevelopment_tools_20
25-2026/students/k3340/Persuk_Viktoria/lr2/task_2/multiprocessing_parse.py
[Multiprocessing] Сохранено: 35 Business Expense Categories for Businesses | Rippling
[Multiprocessing] Сохранено: Семейные расходы и доходы: выбираем статьи бюджета
[Multiprocessing] Сохранено: Какие виды расходов могут быть в семье и какой вариант бюджета подходи

[Multiprocessing] Время выполнения: 1.64 сек
(.venv) (base) MacBook-Air-18:lr2 vikafg$ /Users/vikafg/Documents/GitHub/ITMO_ICT_WebDevelopment_tools_2025-2026/s
tudents/k3340/Persuk_Viktoria/lr2/.venv/bin/python /Users/vikafg/Documents/GitHub/ITMO_ICT_WebDevelopment_tools_20
25-2026/students/k3340/Persuk_Viktoria/lr2/task_2/threading_parse.py
2026-05-12 21:25:06,906 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2026-05-12 21:25:06,906 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 21:25:06,908 INFO sqlalchemy.engine.Engine select current_schema()
2026-05-12 21:25:06,908 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 21:25:06,908 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2026-05-12 21:25:06,908 INFO sqlalchemy.engine.Engine [raw sql] {}
2026-05-12 21:25:06,909 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 21:25:06,910 INFO sqlalchemy.engine.Engine INSERT INTO category (user_id, name) VALUES (%(user_id)s,
%(name)s) RETURNING category.id, category.created_at
2026-05-12 21:25:06,910 INFO sqlalchemy.engine.Engine [generated in 0.00009s] {'user_id': 1, 'name': '35 Business
Expense Categories for Businesses | Rippling'}
2026-05-12 21:25:06,919 INFO sqlalchemy.engine.Engine COMMIT
[Threads] Сохранено: 35 Business Expense Categories for Businesses | Rippling
2026-05-12 21:25:06,929 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 21:25:06,930 INFO sqlalchemy.engine.Engine INSERT INTO category (user_id, name) VALUES (%(user_id)s,
%(name)s) RETURNING category.id, category.created_at
2026-05-12 21:25:06,930 INFO sqlalchemy.engine.Engine [cached since 0.01996s ago] {'user_id': 1, 'name': 'Семейные
 расходы и доходы: выбираем статьи бюджета'}
2026-05-12 21:25:06,941 INFO sqlalchemy.engine.Engine COMMIT
[Threads] Сохранено: Семейные расходы и доходы: выбираем статьи бюджета
2026-05-12 21:25:11,371 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-12 21:25:11,371 INFO sqlalchemy.engine.Engine INSERT INTO category (user_id, name) VALUES (%(user_id)s,
%(name)s) RETURNING category.id, category.created_at
2026-05-12 21:25:11,371 INFO sqlalchemy.engine.Engine [cached since 4.461s ago] {'user_id': 1, 'name': 'Какие виды
 расходов могут быть в семье и какой вариант бюджета подходит вам: тест | Банки.ру'}
2026-05-12 21:25:11,373 INFO sqlalchemy.engine.Engine COMMIT
[Threads] Сохранено: Какие виды расходов могут быть в семье и какой вариант бюджета подходи

[Threads] Время выполнения: 5.12 сек
```
