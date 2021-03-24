import os

import numpy as np
from nms import nms
import cv2

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



def get_nmsbox(box):
    return [box.x1, box.x2, abs(box.x2 - box.x1), abs(box.y2 - box.y1)]

def non_max_suppression(proposal_tooth, test_img):

    nmsboxlist = []
    predscorelist = []
    for tooth in proposal_tooth.inputBoxes:
        nmsboxlist.append(get_nmsbox(tooth))
        predscorelist.append(tooth.score)

    bestrect = nms.boxes(nmsboxlist, predscorelist)
    besttooth = []

    # Load an color image in grayscale
    img_path = os.path.join(img_folder, (test_img + '.png'))
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

    img_pred = img.copy()

    for rectindex in bestrect:
        besttooth.append(proposal_tooth.inputBoxes[rectindex])

    for t in besttooth:

        cv2.rectangle(img_pred
                      , (int(t.x1), int(t.y1))
                      , (int(t.x2), int(t.y2))
                      , color=(255, 0, 0)
                      , thickness=2)
        cv2.putText(img_pred, t.label + ' %.2f' % (t.score),
                    (int(t.x1) + 10, int(t.y1) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.25,
                    (255, 0, 0), 1, cv2.LINE_AA)


    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img_pred)
    cv2.waitKey(0)


if "__main__":

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

    for image in images:
        non_max_suppression(image, image.id)