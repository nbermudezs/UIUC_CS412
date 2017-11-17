__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

try:
    from .LibSVMReader import LibSVMReader
except:
    from LibSVMReader import LibSVMReader

class Dataset:
    def __init__(self, counts_only = False):
        if not counts_only:
            self.examples = []
            self.available_attributes = set()
        self.class_counts = {}
        self.n_samples = 0

    @staticmethod
    def from_file(input_filepath):
        dataset = Dataset()
        reader = LibSVMReader(input_filepath)
        for (features, label) in reader.read():
            dataset.append((features, label))
        return dataset

    def items(self):
        return self.examples

    def append(self, item):
        self.examples.append(item)
        self.available_attributes.update(item[ 0 ].keys())
        self.class_counts[ item[ 1 ] ] = self.class_counts.get(item[ 1 ], 0) + 1
        self.n_samples += 1

    def count_label(self, label):
        self.class_counts[ label ] = self.class_counts.get(label, 0) + 1
        self.n_samples += 1

    def __len__(self):
        return self.n_samples

    '''
    Returns a dictionary where the keys are the different classes
    and the values are Dataset objects containing the examples for
    that class only.
    DO NOT USE ANYMORE
    '''
    def _split_by_class(self):
        result = {}
        for (features, label) in self.examples:
            class_dataset = result.get(label, Dataset())
            class_dataset.append((features, label))
            result[ label ] = class_dataset
        return result

    '''
    Returns a dictionary where the keys are the different values
    of the provided attribute and the values of the dictionary are
    Dataset objects containing the objects that match that criteria.
    '''
    def split_by_attribute(self, attribute):
        result = {}
        for (features, label) in self.examples:
            key = features[ attribute ]
            dataset = result.get(key, Dataset())
            dataset.append((features, label))
            dataset.available_attributes = self.available_attributes
            result[ key ] = dataset
        return result

    def split_counts_by_attribute(self, attribute):
        result = {}
        for features, label in self.examples:
            key = features[ attribute ]
            dataset = result.get(key, Dataset(counts_only = True))
            dataset.count_label(label)
            result[ key ] = dataset
        return result

    '''
    For debugging only
    '''
    def attribute_values(self, attribute):
        result = set()
        for (features, label) in self.examples:
            value = features[ attribute ]
            result.add(value)
        return result

    def is_single_class(self):
        return len(self.class_counts.keys()) == 1

if __name__ == '__main__':
    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    assert not dataset.is_single_class()

    split = dataset._split_by_class()
    assert type(split) == dict
    assert set(split.keys()) == set([ 1, 2, 3 ])
    assert type(split[ 1 ]) == Dataset
    assert split[ 1 ].is_single_class()

    assert type(split[ 2 ]) == Dataset
    assert split[ 2 ].is_single_class()

    assert type(split[ 3 ]) == Dataset
    assert split[ 3 ].is_single_class()

    split = dataset.split_by_attribute(2)
    assert type(split) == dict

    total = 0
    for key in split.keys():
        assert type(split[ key ]) == Dataset
        assert len(split[ key ].class_counts.keys()) > 0
        assert len(split[ key ].examples) > 0
        total += len(split[ key ].examples)
    assert total == len(dataset)

    values = dataset.attribute_values(1)
    assert type(values) == set
    assert len(values) > 0
