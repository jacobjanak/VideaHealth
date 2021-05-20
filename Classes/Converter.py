"""
This class converts data from the format that is given by the nueral network, which is
a parallel array, into an array of objects. For example:

This:
    { "img_001": {"labels": ["tooth_1", "tooth_2"], "scores": [0.5, 0.2]} }

Becomes:
    [ {id: "img_001", inputBoxes: [{label: "tooth_1", score: 0.5}, {label: "tooth_2", score: 0.2}] } ]
"""

from Classes.Image import Image
from Classes.Box import Box


class Converter:

    def __init__(self, unconverted, pa_bw=False):
        self.pa_bw = pa_bw
        self.result = self.parse_image_list(unconverted)
        

    def parse_image_list(self, images_dict):
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
            boxes = self.parse_box_list(value)
            img = None
            if "img_type" in value:
                img = value['img_type']

            images.append(Image(key, boxes, img))

        return images


    def parse_box_list(self, image_dict):
        """
        Converts data from the CSV format into a list of Box objects for an Image.

        Args:
            image_dict: data formatted as a dict of parallel arrays
            i.e. {"labels": ["tooth_1", "tooth_2"], "scores": [0.5, 0.2]}

        Returns:
            arr: array of InputBox objects

        NOTE: Should this class also reverse-convert? That would help with output
        """

        boxes = []
        for i in range(len(image_dict["labels"])):
            if "scores" in image_dict:
                boxes.append(Box(
                    image_dict["labels"][i],
                    image_dict["x1s"][i],
                    image_dict["y1s"][i],
                    image_dict["x2s"][i],
                    image_dict["y2s"][i],
                    image_dict["scores"][i]
                ))
            else:
                boxes.append(Box(
                    image_dict["labels"][i],
                    image_dict["x1s"][i],
                    image_dict["y1s"][i],
                    image_dict["x2s"][i],
                    image_dict["y2s"][i]
                ))

        return boxes

    @staticmethod
    def get_bw_pa(images_input, images_gt, want_bw):

        want = 'pa'
        if want_bw is True:
            want = 'bw'

        new_det = []
        new_gt = []

        for i in range(len(images_input)):
            if images_input[i].type == want:

                if images_input[i].id == images_gt[i].id:
                    new_det.append(images_input[i])
                    new_gt.append(images_gt[i])
                else:
                    print("Why didn't this work?")

        return new_det, new_gt