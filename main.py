import argparse
import sys
import os

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.InputBox import InputBox

# Import accuracy script for testing
from Tests.accuracy import accuracy
from Tests.visualizer import visualizer

# File paths


my_parser = argparse.ArgumentParser()

my_parser.add_argument('-gt', '-groundtruthfile', help='CSV File of GroundTruth to compare with')
my_parser.add_argument('-pf', '-predfile', help='CSV File of the Neural Network Prediction Data')
my_parser.add_argument('-i', '-imgdirectory', help='Directory where the Images related to the Dataset is located')

args = my_parser.parse_args()

'''
#Older Method
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth_2a.csv"
file_pred = data_dir + "/2_input_model_predictions_2.csv"
'''
img_folder = args.i
file_gt = args.gt
file_pred = args.pf

# Read the input CSV file
input_raw = CSVReader(file_pred).output
images_input = Converter(input_raw).result

# Import the ground truth data
gt_raw = CSVReader(file_gt).output
images_gt = Converter(gt_raw).result

############ Test post processing scripts
print("\nTesting haehn script:")
from Scripts.haehn import haehn
images_pred = haehn(images_input)
accuracy(images_pred, images_gt)
#visualizer(images_pred, images_gt)

print("\nTesting best_box script:")
from Scripts.best_box import best_box
images_pred = best_box(images_input)
accuracy(images_pred, images_gt)
#visualizer(images_pred, images_gt)

print("\nTesting nms script:")
from Scripts.non_maximum_suppression import nonmaximum_suppression
images_pred = nonmaximum_suppression(images_input)
accuracy(images_pred, images_gt)
#visualizer(images_pred, images_gt)



print("PredictedBoxes saved as PrediectedBoxes.csv")
