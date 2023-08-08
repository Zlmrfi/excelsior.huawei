from collections import namedtuple
from itertools import product
from dataclasses import dataclass

Point = namedtuple('point', 'x y')


@dataclass(frozen=True)
class Pizzeria:
    k_index: int
    n: int
    e: int
    s: int
    w: int

    def __str__(self):
        return ' '.join(map(str, [self.n, self.e, self.s, self.w]))


def Knuths_Algorithm_X(X, Y):
    # source - https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
    def solve(X, Y, solution):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = select(X, Y, r)
                for s in solve(X, Y, solution):
                    yield s
                deselect(X, Y, r, cols)
                solution.pop()

    def select(X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    return solve(X, Y, [])


def pizza_solution(n, m, k, pizzerias_input):
    # The idea is to build all possible cross-shaped forms for each pizzeria. And reduce the task to the exact cover
    # problem (https://en.wikipedia.org/wiki/Exact_cover) . It is necessary to fill the city (the set of cells of the
    # matrix of size n by m) with crosses (which are a subset of the city) To solve it, use Knuths Algorithm X (
    # https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) In general, the time complexity of the Algorithm X is
    # exponential in the worst case, although it often performs much better in practice.

    all_pizzerias_forms = dict()
    city = set(map(lambda p: Point(p[0], p[1]), product(range(1, m + 1), range(1, n + 1))))

    def check_beyond_borders(point):
        return 1 <= point.x <= m and 1 <= point.y <= n

    # We build all kinds of cruciform shapes for each pizzeria
    for piz_index in range(k):
        x, y, c = pizzerias_input[piz_index]
        for c_for_x in range(c + 1):
            for inc_x in range(c_for_x + 1):
                for inc_y in range(c - c_for_x + 1):
                    ends_points_cross = [Point(x=x, y=y + inc_y), Point(x=x, y=y - (c - c_for_x - inc_y)),
                                         Point(x=x + inc_x, y=y),
                                         Point(x=x - (c_for_x - inc_x), y=y)]
                    if all(map(check_beyond_borders, ends_points_cross)):
                        # we match a set of city cells to the cross
                        cross_points = list(
                            set(Point(x, y_) for y_ in range(y - (c - c_for_x - inc_y), y + inc_y + 1)) | set(
                                Point(x_, y) for x_ in range(x - (c_for_x - inc_x), x + inc_x + 1)))
                        all_pizzerias_forms[Pizzeria(k_index=piz_index, n=inc_y, e=inc_x, s=c - c_for_x - inc_y,
                                                     w=c_for_x - inc_x)] = cross_points
    city = {j: set() for j in city}
    for piz_index in all_pizzerias_forms:
        for j in all_pizzerias_forms[piz_index]:
            city[j].add(piz_index)
    try:
        pizzerias_output = Knuths_Algorithm_X(city, all_pizzerias_forms).__next__()
        pizzerias_output.sort(key=lambda p: p.k_index)

        for piz in pizzerias_output:
            print(piz)

        return pizzerias_output
    except StopIteration:
        print('There is no solution here')
        return -1


if __name__ == '__main__':
    while True:
        try:
            n, m, k = map(int, input().split())
            pizzerias_input = [list(map(int, input().split())) for _ in range(k)]
            pizza_solution(n, m, k, pizzerias_input)
        except ValueError:
            break
