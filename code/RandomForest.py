__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

from util.RandomAttributeSelector import RandomAttributeSelector
from util.RandomSampler import RandomSampler
from DecisionTree import DecisionTree

class RandomForest:
    def __init__(self, size = 5):
        self.size = 5
        self.trees = []
    
    '''
    Wondering the meaning of the name of this function?
    http://animemagics.wikia.com/wiki/Mokuton_Hijutsu_%E2%80%A2_Jukai_Kotan
    '''
    def jukai_kotan(self):
        selector = RandomAttributeSelector()
        self.trees = [ DecisionTree(selector) for i in range(self.size) ]
    
    '''
    Uses data bagging by taking a random sample of the data 
    for every decision tree
    '''
    def train(self, data):
        for tree in self.trees:
            tree.train(RandomSampler.sample(data))
    
    def evaluate(self, data):
        correct = 0
        total = 0
        for (features, label) in data.items():
            predicted_label = self._predict(features)
            if predicted_label == label:
                correct += 1
            total += 1
            
        return (correct / total, None)
    
    def _predict(self, example):
        votes = {}
        for tree in self.trees:
            label = tree._predict(example)
            votes[ label ] = votes.get(label, 0) + 1
        return max(votes.items(), key = lambda x: x[ 1 ])[ 0 ]
        
if __name__ == '__main__':
    import time, sys
    from util.Dataset import Dataset
    from util.Reporter import Reporter, color
    
    mokuton = RandomForest()
    mokuton.jukai_kotan()
    
    if len(sys.argv) < 3:
        print('Usage: python RandomForest.py <train file> <test file>')
        exit()
    
    train_filepath = sys.argv[ 1 ]
    test_filepath = sys.argv[ 2 ]
    
    train_data = Dataset.from_file(train_filepath)
    test_data = Dataset.from_file(test_filepath)
    
    start = time.clock()
    mokuton.train(train_data)
    accuracy, confusion_matrix = mokuton.evaluate(test_data)
    print('Accuracy', accuracy)
    
    print('Finished in: ' + color.BOLD + str(time.clock() - start) + color.END)
    