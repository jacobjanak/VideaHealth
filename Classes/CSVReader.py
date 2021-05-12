"""
This class reads a CSV file given a file path. It does not modify the data at all.

It will automatically detect wether the CSV file is an input or an output. The difference
is that an input CSV will have a "scores" field whereas an output CSV will not.
"""

import pandas as pd
import ast


class CSVReader:

    def __init__(self, path, img_type_path = None):
        if path[-4:] != ".csv":
            raise ValueError("CSV Parser can only parse files ending in .csv")
        
        csv_df = pd.read_csv(path)

        self.path = path
        self.output = self.dataframe_to_dict(csv_df)

        if img_type_path is not None:
            csv_df = pd.read_csv(img_type_path)
            dataset = self.dataframe_to_pw(csv_df)

            pass

    def dataframe_to_pw(self, df):

        for idx, img_id in enumerate(df["img_id"]):
            img_id =  df.iloc[idx]["img_id"]
            img_type = df.iloc[idx]["bw_pa"]
            if (img_id in self.output):
                self.output[img_id]["img_type"] = img_type


    def dataframe_to_dict(self, df):
        """
        Returns a dictionary of a dataframe of predictions or ground truths
        without altering any data or the data structure.

        Args:
            df (pd.Dataframe): the dataframe with input data

        Returns:
            dict: dictionary with the boxes
        """

        boxes_per_img_id = {}
        for idx, img_id in enumerate(df["img_id"]):
            boxes_per_img_id[img_id] = {
                "labels": ast.literal_eval(df.iloc[idx]["labels"]),
                "x1s": ast.literal_eval(df.iloc[idx]["x1s"]),
                "y1s": ast.literal_eval(df.iloc[idx]["y1s"]),
                "x2s": ast.literal_eval(df.iloc[idx]["x2s"]),
                "y2s": ast.literal_eval(df.iloc[idx]["y2s"]),
            }
            if "scores" in df:
                boxes_per_img_id[img_id]["scores"] = ast.literal_eval(df.iloc[idx]["scores"])

        return boxes_per_img_id