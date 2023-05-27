import os
import random
import shutil
import pandas as pd

# newILSVRCTrainPath = '/media/eyal-linux/HDD/newILSVRC-V2/train/'
# newILSVRCValPath = '/media/eyal-linux/HDD/newILSVRC-V2/val/'
# newILSVRCTestPath = '/media/eyal-linux/HDD/newILSVRC-V2/test/'

train = ''
newILSVRCTrainPath = train
test = ''
newILSVRCTestPath = test
val = ''
newILSVRCValPath = val

testSplitLogPath = './testSplitLog'
removedLogPath = './removedLog'

removedLog = open(removedLogPath, 'w+')
testSplitLog = open(testSplitLogPath, 'w+')

if os.path.exists(testSplitLogPath):
    raise Exception('testSplitLog file exists')

if os.path.exists(removedLogPath):
    raise Exception('removedLog file exists')

valAmount = 50
testAmount = 100
amountOfTrainImages = 1300


def splitToVal():
    newILSVRCFolders = getAllFolders(newILSVRCTrainPath)

    for folder in newILSVRCFolders:
        newDirectory = os.path.join(newILSVRCValPath, getLabel(folder))
        os.mkdir(newDirectory)

        folderImages = os.listdir(folder)
        valImages = random.choices(folderImages, k=valAmount)

        for image in valImages:
            imagePath = os.path.join(newILSVRCTrainPath, image)
            shutil.copyfile(imagePath, newDirectory)
            os.remove(imagePath)
        print(f'finished with {folder}')

def splitToTest():
    newILSVRCFolders = getAllFolders(newILSVRCTrainPath)

    testLabelsDF = pd.DataFrame(columns=['image', 'label'])

    for folder in newILSVRCFolders:
        folderImages = os.listdir(folder)
        testImages = random.choices(folderImages, k=testAmount)
        label = getLabel(folder)

        for image in testImages:
            imagePath = os.path.join(newILSVRCTrainPath, image)
            shutil.copyfile(imagePath, newILSVRCTrainPath)
            os.remove(imagePath)
            newRow = {'image': f'{image}', 'label': f'{label}'}
            testLabelsDF = testLabelsDF.append(newRow, ignore_index=True)
            testSplitLog.write(f'image name: {image}, taken from: {label} \n')
            print(f'image name: {image}, taken from: {label}')

    testLabelsDF.to_csv('./test-labels.csv', index=False)


def removeUnnecessaryFiles():
    newILSVRCFolders = getAllFolders(newILSVRCTrainPath)

    for folder in newILSVRCFolders:
        images = os.listdir(folder)
        amountRemoved = 0

        while len(os.listdir(folder)) > 1300:
            randomImage = random.choice(images)
            randomImagePath = os.path.join(newILSVRCTrainPath, randomImage)
            if (os.path.exists(randomImagePath)):
                os.remove(randomImagePath)
                amountRemoved += 1
                removedLog.write(f'label: {os.path.basename(folder)}, image remove: {randomImage} \n')
                print(f'label: {os.path.basename(folder)}, image remove: {randomImage} \n')

        removedLog.write(f'in label: {os.path.basename(folder)}, totally removed: {amountRemoved}')


def getLabels(folder: str):
    labels = []

    for file in getAllFolders(folder):
        if os.path.isdir(file):
            labels.append(os.path.basename(file))

    return labels


def getLabel(folder):
    return os.path.basename(folder)


def getAllFolders(path: str):
    return [f.path.replace('\\', '/') for f in os.scandir(path) if f.is_dir()]


def countFilesInFolder(folder_path):
    return len(os.listdir(folder_path))


# splitToVal()
# splitToTest()
# removeUnnecessaryFiles()

testSplitLog.close()
removedLog.close()
