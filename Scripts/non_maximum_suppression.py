"""
TO DO: Description
"""

from nms import nms


def get_nms_box(t):
    return [t.x1s, t.y1s, abs(t.x2s - t.x1s), abs(t.y2s - t.y1s)]


def nonmaximum_suppression(images):
    for image in images:

        nmsboxlist = []
        predscorelist = []
        for tooth in image.inputBoxes:
            nmsboxlist.append(get_nms_box(tooth))
            predscorelist.append(tooth.score)

        best_rect = nms.boxes(nmsboxlist, predscorelist)

        for rect_index in best_rect:
            box = image.inputBoxes[rect_index]
            if box.score > 0.35:
                image.outputBoxes.append(box)

    return images