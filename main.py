import sys
import os

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box
from Classes.CSVWriter import CSVWriter

# Import accuracy script for testing
from Scripts.missing_tooth import missing_tooth
from Tests.accuracy import accuracy
#from Tests.accuracy3 import getMap
from Tests.metrics import Metrics, Metrics2
from Tests.visualizer import visualizer
from Tests.precision_recall import precision_recall_iou, f1_iou, precision_recall_ious, f1_ious

# Import teeth arrangement script to correct teeth classification
from Scripts.teeth_arrangement import teeth_arrangements
#from Scripts.relabel import relabel
from Scripts.relabel import relabel

# File paths
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth.csv"
file_pred = data_dir + "/2_input_model_predictions.csv"
file_bw_pa = data_dir + "/bw_pa.csv"

# Read the input CSV file
input_raw = CSVReader(file_pred, file_bw_pa).output
images_input = Converter(input_raw).result

# Import the ground truth data
gt_raw = CSVReader(file_gt).output
images_gt = Converter(gt_raw).result

# Specifically check if you want only Bitewing (BW) or Periapical ){PA)
#images_input, images_gt = Converter.get_bw_pa(images_input, images_gt, want_bw=False)

iou_threshold = 0.70

print("\nTesting without Filtering script:")
metrics = Metrics2.calculate_percision_recall_curv(images_input, Converter(gt_raw).result)
metrics.visualize()
perc, recall = metrics.last_percision_recall()
print(f"Metrics: percision={perc} recall={recall}")

images_gt = Converter(gt_raw).result
print('precision, recall = {}'.format(precision_recall_ious(images_input, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_input, images_gt, iou_threshold)))
images_gt = Converter(gt_raw).result
images_input = Converter(input_raw).result

print("\nTesting nms script:")
from Scripts.non_maximum_suppression import nonmaximum_suppression # threshold=0.35, iouThreshold=0.5
images_pred = nonmaximum_suppression(images_input, threshold=0.35, iouThreshold=0.5)
metrics = Metrics2.calculate_percision_recall_curv(images_pred, Converter(gt_raw).result)
#metrics.visualize()
perc, recall = metrics.last_percision_recall()
print(f"Metrics: percision={perc} recall={recall}")
print('precision, recall = {}'.format(precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
#images_gt = Converter(gt_raw).result

print("Teeth Arrangements on NMS")
images_pred = teeth_arrangements(images_pred)
metrics = Metrics2.calculate_percision_recall_curv(images_pred, Converter(gt_raw).result)
#metrics.visualize()
perc, recall = metrics.last_percision_recall()
print(f"Metrics: percision={perc} recall={recall}")
print('precision, recall = {}'.format(precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
#images_gt = Converter(gt_raw).result

print("Missing Tooth on NMS")
images_pred = missing_tooth(images_pred)
metrics = Metrics2.calculate_percision_recall_curv(images_pred, Converter(gt_raw).result)
#metrics.visualize()
perc, recall = metrics.last_percision_recall()
print(f"Metrics: percision={perc} recall={recall}")
print('precision, recall = {}'.format(precision_recall_ious(images_pred, images_gt, iou_threshold)))
print('f1 = {}'.format(f1_ious(images_pred, images_gt, iou_threshold)))
#images_gt = Converter(gt_raw).result

