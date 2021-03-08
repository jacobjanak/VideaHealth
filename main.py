from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.PredictionBoundingBox import PredictionBoundingBox

# test comment

# File paths
# TO DO: make these usable for others
img_folder = "CS410_VideaHealth_sample_data/images"
file_gt = "CS410_VideaHealth_sample_data/1_ground_truth_2a.csv"
file_pred = "CS410_VideaHealth_sample_data/2_input_model_predictions_2.csv"


# Read the input CSV file
Reader = CSVReader(file_pred)

# Convert the data in the CSV into a more usable format
DataConverter = Converter(Reader.output)

# Retrieve the image list
images = DataConverter.result


list_img = []
for pbbox in images[0].inputBoxes:
    if pbbox.label == 'tooth_18':
        list_img.append(pbbox)

list_img.sort(key=lambda ppbox: pbbox.score)



def nms(image):

    tempDict = image.inputDictionary.copy()

    for key in tempDict:
        # Step 1: Slect box with highest objectiveness score
        tempDict[key].sort(key=lambda ppbox: ppbox.score)
        bestpbbox = tempDict[key].pop(0)
        for pbbox in tempDict[key]:
            # Step 2: Compare the overlap of bestpbb with other pbb
            if bestpbbox.iou(pbbox) > 0.50:
                # Step 3: Remove with overlap > 50%
                tempDict[key].remove(pbbox)

        # Step 4: Should loop back to the beginning:



    return tempDict

newDic = nms(images[0])

# Logging
print(images)
print(images[0])
print(images[0].id)
print(len(images[0].inputBoxes))
# test git branch