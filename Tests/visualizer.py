import numpy as np
import cv2
import os

# This simply passes two ImageList


def visualizer(img_folder, script_name, images_pred, images_gt):
    for n in range(len(images_gt)):
        # Essentially setup the GUI for this Image
        img_path = os.path.join(img_folder, (images_gt[n].id + '.png'))
        img = cv2.imread(img_path)

        # no img file
        if img is None:
            max_height = max_width = 0

            for img_pred in images_pred:  # find height & width
                for box in img_pred.outputBoxes:
                    width = abs(box.x2s - box.x1s)
                    height = abs(box.y1s - box.y2s)
                    if width > max_width:
                        max_width = width
                    if height > max_height:
                        max_height = height

            img = create_blank_img(int(max_width), int(max_height))

        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

        img_gt = img.copy()
        img_pred = img.copy()
        img_both = img.copy()

        # For loop of the GroundTruth Data
        for inputBox in images_gt[n].inputBoxes:
            label = 't' + inputBox.label.strip('tooth_')
            cv2.rectangle(img_gt, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)

            cv2.rectangle(img_both, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)
            cv2.putText(img_gt, label,
                        (inputBox.x1s + 10, inputBox.y1s +
                         30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img_both, label,
                        (inputBox.x1s + 10, inputBox.y1s +
                         30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)

        # For Loop of the image prediction output boxes
        for outputBox in images_pred[n].outputBoxes:
            label = 't' + outputBox.label.strip('tooth_')
            if outputBox.score is not None:
                score = "{:.2f}".format(outputBox.score)
            else:
                score = '???'
            cv2.rectangle(img_pred, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)
            cv2.rectangle(img_both, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)

            cv2.putText(img_pred, label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) +
                         30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)

            cv2.putText(img_pred, score,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) +
                         90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (0, 0, 255), 1, cv2.LINE_AA)

            cv2.putText(img_both, label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) +
                         30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)

            cv2.putText(img_both, score,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) +
                         90), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (0, 0, 255), 1, cv2.LINE_AA)

        name = script_name + ': ' + images_gt[n].id
        img_view = np.hstack((img_pred, img_gt, img_both))
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.imshow(name, img_view)
        cv2.waitKey(0)


def create_blank_img(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)  # create image
    # OpenCV use BGR, so we reverse the RGB tuple
    color = tuple(reversed(rgb_color))
    image[:] = color  # fill this image with color
    return image
