__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

from util.LibSVMReader import LibSVMReader
from util.Reporter import Reporter

class DecisionTree:
    def __init__(self):
        pass
    
    def train(self, data):
        pass
    
    def evaluate(self, data):
        pass
    
    def _predict(self, example):
        pass
    

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print('Usage: python DecisionTree.py <train file> <test file>')
        exit()
    
    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]
    
    train_data = LibSVMReader(train_filepath)
    test_data = LibSVMReader(test_filepath)
    
    classifier = DecisionTree()
    classifier.train(train_data)
    metrics = classifier.evaluate(test_data)
    Reporter.to_stdout(metrics)