import sys
import os

from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.InputBox import InputBox

# File paths
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth_2a.csv"
file_pred = data_dir + "/2_input_model_predictions_2.csv"

# Read the input CSV file
Reader = CSVReader(file_pred)

# Convert the data in the CSV into a more usable format
DataConverter = Converter(Reader.output)

# Retrieve the image list
images = DataConverter.result

# Logging
print(images)
print(images[0])
print(images[0].id)
print(len(images[0].inputBoxes))
# test git branch