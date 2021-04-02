from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.Image import Image
from Classes.Box import Box


# Test CSV Reader on a prediction CSV file
pred_correct_result = {
    "img_002": {
        "labels": ['tooth_14', 'tooth_15'],
        "x1s": [514, 1070],
        "y1s": [1075, 1568],
        "x2s": [438, 457],
        "y2s": [121, 256],
        "scores": [0.6, 0.7888]
    },
    "img_003": {
        "labels": ['tooth_3', 'tooth_2'],
        "x1s": [177, 0],
        "y1s": [1, 1],
        "x2s": [422, 188],
        "y2s": [331, 330],
        "scores": [0.001, .5]
    },
}
error_message = "CSV Reader failed to read predictions file correctly"
assert CSVReader("Tests/pred.csv").output == pred_correct_result, error_message


# Test CSV Reader on a ground truth CSV file
gt_correct_result = {
    "img_002": {
        "labels": ["tooth_14", "tooth_15"],
        "x1s": [514, 1070],
        "y1s": [1075, 1568],
        "x2s": [438, 457],
        "y2s": [121, 256]
    },
    "img_003": {
        "labels": ["tooth_3", "tooth_2"],
        "x1s": [177, 0],
        "y1s": [1, 1],
        "x2s": [422, 188],
        "y2s": [331, 330]
    },
}
error_message = "CSV Reader failed to read ground truth file correctly"
assert CSVReader("Tests/gt.csv").output == gt_correct_result, error_message


# Test InputBox class
test_box = Box("tooth_1", 1, 2, 3, 4, 0.5)
error_message = "InputBox failed a test"
assert test_box.label == "tooth_1", error_message
assert test_box.x1s == 1, error_message
assert test_box.y1s == 2, error_message
assert test_box.x2s == 3, error_message
assert test_box.y2s == 4, error_message
assert test_box.score == 0.5, error_message


# Test Image class
boxes = [
    Box("tooth_14", 514, 1075, 438, 121, 0.6),
    Box("tooth_15", 1070, 1568, 457, 256, 0.7888)
]
test_image = Image("img_001", boxes)
error_message = "Image class failed a test"
assert test_image.id == "img_001", error_message
assert test_image.inputBoxes[0].label == boxes[0].label, error_message
assert test_image.inputBoxes[0].x1s == boxes[0].x1s, error_message
assert test_image.inputBoxes[0].y1s == boxes[0].y1s, error_message
assert test_image.inputBoxes[0].x2s == boxes[0].x2s, error_message
assert test_image.inputBoxes[0].y2s == boxes[0].y2s, error_message
assert test_image.inputBoxes[0].score == boxes[0].score, error_message
assert test_image.inputBoxes[1].label == boxes[1].label, error_message
assert test_image.inputBoxes[1].x1s == boxes[1].x1s, error_message
assert test_image.inputBoxes[1].y1s == boxes[1].y1s, error_message
assert test_image.inputBoxes[1].x2s == boxes[1].x2s, error_message
assert test_image.inputBoxes[1].y2s == boxes[1].y2s, error_message
assert test_image.inputBoxes[1].score == boxes[1].score, error_message


# Test Converter class
# Should be tested last since this class imports the Image and InputBox classes
test_input = {
    "img_002": {
        "labels": ["tooth_14", "tooth_15"],
        "x1s": [514, 1070],
        "y1s": [1075, 1568],
        "x2s": [438, 457],
        "y2s": [121, 256],
        "scores": [0.6, 0.7888]
    },
    "img_003": {
        "labels": ["tooth_3", "tooth_2"],
        "x1s": [177, 0],
        "y1s": [1, 1],
        "x2s": [422, 188],
        "y2s": [331, 330],
        "scores": [0.001, 0.5]
    },
}
correct = [
    Image("img_002", [
        Box("tooth_14", 514, 1075, 438, 121, 0.6),
        Box("tooth_15", 1070, 1568, 457, 256, 0.7888)
    ]),
    Image("img_003", [
        Box("tooth_3", 177, 1, 422, 331, 0.001),
        Box("tooth_2", 0, 1, 188, 330, 0.5)
    ])
]
actual = Converter(test_input).result
error_message = "Converter failed to correctly convert its input"
assert actual[0].id == correct[0].id, error_message
assert actual[0].inputBoxes[0].label == correct[0].inputBoxes[0].label, error_message
assert actual[0].inputBoxes[0].x1s == correct[0].inputBoxes[0].x1s, error_message
assert actual[0].inputBoxes[0].y1s == correct[0].inputBoxes[0].y1s, error_message
assert actual[0].inputBoxes[0].x2s == correct[0].inputBoxes[0].x2s, error_message
assert actual[0].inputBoxes[0].y2s == correct[0].inputBoxes[0].y2s, error_message
assert actual[0].inputBoxes[0].score == correct[0].inputBoxes[0].score, error_message
assert actual[1].id == correct[1].id, error_message
assert actual[1].inputBoxes[0].label == correct[1].inputBoxes[0].label, error_message
assert actual[1].inputBoxes[0].x1s == correct[1].inputBoxes[0].x1s, error_message
assert actual[1].inputBoxes[0].y1s == correct[1].inputBoxes[0].y1s, error_message
assert actual[1].inputBoxes[0].x2s == correct[1].inputBoxes[0].x2s, error_message
assert actual[1].inputBoxes[0].y2s == correct[1].inputBoxes[0].y2s, error_message
assert actual[1].inputBoxes[0].score == correct[1].inputBoxes[0].score, error_message


# End
print("All tests passed successfully")
