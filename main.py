# Dependencies
import pandas as pd
import ast

# Class imports
from Classes import Image
from Classes import CSVParser
from Classes import CSVWriter

# def get_dict(df):
#     """ Returns a dictionary of an dataframe of predictions or
#         ground truth

#     Args:
#         df_gt (pd.Dataframe): the dataframe with input data

#     Returns:
#         dict: dictionary with the boxes sorted by img_id
#     """

#     boxes_per_img_id = {}
#     for idx, img_id in enumerate(df["img_id"]):
#         if "scores" in df.keys():
#             boxes_per_img_id[img_id] = {
#                 'labels': ast.literal_eval(df.iloc[idx]["labels"]),
#                 'x1s': ast.literal_eval(df.iloc[idx]["x1s"]),
#                 'y1s': ast.literal_eval(df.iloc[idx]["y1s"]),
#                 'x2s': ast.literal_eval(df.iloc[idx]["x2s"]),
#                 'y2s': ast.literal_eval(df.iloc[idx]["y2s"]),
#                 'scores': ast.literal_eval(df.iloc[idx]["scores"]),
#             }
#         else:
#             boxes_per_img_id[img_id] = {
#                 'labels': ast.literal_eval(df.iloc[idx]["labels"]),
#                 'x1s': ast.literal_eval(df.iloc[idx]["x1s"]),
#                 'y1s': ast.literal_eval(df.iloc[idx]["y1s"]),
#                 'x2s': ast.literal_eval(df.iloc[idx]["x2s"]),
#                 'y2s': ast.literal_eval(df.iloc[idx]["y2s"]),
#             }

#     return boxes_per_img_id

# # Data imports
# img_folder = '/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/images'

# file_gt = '/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/1_ground_truth_2a.csv'
# file_pred = '/Users/jacobjanak/Documents/Code/VideaHealth/CS410_VideaHealth_sample_data/2_input_model_predictions_2.csv'

# df_gt = pd.read_csv(file_gt)
# df_pred = pd.read_csv(file_pred)

# dict_pred = get_dict(df_pred)
# dict_gt = get_dict(df_gt)

# print(dict_gt)