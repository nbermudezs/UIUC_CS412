# Author: Nestor Bermudez <nab6@illinois.edu>
# UIN: 656944870
# September 6th, 2017

def chi_square(matrix):
    r = len(matrix[ 0 ])
    c = len(matrix)

    column_sums = [ sum(matrix[ i ]) for i in range(c) ]
    row_sums = [ sum([ matrix[ i ][ j ] for i in range(c) ]) for j in range(r) ]
    n = sum(column_sums)

    result = 0
    for i in range(c):
        for j in range(r):
            o_ij = matrix[ i ][ j ]
            e_ij = 1.0 * column_sums[ i ] * row_sums[ j ] / n
            result += (o_ij - e_ij) ** 2 /e_ij

    return result

# data contigency table
#  _______________________________________________________________________
# |                  |   Buy diaper   |   Do not buy diaper   |   TOTAL   |
# |     Buy beer     |       150      |         40            |    190    |
# | Do not buy beer  |        15      |       3300            |   3315    |
#  -----------------------------------------------------------------------
# |       TOTAL      |       165      |       3340            |   3505    |

contigency_table = [ [ 150, 15 ], [ 40, 3300 ] ]

print 'chi-square:', round(chi_square(contigency_table), 3)
