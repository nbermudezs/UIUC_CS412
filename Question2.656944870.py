# Author: Nestor Bermudez <nab6@illinois.edu>
# UIN: 656944870
# September 5th, 2017

import csv
import math

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

# Implements formula found in https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#For_a_sample
def pearson(x_vector, y_vector):
    x_mean = mean(x_vector)
    y_mean = mean(y_vector)

    numerator = sum([ (x_vector[ i ] - x_mean) * (y_vector[ i ] - y_mean) for i in range(len(x_vector)) ])
    denominator = math.sqrt(sum([ (x - x_mean) ** 2 for x in x_vector ])) * math.sqrt(sum([ (y - y_mean) ** 2 for y in y_vector ]))
    return numerator / denominator

def covariance(x_vector, y_vector):
    n = len(x_vector)
    x_mean = mean(x_vector)
    y_mean = mean(y_vector)

    return sum([ (x_vector[ i ] - x_mean) * (y_vector[ i ] - y_mean) for i in range(n) ]) / (n - 1)

raw_data = open('data.online.scores.txt', 'rb')
attribute_vector = [ 'student_id', 'midterm_score', 'final_score' ]
online_scores_dict = csv.DictReader(raw_data, delimiter = '\t', fieldnames = attribute_vector)

midterm_scores = [ float(row[ 'midterm_score' ]) for row in online_scores_dict ]

raw_data.seek(0)
final_scores = [ float(row[ 'final_score' ]) for row in online_scores_dict ]

print 'a) Compare empirical variance before and after normalization'
print '\t Before:', round(variance(midterm_scores), 3)
print '\t After:', round(variance(normalize(midterm_scores)), precision)

print 'b) Given original score of 90, what is the corresponding value after normalization?'
print '\t After normalization 90 is', round((90 - mean(midterm_scores)) / standard_deviation(midterm_scores), precision)

print 'c) i. Pearson\'s correlation coefficient (r) between midterm and final scores'
print '\t r =', round(pearson(midterm_scores, final_scores), precision)

print 'c) ii. Pearson\'s correlation coefficient (r) between normalized midterm and final scores'
print '\t r =', round(pearson(normalize(midterm_scores), normalize(final_scores)), precision)

print 'd) i. Covariance between midterm and final scores'
print '\t cov =', round(covariance(midterm_scores, final_scores), precision)

print 'd) ii. Covariance between normalized midterm and final scores'
print '\t cov =', round(covariance(normalize(midterm_scores), normalize(final_scores)), precision)
