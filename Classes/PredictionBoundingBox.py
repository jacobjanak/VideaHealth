"""
TO DO: Description
"""


class PredictionBoundingBox:

    def __init__(self, label, x1, y1, x2, y2, score=None):
        self.label = label
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.score = score

    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    def intersect(self, box2):
        xa = max(self.x1, box2.x1)
        ya = max(self.y1, box2.y1)
        xb = min(self.x2, box2.x2)
        yb = min(self.y2, box2.y2)
        a = max(0, xb - xa + 1)
        b = max(0, yb - ya + 1)
        c = a * b
        return max(0, xb - xa + 1) * max(0, yb - ya + 1)

    def union(self, box2):
        return self.area() + box2.area() - self.intersect(box2)

    def iou(self, box2):
        idk = self.intersect(box2) / (self.union(box2))
        return idk
