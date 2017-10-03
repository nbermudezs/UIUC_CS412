from itertools import combinations

import pdb

frequent_itemsets = []

def create_tuples(filepath):
    result = []
    file_object = open(filepath, 'rb')
    lines = file_object.read().split('\n')[:-1]

    for line in lines:
        values = line.split(' ')
        # itemset = set()
        # itemset.update(values)
        # result.append(itemset)
        result.append(tuple(values))
    return result

def apriori(transactions, minsup = 1):
    frequent_1_itemset = []

    candidates = []
    for transaction in transactions:
        for item in transaction:
            if item not in candidates:
                candidates.append(item)

    # as in k-itemset
    k = 1
    while True:
        frequent_itemsets.append({})

        for candidate in candidates:
            for transaction in transactions:
                if set(candidate).issubset(set(transaction)):
                    new_count = frequent_itemsets[ k - 1 ].get(candidate, 0) + 1
                    frequent_itemsets[ k - 1 ][ candidate ] = new_count

        above_threshold_patterns = []
        to_be_deleted = []
        for pattern, support in frequent_itemsets[ k - 1 ].iteritems():
            if support >= minsup:
                above_threshold_patterns.append(pattern)
            else:
                to_be_deleted.append(pattern)
        if k == 1:
            frequent_1_itemset = above_threshold_patterns

        for item in to_be_deleted:
            del frequent_itemsets[ k - 1 ][ item ]

        if len(above_threshold_patterns) == 0:
            break

        candidates = []
        for pattern in above_threshold_patterns:
            for item in frequent_1_itemset:
                candidate = set(item)
                candidate.update(pattern)
                candidate = tuple(candidate)
                if len(pattern) != len(candidate) and \
                    candidate not in candidates:
                    candidates.append(candidate)
        k = k + 1

    return (k, frequent_itemsets)

def total_count(itemsets):
    count = 0
    for itemset in itemsets:
        for items, _ in itemset.iteritems():
            count += 1
    return count

def pattern_of_length(itemsets, k):
    count = 0
    itemset = itemsets[ k - 1 ]
    for item, _ in itemset.iteritems():
        count += 1
    return count

def find_max_patterns(itemsets, k):
    max_patterns = itemsets[ k - 1 ].keys()
    i = k - 2
    while i >= 0:
        itemset = itemsets[ i ]
        for pattern in itemset:
            pattern_set = set(pattern)
            is_max_pattern = True
            # compare it against all k-itemsets where k > i
            for x in xrange(i + 1, k - 1):
                for_comparison = itemsets[ x ]
                for item in for_comparison:
                    if pattern_set.issubset(set(item)):
                        is_max_pattern = False
                        break
                if not is_max_pattern:
                    break

            if is_max_pattern:
                max_patterns.append(pattern)
        i -= 1
    return max_patterns

def confidence(itemsets, given, implied):
    given_set = set(given)
    given_k = len(given)
    given_support = itemsets[ given_k - 1 ].get(tuple(given_set), 0)
    if given_support == 0:
        return 0

    union = set(given)
    union.update(implied)
    union_k = len(union)
    union_support = itemsets[ union_k - 1 ].get(tuple(union), 0)
    return 1.0 * union_support / given_support

def metrics(transactions, minsup):
    k, itemsets = apriori(transactions, minsup)

    print('Frequent patterns:')
    for itemset in itemsets:
        for items, count in itemset.iteritems():
            print('{0}:{1}'.format(items, count))
    print('====================================')

    for i in range(k):
        print('Total # of patterns of length {0}: {1}'.format(i, pattern_of_length(itemsets, i)))
    print('Total # of patterns: {0}'.format(total_count(itemsets)))

    max_patterns = find_max_patterns(itemsets, k)
    print('Max patterns:')
    for pattern in max_patterns:
        print(pattern)
    print('Number of max patterns: {0}'.format(len(max_patterns)))

    c = confidence(itemsets, ('C', 'E'), tuple('A'))
    print('(C, E) -> A confidence: {0}'.format(round(c, 3)))

    c = confidence(itemsets, ('A', 'B', 'C'), tuple('E'))
    print('(A, B, C) -> E confidence: {0}'.format(round(c, 3)))

if __name__ == '__main__':
    transactions = create_tuples('hw2data/Q3data')
    # for item in transactions:
    #     if len(item) == 2:
    #         print('2', item)

    print('=====================================')
    print('minsup = 20')
    metrics(transactions, 20)
    print('\n\n')

    frequent_itemsets = []

    print('=====================================')
    print('minsup = 10')
    metrics(transactions, 10)
