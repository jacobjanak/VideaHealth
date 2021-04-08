
def accuracy2(images_pred, images_gt):
	total_score = 0
	total_boxes = 0

	for image in images_pred:
		for box in image.outputBoxes:
			total_boxes += 1
			best_score = 0

			for image_gt in images_gt:
				for gt_box in image_gt.inputBoxes:
					
					score = box.iou(gt_box)

					if score > best_score:
						best_score = score

			total_score += best_score

	# print("Number of boxes is {}".format(total_boxes))
	print("Average IOU per box is {}".format(total_score / total_boxes))
