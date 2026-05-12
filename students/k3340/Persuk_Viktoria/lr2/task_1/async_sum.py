import os
import asyncio
import time


TOTAL = 1_000_000_000
workers = os.cpu_count()

chunk_size = TOTAL // workers


async def calculate_sum(start: int, end: int) -> int:
    summ = sum(range(start, end + 1))

    return summ


ranges = []

for i in range(workers):
    if i == 0:
        start = 1
    else:
        start = (i * chunk_size) + 1

    if i == workers - 1:
        end = TOTAL
    else:
        end = ((i + 1) * chunk_size)

    ranges.append((start, end))


async def main():
    tasks = []

    for start, end in ranges:
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    print(sum(results))


if __name__ == '__main__':
    start_time = time.perf_counter()

    asyncio.run(main())

    end_time = time.perf_counter() - start_time

    print(f'Total time: {end_time:.2f} seconds')
