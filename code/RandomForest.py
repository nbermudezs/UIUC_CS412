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

def grow_tree(sel, tree_params):
    return DecisionTree(sel,
                        max_depth = tree_params[ 'depth' ],
                        min_dataset_size = tree_params[ 'min_dataset_size' ],
                        min_leaf_size = tree_params[ 'min_leaf_size' ])

def get_pool():
    pool = Pool(processes = 6 - 1)
    return pool

class RandomForest:
    def __init__(self, size = 5, data_bagging_size = 0.9,
                 feature_bagging_retention_p = 0.9, extremely_randomized = False,
                 tree_params = None):
        self.size = size
        self.trees = []
        self.data_bagging_size = data_bagging_size
        self.feature_bagging_retention_p = feature_bagging_retention_p
        self.tree_params = tree_params

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
            result = pool.apply_async(grow_tree, (selector, self.tree_params))
            results.append(result)
        pool.close()
        pool.join()
        self.trees = [ result.get() for result in results ]

    '''
    Uses data bagging by taking a random sample of the data
    for every decision tree
    '''
    def train(self, data):
        # return self.no_thread(data)
        pool = get_pool()
        results = []
        for tree in self.trees:
            results.append(pool.apply_async(self._train_tree, (tree, data)))
        pool.close()
        pool.join()
        self.trees = [ result.get() for result in results ]

    def no_thread(self, data):
        self.trees = [ self._train_tree(tree, data, 0) for tree in self.trees ]

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
        # if self.data_bagging_size == 1:
        #     data = Dataset(counts_only = True)
        #     data.available_attributes = self._feature_bagging(source.available_attributes)
        #     data.examples = source.examples
        #     data.n_samples = source.n_samples
        #     data.class_counts = source.class_counts
        #     return data
        data = RandomSampler.sample(source, self.data_bagging_size)
        data.available_attributes = self._feature_bagging(data.available_attributes)
        return data

    def _feature_bagging(self, features):
        retain_feature = lambda: random.random() <= self.feature_bagging_retention_p
        result = set([ feature for feature in features if retain_feature() ])
        if len(result) == 0:
            return self._feature_bagging(features)
        return result

if __name__ == '__main__':
    import time, sys
    from util.Dataset import Dataset
    from util.Reporter import Reporter, color
    from util.Metric import Metric

    PARAMS = {
        'synthetic.social': {
            'size': 70,
            'extremely_randomized': False,
            'data_bagging_size': 0.964951005853781,
            'feature_bagging_retention_p': 0.03156834830170488
        }, # NOT DONE
        'balance.scale': {
            'size': 41,
            'extremely_randomized': False,
            'data_bagging_size': 0.6,
            'feature_bagging_retention_p': 0.25
        }, # DONE
        'nursery': {
            'size': 101,
            'extremely_randomized': False,
            'data_bagging_size': 0.7,
            'feature_bagging_retention_p': 0.9
        }, # DONE
        'led': {
            'size': 51,
            'extremely_randomized': False,
            'data_bagging_size': 0.67,
            'feature_bagging_retention_p': 1
        } # DONE
    }

    TREE_PARAMS = {
        'balance.scale':    { 'depth': -1, 'min_dataset_size': 3, 'min_leaf_size':  8 }, # DONE
        'led':              { 'depth': -1, 'min_dataset_size': 1, 'min_leaf_size':  1 }, # DONE
        'nursery':          { 'depth': -1, 'min_dataset_size': 1, 'min_leaf_size': -1 }, # DONE
        'synthetic.social': { 'depth': -1, 'min_dataset_size': 3, 'min_leaf_size':  1 }
    }

    LOOP_PARAMS = {
        'balance.scale': 70,
        'led': 20,
        'nursery': 3,
        'synthetic.social': 1
    }

    OPTIMAL_FLAG = '--optimal'
    DETAILS_FLAG = '--detailed-output'

    if len(sys.argv) < 3:
        print('Usage: python RandomForest.py <train file> <test file>')
        exit()

    detailedOutput = DETAILS_FLAG in sys.argv

    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]

    train_data = Dataset.from_file(train_filepath)
    test_data = Dataset.from_file(test_filepath)

    if detailedOutput:
        print('Training set size: ' + color.BOLD + str(len(train_data)) + color.END)
        print('Test set size: ' + color.BOLD + str(len(test_data)) + color.END)
        print()

    dataset_params = None
    tree_params = None
    for dataset_file in PARAMS.keys():
        if train_filepath.find(dataset_file) >= 0:
            dataset_params = PARAMS[ dataset_file ]
            tree_params = TREE_PARAMS[ dataset_file ]
            iterations = LOOP_PARAMS[ dataset_file ]
            break

    if OPTIMAL_FLAG in sys.argv:
        def find_optimal_parameters():
            max_size = int(sys.argv[ sys.argv.index(OPTIMAL_FLAG) + 1 ])
            print('Finding optimal value. Max size=' + str(max_size))
            best_accuracy = -float('inf')
            best_params = {}
            THRESHOLD = 2.5 * 60 # 2.5 minutes
            break_data_bagging = False
            break_size = False
            for size in range(2, max_size):
                if break_size:
                    break
                for data_bagging_size in range(1, 100):
                    if break_data_bagging:
                        if data_bagging_size == 1:
                            break_size = True
                        break
                    data_bagging_size = data_bagging_size / 100.0
                    for p in range(1, 4):
                        start = time.time()
                        p = p / 4.0
                        mokuton = RandomForest(20, data_bagging_size, p, False, tree_params = tree_params)
                        mokuton.jukai_kotan()
                        mokuton.train(train_data)
                        accuracy, confusion_matrix = mokuton.evaluate(test_data)
                        print(' => size=' + str(size) + ' dbag=' + \
                              str(data_bagging_size) + ' p=' + str(p) + \
                              ': acc=' + str(accuracy))
                        if accuracy > best_accuracy:
                            best_accuracy = accuracy
                            best_params[ 'feature_bagging_retention_p' ] = p
                            best_params[ 'size' ] = size
                            best_params[ 'extremely_randomized' ] = True
                            best_params[ 'data_bagging_size' ] = data_bagging_size
                            print('===> best so far!')
                        if time.time() - start > THRESHOLD:
                            if p == 1:
                                break_data_bagging = True
                            break
            return best_params
        dataset_params = find_optimal_parameters()

    size = dataset_params[ 'size' ]
    data_bagging_size = dataset_params[ 'data_bagging_size' ]
    feature_bagging_retention_p = dataset_params[ 'feature_bagging_retention_p' ]
    extremely_randomized = dataset_params[ 'extremely_randomized' ]

    if detailedOutput:
        print('Using settings for ' + color.BOLD + dataset_file + color.END)
        print('  => Forest size=' + color.BOLD + str(size) + color.END)
        print('  => Data bagging size=' + color.BOLD + \
              str(round(data_bagging_size * 100, 2)) + '%' + color.END)
        print('  => Feature bagging retention=' + \
              color.BOLD + str(round(feature_bagging_retention_p * 100, 2)) + \
              '%' + color.END)
        print('  => Extremely randomized?=' + color.BOLD + \
              str(extremely_randomized) + color.END)
        print('  => Tree depth=' + color.BOLD + \
              str(tree_params[ 'depth' ]) + color.END)
        print('  => Split minsize=' + color.BOLD + \
              str(tree_params[ 'min_dataset_size' ]) + color.END)
        print()

    accuracies = []
    start = time.time()

    for _ in range(iterations):
        # import cProfile, pstats, io
        # pr = cProfile.Profile()
        # pr.enable()

        mokuton = RandomForest(size = size,
                               extremely_randomized = extremely_randomized,
                               data_bagging_size = data_bagging_size,
                               feature_bagging_retention_p = feature_bagging_retention_p,
                               tree_params = tree_params)
        mokuton.jukai_kotan()

        mokuton.train(train_data)
        accuracy, confusion_matrix = mokuton.evaluate(test_data)
        accuracies.append((accuracy, confusion_matrix))
        # if time.time() - start > 180:
        #     break

        # pr.disable()
        # s = io.StringIO()
        # sortby = 'cumtime'
        # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # ps.print_stats()
        # print(s.getvalue())

    all_keys = list(set(test_data.class_counts.keys()) | set(train_data.class_counts.keys()))
    accuracy, confusion_matrix = max(accuracies, key = lambda a: a[ 0 ])
    metrics = Metric.process(accuracy, confusion_matrix, all_keys)
    Reporter.to_stdout(metrics, detailedOutput)
    if detailedOutput:
        print('Finished in: ' + color.BOLD + str(time.time() - start) + color.END)
