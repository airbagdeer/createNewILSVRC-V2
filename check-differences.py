import os

import matplotlib.pyplot as plt

newILSVRCPath = '/media/eyal-linux/HDD/newILSVRC-V2/'
imagenetWholePath = '/media/eyal-linux/HDD/winter21_whole'
existingILSVRCPath = '/home/eyal-linux/Desktop/dropout/ILSVRC/Data/CLS-LOC/train/'
testPath = '/media/eyal-linux/HDD/TEST'
existingILSVRCValPath = '/home/eyal-linux/Desktop/dropout/ILSVRC/Data/CLS-LOC/val/'


def main(folderPath):
    foldersInside = getAllFolders(folderPath)
    countFilesInAllFolders = []
    for folder in foldersInside:
        countFilesInAllFolders.append(countFilesInFolder(folder))
    # print(len(countFilesInAllFolders))
    # print(len(foldersInside))
    print_distribution(countFilesInAllFolders)


def print_distribution(numbers):
    plt.hist(numbers, bins='auto', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Number Distribution')
    # plt.yticks(range(0, max(plt.yticks()[0]), 100))  # Adjust the step size (100) as needed
    plt.show()


def countFilesInFolder(folder_path):
    return len(os.listdir(folder_path))

def getAllFolders(path: str):
    return [f.path.replace('\\', '/') for f in os.scandir(path) if f.is_dir()]

# main(existingILSVRCPath)
main(newILSVRCPath)
# main(imagenetWholePath)
# main(testPath)
# main(existingILSVRCValPath)