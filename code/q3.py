import numpy as np

c1_points_x = [1, 1, 2, 2, 2, 3]
c1_points_y = [3, 2, 1, 2, 3, 2]

centroid = np.mean(c1_points_x), np.mean(c1_points_y)
print('Centroid for c1, iter 1:', centroid)

c2_points_x = [5, 4, 4, 5, 5, 6, 6]
c2_points_y = [3, 3, 5, 4, 5, 4, 5]
centroid = np.mean(c2_points_x), np.mean(c2_points_y)
print('Centroid for c2, iter 1:', centroid)



# 3b

from sklearn.cluster import DBSCAN

X_train = [
    [1, 3],
    [1, 2],
    [2, 1],
    [2, 2],
    [2, 3],
    [3, 2],
    [5, 3],
    [4, 3],
    [4, 5],
    [5, 4],
    [5, 5],
    [6, 4],
    [6, 5]
]

alg = DBSCAN(eps = 1.5, min_samples = 2)
prediction = alg.fit_predict(X_train)
print('3b)', prediction)

# 3c

from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

ytdist = np.array([662., 877., 255., 412., 996., 295., 468., 268., 400., 754., 564., 138., 219., 869., 669.])
Z = hierarchy.linkage(ytdist, 'single')

Z = [
    [1., 2., 1.0, 2.0],
    [3., 4., 1.0, 2.0]
]

plt.figure()
hierarchy.dendrogram(Z)
plt.show()
