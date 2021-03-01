from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.InputBox import InputBox


gt_correct_result = {
    "img_002": {
        "labels": ['tooth_14', 'tooth_15'],
        "x1s": [514, 1070],
        "y1s": [1075, 1568],
        "x2s": [438, 457],
        "y2s": [121, 256]
    },
    "img_003": {
        "labels": ['tooth_3', 'tooth_2'],
        "x1s": [177, 0],
        "y1s": [1, 1],
        "x2s": [422, 188],
        "y2s": [331, 330]
    },
}
error_message = "CSV Reader failed to read ground truth correctly"
assert CSVReader("Tests/gt.csv").output == gt_correct_result, error_message





print("All tests passed successfully")