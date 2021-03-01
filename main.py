
# Classes
from Classes.CSVReader import CSVReader
from Classes.Image import Image
from Classes.InputBox import InputBox

# File paths
img_folder = "/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/images"
file_gt = "/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/1_ground_truth_2a.csv"
file_pred = "/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/2_input_model_predictions_2.csv"


def parse_image_list(images_dict):
    """
    Converts data from the CSV format into a list of Image objects.

    Args:
        images_dict: data formatted as dicts of parallel arrays
        i.e. { "img_001": {"labels": ["tooth_1", "tooth_2"], "scores": [0.5, 0.2]} }

    Returns:
        arr: array of Image objects
    """

    images = []
    for key, value in images_dict.items():
        boxes = parse_box_list(value)
        images.append(Image(key, boxes))

    return images


def parse_box_list(image_dict):
    """
    Converts data from the CSV format into a list of Box objects for an Image.

    Args:
        image_dict: data formatted as a dict of parallel arrays
        i.e. {"labels": ["tooth_1", "tooth_2"], "scores": [0.5, 0.2]}

    Returns:
        arr: array of InputBox objects
    """

    boxes = []
    for i in range(len(image_dict["labels"])):
        boxes.append(InputBox(
            image_dict["labels"][i],
            image_dict["x1s"][i],
            image_dict["y1s"][i],
            image_dict["x2s"][i],
            image_dict["y2s"][i],
            image_dict["scores"][i]
        ))

    return boxes



Reader = CSVReader(file_pred)
images = parse_image_list(Reader.output)


print(images)
print(images[0])
print(images[0].id)
print(len(images[0].inputBoxes))