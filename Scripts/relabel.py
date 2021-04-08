"""
This script relabels teeth so that the labels are more logical.
For example, a set of teeth labelled [10, 12, 13, 14]
becomes [11, 12, 13, 14].
"""

def relabel(images):
	# currently we consider each xray to have 0 or 1 gaps in numbering
	# an xray has 1 gap is it is 2 rows of teeth, 0 gaps if it is 1 row
	gaps = 0

	for image in images:
		image.outputBoxes.sort(key=lambda box: int(box.label[6:]))

		# find the biggest gap between teeth. useful if there's 2 rows of teeth
		# biggest_gap = 1
		# biggest_index = 0
		# for i in range(len(image.outputBoxes) - 1):
		# 	tooth_num = image.outputBoxes[i].label[6:]
		# 	neighbor_num = image.outputBoxes[i + 1].label[6:]
		# 	number_gap = neighbor_num - tooth_num
		# 	if number_gap > biggest_gap:
		# 		biggest_gap = number_gap
		# 		biggest_index = i

		# adjust any labels except for the biggest gap
		for i in range(len(image.outputBoxes) - 1):
			tooth_num = int(image.outputBoxes[i].label[6:])
			neighbor_num = int(image.outputBoxes[i + 1].label[6:])

			# if i != biggest_index:
			if neighbor_num - tooth_num == 2:

				# we need to move a label left or right
				if i < len(image.outputBoxes) - 2:
					r_num = int(image.outputBoxes[i + 2].label[6:])
					if r_num - neighbor_num > 1:
						image.outputBoxes[i + 1].label = "tooth_" + str(neighbor_num - 1)
					elif (i == 0):
						image.outputBoxes[i].label = "tooth_" + str(tooth_num + 1)

				elif i > 1:
					l_num = int(image.outputBoxes[i - 1].label[6:])
					if tooth_num - l_num > 1:
						image.outputBoxes[i].label = "tooth_" + str(tooth_num + 1)
					elif i == len(image.outputBoxes) - 2:
						image.outputBoxes[i + 1].label = "tooth_" + str(neighbor_num - 1)
