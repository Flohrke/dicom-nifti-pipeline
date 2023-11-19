## imports
import os
import config as c
from modules.base_logger import logger, logFile, configFile
import pickle as pkl
import shutil


### Pipeline STAGE 3 - image preprocessing via reshaping and reslicing

logger.info(f"## STAGE 4 has been started - creation of database")

# warning and abort in case of multiple images per patient were allowed during filtering
if c.allowMultiple:
    logger.info(f"-- WARNING: Creation of database will only select one img per patient. If multiple were allowed during filtering then they will be overwritten during copying into database!")
    logger.info(f"-- To resume deactivate allowMultiple in config and make sure only one image per patient was selected during filtering!")
    logger.info(f"## STAGE 4 aborted - creation of database")
    exit(1)

logger.info(f"--- Logging file created under: {logFile}")
logger.info(f"--- Saving config for documenbtation under: {configFile}")

logger.info(f"--- Loading list of filtered images")

# load collection of all filtered imgs for DB creation 
with open(c.pathFilteredImages, 'rb') as handle:
    imageCollection = pkl.load(handle)

# remove any empty slots that indicate that no imgs satisfied requirements for a patient
imageCollection = [x for x in imageCollection if type(x) == str]

# create Database folder structure
if not os.path.exists(c.databaseDirectory + c.databaseName):
    logger.info(f"--- Creating new database folder {c.databaseDirectory + c.databaseName}")
    os.makedirs(c.databaseDirectory + c.databaseName)
    os.makedirs(c.databaseDirectory + c.databaseName + "/imgs")
    os.makedirs(c.databaseDirectory + c.databaseName + "/labels")
    os.makedirs(c.databaseDirectory + c.databaseName + "/clinical")

# extract images from collection and rename to standardized filename regex
logger.info("--- Copying and renaming selected images")
exceptions = list()
for src in imageCollection:

    try:
        # get ID from filename
        oldFilename = src.split("/")[-1]
        ID = oldFilename.split("_")[0].split(c.patientKeywordDatabaseCreation)[1]

        # create new filename and pathing
        newFilename = ID + "_" + c.databaseName + "_" + c.modality + c.suffixToCreateDatabaseFrom
        dest = c.databaseDirectory + c.databaseName + "/imgs/" + newFilename

        # (optional) change src filename to use preprocessed img otherwise native images will be used
        if c.usePreprocessed:
            tmp = oldFilename.split(".")
            tmp = tmp[0] + "_resliced" + c.suffixToCreateDatabaseFrom
            src = src.split("/")[:-1]
            src.append(tmp)
            src = "/".join(src)
        
        # copy selected img
        logger.info("{} -> {}".format(src, dest))
        shutil.copy(src, dest)
    except Exception as e:
        exceptions.append(src)
        logger.info(f"-- ERROR for: {ID}")
        logger.info(e)

logger.info(f"-- Number of exceptions: {len(exceptions)}")
if len(exceptions) != 0:
    for exception in exceptions:
        logger.info({exception})
logger.info(f"-- Number of available images in database: {len(os.listdir(c.databaseDirectory + c.databaseName))}")
logger.info(f"## STAGE 4 has been finsihed - creation of database")





