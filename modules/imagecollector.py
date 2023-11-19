import os
from modules.base_logger import logger
import logging
from nipype.interfaces.dcm2nii import Dcm2niix

# set logging level for nipype interface
nipypeLogger = logging.getLogger("nipype.interface")
nipypeLogger.setLevel(logging.ERROR)

### Class for the convesion of images to desired formats
## currently implemented: dicom -> nifti
class ImageCollector:
    def __init__(self, inputDirectory, outputDirectory):
        self.inputDirectory = inputDirectory
        self.outputDirectory = outputDirectory

    # remove all imgs that have unwanted keywords in filename (i.e. derived imgs)
    def remove_scans_with_unwanted_keywords(self, imagePaths, listOfUnwanted):
        pathsToRemove = list()
        for path in imagePaths:
            if any(ext in path for ext in listOfUnwanted):
                logger.debug("- {} has been removed".format(path))
                pathsToRemove.append(path)
        for path in pathsToRemove:
            imagePaths.remove(path)
        return imagePaths, pathsToRemove

    # convert dicom imgs to dicom and optional ignore secondary
    def dicom_to_nifti_converter(self, imagePath, patientKeyword, scanFolderName="scans"):

        # extract scan name by looking at position behind scan folder in path
        idxScan = imagePath.split("/").index(scanFolderName) + 1
        scanName = imagePath.split("/")[idxScan]

        # extract patient
        patient = ""
        tmp = imagePath.split("/")
        for i in tmp:
            if patientKeyword in i:
                patient = i
        
        # make directory and at the same time only convert dcm that doesn't already exist
        if not os.path.exists(os.path.join(self.outputDirectory, patient, scanName)):
            os.makedirs(os.path.join(self.outputDirectory, patient, scanName))

            logger.info("-- converting {} into scan directory {}".format(patient, scanName))
            converter = Dcm2niix()
            converter.inputs.source_dir = imagePath
            converter.inputs.out_filename = patient
            converter.inputs.merge_imgs = True
            converter.inputs.output_dir = os.path.join(self.outputDirectory, patient, scanName)

            # dont ignore derived since some are useful
            converter.inputs.ignore_deriv = False
            converter.run()

        else:
            logger.info("-- patient img {} in directory {} already exist -- skipped".format(patient, scanName))
        
        return 0

    


        