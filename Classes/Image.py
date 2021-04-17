"""
TO DO: Description
"""


class Image:

    def __init__(self, id, inputBoxes = [], img_type=None):
        self.id = id
        self.inputBoxes = inputBoxes
        self.outputBoxes = []
        self.type = img_type
        # self.outputBoxes = self.postprocessing()

    def __repr__(self):
        return "{}: {} input | {} output".format(self.id, len(self.inputBoxes), len(self.outputBoxes))

    # Eventually we will place our script in this method
    # def postprocessing(self):
    #     """ TO DO:
    #     Uses self.inputBoxes to generate self.outputBoxes

    #     Args:
    #         None

    #     Returns:
    #         None
    #     """

    #     return
