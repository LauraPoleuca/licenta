import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Generate random data points
np.random.seed(0)
X = np.random.rand(100, 2)

# Perform K-means clustering with k=2
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)
labels = kmeans.predict(X)
centers = kmeans.cluster_centers_

# Create two arrays for points in each cluster
cluster1 = X[labels == 0]
cluster2 = X[labels == 1]

# Plot the clusters and cluster centers
plt.scatter(cluster1[:, 0], cluster1[:, 1], c='red', label='Cluster 1')
plt.scatter(cluster2[:, 0], cluster2[:, 1], c='blue', label='Cluster 2')
plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', s=100, label='Cluster Centers')
plt.legend()
plt.title('Binary K-means Clustering')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
