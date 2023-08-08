from collections import deque, defaultdict
import matplotlib.pyplot as plt
from treasurehunt import Line, Point


def treasure_hunt_draw_paths_solution(n, lines, treasure):
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
                plt.plot([part_s[i].x, part_s[i + 1].x], [part_s[i].y, part_s[i + 1].y], marker='o', color='green')

        nodes = set()
        graph = defaultdict(set)
        nodes.add(treasure_node)

        for l in lines:
            nodes.add(l)
            add_square_points(l)
            plt.plot([l.point_1.x, l.point_2.x], [l.point_1.y, l.point_2.y], marker='o', color='black')

        add_external_walls(side_square_1, lambda p: p.y)
        add_external_walls(side_square_2, lambda p: p.x)
        add_external_walls(side_square_3, lambda p: p.y)
        add_external_walls(side_square_4, lambda p: p.x)

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
                    plt.plot([node_1.mid.x, node_2.mid.x], [node_1.mid.y, node_2.mid.y], marker='o', color='red')

        plt.plot(treasure.x, treasure.y, color='yellow', marker='o')

        return graph

    number_of_doors = bfs(get_graph(), treasure_node)
    # if number_of_doors == -1:
    #    print('There is no solution')
    # else:
    #    print('Number of doors = {}'.format(number_of_doors))
    plt.show()
    return number_of_doors


if __name__ == '__main__':
    n = int(input())
    lines = [Line(*map(int, input().split())) for _ in range(n)]
    treasure = Point(*map(float, input().split()))
    treasure_hunt_draw_paths_solution(n, lines, treasure)
