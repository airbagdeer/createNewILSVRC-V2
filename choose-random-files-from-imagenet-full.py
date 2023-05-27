import os
import random
from distutils.dir_util import copy_tree

newILSVRCPath = '/media/eyal-linux/HDD/newILSVRC-V2/'
existingILSVRCPath = '/home/eyal-linux/Desktop/dropout/ILSVRC/Data/CLS-LOC/train/'
testPath = '/media/eyal-linux/HDD/TEST'
imagenetWholePath = '/media/eyal-linux/HDD/winter21_whole'
# imagenetWholePath = testPath

def main():
    ILSVRCLabels = getLabels(existingILSVRCPath)
    imagenetWholeLabels = getLabels(imagenetWholePath)

    iterations = 1000

    newILSVRCPathLabels = []

    while iterations > 0:
        while True:
            newLabel = random.choice(imagenetWholeLabels)
            amountOfImagesInLabel = countFilesInFolder(newLabel)

            if (newLabel not in ILSVRCLabels) and (newLabel not in newILSVRCPathLabels) and (
                    amountOfImagesInLabel >= 1100) and (amountOfImagesInLabel <= 1600):
                copyFolderToNewILSVRC(newLabel)
                newILSVRCPathLabels.append(newLabel)
                iterations -= 1
                print(1000 - iterations, "/", 1000, newLabel)
                break


def copyFolderToNewILSVRC(label):
    newFolder = os.path.join(newILSVRCPath, label)
    os.mkdir(newFolder)
    copy_tree(os.path.join(imagenetWholePath, label), newFolder)


def getLabels(folder: str):
    labels = []

    for file in getAllFolders(folder):
        if os.path.isdir(file):
            labels.append(os.path.basename(file))

    return labels


def getAllFolders(path: str):
    return [f.path.replace('\\', '/') for f in os.scandir(path) if f.is_dir()]


def countFilesInFolder(label):
    return len(os.listdir(os.path.join(imagenetWholePath, label)))


main()
