## imports
import config as c
import pickle
from modules.base_logger import logger, logFile, configFile
from joblib import Parallel, delayed
from modules.imageprocessor import ImageProcessor
from modules.utility import find_images_by_suffix

### Pipeline STAGE 3 - image preprocessing via reshaping and reslicing

logger.info(f"## STAGE 3 has been started - image preprocessing via reshaping and reslicing")

logger.info(f"--- Logging file created under: {logFile}")
logger.info(f"--- Saving config for documenbtation under: {configFile}")

imageprocessor = ImageProcessor(c.outputDirectory)
logger.info(f"--- ImageProcessor build")
logger.debug(f"- INPUT: {imageprocessor.inputDirectory}")

# Either generate list of imgs to convert from inputDirectory or give list
if c.imagesGivenByList:
    logger.info(f"-- Images to process given by list at {c.pathImageList}")
    with open(c.pathImageList, "rb") as input_file:
        imagePaths = pickle.load(input_file)
else:
    logger.info(f"-- Creating list of available images in input directory")
    imagePaths = find_images_by_suffix(c.outputDirectory, c.suffixToProcess)

# only consider native imgs and not anything that already has been resliced
imagePaths = [img for img in imagePaths if "_resliced" not in img]

# for number of imgs consistency only consider individual scan folders (some might cotain multiple versions of same imgs after conversion)
individualImgs = set(["/".join(img.split("/")[:-1]) for img in imagePaths])
logger.info(f"-- Number of available images: {len(individualImgs)}")

logger.info(f"--- Start of image preprocessing")
reports = list()
reports.append(Parallel(c.nJobs)(delayed(imageprocessor.reslice_resample_nifti)(path, c.newDims, c.newVoxelDims, c.setSliceNumberByDesiredThickness)
                for path in imagePaths))
logger.info(f"--- End of image preprocessing")

# remove successful reports
reports = [x for x in reports[0] if x != 0]

logger.info(f"-- Number of exceptions: {len(reports)}")
if len(reports) != 0:
    logger.info(f"-- Exceptions:")
    for report in reports:
        logger.info(report)

logger.info(f"## STAGE 3 has been finished")




