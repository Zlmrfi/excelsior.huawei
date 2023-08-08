import random
from pizza import pizza_solution, Pizzeria as PizzeriaOutput
from pizza_draw_solution import draw_solution
from functools import wraps
from collections import namedtuple
import time
from sympy.combinatorics.partitions import random_integer_partition
from itertools import product
from dataclasses import dataclass

TESTS_NUMBER = 1000
Point = namedtuple('point', 'x y')


@dataclass(frozen=True)
class PizzeriaInput:
    x: int
    y: int
    c: int

    def __str__(self):
        return ' '.join(map(str, [self.x, self.y, self.c]))

    def convert_to_tuple(self):
        return self.x, self.y, self.c


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


pizza = timeit(pizza_solution)


def generator_no_solution():
    # Generates tests in which the solution may not exist
    for _ in range(TESTS_NUMBER):
        n, m = random.randint(1, 30), random.randint(1, 30)
        c = []
        # We break the matrix into pieces
        while len(c) > 200 or len(c) == 0:
            c = list(map(lambda c_: c_ - 1, random_integer_partition(n * m)))
        k = len(c)
        coord = random.sample(list(product(range(1, m + 1), range(1, n + 1))), k)
        pizzerias = [(coord[i][0], coord[i][1], c[i]) for i in range(k)]
        print(' '.join(map(str, [n, m, k])))
        for pizzeria in pizzerias:
            print(' '.join(map(str, pizzeria)))
        output = pizza(n, m, k, pizzerias)
        if output != -1:
            draw_solution(n, m, pizzerias, output)


# generator_no_solution()

def generator_solution_exist():
    # The solution is guaranteed to exist
    for _ in range(TESTS_NUMBER):
        n, m = random.randint(1, 30), random.randint(1, 30)
        city = set(map(lambda p: Point(p[0], p[1]), product(range(1, m + 1), range(1, n + 1))))
        pizzeria_input = []
        pizzeria_output = []

        def is_in_city(points):
            return all(point_ in city for point_ in points)

        # We build crosses, check if they are in the matrix, if there are, add them to the list of input and output
        # data and remove them from the matrix (there could be some optimization here - generate only crosses that
        # are in the matrix, but the solution algorithm is exponential in the worst case, so there is none)
        while city:
            cell = next(iter(city))
            end_point_x_1 = random.sample(range(max(1, cell.x - m), min(cell.x + 1, m + 1)), 1)[0]
            end_point_x_2 = random.sample(range(cell.x, min(cell.x + m, m + 1)), 1)[0]
            end_point_y_1 = random.sample(range(max(cell.y - n, 1), min(cell.y + 1, n + 1)), 1)[0]
            end_point_y_2 = random.sample(range(cell.y, min(cell.y + n, n + 1)), 1)[0]
            cross_points = set(Point(cell.x, y_) for y_ in range(end_point_y_1, end_point_y_2 + 1)) | set(
                Point(x_, cell.y) for x_ in range(end_point_x_1, end_point_x_2 + 1))
            if is_in_city(cross_points):
                c = end_point_x_2 - end_point_x_1 + end_point_y_2 - end_point_y_1
                pizzeria_input.append(PizzeriaInput(cell.x, cell.y, c))
                pizzeria_output.append(
                    PizzeriaOutput(s=cell.y - end_point_y_1, n=end_point_y_2 - cell.y, w=cell.x - end_point_x_1,
                                   e=end_point_x_2 - cell.x, k_index=len(pizzeria_input) - 1))
                for cell_ in cross_points:
                    city.remove(cell_)
        print(' '.join(map(str, [n, m, len(pizzeria_input)])))
        for pizzeria in pizzeria_input:
            print(pizzeria)
        pizzeria_input = list(map(lambda p: p.convert_to_tuple(), pizzeria_input))
        print()
        draw_solution(n, m, pizzeria_input, pizzeria_output)
        output_solution = pizza(n, m, len(pizzeria_input), pizzeria_input)
        assert output_solution != -1
        draw_solution(n, m, pizzeria_input, output_solution)


generator_solution_exist()
