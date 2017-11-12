__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Reporter:
    def to_stdout(metrics):
        Reporter._print_confusion_matrix(metrics[ 'confusion_matrix' ], metrics[ 'class_order' ])
        Reporter._print_overall_accuracy(metrics[ 'overall_accuracy' ])
        Reporter._print_class_metrics(metrics[ 'class_metrics' ])
    
    def _print_confusion_matrix(matrix, class_order):
        print(color.UNDERLINE + color.BOLD + 'Confusion matrix' + color.END)
        for _class in class_order:
            matrix_row = matrix.get(_class, {})
            total = matrix_row.get('total', 0)
            row = []
            for _predicted_class in class_order:
                count = matrix_row.get(_predicted_class, 0)
                row.append('%5s' % str('%4.0f' % count))
            print(' '.join(row))
        print('Class order: ' + color.BOLD + ', '.join(map(lambda x: str(x), class_order)) + color.END)
        print('\n')
    
    def _print_overall_accuracy(acc):
        print('Overall accuracy: ' + color.BOLD + str(round(acc, 2)) + '%' + color.END)
        print('\n')
    
    def _print_class_metrics(metrics):
        classes = metrics.keys()
        for _class in classes:
            class_metrics = metrics[ _class ]
            print(color.UNDERLINE + color.BOLD + 'Metrics for class ' + str(_class) + color.END)
            for metric, value in class_metrics.items():
                print(('%12s' % metric.title()) + ': ' + \
                      color.BOLD + str(round(value * 100, 2)) + '%' + color.END)
            print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
            print('\n')
    
if __name__ == '__main__':
    confusion_matrix = {
        'c1': { 'c1': 98,  'c2': 1,  'c3': 1,      'total': 100 },
        'c2': { 'c1': 0,   'c2': 86.0, 'c3': 4.0,  'total': 100 },
        'c3': { 'c1': 1.1, 'c2': 2.3,  'c3': 96.4, 'total': 100 }
    }
    
    class_metrics = {
        'c1': {
            'sensitivity': 0.3,
            'specificity': 0.5,
            'precision': 1.0,
            'recall': 2.0,
            'f-1 score': 0.9,
            'f-0.5 score': 0.4,
            'f-2 score': 0.6
        },
        'c2': {
            'sensitivity': 0.4,
            'specificity': 0.6,
            'precision': 0.3,
            'recall': 0.7,
            'f-1 score': 0.3,
            'f-0.5 score': 0.7,
            'f-2 score': 0.41
        },
        'c3': {
            'sensitivity': 0.1,
            'specificity': 0.9,
            'precision': 0.7,
            'recall': 0.88,
            'f-1 score': 0.76,
            'f-0.5 score': 0.37,
            'f-2 score': 0.61
        }
    }
    
    metrics = {
        'class_order': [ 'c1', 'c2', 'c3' ],
        'confusion_matrix': confusion_matrix,
        'overall_accuracy': 76.4,
        'class_metrics': class_metrics
    }
    Reporter.to_stdout(metrics)