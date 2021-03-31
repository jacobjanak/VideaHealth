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

    def area(self):
        return (self.x2s - self.x1s + 1) * (self.y2s - self.y1s + 1)

    def intersect(self, box2):
        xa = max(self.x1s, box2.x1s)
        ya = max(self.y1s, box2.y1s)
        xb = min(self.x2s, box2.x2s)
        yb = min(self.y2s, box2.y2s)
        a = max(0, xb - xa + 1)
        b = max(0, yb - ya + 1)
        c = a * b
        return max(0, xb - xa + 1) * max(0, yb - ya + 1)

    def union(self, box2):
        return self.area() + box2.area() - self.intersect(box2)

    def iou(self, box2):
        idk = self.intersect(box2) / (self.union(box2))
        return idk

    def vec1(self):
        return (int(self.x1s), int(self.y1s))

    def vec2(self):
        return (int(self.x2s), int(self.y2s))
