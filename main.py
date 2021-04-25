from Scripts.best_cluster_haehn import best_cluster_haehn
from Scripts.non_maximum_suppression import nonmaximum_suppression
from Scripts.best_box import best_box
from Scripts.haehn import haehn
import sys
import os
from argparse import ArgumentParser
from pathlib import PurePath

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box
from Classes.CSVWriter import CSVWriter

# Import accuracy script for testing
from Tests.accuracy import accuracy
#from Tests.accuracy2 import accuracy2
from Tests.NMSaccuracy import NMSaccuracy
from Tests.accuracy2 import accuracy2
from Tests.visualizer import visualizer
from Tests.precision_recall import precision_recall_iou, f1_iou, precision_recall_ious, f1_ious

# Import teeth arrangement script to correct teeth classification
from Scripts.teeth_arrangement import teeth_arrangements
#from Scripts.relabel import relabel
from Scripts.relabel import relabel

parser = ArgumentParser(
    description="Postprocessing/filtering for tooth detection results")
parser.add_argument("-d", "--data", help="data directory")
parser.add_argument("-i", "--img", help="image directory")
parser.add_argument("-g", "--ground-truth",
                    dest="groundtruth", help="ground truth data")
parser.add_argument("-p", "--predictions", help="prediction data")
parser.add_argument("--iou", dest="threshold", help="IoU threshold")
args = parser.parse_args()

# File paths
project_dir = Path(__file__).parent.absolute()
current_dir = Path.cwd()
if args.data:
    data_dir = current_dir / args.data
else:
    data_dir = project_dir / "CS410_VideaHealth_sample_data"

if args.img:
    img_folder = current_dir / args.img
else:
    img_folder = data_dir / "images"

if args.groundtruth:
    file_gt = current_dir / args.groundtruth
else:
    file_gt = data_dir / "1_ground_truth_2a.csv"

if args.predictions:
    file_pred = current_dir / args.predictions
else:
    file_pred = data_dir / "2_input_model_predictions_2.csv"


# Read the input CSV file
input_raw = CSVReader(file_pred).output
images_input = Converter(input_raw).result

# Import the ground truth data
gt_raw = CSVReader(file_gt).output
images_gt = Converter(gt_raw).result

iou_threshold = args.threshold

# Test post processing scripts
print("\nTesting haehn script:")
images_pred = haehn(images_input)
# teeth_arrangements(images_pred)
# relabel(images_pred)
accuracy(images_pred, images_gt)
print('precision, recall = {}'.format(
    precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
# visualizer(img_folder, 'haehn', images_pred, images_gt)

print("\nTesting best_box script:")
images_pred = best_box(images_input)
# teeth_arrangements(images_pred)
# relabel(images_pred)
accuracy(images_pred, images_gt)
#accuracy2(images_pred, images_gt)
print('precision, recall = {}'.format(
    precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
# visualizer(img_folder, 'best_box', images_pred, images_gt)

print("\nTesting nms script:")
images_pred = nonmaximum_suppression(images_input, 0.5, 0.5)
# teeth_arrangements(images_pred)
# relabel(images_pred)
accuracy(images_pred, images_gt)
#accuracy2(images_pred, images_gt)
# visualizer(img_folder, 'nms', images_pred, images_gt)

print("\nTesting best cluster haehn script:")
images_pred = best_cluster_haehn(images_input)
# teeth_arrangements(images_pred)
# relabel(images_pred)
accuracy(images_pred, images_gt)
#accuracy2(images_pred, images_gt)
print('precision, recall = {}'.format(
    precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
visualizer(img_folder, 'nms', images_pred, images_gt)

# print("\nTesting best cluster haehn script:")
# images_pred = best_cluster_haehn(images_input)
# # teeth_arrangements(images_pred)
# accuracy(images_pred, images_gt)
# print('precision, recall = {}'.format(
#     precision_recall_ious(images_pred, images_gt, iou_threshold)))
# print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
# # visualizer(img_folder, 'nms', images_pred, images_gt)

# Tony's Magic Number Code
# from Scripts.non_maximum_suppression import nonmaximum_suppression
#
# # print("\nTesting nms script:")
# for y in range(1, 101):
#     iouThreshold = y*0.01
#     for x in range(1, 101):
#         images_input = Converter(input_raw).result
#         scoreThreshold = x*0.01
#         print(iouThreshold, scoreThreshold)
#         images_pred = nonmaximum_suppression(images_input, scoreThreshold, iouThreshold)
#         # teeth_arrangements(images_pred)
#         NMSaccuracy(images_pred, images_gt)
#         # visualizer(img_folder, 'nms', images_pred, images_gt)

print()
