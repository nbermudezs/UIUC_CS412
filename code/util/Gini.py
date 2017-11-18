__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

class GiniIndex:
    @staticmethod
    def calculate(D):
        return 1 - sum([
            (n_D_j / D.n_samples)**2
            for _, n_D_j in D.class_counts.items()])

    @staticmethod
    def split(D, attribute):
        # True means it should not fill in the examples. We don't need them
        split = D.split_counts_by_attribute(attribute)
        return sum([
            len(D_j) / D.n_samples * GiniIndex.calculate(D_j)
            for _, D_j in split.items() ])

    @staticmethod
    def impurity_reduction(D, attribute):
        return GiniIndex.calculate(D) - GiniIndex.split(D, attribute)


if __name__ == '__main__':
    from Dataset import Dataset
    from Reporter import color

    dataset = Dataset.from_file('../../data/balance.scale/balance.scale.train')
    print('gini index: ', GiniIndex.calculate(dataset))

    for attribute in dataset.available_attributes:
        reduction = GiniIndex.impurity_reduction(dataset, attribute)
        print('Impurity reduction for attribute ' + color.BOLD + \
              str(attribute) + color.END + ': ' +color.BOLD + str(reduction) + color.END)
