


class percision_recall_class:

    def __init__(self, data):
        pass


    def visualize(self):
        # should show a plot graph
        pass

    def calculate_AP(self):

        pass

    def calculate_mAP(self):
        pass

    @classmethod
    def calculate_percision_recall_curv(self, images_pred, images_gt):

        pred = images_pred[6].inputBoxes.sort(key=lambda x:x.score, reverse=True)
        gt = images_gt[6].inputBoxes




        return None




# We need to implement a precision recall curve
# We can create a specific metric based on what we need
# If we plan to get the percision recall curve
#
#
