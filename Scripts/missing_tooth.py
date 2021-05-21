"""
Steps: 
    1) Sort teeth by x1s.
    2) Seperate upper and lower row of teeth.
    3) Find teeth_gap by gettinG the size of both adjacent teeth divided by 7.
    4) Go through upper teeth and determine if there is a gap between teeth
          if gap > than teeth_gap then bump the current tooth label by 1.
          This also saves a count to see number of missing tooth.
    5) Do the same with lower teeth, but lower label by 1.
    6) Return images.

Notes:
    1) There is a gt that has two missing teeth
"""
import math

from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box

# Used for sorting
upper_teeth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
lower_teeth = [32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17]

# Find them missing teeth algo
def missing_tooth(images_pred):
    result_images = []
    # Goes through every image in images_pred
    for i, image in enumerate(images_pred):
        result_image = Image(image.id)

        # SORT STARTS HERE
        upper_pred = []
        lower_pred = []
        # sort the boxes by x1 value


        image.outputBoxes = sorted(image.outputBoxes, key=lambda box: box.x1s)
        # separate upper and lower teeth in this image
        for box in image.outputBoxes:
            # get only the number of this tooth label
            label_num = int(box.label.strip('tooth_'))
            # Upper
            if label_num in upper_teeth:
                upper_pred.append(box)
            # Lower
            elif label_num in lower_teeth:
                lower_pred.append(box)
            # Error
            else:
                print('Error sorting teeth in missing_tooth.py: ' + str(label_num))
        #SORTING BANANANAS

        if( len(upper_pred) != 0):
            oldX1 = upper_pred[0].x1s
            oldX2 = upper_pred[0].x2s
            oldY1 = upper_pred[0].y1s
            oldY2 = upper_pred[0].y2s
            isMissingTeeth = False
            number_of_missing_teeth = 0

            for j, box in enumerate(upper_pred):
                teeth_gap = ((oldX2 - oldX1) + (upper_pred[j].x2s - upper_pred[j].x1s))/3
                if(isMissingTeeth):
                    label_num = int(box.label.strip('tooth_')) + number_of_missing_teeth
                    upper_pred[j].label = "tooth_" + str(label_num)
                if((upper_pred[j].x1s - oldX2) > teeth_gap):
                    number_of_missing_teeth += 1
                    isMissingTeeth = True
                    label_num = int(box.label.strip('tooth_')) + number_of_missing_teeth
                    upper_pred[j].label = "tooth_" + str(label_num)
                    # print(image.id)
                    # print(upper_pred[j].label)
                    # print(upper_pred[j].x1s - oldX2)
                oldX1 = upper_pred[j].x1s
                oldX2 = upper_pred[j].x2s
                oldY1 = upper_pred[j].y1s
                oldY2 = upper_pred[j].y2s
                result_image.outputBoxes.append(upper_pred[j])

        if( len(lower_pred) != 0):
            oldX1 = lower_pred[0].x1s
            oldX2 = lower_pred[0].x2s
            oldY1 = lower_pred[0].y1s
            oldY2 = lower_pred[0].y2s
            isMissingTeeth = False
            number_of_missing_teeth = 0

            for j, box in enumerate(lower_pred):
                teeth_gap = ((oldX2 - oldX1) + (lower_pred[j].x2s - lower_pred[j].x1s))/3
                if(isMissingTeeth):
                    label_num = int(box.label.strip('tooth_')) + number_of_missing_teeth
                    lower_pred[j].label = "tooth_" + str(label_num)
                if((lower_pred[j].x1s - oldX2) > teeth_gap):
                    number_of_missing_teeth -= 1
                    isMissingTeeth = True
                    label_num = int(box.label.strip('tooth_')) + number_of_missing_teeth
                    lower_pred[j].label = "tooth_" + str(label_num)
                    # print(image.id)
                    # print(lower_pred[j].label)
                    # print(lower_pred[j].x1s - oldX2)
                    # print(lower_pred[j].x1s, oldX2)
                oldX1 = lower_pred[j].x1s
                oldX2 = lower_pred[j].x2s
                oldY1 = lower_pred[j].y1s
                oldY2 = lower_pred[j].y2s
                result_image.outputBoxes.append(lower_pred[j])
        result_images.append(result_image)
    return result_images