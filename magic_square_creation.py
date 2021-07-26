# Program: Magic square of size 3x3 creation at minimal cost

import math
from itertools import combinations, permutations

def is_magic(s, m, n):
    # Return the probability equal to 1 if the sum of all rows, cols, and diags is equal to m. Otherwise probability is less than 1

    return [sum(s[:3]), sum(s[3:6]), sum(s[6:9]), sum(s[:7:3]), sum(s[1:8:3]), sum(s[2:9:3]), sum(s[:9:4]),  sum(s[2:7:2])].count(m)/(2*math.sqrt(n) + 2)


def get_sets_in_magic(m, n, len_group):
    # Return the sets of center, corners and edges

    # Get len_group (e.g, 3) size combinations in [1, 2, 3,...,9] whose sum is equal to m
    comb = [t for t in list(combinations([i + 1 for i in range(n)], len_group)) if sum(t) == m]
    n_involved_sums = {}
    for i in range(n):
        n_involved_sums[i + 1] = sum([1 for t in comb if i + 1 in t])

    # Note there 8 sums to get M in a magic square of 9 elements:
    # 3 rows, 3 cols, and 2 diags.
    # The center element is involved in 4 sums
    # The corners elements are involved in 3 sums
    # The edges element are involved in 2 sums
    # From n_involved_sums we can see the next:
    # 5 is involded in 4 sums, so must be in the center
    # 2, 4, 6, 8 are involved in 3 sums, so must be corners
    # 1, 3, 7, 9 are involded in 2 sums, so must be edges

    # Get sets in magic square
    sets_in_magic = {}
    sets_in_magic['corners'] = []
    sets_in_magic['edges'] = []
    for key, val in n_involved_sums.items():
        if val == 2:
            sets_in_magic['edges'].append(key)
        elif val == 3:
            sets_in_magic['corners'].append(key)
        elif val == 4:
            sets_in_magic['center'] = key
    return sets_in_magic


def get_min_magics_cost(sets, actual, m, n):
    # Return the minimum cost of converting actual in a magic square

    corners = list(permutations(sets['corners']))
    edges = list(permutations(sets['edges']))
    tmp = n * [0]
    tmp[4] = sets['center']
    cost = []
    prev_cost = n*n
    for i in range(len(corners)):
        for j in range(len(edges)):
            tmp[0] = corners[i][0]
            tmp[2] = corners[i][1]
            tmp[6] = corners[i][2]
            tmp[8] = corners[i][3]
            tmp[1] = edges[j][0]
            tmp[3] = edges[j][1]
            tmp[5] = edges[j][2]
            tmp[7] = edges[j][3]
            if is_magic(tmp, m, n) == 1:
                curr_cost = sum([abs(actual[k] - tmp[k]) for k in range(n)])
                cost.append(curr_cost)
                if curr_cost < prev_cost:
                    magic_at_min = tmp[:]
                    prev_cost = curr_cost
    return [magic_at_min[i:i+3] for i in range(0, n, 3)], min(cost)

def forming_magic_square(s, m, sets_len=3):
    flat_s = [j for sub in s for j in sub]
    n = len(flat_s)
    return get_min_magics_cost(get_sets_in_magic(m, n, sets_len), flat_s, m, n)

if __name__ == "__main__":
    M = 15
    s = [[4, 9, 2], [3, 5, 7], [8, 1, 5]]
    magic, cost = forming_magic_square(s, M)
    print('Actual square:')
    print('%s\n%s\n%s\n' % (s[0], s[1], s[2]))
    print('Magic square')
    print('%s\n%s\n%s\n' % (magic[0], magic[1], magic[2]))
    print('At cost: ', cost)

    # TODO: optimize code and create a program for higher nxn sizes (>3)

