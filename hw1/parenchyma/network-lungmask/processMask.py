# from lungmask import mask
import SimpleITK as sitk
import os
import cv2

maskPath = "./non-smooth/mask/"
inputPath = "../../img/"
outputPath = './non-smooth/output/'

masks = os.listdir(maskPath)
inputs = os.listdir(inputPath)

for maskFile in masks:
    inputImg = cv2.imread(inputPath + maskFile[0:-11])
    maskImg = cv2.imread(maskPath + maskFile)

    height = inputImg.shape[0]
    width = inputImg.shape[1]

    for r in range(height):
        for c in range(width):
            if all(maskImg[r, c] == (0, 0, 0)):
                inputImg[r, c] = (0, 0, 0)
    # cv2.imshow("output", inputImg)
    # print(inputImg)
    cv2.imwrite(outputPath + maskFile[0:-11], inputImg)