# import sys
# import os
import math

from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box

# File paths
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_dir = os.path.dirname(current_dir)
# data_dir = project_dir + "/CS410_VideaHealth_sample_data"
# img_folder = data_dir + "/images"
# file_gt = data_dir + "/1_ground_truth_2a.csv"
# file_pred = data_dir + "/2_input_model_predictions_2.csv"

# # Read and convert the input CSV file
# input_raw = CSVReader(file_pred).output
# images_pred = Converter(input_raw).result

# # Read and convert the ground truth CSV file
# gt_raw = CSVReader(file_gt).output
# # images_gt = Converter(gt_raw).result
# images_gt = Converter(input_raw).result

# Making a small change for testing
# images_pred.pop()
# images_pred[0].inputBoxes[0].x1s = 60

def accuracy(images_pred, images_gt):

    # See if the number of images generated is accurate
    difference = len(images_pred) - len(images_gt)
    if difference != 0:
        print("Found {} more images in our result vs. ground truth".format(difference))

    # See if the number of boxes generated is accurate
    # Can't compare the number of boxes unless the number of images is correct
    # else:
    #     difference = 0
    #     for i, image_pred in enumerate(images_pred):
    #         image_gt = images_gt[i]
    #         difference += len(image_pred.outputBoxes) - len(image_gt.inputBoxes)
    #     if difference != 0:
    #         print("Found {} more boxes in our result vs. ground truth".format(difference))

    # Now we compare the actual boxes themselves
    else:
        total_matching_boxes = 0
        missing_boxes = 0
        extra_boxes = 0
        deviation = 0
        numMatch = 0
        offset = 20
        numOfGt = 0

        for i, image_gt in enumerate(images_gt):

            image_pred = None
            # find the image label that match this ground truth image label ex) 'img_002' == 'img_002'
            for j in range(len(images_pred)):
                if images_pred[j].id == image_gt.id:
                    image_pred = images_pred[j]

            # iterate through all output boxes in our prediction
            for k, gt_box in enumerate(image_gt.inputBoxes):
                box_gt = None
                numOfGt += 1
                for j, box_pred in enumerate(image_pred.outputBoxes):
                    
                    # if abs(gt_box.x1s -box_pred.x1s) < offset and abs(gt_box.x2s -box_pred.x2s) < offset and abs(gt_box.y1s -box_pred.y1s) < offset and abs(gt_box.y2s -box_pred.y2s) < offset:
                    #     print("match")
                    #     numMatch += 1
                    if gt_box.iou(box_pred) > 0.5:
                        # print("match")
                        numMatch += 1
        # 
        if numMatch == numOfGt:
            t = input()
            #     # Calculate the amount of pixels our script is off by
            #     if box_gt is not None:
            #         total_matching_boxes += 1

            #         x1_dev = abs(box_pred.x1s - box_gt.x1s)
            #         y1_dev = abs(box_pred.y1s - box_gt.y1s)
            #         deviation += math.sqrt(x1_dev ** 2 + y1_dev ** 2)

            #         x2_dev = abs(box_pred.x2s - box_gt.x2s)
            #         y2_dev = abs(box_pred.y2s - box_gt.y2s)
            #         deviation += math.sqrt(x2_dev ** 2 + y2_dev ** 2)

            #         # Old code that doesn't use hypotenuse:
            #         # deviation += abs(box_pred.x1s - box_gt.x1s)
            #         # deviation += abs(box_pred.y1s - box_gt.y1s)
            #         # deviation += abs(box_pred.x2s - box_gt.x2s)
            #         # deviation += abs(box_pred.y2s - box_gt.y2s)

            #     # Identify extra boxes our script has generated
            #     else: extra_boxes += 1

            # # Identify missing boxes
            # for j, box_gt in enumerate(image_gt.inputBoxes):
            #     box_pred = None
            #     for k in range(len(image_pred.outputBoxes)):
            #         if box_gt.label == image_pred.outputBoxes[k].label:
            #             box_pred = image_pred.outputBoxes[k]
            #             break
            #     if box_pred is None:
            #         missing_boxes += 1

        # print("Found {} missing boxes in our output".format(missing_boxes))
        # print("Found {} extra boxes in our output".format(extra_boxes))
        # print("Average deviation per box is {}".format(deviation / total_matching_boxes))
