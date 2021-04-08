import numpy as np
import cv2, os

# File paths
cur_dir = os.getcwd()
parent_dir = os.pardir
project_dir = os.path.dirname(os.path.join(cur_dir, parent_dir))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth_2a.csv"
file_pred = data_dir + "/2_input_model_predictions_2.csv"

# This simply passes two ImageList

def visualizer(script_name, images_pred, images_gt):

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
            label = 't' + inputBox.label.strip('tooth_')
            cv2.rectangle(img_gt, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)

            cv2.rectangle(img_both, (inputBox.x1s, inputBox.y1s), (inputBox.x2s, inputBox.y2s), color=(100, 255, 0),
                          thickness=2)
            cv2.putText(img_gt, label,
                        (inputBox.x1s + 10, inputBox.y1s + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img_both, label,
                        (inputBox.x1s + 10, inputBox.y1s + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (100, 255, 0), 1, cv2.LINE_AA)

        # For Loop of the image prediction output boxes
        for outputBox in images_pred[n].outputBoxes:
            label = 't' + outputBox.label.strip('tooth_')
            cv2.rectangle(img_pred, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)
            cv2.rectangle(img_both, outputBox.vec1(), outputBox.vec2(), color=(255, 33, 0),
                          thickness=2)

            cv2.putText(img_pred, label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)

            cv2.putText(img_both, label,
                        (int(outputBox.x1s) + 10, int(outputBox.y1s) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 33, 0), 1, cv2.LINE_AA)
        if images_gt[n].id == "img_002":
            name = script_name + ': ' + images_gt[n].id
            img_view = np.hstack((img_pred, img_gt, img_both))
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            cv2.imshow(name, img_view)
            cv2.waitKey(0)

