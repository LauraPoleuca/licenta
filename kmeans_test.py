import numpy as np
import matplotlib.pyplot as plt

def kmeans(X, k, max_iter=400000):
    idx = np.random.choice(len(X), k, replace=False)
    centroids = X[idx, :]
    idk = centroids[:, np.newaxis]
    idk = X - idk

    for i in range(max_iter):
        # Assign each point to the closest centroid
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        clusters = np.argmin(distances, axis=0)

        # Update centroids to be the mean of the points in each cluster
        for j in range(k):
            centroids[j, :] = X[clusters == j, :].mean(axis=0)

    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=clusters, s=50, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.5)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('K-means Clustering')
    plt.show()
    
    return labels, centroids


X = np.random.rand(100, 2)
labels, centroids = kmeans(X, 2)