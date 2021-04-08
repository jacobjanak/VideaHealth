import sys
import os

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box

# Import accuracy script for testing
from Tests.accuracy import accuracy
from Tests.visualizer import visualizer

# Import teeth arrangement script to correct teeth classification
from Scripts.teeth_arrangement import teeth_arrangements

# File paths
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth.csv"
file_pred = data_dir + "/2_input_model_predictions.csv"

# Read the input CSV file
input_raw = CSVReader(file_pred).output
images_input = Converter(input_raw).result

# Import the ground truth data
gt_raw = CSVReader(file_gt).output
images_gt = Converter(gt_raw).result

# ############ Test post processing scripts
# print("\nTesting haehn script:")
# from Scripts.haehn import haehn
# images_pred = haehn(images_input)
# # teeth_arrangements(images_pred)
# accuracy(images_pred, images_gt)
# # visualizer('haehn', images_pred, images_gt)

# print("\nTesting best_box script:")
# from Scripts.best_box import best_box
# images_pred = best_box(images_input)
# # teeth_arrangements(images_pred)
# accuracy(images_pred, images_gt)
# # visualizer('best_box', images_pred, images_gt)

from Scripts.non_maximum_suppression import nonmaximum_suppression

# print("\nTesting nms script:")
for y in range(78, 79):
    iouThreshold = y*0.01
    for x in range(36, 37):
        images_input = Converter(input_raw).result
        scoreThreshold = x*0.01
        print(iouThreshold, scoreThreshold)
        images_pred = nonmaximum_suppression(images_input, scoreThreshold, iouThreshold)
        # teeth_arrangements(images_pred)
        accuracy(images_pred, images_gt)
        visualizer('nms', images_pred, images_gt)

print()
