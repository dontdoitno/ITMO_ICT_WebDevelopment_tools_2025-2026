import os
import multiprocessing
import time


TOTAL = 1_000_000_000
workers = os.cpu_count()

chunk_size = TOTAL // workers


def calculate_sum(start: int, end: int) -> int:
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


if __name__ == '__main__':
    start_time = time.perf_counter()

    with multiprocessing.Pool(processes=workers) as pool:
        multiprocess_sum = pool.starmap(calculate_sum, ranges)
        print(sum(multiprocess_sum))

    end_time = time.perf_counter() - start_time

    print(f'Total time: {end_time:.2f} seconds')
