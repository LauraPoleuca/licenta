import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

# Generate synthetic data with two well-separated clusters
X, y = datasets.make_blobs(n_samples=100, n_features=2, centers=2, cluster_std=1.0, random_state=42)

# Create an SVM classifier
clf = svm.SVC(kernel='linear', C=1000)  # Linear SVM

# Fit the classifier to the data
clf.fit(X, y)

# Create a mesh to plot the decision boundary
xx, yy = np.meshgrid(np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100),
                     np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 100))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot the decision boundary and support vectors
plt.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100, facecolors='none', edgecolors='k')
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, marker='o', edgecolors='k')

plt.title('SVM Classification')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.show()
