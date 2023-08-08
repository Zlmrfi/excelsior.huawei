"""
There may be uncertainty when reading the task.
I thought that the output to such an input should be like this.
1 2
1 1
1 3
1 1 1
output:
2 2 2
not like this:
2 2 1

All the matches of the pattern A in B are calculated, and then they are marked. That
does not happen like this - there was a match, we immediately mark the pattern in B and thus does not allow us to
detect a match that intersected with the previous one
"""
from collections import namedtuple

Point = namedtuple('point', 'x y')
Pattern = namedtuple('pattern', 'A B C D')


def digital_lab_bf(n_a, m_a, n_b, m_b, a, b):
    # brute force solution
    # Time Complexity: O(n_a * m_a * n_b * m_b)
    # matrix b will be changed
    patterns = []

    def is_matches_with_a(pattern_):
        # returns true if the pattern matches A, false otherwise
        for i in range(n_a):
            for j in range(m_a):
                if a[i][j] != b[i + pattern_.A.x][j + pattern_.A.y]:
                    return False
        return True

    def mark_a_located_pattern(pattern_):
        for i in range(pattern_.A.x, pattern_.D.x + 1):
            for j in range(pattern_.A.y, pattern_.B.y + 1):
                if b[i][j] == '0':
                    b[i][j] = '*'
                elif b[i][j] == '1':
                    b[i][j] = '2'

    # adding all submatrices of size A from B
    for p_i in range(n_b - n_a + 1):
        for p_j in range(m_b - m_a + 1):
            patterns.append(
                Pattern(Point(p_i, p_j), Point(p_i, p_j + m_a - 1), Point(p_i + n_a - 1, p_j + m_a - 1),
                        Point(p_i + n_a - 1, p_j)))

    matched_patterns = list(filter(is_matches_with_a, patterns))
    for m_pattern in matched_patterns:
        mark_a_located_pattern(m_pattern)

    return b


if __name__ == '__main__':
    n_A, m_A = map(int, input().split())
    A = [input().split() for _ in range(n_A)]
    n_B, m_B = map(int, input().split())
    B = [input().split() for _ in range(n_B)]
    digital_lab_bf(n_A, m_A, n_B, m_B, A, B)
    for row in B:
        print(' '.join(row))
