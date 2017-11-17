__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

import functools

class GiniIndex:
    def __init__(self, D):
        self.D = D
        self._index = None

    def index(self):
        if not self._index:
            self._index = GiniIndex.calculate(self.D)
        return self._index

    @staticmethod
    def calculate(D):
        return 1 - sum([
            (n_D_j / D.n_samples)**2
            for _, n_D_j in D.class_counts.items()])

    @functools.lru_cache(maxsize = 1024)
    def split(self, attribute):
        # True means it should not fill in the examples. We don't need them
        split = self.D.split_by_attribute(attribute, True)
        return sum([
            len(D_j) / self.D.n_samples * GiniIndex.calculate(D_j)
            for _, D_j in split.items() ])

    @functools.lru_cache(maxsize = 1024)
    def impurity_reduction(self, attribute):
        return self.index() - self.split(attribute)


if __name__ == '__main__':
    from Dataset import Dataset
    from Reporter import color

    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    gini = GiniIndex(dataset)
    print('gini index: ', gini.index())

    for attribute in dataset.available_attributes:
        reduction = gini.impurity_reduction(attribute)
        print('Impurity reduction for attribute ' + color.BOLD + \
              attribute + color.END + ': ' +color.BOLD + str(reduction) + color.END)
