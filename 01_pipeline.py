## imports
import config as c
from modules.base_logger import logger, logFile, configFile
from joblib import Parallel, delayed
from modules.imagecollector import ImageCollector
from modules.utility import find_paths_by_suffix

### Pipeline STAGE 1 - collection and conversion of images

logger.info("### Start of preprocessing pipeline")

logger.info(f"## STAGE 1 has been started - Collection of eligible images and conversion")

logger.info(f"-- Logging file created under: {logFile}")
logger.info(f"-- Saving config for documenbtation under: {configFile}")

imagecollector = ImageCollector(c.inputDirectory, c.outputDirectory)
logger.info(f"--- ImageCollector build")
logger.debug(f"- INPUT: {imagecollector.inputDirectory}")
logger.debug(f"- OUTPUT: {imagecollector.outputDirectory}")

logger.info(f"--- Creating list of available image scan folders in input directory")
imagePaths = find_paths_by_suffix(c.inputDirectory , c.suffixToConvert)
logger.info(f"-- Number of available images: {len(imagePaths)}")

logger.info(f"--- Filtering out all images that contain unwanted keywords: {c.unwantedKeywords}")
imagePaths, removedPaths = imagecollector.remove_scans_with_unwanted_keywords(imagePaths, c.unwantedKeywords)
logger.info(f"-- Images that have been removed:")
for path in removedPaths:
    logger.info(f"- {path}")
logger.info(f"-- Number of available images: {len(imagePaths)}")

logger.info(f"--- Starting image conversion")
Parallel(c.nJobs)(delayed(imagecollector.dicom_to_nifti_converter)(path, c.patientKeywordConversion, c.scanFolderName)
                for path in imagePaths)

logger.info(f"## STAGE 1 has been finished")


