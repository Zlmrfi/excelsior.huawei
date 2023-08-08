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

from dataclasses import dataclass


@dataclass
class Segment:
    start: int
    end: int


def digital_lab_ef(n_a, m_a, n_b, m_b, a, b):
    # effective solution
    # Time Complexity: O(n_a * m_a + n_b * m_b) - is linear of the size of the matrices
    # the idea is to hash all rows of size m_a of matrix B and all rows of matrix A. Hash lists can be
    # interpreted as strings (where a character is a hash) and use the KMP algorithm
    # matrix b will be changed

    def disjoint_equivalent_segments(segments):
        if not segments:
            return segments
        # assert sorted(segments, key=lambda s: s.start) == segments
        list_disjoint = [segments[0]]
        for segment_ in segments[1:]:
            if segment_.start <= list_disjoint[-1].end:
                list_disjoint[-1].end = max(list_disjoint[-1].end, segment_.end)
            else:
                list_disjoint.append(segment_)
        return list_disjoint

    def KnuthMorrisPratt(text, pattern_):
        # from http://code.activestate.com/recipes/117214/
        # Knuth-Morris-Pratt string matching
        # Time Complexity: O(m+n)
        # David Eppstein, UC Irvine, 1 Mar 2002
        # allow indexing into pattern and protect against change during yield
        pattern_ = list(pattern_)

        # build table of shift amounts
        shifts = [1] * (len(pattern_) + 1)
        shift = 1
        for pos in range(len(pattern_)):
            while shift <= pos and pattern_[pos] != pattern_[pos - shift]:
                shift += shifts[pos - shift]
            shifts[pos + 1] = shift

        # do the actual search
        startPos = 0
        matchLen = 0
        for c in text:
            while matchLen == len(pattern_) or \
                    matchLen >= 0 and pattern_[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(pattern_):
                yield startPos

    def mark_a_located_segments(located_segments_):
        for r in range(n_b):
            for segment_ in located_segments_[r]:
                for c in range(segment_.start, segment_.end + 1):
                    if b[r][c] == '0':
                        b[r][c] = '*'
                    elif b[r][c] == '1':
                        b[r][c] = '2'

    a_hash = []
    b_hash = []
    bitmask = int('0' + '1' * (m_a - 1), 2)
    located_segments = [[] for _ in range(n_b)]
    # We hash each row of the matrix A.
    # The hash function of a binary sequence is trivial - turning into a decimal number
    # Time Complexity: O(n_a * m_a)
    for i in range(n_a):
        a_hash.append(int(''.join(a[i]), 2))

    for j in range(m_b - m_a + 1):
        if j == 0:
            # We hash each row of (not completely, only 0 to m_a) the matrix B.
            # Time Complexity: O(n_b * m_a)
            for i in range(n_b):
                b_hash.append(int(''.join(b[i][j:j + m_a]), 2))
        else:
            for i in range(n_b):
                # Here the hash is calculated for the next column (the old value is overwritten - it is no longer needed).
                # We shift the window of size m_a one element to the right
                # The last bit is removed using the mask bit.
                # Then we use the shift bit and add the next bit from the corresponding column
                # Time Complexity: O(n_b)
                b_hash[i] = ((b_hash[i] & bitmask) << 1) + int(b[i][j + m_a - 1])
        # Using the Knuth Morris Pratt algorithm, we find all the matches of the matrix A (more precisely, the list of
        # hashes defining it) in the submatrix B of size n_b * m_a (also in the list of hash rows)
        # Time Complexity: O(n_b + n_a)
        matched_patterns = list(
            map(lambda start_row: Segment(start_row, start_row + n_a - 1), KnuthMorrisPratt(b_hash, a_hash)))
        # this code ensures that each cell when we mark it will be visited exactly ONCE
        # Time Complexity: O(n_b)
        matched_patterns = disjoint_equivalent_segments(matched_patterns)
        located_segment_column = Segment(j, j + m_a - 1)
        for located_segment_row in matched_patterns:
            for row in range(located_segment_row.start, located_segment_row.end + 1):
                if not located_segments[row]:
                    located_segments[row].append(Segment(j, j + m_a - 1))
                elif located_segment_column.start <= located_segments[row][-1].end:
                    located_segments[row][-1].end = max(located_segments[row][-1].end, located_segment_column.end)
                else:
                    located_segments[row].append(Segment(j, j + m_a - 1))

    mark_a_located_segments(located_segments)

    return b


if __name__ == '__main__':

    n_A, m_A = map(int, input().split())
    A = [input().split() for _ in range(n_A)]
    n_B, m_B = map(int, input().split())
    B = [input().split() for _ in range(n_B)]
    digital_lab_ef(n_A, m_A, n_B, m_B, A, B)
    for r in B:
        print(' '.join(r))
