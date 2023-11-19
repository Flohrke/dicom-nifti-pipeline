import os
from modules.base_logger import logger
import logging
import nibabel as nib
import nibabel.processing
from modules.utility import indices


# set logging level for nipype interface
nipypeLogger = logging.getLogger("nipype.interface")
nipypeLogger.setLevel(logging.ERROR)

### Class for the convesion of images to desired formats
## currently implemented: dicom -> nifti


class ImageProcessor:
    def __init__(self, inputDirectory):
        self.inputDirectory = inputDirectory

    # returns list of all paths to files with the given suffix
    def find_images_by_suffix(self, targetSuffix):
        pathList = []
        for dirname, _, filenames in os.walk(self.inputDirectory):
            for filename in filenames:
                if targetSuffix in filename:
                    imagePath = os.path.join(dirname, filename)
                    pathList.append(imagePath)

        return list(set(pathList))
    
    def _create_processed_filename(self, imgPath):

        # prep new filename
        imgName = imgPath.split("/")[-1].split(".nii.gz")[0]
        newImgName = imgName + "_resliced.nii.gz"
        newImgPath = imgPath.split("/")[:-1]
        newPath = os.path.join("/", *newImgPath, newImgName)

        return newPath

    def reslice_resample_nifti(self, imgPath, newDims="", newVoxelDims="", setSliceNumberByDesiredThickness=False):

        try:
            # check what needs to be changed
            img = nib.load(imgPath)

            # copy list since they are mutable
            newDims = newDims.copy()
            newVoxelDims = newVoxelDims.copy()
            if len(newDims) and len(newVoxelDims) == 0:
                logger.info("-- No changed parameters were given")
                return img
            if len(newDims) == 0:
                logger.info("-- Shape dims remain unchanged")
                newDims = img.shape
            elif len(newVoxelDims) == 0:
                logger.info("-- Voxel dims remain unchanged")
                newVoxelDims = img.header.get_zooms()[:3]

            # check if any changes are only partially
            if "original" in newVoxelDims:
                idxs = indices(newVoxelDims, "original")
                for idx in idxs:
                    newVoxelDims[idx] = img.header.get_zooms()[:3][idx]
            if "original" in newDims:
                idxs = indices(newDims, "original")
                for idx in idxs:
                    newDims[idx] = img.shape[idx]

            if setSliceNumberByDesiredThickness:
                voxDimZ = img.header.get_zooms()[:3][2]
                imgShapeZ = img.shape[2]
                factor = newVoxelDims[2]/voxDimZ
                newImgShapeZ = imgShapeZ/factor
                newDims[2] = int(newImgShapeZ)

            # convert to tuple for processing
            newDims = tuple(newDims)
            newVoxelDims = tuple(newVoxelDims)
            imgName = "/".join(imgPath.split("/")[-2:])
            logger.info(f"-- Converting image: {imgName}")

            if setSliceNumberByDesiredThickness:
                logger.info("-- Slice number will be adjusted according to fit required slice thickness")
            logger.info("-- Changing Dims: \t{} -> {}".format(img.shape, newDims))

            logger.info("-- Changing Voxel Dims: {} -> {}".format(img.header.get_zooms()[:3], newVoxelDims))
            newImg = nibabel.processing.conform(img, out_shape=newDims, voxel_size=newVoxelDims)

            # check for any 0 value slices that occured due to reshaping
            data = newImg.get_fdata()
            data = data.reshape(data.shape[0] * data.shape[1], data.shape[2]).mean(axis=0).tolist()
            data = [int(x) for x in data]
            if 0 in data:
                logger.info(f"-- 0 value slices detected and will be removed")
                newImg = self._remove_grey_area(newImg)
 
            # save new img
            newPath = self._create_processed_filename(imgPath)
            logger.info(f"-- Saving new image as {newPath}")
            nib.save(newImg, newPath)
            
            return 0
        
        except Exception as e:

            return [e]

    def _remove_grey_area(self, img):

        affine = img.affine
        header = img.header
        data = img.get_fdata()
        data = data[:, : , data.reshape(data.shape[0] * data.shape[1], data.shape[2]).mean(axis=0).astype(int) < 0]
        newImg = nib.Nifti1Image(dataobj=data, affine = affine, header=header)
        return newImg
