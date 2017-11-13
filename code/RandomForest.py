__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

from util.GiniAttributeSelector import GiniAttributeSelector
from util.RandomAttributeSelector import RandomAttributeSelector
from util.RandomSampler import RandomSampler
from DecisionTree import DecisionTree
from multiprocessing import Pool, cpu_count

import random

def grow_tree(sel, size):
    return DecisionTree(sel, min_dataset_size = size)

def get_pool():
    pool = Pool(processes = cpu_count() - 1)
    return pool

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
        
        pool = get_pool()
        results = []
        for i in range(self.size):
            result = pool.apply_async(grow_tree, (selector, 10))
            results.append(result)
        pool.close()
        pool.join()
        self.trees = [ result.get() for result in results ]
    
    '''
    Uses data bagging by taking a random sample of the data 
    for every decision tree
    '''
    def train(self, data):
        pool = get_pool()
        results = []
        for tree in self.trees:
            results.append(pool.apply_async(self._train_tree, (tree, data)))
        pool.close()
        pool.join()
        self.trees = [ result.get() for result in results ]
    
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

    def _train_tree(self, tree, data):
        tree_data = self._tree_data(data)
        return tree.train(tree_data)
    
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
            'size': 13,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.4
        }, # DONE
        'balance.scale': {
            'size': 301,
            'extremely_randomized': False,
            'data_bagging_size': 0.7,
            'feature_bagging_retention_p': 0.8
        },
        'nursery': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 1
        },
        'led': {
            'size': 7,
            'extremely_randomized': False,
            'data_bagging_size': 0.9,
            'feature_bagging_retention_p': 0.2
        }
    }
    
    OPTIMAL_FLAG = '--optimal'
    
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
    
    if OPTIMAL_FLAG in sys.argv:
        def find_optimal_parameters():
            best_accuracy = -float('inf')
            best_params = {}
            for size in range(2, 11):
                for data_bagging_size in range(1, 9):
                    data_bagging_size = data_bagging_size / 10.0
                    for p in range(1, 9):
                        p = p / 10.0
                        mokuton = RandomForest(size, data_bagging_size, p, True)
                        mokuton.jukai_kotan()
                        mokuton.train(train_data)
                        accuracy, confusion_matrix = mokuton.evaluate(test_data)
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_params[ 'feature_bagging_retention_p' ] = p
                            best_params[ 'size' ] = size
                            best_params[ 'extremely_randomized' ] = True
                            best_params[ 'data_bagging_size' ] = data_bagging_size
            return best_params
        dataset_params = find_optimal_parameters()
        
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
    
    start = time.time()
    mokuton.train(train_data)
    accuracy, confusion_matrix = mokuton.evaluate(test_data)
    metrics = Metric.process(accuracy, confusion_matrix, test_data.classes)
    Reporter.to_stdout(metrics, True)
    print('Finished in: ' + color.BOLD + str(time.time() - start) + color.END)
    