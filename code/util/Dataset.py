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
    def __init__(self):
        self.examples = []
        self.classes = set()
        self.attributes = set()
        self.available_attributes = set()

    @staticmethod
    def from_file(input_filepath):
        dataset = Dataset()
        reader = LibSVMReader(input_filepath)
        for (features, label) in reader.read():
            dataset.append((features, label))
        return dataset

    @staticmethod
    def from_data(examples, classes, attributes):
        dataset = Dataset()
        dataset.examples = examples
        dataset.classes = classes
        dataset.attributes = attributes
        return dataset

    def items(self):
        return self.examples

    def append(self, item):
        self.examples.append(item)
        self.classes.add(item[ 1 ])
        self.attributes = self.attributes.union(set(item[ 0 ].keys()))
        self.available_attributes = self.available_attributes.union(set(item[ 0 ].keys()))

    def __len__(self):
        return len(self.examples)

    '''
    Returns a dictionary where the keys are the different classes
    and the values are Dataset objects containing the examples for
    that class only.
    Dataset.classes will only have one element
    '''
    def split_by_class(self):
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
    Dataset.classes will have the different classes found in such dataset
    which may be a subset of the original list of classes.
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

    def attribute_values(self, attribute):
        result = set()
        for (features, label) in self.examples:
            value = features[ attribute ]
            result.add(value)
        return result

    def is_single_class(self):
        return len(self.classes) == 1

if __name__ == '__main__':
    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    assert type(dataset.classes) == set
    assert dataset.classes == set([ 1, 2, 3 ])
    assert not dataset.is_single_class()

    split = dataset.split_by_class()
    assert type(split) == dict
    assert set(split.keys()) == set([ 1, 2, 3 ])
    assert type(split[ 1 ]) == Dataset
    assert split[ 1 ].classes == set([ 1 ])
    assert split[ 1 ].is_single_class()

    assert type(split[ 2 ]) == Dataset
    assert split[ 2 ].classes == set([ 2 ])
    assert split[ 2 ].is_single_class()

    assert type(split[ 3 ]) == Dataset
    assert split[ 3 ].classes == set([ 3 ])
    assert split[ 3 ].is_single_class()

    split = dataset.split_by_attribute(2)
    assert type(split) == dict

    total = 0
    for key in split.keys():
        assert type(split[ key ]) == Dataset
        assert len(split[ key ].classes) > 0
        assert len(split[ key ].examples) > 0
        total += len(split[ key ].examples)
    assert total == len(dataset)

    values = dataset.attribute_values(1)
    assert type(values) == set
    assert len(values) > 0
