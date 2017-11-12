__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

class Metric:
    def process(accuracy, confusion_matrix, classes):
        result = {}
        result[ 'overall_accuracy' ] = accuracy * 100
        result[ 'confusion_matrix' ] = confusion_matrix
        result[ 'class_order' ] = sorted(list(classes))
        result[ 'class_metrics' ] = {}
        
        for _class in result[ 'class_order' ]:
            result[ 'class_metrics' ][ _class ] = Metric.class_metrics(_class, confusion_matrix)
      
        return result
    
    '''
    Parameters:
        - _class: label to consider
        - matrix: confusion matrix (multi class)
    
    For meaning of variables see: https://en.wikipedia.org/wiki/Confusion_matrix
    '''
    def class_metrics(_class, matrix):
        row = matrix[ _class ]
        P = row[ 'total' ]
        
        TP = row.get(_class, 0)
        TN = 0
        FN = P - TP
        FP = 0
        
        for actual_label, count in matrix.items():
            if not actual_label == _class:
                FP += matrix[ actual_label ].get(_class, 0)
                TN += matrix[ actual_label ][ 'total' ] - matrix[ actual_label ].get(_class, 0)
        
        N = FP + TN
        
        return {
            'accuracy': (TP + TN) / (N + P),
            'f-1 score': Metric._f_beta(TP, FP, FN),
            'f-0.5 score': Metric._f_beta(TP, FP, FN, 0.5),
            'f-2 score': Metric._f_beta(TP, FP, FN, 2),
            'precision': 0.0 if TP == 0 else TP / (TP + FP),
            'recall': TP / P,
            'specificity': TN / (TN + FP)
        }
    
    '''
    Implementation based on the formula found in Wikipedia.
    Ref: https://en.wikipedia.org/wiki/F1_score
    '''
    def _f_beta(TP, FP, FN, beta = 1.0):
        return (1.0 + beta**2) * TP / ((1.0 + beta**2) * TP + (beta**2) * FP + FN)

if __name__ == '__main__':
    matrix = {
        'cat': { 'cat': 5, 'dog': 3, 'rabbit': 0, 'total': 8 },
        'dog': { 'cat': 2, 'dog': 3, 'rabbit': 1, 'total': 6 },
        'rabbit': { 'cat': 0, 'dog': 2, 'rabbit': 11, 'total': 13 }
    }
    metrics = Metric.class_metrics('cat', matrix)
    assert metrics[ 'accuracy' ] == 0.8148148148148148
    assert metrics[ 'f-1 score' ] == 0.6666666666666666
    assert metrics[ 'f-0.5 score' ] == 0.6410256410256411
    assert metrics[ 'f-2 score' ] == 0.6944444444444444
    assert metrics[ 'precision' ] == 0.7142857142857143
    assert metrics[ 'recall' ] == 0.625
    assert metrics[ 'specificity' ] == 0.8947368421052632