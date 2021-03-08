"""
TO DO: Description
"""


class Image:

    def __init__(self, id, inputBoxes):
        self.id = id
        self.inputBoxes = inputBoxes

        self.inputDictionary = dict()

        for ppbox in inputBoxes:
            if ppbox.label not in self.inputDictionary:
                self.inputDictionary[ppbox.label] = [ppbox]
            else:
                self.inputDictionary[ppbox.label].append(ppbox)

        self.outputBoxes = self.postprocessing()

    def __str__(self):
        return f"id: {self.id}"

    def postprocessing(self):
        """ TO DO:
        Uses self.inputBoxes to generate self.outputBoxes

        Args:
            None

        Returns:
            None
        """

        return
