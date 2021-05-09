
# Dependencies
import math
import random

# Classes
from Classes.Box import Box

# Testing
from matplotlib import pyplot as plt

# Thresholds
scoreThresh = 0.01 			# completely ignore all boxes with lower scores
iouClusterThresh = 0.6		# prevent clusters from overlapping
iouCentroidThresh = 0.2 	# prevents centroids from overlapping
iouOutputThresh = 0.3		# prevent output boxes from overlapping
intersectionThresh = 0.6	# prevent output boxes from being inside eachother
totalScoreThresh = 0.4		# removes output boxes with lower total scores
xThresh = 0.05				# for removing boxes that overlap multiple boxes
yThresh = 0.2				# for removing boxes that overlap multiple boxes


# This function is just the caller function for kmeans_iter
def kmeans(images, k=4):
	for image in images:
		boxes = [b for b in image.inputBoxes if b.score > scoreThresh]
		finishedClusters = []

		# Validate input
		if k > len(boxes):
			k = len(boxes)
			if k < 2:
				image.outputBoxes = image.inputBoxes
				continue

		# Start by clustering boxes into k groups
		clusters = kmeans_iter(boxes, k)
		if clusters is None:
			clusters = kmeans_iter(boxes, 2)
			if clusters is None:
				image.outputBoxes = image.inputBoxes
				continue

		# Continuously bisect clusters until they meet a certain criteria
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
		output = [average_box(c) for c in finishedClusters]
		trim_output(output)
		fix_labels(output)
		# display([output])
		image.outputBoxes = output

	return images


def kmeans_iter(boxes, k=2):
	assert len(boxes) >= k, "Number of boxes can't be less than k"

	# Step 1: Pick k random centroids to start the clusters
	# N
	if k == 2:
		centroids = findFurthestBoxes(boxes)
		if centroids is None:
			return None
		clusters = [[centroids[0]], [centroids[1]]]
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


def findFurthestBoxes(boxes):

	# Start by checking the x axis for far away boxes
	leftmostBox = None
	rightMostBox = None
	for box in boxes:
		if leftmostBox is None or box.x1s < leftmostBox.x1s:
			leftmostBox = box
	for box in boxes:
		if rightMostBox is None or box.x2s > rightMostBox.x2s:
			if box != leftmostBox:
				rightMostBox = box

	# Backup option is to check the y axis for far away boxes
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
		return [topmostBox, bottommostBox]
	else:
		return [leftmostBox, rightMostBox]


def average_box(cluster):
	# Return the average of all the boxes in a cluster
	avg = Box("", 0, 0, 0, 0, 1)
	totalScore = 0
	labels = dict()
	for box in cluster:
		totalScore += box.score
		avg.x1s += box.x1s * box.score
		avg.y1s += box.y1s * box.score
		avg.x2s += box.x2s * box.score
		avg.y2s += box.y2s * box.score
		if box.label in labels:
			labels[box.label] += box.score
		else:
			labels[box.label] = box.score
	avg.x1s /= totalScore
	avg.y1s /= totalScore
	avg.x2s /= totalScore
	avg.y2s /= totalScore

	avg.label = max(labels, key=labels.get)

	avg.totalScore = totalScore
	avg.cluster = cluster

	return avg


def trim_output(boxes):
	for i in range(len(boxes)-1, -1, -1):

		# Merge boxes that are too similar
		for j in range(i+1, len(boxes)):
			if j >= len(boxes): break
			if boxes[i].iou(boxes[j]) > iouOutputThresh:				
				boxes[i].cluster.extend(boxes[j].cluster)
				boxes[i] = average_box(boxes[i].cluster)
				boxes.pop(j)
				j -= 1

		# Remove boxes that are inside another box
		for j in range(i+1, len(boxes)):
			if j >= len(boxes): break
			if boxes[i].area() < boxes[j].area():
				smallBoxIndx = i
			else: 
				smallBoxIndx = j
			smallerArea = boxes[smallBoxIndx].area()
			ratio = boxes[i].intersect(boxes[j]) / smallerArea
			if ratio > intersectionThresh:
				boxes.pop(smallBoxIndx)
				if smallBoxIndx == j: j -= 1
				else: break

		# Remove boxes with low confidence
		if boxes[i].totalScore < totalScoreThresh:
			boxes.pop(i)
			continue

		# Remove boxes that are inside multiple other boxes
		"""
		indexOne = None
		indexTwo = None
		midpoint = boxes[i].midpoint()
		width = boxes[i].x2s - boxes[i].x1s
		height = boxes[i].y2s - boxes[i].y1s
		for j in range(len(boxes)):
			if ((abs(midpoint[0] - boxes[j].x1s) / width < xThresh
				or abs(midpoint[0] - boxes[j].x2s) / width < xThresh)
			and (abs(midpoint[1] - boxes[j].midpoint()[1]) / height < yThresh)):
				if indexOne is None:
					indexOne = j
				else:
					indexTwo = j
					for neighbor in [boxes[indexOne], boxes[indexTwo]]:
						neighbor.cluster.append(
							Box(
								boxes[i].label,
								boxes[i].x1s,
								boxes[i].y1s,
								boxes[i].x2s,
								boxes[i].y2s,
								neighbor.totalScore / 2
							)
						)
					boxes[indexOne] = average_box(boxes[indexOne].cluster)
					boxes[indexTwo] = average_box(boxes[indexTwo].cluster)
					boxes.pop(i)
					break
		"""

	return boxes


def fix_labels(boxes):
	labels = dict()
	for box in boxes:
		if box.label in labels:
			labels[box.label].append(box)
		else:
			labels[box.label] = [box]

	for k in labels:
		if len(labels[k]) > 1:
			for i in range(1, len(labels[k])):
				if i < len(labels[k]):
					labels[k][i-1].cluster.extend(labels[k][i].cluster)
					labels[k][i-1] = average_box(labels[k][i-1].cluster)
					labels[k].pop(i)
					i -= 1

	boxes = []
	for k in labels:
		boxes.extend(labels[k])
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

