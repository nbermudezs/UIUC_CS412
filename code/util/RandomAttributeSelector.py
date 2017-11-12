__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

import random

class RandomAttributeSelector:
    '''
    Parameters:
        - dataset: instance of Dataset
        - used_attributes: set containing the attributes already used
                           up in the tree
    '''
    def __call__(self, dataset, used_attributes):
        available = list(dataset.attributes - used_attributes)
        if len(available) == 0:
            return None
        return random.choice(available)
    
if __name__ == '__main__':
    from Dataset import Dataset
    
    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    selector = RandomAttributeSelector()
    best_attribute = selector(dataset, set())
    assert type(best_attribute) == int
    
    best_attribute = selector(dataset, { 2 })
    assert type(best_attribute) == int
    assert best_attribute not in { 2 }
    
    best_attribute = selector(dataset, { 2, 3 })
    assert type(best_attribute) == int
    assert best_attribute not in { 2, 3 }
    
    best_attribute = selector(dataset, { 2, 3, 1, 5 })
    assert best_attribute == 4
    
    split = dataset.split_by_attribute(2)
    best_attribute = selector(split[ 5 ], { 2 })
    assert type(best_attribute) == int
    assert best_attribute not in { 2 }