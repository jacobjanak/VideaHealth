import os

class TextWriter:

    def __init__(self, dataset):
        self.dataset = dataset
        self.filename = None

    # If dataset is ground truth, write a line into the filestream
    def _writegt(self, filestream, box):
        #                   <class_name> <confidence>   <left> <top> <right> <bottom>
        filestream.write(f"{box.label} {int(box.x1s)} {int(box.y1s)} {int(box.x2s)} {int(box.y2s)}\n")

    # If the data set is the detection result, write a line into the filestream
    def _writedtr(self, filestream, box):
        #                   <class_name> <confidence>   <left>         <top>        <right>          <bottom>
        filestream.write(f"{box.label} {box.score} {int(box.x1s)} {int(box.y1s)} {int(box.x2s)} {int(box.y2s)}\n")

    def generate_maP_input(self, ground_truth=False, flderdirect=None):



        dir_path = os.getcwd() + "\\Scripts\\maP\\input"

        #
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        # Create a folder
        folder_path = "detection-results"
        if ground_truth is True:
            folder_path = "ground-truth"
        folder_path = f"{dir_path}\\{folder_path}"

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)


        # For each for each Image object within a List
        for imgcount, image in enumerate(self.dataset):
            f = open(f"{folder_path}\\{image.id}.txt", "w")

            # For each BoundaryBox(Box) in the List of Boxes
            if len(image.outputBoxes) == 0:
                image.outputBoxes = image.inputBoxes

            for boxcount, box in enumerate(image.outputBoxes):

                if ground_truth is False:
                    self._writedtr(f, box)
                else:
                    self._writegt(f, box)

            # Close the filestream
            f.close()









