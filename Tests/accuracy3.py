import os

from Classes.TextWriter import TextWriter
import subprocess

def getMap(images_pred, images_gt):

    detWriter = TextWriter(images_pred)
    gtWriter = TextWriter(images_gt)
    detWriter.generate_maP_input()
    gtWriter.generate_maP_input(ground_truth=True)

    mainDir = os.getcwd()
    mapDir = mainDir + '\\Scripts\\maP'
    os.chdir(mapDir)
    #change directory working for said script (in order to keep it in one location)

    # run script with specific dataset
    output = subprocess.run(["python main.py -na -q -mainnp"], capture_output=True)
    # print(output.stdout)
    out = str(output.stdout)[8:14]
    os.chdir(mainDir)

    return out

