
# Dependencies
import math
import random

# Classes
from Classes.Box import Box

# Testing
from matplotlib import pyplot as plt

# Thresholds
scoreThresh = 0.05 			# completely ignore all boxes with lower scores
iouClusterThresh = 0.6		# prevent clusters from overlapping
iouCentroidThresh = 0.8 	# prevents centroids from overlapping NOTE change from 2
totalScoreThresh = 0.5		# removes output boxes with lower total scores


# This function is just the caller function for kmeans_iter
def kmeans(images, k=2):
	for image in images:
		boxes = [b for b in image.inputBoxes if b.score > scoreThresh]

		# Continuously bisect clusters until they meet a certain criteria
		finishedClusters = []
		clusters = kmeans_iter(boxes, k)
		if clusters is None:
			image.outputBoxes = image.inputBoxes
			continue

		for nextCluster in clusters:

			# Break when clusters are too small
			if len(nextCluster) == 1:
				finishedClusters.append(nextCluster)
				continue

			# We know they're far enough apart so just split them
			if len(nextCluster) == 2:
				finishedClusters.append([nextCluster[0]])
				finishedClusters.append([nextCluster[1]])

			# Run K Means and check validity of results
			results = kmeans_iter(nextCluster, 2)
			if results is None:
				finishedClusters.append(nextCluster)
				continue

			# Stop when the resulting clusters are too close
			avg1 = average_box(results[0])
			avg2 = average_box(results[1])
			intersection = avg1.intersect(avg2)
			if (avg1.iou(avg2) > iouClusterThresh
				or intersection == avg1.area()
				or intersection == avg2.area()):
				finishedClusters.append(nextCluster)
				continue

			# Add resulting clusters to end of list
			clusters.extend(results)
				
		# display(finishedClusters)
		# NOTE before average box, trim out the bad boxes?
		output = [average_box(c) for c in finishedClusters]
		
		trim_output(output)
		# display([output])
		image.outputBoxes = output

	return images


def kmeans_iter(boxes, k=2):
	assert len(boxes) >= k, "Number of boxes can't be less than k"

	# Step 1: Pick k random centroids to start the clusters
	# N
	if k == 2:
		# clusters = []
		leftmostBox = None
		rightMostBox = None
		for box in boxes:
			if leftmostBox is None or box.x1s < leftmostBox.x1s:
				leftmostBox = box
		for box in boxes:
			if rightMostBox is None or box.x2s > rightMostBox.x2s:
				if box != leftmostBox:
					rightMostBox = box
		if leftmostBox.iou(rightMostBox) > iouCentroidThresh:
			topmostBox = None
			bottommostBox = None
			for box in boxes:
				if topmostBox is None or box.y1s < topmostBox.y1s:
					topmostBox = box
			for box in boxes:
				if bottommostBox is None or box.y2s > bottommostBox.y2s:
					if box != topmostBox:
						bottommostBox = box
			if topmostBox.iou(bottommostBox) > iouCentroidThresh:
				return None
			clusters = [[topmostBox], [bottommostBox]]
		else:
			clusters = [[leftmostBox], [rightMostBox]]
	else:
		random.shuffle(boxes)
		clusters = [[c] for c in boxes[:k]]
		overlaps = 0
		done = False
		while not done:
			for i in range(k):
				for j in range(k):
					if i == j: continue
					if clusters[i][0].iou(clusters[j][0]) > iouCentroidThresh:
						if k + overlaps >= len(boxes):
							return None
						clusters[i][0] = boxes[k + overlaps]
						overlaps += 1
						i = 0
						break
				if i == k - 1:
					done = True

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


def average_box(cluster):
	# Return the average of all the boxes in a cluster
	avg = Box("", 0, 0, 0, 0, 1) # TEMP score
	totalScore = 0
	for box in cluster:
		totalScore += box.score
		avg.x1s += box.x1s * box.score
		avg.y1s += box.y1s * box.score
		avg.x2s += box.x2s * box.score
		avg.y2s += box.y2s * box.score
	avg.x1s /= totalScore
	avg.y1s /= totalScore
	avg.x2s /= totalScore
	avg.y2s /= totalScore

	avg.totalScore = totalScore

	return avg


def trim_output(boxes):
	for i in range(len(boxes)-1, -1, -1):
		box = boxes[i]
		if box.totalScore < totalScoreThresh:
			boxes.pop(i)

	return boxes


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

