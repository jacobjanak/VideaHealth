"""
TO DO: Description
"""


class Box:

    def __init__(self, label, x1, y1, x2, y2, score=None):
        self.label = label
        self.x1s = x1
        self.y1s = y1
        self.x2s = x2
        self.y2s = y2
        self.score = score
        self.tp_fp = None

    def area(self):
        return (self.x2s - self.x1s) * (self.y2s - self.y1s)

    # return a tuple cointing the coordinates (x, y)
    def midpoint(self):
        return ((self.x1s + self.x2s) / 2, (self.y1s + self.y2s) / 2)

    # return the number in the tooths label
    def tooth_num(self):
        return int(self.label[6:])

    def new_label(self, number):
        self.label = "tooth_" + str(number)

    def intersect(self, box2):
        xa = max(self.x1s, box2.x1s)
        ya = max(self.y1s, box2.y1s)
        xb = min(self.x2s, box2.x2s)
        yb = min(self.y2s, box2.y2s)
        return max(0, xb - xa) * max(0, yb - ya)

    def union(self, box2):
        return self.area() + box2.area() - self.intersect(box2)

    def iou(self, box2):
        return self.intersect(box2) / (self.union(box2))

    def vec1(self):
        return (int(self.x1s), int(self.y1s))

    def vec2(self):
        return (int(self.x2s), int(self.y2s))

    def __repr__(self):
        if (self.score):
            return "{}: score={:.2f} |{:.2f}, {:.2f}, {:.2f}, {:.2f}|".format(self.label, self.score, self.x1s, self.y1s, self.x2s, self.y2s)
        else:
            return "{}: |{:.2f}, {:.2f}, {:.2f}, {:.2f}|".format(self.label, self.x1s, self.y1s, self.x2s, self.y2s)
