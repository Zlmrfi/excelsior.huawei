import random
from treasurehunt import treasure_hunt_solution, Line, Point
from treasurehunt_draw_paths import treasure_hunt_draw_paths_solution
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


TreasureHunt_solution = timeit(treasure_hunt_solution)
# test generator
for _ in range(TESTS_NUMBER):
    n = random.randint(1, 100)
    end_points = [Point(lambda: 0, lambda: random.randint(1, 99)),
                  Point(lambda: 100, lambda: random.randint(1, 99)),
                  Point(lambda: random.randint(1, 99), lambda: 100),
                  Point(lambda: random.randint(1, 99), lambda: 0)]
    lines = []
    for _ in range(n):
        point_1, point_2 = random.sample(end_points, 2)
        lines.append(Line(point_1.x(), point_1.y(), point_2.x(), point_2.y()))
    treasure = Point(random.uniform(0.0, 100.0), random.uniform(0.0, 100.0))
    print(n, '\n'.join(map(str, lines)), treasure, sep='\n')
    TreasureHunt_solution(n, lines, treasure)
    treasure_hunt_draw_paths_solution(n, lines, treasure)
