## imports
import config as c
from modules.base_logger import logger, logFile, configFile
from modules.imagefilterer import ImageFilterer
from modules.utility import find_images_by_suffix

### Pipeline STAGE 2 - filtering of images according to set requirements 

logger.info(f"## STAGE 2 has been started - image selection and filtering")

logger.info(f"--- Logging file created under: {logFile}")
logger.info(f"--- Saving config for documenbtation under: {configFile}")

imagePaths = find_images_by_suffix(c.outputDirectory , c.suffixToProcess)
imagefilterer = ImageFilterer(imagePaths)
logger.info(f"--- ImageFilterer build")

# only consider native imgs and not anything that already has been resliced
imagePaths = [img for img in imagePaths if "_resliced" not in img]

# for number of imgs consistency only consider individual scan folders (some might contain multiple versions of same imgs after conversion)
individualImgs = set(["/".join(img.split("/")[:-1]) for img in imagePaths])
logger.info(f"-- Number of available images: {len(individualImgs)}")

logger.info(f"--- Start of image filtering")
logger.info(f"-- Organizing images to corresponding patients")
imagefilterer.organize_patients()

logger.info(f"-- Selecting images of patients that contain keywords over native imgs")
imagefilterer.filter_patients_for_keywords(c.wantedKeywords)

logger.info(f"-- Filtering images for patients according to desired slice thickness")
if c.allowMultiple:
    logger.info(f"- Multiple eligible images per patient are allowed")
logger.info(f"- Minimum slice thickness that is allowed {c.desiredThicknessMin}")
logger.info(f"- Maximum slice thickness that is allowed {c.desiredThicknessMax}")
imagefilterer.filter_patients_for_slice_thickness(c.desiredThicknessMax, c.desiredThicknessMin, c.allowMultiple)
logger.info(f"-- Number of available images: {len(imagefilterer.imagePaths)}")

logger.info(f"--- Saving filtered list of image paths under: {c.pathFilteredImages}")
imagefilterer.save_filtered_list(c.pathFilteredImages)

logger.info(f"## STAGE 2 has been finished - image selection and filtering")








