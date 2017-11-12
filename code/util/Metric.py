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
            'precision': TP / (TP + FP),
            'recall': TP / P,
            'specificity': TN / (TN + FP)
        }
    
    '''
    Implementation based on the formula found in Wikipedia.
    Ref: https://en.wikipedia.org/wiki/F1_score
    '''
    def _f_beta(TP, FP, FN, beta = 1.0):
        return (1.0 + beta**2) * TP / ((1.0 + beta**2) * TP + (beta**2) * FP + FN)