import random
from railroads import railroads_solution
from functools import wraps
import time

TESTS_NUMBER = 1000

# calculating the running time of the program
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


Railroads_solution = timeit(railroads_solution)
# test generator
for _ in range(TESTS_NUMBER):
    n = random.randint(1, 1000)
    req_order = list(range(1, n + 1))
    random.shuffle(req_order)
    print(n)
    print(' '.join(map(str, req_order)))
    Railroads_solution(n, req_order)
