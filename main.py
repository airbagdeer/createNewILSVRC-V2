import os
import pathlib
import random
import shutil

import numpy as np

newILSVRCPath = 'H:/imageNet-1k/newILSVRC'
imagenetWholePath = 'H:/imageNet-1k/winter21_whole_test'
existingILSVRCPath = 'H:/imageNet-1k/test'
logFilePath = './logs'

if os.path.exists(logFilePath):
    raise Exception('log file exists')

logFile = open('./logs', 'w+')


def main():
    ILSVRCLabels = getLabels(existingILSVRCPath)
    imagenetWholeLabels = getLabels(imagenetWholePath)

    count = 0

    for label in ILSVRCLabels:
        if label in imagenetWholeLabels:
            newILSVRCImagesPath = os.path.join(newILSVRCPath, label)
            if not os.path.exists(newILSVRCImagesPath):
                os.makedirs(newILSVRCImagesPath)

            logFile.write(f'{count}, label: {label} ,')

            replace_existing_images_with_new(os.path.join(existingILSVRCPath, label),
                                             os.path.join(imagenetWholePath, label),
                                             newILSVRCImagesPath)



def replace_existing_images_with_new(ILSVRCImagesPath: str, imagenetWholeImagesPath: str, newImagesPath: str):
    existingImages = os.listdir(ILSVRCImagesPath)
    newImages = os.listdir(imagenetWholeImagesPath)

    if len(existingImages) * 2.1 < len(newImages):
        replace_all(ILSVRCImagesPath, imagenetWholeImagesPath, newImagesPath)
    else:
        replace_some(ILSVRCImagesPath, imagenetWholeImagesPath, newImagesPath)


def replace_all(ILSVRCImagesPath: str, imagenetWholeImagesPath: str, newILSVRCImagesPath: str):
    buffer = 1 - random.uniform(-0.1, 0.1)
    existingILSVRCImages = os.listdir(ILSVRCImagesPath)
    imagenetWholeImages = os.listdir(imagenetWholeImagesPath)

    newILSVRCAmount = int(len(existingILSVRCImages) * buffer)

    logFile.write(
        f'method: replace_all, existing ILSVRC amount: {len(existingILSVRCImages)}, new ILSVRC amount: {newILSVRCAmount}, imagenet whole amount: {len(imagenetWholeImages)}, buffer: {buffer} \n')

    for image in imagenetWholeImages:
        if image not in existingILSVRCImages:
            shutil.copy(os.path.join(imagenetWholeImagesPath, image), newILSVRCImagesPath)
            newILSVRCAmount -= 1
        if newILSVRCAmount == 0:
            return


def replace_some(ILSVRCImagesPath: str, imagenetWholeImagesPath: str, newILSVRCImagesPath: str):
    existingILSVRCImages = os.listdir(ILSVRCImagesPath)
    imagenetWholeImages = os.listdir(imagenetWholeImagesPath)
    buffer = 1 - random.uniform(-0.1, 0.1)

    differentImages = len(imagenetWholeImages) - len(existingILSVRCImages)
    missingAmount = int(len(existingILSVRCImages) * buffer) - differentImages

    logFile.write(
        f'method: replace_some, existing ILSVRC amount: {len(existingILSVRCImages)}, new ILSVRC amount: {differentImages + missingAmount}, imagenet whole amount: {len(imagenetWholeImages)}, buffer: {buffer} \n')

    for image in imagenetWholeImages:
        if image not in existingILSVRCImages:
            shutil.copy(os.path.join(imagenetWholeImagesPath, image), newILSVRCImagesPath)

    missingImages = random.sample(existingILSVRCImages, missingAmount)

    for image in missingImages:
        shutil.copy(os.path.join(imagenetWholeImagesPath, image), newILSVRCImagesPath)


def checkFileEnding(path: str, ending: str = '.tar'):
    return np.isin(ending, pathlib.Path(path).suffix)


def getAllFolders(path: str):
    return [f.path.replace('\\', '/') for f in os.scandir(path) if f.is_dir()]


def getLabels(folder: str):
    labels = []

    for file in getAllFolders(folder):
        if os.path.isdir(file):
            labels.append(os.path.basename(file))

    return labels


main()
logFile.close()
