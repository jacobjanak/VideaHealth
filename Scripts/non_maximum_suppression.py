"""
TO DO: Description
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def get_nms_box(t):
    return [t.x1s, t.y1s, abs(t.x2s - t.x1s), abs(t.y2s - t.y1s)]


def get_tf_box(t):
    return [t.y1s, t.x1s, t.y2s, t.x2s]


def nonmaximum_suppression(images):
    for image in images:

        nmsboxlist = []
        predscorelist = []
        for tooth in image.inputBoxes:
            # nmsboxlist.append(get_nms_box(tooth))
            nmsboxlist.append(get_tf_box(tooth))
            predscorelist.append(tooth.score)

        # best_rect = nms.boxes(nmsboxlist, predscorelist)
        best_rect = tf.image.non_max_suppression(nmsboxlist, predscorelist, max_output_size=32, score_threshold=0.35)

        for rect_index in best_rect:
            box = image.inputBoxes[rect_index]
            # if box.score > 0.1:
            image.outputBoxes.append(box)

    return images
