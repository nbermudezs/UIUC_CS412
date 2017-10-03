# Author: Nestor Bermudez <nab6@illinois.edu>
# UIN: 656944870
# September 5th, 2017

import csv
import math

def median(sorted_vector):
    mid = len(sorted_vector) // 2
    if (len(sorted_vector) % 2 == 0):
        return (sorted_vector[ mid - 1 ] + sorted_vector[ mid ]) / 2.0
    else:
        return sorted_vector[ mid ]

def quartiles(sorted_vector):
    vector_size = len(sorted_vector)
    q1 = median(sorted_vector[ :(vector_size / 2) ])
    q2 = median(sorted_vector)
    q3 = median(sorted_vector[ int(math.ceil(vector_size / 2)): ])
    return (q1, q2, q3)

def mean(vector):
    return sum(vector) / len(vector)

def mode(vector):
    # group into frequency table
    frequencies = {}

    for value in vector:
        if value in frequencies:
            frequencies[ value ] += 1
        else:
            frequencies[ value ] = 1

    # find max frequency
    max_frequency = max(frequencies.values())

    # return value
    return [ k for k, v in frequencies.items() if v == max_frequency ]

def variance(vector):
    n = len(vector)
    vector_mean = mean(vector)
    sum_of_squares = sum([ (x - vector_mean) ** 2 for x in vector ])
    return sum_of_squares / (n - 1)

raw_data = open('data.online.scores.txt', 'rb')
attribute_vector = [ 'student_id', 'midterm_score', 'final_score' ]
online_scores_dict = csv.DictReader(raw_data, delimiter = '\t', fieldnames = attribute_vector)

midterm_scores = [ float(row[ 'midterm_score' ]) for row in online_scores_dict ]
midterm_scores.sort()

print 'About midterm scores...'
print 'a) MIN & MAX '
print '\tMIN:', midterm_scores[ 0 ]
print '\tMAX:', midterm_scores[ -1 ]

print 'b) First quartile Q1, median, third quartile Q3'
midterm_quartiles = quartiles(midterm_scores)
print '\tQ1:', midterm_quartiles[ 0 ]
print '\tQ2 (median):', midterm_quartiles[ 1 ]
print '\tQ3:', midterm_quartiles[ 2 ]

print 'c) Mean score:', mean(midterm_scores)

print 'd) Mode score:', mode(midterm_scores)

print 'e) Empirical Variance:', round(variance(midterm_scores), 3)
