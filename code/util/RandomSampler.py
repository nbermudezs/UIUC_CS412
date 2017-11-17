__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

try:
    from .Dataset import Dataset
except:
    from Dataset import Dataset

import random

class RandomSampler:
    def sample(data, size = 0.9):
        total = len(data)
        new_data = Dataset()
        for _ in range(int(total * size)):
            new_data.append(random.choice(data.examples))
        return new_data

if __name__ == '__main__':
    train = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    test = Dataset.from_file('../../data/balance.scale/balance.scale.test')
    train, test = RandomSampler._split(train, test)
    assert type(train) == Dataset
    assert type(test) == Dataset
