import random
from digital_lab_effective_solution import digital_lab_ef
from digital_lab_brute_force_solution import digital_lab_bf
from copy import deepcopy
from functools import wraps
import time

TESTS_NUMBER = 1000


def print_matrix(matrix_):
    for row in matrix_:
        print(' '.join(row))


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


Digital_lab_ef = timeit(digital_lab_ef)
Digital_lab_bf = timeit(digital_lab_bf)
# test generator
for _ in range(TESTS_NUMBER):
    n_A, m_A = random.randint(1, 1000), random.randint(1, 1000)
    n_B, m_B = random.randint(1, 1000), random.randint(1, 1000)
    A = [[str(random.randint(0, 1)) for _ in range(m_A)] for _ in range(n_A)]
    B = [[str(random.randint(0, 1)) for _ in range(m_B)] for _ in range(n_B)]
    e_B = Digital_lab_ef(n_A, m_A, n_B, m_B, A, deepcopy(B))
    bf_B = Digital_lab_bf(n_A, m_A, n_B, m_B, A,
                          deepcopy(B))
    print(n_A, m_A)
    print_matrix(A)
    print(n_B, m_B)
    print_matrix(B)
    print()
    print_matrix(e_B)

    assert e_B == bf_B
