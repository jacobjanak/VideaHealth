import math
import random

from matplotlib import pyplot as plt

# Thresholds
scoreThresh = 0.3
iouThresh = 0.5


# This function is just the caller function for kmeans_iter
def kmeans(images, k=2):
	assert k == 2, "Currently can only support k=2" # TEMP

	for image in images:
		boxes = [b for b in image.inputBoxes if b.score > scoreThresh]

		finishedClusters = []
		clusters = kmeans_iter(boxes, k)
		for i in range(5):
			nextCluster = clusters.pop(0)
			if len(nextCluster) > k:
				results = kmeans_iter(nextCluster, k)
				clusters.extend(results)
			else:
				finishedClusters.append(nextCluster)

		display(finishedClusters)
			
			


def kmeans_iter(boxes, k=2):

	# NOTE: fail more gracefully
	assert len(boxes) >= k, "Number of boxes can't be less than k"

	# Step 1: Pick k random centroids to start the clusters
	# N
	while True:
		random.shuffle(boxes)
		clusters = [[c] for c in boxes[:k]]
		# NOTE: prevent infinite loops
		# NOTE: adapt for when k != 2
		if clusters[0][0].iou(clusters[1][0]) < iouThresh:
			break

	done = False
	while not done:

		# Step 2: Cluster remaining boxes with the closest centroid
		# N * k
		for box in boxes:
			closestCluster = None
			closestDistance = 0
			for cluster in clusters:
				distance = euclidean(box, cluster[0])
				if closestCluster is None or distance < closestDistance:
					closestCluster = cluster
					closestDistance = distance
			if box != closestCluster[0]:
				closestCluster.append(box)
					
		# Step 3: Recalculate the best centroid for each cluster
		# N ** 2
		newClusters = []
		for cluster in clusters:
			bestCentroid = None
			bestScore = 0
			for box1 in cluster:
				score = 0
				for box2 in cluster:
					score += euclidean(box1, box2) * box2.score**2
				if bestCentroid is None or score < bestScore:
					bestCentroid = box1
					bestScore = score
			newClusters.append([bestCentroid])

		# Step 4: Repeat steps 2 and 3 until centroids don't change	
		# k
		done = True
		for i in range(k):
			if clusters[i][0] != newClusters[i][0]:
				done = False
				# display(clusters) # TEMP
				clusters = newClusters
				break

	return clusters


def euclidean(box1, box2):
	# NOTE: add a lookup dictionary
	p1 = box1.midpoint()
	p2 = box2.midpoint()

	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def display(clusters):
    plt.figure()
    i = 0
    colors = ["blue", "orange", "green", "red", "purple", "cyan", "olive", "gray", "pink", "brown", "gold", "coral", "lime", "azure", "crimson", "cornflowerblue"]
    for cluster in clusters:
        for box in cluster:
            plt.plot([box.x1s, box.x2s], [box.y1s, box.y1s], color=colors[i])
            plt.plot([box.x1s, box.x1s], [box.y1s, box.y2s], color=colors[i])
            plt.plot([box.x1s, box.x2s], [box.y2s, box.y2s], color=colors[i])
            plt.plot([box.x2s, box.x2s], [box.y1s, box.y2s], color=colors[i])
        i = 0 if i == len(colors) - 1 else i + 1
    plt.show()

