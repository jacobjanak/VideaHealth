from argparse import ArgumentParser
from pathlib import Path

# Import classes
from Classes.CSVReader import CSVReader
from Classes.Converter import Converter
from Classes.CSVWriter import CSVWriter
from Scripts.non_maximum_suppression import nonmaximum_suppression

# Import accuracy script for testing
from Scripts.missing_tooth import missing_tooth

# Import teeth arrangement script to correct teeth classification
from Scripts.teeth_arrangement import teeth_arrangements


parser = ArgumentParser(
    description="Postprocessing/filtering for tooth detection results")
parser.add_argument("-d", "--data", help="data directory")
parser.add_argument("-i", "--img", help="image directory")
parser.add_argument("-g", "--ground-truth",
                    dest="groundtruth", help="ground truth data")
parser.add_argument("-p", "--predictions", help="prediction data")
parser.add_argument("--iou", dest="iouThreshold", help="IoU threshold")
parser.add_argument("--conf", dest="confidenceThreshold", help="Confidence threshold")
parser.add_argument("-b", "--imgtype", help="")
args = parser.parse_args()

# File paths
project_dir = Path(__file__).parent.absolute()
current_dir = Path.cwd()
if args.data:
    data_dir = project_dir / args.data
else:
    data_dir = project_dir / "input"

if args.img:
    img_folder = data_dir / args.img
else:
    img_folder = str(data_dir / "images")

if args.groundtruth:
    file_gt = data_dir / args.groundtruth
else:
    file_gt = str(data_dir / "1_ground_truth.csv")

if args.predictions:
    file_pred = data_dir / args.predictions
else:
    file_pred = str(data_dir / "2_input_model_predictions.csv")

if args.imgtype:
    file_bw_pa = current_dir / args.imgtype
else:
    file_bw_pa = str(data_dir / "bw_pa.csv")

if args.iouThreshold:
    iouThreshold = args.iouThreshold
else:
    iouThreshold = 0.38
if args.confidenceThreshold:
    confidenceTheshold = args.confidenceThreshold
else:
    confidenceThreshold = 0.39

"""
    post_processing_filter
    
    params:
        file_pred = 
        iou_threshold
        confidence_threshold
        file_bw_pa
        
    returns:
        a list of Images


"""


def post_processing_filter(file_pred, iou_threshold, confidence_threshold, file_bw_pa=None):

    # Read the input CSV file
    input_raw = CSVReader(file_pred, file_bw_pa).output
    images_input = Converter(input_raw).result
    images_pred = nonmaximum_suppression(images_input, threshold=confidence_threshold, iouThreshold=iou_threshold)
    images_pred = teeth_arrangements(images_pred)
    images_pred = missing_tooth(images_pred)
    return images_pred

def main():
    data = post_processing_filter(file_pred, iouThreshold, confidenceThreshold)
    CSVWriter(data)


if __name__ == "__main__":
    main()


