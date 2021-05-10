
"""
precision: used to minimize false positives
recall: used to minimize the chance of missing true positive
f1: maximize both precision & recall. works for imbalanced datasets
    (between positives vs. negatives).

"""
from Classes.Image import Image
from Classes.Box import Box


def map_gt_pred(image_pred, image_gt, iou_threshold=0.5):
    gt_map_pred = {'extra': []}  # { gt : preds list}

    length = len(image_pred.outputBoxes)
    pred_boxes = image_pred.outputBoxes.copy() if length > 0 else image_pred.inputBoxes.copy()

    # map each gt to preds
    for gt_box in image_gt.inputBoxes:
        gt_map_pred[gt_box.label] = []

        # iterate through all pred boxes to map them with each gt box
        for pred_box in pred_boxes:
            if pred_box.iou(gt_box) > iou_threshold:
                gt_map_pred[gt_box.label].append(pred_box)  # map this pred box with this gt_box
                pred_boxes.remove(pred_box)  # remove this box from temp pred list

    # box that doesn't get map is extra boxes
    for pred_box in pred_boxes:
        gt_map_pred['extra'].append(pred_box)

    # report some prediction boxes didn't get map
    # if len(pred_boxes) > 0:
    #     print("{} pred boxes didn't get map".format(len(pred_boxes)))
    return gt_map_pred


# def tp_fp_fn(image_pred, image_gt, iou_threshold=0.5):
#     gt_map_pred = map_gt_pred(image_pred, image_gt, iou_threshold)  # { gt : preds list}
#
#     true_positive = 0
#     false_positive = 0
#     false_negative = 0
#
#     # counting true & false positives , false negatives
#     for gt, preds in gt_map_pred.items():
#         if gt != 'extra':
#             # multiple boxes for this gt, pick 1 match, disregard the rest as false positives
#             if len(preds) > 1:
#                 true_positive += 1
#                 false_positive += len(preds) - 1
#             elif len(preds) == 1:
#                 true_positive += 1
#             else:  # false negative
#                 false_negative += 1
#
#     # counting additional false positives
#     extras = gt_map_pred['extra']
#     false_positive += len(extras)
#
#     return true_positive, false_positive, false_negative

def gt_in_preds(gt, preds):
    for pred in preds:
        if gt == pred.label:
            return True
    return False


def tp_fp_fn(image_pred, image_gt, iou_threshold=0.5):
    gt_map_pred = map_gt_pred(image_pred, image_gt, iou_threshold)  # { gt : preds list}

    true_positive = 0
    false_positive = 0
    false_negative = 0

    # counting true & false positives , false negatives
    for gt, preds in gt_map_pred.items():
        if gt != 'extra':
            # multiple boxes for this gt, pick 1 match, disregard the rest as false positives
            if len(preds) > 1 and gt_in_preds(gt, preds):
                true_positive += 1
                false_positive += len(preds) - 1
            elif len(preds) == 1 and gt_in_preds(gt, preds):
                true_positive += 1
            else:  # false negative
                false_negative += 1

    # counting additional false positives
    extras = gt_map_pred['extra']
    false_positive += len(extras)

    return true_positive, false_positive, false_negative


def precision_recall_iou(image_pred, image_gt, iou_threshold=0.5):
    # gt_map_pred = map_gt_pred(image_pred, image_gt, iou_threshold)  # { gt : preds list}
    val = tp_fp_fn(image_pred, image_gt, iou_threshold)
    true_positive = val[0]
    false_positive = val[1]
    false_negative = val[2]

    # # counting true & false positives , false negatives
    # for gt, preds in gt_map_pred.items():
    #     if gt != 'extra':
    #         # multiple boxes for this gt, pick 1 match, disregard the rest as false positives
    #         if len(preds) > 1:
    #             true_positive += 1
    #             false_positive += len(preds) - 1
    #         elif len(preds) == 1:
    #             true_positive += 1
    #         else:  # false negative
    #             false_negative += 1
    #
    # # counting additional false positives
    # extras = gt_map_pred['extra']
    # false_positive += len(extras)

    # formulas
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)

    # edge case
    if true_positive + false_positive <= 0:
        precision = true_positive / -1
    if true_positive + false_negative <= 0:
        recall = true_positive / -1

    # return (precision, recall)
    return precision, recall


def f1_iou(image_pred, image_gt, iou_threshold=0.5):
    precision, recall = precision_recall_iou(image_pred, image_gt, iou_threshold)
    # edge case
    if precision + recall <= 0:
        return 2 * (precision * recall) / -1
    return 2 * (precision * recall) / (precision + recall)


# precision, recall, and f1 for multiple images
# there are multiple definition on how to calculate for multi images:
# 1. calculate sum of tp, fp, fn for all images first then calculate precision & recall then f1
# 2. calculate precision, recall for each img, then average them up, next calculate f1
def precision_recall_ious(images_pred, images_gt, iou_threshold=0.5):
    sum_tp = sum_fp = sum_fn = 0

    for pred, gt in zip(images_pred, images_gt):
        val = tp_fp_fn(pred, gt, iou_threshold)
        sum_tp += val[0]
        sum_fp += val[1]
        sum_fn += val[2]

    # taking care of edge case when divisor = 0
    precision_divisor = (sum_tp + sum_fp) if (sum_tp + sum_fp) > 0 else -1
    recall_divisor = (sum_tp + sum_fn) if (sum_tp + sum_fn) > 0 else -1

    sum_precision = sum_tp / precision_divisor
    sum_recall = sum_tp / recall_divisor

    return sum_precision, sum_recall
    # sum_f1 = 2 * (sum_precision * sum_recall) / (sum_precision + sum_recall)
    # return sum_f1


def f1_ious(images_pred, images_gt, iou_threshold=0.5):
    sum_precision, sum_recall = precision_recall_ious(images_pred, images_gt, iou_threshold)
    f1_divisor = (sum_precision + sum_recall) if (sum_precision + sum_recall) > 0 else -1
    sum_f1 = 2 * (sum_precision * sum_recall) / f1_divisor
    return sum_f1


def precision_label():
    pass