"""
This script relabels teeth so that the labels are more logical.
For example, a set of teeth labelled [10, 12, 13, 14]
becomes [11, 12, 13, 14].
"""

def relabel(images):
	for image in images:
		boxes = image.outputBoxes
		boxes.sort(key=lambda box: box.tooth_num())

		# adjust any labels except for the biggest gap
		for i in range(len(boxes) - 1):

			# get the tooth number of the tooth and its two neighbors
			tooth_num = boxes[i].tooth_num()
			l_num = boxes[i - 1].tooth_num() if i > 0 else None
			r_num = boxes[i + 1].tooth_num() if i < len(boxes) - 2 else None

			# identify lonely teeth
			if ((l_num is None or tooth_num - 1 != l_num) and 
			   	(r_num is None or tooth_num + 1 != r_num)):

				if l_num is None:
					boxes[i].new_label(r_num - 1)

				elif r_num is None:
					boxes[i].new_label(l_num + 1)

				# we now know we need to move boxes[i] but which direction?
				else:
				   	l_diff = tooth_num - l_num
				   	r_diff = r_num - tooth_num

				   	if l_diff < r_diff:
				   		boxes[i].new_label(l_num + 1)

				   	elif r_diff < l_diff:
				   		boxes[i].new_label(r_num - 1)

				   	# this else should happen rarely
				   	else:
				   		# NOTE: we should add much more logic here but for now this is fine
				   		if l_num is not None:
				   			boxes[i].new_label(l_num + 1)
				   		else:
				   			boxes[i].new_label(r_num - 1)
