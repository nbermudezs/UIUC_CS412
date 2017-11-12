__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

try:
    from .Gini import GiniIndex
except:
    from Gini import GiniIndex

class GiniAttributeSelector:
    '''
    Parameters:
        - dataset: instance of Dataset
        - used_attributes: set containing the attributes already used
                           up in the tree
    '''
    def __call__(self, dataset, used_attributes):
        best_attribute = None
        best_reduction = -float('inf')
        attributes = dataset.attributes
        for attribute in (attributes - used_attributes):
            reduction = GiniIndex(dataset).impurity_reduction(attribute)
            if reduction > best_reduction:
                best_reduction = reduction
                best_attribute = attribute
        return best_attribute

if __name__ == '__main__':
    from Dataset import Dataset
    
    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    selector = GiniAttributeSelector()
    best_attribute = selector(dataset, set())
    assert best_attribute == 2
    
    best_attribute = selector(dataset, { 2 })
    assert best_attribute == 3
    
    best_attribute = selector(dataset, { 2, 3 })
    assert best_attribute == 4
    
    split = dataset.split_by_attribute(2)
    best_attribute = selector(split[ 5 ], { 2 })
    assert best_attribute == 1