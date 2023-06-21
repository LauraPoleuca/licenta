import numpy as np

def kmeans(values, k, max_iter = 100000):
    # have a random selection for the centeroids
    # for each point in values, calculate the distance to each centeroid and assign it to the one with the smallest distance
    # calculate the mean for the points in that 
    centroids = np.random.choice(values, k, False)
    # for each centroid i should obtain an array of distances
    # choose the         
    return centroids


values = np.array([1.5, 3.2, 0.78, 5.22, 1.444, 2.01, 4.4, 0.32, 0.1])
centroids = kmeans(values, 2)

print(centroids)