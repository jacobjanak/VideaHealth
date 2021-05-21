
import csv
import pandas as pd
import ast

class CSVWriter:

    # add csv writer to main to run
    # CSVWriter(info, option)
    # option is 1 or greater
    # example 1 is outputBoxes
    # 2 is inputBoxes

    def __init__(self, image_boxes_data, filename=None, in_or_out_boxes=True, debug=False):
        self.date_frame(image_boxes_data, in_or_out_boxes, debug)

    def date_frame(self, data_obj, option, debug):

        boxes = {}

        if option:

            # does outboxBoxes

            for image in data_obj:
                score = []
                label = []
                x1s = []
                y1s = []
                x2s = []
                y2s = []

                for box in image.outputBoxes:
                    label.append(box.label)
                    x1s.append(box.x1s)
                    y1s.append(box.y1s)
                    x2s.append(box.x2s)
                    y2s.append(box.y2s)
                    score.append(box.score)

                boxes[image.id] = {
                    "img_id": image.id,
                    "labels": label,
                    "x1s": x1s,
                    "y1s": y1s,
                    "x2s": x2s,
                    "y2s": y2s,
                    "score": score,
                }


            if boxes == 0:
                print("\n boxes are empty ......")

            #print("boxes", boxes)
            fields = ['img_id', 'x1s', 'y1s', 'x2s', 'y2s', 'score']
            field = pd.DataFrame.from_dict(boxes, orient='index')

            # comment line blow if you do not want to see field

            if debug:
                print("field", field)
            filename = "outputBoxes.csv"
            # change the line below to change file location
            # last \ is the file name if you want to change it

            field.to_csv(r'output\outputBoxes.csv',
                         index=False, header=True)
            if debug:
                print("\n done filename is: " + filename)

        else:

            # does inputBoxes

            for image in data_obj:
                score = []
                label = []
                x1s = []
                y1s = []
                x2s = []
                y2s = []

                for box in image.inputBoxes:
                    label.append(box.label)
                    x1s.append(box.x1s)
                    y1s.append(box.y1s)
                    x2s.append(box.x2s)
                    y2s.append(box.y2s)
                    score.append(box.score)

                boxes[image.id] = {
                    "img_id": image.id,
                    "labels": label,
                    "x1s": x1s,
                    "y1s": y1s,
                    "x2s": x1s,
                    "y2s": y2s,
                    "score": score,
                }

            if debug:
                if boxes == 0:
                    print("\n boxes are empty ......")

            #print("boxes", boxes)
            filename = "inputBoxes.csv"
            fields = ['img_id', 'x1s', 'y1s', 'x2s', 'y2s', 'score']
            field = pd.DataFrame.from_dict(boxes, orient='index')

            # comment line below if you do not want to see output
            print("field", field)

            # change the line below to change file location
            # last \ is the file name if you want to change it
            field.to_csv(r'output\inputBoxes.csv',
                         index=False, header=True)
            print("\n done filename is: " + filename)

