"""Implementation of k-means clustering algorithm. 

These functions are designed to work with cartesian data points
"""

import numpy as np
from matplotlib import pyplot as plt
from Classes.Box import Box


def convert_to_4d_array(points):
    points = np.array(points)
    return points


def visualize_clusters(clusters):
    """
    Visualizes the clusters as boxes
    """
    plt.figure()
    color_index = 0
    colors = ["blue", "orange", "green", "red", "purple", "cyan", "olive", "gray", "pink", "brown", "gold", "coral", "lime", "azure", "crimson", "cornflowerblue"]
    for cluster in clusters:
        points = convert_to_4d_array(cluster)

        for point in points:
            plt.plot([point[0], point[2]], [point[1], point[1]], color=colors[color_index])
            plt.plot([point[0], point[2]], [point[3], point[3]], color=colors[color_index])
            plt.plot([point[0], point[0]], [point[1], point[3]], color=colors[color_index])
            plt.plot([point[2], point[2]], [point[1], point[3]], color=colors[color_index])

        color_index += 1
        if color_index == len(colors):
            color_index = 0

    plt.show()


def SSE(points):
    """
    Calculates the sum of squared errors for the given list of data points.

    Args:
        points: array-like
            Data points

    Returns:
        sse: float
            Sum of squared errors
    """
    points = convert_to_4d_array(points)
    centroid = np.mean(points, 0)
    errors = np.linalg.norm(points-centroid, ord=2)
    return np.sum(errors)


def kmeans(images, k=32, epochs=20, max_iter=1000, verbose=False):
    """
    Clusters the list of points into `k` clusters using k-means clustering
    algorithm.

    Args:
        points: array-like
            Data points
        k: int
            Number of output clusters
        epochs: int
            Number of random starts (to find global optima)
        max_iter: int
            Max iteration per epoch
        verbose: bool
            Display progress on every iteration

    Returns:
        clusters: list with size = k
            List of clusters, where each cluster is a list of data points
    """

    for image in images:
        boxes = image.inputBoxes

        points = []
        for box in boxes:
            points.append([box.x1s, box.y1s, box.x2s, box.y2s])
        points = convert_to_4d_array(points)

        assert len(points) >= k, "Number of data points can't be less than k"

        best_sse = np.inf
        for ep in range(epochs):

            # Randomly initialize k centroids
            np.random.shuffle(points)
            centroids = points[0:k, :]

            last_sse = np.inf
            for it in range(max_iter):

                # Cluster assignment
                clusters = [None] * k
                for p in points:
                    index = np.argmin(np.linalg.norm(centroids-p, 2, 1))
                    if clusters[index] is None:
                        clusters[index] = np.expand_dims(p, 0)
                    else:
                        clusters[index] = np.vstack((clusters[index], p))

                # loop through all elements and remove None values
                for i in range(len(clusters) - 1, -1, -1):
                    if clusters[i] is None:
                        clusters.pop(i)

                # Centroid update
                centroids = [np.mean(c, 0) for c in clusters]

                # SSE calculation
                sse = np.sum([SSE(c) for c in clusters])
                gain = last_sse - sse
                if verbose:
                    print((f'Epoch: {ep:3d}, Iter: {it:4d}, '
                           f'SSE: {sse:12.4f}, Gain: {gain:12.4f}'))

                # Check for improvement
                if sse < best_sse:
                    best_clusters, best_sse = clusters, sse

                # Epoch termination condition
                if np.isclose(gain, 0, atol=0.00001):
                    break
                last_sse = sse

        # Actual K Means code is now done, the rest is extra stuff

        # Average out all the boxes in a cluster into one single box
        outputBoxes = []
        for cluster in best_clusters:
            totalScore = 0
            avgBox = Box("templabel", 0, 0, 0, 0)
            bestScore = 0
            bestLabel = ""
            labels = dict()
            
            for box in cluster:

                # try to find the actual box because we need label and score
                # I had to remove label and score for K means to work, which is not ideal
                boxReference = None
                for realBox in image.inputBoxes:
                    if (realBox.x1s == box[0]
                        and realBox.y1s == box[1]
                        and realBox.x2s == box[2]
                        and realBox.y2s == box[3]):
                        boxReference = realBox

                        """
                        if realBox.label in labels:
                            labels[realBox.label] += realBox.score
                        else:
                            labels[realBox.label] = realBox.score
                        """

                        if realBox.score > bestScore:
                            bestScore = realBox.score
                            bestLabel = realBox.label
                        break

                totalScore += boxReference.score
                avgBox.x1s += box[0] * boxReference.score
                avgBox.y1s += box[1] * boxReference.score
                avgBox.x2s += box[2] * boxReference.score
                avgBox.y2s += box[3] * boxReference.score

            """
            bestLabel = ""
            bestScore = 0
            for key in labels:
                if labels[key] > bestScore:
                    bestScore = labels[key]
                    bestLabel = key
            """
            
            avgBox.label = bestLabel

            # Threshold is 0.4
            if bestScore > 0.4:
                avgBox.x1s /= totalScore
                avgBox.y1s /= totalScore
                avgBox.x2s /= totalScore
                avgBox.y2s /= totalScore
                avgBox.score = .5
                outputBoxes.append(avgBox)

        visualize_clusters(clusters)
        image.outputBoxes = outputBoxes

    return images
