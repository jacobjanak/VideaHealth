import sys
import os

from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.InputBox import InputBox

# File paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth_2a.csv"
file_pred = data_dir + "/2_input_model_predictions_2.csv"

# Read and convert the input CSV file
input_raw = CSVReader(file_pred).output
images_pred = Converter(input_raw).result

# Read and convert the ground truth CSV file
gt_raw = CSVReader(file_gt).output
# images_gt = Converter(gt_raw).result
images_gt = Converter(input_raw).result

# Making a small change for testing
# images_pred.pop()
# images_pred[0].inputBoxes[0].x1s = 60

# See if the number of images generated is accurate
difference = len(images_pred) - len(images_gt)
if difference != 0:
    print("Found {} more images in our result vs. ground truth".format(difference))

# See if the number of boxes generated is accurate
# Can't compare the number of boxes unless the number of images is correct
else:
    difference = 0
    for i, image_pred in enumerate(images_pred):
        image_gt = images_gt[i]
        difference += len(image_pred.inputBoxes) - len(image_gt.inputBoxes)
    if difference != 0:
        print("Found {} more boxes in our result vs. ground truth".format(difference))

    # Now we compare the actual boxes themselves
    else:
        deviation = 0
        for i, image_pred in enumerate(images_pred):
            image_gt = images_gt[i]

            for j, box_pred in enumerate(image_pred.inputBoxes):
                box_gt = image_gt.inputBoxes[j]
                deviation += abs(box_pred.x1s - box_gt.x1s)
                deviation += abs(box_pred.y1s - box_gt.y1s)
                deviation += abs(box_pred.x2s - box_gt.x2s)
                deviation += abs(box_pred.y2s - box_gt.y2s)

        print("Combined deviation of all boxes is {} pixels".format(deviation))
