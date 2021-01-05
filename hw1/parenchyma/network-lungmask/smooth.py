import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# input CT file and mask file
maskPath = "./non-smooth/mask/"
inputPath = "../../img/"

# output smoothed mask file and output file
smoothMaskPath = "./smooth/mask/"
smoothOutputPath = './smooth/output/'

def useMask(sourcePath, mask, name):
    source = cv2.imread(sourcePath)
    height = source.shape[0]
    width = source.shape[1]

    for r in range(height):
        for c in range(width):
            if all(mask[r, c] == (0, 0, 0)):
                source[r, c] = (0, 0, 0)
    cv2.imwrite(name, source)

# Test the best smooth method
mask = cv2.imread("./non-smooth/mask/honeycombing_23.jpg_output.jpg")
kernel = np.ones((5,5),np.float32)/25
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# 2D Convolution
ffilter = cv2.filter2D(mask,-1,kernel)
# Image Blurring
blur = cv2.blur(mask,(5,5))
# Gaussian Filtering
gblur = cv2.GaussianBlur(mask,(5,5),0)
# Median Filtering
median = cv2.medianBlur(mask,5)
# Bilateral Filtering
bblur = cv2.bilateralFilter(mask,9,75,75)

cv2.imwrite("./smooth/smooth-method/filter_honeycombing_23.jpg_output.jpg", ffilter)
cv2.imwrite("./smooth/smooth-method/blur_honeycombing_23.jpg_output.jpg", blur)
cv2.imwrite("./smooth/smooth-method/gblur_honeycombing_23.jpg_output.jpg", gblur)
cv2.imwrite("./smooth/smooth-method/median_honeycombing_23.jpg_output.jpg", median)
cv2.imwrite("./smooth/smooth-method/bblur_honeycombing_23.jpg_output.jpg", bblur)


useMask("../../img/honeycombing_23.jpg", ffilter, "./smooth/smooth-method/filter_honeycombing_23.jpg_output.jpg")
useMask("../../img/honeycombing_23.jpg", blur, "./smooth/smooth-method/blur_honeycombing_23.jpg_output.jpg")
useMask("../../img/honeycombing_23.jpg", gblur, "./smooth/smooth-method/gblur_honeycombing_23.jpg_output.jpg")
useMask("../../img/honeycombing_23.jpg", median, "./smooth/smooth-method/median_honeycombing_23.jpg_output.jpg")
useMask("../../img/honeycombing_23.jpg", bblur, "./smooth/smooth-method/bblur_honeycombing_23.jpg_output.jpg")

# maskFileList = os.listdir(maskPath)
# for maskFile in maskFileList:
#     mask = cv2.imread(maskPath + maskFile)
#     median = cv2.medianBlur(mask,5)
#     cv2.imwrite(smoothMaskPath + maskFile, median)

#     inputImg = cv2.imread(inputPath + maskFile[0:-11])
#     height = inputImg.shape[0]
#     width = inputImg.shape[1]

#     for r in range(height):
#         for c in range(width):
#             if all(median[r, c] == (0, 0, 0)):
#                 inputImg[r, c] = (0, 0, 0)
#     cv2.imwrite(smoothOutputPath + maskFile[0:-11], inputImg)


# inputImg = cv2.imread("./hw1/img/honeycombing_23.jpg")

# height = inputImg.shape[0]
# width = inputImg.shape[1]

# for r in range(height):
#     for c in range(width):
#         if all(dst[r, c] == (0, 0, 0)):
#             inputImg[r, c] = (0, 0, 0)
# cv2.imwrite("./hw1/smooth/output/honeycombing_23.jpg_output.jpg", inputImg)
# print("write finished")
