__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

class LibSVMReader:
    def __init__(self, input_filepath):
        self.input_filepath = input_filepath
        
    def read(self):
        with open(self.input_filepath, 'r') as data_file:
            for line in data_file:
                line = line[:-1]
                split_point = line.find(' ')
                label = line[ :split_point ]
                features = line[ split_point + 1: ].split(' ')
                features = { k:v for k, v in map(lambda a: a.split(':'), features) }
                yield (features, label)

if __name__ == '__main__':
    reader = LibSVMReader('../../data/balance.scale/balance.scale.train')
    for example in reader.read():
        assert type(example) == tuple
        assert type(example[ 0 ]) == dict
        assert type(example[ 1 ]) == str
    