
### logging
# SAVE CONFIG HERE AS WELL AFTER RUN to see parameters
name = "Test" # name of preprocessing run (used for logging and documentation)
logLevel = "INFO" # DEBUG/INFO/WARNING/ERROR/CRITICAL

### Selection of pipeline steps
## 1 = extraction of images that comply with requirements (methods of image creation) and conversion to defined image type
## 2 = filtering of images according to requirments regarding (shape, slice characteristics)
## 3 = preprocessing of images via reshaping and reslicing (either all in directory or given by filtered list from 2)
## 4 = creation of database folder from selected images (list given by 2)

### 0. Parameters for pathing 
inputDirectory = "/mnt/c/Users/Felix/Desktop/WORK/CLAIM/Github/Validate/image-preprocessing/oldPipeline/testData/testingDICOM"
outputDirectory = "/mnt/c/Users/Felix/Desktop/WORK/CLAIM/Github/Validate/image-preprocessing/oldPipeline/testData/testingNifti" # used as input in all STAGES but STAGE 1
databaseDirectory = "/mnt/c/Users/Felix/Desktop/WORK/CLAIM/Github/Validate/image-preprocessing/oldPipeline/testData/"

### 1. Extraction of valid images and conversion of image types
patientKeywordConversion = "MrClean" # short string that indicates location of patient ID in path
scanFolderName = "scans" # name of folder that contains the different scans of each patient
unwantedKeywords = ["mip", "MIP", "COR", "cor", "secondary"] # keywords in the img names that are unwanted (used to exclude derived images for example)
suffixToConvert = ".dcm" # suffix of image files that is searched for (dcm for DICOM files)
nJobs = -1 # number of parallel jobs

### 2. Creation of filtered list of images
allowMultiple = False # if multiple scans of a patient satisfy the requirements allow multiple scans to be selected per patient otherwise only one scan per paient is selected (closest slice thickness to desired thickness)
wantedKeywords = ["Tilt", "Eq"] # keywords to select niftis that were tilt corrected or voxel size equalized if they are available (otherwise native img is chosen)
desiredThicknessMax = 5.5 # desired slice thickness to select patients for (below or match)
desiredThicknessMin = 4.5 # desired slice thickness to select patients for (below or match)
pathFilteredImages = "pipeline/filteredListOfImgs.pkl"

### 3. NIFTI reshape and reslice 
imagesGivenByList = True
pathImageList = "pipeline/filteredListOfImgs.pkl" # if imagesGivenByList == True this is the path to the list (usually created by filtering via STAGE 2)
suffixToProcess = ".nii.gz"
newDims = [512, 512, "original"] # add desired new dimensions if they should remain unchanged add "original"
newVoxelDims = ["original", "original", "original"]
## THIS OVERWRITES THE SET NUMBER OF SLICES
setSliceNumberByDesiredThickness = True # if set to true then the number of slices in a given img will automatically be chosen according to the given desired thickness of slices 

### 4. Creation of database
usePreprocessed = True # if true then resliced images will be used for database creation
databaseName = "BL_NCCT_DB_MMOP_NEW" # name of database
modality = "ncct" # modality of imgs used
patientKeywordDatabaseCreation = "MrClean" # used to extract patient id from filenames
suffixToCreateDatabaseFrom = ".nii.gz" # suffix of img files