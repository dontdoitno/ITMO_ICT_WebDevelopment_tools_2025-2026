import os
import threading
import time


TOTAL = 1_000_000_000
workers = os.cpu_count()

chunk_size = TOTAL // workers

results = [0] * workers


def calculate_sum(index: int, start: int, end: int) -> None:
    results[index] = sum(range(start, end + 1))


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

    ranges.append((i, start, end))


if __name__ == '__main__':
    start_time = time.perf_counter()

    threads = []

    for index, start, end in ranges:
        thread = threading.Thread(
            target=calculate_sum,
            args=(index, start, end)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(sum(results))

    end_time = time.perf_counter() - start_time

    print(f'Total time: {end_time:.2f} seconds')
