import numpy as np
import cv2, os

img_folder = "C:/Users/danle/PycharmProjects/CS410-VideaHealth/CS410_VideaHealth_sample_data/images"
file_gt = "C:/Users/danle/PycharmProjects/CS410-VideaHealth/CS410_VideaHealth_sample_data/1_ground_truth_2a.csv"
file_pred = "C:/Users/danle/PycharmProjects/CS410-VideaHealth/CS410_VideaHealth_sample_data/2_input_model_predictions_2.csv"

# This simply passes two ImageList

def visualizer(images_pred, images_gt):

    for n in range(len(images_gt)):

        # Essentially setup the GUI for this Image
        img_path = os.path.join(img_folder, (images_gt[n].id + '.png'))
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

        img_gt = img.copy()
        img_pred = img.copy()
        img_both = img.copy()

        # For loop of the GroundTruth Data
        for inputBox in images_gt[n].inputBoxes:
            cv2.rectangle(img_gt, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)

            cv2.rectangle(img_both, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)
            cv2.putText(img_gt, inputBox.label,
                        (inputBox.x1s + 10, inputBox.y1s + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img_both, inputBox.label,
                        (inputBox.x1s + 10, inputBox.y1s + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)

        # For Loop of the image prediction output boxes
        for outputBox in images_pred[n].outputBoxes:

            cv2.rectangle(img_pred, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)
            cv2.rectangle(img_both, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)

            cv2.putText(img_pred, outputBox.label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)

            cv2.putText(img_both, outputBox.label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)

        img_view = np.hstack((img_pred, img_gt, img_both))
        # img_view = np.hstack((img_raw, img_pred, img_gt))
        cv2.namedWindow(images_gt[n].id, cv2.WINDOW_NORMAL)
        cv2.imshow(images_gt[n].id, img_view)
        cv2.waitKey(0)

