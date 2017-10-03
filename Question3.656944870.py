# Author: Nestor Bermudez <nab6@illinois.edu>
# UIN: 656944870
# September 5th, 2017

import math
import numpy
import pandas as pd

precision = 3

def mean(vector):
    return 1.0 * sum(vector) / len(vector)

def variance(vector):
    n = len(vector)
    vector_mean = mean(vector)
    sum_of_squares = sum([ (x - vector_mean) ** 2 for x in vector ])
    return 1.0 * sum_of_squares / (n - 1)

def standard_deviation(vector):
    return math.sqrt(variance(vector))

def normalize(vector):
    vector_mean = mean(vector)
    vector_sd = standard_deviation(vector)
    return [ (x - vector_mean) / vector_sd for x in vector ]

def cosine_similarity(x, y):
    dot_product = numpy.dot(x, y)
    norm_x = numpy.linalg.norm(x)
    norm_y = numpy.linalg.norm(y)
    return 1.0 * dot_product / (norm_x * norm_y)

# assumes P(i) = Count(book_i)/Total number of books in X library
# assumes Q(i) = Count(book_i)/Total number of books in Y library
def kl_divergence(x, y):
    sum_x = sum(x)
    sum_y = sum(y)

    result = 0
    for i in range(len(x)):
        pi = 1.0 * x[ i ] / sum_x
        qi = 1.0 * y[ i ] / sum_y
        result += pi * math.log(pi / qi)
    return result

data = pd.read_csv('data.libraries.inventories.txt', delimiter = '\t')

for i, row in data.iterrows():
    if row[ 'library' ] == 'CML':
        cml_inventory = row.tolist()[ 1: ]
    elif row[ 'library' ] == 'CBL':
        cbl_inventory = row.tolist()[ 1: ]

dimension = len(cml_inventory)

# Given the suplement matrix
supplement_matrix = [[ 20, 120 ], [ 2, 58 ]]

jaccard = 1.0 * supplement_matrix[ 1 ][ 1 ] / (supplement_matrix[ 1 ][ 1 ] + supplement_matrix[ 1 ][ 0 ] + supplement_matrix[ 0 ][ 1 ])
print 'a) Jaccard coefficient:', round(jaccard, precision)

print 'b) Minkowski distances'
# |L  |CML|CBL|
# |CML| 0 |   |
# |CBL| d | 0 |
# we are going to calculate d

manhattan_distance = sum([ math.fabs(cml_inventory[ i ] - cbl_inventory[ i ]) for i in range(dimension) ])
print '\t 1. Manhattan distance:', manhattan_distance

euclidean_distance = math.sqrt(sum([ (cml_inventory[ i ] - cbl_inventory[ i ]) ** 2 for i in range(dimension) ]))
print '\t 2. Euclidean distance:', round(euclidean_distance, precision)

supremum_distance = max([ math.fabs(cml_inventory[ i ] - cbl_inventory[ i ]) for i in range(dimension) ])
print '\t 3. Supremum distance:', supremum_distance

print 'c) Cosine similarity:', round(cosine_similarity(cml_inventory, cbl_inventory), precision)

print 'd) KL divergence:', round(kl_divergence(cml_inventory, cbl_inventory), precision)
