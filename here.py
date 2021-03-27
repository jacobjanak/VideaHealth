from tqdm import tqdm  # progress bar library
import numpy as np
import cv2, os
import pandas as pd
import ast
from nms import nms


img_folder = 'C:/Users/I_cha/PycharmProjects/VideaHealth/images'

file_gt = 'C:/Users/I_cha/PycharmProjects/VideaHealth/1_ground_truth_2a.csv'
file_pred = 'C:/Users/I_cha/PycharmProjects/VideaHealth/2_input_model_predictions_2.csv'

test_img = 'img_005'
score_threshold = 0.35


def get_dict(df):
    """ Returns a dictionary of an dataframe of predictions or
        ground truth

    Args:
        df_gt (pd.Dataframe): the dataframe with input data

    Returns:
        dict: dictionary with the boxes sorted by img_id
    """

    boxes_per_img_id = {}
    for idx, img_id in enumerate(df["img_id"]):
        if "scores" in df.keys():
            # ast.literal_eval convert string into python syntax. Ex) '[1, 2]' -> list [1, 2]
            # df.iloc get the value at row index [idx] with column ["..."]
            boxes_per_img_id[img_id] = {
                'labels': ast.literal_eval(df.iloc[idx]["labels"]),
                'x1s': ast.literal_eval(df.iloc[idx]["x1s"]),
                'y1s': ast.literal_eval(df.iloc[idx]["y1s"]),
                'x2s': ast.literal_eval(df.iloc[idx]["x2s"]),
                'y2s': ast.literal_eval(df.iloc[idx]["y2s"]),
                'scores': ast.literal_eval(df.iloc[idx]["scores"]),
            }
        else:
            boxes_per_img_id[img_id] = {
                'labels': ast.literal_eval(df.iloc[idx]["labels"]),
                'x1s': ast.literal_eval(df.iloc[idx]["x1s"]),
                'y1s': ast.literal_eval(df.iloc[idx]["y1s"]),
                'x2s': ast.literal_eval(df.iloc[idx]["x2s"]),
                'y2s': ast.literal_eval(df.iloc[idx]["y2s"]),
            }

    return boxes_per_img_id


"""
    __init__(x1, y1, x2, y2)
    area()
    intersect(box2)
    union(box2)
    iou(box2)
"""


class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __eq__(self, other):
        if isinstance(other, Box):
            return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2
        return False

    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    def intersect(self, box2):
        xa = max(self.x1, box2.x1)
        ya = max(self.y1, box2.y1)
        xb = min(self.x2, box2.x2)
        yb = min(self.y2, box2.y2)
        return max(0, xb - xa + 1) * max(0, yb - ya + 1)

    def union(self, box2):
        return self.area() + box2.area() - self.intersect(box2)

    def iou(self, box2):
        return float(self.intersect(box2)) / float((self.union(box2)))


"""
    __init__(label, x1, y1, x2, y2, score=0):
"""


class Tooth:
    def __init__(self, label, x1, y1, x2, y2, score=0):
        self.label = label
        self.box = Box(x1, y1, x2, y2)
        self.score = score

    def __eq__(self, other):
        if isinstance(other, Tooth):
            return self.label == other.label and self.box == other.box and self.score == other.score
        return False

    def __repr__(self):
        return '%s = %f' % (self.label, self.score)


# box1 = Box(2, 2, 5, 6)
# box2 = Box(3, 4, 6, 11)
# print('box1 area = ' + str(box1.area()))
# print('box2 area = ' + str(box2.area()))
# print('intersect = ' + str(box1.intersect(box2)))
# print('union = ' + str(box1.union(box2)))
# print('iou = ' + str(box1.iou(box2)))


# def non_max_suppression(proposal_tooth):
#     # group boxes by its teeth number
#     dict_tooth = {}
#     labels = set()
#     for tooth in proposal_tooth:
#         labels.add(tooth.label)
#         if tooth.label not in dict_tooth:
#             dict_tooth[tooth.label] = [tooth]
#         else:
#             dict_tooth[tooth.label].append(tooth)
#
#     first_delete = []
#     for label in labels:
#         max_teeth = None
#         # find max score of each group
#         for tooth in dict_tooth[label]:
#             if max_teeth is None:
#                 max_teeth = tooth
#             elif tooth.score > max_teeth.score:
#                 max_teeth = tooth
#
#         first_delete.append(max_teeth)
#
#         # compare max score against others in the group
#         for tooth in dict_tooth[label]:
#             if max_teeth == tooth:
#                 continue
#             elif max_teeth.box.iou(tooth.box) > 0.6:
#                 continue
#             else:
#                 first_delete.append(tooth)
#
#     # detect overall overlapped boxes
#     for tooth_i in first_delete:
#         for tooth_j in first_delete:
#             if tooth_j == tooth_i:
#                 continue
#             elif tooth_i.box.iou(tooth_j.box) > 0.7:
#                 if tooth_i.score < tooth_j.score and tooth_i in first_delete:
#                     first_delete.remove(tooth_i)
#                 elif tooth_j in first_delete:
#                     first_delete.remove(tooth_j)
#
#     # remove tooth with low score
#     # temp = first_delete.copy()
#     # for tooth in temp:
#     #     if tooth.score < 0.3:
#     #         first_delete.remove(tooth)
#     return first_delete
#
# def non_max_suppression(proposal_tooth):
#     propose_list = proposal_tooth.copy()
#     final_list = list()
#     propose_list.sort(key=lambda t: t.score, reverse=True)
#     # propose_list.sort(key=lambda t: int(t.label.strip('tooth__')))
#
#     # remove low score boxes
#     temp = propose_list.copy()
#     for item in propose_list:
#         if item.score < 0.2:
#             temp.remove(item)
#     propose_list = temp.copy()
#
#     # # convert list to dict
#     # dict_proposal = {}
#     # for t in propose_list:
#     #     if t.label in dict_proposal:
#     #         dict_proposal[t.label].append(t)
#     #     else:
#     #         dict_proposal[t.label] = [t]
#     #
#     # # step 1: filter box with the same classification
#     # for label, teeth in dict_proposal.items():
#     #     filter_tooth = teeth.copy()
#     #     filter_tooth.sort(key=lambda t: t.score, reverse=True)
#     #     best = filter_tooth.pop(0)
#     #
#     #     for t in filter_tooth:
#     #         if best.box.iou(t.box) > 0.6:
#     #             filter_tooth.remove(t)
#     #     filter_tooth.append(best)
#     #     filter_tooth.sort(key=lambda t: t.score, reverse=True)
#     #
#     #     dict_proposal[label] = filter_tooth
#     #
#     # # step 2: filter all boxes
#     # propose_list = list()
#     # for label, t2 in dict_proposal.items():
#     #     for item in t2:
#     #         propose_list.append(item)
#
#     while len(propose_list) > 0:
#         # step 2.1: select the box with highest score
#         propose_list.sort(key=lambda t: t.score, reverse=True)
#         # debug_best = max(propose_list, key=lambda t: t.score)
#         best = propose_list.pop(0)
#
#         # compare this best to existing boxes in final_list
#         found = False
#         for final in final_list:
#             if final.box.iou(best.box) > 0.3:
#                 found = True
#                 break
#         if not found:
#             final_list.append(best)  # append it to final list
#
#             # Load an color image in grayscale
#             img_path = os.path.join(img_folder, (test_img + '.png'))
#             img = cv2.imread(img_path)
#             img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
#
#             img_pred = img.copy()
#
#             for t in final_list:
#                 cv2.rectangle(img_pred
#                               , (int(t.box.x1), int(t.box.y1))
#                               , (int(t.box.x2), int(t.box.y2))
#                               , color=(255, 0, 0)
#                               , thickness=2)
#                 cv2.putText(img_pred, t.label + ' %.2f' % (t.score),
#                             (int(t.box.x1) + 10, int(t.box.y1) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.25,
#                             (255, 0, 0), 1, cv2.LINE_AA)
#
#             cv2.rectangle(img_pred
#                           , (int(best.box.x1), int(best.box.y1))
#                           , (int(best.box.x2), int(best.box.y2))
#                           , color=(0, 0, 255)
#                           , thickness=2)
#             cv2.putText(img_pred, best.label + ' %.2f' % (best.score),
#                         (int(best.box.x1) + 10, int(best.box.y1) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.25,
#                         (0, 0, 255), 1, cv2.LINE_AA)
#             cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#             cv2.imshow('img', img_pred)
#             cv2.waitKey(0)
#
#         # step 2.2: compare best box with other boxes
#         for tooth in propose_list:
#             if best.box.iou(tooth.box) > 0.3:
#                 propose_list.remove(tooth)
#
#     # convert list into dict
#     dict_proposal = {}
#     for item in final_list:
#         if dict_proposal and item.label in dict_proposal:
#             dict_proposal[item.label].append(item)
#         else:
#             dict_proposal[item.label] = [item]
#
#     # Load an color image in grayscale
#     img_path = os.path.join(img_folder, (test_img + '.png'))
#     img = cv2.imread(img_path)
#     img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)
#
#     img_raw = img.copy()
#     img_pred = img.copy()
#
#     for l, teeth2 in dict_proposal.items():
#          for t in teeth2:
#             cv2.rectangle(img_pred
#                             , (int(t.box.x1), int(t.box.y1))
#                             , (int(t.box.x2), int(t.box.y2))
#                             , color=(255, 0, 0)
#                             , thickness=2)
#             cv2.putText(img_pred, t.label + ' %.2f' % (t.score),
#                         (int(t.box.x1) + 10, int(t.box.y1) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
#                         (255, 0, 0), 1, cv2.LINE_AA)
#
#     img_view = np.hstack((img_raw, img_pred))
#     # img_view = cv2.resize(img_view, (960, 540))
#     # print(t)
#     cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#     cv2.imshow('img', img_pred)
#     cv2.waitKey(0)
#
#
#
#     return final_list


# ========================================================================  #
# nms library
def non_max_suppression(proposal_tooth):
    rects = []
    scores = []
    labels = []

    for t in proposal_tooth:
        rect = [t.box.x1, t.box.y1, abs(t.box.x2 - t.box.x1), abs(t.box.y2 - t.box.y1)]
        rects.append(rect)
        scores.append(t.score)
        labels.append(t.label)

    indices = nms.boxes(rects, scores)

    # Load an color image in grayscale
    img_path = os.path.join(img_folder, (test_img + '.png'))
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

    img_pred = img.copy()

    for index in indices:
        t = proposal_tooth[index]
        if t.score > score_threshold:
            cv2.rectangle(img_pred
                                , (int(t.box.x1), int(t.box.y1))
                                , (int(t.box.x2), int(t.box.y2))
                                , color=(255, 0, 0)
                                , thickness=2)
            cv2.putText(img_pred, 't' + t.label.strip('tooth_'),
                            (int(t.box.x1) + 10, int(t.box.y1) + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_pred, ' %.2f' % (t.score),
                            (int(t.box.x1) + 0, int(t.box.y1) + 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 0), 1, cv2.LINE_AA)

    cv2.namedWindow(test_img, cv2.WINDOW_NORMAL)
    cv2.imshow(test_img, img_pred)
    cv2.waitKey(0)


df_gt = pd.read_csv(file_gt)
df_pred = pd.read_csv(file_pred)

dict_pred = get_dict(df_pred)
dict_gt = get_dict(df_gt)

row = dict_pred[test_img]
row_gt = dict_gt[test_img]
img_002 = list()
img_002_gt = list()


# parse dict into a list of proposal boxes for img_002
# labels = row['labels']
# labels.sort()
# for l in labels:
#     print(l

for i in range(len(row['labels'])):
    label = row['labels'][i]
    x1 = row['x1s'][i]
    y1 = row['y1s'][i]
    x2 = row['x2s'][i]
    y2 = row['y2s'][i]
    score = row['scores'][i]
    img_002.append(Tooth(label, x1, y1, x2, y2, score))

for i in range(len(row_gt['labels'])):
    label = row_gt['labels'][i]
    x1 = row_gt['x1s'][i]
    y1 = row_gt['y1s'][i]
    x2 = row_gt['x2s'][i]
    y2 = row_gt['y2s'][i]
    # score = row_gt['scores'][i]
    img_002_gt.append(Tooth(label, x1, y1, x2, y2))

for gt in img_002_gt:
    match = 0
    for pred in img_002:
        if pred.box.iou(gt.box) > 0.7:
            match = match + 1
            if match > 1:
                print("DUP: ", end="")
            print(str(pred) + " == " + str(gt))


img_002.sort(key=lambda tooth: tooth.score, reverse=True)
# img_002.sort(key=lambda tooth: int(tooth.label.strip('tooth__')))
# for tooth in img_002:
#     print(tooth.label + "\t" + str(tooth.score))

result = non_max_suppression(img_002)
# print(result)

# img_id = 'img_002'
# gt_img_id = {
#     'x1s': dict_gt[img_id]['x1s'],
#     'y1s': dict_gt[img_id]['y1s'],
#     'x2s': dict_gt[img_id]['x2s'],
#     'y2s': dict_gt[img_id]['y2s'],
#     'labels': dict_gt[img_id]['labels']}
#
# pred_img_id = result

for img_id in tqdm(dict_pred):

    gt_img_id = {
        'x1s': dict_gt[img_id]['x1s'],
        'y1s': dict_gt[img_id]['y1s'],
        'x2s': dict_gt[img_id]['x2s'],
        'y2s': dict_gt[img_id]['y2s'],
        'labels': dict_gt[img_id]['labels']}

    pred_img_id = {
        'x1s': dict_pred[img_id]['x1s'],
        'y1s': dict_pred[img_id]['y1s'],
        'x2s': dict_pred[img_id]['x2s'],
        'y2s': dict_pred[img_id]['y2s'],
        'labels': dict_pred[img_id]['labels'],
        'scores': dict_pred[img_id]['scores']}

    # Load an color image in grayscale
    img_path = os.path.join(img_folder, (img_id + '.png'))
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

    img_raw = img.copy()
    img_gt = img.copy()
    img_pred = img.copy()

    for idx, label in enumerate(gt_img_id["labels"]):
        x1 = int(gt_img_id['x1s'][idx])
        y1 = int(gt_img_id['y1s'][idx])
        x2 = int(gt_img_id['x2s'][idx])
        y2 = int(gt_img_id['y2s'][idx])

        cv2.rectangle(img_gt, (x1, y1), (x2, y2), color=(100, 255, 0),
                      thickness=2)
        cv2.putText(img_gt, label,
                    (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                    (100, 255, 0), 1, cv2.LINE_AA)

    for idx, label in enumerate(pred_img_id["labels"]):
        # if label == 'tooth_21':
        x1 = int(pred_img_id['x1s'][idx])
        y1 = int(pred_img_id['y1s'][idx])
        x2 = int(pred_img_id['x2s'][idx])
        y2 = int(pred_img_id['y2s'][idx])
        score = float(pred_img_id['scores'][idx])

        if score >= 0.0:
            cv2.rectangle(img_pred, (x1, y1), (x2, y2), color=(255, 0, 0),
                          thickness=2)
            cv2.putText(img_pred, label + ' %.2f' % (score),
                        (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                        (255, 0, 0), 1, cv2.LINE_AA)

    img_view = np.hstack((img_raw, img_pred, img_gt))
    # img_view = cv2.resize(img_view, (960, 540))
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img_view)
    cv2.waitKey(0)
