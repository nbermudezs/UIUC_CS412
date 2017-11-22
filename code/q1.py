from sklearn.datasets import load_svmlight_file
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import AdaBoostClassifier

'''
    Cuisine: 1 = American, 2 = Korean, 3 = Thai
    Price: 1 = $, 2 = $$, 3 = $$$
    Delivery: 1 = Yes, 2 = No
    Popularity: 1 = P, 2 = NP
'''
X_train, y_train = load_svmlight_file('./q1.train.data')
X_train = X_train.toarray()

clf = BernoulliNB()
clf.fit(X_train, y_train)

'''
    Cuisine = Korean, Price = $, Delivery = 1
'''
prediction = clf.predict([[2, 1, 1 ]])
print('1b: Is Popular?', prediction[0] == 1)
print('Probabilities:', clf.predict_proba([[2, 1, 1]])[0])

bagging = AdaBoostClassifier(clf)
bagging.fit(X_train, y_train)
print('Ensemble probabilities:', bagging.predict_proba([[2, 1, 1]])[0])
