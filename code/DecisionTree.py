__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

import random
from multiprocessing import Pool, cpu_count
from util.NonDemonicProcessPool import NonDemonicPool

def get_pool():
    pool = NonDemonicPool(processes = cpu_count() - 1)
    return pool

class DecisionTreeNode:
    '''
    branches will be a dictionary where the key is the value of the attribute
    handled by this node and the value is the next node.
    '''
    def __init__(self, attribute):
        self.attribute = attribute
        self.branches = {}

    '''
    If the value has not been seen before just take a random branch
    as suggested in the homework.
    '''
    def __call__(self, example):
        value = example[ self.attribute ]
        if value in self.branches:
            return self.branches[ value ](example)
        else:
            branch_key = random.choice(list(self.branches.keys()))
            return self.branches[ branch_key ](example)

    '''
    Add branch to the tree. Will need this when building the tree.
    '''
    def grow(self, value, subtree):
        self.branches[ value ] = subtree
        return self

    def display(self, depth = 0):
        result = ''
        for val, branch in self.branches.items():
            result += '|' + '-' * depth + str(self.attribute) + ' = ' + str(val) + '\n'
            result += '|' + '-' * 2 * depth + branch.display(depth + 1) + '\n'
        return result

class DecisionTreeLeaf:
    def __init__(self, label):
        self.label = label

    def __call__(self, example):
        return self.label

    def display(self, depth = 0):
        return '-' * depth + 'label=' + str(self.label)


class DecisionTree:
    def __init__(self, selector, max_depth = -1,
                 min_dataset_size = 1, parallel = False, min_leaf_size = -1):
        self.tree = None
        self.selector = selector
        self.max_depth = max_depth
        self.min_dataset_size = min_dataset_size
        self.parallel = parallel
        self.min_leaf_size = min_leaf_size

    '''
    Parameters:
        - data: instance of Dataset
    '''
    def train(self, data):
        selected_attribute = self.selector(data, set())
        self.tree = self._build_tree(data, selected_attribute, { selected_attribute })
        return self

    '''
    Parameters:
        - data: instance of Dataset
    '''
    def evaluate(self, data):
        correct = 0
        total = 0
        confusion_matrix = {}
        for (example, label) in data.items():
            predicted_label = self._predict(example)

            # stats
            if predicted_label == label:
                correct += 1
            total += 1

            # update confusion matrix
            matrix_row = confusion_matrix.get(label, {})
            matrix_row[ predicted_label ] = matrix_row.get(predicted_label, 0) + 1
            matrix_row[ 'total' ] = matrix_row.get('total', 0) + 1
            confusion_matrix[ label ] = matrix_row

        return (correct / total, confusion_matrix)

    def _predict(self, example):
        return self.tree(example)

    def _build_tree(self, data, attribute, used_attributes, depth = 0):
        if data.is_single_class():
            return DecisionTreeLeaf(min(data.class_counts.keys()))
        if depth == self.max_depth or len(data) <= self.min_dataset_size or not attribute:
            best = max(data.class_counts.items(), key = lambda x: x[ 1 ])[ 0 ]
            return DecisionTreeLeaf(best)

        subtree = DecisionTreeNode(attribute)
        split = data.split_by_attribute(attribute)
        if self.parallel:
            branches = []
            pool = get_pool()

        if self.min_leaf_size > 0:
            max_value = max(split.items(), key = lambda x: len(x[ 1 ]))[ 0 ]
        for value, dataset in split.items():
            if (len(dataset)) <= self.min_leaf_size and value != max_value:
                best = max(data.class_counts.items(), key = lambda x: x[ 1 ])[ 0 ]
                subtree.grow(value, DecisionTreeLeaf(best))
                continue
            best_attribute = self.selector(dataset, used_attributes)
            if self.parallel:
                branch = pool.apply_async(self._build_tree,
                                          (dataset, best_attribute,
                                           used_attributes ^ { best_attribute },
                                           depth + 1))
                branches.append((value, branch))
            else:
                branch = self._build_tree(dataset,
                                          best_attribute,
                                          used_attributes ^ { best_attribute },
                                          depth + 1)
                subtree.grow(value, branch)

        if self.parallel:
            pool.close()
            pool.join()
            for (value, branch) in branches:
                subtree.grow(value, branch.get())
        return subtree

    def __str__(self):
        return self.tree.display()


if __name__ == '__main__':
    import time, sys
    from util.Dataset import Dataset
    from util.Reporter import Reporter, color
    from util.GiniAttributeSelector import GiniAttributeSelector
    from util.Metric import Metric

    if len(sys.argv) < 3:
        print('Usage: python DecisionTree.py <train file> <test file>')
        exit()

    SHUFFLE_FLAG = '--shuffle'
    OPTIMAL_FLAG = '--optimal'
    DETAILS_FLAG = '--detailed-output'

    PARAMS = {
        'balance.scale':    { 'depth':  3, 'min_dataset_size':  6, 'min_leaf_size':  1, 'parallel': False },
        'led':              { 'depth':  5, 'min_dataset_size':  1, 'min_leaf_size':  1, 'parallel': False }, # DONE
        'nursery':          { 'depth': -1, 'min_dataset_size':  1, 'min_leaf_size': -1, 'parallel': False }, # DONE
        'synthetic.social': { 'depth': 13, 'min_dataset_size': 66, 'min_leaf_size':  1, 'parallel':  True }  # DONE
    }

    detailedOutput = DETAILS_FLAG in sys.argv

    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]

    train_data = Dataset.from_file(train_filepath)
    test_data = Dataset.from_file(test_filepath)
    if SHUFFLE_FLAG in sys.argv:
        from util.RandomSampler import RandomSampler
        train_data = RandomSampler.sample(train_data)

    if detailedOutput:
        print('Training set size: ' + color.BOLD + str(len(train_data)) + color.END)
        print('Test set size: ' + color.BOLD + str(len(test_data)) + color.END)
        print()

    key = None
    for dataset_file in PARAMS.keys():
        if train_filepath.find(dataset_file) >= 0:
            key = dataset_file
            break

    depth = PARAMS[ key ][ 'depth' ]
    min_size = PARAMS[ key ][ 'min_dataset_size' ]
    parallel = PARAMS[ key ][ 'parallel' ]
    leaf_size = PARAMS[ key ][ 'min_leaf_size' ]

    def find_optimal_parameters():
        best_accuracy = -float('inf')
        best_depth = 0
        best_minsize = 0
        for depth in range(1, len(train_data.available_attributes) + 1, int(len(train_data.available_attributes) * 0.2)):
            for min_size in range(1, int(len(test_data) * 0.1), int(len(test_data) * 0.01)):
                classifier = DecisionTree(GiniAttributeSelector(), depth, min_size)
                classifier.train(train_data)
                accuracy, confusion_matrix = classifier.evaluate(test_data)
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_depth = depth
                    best_minsize = min_size
        return best_depth, best_minsize

    if OPTIMAL_FLAG in sys.argv:
        depth, min_size = find_optimal_parameters()

    if detailedOutput:
        print('Using settings for ' + color.BOLD + key + color.END)
        print('  => Depth=' + color.BOLD + str(depth) + color.END)
        print('  => Minsize=' + color.BOLD + str(min_size) + color.END)
        print()

    start = time.time()
    classifier = DecisionTree(GiniAttributeSelector(), depth, min_size, parallel, leaf_size)
    classifier.train(train_data)
    accuracy, confusion_matrix = classifier.evaluate(test_data)
    metrics = Metric.process(accuracy, confusion_matrix, train_data.class_counts.keys())
    Reporter.to_stdout(metrics, detailedOutput)

    if detailedOutput:
        accuracy, confusion_matrix = classifier.evaluate(train_data)
        metrics = Metric.process(accuracy, confusion_matrix, train_data.class_counts.keys())
        Reporter.to_stdout(metrics, detailedOutput)
        print('Finished in: ' + color.BOLD + str(time.time() - start) + color.END)
