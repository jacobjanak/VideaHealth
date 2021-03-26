"""
TO DO: Description
"""


class OutputBox:

    def __init__(self, label, x1s, y1s, x2s, y2s):
        self.label = label
        self.x1s = x1s
        self.y1s = y1s
        self.x2s = x2s
        self.y2s = y2s

    def vec1(self):
        return (int(self.x1s), int(self.y1s))

    def vec2(self):
        return (int(self.x2s), int(self.y2s))

