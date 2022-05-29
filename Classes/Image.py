class Image:

    def __init__(self, id, inputBoxes = [], img_type=None):
        self.id = id
        self.inputBoxes = inputBoxes
        self.outputBoxes = []
        self.type = img_type

    def __repr__(self):
        return "{}: {} input | {} output".format(self.id, len(self.inputBoxes), len(self.outputBoxes))
