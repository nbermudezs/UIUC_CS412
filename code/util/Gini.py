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
            self._index = 1 - sum([
                (n_D_j / len(self.D))**2
                for _, n_D_j in self.D.class_counts.items() ])
        return self._index

    @functools.lru_cache(maxsize = 1024)
    def split(self, attribute):
        split = self.D.split_by_attribute(attribute)
        return sum([
            len(D_j) / len(self.D) * GiniIndex(D_j).index()
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
