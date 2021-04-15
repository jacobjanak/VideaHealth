import math

from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box

upper_teeth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
lower_teeth = [32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17]

teethGap = 100;


def missing_tooth(images_pred):
    for i, image in enumerate(images_pred):
        # SORT STARTS HERE
        upper_pred = []
        lower_pred = []
        # sort the boxes by x1 value
        image.inputBoxes = sorted(image.inputBoxes, key=lambda box: box.x1s)
        # separate upper and lower teeth in this image
        for box in image.inputBoxes:
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
                print('Error teeth arrangement: ' + str(label_num))
        # SORTING BANANANAS

        if (len(upper_pred) != 0):
            oldX1 = upper_pred[0].x1s
            oldX2 = upper_pred[0].x2s
            oldY1 = upper_pred[0].y1s
            oldY2 = upper_pred[0].y2s

            for j, box in enumerate(upper_pred):
                if ((upper_pred[j].x1s - oldX2) > teethGap):
                    print(image.id)
                    print(upper_pred[j].label)
                    print(upper_pred[j].x1s, oldX2)
                oldX1 = upper_pred[j].x1s
                oldX2 = upper_pred[j].x2s
                oldY1 = upper_pred[j].y1s
                oldY2 = upper_pred[j].y2s

        if (len(lower_pred) != 0):

            oldX1 = lower_pred[0].x1s
            oldX2 = lower_pred[0].x2s
            oldY1 = lower_pred[0].y1s
            oldY2 = lower_pred[0].y2s

            for j, box in enumerate(lower_pred):
                if ((lower_pred[j].x1s - oldX2) > teethGap):
                    print(image.id)
                    print(lower_pred[j].label)
                oldX1 = lower_pred[j].x1s
                oldX2 = lower_pred[j].x2s
                oldY1 = lower_pred[j].y1s
                oldY2 = lower_pred[j].y2s
