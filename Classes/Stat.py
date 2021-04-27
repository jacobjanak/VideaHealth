class Stat:
    def __init__(self, score, iou, p, r, f1):
        self.score = score
        self.iou = iou
        self.p = p
        self.r = r
        self.f1 = f1

    def __repr__(self):
        return '{} {}: precision, recall = ({}, 0.{}) f1 = {}'.format(self.score, self.iou, self.p, self.r, self.f1)