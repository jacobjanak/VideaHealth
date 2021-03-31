"""
This script is very simple. It works by grouping all input
boxes by label. Then, it simply selects the box with the highest
score for each label.

Current statistics of this algorithm (via accuracy.py):
    Found 0 missing boxes in our output
    Found 9 extra boxes in our output
    Average deviation per box is 85.58067425684474

Args:
    images ([Image]): a list of images containing input boxes

Returns:
    result_images ([Image]): a list of images containing output boxes
"""

from Classes.Image import Image


def best_box(images):
    result_images = []
    for image in images:
        result_image = Image(image.id)

        # Group boxes by label
        label_dict = dict()
        for box in image.inputBoxes:
            if box.label in label_dict:
                label_dict[box.label].append(box)
            else:
                label_dict[box.label] = [box]

        # Generate output boxes
        for key in label_dict:
            boxes = label_dict[key]

            # Find the box with the highest score
            best_box = boxes[0]
            for box in boxes:
                if box.score > best_box.score:
                    best_box = box

            # Store and return results
            if best_box.score > 0.35:
                result_image.outputBoxes.append(best_box)
        result_images.append(result_image)
    return result_images
