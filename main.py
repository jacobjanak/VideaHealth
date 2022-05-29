import sys
import os
from argparse import ArgumentParser
from pathlib import PurePath, Path

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box
from Classes.CSVWriter import CSVWriter

# Import scripts
from Scripts.non_maximum_suppression import nonmaximum_suppression
from Scripts.teeth_arrangement import teeth_arrangements
from Scripts.missing_tooth import missing_tooth
from Scripts.relabel import relabel

# Quanitifies the accuracy of our output
from Tests.precision_recall import precision_recall_iou, f1_iou, precision_recall_ious, f1_ious

# Visualizer to see the results on an image
from Tests.visualizer import visualizer






# Command line arguments
parser = ArgumentParser()
parser.add_argument("-V", "--visualize", action="store_true", help="Visualize the data")
args = parser.parse_args()

# File paths
project_dir = Path(__file__).parent.absolute()
current_dir = Path.cwd()
data_dir = project_dir / "CS410_VideaHealth_sample_data"
img_folder = str(data_dir / "images")
file_gt = str(data_dir / "1_ground_truth.csv")
file_pred = str(data_dir / "2_input_model_predictions.csv")
file_bw_pa = str(data_dir / "bw_pa.csv")

# Read the input CSV file
input_raw = CSVReader(file_pred, file_bw_pa).output
images_input = Converter(input_raw).result

# Import the ground truth data
gt_raw = CSVReader(file_gt).output
images_gt = Converter(gt_raw).result

iou_threshold = 0.39

print("\nTesting Without Script:")
(precision, recall) = precision_recall_ious(images_input, images_gt)
print('precision, recall = {}'.format((precision, recall)))
print('f1 = {}'.format(f1_ious(precision, recall)))
images_gt = Converter(gt_raw).result
images_input = Converter(input_raw).result

print("\nTesting NMS script:")
images_pred = nonmaximum_suppression(images_input, iou_threshold, iou_threshold)
(precision, recall) = precision_recall_ious(images_pred, images_gt, iou_threshold)
print('precision, recall = {}'.format((precision, recall)))
print('f1 = {}'.format(f1_ious(precision, recall)))

print("\nTeeth Arrangements on NMS")
images_pred = teeth_arrangements(images_pred)
(precision, recall) = precision_recall_ious(images_pred, images_gt, iou_threshold)
print('precision, recall = {}'.format((precision, recall)))
print('f1 = {}'.format(f1_ious(precision, recall)))

print("\nMissing Tooth on NMS")
images_pred = missing_tooth(images_pred)
(precision, recall) = precision_recall_ious(images_pred, images_gt, iou_threshold)
print('precision, recall = {}'.format((precision, recall)))
print('f1 = {}'.format(f1_ious(precision, recall)))

print("\nRelabel on NMS")
images_pred = relabel(images_pred)
(precision, recall) = precision_recall_ious(images_pred, images_gt, iou_threshold)
print('precision, recall = {}'.format((precision, recall)))
print('f1 = {}\n'.format(f1_ious(precision, recall)))

if args.visualize:
	visualizer(img_folder, "NMS", images_pred, images_gt)
