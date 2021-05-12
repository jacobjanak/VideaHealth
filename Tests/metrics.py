import matplotlib.pylab as plt


class Metrics:

    def __init__(self,bbox_list, tp_fp_list, percision_list, recall_list):
        self.bbox_list = bbox_list
        self.tp_fp_list = tp_fp_list
        self.percision_list = percision_list
        self.recall_list = recall_list


    def visualize(self):



        plt.plot(self.recall_list, self.percision_list)
        plt.suptitle('Percision X Recall Curve with no Classification')
        plt.axis([0, 1.2, 0, 1.2])
        plt.ylabel('Percision')
        plt.xlabel('Recall')
        plt.show()

        pass

    def last_percision_recall(self):
        return self.percision_list[len(self.percision_list) -1], self.recall_list[len(self.recall_list) -1]

    def calculate_AP(self):

        pass

    def calculate_mAP(self):
        pass

    @classmethod
    def calculate_percision_recall_curv(cls, images_pred, images_gt, iou_threshold=0.7, byClassification=False):



        bbox_list = []
        tp_fp_list = []
        percision_list = []
        recall_list = []

        # put them in tuple (rank, fp/tp, percision, recall, interporlation(will considerlater))
        false_positives = 0
        true_positives = 0
        false_negatives = 0

        # Gives of len of all of the Ground Truth BoundaryBoxes in dataset
        for gt in images_gt:
            false_negatives += len(gt.inputBoxes)

        # needed to evaluate, but potentially not really
        true_pos_map_gt = {}
        passiou = None

        for i in range(len(images_pred)):

            if (len(images_pred[i].outputBoxes) == 0):
                images_pred[i].outputBoxes = images_pred[i].inputBoxes

            pred = images_pred[i].outputBoxes
            pred.sort(key=lambda x: x.score, reverse=True)
            gt = images_gt[i].inputBoxes

            for predictedBoundaryBox in pred:
                passiou = False
                for groundtruthBoundaryBox in gt:

                    # implementation later
                    # if (predictedBoundaryBox.label != groundtruthBoundaryBox.label):
                    #     continue

                    iou_score = predictedBoundaryBox.iou(groundtruthBoundaryBox)

                    # If it passes iou, the predictedBoundaryBox is a True Positive
                    if (iou_score >= iou_threshold):

                        # Storing data incase for future refrences
                        true_pos_map_gt[predictedBoundaryBox.label] = (predictedBoundaryBox,groundtruthBoundaryBox)
                        # We remove so other BoundaryBox can't find it as a TP
                        gt.remove(groundtruthBoundaryBox)
                        #we have
                        true_positives+=1
                        false_negatives-=1
                        passiou = True
                        break

                # If it never goes into the if block to break the nested for loop, then we count the predictedBox as a fp
                str = 'TP'
                if (passiou is False):
                    str = 'FP'
                    false_positives += 1

                percision = true_positives / (true_positives + false_positives)
                recall = true_positives / (true_positives + false_negatives)

                bbox_list.append(predictedBoundaryBox)
                tp_fp_list.append(str)
                percision_list.append(percision)
                recall_list.append(recall)

                #data.append((predictedBoundaryBox, str, percision, recall))

        return cls(bbox_list, tp_fp_list, percision_list, recall_list)


class info_label:
    def __init__(self, label,tp, fp, fn):
        self.label = label
        self.tp = tp
        self.fp = fp
        self.fn = fn
        self.bbox_list = []
        self.tp_fp_list = []
        self.percision_list = []
        self.recall_list = []

    def update(self, predictedBoundaryBox, tp_fp):
        percision = self.tp / (self.tp + self.fp)
        recall = self.tp / (self.tp + self.fn)

        self.bbox_list.append(predictedBoundaryBox)
        self.tp_fp_list.append(tp_fp)
        self.percision_list.append(percision)
        self.recall_list.append(recall)





class Metrics2:

    def __init__(self,bbox_list, tp_fp_list, percision_list, recall_list, classification_data):
        self.bbox_list = bbox_list
        self.tp_fp_list = tp_fp_list
        self.percision_list = percision_list
        self.recall_list = recall_list
        self.classification_data = classification_data


    def visualize(self):



        plt.plot(self.recall_list, self.percision_list)
        plt.suptitle('Percision X Recall Curve with no Classification')
        plt.axis([0, 1.2, 0, 1.2])
        plt.ylabel('Percision')
        plt.xlabel('Recall')
        plt.show()

        pass

    def last_percision_recall(self):
        return self.percision_list[len(self.percision_list) -1], self.recall_list[len(self.recall_list) -1]

    def visualize_2(self):

        for tooth_label, tooth in self.classification_data.items():
            plt.plot(tooth.recall_list, tooth.percision_list)
            plt.suptitle('Percision X Recall Curve for {}'.format(tooth_label))
            plt.axis([0, 1.2, 0, 1.2])
            plt.ylabel('Percision')
            plt.xlabel('Recall')
            plt.show()
            plt.clf()

    def calculate_AP(self):

        pass

    def calculate_mAP(self):
        pass

    @classmethod
    def calculate_percision_recall_curv(cls, images_pred, images_gt, iou_threshold=0.7):

        bbox_list = []
        tp_fp_list = []
        percision_list = []
        recall_list = []

        kek = dict()

        # put them in tuple (rank, fp/tp, percision, recall, interporlation(will considerlater))
        false_positives = 0
        true_positives = 0
        false_negatives = 0

        # Gives of len of all of the Ground Truth BoundaryBoxes in dataset
        for gt in images_gt:
            for gtbox in gt.inputBoxes:
                if gtbox.label in kek:
                    false_negatives +=1
                    kek[gtbox.label].fn +=1
                else:
                    false_negatives+=1
                    kek[gtbox.label] = info_label(gtbox.label, 0, 0, 1)


        # needed to evaluate, but potentially not really
        true_pos_map_gt = {}
        passiou = None

        for i in range(len(images_pred)):

            if (len(images_pred[i].outputBoxes) == 0):
                images_pred[i].outputBoxes = images_pred[i].inputBoxes

            pred = images_pred[i].outputBoxes
            pred.sort(key=lambda x: x.score, reverse=True)
            gt = images_gt[i].inputBoxes

            for predictedBoundaryBox in pred:
                passiou = False
                for groundtruthBoundaryBox in gt:

                    # If it's not the same label, we just skip it.
                    if (predictedBoundaryBox.label != groundtruthBoundaryBox.label):
                         continue

                    iou_score = predictedBoundaryBox.iou(groundtruthBoundaryBox)

                    # If it passes iou, the predictedBoundaryBox is a True Positive
                    if (iou_score >= iou_threshold):

                        # Storing data incase for future refrences
                        true_pos_map_gt[predictedBoundaryBox.label] = (predictedBoundaryBox,groundtruthBoundaryBox)
                        # We remove so other BoundaryBox can't find it as a TP
                        gt.remove(groundtruthBoundaryBox)
                        #we have
                        kek[predictedBoundaryBox.label].tp+=1
                        kek[predictedBoundaryBox.label].fn-=1

                        true_positives+=1
                        false_negatives-=1
                        passiou = True
                        break

                # If it never goes into the if block to break the nested for loop, then we count the predictedBox as a fp
                str = 'TP'
                predictedBoundaryBox.tp_fp = str
                if (passiou is False):
                    str = 'FP'
                    predictedBoundaryBox.tp_fp = str
                    if predictedBoundaryBox.label in kek:
                        kek[predictedBoundaryBox.label].fp += 1
                    false_positives += 1

                percision = true_positives / (true_positives + false_positives)
                recall = true_positives / (true_positives + false_negatives)

                bbox_list.append(predictedBoundaryBox)
                tp_fp_list.append(str)
                percision_list.append(percision)
                recall_list.append(recall)

                if predictedBoundaryBox.label in kek:
                    kek[predictedBoundaryBox.label].update(predictedBoundaryBox, str)



                #data.append((predictedBoundaryBox, str, percision, recall))

        return cls(bbox_list, tp_fp_list, percision_list, recall_list, kek)


if __name__ == '__main__':
    plt.plot([1,2,3,20])
    plt.ylabel('some numbers')
    plt.xlabel('some more numbers')
    plt.show()

    print(f"Hello World {__file__}")

# We need to implement a precision recall curve
# We can create a specific metric based on what we need
# If we plan to get the percision recall curve
#
#
