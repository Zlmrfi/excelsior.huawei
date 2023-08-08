from collections import deque, defaultdict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return ' '.join(map(str, [self.x, self.y]))


class Line:
    def __init__(self, x_1, y_1, x_2, y_2, external=False):
        self.point_1 = Point(x_1, y_1)
        self.point_2 = Point(x_2, y_2)
        self.A = self.point_1.y - self.point_2.y
        self.B = self.point_2.x - self.point_1.x
        self.C = self.point_1.x * self.point_2.y - self.point_2.x * self.point_1.y
        self.mid = Point((self.point_1.x + self.point_2.x) / 2, (self.point_1.y + self.point_2.y) / 2)
        self.external = external

    def is_intersect(self, other):
        # I hope I wrote this function correctly
        if self.A == other.A and self.B == other.B and self.C == other.C:
            def on_one_line(l_1, l_2, projector):
                if min(projector(l_2)) <= min(projector(l_1)) <= max(projector(l_2)):
                    return True

            conds_1 = [
                on_one_line(self, other, lambda l: (l.point_1.x, l.point_2.x)),
                on_one_line(other, self, lambda l: (l.point_1.x, l.point_2.x))]
            conds_2 = [
                on_one_line(self, other, lambda l: (l.point_1.y, l.point_2.y)),
                on_one_line(other, self, lambda l: (l.point_1.y, l.point_2.y))
            ]
            if any(conds_1) and any(conds_2):
                return True
        if self.A * other.B - other.A * self.B != 0:
            x = - (self.C * other.B - other.C * self.B) / (self.A * other.B - other.A * self.B)
            y = - (self.A * other.C - other.A * self.C) / (self.A * other.B - other.A * self.B)
            lower_bound_x = max(min(self.point_1.x, self.point_2.x), min(
                other.point_1.x, other.point_2.x))

            upper_bound_x = min(max(self.point_1.x, self.point_2.x),
                                max(other.point_1.x,
                                    other.point_2.x))
            lower_bound_y = max(
                min(self.point_1.y,
                    self.point_2.y),
                min(
                    other.point_1.y,
                    other.point_2.y))
            upper_bound_y = min(
                max(
                    self.point_1.y, self.point_2.y), max(other.point_1.y,
                                                         other.point_2.y))
            if lower_bound_x <= x <= upper_bound_x and lower_bound_y <= y <= upper_bound_y:
                return True

        return False

    def __str__(self):
        return ' '.join(map(str, [self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y]))


def treasure_hunt_solution(n, lines, treasure):
    # The idea is to build a graph. Vertices are lines (outer, inner walls and treasure are a degenerate line). We
    # connect two vertices if and only if the line connecting the midpoints of these two vertices (lines) does not
    # intersect any inner wall. Next, we run BFS from the treasure on the constructed graph
    # Time complexity - O(n^3)
    treasure_node = Line(treasure.x, treasure.y, treasure.x, treasure.y)
    side_square_1, side_square_2, side_square_3, side_square_4 = {Point(0, 0), Point(0, 100)}, {Point(0, 0),
                                                                                                Point(100, 0)}, {
                                                                     Point(100, 0),
                                                                     Point(100, 100)}, {
                                                                     Point(0, 100), Point(100, 100)}

    def bfs(graph, node):
        visited = [node]
        queue = deque([(node, 0)])
        while queue:
            m, step = queue.popleft()
            # we reached the outer wall
            if m.external:
                return step
            for neighbour in graph[m]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append((neighbour, step + 1))
        return -1

    def get_graph():
        def add_square_points(l):
            if l.point_1.x == 0:
                side_square_1.add(l.point_1)
            if l.point_2.x == 0:
                side_square_1.add(l.point_2)
            if l.point_1.y == 0:
                side_square_2.add(l.point_1)
            if l.point_2.y == 0:
                side_square_2.add(l.point_2)
            if l.point_1.x == 100:
                side_square_3.add(l.point_1)
            if l.point_2.x == 100:
                side_square_3.add(l.point_2)
            if l.point_1.y == 100:
                side_square_4.add(l.point_1)
            if l.point_2.y == 100:
                side_square_4.add(l.point_2)

        def add_external_walls(part, sort_func):
            part_s = sorted(list(part), key=sort_func)
            for i in range(len(part_s) - 1):
                nodes.add(Line(part_s[i].x, part_s[i].y, part_s[i + 1].x, part_s[i + 1].y, external=True))

        nodes = set()
        graph = defaultdict(set)
        # adding nodes
        nodes.add(treasure_node)
        for l in lines:
            nodes.add(l)
            add_square_points(l)

        add_external_walls(side_square_1, lambda p: p.y)
        add_external_walls(side_square_2, lambda p: p.x)
        add_external_walls(side_square_3, lambda p: p.y)
        add_external_walls(side_square_4, lambda p: p.x)
        # adding edges
        for node_1 in nodes:
            for node_2 in nodes:
                connect_mid = Line(node_1.mid.x, node_1.mid.y, node_2.mid.x, node_2.mid.y)

                def cond_(node_):
                    return node_ != node_1 and node_ != node_2 and not node_.external and node_ != treasure_node

                if all(not connect_mid.is_intersect(node_3) if cond_(node_3) else True
                       for node_3
                       in nodes) and node_1 != node_2:
                    graph[node_1].add(node_2)
                    graph[node_2].add(node_1)

        return graph

    number_of_doors = bfs(get_graph(), treasure_node)
    if number_of_doors == -1:
        print('There is no solution')
    else:
        print('Number of doors = {}'.format(number_of_doors))
    return number_of_doors


if __name__ == '__main__':
    n = int(input())
    lines = [Line(*map(int, input().split())) for _ in range(n)]
    treasure = Point(*map(float, input().split()))
    treasure_hunt_solution(n, lines, treasure)
