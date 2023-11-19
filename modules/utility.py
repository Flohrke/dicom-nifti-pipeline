import numpy as np
import os

def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

# get value from list of values that is closest to input value
def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]

# returns list of all paths to files with the given suffix
def find_images_by_suffix(inputDirectory, targetSuffix) -> list:
    pathList = []
    for dirname, _, filenames in os.walk(inputDirectory):
        for filename in filenames:
            if targetSuffix in filename:
                imagePath = os.path.join(dirname, filename)
                pathList.append(imagePath)

    return list(set(pathList))

# returns list of all paths to folders that contain files with the given suffix
def find_paths_by_suffix(inputDirectory, targetSuffix) -> list:
    pathList = []
    for dirname, _, filenames in os.walk(inputDirectory):
        for filename in filenames:
            if targetSuffix in filename:
                imagePath = os.path.join(dirname, filename)

                # only get the structure up to folder containing img files
                imagePath = "/".join(imagePath.split("/")[:-1])
                pathList.append(imagePath)
    return list(set(pathList))