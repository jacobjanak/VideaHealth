"""
Dis is Monke code
idea:
    1. pick best score box
    2. cluster all box overlapped this best box using IOU
    3. averaging position of all boxes in cluster to create a new box as result box
    4. repeat till satisfy
"""

from Classes.Image import Image
from Classes.Box import Box


def best_cluster_haehn(images):
    result_images = []
    for image in images:
        groups = {}
        result_image = Image(image.id)

        inputBoxes_temp = image.inputBoxes.copy()

        # grouping algorithm
        while len(inputBoxes_temp) > 0:
            best_box = max(inputBoxes_temp, key=lambda box: box.score)  # get a box with best score

            # loop till best_box score is too low
            if best_box.score < 0.35:
                break

            inputBoxes_temp.pop(inputBoxes_temp.index(best_box))  # remove best_box from the list
            if best_box not in groups:
                groups[best_box] = []

            # group best_box with any other boxes that overlapped this box
            for box in inputBoxes_temp:
                if box.iou(best_box) > 0.3 and box.score > 0.1:
                    groups[best_box].append(box)
                    inputBoxes_temp.remove(box)

        # loop through each group to create new resulting boxes
        for bestbox, candidates in groups.items():
            result_box = Box(bestbox.label, 0, 0, 0, 0, bestbox.score)

            # Get the combined score of all boxes with this label
            total_score = sum(box.score ** 3 for box in candidates)

            for box in candidates:
                # Average out the x and y coordinates of the boxes
                dominance = box.score ** 3 / total_score
                result_box.x1s += box.x1s * dominance
                result_box.y1s += box.y1s * dominance
                result_box.x2s += box.x2s * dominance
                result_box.y2s += box.y2s * dominance

            result_image.outputBoxes.append(result_box)
        result_images.append(result_image)
    return result_images
