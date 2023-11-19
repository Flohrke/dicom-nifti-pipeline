from modules.base_logger import logger
import nibabel as nib
import pickle as pkl
import os
from modules.utility import closest_value

### Class for the convesion of images to desired formats
## currently implemented: dicom -> nifti
class ImageFilterer:
    def __init__(self, imagePaths) -> None:
        self.imagePaths = imagePaths
        
    def organize_patients(self):
        # collect all unique patients
        patients = list()
        for path in self.imagePaths:
            patient = path.split("/")[-3]
            patients.append(patient)
        patients = list(set(patients))

        # create dict with patient as key and all paths belonging to the patient as item
        pathsPerPatient = {}
        for patient in patients:
            patientPaths = [i for i in self.imagePaths if patient in i]
            pathsPerPatient[patient] = patientPaths

        # save changes to image paths list
        self.imagePaths = pathsPerPatient
    
    def filter_patients_for_keywords(self, wantedKeywords) -> None:
        # iterate over each patient with corresponding img paths
        filteredPatients = {}
        for key, item in self.imagePaths.items():
            tmp = item.copy()

            # check for ideal scenario that img contains all keyowrds
            filteredPaths = [i for i in tmp if all(xi in i for xi in wantedKeywords)]

            # if non found check for second best of img containing some keywords
            if len(filteredPaths) == 0:
                filteredPaths = [i for i in tmp if any(xi in i for xi in wantedKeywords)]
            
            # if none found leave paths unfiltered
            if len(filteredPaths) == 0:
                filteredPaths = tmp
            filteredPatients[key] = filteredPaths

        # save changes to image paths list
        self.imagePaths = filteredPatients

    def filter_patients_for_slice_thickness(self, desiredThicknessMax, desiredThicknessMin, allowMultiple=False) -> None:
        imgsWithElegibleThickness = list()
        for patient, paths in self.imagePaths.items():
            # load all slice thicknesses
            tmp = list()
            thicknesses = list()
            for path in paths:
                img = nib.load(path)
                thickness = img.header["pixdim"][3]

                # filter out paths that have thickness above desired value
                if thickness <= desiredThicknessMax and thickness >= desiredThicknessMin:
                    tmp.append(path)
                    thicknesses.append(thickness)

            # if no imgs eligible just append empty list
            if len(tmp) == 0:
                logger.info(f"-- no eligible imgs found for patient {patient}")
                imgsWithElegibleThickness.append(tmp)
                continue
            # if multiple path are eligible and multiple is allowed append all paths
            elif allowMultiple:
                print(f"-- {len(tmp)} imgs found for patient {patient}")
                imgsWithElegibleThickness.append(tmp)
                continue
            # if multiple not allowed the from all eligible paths of a patient select the one that has thickness closest to desired value
            else:
                logger.info(f"-- best img selected for patient {patient}")      
                value = closest_value(thicknesses, desiredThicknessMax)
                logger.info(f"-- best thickness value used {value}")
                tmp = tmp[thicknesses.index(value)]
            imgsWithElegibleThickness.append(tmp)

        # save changes to image paths list
        imgsWithElegibleThickness = [img for img in imgsWithElegibleThickness if len(img) != 0]
        self.imagePaths = imgsWithElegibleThickness

    def save_filtered_list(self, pathImgList) -> None:
        with open(pathImgList, 'wb') as handle:
            pkl.dump(self.imagePaths, handle)
