from collections import deque


def railroads_solution(n, req_order):
    # The solution is based on the statement - if a wagon gets into the station stack, and it coincides with the last
    # unoccupied one in the required permutation stack, then it needs to be sent by B and after the stack of the
    # original cars becomes empty, you need to pull elements from the station stack element by element and check them
    # for equality with the rest of the permutation stack
    # Time complexity - O(n)
    req_order = deque(req_order)
    init_order = deque(range(1, n + 1))
    station_order = deque()
    while init_order:
        coach = init_order.popleft()
        if coach == req_order[0]:
            req_order.popleft()
        else:
            station_order.append(coach)
    station_order.reverse()
    if station_order == req_order:
        print('Yes')
    else:
        print('No')


if __name__ == '__main__':
    while True:
        n = int(input())
        if n == 0:
            break
        while True:
            req_order = list(map(int, input().split()))
            if req_order == [0]:
                break
            railroads_solution(n, req_order)
        print()
