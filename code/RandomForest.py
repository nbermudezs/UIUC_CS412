__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

from util.GiniAttributeSelector import GiniAttributeSelector
from util.RandomAttributeSelector import RandomAttributeSelector
from util.RandomSampler import RandomSampler
from DecisionTree import DecisionTree

import random

class RandomForest:
    def __init__(self, size = 5, data_bagging_size = 0.9,
                 feature_bagging_retention_p = 0.9, extremely_randomized = False):
        self.size = size
        self.trees = []
        self.data_bagging_size = data_bagging_size
        self.feature_bagging_retention_p = feature_bagging_retention_p
        
        '''
        When this flag is set to True the next feature used for splitting
        is selected randomly instead of using the Gini index.
        See https://en.wikipedia.org/wiki/Random_forest#Algorithm for ref.
        '''
        self.extremely_randomized = extremely_randomized
    
    '''
    Wondering the meaning of the name of this function?
    http://animemagics.wikia.com/wiki/Mokuton_Hijutsu_%E2%80%A2_Jukai_Kotan
    '''
    def jukai_kotan(self):
        if self.extremely_randomized:
            selector = RandomAttributeSelector()
        else:
            selector = GiniAttributeSelector()
        self.trees = [ DecisionTree(selector, min_dataset_size = 10)
                       for i in range(self.size) ]
    
    '''
    Uses data bagging by taking a random sample of the data 
    for every decision tree
    '''
    def train(self, data):
        for tree in self.trees:
            tree_data = self._tree_data(data)
            tree.train(tree_data)
    
    def evaluate(self, data):
        correct = 0
        total = 0
        confusion_matrix = {}
        for (features, label) in data.items():
            predicted_label = self._predict(features)
            if predicted_label == label:
                correct += 1
            total += 1
            
            matrix_row = confusion_matrix.get(label, {})
            matrix_row[ predicted_label ] = matrix_row.get(predicted_label, 0) + 1
            matrix_row[ 'total' ] = matrix_row.get('total', 0) + 1
            confusion_matrix[ label ] = matrix_row
            
        return (correct / total, confusion_matrix)
    
    def _predict(self, example):
        votes = {}
        for tree in self.trees:
            label = tree._predict(example)
            votes[ label ] = votes.get(label, 0) + 1
        return max(votes.items(), key = lambda x: x[ 1 ])[ 0 ]
    
    def _tree_data(self, source):
        data = RandomSampler.sample(source, self.data_bagging_size)
        data.available_attributes = self._feature_bagging(data.attributes)
        return data
    
    def _feature_bagging(self, features):
        retain_feature = lambda: random.random() <= self.feature_bagging_retention_p
        return set([ feature for feature in features if retain_feature() ])
        
if __name__ == '__main__':
    import time, sys
    from util.Dataset import Dataset
    from util.Reporter import Reporter, color
    from util.Metric import Metric
    
    PARAMS = {
        'synthetic.social': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.2
        }, # DONE
        'balance.scale': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.2
        },
        'nursery': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.2
        },
        'led': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.2
        }
    }
    
    if len(sys.argv) < 3:
        print('Usage: python RandomForest.py <train file> <test file>')
        exit()
    
    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]
    
    train_data = Dataset.from_file(train_filepath)
    test_data = Dataset.from_file(test_filepath)
    
    print('Training set size: ' + color.BOLD + str(len(train_data)) + color.END)
    print('Test set size: ' + color.BOLD + str(len(test_data)) + color.END)
    print()
    
    dataset_params = None
    for dataset_file in PARAMS.keys():
        if train_filepath.find(dataset_file) >= 0:
            dataset_params = PARAMS[ dataset_file ]
            break
    
    size = dataset_params[ 'size' ]
    data_bagging_size = dataset_params[ 'data_bagging_size' ]
    feature_bagging_retention_p = dataset_params[ 'feature_bagging_retention_p' ]
    extremely_randomized = dataset_params[ 'extremely_randomized' ]
        
    print('Using settings for ' + color.BOLD + dataset_file + color.END)
    print('  => Forest size=' + color.BOLD + str(size) + color.END)
    print('  => Data bagging size=' + color.BOLD + str(round(data_bagging_size * 100, 2)) + '%' + color.END)
    print('  => Feature bagging retention=' + color.BOLD + str(round(feature_bagging_retention_p * 100, 2)) + '%' + color.END)
    print('  => Extremely randomized?=' + color.BOLD + str(extremely_randomized) + color.END)
    print()
    
    mokuton = RandomForest(size = size,
                           extremely_randomized = extremely_randomized,
                           data_bagging_size = data_bagging_size,
                           feature_bagging_retention_p = feature_bagging_retention_p)
    mokuton.jukai_kotan()
    
    start = time.clock()
    mokuton.train(train_data)
    accuracy, confusion_matrix = mokuton.evaluate(test_data)
    metrics = Metric.process(accuracy, confusion_matrix, test_data.classes)
    Reporter.to_stdout(metrics)
    print('Finished in: ' + color.BOLD + str(time.clock() - start) + color.END)
    