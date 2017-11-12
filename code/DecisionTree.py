__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

import random

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

class DecisionTreeLeaf:
    def __init__(self, label):
        self.label = label
    
    def __call__(self, example):
        return self.label


class DecisionTree:
    def __init__(self, selector, max_depth = -1, min_dataset_size = 1):
        self.tree = None
        self.selector = selector
        self.max_depth = max_depth
        self.min_dataset_size = min_dataset_size
    
    '''
    Parameters:
        - data: instance of Dataset
    '''
    def train(self, data):
        selected_attribute = self.selector(data, set())
        self.tree = self._build_tree(data, selected_attribute, { selected_attribute })
    
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
            return DecisionTreeLeaf(min(data.classes))
        if depth == self.max_depth or len(data) <= self.min_dataset_size:
            split = data.split_by_class()
            best = max(split.items(), key = lambda x: len(x[ 1 ]))[ 0 ]
            return DecisionTreeLeaf(best)
            
        subtree = DecisionTreeNode(attribute)
        split = data.split_by_attribute(attribute)
        for value, dataset in split.items():
            best_attribute = self.selector(dataset, used_attributes)
            branch = self._build_tree(dataset, best_attribute, used_attributes ^ { best_attribute }, depth + 1)
            subtree.grow(value, branch)
        return subtree
    

if __name__ == '__main__':
    import time, sys
    from util.Dataset import Dataset
    from util.Reporter import Reporter, color
    from util.GiniAttributeSelector import GiniAttributeSelector
    from util.Metric import Metric
    
    if len(sys.argv) < 3:
        print('Usage: python DecisionTree.py <train file> <test file>')
        exit()
    
    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]
    
    train_data = Dataset.from_file(train_filepath)
    test_data = Dataset.from_file(test_filepath)
    
    start = time.clock()
    classifier = DecisionTree(GiniAttributeSelector())
    classifier.train(train_data)
    accuracy, confusion_matrix = classifier.evaluate(test_data)
    metrics = Metric.process(accuracy, confusion_matrix, test_data.classes)
    Reporter.to_stdout(metrics)
    print('Finished in: ' + color.BOLD + str(time.clock() - start) + color.END)