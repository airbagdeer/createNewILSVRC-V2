import os
import pathlib
import tarfile

import numpy as np


def main():
    dirPath = 'H:/imageNet-1k/untar_script_test'

    for file in os.listdir(dirPath):
        if isTar(file):
            fullFilePath = os.path.join(dirPath, file)
            newDirectory = os.path.join(dirPath, file.replace('.tar', ''))
            if not os.path.exists(newDirectory):
                os.makedirs(newDirectory)

            tar = tarfile.open(fullFilePath)
            tar.extractall(newDirectory)
            tar.close()

            os.remove(fullFilePath)


def isTar(path: str):
    return np.isin('.tar', pathlib.Path(path).suffix)


main()
