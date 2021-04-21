"""
This postprocessing script is named after professor Haehn because
he gave us this idea in a Zoom meeting. The script works by grouping
boxes based on their label. Then, the script creates one output box
for each label by averaging out all the x and y coordinates of the
input boxes, using box.score as the weight when calculating the average.
So, boxes with a higher score have a greater impact on the resulting
output box. I found that cubing the scores led to greater accuracy.

Current statistics of this algorithm (via accuracy.py):
    Found 0 missing boxes in our output
    Found 8 extra boxes in our output
    Average deviation per box is 103.53122411304943

Args:
    images ([Image]): a list of images containing input boxes

Returns:
    result_images ([Image]): a list of images containing output boxes
"""

from Classes.Image import Image
from Classes.Box import Box


def haehn(images):
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

            # Get the combined score of all boxes with this label
            total_score = sum(box.score ** 3 for box in boxes)

            # Create the output box
            if total_score > 0.1:
                box_meets_threshhold = False
                result_box = Box(key, 0, 0, 0, 0)
                for box in boxes:

                    # Make sure at least one of the boxes meets threshhold
                    if box.score > 0.5:
                        box_meets_threshhold = True

                    # Average out the x and y coordinates of the boxes
                    dominance = box.score ** 3 / total_score
                    result_box.x1s += box.x1s * dominance
                    result_box.y1s += box.y1s * dominance
                    result_box.x2s += box.x2s * dominance
                    result_box.y2s += box.y2s * dominance
                    result_box.score = box.score # not gonna work well

                # Store and return results
                if box_meets_threshhold:
                    result_image.outputBoxes.append(result_box)
        result_images.append(result_image)
    return result_images
