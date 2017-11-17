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
    def _split(train_data, test_data, valid_size = 0.1):
        examples = train_data.examples + test_data.examples
        classes = train_data.classes ^ test_data.classes
        attributes = train_data.available_attributes ^ test_data.available_attributes
        combined = Dataset.from_data(examples, classes, attributes)

        indices = list(range(0, len(examples)))
        random.shuffle(indices)

        train = Dataset()
        test = Dataset()
        for i, index in enumerate(indices):
            if i < len(examples) * valid_size:
                test.append(examples[ index ])
            else:
                train.append(examples[ index ])

        return train, test

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
