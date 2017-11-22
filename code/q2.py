from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# training data set
X_train = [
    [1, 0.5],
    [2, 1.2],
    [2.5, 2],
    [3, 2],
    [1.5, 2],
    [2.3, 3],
    [1.2, 1.9],
    [0.8, 1]
]
y_train = [1, 1, 1, 1, -1, -1, -1, -1]

clf = KNeighborsClassifier(n_neighbors = 3, algorithm = 'brute')
clf.fit(X_train, y_train)

# test data set
X_test = [
    [2.7, 2.7],
    [2.5, 1],
    [1.5, 2.5],
    [1.2, 1]
]
y_test = [1, 1, -1, -1]

accuracy = clf.score(X_test, y_test)
print('1-NN accuracy:', accuracy)
print('D:', clf.predict(X_test))
