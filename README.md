# image-preprocessing pipeline

### File overview
* [config.py](config.py): Config file for setting paths and parameters of pipeline
* [01_imageExtraction.py](01_imageExtraction.py): Script for extracting valid image files (filtering by keywords) and conversion to nifti 
* [02_imagePreprocessing.py](02_imagePreprocessing.py): Script for reslice/reshape operations and optional creation of list for images that satisfy slice thickness requirements 
* [03_imageMMOPPreparation.py](03_imageMMOPPreparation.py): Script that uses prior created image list to build MMOP Database

### How to use
00. * [config.py](config.py)
* See below the different parameters separated by to which part of the pipeline apply 

01. [01_imageExtraction.py](01_imageExtraction.py)
* *inputDirDICOM*/*outputDirNIFTI*: set the input path for the dicom imgs and the output path for the nifti imgs
* *patientKeyword*: defines a keyword given that indicates the location of the patient ID in the foldername of the input directory (example foldername: 0001dummy_dummyDB would use "dummy")
* *scanFolderName*: defines the name of the folder in the input directory that contains the .dcm files
* *unwantedKeywords*: words contained in scanfolder names that should be excluded from conversion (for example that indicate derived imgs)
* *ignore*: in the case of some folders being named differently that contain imgs that are unwanted
* *suffixToConvert*: filename suffix to identify files to convert (currently only supports "dcm")
* *n_jobs*: number of jobs to run for parallel processing 

02. [02_imagePreprocessing.py](02_imagePreprocessing.py)
* *inputDirNIFTI* set the input path for the nifti imgs / preprocessed imgs will be saved here too with added descriptor "_resliced"
* *suffix*: filename suffix to identify files to convert (currently only supports "nii.gz")
* *newDims*: List with new dimensions the imgs should be reshaped into / if original shapes should be kept than the input is "original" (example if x and y should be changed to 512 and z should be unchanged: [512, 512, "original"])
* *newVoxelDims*: List with new dimensions the voxels should be resliced into / if original shapes should be kept than the input is "original" (example if x and y should be changed to 2 mm and z should be unchanged: [2, 2, "original"])
* *prepareListOfFilteredImgs*: if set true a list of paths is created which is filtered according to certain criteria (used for MMOP Database creation in step 03)
* *wantedKeywords*: keywords that are used when filtering to be prefered over imgs without the keywords (example: when dcm are converted they are sometimes tilt corrected and equalized -> output folder contains then Tilt/Eq imgs and the originals -> with keywords "Tilt/Eq" the corrected imgs are then preferred)
* *desiredThickness*: slice thickness that is desired for filtered list / only imgs are selected that have the desired thickness or a thickness below
* *allowMultiple*: if true multiple scans per patient are allowed (example: patient has two imgs that satisfy slice thickness) otherwise only one scan per patient is chosen (with thickness closest to desired)
* *pathDatavaseImageCollection*: path to where the list of filtered img paths is saved 

03. [03_imageExtraction.py](03_imageExtraction.py)
* *inputDir*: path to nifti imgs
* *dataBasePath*: path to where the Database will be created
* *database*: name of the database to be created (defines foldername)
* *modality*: name of the img modality used
* *pathDatavaseImageCollection*: path to where the list of filtered img paths is saved 
* *patientKeyword*: defines a keyword given that indicates the location of the patient ID in the foldername of the input directory (example foldername: 0001dummy_dummyDB would use "dummy")
* *preprocessing*: if true then preprocessed imgs will be used from the filtered img list (looks for keyword "_resliced")
* *suffixToCreateDatabaseFrom*: filename suffix to identify files to convert (currently only supports "nii.gz")

### Addtional notes


