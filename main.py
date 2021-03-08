from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.InputBox import InputBox

# test comment

# File paths
# TO DO: make these usable for others
img_folder = "C:/Users/I_cha/PycharmProjects/CS410-VideaHealth/VideaHealth/images"
file_gt = "C:/Users/I_cha/PycharmProjects/CS410-VideaHealth/VideaHealth/1_ground_truth_2a.csv"
file_pred = "C:/Users/I_cha/PycharmProjects/CS410-VideaHealth/VideaHealth/2_input_model_predictions_2.csv"


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