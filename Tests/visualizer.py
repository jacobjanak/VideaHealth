import numpy as np
import cv2
import os

from Tests.visualizer_GUI import show_visualizer

# File paths
cur_dir = os.getcwd()
parent_dir = os.pardir
project_dir = os.path.dirname(os.path.join(cur_dir, parent_dir))
data_dir = project_dir + "/CS410_VideaHealth_sample_data"
img_folder = data_dir + "/images"
file_gt = data_dir + "/1_ground_truth_2a.csv"
file_pred = data_dir + "/2_input_model_predictions_2.csv"

pred_color = (252, 3, 3)  # (255, 33, 0)
pred_txt_color = (3, 3, 252)
gt_color = (100, 255, 0)
pred_color_fp =  (0, 98, 255)
pred_color_tp = (252, 3, 3)
gt_txt_color = gt_color


# This simply passes two ImageList
def visualizer(script_name, images_pred, images_gt):
    images = []
    for n in range(len(images_gt)):
        # Essentially setup the GUI for this Image
        img_path = os.path.join(img_folder, (images_gt[n].id + '.png'))
        img = cv2.imread(img_path)

        # calculate img width, height
        padding_x = padding_y = 0
        img_width = img_height = 0
        if img is None:  # no img file
            img_width, img_height, padding_x, padding_y = cal_blank_img_size(images_gt[n], images_pred[n])
            img = create_blank_img(int(img_width), int(img_height))  # create img fill with black color
        else:
            img_width = img.shape[1]
            img_height = img.shape[0]

            padding_x = img_width // 30
            padding_y = img_height // 30
            img = cv2.copyMakeBorder(img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_CONSTANT, value=(0, 0, 0))

            img_width = img.shape[1]
            img_height = img.shape[0]

        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

        img_gt = img.copy()
        img_pred = img.copy()
        img_both = img.copy()

        fontface = cv2.FONT_HERSHEY_COMPLEX_SMALL
        thickness = 1

        # For loop of the GroundTruth Data
        for inputBox in images_gt[n].inputBoxes:
            label = 't' + inputBox.label.strip('tooth_')

            font_scale = cal_optimal_font_scale(label, img_width, img_height)

            cv2.rectangle(img_gt, (inputBox.x1s + padding_x, inputBox.y1s + padding_y), (inputBox.x2s + padding_x, inputBox.y2s + padding_y), color=gt_color,
                          thickness=thickness)

            cv2.rectangle(img_both, (inputBox.x1s + padding_x, inputBox.y1s + padding_y), (inputBox.x2s + padding_x, inputBox.y2s + padding_y), color=gt_color,
                          thickness=thickness)

            cv2.putText(img_gt, label, (inputBox.x1s + padding_x, inputBox.y1s + padding_y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, gt_txt_color, thickness, cv2.LINE_AA)

            cv2.putText(img_both, label, (inputBox.x1s + padding_x, inputBox.y1s + padding_y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, gt_txt_color, thickness, cv2.LINE_AA)

        # For Loop of the image prediction output boxes
        for outputBox in images_pred[n].outputBoxes:
            label = 't' + outputBox.label.strip('tooth_')
            if outputBox.score is not None:
                score = "{:.2f}".format(outputBox.score)
            else:
                score = '???'

            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, 2)
            label_offset = label_height + (padding_y // 50)

            x1, y1 = outputBox.vec1()
            x2, y2 = outputBox.vec2()

            # I implemented a tp fp
            if (outputBox.tp_fp == 'TP'):
                cv2.rectangle(img_pred, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color_tp, thickness=2)

                cv2.rectangle(img_both, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color_tp, thickness=2)
            elif outputBox.tp_fp == 'FP':

                cv2.rectangle(img_pred, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color_fp, thickness=2)

                cv2.rectangle(img_both, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color_fp, thickness=2)
            else:
                cv2.rectangle(img_pred, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color, thickness=2)

                cv2.rectangle(img_both, (x1 + padding_x, y1 + padding_y), (x2 + padding_x, y2 + padding_y),
                              color=pred_color, thickness=2)

            # add prediction tooth label
            # I change 2nd arg from label to
            cv2.putText(img_pred, "{} {:0.2f}".format(label, outputBox.score), (int(outputBox.x1s) + padding_x, int(outputBox.y2s) + padding_y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, pred_txt_color, 2, cv2.LINE_AA)

            cv2.putText(img_both, label, (int(outputBox.x1s) + padding_x, int(outputBox.y2s) + padding_y),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, pred_txt_color, 2, cv2.LINE_AA)

            # add prediction tooth score
            # cv2.putText(img_pred, score, (int(outputBox.x1s) + padding_x, int(outputBox.y2s) + padding_y - label_offset),
            #             cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, pred_txt_color, 2, cv2.LINE_AA)
            # cv2.putText(img_both, score, (int(outputBox.x1s) + padding_x, int(outputBox.y2s) + padding_y - label_offset),
            #             cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, pred_txt_color, 2, cv2.LINE_AA)

        # # for loop to make dots for each 5 pixel
        # for i in range(0, int(img_width), 5):
        #     cv2.putText(img_pred, '|', (i, 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
        #                 (255, 255, i + 10), 1, cv2.LINE_AA)
        #
        # for j in range(0, int(img_height), 5):
        #     cv2.putText(img_pred, '-', (5, j), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
        #                 (255, 255, j + 10), 1, cv2.LINE_AA)

        name = script_name + ': ' + images_gt[n].id
        img_view = np.hstack((img_pred, img_gt, img_both))
        images.append(img_view)

        # cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        # cv2.imshow(name, img_view)
        # cv2.waitKey(0)
    show_visualizer(images)


def cal_optimal_font_scale(txt, rect_width):
    for scale in reversed(range(1, 60, 1)):
        text_size = cv2.getTextSize(txt, fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=scale/10, thickness=1)
        txt_width = text_size[0][0]
        if 0 < txt_width <= rect_width * 0.04:
            return scale/10
    return 1

def cal_optimal_font_scale(txt, rect_width, rect_height):
    # we want the scale to be a percentage of the area
    area = rect_width * rect_height
    ratio = 0.05 * area

    for scale in reversed(range(1, 100)):
        (txt_width, txt_height), txt_baseline = cv2.getTextSize(txt, fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=scale/100, thickness=1)
        txt_area = txt_width * txt_height

        if 0 < txt_area < ratio:
            return scale/100
    return 1


def cal_blank_img_size(img_gt, img_pred):
    # calculate ground truth image size
    img_gt_x2 = max(img_gt.inputBoxes, key=lambda box: box.x2s).x2s
    img_gt_y2 = max(img_gt.inputBoxes, key=lambda box: box.y2s).y2s

    # calculate pred image size
    img_pred_x2 = max(img_pred.outputBoxes, key=lambda box: box.x2s).x2s
    img_pred_y2 = max(img_pred.outputBoxes, key=lambda box: box.y2s).y2s

    # calculate image size that large enough for both
    new_x2 = int(max(img_gt_x2, img_pred_x2))
    new_y2 = int(max(img_gt_y2, img_pred_y2))

    # calculate padding
    max_width = int(abs(new_x2))
    max_height = int(abs(new_y2))
    padding_x = max_width // 4
    padding_y = max_height // 4

    # make padding divisible by 2
    if padding_x % 2 != 0:
        padding_x = padding_x + 1
    if padding_y % 2 != 0:
        padding_y = padding_y + 1

    max_width = max_width + padding_x * 2
    max_height = max_height + padding_y * 2

    return int(max_width), int(max_height), padding_x, padding_y


def create_blank_img(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)  # create image
    color = tuple(reversed(rgb_color))  # OpenCV use BGR, so we reverse the RGB tuple
    image[:] = color  # fill this image with color
    return image
