import os
import random
import shutil
from distutils.dir_util import copy_tree

newILSVRCPath = '/media/eyal-linux/HDD/newILSVRC-V2/'
existingILSVRCPath = '/home/eyal-linux/Desktop/dropout/ILSVRC/Data/CLS-LOC/train/'
testPath = '/media/eyal-linux/HDD/TEST'
imagenetWholePath = '/media/eyal-linux/HDD/winter21_whole'
# imagenetWholePath = testPath

logFilePath = './logsMistake'

# if os.path.exists(logFilePath):
#     raise Exception('log file exists')

logFile = open(logFilePath, 'w+')


def main():
    ILSVRCLabels = getLabels(existingILSVRCPath)
    imagenetWholeLabels = getLabels(imagenetWholePath)

    newILSVRCPathLabels = getLabels(newILSVRCPath)

    while countFilesInFolder(newILSVRCPath) <= 1000:
        while True:
            newLabel = random.choice(imagenetWholeLabels)
            amountOfImagesInLabel = len(os.listdir(os.path.join(imagenetWholePath, newLabel)))

            if(newLabel not in newILSVRCPathLabels) and (
                    amountOfImagesInLabel >= 1450):
                copyFolderToNewILSVRC(newLabel)
                newILSVRCPathLabels.append(newLabel)
                print(countFilesInFolder(newILSVRCPath), "/", 1000, newLabel, amountOfImagesInLabel)
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


def countFilesInFolder(folder_path):
    return len(os.listdir(folder_path))


def fixMistake():
    newILSVRCFolders = getAllFolders(newILSVRCPath)

    amountDeleted = 0

    for folder in newILSVRCFolders:
        filesInFolder = countFilesInFolder(folder)
        if filesInFolder < 1450:
            shutil.rmtree(folder)
            amountDeleted += 1
            print(amountDeleted, os.path.basename(folder))
            logFile.write(
                f'{amountDeleted}, folderDeleted: {os.path.basename(folder)}, files In Folder: {filesInFolder} \n')


# main()
# print(countFilesInFolder(existingILSVRCPath))
fixMistake()

logFile.close()
