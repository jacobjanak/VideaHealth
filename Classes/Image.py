"""
TO DO: Description
"""


class Image:

    def __init__(self, id, inputBoxes = []):
        self.id = id
        self.inputBoxes = inputBoxes
        self.outputBoxes = []
        # self.outputBoxes = self.postprocessing()

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
